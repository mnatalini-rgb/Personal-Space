#!/bin/bash
# Roadmap Dashboard Data Refresh Script
# Pulls Jira tickets from Board 222 (AD project) and outputs JSON
# for the roadmap-dashboard.html to consume.
#
# Usage: ./scripts/refresh-roadmap.sh
# Requires: jira-cli installed + JIRA_API_TOKEN env var set
#
# Output: data/jira_exports/roadmap_tickets.json
#
# Last updated: 2026-04-03

set -euo pipefail

OUTPUT_DIR="$(dirname "$0")/../data/jira_exports"
mkdir -p "$OUTPUT_DIR"

echo "=== Roadmap Data Refresh (Jira) ==="
echo "Project: AD | Board: 222"
echo "Output:  $OUTPUT_DIR"
echo "Time:    $(date)"
echo ""

# Check jira-cli is available
if ! command -v jira &> /dev/null; then
  echo "ERROR: jira-cli not found. Install with: brew install ankitpokhrel/jira-cli/jira-cli"
  exit 1
fi

# Check JIRA_API_TOKEN
if [ -z "${JIRA_API_TOKEN:-}" ]; then
  echo "ERROR: JIRA_API_TOKEN not set. Export it before running:"
  echo "  export JIRA_API_TOKEN='your-token'"
  exit 1
fi

# ─────────────────────────────────────────────
# 1. Active tickets (In Progress, Review, To Do)
# ─────────────────────────────────────────────
echo "[1/4] Active tickets (In Progress + Review + To Do)..."
jira issue list \
  --project AD \
  --jql 'project = AD AND status IN ("In Progress", "Review", "To Do") ORDER BY priority ASC, updated DESC' \
  --plain \
  --no-headers \
  --columns key,summary,status,assignee,priority,type,created,updated \
  2>/dev/null > "$OUTPUT_DIR/active_tickets.tsv" || true

ACTIVE_COUNT=$(wc -l < "$OUTPUT_DIR/active_tickets.tsv" | tr -d ' ')
echo "  Found $ACTIVE_COUNT active tickets"

# ─────────────────────────────────────────────
# 2. Recently completed tickets (last 30 days)
# ─────────────────────────────────────────────
echo "[2/4] Recently completed tickets (last 30 days)..."
jira issue list \
  --project AD \
  --jql 'project = AD AND status = "Done" AND updated >= -30d ORDER BY updated DESC' \
  --plain \
  --no-headers \
  --columns key,summary,status,assignee,priority,type,created,updated \
  2>/dev/null > "$OUTPUT_DIR/done_tickets.tsv" || true

DONE_COUNT=$(wc -l < "$OUTPUT_DIR/done_tickets.tsv" | tr -d ' ')
echo "  Found $DONE_COUNT recently completed tickets"

# ─────────────────────────────────────────────
# 3. Sprint data from board
# ─────────────────────────────────────────────
echo "[3/4] Active sprints from Board 222..."
jira sprint list \
  --board 222 \
  --state active,future \
  --plain \
  --no-headers \
  2>/dev/null > "$OUTPUT_DIR/sprints.tsv" || true

SPRINT_COUNT=$(wc -l < "$OUTPUT_DIR/sprints.tsv" | tr -d ' ')
echo "  Found $SPRINT_COUNT active/future sprints"

# ─────────────────────────────────────────────
# 4. Peripherals + Skin Vault specific tickets
#    (key project areas for roadmap)
# ─────────────────────────────────────────────
echo "[4/4] Key initiative tickets (Peripherals + Skin Vault)..."
jira issue list \
  --project AD \
  --jql 'project = AD AND (summary ~ "Peripheral*" OR summary ~ "Skin*" OR summary ~ "skin*" OR summary ~ "peripheral*") AND status != "Done" ORDER BY priority ASC' \
  --plain \
  --no-headers \
  --columns key,summary,status,assignee,priority,type \
  2>/dev/null > "$OUTPUT_DIR/key_initiatives.tsv" || true

KEY_COUNT=$(wc -l < "$OUTPUT_DIR/key_initiatives.tsv" | tr -d ' ')
echo "  Found $KEY_COUNT key initiative tickets"

# ─────────────────────────────────────────────
# Convert to JSON summary
# ─────────────────────────────────────────────
echo ""
echo "Converting to JSON..."

python3 -c "
import json, csv, sys, os
from datetime import datetime

output_dir = '$OUTPUT_DIR'

def parse_tsv(filename):
    filepath = os.path.join(output_dir, filename)
    rows = []
    if not os.path.exists(filepath):
        return rows
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 6:
                rows.append({
                    'key': parts[0].strip(),
                    'summary': parts[1].strip(),
                    'status': parts[2].strip(),
                    'assignee': parts[3].strip() if len(parts) > 3 else '',
                    'priority': parts[4].strip() if len(parts) > 4 else '',
                    'type': parts[5].strip() if len(parts) > 5 else ''
                })
    return rows

# Map assignee names to team member IDs
ASSIGNEE_MAP = {
    'anouk lubbers': 'anouk',
    'isabel diezma': 'isabel',
    'isabel diezma perez': 'isabel',
    'egor shestakov': 'egor',
    'teodor kuzmanov': 'teodor',
    'omar del real ouldam': 'omar',
    'moritz natalini': 'moritz',
    'ilya rabchynski': None  # left the team
}

def map_assignee(name):
    if not name:
        return None
    return ASSIGNEE_MAP.get(name.lower().strip(), name.lower().strip())

active = parse_tsv('active_tickets.tsv')
done = parse_tsv('done_tickets.tsv')
key_init = parse_tsv('key_initiatives.tsv')

# Build roadmap JSON
roadmap = {
    'refreshed_at': datetime.now().isoformat(),
    'active_tickets': [{**t, 'memberId': map_assignee(t.get('assignee', ''))} for t in active],
    'done_tickets': [{**t, 'memberId': map_assignee(t.get('assignee', ''))} for t in done],
    'key_initiatives': [{**t, 'memberId': map_assignee(t.get('assignee', ''))} for t in key_init],
    'summary': {
        'total_active': len(active),
        'total_done_30d': len(done),
        'key_initiatives': len(key_init),
        'by_assignee': {}
    }
}

# Count per assignee
for t in active:
    assignee = t.get('assignee', 'Unassigned') or 'Unassigned'
    roadmap['summary']['by_assignee'][assignee] = roadmap['summary']['by_assignee'].get(assignee, 0) + 1

with open(os.path.join(output_dir, 'roadmap_tickets.json'), 'w') as f:
    json.dump(roadmap, f, indent=2)

print(f'  Wrote roadmap_tickets.json ({len(active)} active, {len(done)} done, {len(key_init)} key)')
"

echo ""
echo "=== ROADMAP REFRESH DONE ==="
echo "Output: $OUTPUT_DIR/roadmap_tickets.json"
echo ""
echo "Files:"
ls -lh "$OUTPUT_DIR"/ 2>/dev/null || true
echo ""
echo "Next: Open roadmap-dashboard.html and manually update sprint assignments"
echo "      based on the Jira data in roadmap_tickets.json"
echo ""
echo "Tip: To auto-inject into dashboard, run:"
echo "  cat $OUTPUT_DIR/roadmap_tickets.json | python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin)))'"
