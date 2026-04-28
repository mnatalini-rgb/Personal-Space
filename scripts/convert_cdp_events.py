#!/usr/bin/env python3
"""
Convert CDP Snowflake CSV exports into a compact JSON for the NSM dashboard.

Input:
  - events CSV  (wide format: event_type, user_id, week1_users, week1_events, ...)
  - country CSV (user_id, country)

Output:
  - data/bq_exports/cdp_tradeit_signals.json

Structure:
  [
    { "week": "2026-04-13", "region": "EU", "event_type": "trade", "distinct_users": 123, "total_events": 456 },
    ...
  ]
"""

import csv
import json
import sys
import os
from collections import defaultdict

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_CSV = os.path.join(PROJECT_DIR, "data", "brand_integrations",
    "faceit_snowflake_analytics rep__cdp_service__user_events 2026-04-20T1250.csv")
COUNTRY_CSV = os.path.join(PROJECT_DIR, "data", "brand_integrations",
    "faceit_snowflake_analytics rep__cdp_service__user_events 2026-04-20T1255.csv")
OUTPUT_JSON = os.path.join(PROJECT_DIR, "data", "bq_exports", "cdp_tradeit_signals.json")

# Tradeit commercial region mapping (country ISO2 -> region)
CIS_COUNTRIES = {'RU', 'BY', 'KZ', 'UA', 'UZ', 'KG', 'TJ', 'TM', 'AM', 'AZ', 'GE', 'MD'}
CIS_EXC_COUNTRIES = CIS_COUNTRIES - {'RU'}  # CIS excluding Russia

EU_COUNTRIES = {
    'AL', 'AD', 'AT', 'BA', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FO',
    'FR', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'XK', 'LV', 'LI', 'LT', 'LU',
    'MK', 'MT', 'MC', 'ME', 'NL', 'NO', 'PL', 'PT', 'RO', 'SM', 'RS', 'SK',
    'SI', 'ES', 'SE', 'CH', 'GB', 'VA', 'GI', 'GG', 'IM', 'JE', 'AX',
    'TR',  # Turkey → EU per user confirmation
}

NA_COUNTRIES = {'US', 'CA'}

LATAM_COUNTRIES = {
    'AR', 'BO', 'BR', 'CL', 'CO', 'CR', 'CU', 'DO', 'EC', 'SV', 'GT', 'HN',
    'MX', 'NI', 'PA', 'PY', 'PE', 'PR', 'UY', 'VE', 'GY', 'SR', 'BZ',
    'GF', 'GP', 'MQ', 'HT', 'JM', 'TT', 'BB', 'BS', 'AG', 'DM', 'GD',
    'KN', 'LC', 'VC', 'AW', 'CW', 'SX', 'BQ', 'TC', 'VG', 'VI', 'AI',
    'BM', 'KY', 'MS', 'MF', 'BL', 'PM',
}

MENA_COUNTRIES = {
    'DZ', 'BH', 'EG', 'IQ', 'IR', 'IL', 'JO', 'KW', 'LB', 'LY', 'MA',
    'OM', 'PS', 'QA', 'SA', 'SD', 'SY', 'TN', 'AE', 'YE', 'EH',
}

APAC_COUNTRIES = {
    'AF', 'AU', 'BD', 'BN', 'BT', 'KH', 'CN', 'FJ', 'HK', 'IN', 'ID',
    'JP', 'KR', 'KP', 'LA', 'MO', 'MY', 'MV', 'MN', 'MM', 'NP', 'NZ',
    'PK', 'PG', 'PH', 'SG', 'LK', 'TW', 'TH', 'TL', 'VN', 'WS', 'TO',
    'FM', 'KI', 'MH', 'NR', 'NU', 'PW', 'SB', 'TV', 'VU', 'CK', 'PF',
    'NC', 'AS', 'GU', 'MP', 'CC', 'CX', 'NF', 'HM',
}


