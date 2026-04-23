SELECT
  country,
  COUNT(DISTINCT CASE WHEN event_timestamp >= TIMESTAMP("2026-04-16") AND event_timestamp < TIMESTAMP("2026-04-23") THEN user_id END) as wau_this_week,
  COUNT(DISTINCT CASE WHEN event_timestamp >= TIMESTAMP("2026-04-09") AND event_timestamp < TIMESTAMP("2026-04-16") THEN user_id END) as wau_last_week
FROM `faceit-events-prod-2.user.new_tracking_session_v1`
WHERE event_timestamp >= TIMESTAMP("2026-04-09") AND event_timestamp < TIMESTAMP("2026-04-23")
  AND user_id IS NOT NULL
  AND user_id != ''
GROUP BY country
HAVING wau_this_week > 0 OR wau_last_week > 0
ORDER BY wau_this_week DESC
LIMIT 50
