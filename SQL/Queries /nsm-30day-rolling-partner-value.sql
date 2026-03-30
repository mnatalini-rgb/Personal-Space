-- =============================================================================
-- NSM 30-Day Rolling: Total Partner Value & €/1K EBU
-- =============================================================================
-- Replaces weekly aggregation with a 30-day rolling window.
-- Computes daily partner value from mission completions × € conversion rates,
-- then applies a 30-day rolling SUM for a smooth, seasonality-resistant trend.
--
-- Usage: Run daily or schedule in Apps Script / BQ scheduled query.
-- Output: One row per partner per day with rolling_30d_value and rolling_30d_ebu.
-- =============================================================================

-- Step 1: Daily partner value from conversion events
WITH daily_conversions AS (
  SELECT
    DATE(event_timestamp) AS day,
    [partner_column] AS partner_id,
    [conversion_type_column] AS conversion_type,
    COUNT(*) AS conversion_count
  FROM
    `[project.dataset.conversion_events_table]`
  WHERE
    DATE(event_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)  -- 90 days to allow 30-day window with 60-day history
  GROUP BY
    day, partner_id, conversion_type
),

-- Step 2: Apply € values per conversion type per partner
-- NOTE: Update these rates when partner contracts change
daily_value AS (
  SELECT
    dc.day,
    dc.partner_id,
    dc.conversion_type,
    dc.conversion_count,
    dc.conversion_count * CASE
      -- Tradeit
      WHEN dc.partner_id = 'tradeit' AND dc.conversion_type = 'account_linkage' THEN 0.38
      WHEN dc.partner_id = 'tradeit' AND dc.conversion_type = 'trade_1' THEN 0.04
      WHEN dc.partner_id = 'tradeit' AND dc.conversion_type = 'trade_250' THEN 8.75
      -- Winline
      WHEN dc.partner_id = 'winline' AND dc.conversion_type = 'account_linkage' THEN 4.33
      WHEN dc.partner_id = 'winline' AND dc.conversion_type = 'kyc' THEN 8.66
      WHEN dc.partner_id = 'winline' AND dc.conversion_type = 'first_deposit' THEN 121.10
      WHEN dc.partner_id = 'winline' AND dc.conversion_type = 'second_deposit' THEN 4.33
      WHEN dc.partner_id = 'winline' AND dc.conversion_type = 'bet' THEN 4.33
      -- WhiteMarket
      WHEN dc.partner_id = 'whitemarket' AND dc.conversion_type = 'account_linkage' THEN 0.38
      WHEN dc.partner_id = 'whitemarket' AND dc.conversion_type = 'buy_any' THEN 0.05
      WHEN dc.partner_id = 'whitemarket' AND dc.conversion_type = 'buy_100' THEN 12.50
      WHEN dc.partner_id = 'whitemarket' AND dc.conversion_type = 'buy_300' THEN 50.00
      ELSE 0
    END AS day_value_eur
  FROM daily_conversions dc
),

-- Step 3: Aggregate to daily totals per partner
daily_partner_value AS (
  SELECT
    day,
    partner_id,
    SUM(day_value_eur) AS day_value,
    SUM(conversion_count) AS day_conversions
  FROM daily_value
  GROUP BY day, partner_id
),

-- Step 4: Daily EBU per partner (users exposed to brand activation)
daily_ebu AS (
  SELECT
    DATE(event_timestamp) AS day,
    [partner_column] AS partner_id,
    COUNT(DISTINCT user_id) AS day_ebu
  FROM
    `[project.dataset.ebu_events_table]`
  WHERE
    DATE(event_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
  GROUP BY
    day, partner_id
),

-- Step 5: Join and compute 30-day rolling windows
combined AS (
  SELECT
    COALESCE(v.day, e.day) AS day,
    COALESCE(v.partner_id, e.partner_id) AS partner_id,
    COALESCE(v.day_value, 0) AS day_value,
    COALESCE(v.day_conversions, 0) AS day_conversions,
    COALESCE(e.day_ebu, 0) AS day_ebu
  FROM daily_partner_value v
  FULL OUTER JOIN daily_ebu e
    ON v.day = e.day AND v.partner_id = e.partner_id
)

-- Step 6: Final output with rolling 30-day aggregation
SELECT
  day,
  partner_id,
  day_value,
  day_ebu,

  -- 30-day rolling Total Partner Value
  SUM(day_value) OVER (
    PARTITION BY partner_id
    ORDER BY day
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
  ) AS rolling_30d_value,

  -- 30-day rolling EBU (approximate — uses daily uniques, not deduplicated across 30 days)
  -- For exact dedup, use a separate 30-day distinct count query
  SUM(day_ebu) OVER (
    PARTITION BY partner_id
    ORDER BY day
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
  ) AS rolling_30d_ebu_approx,

  -- 30-day rolling € per 1K EBU
  SAFE_DIVIDE(
    SUM(day_value) OVER (
      PARTITION BY partner_id
      ORDER BY day
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ),
    SUM(day_ebu) OVER (
      PARTITION BY partner_id
      ORDER BY day
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    )
  ) * 1000 AS rolling_30d_eur_per_1k_ebu

FROM combined
WHERE day >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)  -- Output last 60 days of rolling values
ORDER BY partner_id, day DESC
;
