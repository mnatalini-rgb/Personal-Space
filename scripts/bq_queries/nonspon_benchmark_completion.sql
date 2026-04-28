-- Non-sponsored mission completion benchmark
-- Compares Clicked / Impression-Only / No-Notification cohorts
-- for internal campaigns (Premium, Prestige Path, etc.)
--
-- ⚠️  Replace the campaign name filters below after running discovery_campaign_names.sql.
--     Current filters are best guesses based on known internal campaign names.

WITH notification_users AS (
  SELECT
    user_id,
    entity_id AS campaign_id,
    MAX(CASE WHEN interaction = 'click' THEN 1 ELSE 0 END) AS clicked
  FROM `faceit-events-prod-2.user.user_notification_interaction_v2`
  WHERE notification_type = 'activity'
    AND entity_type = 'CAMPAIGN'
    AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY 1, 2
),

campaign_names AS (
  SELECT _id, name
  FROM `business-intelligence-prod.CampaignService.Campaigns`
  WHERE LOWER(name) LIKE '%premium%'
     OR LOWER(name) LIKE '%prestige%'
     OR LOWER(name) LIKE '%season%path%'
     OR LOWER(name) LIKE '%beta%april%'
),

mission_status AS (
  SELECT
    m.user_id,
    m.campaign_id,
    COUNT(*) AS total_tasks,
    COUNTIF(CAST(value AS INT64) >= CAST(target AS INT64)) AS completed_tasks,
    CASE
      WHEN COUNTIF(CAST(value AS INT64) >= CAST(target AS INT64)) = COUNT(*) THEN 'all_complete'
      WHEN COUNTIF(CAST(value AS INT64) >= CAST(target AS INT64)) > 0 THEN 'partial'
      ELSE 'none'
    END AS completion_status
  FROM `business-intelligence-prod.CampaignService.UserMissions` m
  INNER JOIN campaign_names c ON m.campaign_id = c._id
  GROUP BY 1, 2
),

-- Three cohorts: Clicked, Impression Only, No Notification
cohorted AS (
  SELECT
    c.name AS campaign_name,
    m.user_id,
    m.campaign_id,
    m.total_tasks,
    m.completed_tasks,
    m.completion_status,
    CASE
      WHEN n.clicked = 1 THEN 'Clicked'
      WHEN n.clicked = 0 THEN 'Impression Only'
      ELSE 'No Notification'
    END AS cohort
  FROM mission_status m
  INNER JOIN campaign_names c ON m.campaign_id = c._id
  LEFT JOIN notification_users n
    ON m.user_id = n.user_id AND m.campaign_id = n.campaign_id
)

SELECT
  campaign_name,
  cohort,
  COUNT(*) AS users,
  COUNTIF(completion_status IN ('partial', 'all_complete')) AS any_task_complete,
  COUNTIF(completion_status = 'all_complete') AS all_tasks_complete,
  ROUND(SAFE_DIVIDE(
    COUNTIF(completion_status IN ('partial', 'all_complete')),
    COUNT(*)
  ) * 100, 2) AS any_completion_rate,
  ROUND(SAFE_DIVIDE(
    COUNTIF(completion_status = 'all_complete'),
    COUNT(*)
  ) * 100, 2) AS full_completion_rate,
  ROUND(AVG(COALESCE(completed_tasks, 0)), 2) AS avg_tasks_completed,
  ROUND(AVG(COALESCE(total_tasks, 0)), 2) AS avg_total_tasks
FROM cohorted
GROUP BY 1, 2
HAVING COUNT(*) >= 50
ORDER BY campaign_name, cohort
