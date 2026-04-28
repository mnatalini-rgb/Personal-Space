-- 30-day rolling active players (match-based) with geo breakdown
-- This period: Mar 28 – Apr 26, 2026
-- Last period: Feb 26 – Mar 27, 2026
-- Source: fact__daily_active_players (pre-aggregated match participation)
SELECT
  u.country_iso_code AS country,
  COUNT(DISTINCT CASE WHEN p.day >= '2026-03-28' AND p.day <= '2026-04-26' THEN p.user_id END) AS active_this_period,
  COUNT(DISTINCT CASE WHEN p.day >= '2026-02-26' AND p.day <= '2026-03-27' THEN p.user_id END) AS active_last_period
FROM `business-intelligence-prod.dbt_user.fact__daily_active_players` p
JOIN `business-intelligence-prod.DataMart.Users` u
  ON p.user_id = u.user_id
WHERE p.day >= '2026-02-26'
  AND p.day <= '2026-04-26'
  AND u.country_iso_code IS NOT NULL
GROUP BY country
HAVING active_this_period > 0 OR active_last_period > 0
ORDER BY active_this_period DESC
LIMIT 50