def country_to_region(country_code):
    if not country_code:
        return None
    c = country_code.upper().strip()
    if c == 'RU':
        return 'CIS'
    if c in CIS_EXC_COUNTRIES:
        return 'CIS EXC'
    if c in EU_COUNTRIES:
        return 'EU'
    if c in NA_COUNTRIES:
        return 'NA'
    if c in LATAM_COUNTRIES:
        return 'LATAM'
    if c in MENA_COUNTRIES:
        return 'MENA'
    if c in APAC_COUNTRIES:
        return 'APAC'
    # Fallback: African + other countries not in any Tradeit region
    return None


def main():
    # Step 1: Load country mapping
    print("Loading country mapping...")
    user_country = {}
    with open(COUNTRY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) >= 2:
                uid = row[0].strip()
                country = row[1].strip() if row[1].strip() else None
                if uid:
                    user_country[uid] = country
    print(f"  {len(user_country)} users loaded, {sum(1 for v in user_country.values() if v)} with country")

    # Step 2: Parse header to extract week dates
    print("Parsing events CSV header...")
    with open(EVENTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header_row1 = next(reader)  # Week dates (repeated pairs)
        header_row2 = next(reader)  # Column labels

    # header_row1: ['', 'Event Created At Week', '2026-04-13', '2026-04-13', '2026-04-06', ...]
    # Pairs of (Distinct Users, Unique Events) per week
    weeks = []
    for i in range(2, len(header_row1), 2):
        week_date = header_row1[i].strip()
        if week_date:
            weeks.append(week_date)
    print(f"  {len(weeks)} weeks: {weeks[-1]} → {weeks[0]}")

    # Step 3: Parse events and aggregate by (event_type, region, week)
    print("Processing events...")
    # agg[event_type][region][week] = { users: set(), events: int }
    agg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'users': set(), 'events': 0})))

    row_count = 0
    unmapped_users = set()
    with open(EVENTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row 1
        next(reader)  # skip header row 2
        for row in reader:
            if len(row) < 3:
                continue
            event_type = row[0].strip()
            user_id = row[1].strip()
            if not event_type or not user_id:
                continue

            country = user_country.get(user_id)
            region = country_to_region(country)
            if region is None:
                unmapped_users.add(user_id)
                region = 'OTHER'

            # Parse week columns (pairs: distinct_users, unique_events)
            for wi, week in enumerate(weeks):
                col_users = 2 + wi * 2
                col_events = 3 + wi * 2
                if col_events >= len(row):
                    break
                du = row[col_users].strip()
                ue = row[col_events].strip()
                if du and int(du) > 0:
                    agg[event_type][region][week]['users'].add(user_id)
                    agg[event_type][region][week]['events'] += int(ue) if ue else 0

            row_count += 1
            if row_count % 100000 == 0:
                print(f"  ... {row_count} rows processed")

    print(f"  {row_count} total rows processed")
    print(f"  {len(unmapped_users)} users with no region mapping → grouped as OTHER")

    # Step 4: Flatten to JSON array
    print("Building JSON output...")
    output = []
    for event_type in sorted(agg.keys()):
        for region in sorted(agg[event_type].keys()):
            for week in sorted(agg[event_type][region].keys()):
                entry = agg[event_type][region][week]
                output.append({
                    'week': week,
                    'region': region,
                    'event_type': event_type,
                    'distinct_users': len(entry['users']),
                    'total_events': entry['events']
                })

    print(f"  {len(output)} aggregate rows")

    # Step 5: Write output
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, separators=(',', ':'))

    size_kb = os.path.getsize(OUTPUT_JSON) / 1024
    print(f"\n✓ Written to {OUTPUT_JSON} ({size_kb:.0f} KB, {len(output)} rows)")

    # Summary stats
    print("\nSummary by event type:")
    for et in sorted(agg.keys()):
        total_users = set()
        for region in agg[et]:
            for week in agg[et][region]:
                total_users.update(agg[et][region][week]['users'])
        print(f"  {et}: {len(total_users):,} unique users")

    print("\nSummary by region:")
    region_totals = defaultdict(set)
    for et in agg:
        for region in agg[et]:
            for week in agg[et][region]:
                region_totals[region].update(agg[et][region][week]['users'])
    for region in sorted(region_totals.keys()):
        print(f"  {region}: {len(region_totals[region]):,} unique users")


if __name__ == '__main__':
    main()
