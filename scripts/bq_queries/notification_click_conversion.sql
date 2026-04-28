WITH notification_users AS (
  SELECT
    user_id,
    entity_id AS campaign_id,
    MAX(CASE WHEN interaction = 'click' THEN 1 ELSE 0 END) AS clicked,
    COUNT(CASE WHEN interaction = 'impression' THEN 1 END) AS impression_count,
    COUNT(CASE WHEN interaction = 'click' THEN 1 END) AS click_count
  FROM `faceit-events-prod-2.user.user_notification_interaction_v2`
  WHERE notification_type = 'activity'
    AND entity_type = 'CAMPAIGN'
    AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY 1, 2
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
joined AS (
  SELECT
    n.campaign_id,
    n.clicked,
    m.total_tasks,
    m.completed_tasks,
    m.completion_status
  FROM notification_users n
  LEFT JOIN mission_status m
    ON n.user_id = m.user_id AND n.campaign_id = m.campaign_id
)
SELECT
  CASE WHEN clicked = 1 THEN 'Clicked Notification' ELSE 'Impression Only' END AS user_group,
  COUNT(*) AS users,
  COUNTIF(completion_status = 'all_complete') AS all_tasks_complete,
  COUNTIF(completion_status IN ('partial', 'all_complete')) AS any_task_complete,
  COUNTIF(completion_status = 'none' OR completion_status IS NULL) AS no_tasks_complete,
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
FROM joined
GROUP BY 1
ORDER BY 1
