-- =============================================================================
-- ENRICHMENT DIMENSIONS — 5 New Data Points for All Funnel Stages
-- Period: YTD 2026-01-01 to 2026-03-31
-- Partners: Combined (all), Tradeit, Winline, WhiteMarket
-- =============================================================================
--
-- SCHEMA VERIFIED:
--   fact__user_campaign_missions: user_id, campaign_id, created_at, mission_id,
--     user_mission_status, user_mission_progress, etc.
--   dim__campaigns: campaign_id, technical_name, name, status, organizer_id
--
-- Campaign → Stage mapping (verified from BQ data):
--   TRADEIT GENERAL MISSION*              → tradeit / EBU
--   TRADEIT*AL & NO TRADE*                → tradeit / AL
--   TRADEIT*AL & TRADE*                   → tradeit / C2
--   *AGNOSTIC MISSION*                    → winline / EBU
--   KZ NO AL USERS*                       → winline / EBU
--   *KZ AL USERS*                         → winline / AL
--   *NO KYC*  (excl test)                 → winline / C1
--   *NO FTD*  (excl test)                 → winline / FTD
--   *FTD* (not NO FTD, not test)          → winline / Bet
--   *WHALE*                               → winline / Bet
--   WHITEMARKET MISSION 1*NO AL*          → whitemarket / EBU
--   WHITEMARKET MISSION 2*AL*NO BUY*      → whitemarket / AL
--   WHITEMARKET MISSION 3*AL*BUY*         → whitemarket / C2
-- =============================================================================


-- =============================================================================
-- QUERY 1: Geographic Distribution per Stage per Partner
--
-- Returns: partner, funnel_stage, country, user_count, pct_of_stage
-- Card type: Horizontal bar chart (top 10 countries per stage)
-- =============================================================================

WITH stage_users AS (
  SELECT DISTINCT
    ucm.user_id,
    CASE
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%'                            THEN 'tradeit'
      WHEN UPPER(c.technical_name) LIKE '%AGNOSTIC%'                           THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%WINLINE%'                            THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'KZ %'                                THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'MISSION %'
           AND (UPPER(c.technical_name) LIKE '%NO KYC%'
                OR UPPER(c.technical_name) LIKE '%NO FTD%'
                OR UPPER(c.technical_name) LIKE '%FTD%'
                OR UPPER(c.technical_name) LIKE '%WHALE%')                     THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%WHITEMARKET%'                        THEN 'whitemarket'
      ELSE NULL
    END AS partner,
    CASE
      -- Tradeit
      WHEN UPPER(c.technical_name) LIKE 'TRADEIT GENERAL MISSION%'             THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & NO TRADE%'              THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%NO TRADE%'                THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & TRADE%'                 THEN 'C2'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(c.technical_name) NOT LIKE '%NO TRADE%'                   THEN 'C2'
      -- Winline EBU
      WHEN UPPER(c.technical_name) LIKE '%AGNOSTIC MISSION%'                   THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE 'KZ NO AL USERS%'                     THEN 'EBU'
      -- Winline AL
      WHEN UPPER(c.technical_name) LIKE '%KZ AL USERS%'                       THEN 'AL'
      -- Winline C1 (NO KYC)
      WHEN UPPER(c.technical_name) LIKE '%NO KYC%'                            THEN 'C1'
      -- Winline FTD stage (NO FTD = users who haven't deposited yet)
      WHEN UPPER(c.technical_name) LIKE '%NO FTD%'                            THEN 'FTD'
      -- Winline Bet (BOFU): FTD missions (users who HAVE deposited) + WHALE
      WHEN UPPER(c.technical_name) LIKE '%WHALE%'                             THEN 'Bet'
      WHEN UPPER(c.technical_name) LIKE '%FTD%'
           AND UPPER(c.technical_name) NOT LIKE '%NO FTD%'                     THEN 'Bet'
      -- WhiteMarket
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 1%NO AL%'        THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 2%AL%NO BUY%'    THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%'       THEN 'C2'
      ELSE NULL
    END AS funnel_stage
  FROM `business-intelligence-prod.dbt_user.fact__user_campaign_missions` ucm
  JOIN `business-intelligence-prod.dbt_user.dim__campaigns` c
    ON ucm.campaign_id = c.campaign_id
  WHERE ucm.created_at >= TIMESTAMP('2026-01-01')
    AND ucm.created_at <  TIMESTAMP('2026-04-01')
    -- Exclude non-partner campaigns
    AND UPPER(c.technical_name) NOT LIKE '%5-STACK%'
    AND UPPER(c.technical_name) NOT LIKE '%PREMIUM MONTHLY%'
    AND UPPER(c.technical_name) NOT LIKE '%FACEIT WEEKLY%'
    AND UPPER(c.technical_name) NOT LIKE '%COUNTER-STRIKE COUNTDOWN%'
),

geo_data AS (
  SELECT
    su.partner,
    su.funnel_stage,
    IFNULL(u.country_iso_code, 'UNKNOWN') AS country,
    COUNT(DISTINCT su.user_id) AS user_count
  FROM stage_users su
  JOIN `business-intelligence-prod.DataMart.Users` u
    ON su.user_id = u.user_id
  WHERE su.funnel_stage IS NOT NULL
    AND su.partner IS NOT NULL
  GROUP BY su.partner, su.funnel_stage, u.country_iso_code
),

stage_totals AS (
  SELECT partner, funnel_stage, SUM(user_count) AS total
  FROM geo_data
  GROUP BY partner, funnel_stage
)

SELECT
  g.partner,
  g.funnel_stage,
  g.country,
  g.user_count,
  ROUND(100.0 * g.user_count / t.total, 1) AS pct_of_stage,
  t.total AS stage_total
FROM geo_data g
JOIN stage_totals t
  ON g.partner = t.partner AND g.funnel_stage = t.funnel_stage
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY g.partner, g.funnel_stage
  ORDER BY g.user_count DESC
) <= 10
ORDER BY g.partner, g.funnel_stage, g.user_count DESC;


