-- EE vs Traditional notification → challenge completion rates
-- Compares Engagement Engine frameworks (reward_motivation, competitive_pressure,
-- progress_completion, live_reward_rush) against standard activity notifications
-- (earn_fp, claimed_rewards_in_campaign, complete_last_mission, joined_campaign, etc.)
-- on actual mission completion, not just CTR.

WITH notification_users AS (
  SELECT
    user_id,
    entity_id AS campaign_id,
    notification_name,
    CASE
      WHEN notification_name IN (
        'reward_motivation', 'competitive_pressure',
        'progress_completion', 'live_reward_rush'
      ) THEN 'EE Framework'
      ELSE 'Traditional Activity'
    END AS notification_category,
    MAX(CASE WHEN interaction = 'click' THEN 1 ELSE 0 END) AS clicked
  FROM `faceit-events-prod-2.user.user_notification_interaction_v2`
  WHERE notification_type = 'activity'
    AND entity_type = 'CAMPAIGN'
    AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY 1, 2, 3
),

mission_status AS (
  SELECT
    user_id,
    campaign_id,
    COUNT(*) AS total_tasks,
    COUNTIF(CAST(value AS INT64) >= CAST(target AS INT64)) AS completed_tasks,
    CASE
      WHEN COUNTIF(CAST(value AS INT64) >= CAST(target AS INT64)) = COUNT(*) THEN 'all_complete'
      WHEN COUNTIF(CAST(value AS INT64) >= CAST(target AS INT64)) > 0 THEN 'partial'
      ELSE 'none'
    END AS completion_status
  FROM `business-intelligence-prod.CampaignService.UserMissions`
  GROUP BY 1, 2
),

-- Part A: Category-level (EE vs Traditional)
category_stats AS (
  SELECT
    n.notification_category,
    CASE WHEN n.clicked = 1 THEN 'Clicked' ELSE 'Impression Only' END AS cohort,
    COUNT(DISTINCT CONCAT(n.user_id, '-', n.campaign_id)) AS user_campaign_pairs,
    COUNTIF(m.completion_status IN ('partial', 'all_complete')) AS any_task_complete,
    COUNTIF(m.completion_status = 'all_complete') AS all_tasks_complete,
    ROUND(SAFE_DIVIDE(
      COUNTIF(m.completion_status IN ('partial', 'all_complete')),
      COUNT(*)
    ) * 100, 2) AS any_completion_rate,
    ROUND(SAFE_DIVIDE(
      COUNTIF(m.completion_status = 'all_complete'),
      COUNT(*)
    ) * 100, 2) AS full_completion_rate,
    ROUND(AVG(COALESCE(m.completed_tasks, 0)), 2) AS avg_tasks_completed
  FROM notification_users n
  LEFT JOIN mission_status m
    ON n.user_id = m.user_id AND n.campaign_id = m.campaign_id
  GROUP BY 1, 2
),

-- Part B: Per-framework breakdown (granular EE view)
framework_stats AS (
  SELECT
    n.notification_name AS framework,
    n.notification_category,
    CASE WHEN n.clicked = 1 THEN 'Clicked' ELSE 'Impression Only' END AS cohort,
    COUNT(*) AS user_campaign_pairs,
    COUNTIF(m.completion_status IN ('partial', 'all_complete')) AS any_task_complete,
    COUNTIF(m.completion_status = 'all_complete') AS all_tasks_complete,
    ROUND(SAFE_DIVIDE(
      COUNTIF(m.completion_status IN ('partial', 'all_complete')),
      COUNT(*)
    ) * 100, 2) AS any_completion_rate,
    ROUND(SAFE_DIVIDE(
      COUNTIF(m.completion_status = 'all_complete'),
      COUNT(*)
    ) * 100, 2) AS full_completion_rate,
    ROUND(AVG(COALESCE(m.completed_tasks, 0)), 2) AS avg_tasks_completed
  FROM notification_users n
  LEFT JOIN mission_status m
    ON n.user_id = m.user_id AND n.campaign_id = m.campaign_id
  GROUP BY 1, 2, 3
  HAVING COUNT(*) >= 50
)

-- Run Part A first, then Part B (comment/uncomment as needed)

-- PART A: High-level EE vs Traditional (already run)
-- SELECT * FROM category_stats
-- ORDER BY notification_category, cohort;

-- PART B: Per-framework detail
SELECT * FROM framework_stats
ORDER BY notification_category, framework, cohort;
