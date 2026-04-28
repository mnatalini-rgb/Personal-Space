-- =============================================================================
-- REWARDS TAB — EFFECTIVENESS BY MISSION CHALLENGE / FUNNEL STEP
-- Goal: connect reward cost to partner funnel progress so we can answer:
--   - cost per AL / C1 / C2 / C3
--   - reward efficiency by campaign
--   - value created vs reward cost using NSM € values
--
-- This file intentionally mirrors the existing campaign-pattern logic already
-- used in enrichment-dimensions-ytd.sql and the Tradeit NSM analysis.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 1 — Campaign to partner / funnel-stage mapping
-- Sanity check first. Review this output before using the later queries.
-- -----------------------------------------------------------------------------
WITH campaign_map AS (
  SELECT
    CAST(campaign_id AS STRING) AS campaign_id,
    technical_name,
    name,
    organizer_id,
    CASE
      WHEN organizer_id = '976fe92b-0998-4a2a-86a6-f655bbab8f07' THEN 'tradeit'
      WHEN organizer_id IN ('397f5239-ab93-484d-9f94-4231b0cfa48e', 'a8f12da7-d377-4b9f-aedf-a33cb1283b20', 'b5efeb75-4f23-494e-bc85-9319c1a87c75') THEN 'winline'
      WHEN organizer_id = 'db18537b-4172-4813-b089-36490c1553b7' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%' THEN 'tradeit'
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WINLINE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'KZ %' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO KYC%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %WHALE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WHITEMARKET%' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%PAYSAFE%' THEN 'paysafe'
      ELSE 'unknown'
    END AS partner,
    CASE
      -- Tradeit campaign-stage mapping
      WHEN UPPER(technical_name) LIKE 'TRADEIT GENERAL MISSION%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL & NO TRADE%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL%NO TRADE%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL & TRADE%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(technical_name) NOT LIKE '%NO TRADE%' THEN 'C2'

      -- Winline campaign-stage mapping
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE 'KZ NO AL USERS%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE '%KZ AL USERS%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%NO KYC%' THEN 'C1'
      WHEN UPPER(technical_name) LIKE '%NO FTD%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%WHALE%' THEN 'C3'
      WHEN UPPER(technical_name) LIKE '%FTD%'
           AND UPPER(technical_name) NOT LIKE '%NO FTD%' THEN 'C3'

      -- WhiteMarket mapping
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 1%NO AL%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 2%AL%NO BUY%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%' THEN 'C2'
      ELSE 'UNMAPPED'
    END AS campaign_stage
  FROM `business-intelligence-prod.dbt_user.dim__campaigns`
)
SELECT *
FROM campaign_map
ORDER BY partner, campaign_stage, technical_name;


