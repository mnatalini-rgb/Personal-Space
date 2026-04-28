WITH notification_users AS (
  SELECT
    n.user_id,
    n.entity_id AS campaign_id,
    MAX(CASE WHEN n.interaction = 'click' THEN 1 ELSE 0 END) AS clicked,
    COUNT(CASE WHEN n.interaction = 'impression' THEN 1 END) AS impression_count,
    COUNT(CASE WHEN n.interaction = 'click' THEN 1 END) AS click_count
  FROM `faceit-events-prod-2.user.user_notification_interaction_v2` n
  WHERE n.notification_type = 'activity'
    AND n.entity_type = 'CAMPAIGN'
    AND n.event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY 1, 2
),
campaign_names AS (
  SELECT _id, name
  FROM `business-intelligence-prod.CampaignService.Campaigns`
),
mission_status AS (
  SELECT
    user_id,
    campaign_id,
    COUNT(*) AS total_tasks,
    COUNTIF(CAST(value AS INT64) >= CAST(target AS INT64)) AS completed_tasks
  FROM `business-intelligence-prod.CampaignService.UserMissions`
  GROUP BY 1, 2
),
joined AS (
  SELECT
    n.campaign_id,
    c.name AS campaign_name,
    CASE WHEN n.clicked = 1 THEN 'Clicked' ELSE 'Impression Only' END AS user_group,
    COALESCE(m.completed_tasks, 0) AS completed_tasks,
    COALESCE(m.total_tasks, 0) AS total_tasks,
    CASE
      WHEN COALESCE(m.completed_tasks, 0) > 0 THEN 1 ELSE 0
    END AS has_any_completion
  FROM notification_users n
  LEFT JOIN campaign_names c ON n.campaign_id = c._id
  LEFT JOIN mission_status m ON n.user_id = m.user_id AND n.campaign_id = m.campaign_id
)
SELECT
  campaign_name,
  user_group,
  COUNT(*) AS users,
  SUM(has_any_completion) AS users_with_completion,
  ROUND(SAFE_DIVIDE(SUM(has_any_completion), COUNT(*)) * 100, 2) AS completion_rate,
  ROUND(AVG(completed_tasks), 2) AS avg_tasks_done,
  ROUND(AVG(total_tasks), 2) AS avg_total_tasks
FROM joined
GROUP BY 1, 2
HAVING COUNT(*) >= 100
ORDER BY campaign_name, user_group
