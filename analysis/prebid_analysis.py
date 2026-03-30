it's 15%#!/usr/bin/env python3
"""
Prebid Experiment Analysis: Moba vs Publift on CSStats.gg
Period: 25 Feb - 16 Mar 2026
Primary Metric: Revenue per Page View (RPV)
"""

import csv
import json
from collections import defaultdict

# ============================================================
# 1. COUNTRY NAME NORMALIZATION MAP
# Maps GA / revenue file names → canonical name (matching tier file)
# ============================================================
COUNTRY_NORMALIZE = {
    # GA uses these
    "Türkiye": "Turkiye",
    "Bosnia & Herzegovina": "Bosnia and Herzegovina",
    "Congo - Kinshasa": "Democratic Republic of the Congo",
    "St. Kitts & Nevis": "Saint Kitts and Nevis",
    "St. Martin": "Saint Martin",
    "St. Pierre & Miquelon": "Saint Pierre and Miquelon",
    "Trinidad & Tobago": "Trinidad and Tobago",
    "Antigua & Barbuda": "Antigua and Barbuda",
    "Curaçao": "Curacao",
    "Réunion": "Reunion",
    "Åland Islands": "Aland Islands",
    # Moba uses these
    "The Bahamas": "Bahamas",
    # Publift uses these
    "Saint Kitts and Nevis": "Saint Kitts and Nevis",
    "Turks and Caicos Islands": "Turks and Caicos Islands",
}

def normalize(name):
    name = name.strip()
    return COUNTRY_NORMALIZE.get(name, name)