-- =============================================================================
-- QUERY 2: Match Activity (30d) per Stage per Partner
--
-- Returns: partner, funnel_stage, activity_bucket, user_count, pct, stage_avg
-- Buckets: 0 matches, 1-5, 6-15, 16-30, 31-50, 50+
-- Card type: Horizontal bar chart + avg matches KPI
-- =============================================================================

WITH stage_users AS (
  SELECT DISTINCT
    ucm.user_id,
    CASE
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%'                            THEN 'tradeit'
      WHEN UPPER(c.technical_name) LIKE '%AGNOSTIC%'                           THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%WINLINE%'                            THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'KZ %'                                THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'MISSION %'
           AND (UPPER(c.technical_name) LIKE '%NO KYC%'
                OR UPPER(c.technical_name) LIKE '%NO FTD%'
                OR UPPER(c.technical_name) LIKE '%FTD%'
                OR UPPER(c.technical_name) LIKE '%WHALE%')                     THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%WHITEMARKET%'                        THEN 'whitemarket'
      ELSE NULL
    END AS partner,
    CASE
      WHEN UPPER(c.technical_name) LIKE 'TRADEIT GENERAL MISSION%'             THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & NO TRADE%'              THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%NO TRADE%'                THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & TRADE%'                 THEN 'C2'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(c.technical_name) NOT LIKE '%NO TRADE%'                   THEN 'C2'
      WHEN UPPER(c.technical_name) LIKE '%AGNOSTIC MISSION%'                   THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE 'KZ NO AL USERS%'                     THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE '%KZ AL USERS%'                       THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%NO KYC%'                            THEN 'C1'
      WHEN UPPER(c.technical_name) LIKE '%NO FTD%'                            THEN 'FTD'
      WHEN UPPER(c.technical_name) LIKE '%WHALE%'                             THEN 'Bet'
      WHEN UPPER(c.technical_name) LIKE '%FTD%'
           AND UPPER(c.technical_name) NOT LIKE '%NO FTD%'                     THEN 'Bet'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 1%NO AL%'        THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 2%AL%NO BUY%'    THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%'       THEN 'C2'
      ELSE NULL
    END AS funnel_stage
  FROM `business-intelligence-prod.dbt_user.fact__user_campaign_missions` ucm
  JOIN `business-intelligence-prod.dbt_user.dim__campaigns` c
    ON ucm.campaign_id = c.campaign_id
  WHERE ucm.created_at >= TIMESTAMP('2026-01-01')
    AND ucm.created_at <  TIMESTAMP('2026-04-01')
    AND UPPER(c.technical_name) NOT LIKE '%5-STACK%'
    AND UPPER(c.technical_name) NOT LIKE '%PREMIUM MONTHLY%'
    AND UPPER(c.technical_name) NOT LIKE '%FACEIT WEEKLY%'
    AND UPPER(c.technical_name) NOT LIKE '%COUNTER-STRIKE COUNTDOWN%'
),

