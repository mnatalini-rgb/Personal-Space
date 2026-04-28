SELECT
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
  AND notification_name IN (
    'earn_fp',
    'claimed_rewards_in_campaign',
    'complete_last_mission',
    'shop_order_expiration_reminder',
    'reward_not_claimed_reminder'
  )
  AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1
ORDER BY user_ctr DESC
