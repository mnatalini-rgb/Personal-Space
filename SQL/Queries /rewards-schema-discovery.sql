-- =============================================================================
-- REWARDS TAB — SCHEMA DISCOVERY
-- Goal: validate the source tables/columns before building reward cost +
-- funnel-step effectiveness logic.
--
-- Run each query independently in BigQuery.
-- If a dataset/table path differs in your environment, adjust the dataset name
-- but keep the same validation sequence.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 1 — CampaignService schema inventory
-- Confirms the columns available in the 3 core mission/reward tables referenced
-- in existing PM docs:
--   - business-intelligence-prod.CampaignService.UserMissions
--   - business-intelligence-prod.CampaignService.UserRewards
--   - business-intelligence-prod.CampaignService.Campaigns
-- -----------------------------------------------------------------------------
SELECT
  table_name,
  column_name,
  data_type,
  is_nullable,
  ordinal_position
FROM `business-intelligence-prod.CampaignService.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name IN ('UserMissions', 'UserRewards', 'Campaigns')
ORDER BY table_name, ordinal_position;


-- -----------------------------------------------------------------------------
-- QUERY 1B — dbt_user schema inventory (repo canonical analytics path)
-- Existing working SQL in this repo uses these tables for campaign mapping.
-- -----------------------------------------------------------------------------
SELECT
  table_name,
  column_name,
  data_type,
  is_nullable,
  ordinal_position
FROM `business-intelligence-prod.dbt_user.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name IN ('fact__user_campaign_missions', 'dim__campaigns')
ORDER BY table_name, ordinal_position;


-- -----------------------------------------------------------------------------
-- QUERY 2 — Transactions schema inventory
-- We need this because FP truth should come from transaction history rather than
-- reward-awarded fields.
--
-- If this dataset name differs, replace TransactionsService below.
-- -----------------------------------------------------------------------------
SELECT
  table_name,
  column_name,
  data_type,
  is_nullable,
  ordinal_position
FROM `business-intelligence-prod.TransactionsService.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'TransactionHistory'
ORDER BY ordinal_position;


-- -----------------------------------------------------------------------------
-- QUERY 3 — Quick sample: UserMissions
-- Validate the actual completion timestamp, mission/campaign identifiers, and
-- any challenge/task naming fields.
-- -----------------------------------------------------------------------------
SELECT *
FROM `business-intelligence-prod.CampaignService.UserMissions`
LIMIT 20;


-- -----------------------------------------------------------------------------
-- QUERY 4 — Quick sample: UserRewards
-- Validate reward typing, campaign linkage, reward status, FP amount fields,
-- and any subscription-plan fields.
-- -----------------------------------------------------------------------------
SELECT *
FROM `business-intelligence-prod.CampaignService.UserRewards`
LIMIT 20;


-- -----------------------------------------------------------------------------
-- QUERY 5 — Quick sample: Campaigns
-- Validate the campaign naming and partner/org fields used for stage mapping.
-- -----------------------------------------------------------------------------
SELECT *
FROM `business-intelligence-prod.CampaignService.Campaigns`
LIMIT 20;


-- -----------------------------------------------------------------------------
-- QUERY 6 — Quick sample: TransactionHistory filtered to FACEIT Points
-- Validate the transaction timestamp, amount sign convention, user linkage,
-- and any metadata fields that may contain campaign/reward references.
-- -----------------------------------------------------------------------------
SELECT *
FROM `business-intelligence-prod.TransactionsService.TransactionHistory`
WHERE currency = 'faceit_points'
LIMIT 50;


-- -----------------------------------------------------------------------------
-- QUERY 7 — Check nested/meta fields in FP transactions
-- Helpful when campaign_id is stored inside JSON/nested metadata rather than a
-- top-level column. Replace the selected metadata fields if needed after Query 6.
-- -----------------------------------------------------------------------------
SELECT
  created_at,
  entity.id AS user_id,
  amount,
  currency,
  entity,
  properties,
  annotations
FROM `business-intelligence-prod.TransactionsService.TransactionHistory`
WHERE currency = 'faceit_points'
LIMIT 50;


-- -----------------------------------------------------------------------------
-- QUERY 8 — Subscription signal validation from DataMart.Users
-- This does NOT give mission-awarded subscriptions by itself; it validates the
-- nested subscription structure so we know what dimensions exist.
-- -----------------------------------------------------------------------------
SELECT
  user_id,
  active_subscriptions
FROM `business-intelligence-prod.DataMart.Users`
WHERE ARRAY_LENGTH(active_subscriptions) > 0
LIMIT 20;


-- -----------------------------------------------------------------------------
-- QUERY 9 — Mission/reward join sanity check
-- Confirms that campaign_id is the correct join key between UserMissions and
-- UserRewards.
-- -----------------------------------------------------------------------------
SELECT
  um.campaign_id,
  COUNT(*) AS mission_rows,
  COUNT(ur.campaign_id) AS matched_reward_rows
FROM `business-intelligence-prod.CampaignService.UserMissions` um
LEFT JOIN `business-intelligence-prod.CampaignService.UserRewards` ur
  ON um.campaign_id = ur.campaign_id
GROUP BY um.campaign_id
ORDER BY matched_reward_rows DESC
LIMIT 50;


-- -----------------------------------------------------------------------------
-- QUERY 10 — Date-field discovery
-- Helps identify the correct event timestamp fields to use in the production
-- monthly/YTD queries.
-- -----------------------------------------------------------------------------
SELECT
  'UserMissions' AS source,
  MIN(CAST(created_at AS TIMESTAMP)) AS min_ts,
  MAX(CAST(created_at AS TIMESTAMP)) AS max_ts
FROM `business-intelligence-prod.CampaignService.UserMissions`

UNION ALL

SELECT
  'UserRewards' AS source,
  MIN(CAST(created_at AS TIMESTAMP)) AS min_ts,
  MAX(CAST(created_at AS TIMESTAMP)) AS max_ts
FROM `business-intelligence-prod.CampaignService.UserRewards`

UNION ALL

SELECT
  'TransactionHistory' AS source,
  MIN(CAST(created_at AS TIMESTAMP)) AS min_ts,
  MAX(CAST(created_at AS TIMESTAMP)) AS max_ts
FROM `business-intelligence-prod.TransactionsService.TransactionHistory`;
