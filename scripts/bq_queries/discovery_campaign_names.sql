-- =============================================================================
-- DISCOVERY: List all campaign names from last 30 days with user counts
-- Purpose: Identify which campaigns are sponsored (partner) vs internal (Premium)
--          so we can hardcode the right filter in the benchmark query.
-- Run this FIRST, then use the output to confirm campaign names.
-- =============================================================================

WITH active_campaigns AS (
  SELECT DISTINCT campaign_id
  FROM `business-intelligence-prod.CampaignService.UserMissions`
  WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
)
SELECT
  c._id AS campaign_id,
  c.name AS campaign_name,
  COUNT(DISTINCT m.user_id) AS users_with_missions
FROM `business-intelligence-prod.CampaignService.Campaigns` c
INNER JOIN active_campaigns ac ON c._id = ac.campaign_id
INNER JOIN `business-intelligence-prod.CampaignService.UserMissions` m
  ON c._id = m.campaign_id
  AND m.created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1, 2
ORDER BY users_with_missions DESC
LIMIT 30
