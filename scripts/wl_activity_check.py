#!/usr/bin/env python3
"""Query last match activity for Winline-linked FACEIT users via batched BQ queries."""

import csv
import json
import subprocess
import sys
from collections import defaultdict

CSV_PATH = "data/brand_integrations/faceit_snowflake_analytics rep__cdp_service__user_events 2026-04-23T1549.csv"
BQ = "/opt/homebrew/bin/bq"
BATCH_SIZE = 5000

def load_user_ids(path):
    ids = []
    with open(path, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and row[0].strip():
                ids.append(row[0].strip())
    return ids

def run_bq_batch(user_ids):
    id_list = ", ".join(f"'{uid}'" for uid in user_ids)
    query = f"""
SELECT
  activity_bucket,
  COUNT(*) as user_count,
  SUM(total_matches) as total_matches
FROM (
  SELECT
    uid,
    CASE
      WHEN h.last_finished_match_at IS NULL THEN 'never_played'
      WHEN h.last_finished_match_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY) THEN 'active_7d'
      WHEN h.last_finished_match_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY) THEN 'active_30d'
      WHEN h.last_finished_match_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY) THEN 'active_90d'
      WHEN h.last_finished_match_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 180 DAY) THEN 'active_180d'
      WHEN h.last_finished_match_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY) THEN 'active_365d'
      ELSE 'inactive_over_1y'
    END as activity_bucket,
    IFNULL(h.matches_finished, 0) as total_matches
  FROM UNNEST([{id_list}]) AS uid
  LEFT JOIN `business-intelligence-prod.dbt_user.dim__user_match_history` h
    ON h.user_id = uid
)
GROUP BY activity_bucket
"""
    result = subprocess.run(
        [BQ, "query", "--use_legacy_sql=false", "--format=prettyjson", "--max_rows=20"],
        input=query, capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        print(f"  BQ error: {result.stderr[:200]}", file=sys.stderr)
        return None
    return json.loads(result.stdout)

def main():
    print("Loading user IDs...")
    user_ids = load_user_ids(CSV_PATH)
    total = len(user_ids)
    print(f"  {total:,} Winline-linked users")

    batches = [user_ids[i:i+BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]
    print(f"  {len(batches)} batches of {BATCH_SIZE}")
    print()

    agg = defaultdict(lambda: {"user_count": 0, "total_matches": 0})

    for i, batch in enumerate(batches):
        pct = (i + 1) / len(batches) * 100
        print(f"\r  [{i+1}/{len(batches)}] ({pct:.0f}%) Querying batch...", end="", flush=True)
        rows = run_bq_batch(batch)
        if rows:
            for row in rows:
                bucket = row["activity_bucket"]
                agg[bucket]["user_count"] += int(row["user_count"])
                agg[bucket]["total_matches"] += int(row["total_matches"])

    print("\n")

    bucket_order = [
        "active_7d", "active_30d", "active_90d",
        "active_180d", "active_365d", "inactive_over_1y", "never_played"
    ]
    bucket_labels = {
        "active_7d": "Active (last 7 days)",
        "active_30d": "Active (8-30 days)",
        "active_90d": "Active (31-90 days)",
        "active_180d": "Active (91-180 days)",
        "active_365d": "Active (181-365 days)",
        "inactive_over_1y": "Inactive (>1 year)",
        "never_played": "Never played on FACEIT",
    }

    total_found = sum(v["user_count"] for v in agg.values())
    total_matches = sum(v["total_matches"] for v in agg.values())

    print("=" * 65)
    print(f"  WINLINE ACCOUNT LINKAGE — FACEIT ACTIVITY STATUS")
    print(f"  Users analyzed: {total_found:,} / {total:,}")
    print(f"  Total lifetime matches: {total_matches:,}")
    print("=" * 65)
    print(f"  {'Bucket':<30} {'Users':>10} {'%':>8} {'Matches':>12}")
    print("-" * 65)

    for bucket in bucket_order:
        data = agg.get(bucket, {"user_count": 0, "total_matches": 0})
        pct = data["user_count"] / total_found * 100 if total_found else 0
        print(f"  {bucket_labels[bucket]:<30} {data['user_count']:>10,} {pct:>7.1f}% {data['total_matches']:>12,}")

    print("-" * 65)

    active_30 = agg.get("active_7d", {}).get("user_count", 0) + agg.get("active_30d", {}).get("user_count", 0)
    active_90 = active_30 + agg.get("active_90d", {}).get("user_count", 0)
    print(f"\n  MAU (30d active): {active_30:,} ({active_30/total_found*100:.1f}%)" if total_found else "")
    print(f"  QAU (90d active): {active_90:,} ({active_90/total_found*100:.1f}%)" if total_found else "")

    results = {
        "total_wl_users": total,
        "total_matched": total_found,
        "total_lifetime_matches": total_matches,
        "buckets": {b: agg.get(b, {"user_count": 0, "total_matches": 0}) for b in bucket_order}
    }
    with open("data/brand_integrations/wl_activity_status.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to data/brand_integrations/wl_activity_status.json")

if __name__ == "__main__":
    main()