match_counts AS (
  SELECT
    su.user_id,
    su.partner,
    su.funnel_stage,
    IFNULL(m.match_count_30d, 0) AS match_count_30d
  FROM stage_users su
  LEFT JOIN (
    SELECT
      pu.user_id,
      COUNT(DISTINCT mat.match_id) AS match_count_30d
    FROM `business-intelligence-prod.DataMart.Matches` mat,
      UNNEST(mat.teams) t,
      UNNEST(t.parties) p,
      UNNEST(p.users) pu
    WHERE mat.created_at >= TIMESTAMP('2026-03-01')
      AND mat.created_at <  TIMESTAMP('2026-04-01')
      AND mat.finished_at IS NOT NULL
    GROUP BY pu.user_id
  ) m ON su.user_id = m.user_id
  WHERE su.funnel_stage IS NOT NULL
    AND su.partner IS NOT NULL
),

bucketed AS (
  SELECT
    partner,
    funnel_stage,
    match_count_30d,
    CASE
      WHEN match_count_30d = 0                 THEN '0 matches'
      WHEN match_count_30d BETWEEN 1 AND 5     THEN '1-5'
      WHEN match_count_30d BETWEEN 6 AND 15    THEN '6-15'
      WHEN match_count_30d BETWEEN 16 AND 30   THEN '16-30'
      WHEN match_count_30d BETWEEN 31 AND 50   THEN '31-50'
      ELSE '50+'
    END AS activity_bucket,
    CASE
      WHEN match_count_30d = 0                 THEN 1
      WHEN match_count_30d BETWEEN 1 AND 5     THEN 2
      WHEN match_count_30d BETWEEN 6 AND 15    THEN 3
      WHEN match_count_30d BETWEEN 16 AND 30   THEN 4
      WHEN match_count_30d BETWEEN 31 AND 50   THEN 5
      ELSE 6
    END AS bucket_order
  FROM match_counts
),

agg AS (
  SELECT
    partner,
    funnel_stage,
    activity_bucket,
    bucket_order,
    COUNT(*) AS user_count
  FROM bucketed
  GROUP BY partner, funnel_stage, activity_bucket, bucket_order
),

stage_totals AS (
  SELECT partner, funnel_stage, SUM(user_count) AS total
  FROM agg
  GROUP BY partner, funnel_stage
),

stage_avg AS (
  SELECT partner, funnel_stage, ROUND(AVG(match_count_30d), 1) AS avg_matches_30d
  FROM bucketed
  GROUP BY partner, funnel_stage
)

SELECT
  a.partner,
  a.funnel_stage,
  a.activity_bucket,
  a.bucket_order,
  a.user_count,
  ROUND(100.0 * a.user_count / t.total, 1) AS pct_of_stage,
  t.total AS stage_total,
  sa.avg_matches_30d AS stage_avg_matches
FROM agg a
JOIN stage_totals t ON a.partner = t.partner AND a.funnel_stage = t.funnel_stage
JOIN stage_avg sa ON a.partner = sa.partner AND a.funnel_stage = sa.funnel_stage
ORDER BY a.partner, a.funnel_stage, a.bucket_order;


