#!/bin/bash
# NSM Dashboard Data Refresh Script
# Pulls mission, EBU, and conversion data from BigQuery
# Output: JSON files consumed by nsm-dashboard.html
#
# Usage: ./scripts/refresh-nsm-data.sh
# Requires: gcloud SDK authenticated as m.natalini@efg.gg
#
# Last updated: 2026-04-06

set -euo pipefail

# Add gcloud to PATH (macOS homebrew). In CI, setup-gcloud handles this.
if [ -d "/opt/homebrew/share/google-cloud-sdk/bin" ]; then
    export PATH="/opt/homebrew/share/google-cloud-sdk/bin:$PATH"
fi

PROJECT="business-intelligence-prod"
OUTPUT_DIR="$(dirname "$0")/../data/bq_exports"
mkdir -p "$OUTPUT_DIR"

echo "=== NSM Dashboard Data Refresh ==="
echo "Project: $PROJECT"
echo "Output:  $OUTPUT_DIR"
echo "Time:    $(date)"
echo ""

# ─────────────────────────────────────────────
# Partner config
# ─────────────────────────────────────────────
TRADEIT_ORG="976fe92b-0998-4a2a-86a6-f655bbab8f07"
WINLINE_ORG="397f5239-ab93-484d-9f94-4231b0cfa48e"
WINLINE_BY_ORG="a8f12da7-d377-4b9f-aedf-a33cb1283b20"
WINLINE_KZ_ORG="b5efeb75-4f23-494e-bc85-9319c1a87c75"
WHITEMARKET_ORG="db18537b-4172-4813-b089-36490c1553b7"

# € values per conversion type (from NSM per Partner - Value.tsv)
# These are applied client-side in the dashboard; we just export counts here.

# ─────────────────────────────────────────────
# Q1: EBU per partner YTD + deduplicated total
# ─────────────────────────────────────────────
echo "[1/7] EBU per partner (YTD)..."
bq query --project_id="$PROJECT" --use_legacy_sql=false --format=json --max_rows=10 '
WITH partner_campaigns AS (
  SELECT
    _id as campaign_id,
    CASE
      WHEN organizer.id = "'"$TRADEIT_ORG"'" THEN "Tradeit"
      WHEN organizer.id = "'"$WINLINE_ORG"'" THEN "Winline"
      WHEN organizer.id = "'"$WINLINE_BY_ORG"'" THEN "Winline_BY"
      WHEN organizer.id = "'"$WINLINE_KZ_ORG"'" THEN "Winline_KZ"
      WHEN organizer.id = "'"$WHITEMARKET_ORG"'" THEN "WhiteMarket"
    END as partner
  FROM `business-intelligence-prod.CampaignService.Campaigns`
  WHERE organizer.id IN ("'"$TRADEIT_ORG"'", "'"$WINLINE_ORG"'", "'"$WINLINE_BY_ORG"'", "'"$WINLINE_KZ_ORG"'", "'"$WHITEMARKET_ORG"'")
    AND schedule.start_date >= "2025-12-01"
),
per_partner AS (
  SELECT pc.partner, COUNT(DISTINCT um.user_id) as ebu
  FROM `business-intelligence-prod.CampaignService.UserMissions` um
  JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
  GROUP BY pc.partner
),
winline_all AS (
  SELECT "Winline_All" as partner, COUNT(DISTINCT um.user_id) as ebu
  FROM `business-intelligence-prod.CampaignService.UserMissions` um
  JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
  WHERE pc.partner IN ("Winline", "Winline_BY", "Winline_KZ")
),
total AS (
  SELECT "Portfolio" as partner, COUNT(DISTINCT um.user_id) as ebu
  FROM `business-intelligence-prod.CampaignService.UserMissions` um
  JOIN (SELECT campaign_id FROM partner_campaigns) pc ON um.campaign_id = pc.campaign_id
)
SELECT * FROM per_partner
UNION ALL
SELECT * FROM winline_all
UNION ALL
SELECT * FROM total
ORDER BY ebu DESC
' > "$OUTPUT_DIR/ebu_ytd.json" 2>/dev/null

echo "  ✓ Saved ebu_ytd.json"

