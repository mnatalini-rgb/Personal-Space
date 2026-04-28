-- 30-day rolling active users (event-based, any platform interaction)
-- This period: Mar 28 – Apr 26, 2026
-- Last period: Feb 26 – Mar 27, 2026
-- Source: fact__daily_active_users (any event, not just matches)
-- Use case: Advertising — impressionable audience
SELECT
  u.country_iso_code AS country,
  COUNT(DISTINCT CASE WHEN a.day >= '2026-03-28' AND a.day <= '2026-04-26' THEN a.user_id END) AS users_this_period,
  COUNT(DISTINCT CASE WHEN a.day >= '2026-02-26' AND a.day <= '2026-03-27' THEN a.user_id END) AS users_last_period
FROM `business-intelligence-prod.dbt_user.fact__daily_active_users` a
JOIN `business-intelligence-prod.DataMart.Users` u
  ON a.user_id = u.user_id
WHERE a.day >= '2026-02-26'
  AND a.day <= '2026-04-26'
  AND u.country_iso_code IS NOT NULL
GROUP BY country
HAVING users_this_period > 0 OR users_last_period > 0
ORDER BY users_this_period DESC
LIMIT 50
