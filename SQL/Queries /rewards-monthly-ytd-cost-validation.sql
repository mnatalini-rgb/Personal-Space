-- =============================================================================
-- REWARDS TAB — MONTHLY + YTD COST VALIDATION
-- Goal: produce a clean reward-cost view per partner with a split between:
--   1) FACEIT Points actually paid (source of truth = TransactionHistory)
--   2) Premium subscriptions awarded (requires subscription unit pricing)
--   3) Combined monthly and YTD total
--
-- IMPORTANT
-- - Use this after confirming the exact column names via rewards-schema-discovery.sql
-- - Adjust metadata extraction if campaign_id is nested inside meta/entity fields
-- - Replace subscription unit prices below with Finance-confirmed values
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 1 — Monthly FP paid by partner
-- Uses actual credited FP transactions, not faceit_points_awarded.
-- Assumption: FP payouts are negative amounts in TransactionHistory.
-- If your environment stores payouts as positive values, remove ABS().
-- -----------------------------------------------------------------------------
WITH params AS (
  SELECT DATE('2026-01-01') AS report_start, CURRENT_DATE() AS report_end
),
fp_transactions AS (
  SELECT
    DATE_TRUNC(DATE(t.created_at), MONTH) AS month,
    CAST(t.properties.campaign_id AS STRING) AS campaign_id,
    t.entity.id AS user_id,
    ABS(t.amount) AS fp_paid
  FROM `business-intelligence-prod.TransactionsService.TransactionHistory` t
  CROSS JOIN params p
  WHERE t.currency = 'faceit_points'
    AND t.entity.type = 'user'
    AND DATE(t.created_at) BETWEEN p.report_start AND p.report_end
),
campaign_map AS (
  SELECT
    CAST(campaign_id AS STRING) AS campaign_id,
    organizer_id AS partner_key,
    technical_name,
    name
  FROM `business-intelligence-prod.dbt_user.dim__campaigns`
),
fp_by_partner AS (
  SELECT
    ft.month,
    CASE
      WHEN cm.partner_key = '976fe92b-0998-4a2a-86a6-f655bbab8f07' THEN 'tradeit'
      WHEN cm.partner_key IN ('397f5239-ab93-484d-9f94-4231b0cfa48e', 'a8f12da7-d377-4b9f-aedf-a33cb1283b20', 'b5efeb75-4f23-494e-bc85-9319c1a87c75') THEN 'winline'
      WHEN cm.partner_key = 'db18537b-4172-4813-b089-36490c1553b7' THEN 'whitemarket'
      WHEN UPPER(cm.technical_name) LIKE '%TRADEIT%' THEN 'tradeit'
      WHEN UPPER(cm.technical_name) LIKE '%WINLINE%' OR UPPER(cm.technical_name) LIKE '%AGNOSTIC MISSION%' OR UPPER(cm.technical_name) LIKE 'KZ %' THEN 'winline'
      WHEN UPPER(cm.technical_name) LIKE 'MISSION %NO KYC%' THEN 'winline'
      WHEN UPPER(cm.technical_name) LIKE 'MISSION %NO FTD%' THEN 'winline'
      WHEN UPPER(cm.technical_name) LIKE 'MISSION %FTD%' THEN 'winline'
      WHEN UPPER(cm.technical_name) LIKE 'MISSION %WHALE%' THEN 'winline'
      WHEN UPPER(cm.technical_name) LIKE '%WHITEMARKET%' THEN 'whitemarket'
      WHEN UPPER(cm.technical_name) LIKE '%PAYSAFE%' THEN 'paysafe'
      ELSE LOWER(COALESCE(cm.partner_key, 'unknown'))
    END AS partner,
    SUM(ft.fp_paid) AS fp_paid_total
  FROM fp_transactions ft
  LEFT JOIN campaign_map cm
    ON ft.campaign_id = cm.campaign_id
  GROUP BY 1, 2
)
SELECT
  month,
  partner,
  fp_paid_total
FROM fp_by_partner
ORDER BY month, partner;


-- -----------------------------------------------------------------------------
-- QUERY 2 — Monthly subscription awards by partner
-- This assumes subscriptions are recorded in CampaignService.UserRewards.
-- We have validated `status` on UserRewards, but not a reliable field that
-- identifies which rewards are subscriptions. Use rewards-schema-discovery.sql
-- QUERY 4 to inspect runtime columns before enabling this again.
-- -----------------------------------------------------------------------------
SELECT
  'TODO_VALIDATE_USERREWARDS_SUBSCRIPTION_FIELD' AS status,
  'Run rewards-schema-discovery.sql QUERY 4 and identify the runtime column that distinguishes premium subscription rewards from FP/item rewards.' AS next_step,
  'Validated UserRewards fields so far from repo/runtime evidence: created_at, campaign_id, user_id, status.' AS notes;


