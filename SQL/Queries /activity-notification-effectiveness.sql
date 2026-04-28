-- =============================================================================
-- ACTIVITY NOTIFICATION EFFECTIVENESS — STARTER ANALYSIS
-- Goal: measure whether activity notifications improve mission challenge
-- completion for already-engaged users, starting with the Engagement Engine
-- use case described in context/experiments.md.
--
-- IMPORTANT
-- - This file is intentionally split into schema discovery + analysis queries.
-- - Run the discovery queries first, then replace placeholder table / field names
--   in the analysis queries once the exact notification exposure source is
--   validated in your environment.
-- - Repo evidence today:
--     * context/experiments.md → Winline BOFU notification experiment
--     * docs/product_documentation/Brand Integrations Overview.md → EE sends
--       activity notifications to users stuck on mission challenges
--     * data/brand_integrations/faceit_snowflake_analytics rep__cdp_service__user_events *.csv
--       → contains a notification event row in local exports
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 1 — Schema discovery for notification exposure events
-- Use this to locate the warehouse table that stores activity / push
-- notification exposures or sends.
-- Replace the dataset if your notification events live outside faceit-events.
-- -----------------------------------------------------------------------------
SELECT
  table_name,
  column_name,
  data_type,
  is_nullable,
  ordinal_position
FROM `business-intelligence-prod.faceit-events.INFORMATION_SCHEMA.COLUMNS`
WHERE LOWER(table_name) LIKE '%notification%'
   OR LOWER(table_name) LIKE '%user_events%'
   OR LOWER(table_name) LIKE '%event%'
ORDER BY table_name, ordinal_position;


-- -----------------------------------------------------------------------------
-- QUERY 2 — Event-name discovery inside the likely CDP / user-events table
-- Replace [notification_events_table] with the best candidate from Query 1.
-- Goal: find the exact event_name / event_type used for activity notifications.
-- -----------------------------------------------------------------------------
SELECT
  LOWER(COALESCE(event_name, event_type, name, category, 'unknown')) AS event_name_guess,
  COUNT(*) AS rows
FROM `[notification_events_table]`
GROUP BY 1
ORDER BY rows DESC;


-- -----------------------------------------------------------------------------
-- QUERY 3 — Notification exposure baseline by day
-- Replace placeholders after Query 1 + 2 validation.
-- Goal: understand send volume and targeting cadence before joining to missions.
-- -----------------------------------------------------------------------------
SELECT
  DATE([event_timestamp]) AS event_date,
  COUNT(*) AS notification_events,
  COUNT(DISTINCT [user_id]) AS notified_users,
  COUNT(DISTINCT [campaign_id]) AS campaigns_touched
FROM `[notification_events_table]`
WHERE LOWER([event_name_field]) IN ('notification', 'activity_notification', 'push_notification')
  AND DATE([event_timestamp]) BETWEEN DATE('2026-01-01') AND CURRENT_DATE()
GROUP BY 1
ORDER BY 1;


-- -----------------------------------------------------------------------------
-- QUERY 4 — Mission challenge completion baseline by campaign / challenge / day
-- Reuses the canonical mission table pattern from the repo.
-- -----------------------------------------------------------------------------
WITH params AS (
  SELECT DATE('2026-01-01') AS report_start, CURRENT_DATE() AS report_end
)
SELECT
  DATE(CAST(um.created_at AS TIMESTAMP)) AS completion_date,
  CAST(um.campaign_id AS STRING) AS campaign_id,
  COUNT(*) AS completion_events,
  COUNT(DISTINCT um.user_id) AS unique_completers
