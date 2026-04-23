#!/bin/bash
# refresh_audience_pulse.sh — Refresh Audience Pulse dashboard with latest BQ data
# Usage: ./scripts/refresh_audience_pulse.sh
#
# Requires: bq CLI authenticated, jq, python3
# Output: Updates scripts/data/pulse_*.json and audience-pulse-dashboard.html

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$SCRIPT_DIR/data"
QUERY_DIR="$SCRIPT_DIR/bq_queries"
DASHBOARD="$PROJECT_DIR/audience-pulse-dashboard.html"

BQ="/opt/homebrew/bin/bq"

# Compute date ranges: current week = last 7 days ending yesterday, prior week = 7 days before that
TODAY=$(date -v-1d +%Y-%m-%d)  # yesterday (latest full day)
WEEK_END=$(date -j -f "%Y-%m-%d" "$TODAY" +%Y-%m-%d)
WEEK_START=$(date -j -v-6d -f "%Y-%m-%d" "$TODAY" +%Y-%m-%d)
PREV_END=$(date -j -v-1d -f "%Y-%m-%d" "$WEEK_START" +%Y-%m-%d)
PREV_START=$(date -j -v-6d -f "%Y-%m-%d" "$PREV_END" +%Y-%m-%d)

# For BQ queries we need the day AFTER end (exclusive upper bound)
WEEK_END_EXCL=$(date -j -v+1d -f "%Y-%m-%d" "$WEEK_END" +%Y-%m-%d)
PREV_END_EXCL=$(date -j -v+1d -f "%Y-%m-%d" "$PREV_END" +%Y-%m-%d)

echo "=== Audience Pulse Refresh ==="
echo "This week:  $WEEK_START to $WEEK_END"
echo "Last week:  $PREV_START to $PREV_END"
echo ""

mkdir -p "$DATA_DIR"

# --- Q1: Users by Geo ---
echo "[1/4] Querying user base by geo..."
$BQ query --use_legacy_sql=false --format=prettyjson --max_rows=50 \
"SELECT
  country_iso_code AS country,
  COUNT(*) AS total_users,
  COUNTIF(created_at >= TIMESTAMP('$WEEK_START') AND created_at < TIMESTAMP('$WEEK_END_EXCL')) AS new_this_week,
  COUNTIF(created_at >= TIMESTAMP('$PREV_START') AND created_at < TIMESTAMP('$PREV_END_EXCL')) AS new_last_week
