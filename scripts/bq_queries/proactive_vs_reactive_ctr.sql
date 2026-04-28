WITH categorized AS (
  SELECT
    CASE
      WHEN notification_name IN ('earn_fp', 'claimed_rewards_in_campaign', 'complete_last_mission') THEN 'Re-engagement (proactive)'
      WHEN notification_name IN ('shop_order_expiration_reminder', 'reward_not_claimed_reminder') THEN 'Reward reminder (time-delayed)'
      WHEN notification_name LIKE 'user_joined%' THEN 'Join moment (reactive)'
      WHEN notification_name LIKE '%completed%' OR notification_name LIKE 'shop_order_created%' OR notification_name LIKE 'mission_completed%' THEN 'Task completion (reactive)'
      WHEN notification_name LIKE '%claimed%' THEN 'Reward claim (reactive)'
      ELSE 'Other'
    END AS category,
    interaction,
    user_id
  FROM `faceit-events-prod-2.user.user_notification_interaction_v2`
  WHERE notification_type = 'activity'
    AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
)
SELECT
  category,
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
FROM categorized
GROUP BY 1
ORDER BY user_ctr DESC
