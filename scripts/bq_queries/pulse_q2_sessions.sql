WITH sessions AS (
  SELECT
    country,
    DATE(event_timestamp) AS session_date
  FROM `faceit-events-prod-2.user.new_tracking_session_v1`
  WHERE event_timestamp >= TIMESTAMP('2026-04-13')
    AND event_timestamp < TIMESTAMP('2026-04-27')
    AND country IS NOT NULL
    AND TRIM(country) != ''
)
SELECT
  country,
  COUNTIF(session_date >= '2026-04-20') AS sessions_this_week,
  COUNTIF(session_date < '2026-04-20') AS sessions_last_week
FROM sessions
GROUP BY country
ORDER BY sessions_this_week DESC
LIMIT 50