FROM \`business-intelligence-prod.DataMart.Users\`
WHERE country_iso_code IS NOT NULL
  AND TRIM(country_iso_code) != ''
GROUP BY country_iso_code
ORDER BY total_users DESC
LIMIT 50" > "$DATA_DIR/pulse_users.json"
echo "  -> Saved pulse_users.json"

# --- Q2: Sessions by Geo ---
echo "[2/4] Querying sessions by geo..."
$BQ query --use_legacy_sql=false --format=prettyjson --max_rows=50 \
"SELECT
  country,
  COUNT(CASE WHEN event_timestamp >= TIMESTAMP('$WEEK_START') AND event_timestamp < TIMESTAMP('$WEEK_END_EXCL') THEN 1 END) AS sessions_this_week,
  COUNT(CASE WHEN event_timestamp >= TIMESTAMP('$PREV_START') AND event_timestamp < TIMESTAMP('$PREV_END_EXCL') THEN 1 END) AS sessions_last_week
FROM \`faceit-events-prod-2.user.new_tracking_session_v1\`
WHERE event_timestamp >= TIMESTAMP('$PREV_START')
  AND event_timestamp < TIMESTAMP('$WEEK_END_EXCL')
  AND country IS NOT NULL AND TRIM(country) != ''
GROUP BY country
ORDER BY sessions_this_week DESC
LIMIT 50" > "$DATA_DIR/pulse_sessions.json"
echo "  -> Saved pulse_sessions.json"

# --- Q3: Matches by Region × Game ---
echo "[3/4] Querying matches by region and game..."
$BQ query --use_legacy_sql=false --format=prettyjson --max_rows=50 \
"SELECT
  region,
  game,
  COUNTIF(created_at >= TIMESTAMP('$WEEK_START') AND created_at < TIMESTAMP('$WEEK_END_EXCL')) as matches_this_week,
  COUNTIF(created_at >= TIMESTAMP('$PREV_START') AND created_at < TIMESTAMP('$PREV_END_EXCL')) as matches_last_week
FROM \`business-intelligence-prod.DataMart.Matches\`
WHERE created_at >= TIMESTAMP('$PREV_START')
  AND created_at < TIMESTAMP('$WEEK_END_EXCL')
  AND state = 'finished'
GROUP BY region, game
HAVING matches_this_week > 0 OR matches_last_week > 0
ORDER BY matches_this_week DESC
LIMIT 50" > "$DATA_DIR/pulse_matches.json"
echo "  -> Saved pulse_matches.json"

# --- Q4: WAU by Geo ---
echo "[4/4] Querying weekly active users by geo..."
$BQ query --use_legacy_sql=false --format=prettyjson --max_rows=50 \
"SELECT
  country,
  COUNT(DISTINCT CASE WHEN event_timestamp >= TIMESTAMP('$WEEK_START') AND event_timestamp < TIMESTAMP('$WEEK_END_EXCL') THEN user_id END) as wau_this_week,
  COUNT(DISTINCT CASE WHEN event_timestamp >= TIMESTAMP('$PREV_START') AND event_timestamp < TIMESTAMP('$PREV_END_EXCL') THEN user_id END) as wau_last_week
FROM \`faceit-events-prod-2.user.new_tracking_session_v1\`
WHERE event_timestamp >= TIMESTAMP('$PREV_START')
  AND event_timestamp < TIMESTAMP('$WEEK_END_EXCL')
  AND user_id IS NOT NULL AND user_id != ''
GROUP BY country
HAVING wau_this_week > 0 OR wau_last_week > 0
ORDER BY wau_this_week DESC
LIMIT 50" > "$DATA_DIR/pulse_wau.json"
echo "  -> Saved pulse_wau.json"

echo ""
echo "=== All queries complete ==="
echo ""

# --- Assemble dashboard HTML ---
echo "Assembling dashboard..."

python3 - "$DATA_DIR" "$DASHBOARD" "$WEEK_START" "$WEEK_END" "$PREV_START" "$PREV_END" <<'PYEOF'
import json, sys, re
from datetime import datetime

data_dir = sys.argv[1]
dashboard = sys.argv[2]
week_start = sys.argv[3]
week_end = sys.argv[4]
prev_start = sys.argv[5]
prev_end = sys.argv[6]

def load(name):
    with open(f"{data_dir}/{name}") as f:
        return json.load(f)

users = load("pulse_users.json")
sessions = load("pulse_sessions.json")
matches = load("pulse_matches.json")
wau = load("pulse_wau.json")

# Read existing dashboard
with open(dashboard) as f:
    html = f.read()

# Format date range for display
ws = datetime.strptime(week_start, "%Y-%m-%d")
we = datetime.strptime(week_end, "%Y-%m-%d")
ps = datetime.strptime(prev_start, "%Y-%m-%d")
pe = datetime.strptime(prev_end, "%Y-%m-%d")
date_str = f"{ws.strftime('%b %d')}–{we.strftime('%d')} vs {ps.strftime('%b %d')}–{pe.strftime('%d')}, {we.year}"

# Update DASHBOARD_META
html = re.sub(
    r'lastUpdated:\s*"[^"]*"',
    f'lastUpdated: "{datetime.now().strftime("%Y-%m-%d")}"',
    html
)
html = re.sub(
    r'weekStart:\s*"[^"]*"',
    f'weekStart: "{week_start}"',
    html
)
html = re.sub(
    r'weekEnd:\s*"[^"]*"',
    f'weekEnd: "{week_end}"',
    html
)
html = re.sub(
    r'compareStart:\s*"[^"]*"',
    f'compareStart: "{prev_start}"',
    html
)
html = re.sub(
    r'compareEnd:\s*"[^"]*"',
    f'compareEnd: "{prev_end}"',
    html
)

# Update date range display
html = re.sub(
    r'(id="date-range">)[^<]*(</p>)',
    f'\\g<1>{date_str}\\2',
    html
)

# Replace data arrays
def replace_data(html, var_name, data):
    pattern = rf'(const {var_name} = )\[[\s\S]*?\];'
    replacement = f'\\g<1>{json.dumps(data, indent=12)};'
    return re.sub(pattern, replacement, html)

html = replace_data(html, "USERS_DATA", users)
html = replace_data(html, "SESSIONS_DATA", sessions)
html = replace_data(html, "MATCHES_DATA", matches)
html = replace_data(html, "WAU_DATA", wau)

with open(dashboard, "w") as f:
    f.write(html)

print(f"  -> Dashboard updated with date range: {date_str}")
PYEOF

echo ""
echo "=== Refresh complete ==="
echo "Dashboard: $DASHBOARD"
echo "Data: $DATA_DIR/pulse_*.json"
