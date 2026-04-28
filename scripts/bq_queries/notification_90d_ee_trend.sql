SELECT
  DATE_TRUNC(DATE(event_timestamp), WEEK(MONDAY)) AS week_start,
  notification_name,
  COUNT(CASE WHEN interaction = 'impression' THEN 1 END) AS impressions,
  COUNT(CASE WHEN interaction = 'click' THEN 1 END) AS clicks,
  ROUND(SAFE_DIVIDE(
    COUNT(CASE WHEN interaction = 'click' THEN 1 END),
    COUNT(CASE WHEN interaction = 'impression' THEN 1 END)
  ) * 100, 2) AS event_ctr,
  COUNT(DISTINCT CASE WHEN interaction = 'impression' THEN user_id END) AS users_impressed,
  COUNT(DISTINCT CASE WHEN interaction = 'click' THEN user_id END) AS users_clicked,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN interaction = 'click' THEN user_id END),
    COUNT(DISTINCT CASE WHEN interaction = 'impression' THEN user_id END)
  ) * 100, 2) AS user_ctr
FROM `faceit-events-prod-2.user.user_notification_interaction_v2`
WHERE notification_type = 'activity'
  AND entity_type = 'CAMPAIGN'
  AND notification_name IN (
    'live_reward_rush', 'progress_completion',
    'reward_motivation', 'competitive_pressure'
  )
  AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY 1, 2
ORDER BY notification_name, week_start