# ─────────────────────────────────────────────
# Q2: Weekly EBU per partner
# ─────────────────────────────────────────────
echo "[2/7] Weekly EBU per partner..."
bq query --project_id="$PROJECT" --use_legacy_sql=false --format=json --max_rows=200 '
WITH partner_campaigns AS (
  SELECT
    _id as campaign_id,
    CASE
      WHEN organizer.id = "'"$TRADEIT_ORG"'" THEN "Tradeit"
      WHEN organizer.id = "'"$WINLINE_ORG"'" THEN "Winline"
      WHEN organizer.id = "'"$WINLINE_BY_ORG"'" THEN "Winline_BY"
      WHEN organizer.id = "'"$WINLINE_KZ_ORG"'" THEN "Winline_KZ"
      WHEN organizer.id = "'"$WHITEMARKET_ORG"'" THEN "WhiteMarket"
    END as partner
  FROM `business-intelligence-prod.CampaignService.Campaigns`
  WHERE organizer.id IN ("'"$TRADEIT_ORG"'", "'"$WINLINE_ORG"'", "'"$WINLINE_BY_ORG"'", "'"$WINLINE_KZ_ORG"'", "'"$WHITEMARKET_ORG"'")
    AND schedule.start_date >= "2025-12-01"
)
SELECT
  DATE_TRUNC(DATE(um.created_at), WEEK(MONDAY)) as week_start,
  pc.partner,
  COUNT(DISTINCT um.user_id) as weekly_ebu
FROM `business-intelligence-prod.CampaignService.UserMissions` um
JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
WHERE um.created_at >= "2025-12-01"
GROUP BY week_start, pc.partner
ORDER BY week_start, pc.partner
' > "$OUTPUT_DIR/weekly_ebu_by_partner.json" 2>/dev/null

echo "  ✓ Saved weekly_ebu_by_partner.json"

# ─────────────────────────────────────────────
# Q3: Weekly deduplicated total EBU
# ─────────────────────────────────────────────
echo "[3/7] Weekly deduplicated EBU (portfolio)..."
bq query --project_id="$PROJECT" --use_legacy_sql=false --format=json --max_rows=200 '
WITH partner_campaigns AS (
  SELECT _id as campaign_id
  FROM `business-intelligence-prod.CampaignService.Campaigns`
  WHERE organizer.id IN ("'"$TRADEIT_ORG"'", "'"$WINLINE_ORG"'", "'"$WINLINE_BY_ORG"'", "'"$WINLINE_KZ_ORG"'", "'"$WHITEMARKET_ORG"'")
    AND schedule.start_date >= "2025-12-01"
)
SELECT
  DATE_TRUNC(DATE(um.created_at), WEEK(MONDAY)) as week_start,
  COUNT(DISTINCT um.user_id) as weekly_ebu_dedup
FROM `business-intelligence-prod.CampaignService.UserMissions` um
JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
WHERE um.created_at >= "2025-12-01"
GROUP BY week_start
ORDER BY week_start
' > "$OUTPUT_DIR/weekly_ebu_dedup.json" 2>/dev/null

echo "  ✓ Saved weekly_ebu_dedup.json"

# ─────────────────────────────────────────────
# Q4: Mission completions by challenge per partner per month
# (feeds Missions tabs + NSM € value calculation)
# ─────────────────────────────────────────────
echo "[4/7] Mission completions by challenge..."
bq query --project_id="$PROJECT" --use_legacy_sql=false --format=json --max_rows=500 '
WITH partner_campaigns AS (
  SELECT
    _id as campaign_id,
    technical_name,
    CASE
      WHEN organizer.id = "'"$TRADEIT_ORG"'" THEN "Tradeit"
      WHEN organizer.id = "'"$WINLINE_ORG"'" THEN "Winline"
      WHEN organizer.id = "'"$WINLINE_BY_ORG"'" THEN "Winline_BY"
      WHEN organizer.id = "'"$WINLINE_KZ_ORG"'" THEN "Winline_KZ"
      WHEN organizer.id = "'"$WHITEMARKET_ORG"'" THEN "WhiteMarket"
    END as partner
  FROM `business-intelligence-prod.CampaignService.Campaigns`
  WHERE organizer.id IN ("'"$TRADEIT_ORG"'", "'"$WINLINE_ORG"'", "'"$WINLINE_BY_ORG"'", "'"$WINLINE_KZ_ORG"'", "'"$WHITEMARKET_ORG"'")
    AND schedule.start_date >= "2025-12-01"
)
SELECT
  pc.partner,
  pc.technical_name as campaign_technical_name,
  FORMAT_DATE("%Y-%m", DATE(um.updated_at)) as month,
  um.name as challenge_name,
  COUNT(*) as completions,
  COUNT(DISTINCT um.user_id) as unique_users