# ============================================================
# 2. LOAD TIER MAPPING
# ============================================================
tiers = {}
with open("Tier country  - Sheet1.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if len(row) >= 2:
            tier = row[0].strip()
            country = normalize(row[1])
            tiers[country] = tier


# ============================================================
# 3. LOAD PAGE VIEWS (GA export)
# ============================================================
pageviews = {}  # country -> {"prebid": int, "publift": int}

with open("Pub_Moba_pageviews.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Data starts at line 9 (0-indexed: line 8), skip header rows
# Line 7 (0-indexed): ads_ab_variant,prebid,publift,(not set),,Totals
# Line 8 (0-indexed): Country,Views,Views,Views,Views,Views
# Line 9 (0-indexed): grand total row (starts with comma)
# Line 10+: country data

data_lines = lines[8:]  # from "Country,Views,..." onward
reader = csv.reader(data_lines)
header = next(reader)  # Country,Views,Views,Views,Views,Views

for row in reader:
    if len(row) < 5:
        continue
    country_raw = row[0].strip()
    if not country_raw or country_raw == "(not set)":
        continue  # skip blank/not-set rows
    
    country = normalize(country_raw)
    
    try:
        prebid_views = int(row[1]) if row[1] else 0
        publift_views = int(row[2]) if row[2] else 0
    except ValueError:
        continue
    
    pageviews[country] = {
        "prebid": prebid_views,
        "publift": publift_views,
    }


# ============================================================
# 4. LOAD MOBA REVENUE
# ============================================================
moba_revenue = {}  # country -> float

with open("Moba report Revenues CSStats.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the "Country,Total revenue" header line
start_idx = None
for i, line in enumerate(lines):
    if line.strip().startswith("Country,Total revenue"):
        start_idx = i
        break

if start_idx is not None:
    data_lines = lines[start_idx:]
    reader = csv.reader(data_lines)
    header = next(reader)  # Country,Total revenue
    
    for row in reader:
        if len(row) < 2:
            continue
        country_raw = row[0].strip()
        if not country_raw:
            continue  # skip blank country (aggregate row)
        
        country = normalize(country_raw)
        try:
            rev = float(row[1]) if row[1] else 0.0
        except ValueError:
            continue
        
        moba_revenue[country] = rev


# ============================================================
# 5. LOAD PUBLIFT REVENUE
# ============================================================
publift_revenue = {}  # country -> float

with open("Publift_CSStats Revenue Report.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = None
for i, line in enumerate(lines):
    if line.strip().startswith("Country,Total revenue"):
        start_idx = i
        break

if start_idx is not None:
    data_lines = lines[start_idx:]
    reader = csv.reader(data_lines)
    header = next(reader)
    
    for row in reader:
        if len(row) < 2:
            continue
        country_raw = row[0].strip()
        if not country_raw:
            continue
        
        country = normalize(country_raw)
        try:
            rev = float(row[1]) if row[1] else 0.0
        except ValueError:
            continue
        
        publift_revenue[country] = rev


# ============================================================
# 6. EXCLUDE RUSSIA & JOIN DATA
# ============================================================
EXCLUDE = {"Russia"}

# All countries across all datasets
all_countries = set()
all_countries.update(pageviews.keys())
all_countries.update(moba_revenue.keys())
all_countries.update(publift_revenue.keys())
all_countries -= EXCLUDE

# Build joined dataset
joined = []
unmatched_tier = []

for country in sorted(all_countries):
    tier = tiers.get(country, "Untiered")
    pv = pageviews.get(country, {"prebid": 0, "publift": 0})
    moba_rev = moba_revenue.get(country, 0.0)
    publift_rev = publift_revenue.get(country, 0.0)
    
    if tier == "Untiered":
        unmatched_tier.append(country)
    
    joined.append({
        "country": country,
        "tier": tier,
        "prebid_views": pv["prebid"],
        "publift_views": pv["publift"],
        "moba_revenue": moba_rev,
        "publift_revenue_gross": publift_rev,
        "publift_revenue_net": publift_rev * 0.85,  # 15% commission deducted
    })


# ============================================================
# 7. AGGREGATE BY TIER
# ============================================================
tier_agg = defaultdict(lambda: {
    "prebid_views": 0,
    "publift_views": 0,
    "moba_revenue": 0.0,
    "publift_revenue_gross": 0.0,
    "publift_revenue_net": 0.0,
    "countries": 0,
})

for row in joined:
    t = row["tier"]
    tier_agg[t]["prebid_views"] += row["prebid_views"]
    tier_agg[t]["publift_views"] += row["publift_views"]
    tier_agg[t]["moba_revenue"] += row["moba_revenue"]
    tier_agg[t]["publift_revenue_gross"] += row["publift_revenue_gross"]
    tier_agg[t]["publift_revenue_net"] += row["publift_revenue_net"]
    tier_agg[t]["countries"] += 1

# Also build "excl. US" variant
tier_agg_no_us = defaultdict(lambda: {
    "prebid_views": 0,
    "publift_views": 0,
    "moba_revenue": 0.0,
    "publift_revenue_gross": 0.0,
    "publift_revenue_net": 0.0,
    "countries": 0,
})

for row in joined:
    if row["country"] == "United States":
        continue
    t = row["tier"]
    tier_agg_no_us[t]["prebid_views"] += row["prebid_views"]
    tier_agg_no_us[t]["publift_views"] += row["publift_views"]
    tier_agg_no_us[t]["moba_revenue"] += row["moba_revenue"]
    tier_agg_no_us[t]["publift_revenue_gross"] += row["publift_revenue_gross"]
    tier_agg_no_us[t]["publift_revenue_net"] += row["publift_revenue_net"]
    tier_agg_no_us[t]["countries"] += 1


# ============================================================
# 8. CALCULATE RPV & eCPM
# ============================================================
def calc_metrics(agg):
    results = {}
    for tier in ["Tier 1", "Tier 2", "Tier 3", "Untiered"]:
        if tier not in agg:
            continue
        d = agg[tier]
        moba_rpv = d["moba_revenue"] / d["prebid_views"] if d["prebid_views"] > 0 else 0
        publift_rpv_gross = d["publift_revenue_gross"] / d["publift_views"] if d["publift_views"] > 0 else 0
        publift_rpv_net = d["publift_revenue_net"] / d["publift_views"] if d["publift_views"] > 0 else 0
        
        # eCPM = RPV * 1000
        moba_ecpm = moba_rpv * 1000
        publift_ecpm_gross = publift_rpv_gross * 1000
        publift_ecpm_net = publift_rpv_net * 1000
        
        # Diff: Moba vs Publift net
        if publift_rpv_net > 0:
            rpv_diff_pct = ((moba_rpv - publift_rpv_net) / publift_rpv_net) * 100
        else:
            rpv_diff_pct = float('inf')
        
        results[tier] = {
            "prebid_views": d["prebid_views"],
            "publift_views": d["publift_views"],
            "moba_revenue": d["moba_revenue"],
            "publift_revenue_gross": d["publift_revenue_gross"],
            "publift_revenue_net": d["publift_revenue_net"],
            "moba_rpv": moba_rpv,
            "publift_rpv_gross": publift_rpv_gross,
            "publift_rpv_net": publift_rpv_net,
            "moba_ecpm": moba_ecpm,
            "publift_ecpm_gross": publift_ecpm_gross,
            "publift_ecpm_net": publift_ecpm_net,
            "rpv_diff_vs_net_pct": rpv_diff_pct,
            "countries": d["countries"],
        }
    return results


results_all = calc_metrics(tier_agg)
results_no_us = calc_metrics(tier_agg_no_us)

# Grand totals
def grand_total(agg):
    gt = {
        "prebid_views": 0, "publift_views": 0,
        "moba_revenue": 0.0, "publift_revenue_gross": 0.0, "publift_revenue_net": 0.0,
    }
    for d in agg.values():
        gt["prebid_views"] += d["prebid_views"]
        gt["publift_views"] += d["publift_views"]
        gt["moba_revenue"] += d["moba_revenue"]
        gt["publift_revenue_gross"] += d["publift_revenue_gross"]
        gt["publift_revenue_net"] += d["publift_revenue_net"]
    
    gt["moba_rpv"] = gt["moba_revenue"] / gt["prebid_views"] if gt["prebid_views"] > 0 else 0
    gt["publift_rpv_gross"] = gt["publift_revenue_gross"] / gt["publift_views"] if gt["publift_views"] > 0 else 0
    gt["publift_rpv_net"] = gt["publift_revenue_net"] / gt["publift_views"] if gt["publift_views"] > 0 else 0
    gt["moba_ecpm"] = gt["moba_rpv"] * 1000
    gt["publift_ecpm_gross"] = gt["publift_rpv_gross"] * 1000
    gt["publift_ecpm_net"] = gt["publift_rpv_net"] * 1000
    if gt["publift_rpv_net"] > 0:
        gt["rpv_diff_vs_net_pct"] = ((gt["moba_rpv"] - gt["publift_rpv_net"]) / gt["publift_rpv_net"]) * 100
    else:
        gt["rpv_diff_vs_net_pct"] = 0
    return gt

gt_all = grand_total(tier_agg)
gt_no_us = grand_total(tier_agg_no_us)


# ============================================================
# 9. US ANOMALY DETAIL
# ============================================================
us_data = None
for row in joined:
    if row["country"] == "United States":
        us_data = row
        break


# ============================================================
# 10. TOP COUNTRIES BY REVENUE (for context)
# ============================================================
top_moba = sorted(joined, key=lambda x: x["moba_revenue"], reverse=True)[:15]
top_publift = sorted(joined, key=lambda x: x["publift_revenue_gross"], reverse=True)[:15]


# ============================================================
# 11. PRINT RESULTS
# ============================================================
def fmt_money(v):
    return f"${v:,.2f}"

def fmt_pct(v):
    return f"{v:+.1f}%"

def fmt_rpv(v):
    return f"${v:.6f}"

def fmt_ecpm(v):
    return f"${v:.4f}"

def fmt_int(v):
    return f"{v:,}"


print("=" * 80)
print("PREBID EXPERIMENT: MOBA vs PUBLIFT — CSStats.gg")
print("Period: 25 Feb – 16 Mar 2026 | Russia excluded")
print("Primary Metric: Revenue per Page View (RPV)")
print("=" * 80)

print("\n" + "─" * 80)
print("SECTION A: TIER-LEVEL ANALYSIS (All Countries, Russia excluded)")
print("─" * 80)

for tier in ["Tier 1", "Tier 2", "Tier 3"]:
    if tier not in results_all:
        continue
    r = results_all[tier]
    print(f"\n  {tier} ({r['countries']} countries)")
    print(f"  {'Metric':<30} {'Moba (Prebid)':>18} {'Publift (Gross)':>18} {'Publift (Net 80%)':>18}")
    print(f"  {'─'*30} {'─'*18} {'─'*18} {'─'*18}")
    print(f"  {'Page Views':<30} {fmt_int(r['prebid_views']):>18} {fmt_int(r['publift_views']):>18} {'':>18}")
    print(f"  {'Revenue':<30} {fmt_money(r['moba_revenue']):>18} {fmt_money(r['publift_revenue_gross']):>18} {fmt_money(r['publift_revenue_net']):>18}")
    print(f"  {'RPV':<30} {fmt_rpv(r['moba_rpv']):>18} {fmt_rpv(r['publift_rpv_gross']):>18} {fmt_rpv(r['publift_rpv_net']):>18}")
    print(f"  {'eCPM (RPV×1000)':<30} {fmt_ecpm(r['moba_ecpm']):>18} {fmt_ecpm(r['publift_ecpm_gross']):>18} {fmt_ecpm(r['publift_ecpm_net']):>18}")
    print(f"  {'Moba vs Publift Net':<30} {fmt_pct(r['rpv_diff_vs_net_pct']):>18}")

print(f"\n  {'GRAND TOTAL':}")
print(f"  {'Metric':<30} {'Moba (Prebid)':>18} {'Publift (Gross)':>18} {'Publift (Net 80%)':>18}")
print(f"  {'─'*30} {'─'*18} {'─'*18} {'─'*18}")
print(f"  {'Page Views':<30} {fmt_int(gt_all['prebid_views']):>18} {fmt_int(gt_all['publift_views']):>18} {'':>18}")
print(f"  {'Revenue':<30} {fmt_money(gt_all['moba_revenue']):>18} {fmt_money(gt_all['publift_revenue_gross']):>18} {fmt_money(gt_all['publift_revenue_net']):>18}")
print(f"  {'RPV':<30} {fmt_rpv(gt_all['moba_rpv']):>18} {fmt_rpv(gt_all['publift_rpv_gross']):>18} {fmt_rpv(gt_all['publift_rpv_net']):>18}")
print(f"  {'eCPM (RPV×1000)':<30} {fmt_ecpm(gt_all['moba_ecpm']):>18} {fmt_ecpm(gt_all['publift_ecpm_gross']):>18} {fmt_ecpm(gt_all['publift_ecpm_net']):>18}")
print(f"  {'Moba vs Publift Net':<30} {fmt_pct(gt_all['rpv_diff_vs_net_pct']):>18}")


print("\n\n" + "─" * 80)
print("SECTION B: TIER-LEVEL ANALYSIS (Excluding US — anomaly removed)")
print("─" * 80)

for tier in ["Tier 1", "Tier 2", "Tier 3"]:
    if tier not in results_no_us:
        continue
    r = results_no_us[tier]
    print(f"\n  {tier} ({r['countries']} countries)")
    print(f"  {'Metric':<30} {'Moba (Prebid)':>18} {'Publift (Gross)':>18} {'Publift (Net 80%)':>18}")
    print(f"  {'─'*30} {'─'*18} {'─'*18} {'─'*18}")
    print(f"  {'Page Views':<30} {fmt_int(r['prebid_views']):>18} {fmt_int(r['publift_views']):>18} {'':>18}")
    print(f"  {'Revenue':<30} {fmt_money(r['moba_revenue']):>18} {fmt_money(r['publift_revenue_gross']):>18} {fmt_money(r['publift_revenue_net']):>18}")
    print(f"  {'RPV':<30} {fmt_rpv(r['moba_rpv']):>18} {fmt_rpv(r['publift_rpv_gross']):>18} {fmt_rpv(r['publift_rpv_net']):>18}")
    print(f"  {'eCPM (RPV×1000)':<30} {fmt_ecpm(r['moba_ecpm']):>18} {fmt_ecpm(r['publift_ecpm_gross']):>18} {fmt_ecpm(r['publift_ecpm_net']):>18}")
    print(f"  {'Moba vs Publift Net':<30} {fmt_pct(r['rpv_diff_vs_net_pct']):>18}")

print(f"\n  {'GRAND TOTAL (excl. US)':}")
print(f"  {'Metric':<30} {'Moba (Prebid)':>18} {'Publift (Gross)':>18} {'Publift (Net 80%)':>18}")
print(f"  {'─'*30} {'─'*18} {'─'*18} {'─'*18}")
print(f"  {'Page Views':<30} {fmt_int(gt_no_us['prebid_views']):>18} {fmt_int(gt_no_us['publift_views']):>18} {'':>18}")
print(f"  {'Revenue':<30} {fmt_money(gt_no_us['moba_revenue']):>18} {fmt_money(gt_no_us['publift_revenue_gross']):>18} {fmt_money(gt_no_us['publift_revenue_net']):>18}")
print(f"  {'RPV':<30} {fmt_rpv(gt_no_us['moba_rpv']):>18} {fmt_rpv(gt_no_us['publift_rpv_gross']):>18} {fmt_rpv(gt_no_us['publift_rpv_net']):>18}")
print(f"  {'eCPM (RPV×1000)':<30} {fmt_ecpm(gt_no_us['moba_ecpm']):>18} {fmt_ecpm(gt_no_us['publift_ecpm_gross']):>18} {fmt_ecpm(gt_no_us['publift_ecpm_net']):>18}")
print(f"  {'Moba vs Publift Net':<30} {fmt_pct(gt_no_us['rpv_diff_vs_net_pct']):>18}")


print("\n\n" + "─" * 80)
print("SECTION C: US REVENUE ANOMALY")
print("─" * 80)

if us_data:
    print(f"\n  Country: United States")
    print(f"  Moba page views:     {fmt_int(us_data['prebid_views'])}")
    print(f"  Publift page views:  {fmt_int(us_data['publift_views'])}")
    print(f"  Moba revenue:        {fmt_money(us_data['moba_revenue'])}")
    print(f"  Publift revenue:     {fmt_money(us_data['publift_revenue_gross'])}")
    print(f"  ")
    moba_us_rpv = us_data['moba_revenue'] / us_data['prebid_views'] if us_data['prebid_views'] > 0 else 0
    pub_us_rpv = us_data['publift_revenue_gross'] / us_data['publift_views'] if us_data['publift_views'] > 0 else 0
    print(f"  Moba RPV:    {fmt_rpv(moba_us_rpv)}  (eCPM: {fmt_ecpm(moba_us_rpv*1000)})")
    print(f"  Publift RPV: {fmt_rpv(pub_us_rpv)}  (eCPM: {fmt_ecpm(pub_us_rpv*1000)})")
    print(f"  ")
    print(f"  FLAG: Moba US revenue is {us_data['moba_revenue']/us_data['publift_revenue_gross']:.0f}x Publift.")
    print(f"  Possible causes:")
    print(f"    - Different ad unit IDs (Moba filters 2 units vs Publift 1 unit)")
    print(f"    - GAM attribution differences")
    print(f"    - Publift may not have US demand partners configured for this unit")
    print(f"  Recommendation: Investigate with Moba/GAM before drawing conclusions from US data.")


print("\n\n" + "─" * 80)
print("SECTION D: TOP 15 COUNTRIES BY REVENUE")
print("─" * 80)

print(f"\n  {'Moba Top 15':}")
print(f"  {'#':<4} {'Country':<30} {'Revenue':>12} {'Views':>12} {'RPV':>12} {'Tier':>8}")
for i, row in enumerate(top_moba, 1):
    rpv = row["moba_revenue"] / row["prebid_views"] if row["prebid_views"] > 0 else 0
    print(f"  {i:<4} {row['country']:<30} {fmt_money(row['moba_revenue']):>12} {fmt_int(row['prebid_views']):>12} {fmt_rpv(rpv):>12} {row['tier']:>8}")

print(f"\n  {'Publift Top 15 (Gross)':}")
print(f"  {'#':<4} {'Country':<30} {'Revenue':>12} {'Views':>12} {'RPV':>12} {'Tier':>8}")
for i, row in enumerate(top_publift, 1):
    rpv = row["publift_revenue_gross"] / row["publift_views"] if row["publift_views"] > 0 else 0
    print(f"  {i:<4} {row['country']:<30} {fmt_money(row['publift_revenue_gross']):>12} {fmt_int(row['publift_views']):>12} {fmt_rpv(rpv):>12} {row['tier']:>8}")


print("\n\n" + "─" * 80)
print("SECTION E: DATA QUALITY NOTES")
print("─" * 80)

print(f"\n  Countries with no tier mapping ({len(unmatched_tier)}):")
for c in sorted(unmatched_tier):
    pv = pageviews.get(c, {"prebid": 0, "publift": 0})
    print(f"    - {c} (prebid views: {fmt_int(pv['prebid'])}, publift views: {fmt_int(pv['publift'])})")

# Check for countries in revenue but not in pageviews
rev_only_moba = set(moba_revenue.keys()) - set(pageviews.keys()) - EXCLUDE
rev_only_publift = set(publift_revenue.keys()) - set(pageviews.keys()) - EXCLUDE
if rev_only_moba:
    print(f"\n  Countries in Moba revenue but NOT in GA page views:")
    for c in sorted(rev_only_moba):
        print(f"    - {c} (revenue: {fmt_money(moba_revenue[c])})")
if rev_only_publift:
    print(f"\n  Countries in Publift revenue but NOT in GA page views:")
    for c in sorted(rev_only_publift):
        print(f"    - {c} (revenue: {fmt_money(publift_revenue[c])})")

# Countries in GA but not in either revenue file
pv_only = set(pageviews.keys()) - set(moba_revenue.keys()) - set(publift_revenue.keys()) - EXCLUDE
if pv_only:
    print(f"\n  Countries in GA page views but NOT in any revenue file:")
    for c in sorted(pv_only):
        pv = pageviews[c]
        print(f"    - {c} (prebid: {fmt_int(pv['prebid'])}, publift: {fmt_int(pv['publift'])})")


print("\n\n" + "─" * 80)
print("SECTION F: SUMMARY & RECOMMENDATION")
print("─" * 80)

print(f"""
  EXECUTIVE SUMMARY (Russia excluded, 25 Feb – 16 Mar 2026)
  
  Including US:
    Moba RPV:           {fmt_rpv(gt_all['moba_rpv'])}  (eCPM: {fmt_ecpm(gt_all['moba_ecpm'])})
    Publift RPV (net):  {fmt_rpv(gt_all['publift_rpv_net'])}  (eCPM: {fmt_ecpm(gt_all['publift_ecpm_net'])})
    Moba vs Publift:    {fmt_pct(gt_all['rpv_diff_vs_net_pct'])}
  
  Excluding US (anomaly):
    Moba RPV:           {fmt_rpv(gt_no_us['moba_rpv'])}  (eCPM: {fmt_ecpm(gt_no_us['moba_ecpm'])})
    Publift RPV (net):  {fmt_rpv(gt_no_us['publift_rpv_net'])}  (eCPM: {fmt_ecpm(gt_no_us['publift_ecpm_net'])})
    Moba vs Publift:    {fmt_pct(gt_no_us['rpv_diff_vs_net_pct'])}
  
  KEY FINDINGS:
  1. After accounting for Publift's ~20% commission, Moba's net position changes
  2. The US revenue anomaly ($67.84 Moba vs $0.29 Publift) requires investigation
  3. Tier-level analysis reveals different dynamics across market tiers
  4. Fill rate comparison is unreliable (Publift uses GAM placeholder line item)
  
  RECOMMENDATION:
  [See presentation for final recommendation based on tier-level analysis]
""")


# ============================================================
# 12. EXPORT DATA FOR HTML PRESENTATION
# ============================================================
export = {
    "period": "25 Feb – 16 Mar 2026",
    "exclusions": ["Russia"],
    "results_all": {},
    "results_no_us": {},
    "grand_total_all": gt_all,
    "grand_total_no_us": gt_no_us,
    "us_anomaly": None,
    "unmatched_tier_countries": unmatched_tier,
}

for tier in results_all:
    export["results_all"][tier] = results_all[tier]
for tier in results_no_us:
    export["results_no_us"][tier] = results_no_us[tier]

if us_data:
    export["us_anomaly"] = us_data

with open("prebid_analysis_data.json", "w") as f:
    json.dump(export, f, indent=2, default=str)

print("\n  Data exported to prebid_analysis_data.json for HTML presentation generation.")
print("=" * 80)
