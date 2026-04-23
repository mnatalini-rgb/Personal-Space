SELECT
  region,
  game,
  COUNTIF(created_at >= TIMESTAMP("2026-04-16") AND created_at < TIMESTAMP("2026-04-23")) as matches_this_week,
  COUNTIF(created_at >= TIMESTAMP("2026-04-09") AND created_at < TIMESTAMP("2026-04-16")) as matches_last_week
FROM `business-intelligence-prod.DataMart.Matches`
WHERE created_at >= TIMESTAMP("2026-04-09") AND created_at < TIMESTAMP("2026-04-23")
  AND state = 'finished'
GROUP BY region, game
HAVING matches_this_week > 0 OR matches_last_week > 0
ORDER BY matches_this_week DESC
LIMIT 50
