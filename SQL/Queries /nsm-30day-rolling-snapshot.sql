-- NSM 30-Day Rolling: Quick Snapshot (Current Day)
-- Returns one row per partner with the latest 30-day rolling figures.

WITH daily_value AS (
  SELECT
    [partner_column] AS partner_id,
    DATE(event_timestamp) AS day,
    [conversion_type_column] AS conversion_type,
    COUNT(*) AS conversions
  FROM `[project.dataset.conversion_events_table]`
  WHERE DATE(event_timestamp) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AND CURRENT_DATE()
  GROUP BY partner_id, day, conversion_type
),

valued AS (
  SELECT
    partner_id,
    SUM(conversions * CASE
      WHEN partner_id = 'tradeit' AND conversion_type = 'account_linkage' THEN 0.38
      WHEN partner_id = 'tradeit' AND conversion_type = 'trade_1' THEN 0.04
      WHEN partner_id = 'tradeit' AND conversion_type = 'trade_250' THEN 8.75
      WHEN partner_id = 'winline' AND conversion_type = 'account_linkage' THEN 4.33
      WHEN partner_id = 'winline' AND conversion_type = 'kyc' THEN 8.66
      WHEN partner_id = 'winline' AND conversion_type = 'first_deposit' THEN 121.10
      WHEN partner_id = 'winline' AND conversion_type = 'second_deposit' THEN 4.33
      WHEN partner_id = 'winline' AND conversion_type = 'bet' THEN 4.33
      WHEN partner_id = 'whitemarket' AND conversion_type = 'account_linkage' THEN 0.38
      WHEN partner_id = 'whitemarket' AND conversion_type = 'buy_any' THEN 0.05
      WHEN partner_id = 'whitemarket' AND conversion_type = 'buy_100' THEN 12.50
      WHEN partner_id = 'whitemarket' AND conversion_type = 'buy_300' THEN 50.00
      ELSE 0
    END) AS total_30d_value,
    SUM(conversions) AS total_30d_conversions
  FROM daily_value
  GROUP BY partner_id
),

ebu AS (
  SELECT
    [partner_column] AS partner_id,
    COUNT(DISTINCT user_id) AS ebu_30d
  FROM `[project.dataset.ebu_events_table]`
  WHERE DATE(event_timestamp) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AND CURRENT_DATE()
  GROUP BY partner_id
)

SELECT
  v.partner_id,
  v.total_30d_value,
  v.total_30d_conversions,
  e.ebu_30d,
  SAFE_DIVIDE(v.total_30d_value, e.ebu_30d) * 1000 AS eur_per_1k_ebu_30d,
  DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AS window_start,
  CURRENT_DATE() AS window_end
FROM valued v
LEFT JOIN ebu e ON v.partner_id = e.partner_id
ORDER BY total_30d_value DESC
;