-- =============================================================================
-- QUERY 3: Solo vs Party per Stage per Partner
--
-- Returns: partner, funnel_stage, play_mode, user_count, pct
-- Classification: >50% of 30d matches in party (size>1) = Party Player
-- Card type: Donut chart (Solo / Party / No Matches)
-- =============================================================================

WITH stage_users AS (
  SELECT DISTINCT
    ucm.user_id,
    CASE
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%'                            THEN 'tradeit'
      WHEN UPPER(c.technical_name) LIKE '%AGNOSTIC%'                           THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%WINLINE%'                            THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'KZ %'                                THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'MISSION %'
           AND (UPPER(c.technical_name) LIKE '%NO KYC%'
                OR UPPER(c.technical_name) LIKE '%NO FTD%'
                OR UPPER(c.technical_name) LIKE '%FTD%'
                OR UPPER(c.technical_name) LIKE '%WHALE%')                     THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%WHITEMARKET%'                        THEN 'whitemarket'
      ELSE NULL
    END AS partner,
    CASE
      WHEN UPPER(c.technical_name) LIKE 'TRADEIT GENERAL MISSION%'             THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & NO TRADE%'              THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%NO TRADE%'                THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & TRADE%'                 THEN 'C2'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(c.technical_name) NOT LIKE '%NO TRADE%'                   THEN 'C2'
      WHEN UPPER(c.technical_name) LIKE '%AGNOSTIC MISSION%'                   THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE 'KZ NO AL USERS%'                     THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE '%KZ AL USERS%'                       THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%NO KYC%'                            THEN 'C1'
      WHEN UPPER(c.technical_name) LIKE '%NO FTD%'                            THEN 'FTD'
      WHEN UPPER(c.technical_name) LIKE '%WHALE%'                             THEN 'Bet'
      WHEN UPPER(c.technical_name) LIKE '%FTD%'
           AND UPPER(c.technical_name) NOT LIKE '%NO FTD%'                     THEN 'Bet'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 1%NO AL%'        THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 2%AL%NO BUY%'    THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%'       THEN 'C2'
      ELSE NULL
    END AS funnel_stage
  FROM `business-intelligence-prod.dbt_user.fact__user_campaign_missions` ucm
  JOIN `business-intelligence-prod.dbt_user.dim__campaigns` c
    ON ucm.campaign_id = c.campaign_id
  WHERE ucm.created_at >= TIMESTAMP('2026-01-01')
    AND ucm.created_at <  TIMESTAMP('2026-04-01')
    AND UPPER(c.technical_name) NOT LIKE '%5-STACK%'
    AND UPPER(c.technical_name) NOT LIKE '%PREMIUM MONTHLY%'
    AND UPPER(c.technical_name) NOT LIKE '%FACEIT WEEKLY%'
    AND UPPER(c.technical_name) NOT LIKE '%COUNTER-STRIKE COUNTDOWN%'
),

user_match_modes AS (
  SELECT
    pu.user_id,
    mat.match_id,
    MAX(p.size) AS party_size
  FROM `business-intelligence-prod.DataMart.Matches` mat,
    UNNEST(mat.teams) t,
    UNNEST(t.parties) p,
    UNNEST(p.users) pu
  WHERE mat.created_at >= TIMESTAMP('2026-03-01')
    AND mat.created_at <  TIMESTAMP('2026-04-01')
    AND mat.finished_at IS NOT NULL
  GROUP BY pu.user_id, mat.match_id
),

user_mode_summary AS (
  SELECT
    user_id,
    COUNT(*) AS total_matches,
    COUNTIF(party_size > 1) AS party_matches,
    ROUND(100.0 * COUNTIF(party_size > 1) / COUNT(*), 1) AS party_pct
  FROM user_match_modes
  GROUP BY user_id
),