-- -----------------------------------------------------------------------------
-- QUERY 2 — Mission completions with funnel-step mapping
-- Uses the validated campaign-stage mapping directly because the underlying
-- mission table does not expose challenge_name in the current schema.
-- -----------------------------------------------------------------------------
WITH params AS (
  SELECT DATE('2026-01-01') AS report_start, CURRENT_DATE() AS report_end
),
campaign_map AS (
  SELECT
    CAST(campaign_id AS STRING) AS campaign_id,
    technical_name,
    organizer_id,
    CASE
      WHEN organizer_id = '976fe92b-0998-4a2a-86a6-f655bbab8f07' THEN 'tradeit'
      WHEN organizer_id IN ('397f5239-ab93-484d-9f94-4231b0cfa48e', 'a8f12da7-d377-4b9f-aedf-a33cb1283b20', 'b5efeb75-4f23-494e-bc85-9319c1a87c75') THEN 'winline'
      WHEN organizer_id = 'db18537b-4172-4813-b089-36490c1553b7' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%' THEN 'tradeit'
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WINLINE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'KZ %' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO KYC%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %WHALE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WHITEMARKET%' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%PAYSAFE%' THEN 'paysafe'
      ELSE 'unknown'
    END AS partner,
    CASE
      WHEN UPPER(technical_name) LIKE 'TRADEIT GENERAL MISSION%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL & NO TRADE%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL%NO TRADE%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL & TRADE%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(technical_name) NOT LIKE '%NO TRADE%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE 'KZ NO AL USERS%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE '%KZ AL USERS%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%NO KYC%' THEN 'C1'
      WHEN UPPER(technical_name) LIKE '%NO FTD%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%WHALE%' THEN 'C3'
      WHEN UPPER(technical_name) LIKE '%FTD%'
           AND UPPER(technical_name) NOT LIKE '%NO FTD%' THEN 'C3'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 1%NO AL%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 2%AL%NO BUY%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%' THEN 'C2'
      ELSE 'UNMAPPED'
    END AS campaign_stage
  FROM `business-intelligence-prod.dbt_user.dim__campaigns`
),
mission_rows AS (
  SELECT
    DATE_TRUNC(DATE(CAST(um.created_at AS TIMESTAMP)), MONTH) AS month,
    CAST(um.campaign_id AS STRING) AS campaign_id,
    cm.partner,
    cm.technical_name,
    cm.campaign_stage,
    CAST(um.mission_id AS STRING) AS mission_id,
    COUNT(*) AS completion_events,
    COUNT(DISTINCT um.user_id) AS unique_users
  FROM `business-intelligence-prod.CampaignService.UserMissions` um
  LEFT JOIN campaign_map cm
    ON CAST(um.campaign_id AS STRING) = cm.campaign_id
  CROSS JOIN params p
  WHERE DATE(CAST(um.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
  GROUP BY 1, 2, 3, 4, 5, 6
),
step_mapped AS (
  SELECT
    month,
    campaign_id,
    partner,
    technical_name,
    mission_id,
    completion_events,
    unique_users,
    campaign_stage AS funnel_step
  FROM mission_rows
)
SELECT
  month,
  partner,
  campaign_id,
  technical_name,
  mission_id,
  funnel_step,
  completion_events,
  unique_users
FROM step_mapped
ORDER BY month, partner, technical_name, funnel_step, mission_id;


-- -----------------------------------------------------------------------------
-- QUERY 3 — Reward cost per funnel step + NSM value generated
-- This is the main output for the Rewards tab / Performance & Ops tab.
-- It combines:
--   - FP paid (actual)
--   - subscription cost (temporarily zero until UserRewards reward-kind field is validated)
--   - funnel-step completions
--   - NSM € values by partner and step
-- -----------------------------------------------------------------------------
WITH params AS (
  SELECT DATE('2026-01-01') AS report_start, CURRENT_DATE() AS report_end
),
campaign_map AS (
  SELECT
    CAST(campaign_id AS STRING) AS campaign_id,
    technical_name,
    organizer_id,
    CASE
      WHEN organizer_id = '976fe92b-0998-4a2a-86a6-f655bbab8f07' THEN 'tradeit'
      WHEN organizer_id IN ('397f5239-ab93-484d-9f94-4231b0cfa48e', 'a8f12da7-d377-4b9f-aedf-a33cb1283b20', 'b5efeb75-4f23-494e-bc85-9319c1a87c75') THEN 'winline'
      WHEN organizer_id = 'db18537b-4172-4813-b089-36490c1553b7' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%' THEN 'tradeit'
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WINLINE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'KZ %' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO KYC%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %WHALE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WHITEMARKET%' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%PAYSAFE%' THEN 'paysafe'
      ELSE 'unknown'
    END AS partner,
    CASE
      WHEN UPPER(technical_name) LIKE 'TRADEIT GENERAL MISSION%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL & NO TRADE%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL%NO TRADE%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL & TRADE%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(technical_name) NOT LIKE '%NO TRADE%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE 'KZ NO AL USERS%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE '%KZ AL USERS%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%NO KYC%' THEN 'C1'
      WHEN UPPER(technical_name) LIKE '%NO FTD%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%WHALE%' THEN 'C3'
      WHEN UPPER(technical_name) LIKE '%FTD%'
           AND UPPER(technical_name) NOT LIKE '%NO FTD%' THEN 'C3'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 1%NO AL%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 2%AL%NO BUY%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%' THEN 'C2'
      ELSE 'UNMAPPED'
    END AS campaign_stage
  FROM `business-intelligence-prod.dbt_user.dim__campaigns`
),
nsm_values AS (
  SELECT 'tradeit' AS partner, 'AL' AS funnel_step, 0.38 AS eur_value UNION ALL
  SELECT 'tradeit', 'C1', 0.04 UNION ALL
  SELECT 'tradeit', 'C2', 8.75 UNION ALL
  SELECT 'tradeit', 'C3', 35.00 UNION ALL

  SELECT 'winline', 'AL', 4.33 UNION ALL
  SELECT 'winline', 'C1', 8.66 UNION ALL
  SELECT 'winline', 'C2', 121.10 UNION ALL
  SELECT 'winline', 'C3', 4.33 UNION ALL

  SELECT 'whitemarket', 'AL', 0.38 UNION ALL
  SELECT 'whitemarket', 'C1', 0.05 UNION ALL
  SELECT 'whitemarket', 'C2', 12.50 UNION ALL
  SELECT 'whitemarket', 'C3', 50.00 UNION ALL

  SELECT 'paysafe', 'AL', 2.50 UNION ALL
  SELECT 'paysafe', 'C1', 5.00 UNION ALL
  SELECT 'paysafe', 'C2', 17.50
),
funnel_completions AS (
  SELECT
    DATE_TRUNC(DATE(CAST(um.created_at AS TIMESTAMP)), MONTH) AS month,
    CAST(um.campaign_id AS STRING) AS campaign_id,
    cm.partner,
    cm.technical_name,
    cm.campaign_stage AS funnel_step,
    COUNT(DISTINCT um.user_id) AS unique_converters
  FROM `business-intelligence-prod.CampaignService.UserMissions` um
  LEFT JOIN campaign_map cm
    ON CAST(um.campaign_id AS STRING) = cm.campaign_id
  CROSS JOIN params p
  WHERE DATE(CAST(um.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
  GROUP BY 1, 2, 3, 4, 5
),
fp_costs AS (
  SELECT
    DATE_TRUNC(DATE(t.created_at), MONTH) AS month,
    CAST(t.properties.campaign_id AS STRING) AS campaign_id,
    SUM(ABS(t.amount)) AS fp_paid_total
  FROM `business-intelligence-prod.TransactionsService.TransactionHistory` t
  CROSS JOIN params p
  WHERE t.currency = 'faceit_points'
    AND t.entity.type = 'user'
    AND DATE(t.created_at) BETWEEN p.report_start AND p.report_end
  GROUP BY 1, 2
),
subscription_costs AS (
  SELECT
    CAST(NULL AS DATE) AS month,
    CAST(NULL AS STRING) AS campaign_id,
    CAST(0 AS INT64) AS subscription_awards,
    CAST(0 AS FLOAT64) AS subscription_cost_gbp
  FROM UNNEST([]) AS _
),
campaign_costs AS (
  SELECT
    COALESCE(f.month, s.month) AS month,
    COALESCE(f.campaign_id, s.campaign_id) AS campaign_id,
    COALESCE(f.fp_paid_total, 0) AS fp_paid_total,
    COALESCE(s.subscription_awards, 0) AS subscription_awards,
    COALESCE(s.subscription_cost_gbp, 0) AS subscription_cost_gbp,
    COALESCE(f.fp_paid_total, 0) + COALESCE(s.subscription_cost_gbp, 0) AS total_reward_cost_gbp
  FROM fp_costs f
  FULL OUTER JOIN subscription_costs s
    ON f.month = s.month
   AND f.campaign_id = s.campaign_id
)
SELECT
  fc.month,
  fc.partner,
  fc.funnel_step,
  fc.campaign_id,
  fc.technical_name,
  fc.unique_converters,
  cc.fp_paid_total,
  cc.subscription_awards,
  cc.subscription_cost_gbp,
  cc.total_reward_cost_gbp,
  nv.eur_value AS nsm_eur_per_conversion,
  fc.unique_converters * COALESCE(nv.eur_value, 0) AS total_nsm_value_eur,
  SAFE_DIVIDE(cc.total_reward_cost_gbp, fc.unique_converters) AS reward_cost_per_conversion,
  SAFE_DIVIDE(fc.unique_converters * COALESCE(nv.eur_value, 0), NULLIF(cc.total_reward_cost_gbp, 0)) AS value_to_cost_ratio
FROM funnel_completions fc
LEFT JOIN campaign_costs cc
  ON fc.month = cc.month
 AND fc.campaign_id = cc.campaign_id
LEFT JOIN nsm_values nv
  ON fc.partner = nv.partner
 AND fc.funnel_step = nv.funnel_step
WHERE fc.funnel_step IS NOT NULL
  AND fc.funnel_step NOT IN ('EBU', 'UNMAPPED')
ORDER BY fc.month, fc.partner, fc.funnel_step, total_nsm_value_eur DESC;


-- -----------------------------------------------------------------------------
-- QUERY 4 — Reward effectiveness by funnel step (completion -> reward outcome)
-- Broader effectiveness view for Performance & Ops.
-- This intentionally goes beyond FP / subscriptions and looks at how mission
-- challenge completion translates into reward outcomes in UserRewards.
--
-- Core outputs:
--   - unique completers at the funnel-step level
--   - reward rows by status (completed / expired / in_progress / available ...)
--   - claim rate = completed / (completed + expired)
--   - reward rows per completer
--
-- Important caveat:
-- UserRewards does not currently expose a validated reward-kind field in our
-- runtime usage, so this query measures reward OUTCOME effectiveness, not yet
-- reward-TYPE effectiveness.
--
-- Join caveat:
-- This is a campaign-month effectiveness view. It connects mission completions
-- and reward outcomes at campaign_id + month level, which matches the main repo
-- pattern for reward reporting. It is not yet a strict per-user causal join
-- from a specific mission completion row to a specific reward row.
-- -----------------------------------------------------------------------------
WITH params AS (
  SELECT DATE('2026-01-01') AS report_start, CURRENT_DATE() AS report_end
),
campaign_map AS (
  SELECT
    CAST(campaign_id AS STRING) AS campaign_id,
    technical_name,
    organizer_id,
    CASE
      WHEN organizer_id = '976fe92b-0998-4a2a-86a6-f655bbab8f07' THEN 'tradeit'
      WHEN organizer_id IN ('397f5239-ab93-484d-9f94-4231b0cfa48e', 'a8f12da7-d377-4b9f-aedf-a33cb1283b20', 'b5efeb75-4f23-494e-bc85-9319c1a87c75') THEN 'winline'
      WHEN organizer_id = 'db18537b-4172-4813-b089-36490c1553b7' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%' THEN 'tradeit'
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WINLINE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'KZ %' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO KYC%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %WHALE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WHITEMARKET%' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%PAYSAFE%' THEN 'paysafe'
      ELSE 'unknown'
    END AS partner,
    CASE
      WHEN UPPER(technical_name) LIKE 'TRADEIT GENERAL MISSION%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL & NO TRADE%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL%NO TRADE%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL & TRADE%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(technical_name) NOT LIKE '%NO TRADE%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE 'KZ NO AL USERS%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE '%KZ AL USERS%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%NO KYC%' THEN 'C1'
      WHEN UPPER(technical_name) LIKE '%NO FTD%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%WHALE%' THEN 'C3'
      WHEN UPPER(technical_name) LIKE '%FTD%'
           AND UPPER(technical_name) NOT LIKE '%NO FTD%' THEN 'C3'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 1%NO AL%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 2%AL%NO BUY%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%' THEN 'C2'
      ELSE 'UNMAPPED'
    END AS funnel_step
  FROM `business-intelligence-prod.dbt_user.dim__campaigns`
),
mission_completions AS (
  SELECT
    DATE_TRUNC(DATE(CAST(um.created_at AS TIMESTAMP)), MONTH) AS month,
    CAST(um.campaign_id AS STRING) AS campaign_id,
    cm.partner,
    cm.technical_name,
    cm.funnel_step,
    COUNT(*) AS completion_events,
    COUNT(DISTINCT um.user_id) AS unique_completers
  FROM `business-intelligence-prod.CampaignService.UserMissions` um
  LEFT JOIN campaign_map cm
    ON CAST(um.campaign_id AS STRING) = cm.campaign_id
  CROSS JOIN params p
  WHERE DATE(CAST(um.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
  GROUP BY 1, 2, 3, 4, 5
),
reward_statuses AS (
  SELECT
    DATE_TRUNC(DATE(CAST(ur.created_at AS TIMESTAMP)), MONTH) AS month,
    CAST(ur.campaign_id AS STRING) AS campaign_id,
    LOWER(CAST(ur.status AS STRING)) AS reward_status,
    COUNT(*) AS reward_rows,
    COUNT(DISTINCT ur.user_id) AS unique_reward_users
  FROM `business-intelligence-prod.CampaignService.UserRewards` ur
  CROSS JOIN params p
  WHERE DATE(CAST(ur.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
  GROUP BY 1, 2, 3
),
reward_status_pivot AS (
  SELECT
    month,
    campaign_id,
    SUM(CASE WHEN reward_status = 'completed' THEN reward_rows ELSE 0 END) AS completed_rewards,
    SUM(CASE WHEN reward_status = 'expired' THEN reward_rows ELSE 0 END) AS expired_rewards,
    SUM(CASE WHEN reward_status = 'claimed' THEN reward_rows ELSE 0 END) AS claimed_rewards,
    SUM(CASE WHEN reward_status = 'available' THEN reward_rows ELSE 0 END) AS available_rewards,
    SUM(CASE WHEN reward_status = 'in_progress' THEN reward_rows ELSE 0 END) AS in_progress_rewards,
    SUM(CASE WHEN reward_status = 'not_started' THEN reward_rows ELSE 0 END) AS not_started_rewards,
    SUM(reward_rows) AS total_reward_rows,
    MAX(CASE WHEN reward_status = 'completed' THEN unique_reward_users ELSE 0 END) AS completed_reward_users,
    MAX(CASE WHEN reward_status = 'expired' THEN unique_reward_users ELSE 0 END) AS expired_reward_users,
    MAX(CASE WHEN reward_status = 'claimed' THEN unique_reward_users ELSE 0 END) AS claimed_reward_users,
    MAX(CASE WHEN reward_status = 'available' THEN unique_reward_users ELSE 0 END) AS available_reward_users,
    MAX(CASE WHEN reward_status = 'in_progress' THEN unique_reward_users ELSE 0 END) AS in_progress_reward_users,
    MAX(CASE WHEN reward_status = 'not_started' THEN unique_reward_users ELSE 0 END) AS not_started_reward_users
  FROM reward_statuses
  GROUP BY 1, 2
)
SELECT
  mc.month,
  mc.partner,
  mc.funnel_step,
  mc.campaign_id,
  mc.technical_name,
  mc.completion_events,
  mc.unique_completers,
  COALESCE(rp.completed_rewards, 0) AS completed_rewards,
  COALESCE(rp.expired_rewards, 0) AS expired_rewards,
  COALESCE(rp.claimed_rewards, 0) AS claimed_rewards,
  COALESCE(rp.available_rewards, 0) AS available_rewards,
  COALESCE(rp.in_progress_rewards, 0) AS in_progress_rewards,
  COALESCE(rp.not_started_rewards, 0) AS not_started_rewards,
  COALESCE(rp.total_reward_rows, 0) AS total_reward_rows,
  COALESCE(rp.completed_reward_users, 0) AS completed_reward_users,
  COALESCE(rp.expired_reward_users, 0) AS expired_reward_users,
  COALESCE(rp.claimed_reward_users, 0) AS claimed_reward_users,
  COALESCE(rp.available_reward_users, 0) AS available_reward_users,
  COALESCE(rp.in_progress_reward_users, 0) AS in_progress_reward_users,
  COALESCE(rp.not_started_reward_users, 0) AS not_started_reward_users,
  SAFE_DIVIDE(COALESCE(rp.completed_rewards, 0), NULLIF(COALESCE(rp.completed_rewards, 0) + COALESCE(rp.expired_rewards, 0), 0)) AS claim_rate_completed_vs_expired,
  SAFE_DIVIDE(
    COALESCE(rp.completed_rewards, 0) + COALESCE(rp.claimed_rewards, 0),
    NULLIF(COALESCE(rp.total_reward_rows, 0), 0)
  ) AS successful_share_of_reward_rows,
  SAFE_DIVIDE(COALESCE(rp.completed_rewards, 0), NULLIF(COALESCE(rp.total_reward_rows, 0), 0)) AS completed_share_of_reward_rows,
  SAFE_DIVIDE(COALESCE(rp.expired_rewards, 0), NULLIF(COALESCE(rp.total_reward_rows, 0), 0)) AS expired_share_of_reward_rows,
  SAFE_DIVIDE(COALESCE(rp.available_rewards, 0) + COALESCE(rp.in_progress_rewards, 0) + COALESCE(rp.not_started_rewards, 0), NULLIF(COALESCE(rp.total_reward_rows, 0), 0)) AS pending_share_of_reward_rows,
  SAFE_DIVIDE(COALESCE(rp.total_reward_rows, 0), NULLIF(mc.unique_completers, 0)) AS reward_rows_per_completer,
  SAFE_DIVIDE(COALESCE(rp.completed_reward_users, 0), NULLIF(mc.unique_completers, 0)) AS completed_reward_user_coverage,
  SAFE_DIVIDE(COALESCE(rp.expired_reward_users, 0), NULLIF(mc.unique_completers, 0)) AS expired_reward_user_coverage,
  SAFE_DIVIDE(COALESCE(rp.claimed_reward_users, 0), NULLIF(mc.unique_completers, 0)) AS claimed_reward_user_coverage
FROM mission_completions mc
LEFT JOIN reward_status_pivot rp
  ON mc.month = rp.month
 AND mc.campaign_id = rp.campaign_id
WHERE mc.funnel_step IS NOT NULL
  AND mc.funnel_step NOT IN ('EBU', 'UNMAPPED')
ORDER BY mc.month, mc.partner, mc.funnel_step, mc.unique_completers DESC;


-- -----------------------------------------------------------------------------
-- QUERY 5 — Reward effectiveness by inferred reward type
-- Live-query extension of QUERY 4.
--
-- Goal:
-- Compare reward outcome effectiveness by inferred reward type, not just by
-- partner / funnel step.
--
-- Type inference is intentionally conservative and based on runtime fields we
-- have actually seen in UserRewards and in the local reward-progress export:
--   - points present    -> faceit_points
--   - item present      -> shop_item
--   - code present      -> code_reward
--   - type field set    -> lower(type)
--   - otherwise         -> unknown
-- -----------------------------------------------------------------------------
WITH params AS (
  SELECT DATE('2026-01-01') AS report_start, CURRENT_DATE() AS report_end
),
campaign_map AS (
  SELECT
    CAST(campaign_id AS STRING) AS campaign_id,
    technical_name,
    organizer_id,
    CASE
      WHEN organizer_id = '976fe92b-0998-4a2a-86a6-f655bbab8f07' THEN 'tradeit'
      WHEN organizer_id IN ('397f5239-ab93-484d-9f94-4231b0cfa48e', 'a8f12da7-d377-4b9f-aedf-a33cb1283b20', 'b5efeb75-4f23-494e-bc85-9319c1a87c75') THEN 'winline'
      WHEN organizer_id = 'db18537b-4172-4813-b089-36490c1553b7' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%' THEN 'tradeit'
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WINLINE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'KZ %' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO KYC%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %WHALE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WHITEMARKET%' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%PAYSAFE%' THEN 'paysafe'
      ELSE 'unknown'
    END AS partner,
    CASE
      WHEN UPPER(technical_name) LIKE 'TRADEIT GENERAL MISSION%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL & NO TRADE%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL%NO TRADE%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL & TRADE%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(technical_name) NOT LIKE '%NO TRADE%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE 'KZ NO AL USERS%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE '%KZ AL USERS%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE '%NO KYC%' THEN 'C1'
      WHEN UPPER(technical_name) LIKE '%NO FTD%' THEN 'C2'
      WHEN UPPER(technical_name) LIKE '%WHALE%' THEN 'C3'
      WHEN UPPER(technical_name) LIKE '%FTD%'
           AND UPPER(technical_name) NOT LIKE '%NO FTD%' THEN 'C3'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 1%NO AL%' THEN 'EBU'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 2%AL%NO BUY%' THEN 'AL'
      WHEN UPPER(technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%' THEN 'C2'
      ELSE 'UNMAPPED'
    END AS funnel_step
  FROM `business-intelligence-prod.dbt_user.dim__campaigns`
),
mission_completions AS (
  SELECT
    DATE_TRUNC(DATE(CAST(um.created_at AS TIMESTAMP)), MONTH) AS month,
    CAST(um.campaign_id AS STRING) AS campaign_id,
    cm.partner,
    cm.technical_name,
    cm.funnel_step,
    COUNT(*) AS completion_events,
    COUNT(DISTINCT um.user_id) AS unique_completers
  FROM `business-intelligence-prod.CampaignService.UserMissions` um
  LEFT JOIN campaign_map cm
    ON CAST(um.campaign_id AS STRING) = cm.campaign_id
  CROSS JOIN params p
  WHERE DATE(CAST(um.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
  GROUP BY 1, 2, 3, 4, 5
),
reward_type_statuses AS (
  SELECT
    DATE_TRUNC(DATE(CAST(ur.created_at AS TIMESTAMP)), MONTH) AS month,
    CAST(ur.campaign_id AS STRING) AS campaign_id,
    CASE
      WHEN ur.points.amount IS NOT NULL THEN 'faceit_points'
      WHEN ur.item.id IS NOT NULL THEN 'shop_item'
      WHEN ur.code.id IS NOT NULL THEN 'code_reward'
      WHEN LOWER(CAST(ur.type AS STRING)) IS NOT NULL AND LOWER(CAST(ur.type AS STRING)) NOT IN ('', 'null') THEN LOWER(CAST(ur.type AS STRING))
      ELSE 'unknown'
    END AS inferred_reward_type,
    LOWER(CAST(ur.status AS STRING)) AS reward_status,
    COUNT(*) AS reward_rows,
    COUNT(DISTINCT ur.user_id) AS unique_reward_users
  FROM `business-intelligence-prod.CampaignService.UserRewards` ur
  CROSS JOIN params p
  WHERE DATE(CAST(ur.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
  GROUP BY 1, 2, 3, 4
),
reward_type_pivot AS (
  SELECT
    month,
    campaign_id,
    inferred_reward_type,
    SUM(CASE WHEN reward_status = 'completed' THEN reward_rows ELSE 0 END) AS completed_rewards,
    SUM(CASE WHEN reward_status = 'expired' THEN reward_rows ELSE 0 END) AS expired_rewards,
    SUM(CASE WHEN reward_status = 'claimed' THEN reward_rows ELSE 0 END) AS claimed_rewards,
    SUM(CASE WHEN reward_status = 'available' THEN reward_rows ELSE 0 END) AS available_rewards,
    SUM(CASE WHEN reward_status = 'in_progress' THEN reward_rows ELSE 0 END) AS in_progress_rewards,
    SUM(CASE WHEN reward_status = 'not_started' THEN reward_rows ELSE 0 END) AS not_started_rewards,
    SUM(CASE WHEN reward_status = 'failed' THEN reward_rows ELSE 0 END) AS failed_rewards,
    SUM(reward_rows) AS total_reward_rows,
    MAX(CASE WHEN reward_status = 'completed' THEN unique_reward_users ELSE 0 END) AS completed_reward_users,
    MAX(CASE WHEN reward_status = 'expired' THEN unique_reward_users ELSE 0 END) AS expired_reward_users,
    MAX(CASE WHEN reward_status = 'claimed' THEN unique_reward_users ELSE 0 END) AS claimed_reward_users
  FROM reward_type_statuses
  GROUP BY 1, 2, 3
)
SELECT
  mc.month,
  mc.partner,
  mc.funnel_step,
  mc.campaign_id,
  mc.technical_name,
  rtp.inferred_reward_type,
  mc.completion_events,
  mc.unique_completers,
  COALESCE(rtp.completed_rewards, 0) AS completed_rewards,
  COALESCE(rtp.expired_rewards, 0) AS expired_rewards,
  COALESCE(rtp.claimed_rewards, 0) AS claimed_rewards,
  COALESCE(rtp.available_rewards, 0) AS available_rewards,
  COALESCE(rtp.in_progress_rewards, 0) AS in_progress_rewards,
  COALESCE(rtp.not_started_rewards, 0) AS not_started_rewards,
  COALESCE(rtp.failed_rewards, 0) AS failed_rewards,
  COALESCE(rtp.total_reward_rows, 0) AS total_reward_rows,
  SAFE_DIVIDE(COALESCE(rtp.completed_rewards, 0), NULLIF(COALESCE(rtp.completed_rewards, 0) + COALESCE(rtp.expired_rewards, 0), 0)) AS claim_rate_completed_vs_expired,
  SAFE_DIVIDE(COALESCE(rtp.completed_rewards, 0) + COALESCE(rtp.claimed_rewards, 0), NULLIF(COALESCE(rtp.total_reward_rows, 0), 0)) AS successful_share_of_reward_rows,
  SAFE_DIVIDE(COALESCE(rtp.expired_rewards, 0), NULLIF(COALESCE(rtp.total_reward_rows, 0), 0)) AS expired_share_of_reward_rows,
  SAFE_DIVIDE(COALESCE(rtp.available_rewards, 0) + COALESCE(rtp.in_progress_rewards, 0) + COALESCE(rtp.not_started_rewards, 0), NULLIF(COALESCE(rtp.total_reward_rows, 0), 0)) AS pending_share_of_reward_rows,
  SAFE_DIVIDE(COALESCE(rtp.total_reward_rows, 0), NULLIF(mc.unique_completers, 0)) AS reward_rows_per_completer,
  SAFE_DIVIDE(COALESCE(rtp.completed_reward_users, 0), NULLIF(mc.unique_completers, 0)) AS completed_reward_user_coverage,
  SAFE_DIVIDE(COALESCE(rtp.expired_reward_users, 0), NULLIF(mc.unique_completers, 0)) AS expired_reward_user_coverage,
  SAFE_DIVIDE(COALESCE(rtp.claimed_reward_users, 0), NULLIF(mc.unique_completers, 0)) AS claimed_reward_user_coverage
FROM mission_completions mc
LEFT JOIN reward_type_pivot rtp
  ON mc.month = rtp.month
 AND mc.campaign_id = rtp.campaign_id
WHERE mc.funnel_step IS NOT NULL
  AND mc.funnel_step NOT IN ('EBU', 'UNMAPPED')
ORDER BY mc.month, mc.partner, mc.funnel_step, rtp.inferred_reward_type, mc.unique_completers DESC;


-- -----------------------------------------------------------------------------
-- QUERY 6 — UserRewards type-field coverage diagnostic
-- Use this when QUERY 5 returns mostly/all `unknown` inferred reward types.
-- It shows whether the runtime UserRewards table is actually populating the
-- nested fields we expected for type inference.
-- -----------------------------------------------------------------------------
WITH params AS (
  SELECT DATE('2026-01-01') AS report_start, CURRENT_DATE() AS report_end
),
campaign_map AS (
  SELECT
    CAST(campaign_id AS STRING) AS campaign_id,
    technical_name,
    organizer_id,
    CASE
      WHEN organizer_id = '976fe92b-0998-4a2a-86a6-f655bbab8f07' THEN 'tradeit'
      WHEN organizer_id IN ('397f5239-ab93-484d-9f94-4231b0cfa48e', 'a8f12da7-d377-4b9f-aedf-a33cb1283b20', 'b5efeb75-4f23-494e-bc85-9319c1a87c75') THEN 'winline'
      WHEN organizer_id = 'db18537b-4172-4813-b089-36490c1553b7' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%TRADEIT%' THEN 'tradeit'
      WHEN UPPER(technical_name) LIKE '%AGNOSTIC MISSION%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WINLINE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'KZ %' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO KYC%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %NO FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %FTD%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE 'MISSION %WHALE%' THEN 'winline'
      WHEN UPPER(technical_name) LIKE '%WHITEMARKET%' THEN 'whitemarket'
      WHEN UPPER(technical_name) LIKE '%PAYSAFE%' THEN 'paysafe'
      ELSE 'unknown'
    END AS partner
  FROM `business-intelligence-prod.dbt_user.dim__campaigns`
)
SELECT
  DATE_TRUNC(DATE(CAST(ur.created_at AS TIMESTAMP)), MONTH) AS month,
  cm.partner,
  COUNT(*) AS reward_rows,
  COUNTIF(ur.points.amount IS NOT NULL) AS rows_with_points_amount,
  COUNTIF(ur.item.id IS NOT NULL) AS rows_with_item_id,
  COUNTIF(ur.code.id IS NOT NULL) AS rows_with_code_id,
  COUNTIF(LOWER(CAST(ur.type AS STRING)) IS NOT NULL AND LOWER(CAST(ur.type AS STRING)) NOT IN ('', 'null')) AS rows_with_type_value,
  COUNTIF(LOWER(CAST(ur.status AS STRING)) = 'completed') AS completed_rows,
  COUNTIF(LOWER(CAST(ur.status AS STRING)) = 'claimed') AS claimed_rows,
  COUNTIF(LOWER(CAST(ur.status AS STRING)) = 'expired') AS expired_rows,
  COUNTIF(LOWER(CAST(ur.status AS STRING)) = 'available') AS available_rows,
  COUNTIF(LOWER(CAST(ur.status AS STRING)) = 'in_progress') AS in_progress_rows
FROM `business-intelligence-prod.CampaignService.UserRewards` ur
LEFT JOIN campaign_map cm
  ON CAST(ur.campaign_id AS STRING) = cm.campaign_id
CROSS JOIN params p
WHERE DATE(CAST(ur.created_at AS TIMESTAMP)) BETWEEN p.report_start AND p.report_end
GROUP BY 1, 2
ORDER BY month, partner;
