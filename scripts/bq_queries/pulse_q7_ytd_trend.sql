-- YTD weekly active users + active players trend
-- Period: 2026-01-01 to 2026-04-26, aggregated by ISO week
WITH weeks AS (
  SELECT DATE_TRUNC(day, ISOWEEK) AS week_start, user_id
  FROM `business-intelligence-prod.dbt_user.fact__daily_active_users`
  WHERE day >= '2026-01-01' AND day <= '2026-04-26'
),
player_weeks AS (
  SELECT DATE_TRUNC(day, ISOWEEK) AS week_start, user_id
  FROM `business-intelligence-prod.dbt_user.fact__daily_active_players`
  WHERE day >= '2026-01-01' AND day <= '2026-04-26'
),
au AS (
  SELECT week_start, COUNT(DISTINCT user_id) AS active_users
  FROM weeks GROUP BY week_start
),
ap AS (
  SELECT week_start, COUNT(DISTINCT user_id) AS active_players
  FROM player_weeks GROUP BY week_start
)
SELECT
  FORMAT_DATE('%Y-%m-%d', au.week_start) AS week,
  au.active_users,
  COALESCE(ap.active_players, 0) AS active_players
FROM au
LEFT JOIN ap ON au.week_start = ap.week_start
ORDER BY au.week_start