FROM `business-intelligence-prod.CampaignService.UserMissions` um
JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
WHERE um.status = "complete"
GROUP BY pc.partner, pc.technical_name, month, challenge_name
ORDER BY pc.partner, month, completions DESC
' > "$OUTPUT_DIR/mission_completions.json" 2>/dev/null

echo "  ✓ Saved mission_completions.json"

# ─────────────────────────────────────────────
# Q5: Weekly mission completions by challenge per partner
# (for weekly trend charts)
# ─────────────────────────────────────────────
echo "[5/7] Weekly mission completions..."
bq query --project_id="$PROJECT" --use_legacy_sql=false --format=json --max_rows=1000 '
WITH partner_campaigns AS (
  SELECT
    _id as campaign_id,
    technical_name,
    CASE
      WHEN organizer.id = "'"$TRADEIT_ORG"'" THEN "Tradeit"
      WHEN organizer.id = "'"$WINLINE_ORG"'" THEN "Winline"
      WHEN organizer.id = "'"$WINLINE_BY_ORG"'" THEN "Winline_BY"
      WHEN organizer.id = "'"$WINLINE_KZ_ORG"'" THEN "Winline_KZ"
      WHEN organizer.id = "'"$WHITEMARKET_ORG"'" THEN "WhiteMarket"
    END as partner
  FROM `business-intelligence-prod.CampaignService.Campaigns`
  WHERE organizer.id IN ("'"$TRADEIT_ORG"'", "'"$WINLINE_ORG"'", "'"$WINLINE_BY_ORG"'", "'"$WINLINE_KZ_ORG"'", "'"$WHITEMARKET_ORG"'")
    AND schedule.start_date >= "2025-12-01"
)
SELECT
  DATE_TRUNC(DATE(um.updated_at), WEEK(MONDAY)) as week_start,
  pc.partner,
  um.name as challenge_name,
  COUNT(*) as completions,
  COUNT(DISTINCT um.user_id) as unique_users
FROM `business-intelligence-prod.CampaignService.UserMissions` um
JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
WHERE um.status = "complete"
  AND um.updated_at >= "2025-12-01"
GROUP BY week_start, pc.partner, challenge_name
ORDER BY week_start, pc.partner, completions DESC
' > "$OUTPUT_DIR/weekly_mission_completions.json" 2>/dev/null

echo "  ✓ Saved weekly_mission_completions.json"

# ─────────────────────────────────────────────
# Q6: Reward claims (for AL tracking — especially Tradeit)
# ─────────────────────────────────────────────
echo "[6/7] Reward claims by partner..."
bq query --project_id="$PROJECT" --use_legacy_sql=false --format=json --max_rows=200 '
WITH partner_campaigns AS (
  SELECT
    _id as campaign_id,
    technical_name,
    CASE
      WHEN organizer.id = "'"$TRADEIT_ORG"'" THEN "Tradeit"
      WHEN organizer.id = "'"$WINLINE_ORG"'" THEN "Winline"
      WHEN organizer.id = "'"$WINLINE_BY_ORG"'" THEN "Winline_BY"
      WHEN organizer.id = "'"$WINLINE_KZ_ORG"'" THEN "Winline_KZ"
      WHEN organizer.id = "'"$WHITEMARKET_ORG"'" THEN "WhiteMarket"
    END as partner
  FROM `business-intelligence-prod.CampaignService.Campaigns`
  WHERE organizer.id IN ("'"$TRADEIT_ORG"'", "'"$WINLINE_ORG"'", "'"$WINLINE_BY_ORG"'", "'"$WINLINE_KZ_ORG"'", "'"$WHITEMARKET_ORG"'")
    AND schedule.start_date >= "2025-12-01"
)
SELECT
  pc.partner,
  pc.technical_name as campaign_technical_name,
  FORMAT_DATE("%Y-%m", DATE(ur.created_at)) as month,
  ur.status as reward_status,
  COUNT(*) as cnt,
  COUNT(DISTINCT ur.user_id) as unique_users