FROM `business-intelligence-prod.CampaignService.UserMissions` um
CROSS JOIN params p
WHERE DATE(CAST(um.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
GROUP BY 1, 2
ORDER BY 1, 2;


-- -----------------------------------------------------------------------------
-- QUERY 5 — Notification effectiveness (treated users)
-- Replace placeholder fields once the notification source is validated.
-- This is the first real read: how many notified users completed the mission
-- challenge within the post-notification window.
-- -----------------------------------------------------------------------------
WITH params AS (
  SELECT
    DATE('2026-01-01') AS report_start,
    CURRENT_DATE() AS report_end,
    72 AS completion_window_hours
),
notification_exposure AS (
  SELECT
    [user_id] AS user_id,
    CAST([campaign_id] AS STRING) AS campaign_id,
    TIMESTAMP([event_timestamp]) AS notification_ts,
    COALESCE([variant_name], [framework_name], 'unknown') AS variant_name
  FROM `[notification_events_table]`
  CROSS JOIN params p
  WHERE LOWER([event_name_field]) IN ('notification', 'activity_notification', 'push_notification')
    AND DATE([event_timestamp]) BETWEEN p.report_start AND p.report_end
),
mission_completion AS (
  SELECT
    CAST(um.user_id AS STRING) AS user_id,
    CAST(um.campaign_id AS STRING) AS campaign_id,
    TIMESTAMP(CAST(um.created_at AS TIMESTAMP)) AS completion_ts
  FROM `business-intelligence-prod.CampaignService.UserMissions` um
  CROSS JOIN params p
  WHERE DATE(CAST(um.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
),
treated AS (
  SELECT
    ne.campaign_id,
    ne.variant_name,
    COUNT(DISTINCT ne.user_id) AS notified_users,
    COUNT(DISTINCT CASE
      WHEN mc.completion_ts BETWEEN ne.notification_ts
           AND TIMESTAMP_ADD(ne.notification_ts, INTERVAL (SELECT completion_window_hours FROM params) HOUR)
      THEN ne.user_id
    END) AS users_completed_in_window
  FROM notification_exposure ne
  LEFT JOIN mission_completion mc
    ON ne.user_id = mc.user_id
   AND ne.campaign_id = mc.campaign_id
  GROUP BY 1, 2
)
SELECT
  campaign_id,
  variant_name,
  notified_users,
  users_completed_in_window,
  SAFE_DIVIDE(users_completed_in_window, notified_users) AS completion_rate_after_notification
FROM treated
ORDER BY notified_users DESC, campaign_id, variant_name;


-- -----------------------------------------------------------------------------
-- QUERY 6 — Notification uplift vs non-notified users in the same campaign
-- This gives the practical PM read: do notified users complete more often than
-- comparable active campaign users who were not notified?
-- -----------------------------------------------------------------------------
WITH params AS (
  SELECT
    DATE('2026-01-01') AS report_start,
    CURRENT_DATE() AS report_end,
    72 AS completion_window_hours
),
notification_exposure AS (
  SELECT DISTINCT
    [user_id] AS user_id,
    CAST([campaign_id] AS STRING) AS campaign_id,
    TIMESTAMP([event_timestamp]) AS notification_ts,
    COALESCE([variant_name], [framework_name], 'unknown') AS variant_name
  FROM `[notification_events_table]`
  CROSS JOIN params p
  WHERE LOWER([event_name_field]) IN ('notification', 'activity_notification', 'push_notification')
    AND DATE([event_timestamp]) BETWEEN p.report_start AND p.report_end
),
campaign_population AS (
  SELECT DISTINCT
    CAST(um.user_id AS STRING) AS user_id,
    CAST(um.campaign_id AS STRING) AS campaign_id,
    TIMESTAMP(CAST(um.created_at AS TIMESTAMP)) AS activity_ts
  FROM `business-intelligence-prod.CampaignService.UserMissions` um
  CROSS JOIN params p
  WHERE DATE(CAST(um.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
),
completion_events AS (
  SELECT DISTINCT
    CAST(um.user_id AS STRING) AS user_id,
    CAST(um.campaign_id AS STRING) AS campaign_id,
    TIMESTAMP(CAST(um.created_at AS TIMESTAMP)) AS completion_ts
  FROM `business-intelligence-prod.CampaignService.UserMissions` um
  CROSS JOIN params p
  WHERE DATE(CAST(um.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
),
treated AS (
  SELECT
    ne.campaign_id,
    ne.variant_name,
    COUNT(DISTINCT ne.user_id) AS users,
    COUNT(DISTINCT CASE
      WHEN ce.completion_ts BETWEEN ne.notification_ts
           AND TIMESTAMP_ADD(ne.notification_ts, INTERVAL (SELECT completion_window_hours FROM params) HOUR)
      THEN ne.user_id
    END) AS completers
  FROM notification_exposure ne
  LEFT JOIN completion_events ce
    ON ne.user_id = ce.user_id
   AND ne.campaign_id = ce.campaign_id
  GROUP BY 1, 2
),
control AS (
  SELECT
    cp.campaign_id,
    'not_notified' AS variant_name,
    COUNT(DISTINCT cp.user_id) AS users,
    COUNT(DISTINCT ce.user_id) AS completers
  FROM campaign_population cp
  LEFT JOIN notification_exposure ne
    ON cp.user_id = ne.user_id
   AND cp.campaign_id = ne.campaign_id
  LEFT JOIN completion_events ce
    ON cp.user_id = ce.user_id
   AND cp.campaign_id = ce.campaign_id
  WHERE ne.user_id IS NULL
  GROUP BY 1, 2
),
combined AS (
  SELECT * FROM treated
  UNION ALL
  SELECT * FROM control
)
SELECT
  campaign_id,
  variant_name,
  users,
  completers,
  SAFE_DIVIDE(completers, users) AS completion_rate,
  completion_rate - MAX(IF(variant_name = 'not_notified', completion_rate, NULL)) OVER (PARTITION BY campaign_id) AS absolute_uplift_vs_control
FROM (
  SELECT
    campaign_id,
    variant_name,
    users,
    completers,
    SAFE_DIVIDE(completers, users) AS completion_rate
  FROM combined
)
ORDER BY campaign_id, variant_name;


-- -----------------------------------------------------------------------------
-- QUERY 7 — Convert notification uplift into € value using NSM rates
-- Uses the same partner-level euro-per-conversion rates already used elsewhere
-- in this repo. Replace the campaign→partner mapping if needed.
-- -----------------------------------------------------------------------------
WITH nsm_values AS (
  SELECT 'tradeit' AS partner, 8.75 AS eur_value_c2 UNION ALL
  SELECT 'winline', 121.10 UNION ALL
  SELECT 'whitemarket', 12.50 UNION ALL
  SELECT 'paysafe', 17.50
),
uplift AS (
  -- Replace this SELECT with the output of QUERY 6 once variant / control is validated
  SELECT
    '[campaign_id]' AS campaign_id,
    'winline' AS partner,
    'progress_completion' AS variant_name,
    0.0020 AS absolute_uplift_vs_control,
    10000 AS eligible_users
)
SELECT
  campaign_id,
  partner,
  variant_name,
  absolute_uplift_vs_control,
  eligible_users,
  absolute_uplift_vs_control * eligible_users AS incremental_completers,
  (absolute_uplift_vs_control * eligible_users) * eur_value_c2 AS incremental_nsm_value_eur
FROM uplift u
LEFT JOIN nsm_values nv
  ON u.partner = nv.partner;