classified AS (
  SELECT
    su.partner,
    su.funnel_stage,
    su.user_id,
    CASE
      WHEN ums.total_matches IS NULL OR ums.total_matches = 0 THEN 'No Matches'
      WHEN ums.party_pct > 50 THEN 'Party Player'
      ELSE 'Solo Player'
    END AS play_mode
  FROM stage_users su
  LEFT JOIN user_mode_summary ums ON su.user_id = ums.user_id
  WHERE su.funnel_stage IS NOT NULL
    AND su.partner IS NOT NULL
),

agg AS (
  SELECT partner, funnel_stage, play_mode, COUNT(*) AS user_count
  FROM classified
  GROUP BY partner, funnel_stage, play_mode
),

stage_totals AS (
  SELECT partner, funnel_stage, SUM(user_count) AS total
  FROM agg
  GROUP BY partner, funnel_stage
)

SELECT
  a.partner,
  a.funnel_stage,
  a.play_mode,
  a.user_count,
  ROUND(100.0 * a.user_count / t.total, 1) AS pct_of_stage,
  t.total AS stage_total
FROM agg a
JOIN stage_totals t ON a.partner = t.partner AND a.funnel_stage = t.funnel_stage
ORDER BY a.partner, a.funnel_stage, a.play_mode;


-- =============================================================================
-- QUERY 4: Skill × Spending Matrix (BOFU only)
--
-- Returns: partner, skill_tier, spending_tier, user_count, pct
-- Skill: High (7-10), Mid (4-6), Low (0-3) from games[].skill_level
-- Spending: High (>10K FP spent), Mid (1K-10K), Low (<1K)
-- Card type: 3×3 heatmap matrix
-- =============================================================================

WITH stage_users AS (
  -- BOFU only: Tradeit C2, Winline Bet, WhiteMarket C2
  SELECT DISTINCT
    ucm.user_id,
    CASE
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & TRADE%'                 THEN 'tradeit'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(c.technical_name) NOT LIKE '%NO TRADE%'                   THEN 'tradeit'
      WHEN UPPER(c.technical_name) LIKE '%WHALE%'                             THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%FTD%'
           AND UPPER(c.technical_name) NOT LIKE '%NO FTD%'
           AND (UPPER(c.technical_name) LIKE '%WINLINE%'
                OR UPPER(c.technical_name) LIKE 'MISSION %')                   THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%'       THEN 'whitemarket'
      ELSE NULL
    END AS partner
  FROM `business-intelligence-prod.dbt_user.fact__user_campaign_missions` ucm
  JOIN `business-intelligence-prod.dbt_user.dim__campaigns` c
    ON ucm.campaign_id = c.campaign_id
  WHERE ucm.created_at >= TIMESTAMP('2026-01-01')
    AND ucm.created_at <  TIMESTAMP('2026-04-01')
    AND (
      UPPER(c.technical_name) LIKE '%TRADEIT%AL & TRADE%'
      OR UPPER(c.technical_name) LIKE '%TRADEIT%AL%TRADE%'
      OR UPPER(c.technical_name) LIKE '%WHALE%'
      OR (UPPER(c.technical_name) LIKE '%FTD%'
          AND UPPER(c.technical_name) NOT LIKE '%NO FTD%')
      OR UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%'
    )
),

user_skill AS (
  SELECT
    u.user_id,
    MAX(g.skill_level) AS skill_level
  FROM `business-intelligence-prod.DataMart.Users` u,
    UNNEST(u.games) g
  WHERE g.skill_level IS NOT NULL
  GROUP BY u.user_id
),

-- Spending = PURCHASE type transactions (shop buys, always negative amount)
-- currency is 'faceit_points' (not 'FP'), type = 'PURCHASE'
-- Avg purchase ~-3,462 FP; tiers: Low <1K, Mid 1K-10K, High >10K
user_spending AS (
  SELECT
    entity.id AS user_id,
    ABS(SUM(amount)) AS total_fp_spent
  FROM `business-intelligence-prod.TransactionsService.TransactionHistory`
  WHERE created_at >= TIMESTAMP('2025-01-01')
    AND created_at <  TIMESTAMP('2026-04-01')
    AND currency = 'faceit_points'
    AND type = 'PURCHASE'
  GROUP BY entity.id
),

