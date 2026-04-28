WITH player_matches AS (
  SELECT
    s.user_id,
    u.country_iso_code AS country,
    DATE(s.started_at) AS play_date
  FROM `business-intelligence-prod.dbt_user.dim__cs_ingame_player_stats` s
  JOIN `business-intelligence-prod.DataMart.Users` u
    ON s.user_id = u.user_id
  WHERE s.started_at >= TIMESTAMP('2026-04-09')
    AND s.started_at < TIMESTAMP('2026-04-23')
    AND u.country_iso_code IS NOT NULL
)
SELECT
  country,
  COUNT(DISTINCT CASE WHEN play_date >= '2026-04-16' THEN user_id END) AS players_this_week,
  COUNT(DISTINCT CASE WHEN play_date < '2026-04-16' THEN user_id END) AS players_last_week,
  COUNTIF(play_date >= '2026-04-16') AS games_this_week,
  COUNTIF(play_date < '2026-04-16') AS games_last_week
FROM player_matches
GROUP BY country
ORDER BY players_this_week DESC
LIMIT 50
