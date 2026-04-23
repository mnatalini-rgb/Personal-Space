SELECT
  country_iso_code AS country,
  COUNT(*) AS total_users,
  COUNTIF(created_at >= TIMESTAMP('2026-04-16') AND created_at < TIMESTAMP('2026-04-23')) AS new_this_week,
  COUNTIF(created_at >= TIMESTAMP('2026-04-09') AND created_at < TIMESTAMP('2026-04-16')) AS new_last_week
FROM `business-intelligence-prod.DataMart.Users`
WHERE country_iso_code IS NOT NULL
  AND TRIM(country_iso_code) != ''
GROUP BY country_iso_code
ORDER BY total_users DESC
LIMIT 50