classified AS (
  SELECT
    su.partner,
    su.user_id,
    CASE
      WHEN IFNULL(us.skill_level, 0) >= 7 THEN 'High Skill'
      WHEN IFNULL(us.skill_level, 0) >= 4 THEN 'Mid Skill'
      ELSE 'Low Skill'
    END AS skill_tier,
    CASE
      WHEN IFNULL(usp.total_fp_spent, 0) >= 10000 THEN 'High Spender'
      WHEN IFNULL(usp.total_fp_spent, 0) >= 1000  THEN 'Mid Spender'
      ELSE 'Low Spender'
    END AS spending_tier
  FROM stage_users su
  LEFT JOIN user_skill us ON su.user_id = us.user_id
  LEFT JOIN user_spending usp ON su.user_id = usp.user_id
  WHERE su.partner IS NOT NULL
),

agg AS (
  SELECT partner, skill_tier, spending_tier, COUNT(*) AS user_count
  FROM classified
  GROUP BY partner, skill_tier, spending_tier
),

partner_totals AS (
  SELECT partner, SUM(user_count) AS total
  FROM agg
  GROUP BY partner
)

SELECT
  a.partner,
  a.skill_tier,
  a.spending_tier,
  a.user_count,
  ROUND(100.0 * a.user_count / pt.total, 1) AS pct_of_bofu,
  pt.total AS bofu_total
FROM agg a
JOIN partner_totals pt ON a.partner = pt.partner
ORDER BY a.partner,
  CASE a.skill_tier WHEN 'High Skill' THEN 1 WHEN 'Mid Skill' THEN 2 ELSE 3 END,
  CASE a.spending_tier WHEN 'High Spender' THEN 1 WHEN 'Mid Spender' THEN 2 ELSE 3 END;


-- =============================================================================
-- QUERY 5: Stage Velocity — Median Days Between Funnel Stages
--
-- Returns: partner, from_stage, to_stage, median_days, p25, p75, user_count
-- Logic: First activation timestamp per user per stage, diff consecutive stages
-- No time filter on stage_users — need full history for prior-stage timestamps
-- Card type: KPI metric with P25-P75 range
-- =============================================================================

WITH user_stage_timestamps AS (
  SELECT
    ucm.user_id,
    CASE
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%'                            THEN 'tradeit'
      WHEN UPPER(c.technical_name) LIKE '%AGNOSTIC%'                           THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%WINLINE%'                            THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'KZ %'                                THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'MISSION %'
           AND (UPPER(c.technical_name) LIKE '%NO KYC%'
                OR UPPER(c.technical_name) LIKE '%NO FTD%'
                OR UPPER(c.technical_name) LIKE '%FTD%'
                OR UPPER(c.technical_name) LIKE '%WHALE%')                     THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%WHITEMARKET%'                        THEN 'whitemarket'
      ELSE NULL
    END AS partner,
    CASE
      WHEN UPPER(c.technical_name) LIKE 'TRADEIT GENERAL MISSION%'             THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & NO TRADE%'              THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%NO TRADE%'                THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & TRADE%'                 THEN 'C2'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(c.technical_name) NOT LIKE '%NO TRADE%'                   THEN 'C2'
      WHEN UPPER(c.technical_name) LIKE '%AGNOSTIC MISSION%'                   THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE 'KZ NO AL USERS%'                     THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE '%KZ AL USERS%'                       THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%NO KYC%'                            THEN 'C1'
      WHEN UPPER(c.technical_name) LIKE '%NO FTD%'                            THEN 'FTD'
      WHEN UPPER(c.technical_name) LIKE '%WHALE%'                             THEN 'Bet'
      WHEN UPPER(c.technical_name) LIKE '%FTD%'
           AND UPPER(c.technical_name) NOT LIKE '%NO FTD%'                     THEN 'Bet'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 1%NO AL%'        THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 2%AL%NO BUY%'    THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%'       THEN 'C2'
      ELSE NULL
    END AS funnel_stage,
    -- First activation = earliest created_at for this user in this stage
    MIN(ucm.created_at) AS first_activation
  FROM `business-intelligence-prod.dbt_user.fact__user_campaign_missions` ucm
  JOIN `business-intelligence-prod.dbt_user.dim__campaigns` c
    ON ucm.campaign_id = c.campaign_id
  WHERE UPPER(c.technical_name) NOT LIKE '%5-STACK%'
    AND UPPER(c.technical_name) NOT LIKE '%PREMIUM MONTHLY%'
    AND UPPER(c.technical_name) NOT LIKE '%FACEIT WEEKLY%'
    AND UPPER(c.technical_name) NOT LIKE '%COUNTER-STRIKE COUNTDOWN%'
  GROUP BY
    ucm.user_id,
    partner,
    funnel_stage
),