FROM `business-intelligence-prod.CampaignService.UserRewards` ur
JOIN partner_campaigns pc ON ur.campaign_id = pc.campaign_id
GROUP BY pc.partner, pc.technical_name, month, reward_status
ORDER BY pc.partner, month, cnt DESC
' > "$OUTPUT_DIR/reward_claims.json" 2>/dev/null

echo "  ✓ Saved reward_claims.json"

# ─────────────────────────────────────────────
# Q7: Account Linkages (AL) by partner per week and month
# Source: CDP event table (covers all partners, including those without AL mission challenges)
#
# ID mapping problem: CampaignService.Campaigns._id = config_id (UUID format),
# but account_linkage_operation_v1.parent_id = real campaign_id (hex/ObjectId).
# We bridge via dbt_user.dim__campaigns which has both config_id and campaign_id.
# ─────────────────────────────────────────────
echo "[7/7] Account linkages by partner..."
if bq query --project_id="$PROJECT" --use_legacy_sql=false --format=json --max_rows=500 '
WITH partner_campaigns AS (
  SELECT
    _id as config_id,
    CASE
      WHEN organizer.id = "'"$TRADEIT_ORG"'" THEN "Tradeit"
      WHEN organizer.id = "'"$WINLINE_ORG"'" THEN "Winline"
      WHEN organizer.id = "'"$WINLINE_BY_ORG"'" THEN "Winline_BY"
      WHEN organizer.id = "'"$WINLINE_KZ_ORG"'" THEN "Winline_KZ"
      WHEN organizer.id = "'"$WHITEMARKET_ORG"'" THEN "WhiteMarket"
    END as partner
  FROM `business-intelligence-prod.CampaignService.Campaigns`
  WHERE organizer.id IN ("'"$TRADEIT_ORG"'", "'"$WINLINE_ORG"'", "'"$WINLINE_BY_ORG"'", "'"$WINLINE_KZ_ORG"'", "'"$WHITEMARKET_ORG"'")
    AND schedule.start_date >= "2025-12-01"
),
id_mapping AS (
  SELECT
    pc.config_id,
    pc.partner,
    dc.campaign_id as real_campaign_id
  FROM partner_campaigns pc
  JOIN `business-intelligence-prod.dbt_user.dim__campaigns` dc
    ON pc.config_id = dc.config_id
)
SELECT
  im.partner,
  FORMAT_DATE("%Y-%m", DATE(al.event_timestamp)) as month,
  DATE_TRUNC(DATE(al.event_timestamp), WEEK(MONDAY)) as week_start,
  COUNT(*) as al_count,
  COUNT(DISTINCT al.user_id) as unique_users
FROM `faceit-events-prod-2.user.account_linkage_operation_v1` al
JOIN id_mapping im ON al.parent_id = im.real_campaign_id
WHERE al.parent_type = "CAMPAIGN"
  AND al.operation = "CONNECT"
  AND al.event_timestamp >= "2025-12-01"
GROUP BY im.partner, month, week_start
ORDER BY im.partner, month, week_start
' > "$OUTPUT_DIR/account_linkages.json" 2>/dev/null; then
  echo "  ✓ Saved account_linkages.json"
else
  echo "  ⚠ Q7 failed (likely missing cross-project access to faceit-events-prod-2)"
  echo "  → Writing empty array — dashboard will show zero AL counts"
  echo "[]" > "$OUTPUT_DIR/account_linkages.json"
fi

echo ""
echo "=== DATA EXPORT DONE ==="
echo "All data exported to: $OUTPUT_DIR/"
echo ""
echo "Files:"
ls -lh "$OUTPUT_DIR"/*.json

# --- Step 2: Build dashboard ---
echo ""
echo "=== BUILDING DASHBOARD ==="
SCRIPT_DIR="$(dirname "$0")"
bash "$SCRIPT_DIR/build-dashboard.sh"
BUILD_EXIT=$?

if [ $BUILD_EXIT -eq 0 ]; then
  echo ""
  echo "=== ALL DONE ==="
  echo "Dashboard built and ready at: ../Personal-Space/nsm-dashboard.html"
  echo "To publish: cd ../Personal-Space && git add . && git commit -m 'Update dashboard data' && git push"
else
  echo ""
  echo "=== BUILD FAILED ==="
  echo "Data was exported successfully, but dashboard build failed (exit code $BUILD_EXIT)."
  echo "Try running manually: bash scripts/build-dashboard.sh"
  exit $BUILD_EXIT
fi
