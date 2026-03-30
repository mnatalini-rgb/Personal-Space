#!/bin/bash
# NSM Dashboard Build Script
# Reads BQ-exported JSON files and injects them into the dashboard HTML template
# Output: Personal-Space/nsm-dashboard.html (ready for GitHub Pages)
#
# Usage: ./scripts/build-dashboard.sh
# Run after: ./scripts/refresh-nsm-data.sh
#
# Last updated: 2026-03-21

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_DIR/data/bq_exports"
TEMPLATE="$PROJECT_DIR/analysis/nsm-dashboard.html"
OUTPUT_DIR="$PROJECT_DIR/../Personal-Space"
OUTPUT="$OUTPUT_DIR/nsm-dashboard.html"

echo "=== NSM Dashboard Build ==="
echo "Template:  $TEMPLATE"
echo "Data dir:  $DATA_DIR"
echo "Output:    $OUTPUT"
echo "Time:      $(date)"
echo ""

# ─────────────────────────────────────────────
# Verify all required files exist
# ─────────────────────────────────────────────
REQUIRED_FILES=(
    "ebu_ytd.json"
    "weekly_ebu_dedup.json"
    "weekly_ebu_by_partner.json"
    "mission_completions.json"
    "weekly_mission_completions.json"
    "reward_claims.json"
)

for f in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$DATA_DIR/$f" ]; then
        echo "ERROR: Missing required file: $DATA_DIR/$f"
        echo "Run ./scripts/refresh-nsm-data.sh first."
        exit 1
    fi
done

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Missing template: $TEMPLATE"
    exit 1
fi

if [ ! -d "$OUTPUT_DIR" ]; then
    echo "ERROR: Output directory does not exist: $OUTPUT_DIR"
    echo "Clone the Personal-Space repo first."
    exit 1
fi

echo "✓ All required files found"
echo ""

# ─────────────────────────────────────────────
# Read JSON files and construct BQ_DATA object
# ─────────────────────────────────────────────
echo "Building BQ_DATA object..."

# Read each JSON file into a variable (single-line JSON)
EBU_YTD=$(cat "$DATA_DIR/ebu_ytd.json" | tr -d '\n')
WEEKLY_EBU_DEDUP=$(cat "$DATA_DIR/weekly_ebu_dedup.json" | tr -d '\n')
WEEKLY_EBU_BY_PARTNER=$(cat "$DATA_DIR/weekly_ebu_by_partner.json" | tr -d '\n')
MISSION_COMPLETIONS=$(cat "$DATA_DIR/mission_completions.json" | tr -d '\n')
WEEKLY_MISSION_COMPLETIONS=$(cat "$DATA_DIR/weekly_mission_completions.json" | tr -d '\n')
REWARD_CLAIMS=$(cat "$DATA_DIR/reward_claims.json" | tr -d '\n')

# Build the BQ_DATA JavaScript object
# Using a heredoc to construct the replacement line
BQ_DATA_JS="const BQ_DATA = {
            ebuYtd: ${EBU_YTD},
            weeklyEbuDedup: ${WEEKLY_EBU_DEDUP},
            weeklyEbuByPartner: ${WEEKLY_EBU_BY_PARTNER},
            missionCompletions: ${MISSION_COMPLETIONS},
            weeklyMissionCompletions: ${WEEKLY_MISSION_COMPLETIONS},
            rewardClaims: ${REWARD_CLAIMS},
            buildTimestamp: \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
        }; // %%BQ_DATA_PLACEHOLDER%%"

echo "✓ BQ_DATA object constructed"

# ─────────────────────────────────────────────
# Inject BQ_DATA into template and write output
# ─────────────────────────────────────────────
echo "Injecting data into template..."

# We need to replace the placeholder line with the actual data.
# The placeholder is: const BQ_DATA = null; // %%BQ_DATA_PLACEHOLDER%%
# Strategy: Use Python for reliable multi-line string replacement

python3 -c "
import sys

template_path = sys.argv[1]
output_path = sys.argv[2]

with open(template_path, 'r') as f:
    content = f.read()

# Find and replace the placeholder line
placeholder = 'const BQ_DATA = null; // %%BQ_DATA_PLACEHOLDER%%'
replacement = '''${BQ_DATA_JS}'''

if placeholder not in content:
    print('ERROR: Placeholder not found in template!')
    print('Looking for:', placeholder)
    sys.exit(1)

content = content.replace(placeholder, replacement)

with open(output_path, 'w') as f:
    f.write(content)

print(f'✓ Written to {output_path}')
" "$TEMPLATE" "$OUTPUT"

echo ""

# ─────────────────────────────────────────────
# Verify output
# ─────────────────────────────────────────────
if [ -f "$OUTPUT" ]; then
    SIZE=$(wc -c < "$OUTPUT" | tr -d ' ')
    LINES=$(wc -l < "$OUTPUT" | tr -d ' ')
    echo "=== BUILD COMPLETE ==="
    echo "Output: $OUTPUT"
    echo "Size:   ${SIZE} bytes / ${LINES} lines"
    echo ""
    
    # Verify BQ_DATA was injected
    if grep -q "buildTimestamp" "$OUTPUT"; then
        echo "✓ BQ_DATA injection verified"
    else
        echo "WARNING: BQ_DATA may not have been injected correctly"
    fi
    
    echo ""
    echo "Next steps:"
    echo "  1. Open $OUTPUT in a browser to verify"
    echo "  2. cd ../Personal-Space && git add . && git commit -m 'Update dashboard data' && git push"
else
    echo "ERROR: Output file was not created"
    exit 1
fi