-- -----------------------------------------------------------------------------
-- QUERY 3 — Combined monthly reward cost (FP + subscriptions) with YTD rollup
-- Produces the shape needed for the Rewards tab summary layer.
-- -----------------------------------------------------------------------------
WITH params AS (
  SELECT DATE('2026-01-01') AS report_start, CURRENT_DATE() AS report_end
),
campaign_map AS (
  SELECT
    CAST(campaign_id AS STRING) AS campaign_id,
    technical_name,
    organizer_id AS partner_key
  FROM `business-intelligence-prod.dbt_user.dim__campaigns`
  WHERE organizer_id IN (
    '976fe92b-0998-4a2a-86a6-f655bbab8f07',
    '397f5239-ab93-484d-9f94-4231b0cfa48e',
    'a8f12da7-d377-4b9f-aedf-a33cb1283b20',
    'b5efeb75-4f23-494e-bc85-9319c1a87c75',
    'db18537b-4172-4813-b089-36490c1553b7'
  )
),
fp_transactions AS (
  SELECT
    DATE_TRUNC(DATE(t.created_at), MONTH) AS month,
    CAST(t.properties.campaign_id AS STRING) AS campaign_id,
    ABS(t.amount) AS fp_paid
  FROM `business-intelligence-prod.TransactionsService.TransactionHistory` t
  JOIN campaign_map cm
    ON CAST(t.properties.campaign_id AS STRING) = cm.campaign_id
  CROSS JOIN params p
  WHERE t.currency = 'faceit_points'
    AND t.entity.type = 'user'
    AND DATE(t.created_at) BETWEEN p.report_start AND p.report_end
),
fp_monthly AS (
  SELECT
    ft.month,
    CASE
      WHEN cm.partner_key = '976fe92b-0998-4a2a-86a6-f655bbab8f07' THEN 'tradeit'
      WHEN cm.partner_key IN ('397f5239-ab93-484d-9f94-4231b0cfa48e', 'a8f12da7-d377-4b9f-aedf-a33cb1283b20', 'b5efeb75-4f23-494e-bc85-9319c1a87c75') THEN 'winline'
      WHEN cm.partner_key = 'db18537b-4172-4813-b089-36490c1553b7' THEN 'whitemarket'
      WHEN UPPER(cm.technical_name) LIKE '%TRADEIT%' THEN 'tradeit'
      WHEN UPPER(cm.technical_name) LIKE '%WINLINE%' OR UPPER(cm.technical_name) LIKE '%AGNOSTIC MISSION%' OR UPPER(cm.technical_name) LIKE 'KZ %' THEN 'winline'
      WHEN UPPER(cm.technical_name) LIKE 'MISSION %NO KYC%' THEN 'winline'
      WHEN UPPER(cm.technical_name) LIKE 'MISSION %NO FTD%' THEN 'winline'
      WHEN UPPER(cm.technical_name) LIKE 'MISSION %FTD%' THEN 'winline'
      WHEN UPPER(cm.technical_name) LIKE 'MISSION %WHALE%' THEN 'winline'
      WHEN UPPER(cm.technical_name) LIKE '%WHITEMARKET%' THEN 'whitemarket'
      WHEN UPPER(cm.technical_name) LIKE '%PAYSAFE%' THEN 'paysafe'
      ELSE LOWER(COALESCE(cm.partner_key, 'unknown'))
    END AS partner,
    SUM(ft.fp_paid) AS fp_paid_total
  FROM fp_transactions ft
  LEFT JOIN campaign_map cm
    ON ft.campaign_id = cm.campaign_id
  GROUP BY 1, 2
),
subscription_monthly AS (
  SELECT
    CAST(NULL AS DATE) AS month,
    CAST(NULL AS STRING) AS partner,
    CAST(0 AS INT64) AS subscription_awards,
    CAST(0 AS FLOAT64) AS subscription_cost_gbp
  FROM UNNEST([]) AS _
),
monthly_costs AS (
  SELECT
    frame.month,
    frame.partner,
    COALESCE(f.fp_paid_total, 0) AS fp_paid_total,
    COALESCE(s.subscription_awards, 0) AS subscription_awards,
    COALESCE(s.subscription_cost_gbp, 0) AS subscription_cost_gbp,
    COALESCE(f.fp_paid_total, 0) + COALESCE(s.subscription_cost_gbp, 0) AS total_reward_cost_gbp
  FROM (
    SELECT month, partner
    FROM UNNEST(GENERATE_DATE_ARRAY(DATE('2026-01-01'), DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)) AS month
    CROSS JOIN UNNEST(['tradeit', 'winline', 'whitemarket']) AS partner
  ) frame
  LEFT JOIN fp_monthly f
    ON frame.month = f.month
   AND frame.partner = f.partner
  LEFT JOIN subscription_monthly s
    ON frame.month = s.month
   AND frame.partner = s.partner
)
SELECT
  month,
  partner,
  fp_paid_total,
  subscription_awards,
  subscription_cost_gbp,
  total_reward_cost_gbp,
  SUM(total_reward_cost_gbp) OVER (
    PARTITION BY partner
    ORDER BY month
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS ytd_reward_cost_gbp
FROM monthly_costs
ORDER BY month, partner;