stage_order AS (
  SELECT 'tradeit' AS partner, 'EBU' AS stage, 1 AS ord UNION ALL
  SELECT 'tradeit', 'AL', 2 UNION ALL
  SELECT 'tradeit', 'C2', 3 UNION ALL
  SELECT 'winline', 'EBU', 1 UNION ALL
  SELECT 'winline', 'AL', 2 UNION ALL
  SELECT 'winline', 'C1', 3 UNION ALL
  SELECT 'winline', 'FTD', 4 UNION ALL
  SELECT 'winline', 'Bet', 5 UNION ALL
  SELECT 'whitemarket', 'EBU', 1 UNION ALL
  SELECT 'whitemarket', 'AL', 2 UNION ALL
  SELECT 'whitemarket', 'C2', 3
),

user_pivoted AS (
  SELECT
    ust.user_id,
    ust.partner,
    ust.funnel_stage,
    ust.first_activation,
    so.ord AS stage_ord
  FROM user_stage_timestamps ust
  JOIN stage_order so ON ust.partner = so.partner AND ust.funnel_stage = so.stage
  WHERE ust.partner IS NOT NULL
    AND ust.funnel_stage IS NOT NULL
),

transitions AS (
  SELECT
    curr.partner,
    prev_so.stage AS from_stage,
    curr.funnel_stage AS to_stage,
    curr.user_id,
    TIMESTAMP_DIFF(curr.first_activation, prev.first_activation, DAY) AS days_between
  FROM user_pivoted curr
  JOIN stage_order prev_so
    ON curr.partner = prev_so.partner AND prev_so.ord = curr.stage_ord - 1
  JOIN user_pivoted prev
    ON curr.user_id = prev.user_id
    AND curr.partner = prev.partner
    AND prev.funnel_stage = prev_so.stage
  WHERE curr.first_activation > prev.first_activation
)

SELECT
  partner,
  from_stage,
  to_stage,
  COUNT(*) AS user_count,
  APPROX_QUANTILES(days_between, 4)[OFFSET(2)] AS median_days,
  APPROX_QUANTILES(days_between, 4)[OFFSET(1)] AS p25_days,
  APPROX_QUANTILES(days_between, 4)[OFFSET(3)] AS p75_days,
  ROUND(AVG(days_between), 1) AS avg_days
FROM transitions
WHERE days_between >= 0
GROUP BY partner, from_stage, to_stage
ORDER BY partner,
  CASE from_stage
    WHEN 'EBU' THEN 1 WHEN 'AL' THEN 2 WHEN 'C1' THEN 3
    WHEN 'FTD' THEN 4 WHEN 'C2' THEN 3 ELSE 5
  END;


-- =============================================================================
-- QUERY 6: Age Group Distribution per Stage per Partner
--
-- Returns: partner, funnel_stage, age_group, user_count, pct_of_stage
-- Card type: Horizontal bar chart (6 age buckets, sorted by size,
--            warning colors on minors and invalid)
-- Source: dbt_user.dim__users.age_tier (98.5% coverage)
-- Grouping: <13/Invalid ⚠ (0-12 + Unknown + error),
--           13-17 ⚠, 18-24, 25-34, 35-44, 45+ (45-54 + 55-64 + 65+)
-- =============================================================================

WITH stage_users AS (
  SELECT DISTINCT
    ucm.user_id,
    CASE
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%'                            THEN 'tradeit'
      WHEN UPPER(c.technical_name) LIKE '%AGNOSTIC%'                           THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%WINLINE%'                            THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'KZ %'                                THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE 'MISSION %'
           AND (UPPER(c.technical_name) LIKE '%NO KYC%'
                OR UPPER(c.technical_name) LIKE '%NO FTD%'
                OR UPPER(c.technical_name) LIKE '%FTD%'
                OR UPPER(c.technical_name) LIKE '%WHALE%')                     THEN 'winline'
      WHEN UPPER(c.technical_name) LIKE '%WHITEMARKET%'                        THEN 'whitemarket'
      ELSE NULL
    END AS partner,
    CASE
      -- Tradeit
      WHEN UPPER(c.technical_name) LIKE 'TRADEIT GENERAL MISSION%'             THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & NO TRADE%'              THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%NO TRADE%'                THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL & TRADE%'                 THEN 'C2'
      WHEN UPPER(c.technical_name) LIKE '%TRADEIT%AL%TRADE%'
           AND UPPER(c.technical_name) NOT LIKE '%NO TRADE%'                   THEN 'C2'
      -- Winline EBU
      WHEN UPPER(c.technical_name) LIKE '%AGNOSTIC MISSION%'                   THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE 'KZ NO AL USERS%'                     THEN 'EBU'
      -- Winline AL
      WHEN UPPER(c.technical_name) LIKE '%KZ AL USERS%'                       THEN 'AL'
      -- Winline C1 (NO KYC)
      WHEN UPPER(c.technical_name) LIKE '%NO KYC%'                            THEN 'C1'
      -- Winline FTD stage (NO FTD = users who haven't deposited yet)
      WHEN UPPER(c.technical_name) LIKE '%NO FTD%'                            THEN 'FTD'
      -- Winline Bet (BOFU): FTD missions (users who HAVE deposited) + WHALE
      WHEN UPPER(c.technical_name) LIKE '%WHALE%'                             THEN 'Bet'
      WHEN UPPER(c.technical_name) LIKE '%FTD%'
           AND UPPER(c.technical_name) NOT LIKE '%NO FTD%'                     THEN 'Bet'
      -- WhiteMarket
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 1%NO AL%'        THEN 'EBU'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 2%AL%NO BUY%'    THEN 'AL'
      WHEN UPPER(c.technical_name) LIKE 'WHITEMARKET MISSION 3%AL%BUY%'       THEN 'C2'
      ELSE NULL
    END AS funnel_stage
  FROM `business-intelligence-prod.dbt_user.fact__user_campaign_missions` ucm
  JOIN `business-intelligence-prod.dbt_user.dim__campaigns` c
    ON ucm.campaign_id = c.campaign_id
  WHERE ucm.created_at >= '2026-01-01'
    AND ucm.created_at < '2026-04-01'
    AND ucm.user_mission_status = 'COMPLETED'
    AND UPPER(c.technical_name) NOT LIKE '%TEST%'
)

SELECT
  su.partner,
  su.funnel_stage,
  CASE
    WHEN u.age_tier IN ('0-12', 'Unknown', 'error') THEN '<13 / Invalid'
    WHEN u.age_tier = '13-17'                        THEN '13-17'
    WHEN u.age_tier = '18-24'                        THEN '18-24'
    WHEN u.age_tier = '25-34'                        THEN '25-34'
    WHEN u.age_tier = '35-44'                        THEN '35-44'
    WHEN u.age_tier IN ('45-54', '55-64', '65+')     THEN '45+'
    ELSE '<13 / Invalid'
  END AS age_group,
  COUNT(DISTINCT su.user_id) AS user_count
FROM stage_users su
JOIN `business-intelligence-prod.dbt_user.dim__users` u
  ON su.user_id = u.user_id
WHERE su.partner IS NOT NULL
  AND su.funnel_stage IS NOT NULL
GROUP BY su.partner, su.funnel_stage, age_group
ORDER BY su.partner, su.funnel_stage, user_count DESC;
