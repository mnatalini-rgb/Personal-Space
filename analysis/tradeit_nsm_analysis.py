
# Tradeit Mission NSM Analysis — Jan, Feb & Mar 2026
# Primary metric: € Value per conversion (replaces deprecated OVU formula)
# € per 1K EBU = normalised rate for cross-region/month comparison
#
# Tracking cadence: 30-day rolling window (March 2026 onwards)
# Monthly aggregation below serves as input for the rolling calculation.
# The NSM dashboard computes the rolling 30-day window from daily BQ data;
# this script provides the per-mission breakdown and static analysis.

EURO_PER_CONVERSION = {
    "AL": 0.38,        # Account Linkage
    "C1_trade1": 0.04, # Trade any item
    "C2_trade250": 8.75,# Trade $250+
    "C3_trade1000": 35.00, # Trade $1,000+ (not tracked in current missions — future opportunity)
    "C4_trade5": 0.18, # Trade 5 items (not tracked in current missions)
}

# (month, region, segment, joined, tasks[])
# tasks: [{task, action, completed, prizes_claimed}]
missions = [
    # ── JAN 2026 ──
    ("Jan", "North America", "TOFU-A", 21533, [
        {"task": 1, "action": "Play 1 game", "completed": 18292, "prizes_claimed": 866},
        {"task": 2, "action": "Trade any item", "completed": 176, "prizes_claimed": 175},
        {"task": 3, "action": "Trade $250+", "completed": 19, "prizes_claimed": 19},
    ]),
    ("Jan", "North America", "TOFU-B", 21667, [
        {"task": 1, "action": "Play 1 game", "completed": 18410, "prizes_claimed": 956},
        {"task": 2, "action": "Trade any item", "completed": 221, "prizes_claimed": 220},
        {"task": 3, "action": "Trade $250+", "completed": 17, "prizes_claimed": 17},
    ]),
    ("Jan", "North America", "MOFU", 5757, [
        {"task": 1, "action": "Play 1 game", "completed": 5179, "prizes_claimed": 5177},
        {"task": 2, "action": "Trade any item", "completed": 98, "prizes_claimed": 98},
        {"task": 3, "action": "Trade $250+", "completed": 14, "prizes_claimed": 14},
    ]),
    ("Jan", "North America", "BOFU", 4540, [
        {"task": 1, "action": "Play 1 game", "completed": 4072, "prizes_claimed": 4070},
        {"task": 2, "action": "Trade $250+", "completed": 231, "prizes_claimed": 231},
    ]),
    ("Jan", "CIS", "TOFU", 385376, [
        {"task": 1, "action": "Play 1 game", "completed": 360007, "prizes_claimed": 6285},
        {"task": 2, "action": "Trade any item", "completed": 1190, "prizes_claimed": 1190},
        {"task": 3, "action": "Trade $250+", "completed": 65, "prizes_claimed": 65},
    ]),
    ("Jan", "CIS", "MOFU", 55297, [
        {"task": 1, "action": "Play 1 game", "completed": 52508, "prizes_claimed": 52488},
        {"task": 2, "action": "Trade any item", "completed": 485, "prizes_claimed": 483},
        {"task": 3, "action": "Trade $250+", "completed": 18, "prizes_claimed": 18},
    ]),
    ("Jan", "CIS", "BOFU", 23588, [
        {"task": 1, "action": "Play 1 game", "completed": 22421, "prizes_claimed": 22416},
        {"task": 2, "action": "Trade $250+", "completed": 332, "prizes_claimed": 332},
    ]),
    ("Jan", "MENA", "TOFU", 14626, [
        {"task": 1, "action": "Play 1 game", "completed": 12830, "prizes_claimed": 608},
        {"task": 2, "action": "Trade any item", "completed": 164, "prizes_claimed": 164},
        {"task": 3, "action": "Trade $250+", "completed": 13, "prizes_claimed": 13},
    ]),
    ("Jan", "MENA", "MOFU", 2017, [
        {"task": 1, "action": "Play 1 game", "completed": 1853, "prizes_claimed": 1851},
        {"task": 2, "action": "Trade any item", "completed": 59, "prizes_claimed": 59},
        {"task": 3, "action": "Trade $250+", "completed": 3, "prizes_claimed": 3},
    ]),
    ("Jan", "MENA", "BOFU", 1414, [
        {"task": 1, "action": "Play 1 game", "completed": 1293, "prizes_claimed": 1291},
        {"task": 2, "action": "Trade $250+", "completed": 57, "prizes_claimed": 57},
    ]),
    ("Jan", "APAC", "TOFU", 48715, [
        {"task": 1, "action": "Play 1 game", "completed": 42603, "prizes_claimed": 1052},
        {"task": 2, "action": "Trade any item", "completed": 206, "prizes_claimed": 206},
        {"task": 3, "action": "Trade $250+", "completed": 19, "prizes_claimed": 19},
    ]),
    ("Jan", "APAC", "MOFU", 3960, [
        {"task": 1, "action": "Play 1 game", "completed": 3675, "prizes_claimed": 3671},
        {"task": 2, "action": "Trade any item", "completed": 75, "prizes_claimed": 75},
        {"task": 3, "action": "Trade $250+", "completed": 10, "prizes_claimed": 10},
    ]),
    ("Jan", "APAC", "BOFU", 2224, [
        {"task": 1, "action": "Play 1 game", "completed": 2043, "prizes_claimed": 2041},
        {"task": 2, "action": "Trade $250+", "completed": 62, "prizes_claimed": 62},
    ]),

    # ── FEB 2026 ──
    ("Feb", "North America", "TOFU", 47078, [
        {"task": 1, "action": "Play 1 game", "completed": 39972, "prizes_claimed": 1924},
        {"task": 2, "action": "Trade any item", "completed": 491, "prizes_claimed": 490},
        {"task": 3, "action": "Trade $250+", "completed": 41, "prizes_claimed": 41},
    ]),
    ("Feb", "North America", "MOFU", 5764, [
        {"task": 1, "action": "Play 1 game", "completed": 5133, "prizes_claimed": 5130},
        {"task": 2, "action": "Trade any item", "completed": 93, "prizes_claimed": 93},
        {"task": 3, "action": "Trade $250+", "completed": 11, "prizes_claimed": 11},
    ]),
    ("Feb", "North America", "BOFU", 4543, [
        {"task": 1, "action": "Play 1 game", "completed": 4036, "prizes_claimed": 4036},
        {"task": 2, "action": "Trade $250+", "completed": 179, "prizes_claimed": 179},
    ]),
    ("Feb", "CIS", "TOFU", 390909, [
        {"task": 1, "action": "Play 1 game", "completed": 364668, "prizes_claimed": 9025},
        {"task": 2, "action": "Trade any item", "completed": 1826, "prizes_claimed": 1825},
        {"task": 3, "action": "Trade $250+", "completed": 112, "prizes_claimed": 112},
    ]),
    ("Feb", "CIS", "MOFU", 58106, [
        {"task": 1, "action": "Play 1 game", "completed": 55082, "prizes_claimed": 55045},
        {"task": 2, "action": "Trade any item", "completed": 647, "prizes_claimed": 646},
        {"task": 3, "action": "Trade $250+", "completed": 18, "prizes_claimed": 18},
    ]),
    ("Feb", "CIS", "BOFU", 24923, [
        {"task": 1, "action": "Play 1 game", "completed": 23649, "prizes_claimed": 23635},
        {"task": 2, "action": "Trade $250+", "completed": 347, "prizes_claimed": 347},
    ]),
    ("Feb", "MENA", "TOFU", 14746, [
        {"task": 1, "action": "Play 1 game", "completed": 13180, "prizes_claimed": 608},
        {"task": 2, "action": "Trade any item", "completed": 179, "prizes_claimed": 179},
        {"task": 3, "action": "Trade $250+", "completed": 6, "prizes_claimed": 6},
    ]),
    ("Feb", "MENA", "MOFU", 2236, [
        {"task": 1, "action": "Play 1 game", "completed": 2095, "prizes_claimed": 2094},
        {"task": 2, "action": "Trade any item", "completed": 55, "prizes_claimed": 55},
        {"task": 3, "action": "Trade $250+", "completed": 0, "prizes_claimed": 0},
    ]),
    ("Feb", "MENA", "BOFU", 1629, [
        {"task": 1, "action": "Play 1 game", "completed": 1513, "prizes_claimed": 1512},
        {"task": 2, "action": "Trade $250+", "completed": 71, "prizes_claimed": 71},
    ]),
    ("Feb", "APAC", "TOFU", 44513, [
        {"task": 1, "action": "Play 1 game", "completed": 38724, "prizes_claimed": 966},
        {"task": 2, "action": "Trade any item", "completed": 207, "prizes_claimed": 207},
        {"task": 3, "action": "Trade $250+", "completed": 21, "prizes_claimed": 21},
    ]),
    ("Feb", "APAC", "MOFU", 3906, [
        {"task": 1, "action": "Play 1 game", "completed": 3595, "prizes_claimed": 3590},
        {"task": 2, "action": "Trade any item", "completed": 58, "prizes_claimed": 58},
        {"task": 3, "action": "Trade $250+", "completed": 6, "prizes_claimed": 6},
    ]),
    ("Feb", "APAC", "BOFU", 2174, [
        {"task": 1, "action": "Play 1 game", "completed": 2001, "prizes_claimed": 2000},
        {"task": 2, "action": "Trade $250+", "completed": 64, "prizes_claimed": 64},
    ]),
]


def extract_conversions(segment, tasks):
    # TOFU: AL = Task 1 prizes_claimed (implicit linkage), C1 = Task 2 completed, C2 = Task 3 completed
    # MOFU: AL = 0 (already linked), C1 = Task 2 completed, C2 = Task 3 completed
    # BOFU: AL = 0, C1 = 0 (already traded), C2 = Task 2 completed
    seg = segment.upper().replace("-A", "").replace("-B", "")
    if seg == "TOFU":
        return {
            "AL": tasks[0]["prizes_claimed"],
            "C1": tasks[1]["completed"] if len(tasks) > 1 else 0,
            "C2": tasks[2]["completed"] if len(tasks) > 2 else 0,
        }
    elif seg == "MOFU":
        return {
            "AL": 0,
            "C1": tasks[1]["completed"] if len(tasks) > 1 else 0,
            "C2": tasks[2]["completed"] if len(tasks) > 2 else 0,
        }
    elif seg == "BOFU":
        return {
            "AL": 0,
            "C1": 0,
            "C2": tasks[1]["completed"] if len(tasks) > 1 else 0,
        }
    return {"AL": 0, "C1": 0, "C2": 0}


def calc_euro(conv):
    # € = AL × €0.38  +  C1 × €0.04  +  C2 × €8.75
    # C3 (Trade $1,000+) and C4 (Trade 5) not tracked in current missions
    return (
        EURO_PER_CONVERSION["AL"] * conv["AL"]
        + EURO_PER_CONVERSION["C1_trade1"] * conv["C1"]
        + EURO_PER_CONVERSION["C2_trade250"] * conv["C2"]
    )


results = []
for month, region, segment, joined, tasks in missions:
    conv = extract_conversions(segment, tasks)
    euro = calc_euro(conv)
    ebu = joined
    euro_per_1k = (euro / ebu * 1000) if ebu > 0 else 0
    results.append({
        "month": month, "region": region, "segment": segment, "ebu": ebu,
        "task1_completed": tasks[0]["completed"],
        "task1_prizes": tasks[0]["prizes_claimed"],
        "AL": conv["AL"], "C1": conv["C1"], "C2": conv["C2"],
        "euro": round(euro, 2),
        "euro_per_1k_ebu": round(euro_per_1k, 2),
    })


def print_section(title):
    print(f"\n{'='*90}")
    print(f"  {title}")
    print(f"{'='*90}")


def print_table(headers, rows, widths=None):
    if not widths:
        widths = [max(len(str(h)), max(len(str(r[i])) for r in rows)) + 2
                  for i, h in enumerate(headers)]
    print("".join(str(h).ljust(w) for h, w in zip(headers, widths)))
    print("-" * sum(widths))
    for row in rows:
        print("".join(str(v).ljust(w) for v, w in zip(row, widths)))


def merge_tofu_ab(results_list, month, region):
    tofu_a = [r for r in results_list if r["month"] == month and r["region"] == region and r["segment"] == "TOFU-A"]
    tofu_b = [r for r in results_list if r["month"] == month and r["region"] == region and r["segment"] == "TOFU-B"]
    others = [r for r in results_list if r["month"] == month and r["region"] == region and "TOFU" not in r["segment"]]
    merged = []
    if tofu_a and tofu_b:
        a, b = tofu_a[0], tofu_b[0]
        combined_ebu = a["ebu"] + b["ebu"]
        combined_euro = a["euro"] + b["euro"]
        merged.append({
            "segment": "TOFU (A+B)", "ebu": combined_ebu,
            "AL": a["AL"] + b["AL"], "C1": a["C1"] + b["C1"], "C2": a["C2"] + b["C2"],
            "euro": round(combined_euro, 2),
            "euro_per_1k_ebu": round(combined_euro / combined_ebu * 1000, 2) if combined_ebu > 0 else 0,
        })
    else:
        merged.extend([r for r in results_list if r["month"] == month and r["region"] == region and "TOFU" in r["segment"]])
    merged.extend(others)
    return merged


# ══════════════════════════════════════════════════════════════════════════════
# 1. MISSION-LEVEL DETAIL
# ══════════════════════════════════════════════════════════════════════════════

print_section("1. TRADEIT NSM — MISSION-LEVEL DETAIL (€ Value)")
print("""
  Metric: € Value generated per conversion point
  € per conversion: AL = €0.38 | Trade 1 (C1) = €0.04 | Trade $250 (C2) = €8.75
  Not tracked: Trade $1,000 (€35.00), Trade 5 (€0.18) — future opportunity
  EBU = Users who joined the mission
  € per 1K EBU = normalised rate for cross-region comparison
""")

for month in ["Jan", "Feb"]:
    print(f"\n── {month.upper()} 2026 {'─'*65}")
    headers = ["Region", "Segment", "EBU", "AL", "C1", "C2", "€ Value", "€/1K EBU"]
    rows = []
    for r in [x for x in results if x["month"] == month]:
        rows.append([
            r["region"], r["segment"],
            f"{r['ebu']:,}", f"{r['AL']:,}", f"{r['C1']:,}", f"{r['C2']:,}",
            f"€{r['euro']:,.2f}", f"€{r['euro_per_1k_ebu']:,.2f}"
        ])
    print_table(headers, rows, [18, 12, 12, 8, 8, 8, 12, 12])


# ══════════════════════════════════════════════════════════════════════════════
# 2. REGION-LEVEL SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print_section("2. REGION-LEVEL SUMMARY (All Segments Merged)")

region_agg = {}
for r in results:
    key = (r["month"], r["region"])
    if key not in region_agg:
        region_agg[key] = {"ebu": 0, "AL": 0, "C1": 0, "C2": 0, "euro": 0.0}
    region_agg[key]["ebu"] += r["ebu"]
    region_agg[key]["AL"] += r["AL"]
    region_agg[key]["C1"] += r["C1"]
    region_agg[key]["C2"] += r["C2"]
    region_agg[key]["euro"] += r["euro"]

REGIONS = ["North America", "CIS", "MENA", "APAC"]

for month in ["Jan", "Feb"]:
    print(f"\n── {month.upper()} 2026 {'─'*65}")
    headers = ["Region", "EBU", "AL", "C1", "C2", "€ Value", "€/1K EBU"]
    rows = []
    for region in REGIONS:
        d = region_agg[(month, region)]
        e1k = d["euro"] / d["ebu"] * 1000 if d["ebu"] > 0 else 0
        rows.append([region, f"{d['ebu']:,}", f"{d['AL']:,}", f"{d['C1']:,}", f"{d['C2']:,}",
                      f"€{d['euro']:,.2f}", f"€{e1k:,.2f}"])
    total = {k: sum(region_agg[(month, r)][k] for r in REGIONS) for k in ["ebu", "AL", "C1", "C2", "euro"]}
    e1k_total = total["euro"] / total["ebu"] * 1000 if total["ebu"] > 0 else 0
    rows.append(["TOTAL", f"{total['ebu']:,}", f"{total['AL']:,}", f"{total['C1']:,}", f"{total['C2']:,}",
                  f"€{total['euro']:,.2f}", f"€{e1k_total:,.2f}"])
    print_table(headers, rows, [18, 12, 10, 10, 8, 14, 14])


# ══════════════════════════════════════════════════════════════════════════════
# 3. MONTH-OVER-MONTH COMPARISON
# ══════════════════════════════════════════════════════════════════════════════

print_section("3. MONTH-OVER-MONTH COMPARISON (Jan → Feb)")

headers = ["Region", "Jan €/1K", "Feb €/1K", "Δ €/1K", "Δ %", "Jan € Total", "Feb € Total", "€ Δ %"]
rows = []

for region in REGIONS:
    jan, feb = region_agg[("Jan", region)], region_agg[("Feb", region)]
    j1k = jan["euro"] / jan["ebu"] * 1000 if jan["ebu"] > 0 else 0
    f1k = feb["euro"] / feb["ebu"] * 1000 if feb["ebu"] > 0 else 0
    d1k = f1k - j1k
    d1k_pct = (d1k / j1k * 100) if j1k > 0 else 0
    e_delta = ((feb["euro"] - jan["euro"]) / jan["euro"] * 100) if jan["euro"] > 0 else 0
    rows.append([region, f"€{j1k:,.2f}", f"€{f1k:,.2f}", f"{d1k:+,.2f}", f"{d1k_pct:+.1f}%",
                  f"€{jan['euro']:,.2f}", f"€{feb['euro']:,.2f}", f"{e_delta:+.1f}%"])

jan_t = {k: sum(region_agg[("Jan", r)][k] for r in REGIONS) for k in ["ebu", "euro"]}
feb_t = {k: sum(region_agg[("Feb", r)][k] for r in REGIONS) for k in ["ebu", "euro"]}
j1k_t = jan_t["euro"] / jan_t["ebu"] * 1000
f1k_t = feb_t["euro"] / feb_t["ebu"] * 1000
d1k_t = f1k_t - j1k_t
rows.append(["TOTAL", f"€{j1k_t:,.2f}", f"€{f1k_t:,.2f}", f"{d1k_t:+,.2f}",
              f"{d1k_t/j1k_t*100:+.1f}%", f"€{jan_t['euro']:,.2f}", f"€{feb_t['euro']:,.2f}",
              f"{(feb_t['euro']-jan_t['euro'])/jan_t['euro']*100:+.1f}%"])
print_table(headers, rows, [18, 12, 12, 12, 10, 14, 14, 10])


# ══════════════════════════════════════════════════════════════════════════════
# 4. NA A/B TEST (Jan only)
# ══════════════════════════════════════════════════════════════════════════════

print_section("4. NA A/B TEST — GROUP A (1000 FP) vs GROUP B (2000 FP) — JAN 2026")

ga = [r for r in results if r["segment"] == "TOFU-A"][0]
gb = [r for r in results if r["segment"] == "TOFU-B"][0]

print(f"""
                          {'Group A (1000 FP)':>20}  {'Group B (2000 FP)':>20}  {'Δ':>10}  {'Δ %':>10}
{'─'*90}""")

for label, key in [("EBU (Joined)", "ebu"), ("Task 1 Completed", "task1_completed"),
                    ("AL (implicit)", "AL"), ("C1 (Trade any)", "C1"), ("C2 (Trade $250+)", "C2"),
                    ("€ Value", "euro"), ("€ per 1K EBU", "euro_per_1k_ebu")]:
    a, b = ga[key], gb[key]
    delta = b - a
    pct = (delta / a * 100) if a else 0
    if isinstance(a, float):
        print(f"  {label:<28} {a:>20,.2f}  {b:>20,.2f}  {delta:>+10,.2f}  {pct:>+9.1f}%")
    else:
        print(f"  {label:<28} {a:>20,}  {b:>20,}  {delta:>+10,}  {pct:>+9.1f}%")

# Conversion rates: AL claim rate, C1-to-joined, C2-to-joined
print(f"\n  Conversion Rates:")
for label, num_key, denom_key in [
    ("AL Rate (prizes / T1 completed)", "AL", "task1_completed"),
    ("C1 Rate (trade / joined)", "C1", "ebu"),
    ("C2 Rate ($250+ / joined)", "C2", "ebu"),
]:
    a_r = ga[num_key] / ga[denom_key] * 100 if ga[denom_key] else 0
    b_r = gb[num_key] / gb[denom_key] * 100 if gb[denom_key] else 0
    print(f"  {label:35} {a_r:>18.3f}%  {b_r:>18.3f}%  {b_r-a_r:>+10.3f}pp")


# ══════════════════════════════════════════════════════════════════════════════
# 5. SEGMENT PERFORMANCE BY REGION
# ══════════════════════════════════════════════════════════════════════════════

print_section("5. SEGMENT PERFORMANCE BY REGION")

for month in ["Jan", "Feb"]:
    print(f"\n── {month.upper()} 2026 {'─'*65}")
    for region in REGIONS:
        seg_data = merge_tofu_ab(results, month, region)
        if not seg_data:
            continue
        print(f"\n  {region}:")
        headers = ["Segment", "EBU", "AL", "C1", "C2", "€ Value", "€/1K EBU"]
        rows = []
        for s in seg_data:
            rows.append([s["segment"], f"{s['ebu']:,}", f"{s['AL']:,}", f"{s['C1']:,}", f"{s['C2']:,}",
                          f"€{s['euro']:,.2f}", f"€{s['euro_per_1k_ebu']:,.2f}"])
        print_table(headers, rows, [14, 12, 8, 8, 8, 12, 12])


# ══════════════════════════════════════════════════════════════════════════════
# 6. € VALUE BREAKDOWN BY CONVERSION TYPE
# ══════════════════════════════════════════════════════════════════════════════

print_section("6. € VALUE BREAKDOWN — WHERE DOES THE VALUE COME FROM?")

for month in ["Jan", "Feb"]:
    month_r = [r for r in results if r["month"] == month]
    total_al = sum(r["AL"] for r in month_r)
    total_c1 = sum(r["C1"] for r in month_r)
    total_c2 = sum(r["C2"] for r in month_r)
    euro_al = total_al * 0.38
    euro_c1 = total_c1 * 0.04
    euro_c2 = total_c2 * 8.75
    euro_total = euro_al + euro_c1 + euro_c2
    pct_al = euro_al / euro_total * 100 if euro_total else 0
    pct_c1 = euro_c1 / euro_total * 100 if euro_total else 0
    pct_c2 = euro_c2 / euro_total * 100 if euro_total else 0

    print(f"\n── {month.upper()} 2026 {'─'*65}")
    print(f"  {'Conversion':<25} {'Count':>10} {'€/unit':>10} {'€ Total':>14} {'% of Total':>12}")
    print(f"  {'-'*71}")
    print(f"  {'AL (Account Linkage)':<25} {total_al:>10,} {'€0.38':>10} {'€'+f'{euro_al:,.2f}':>14} {pct_al:>11.1f}%")
    print(f"  {'C1 (Trade any item)':<25} {total_c1:>10,} {'€0.04':>10} {'€'+f'{euro_c1:,.2f}':>14} {pct_c1:>11.1f}%")
    print(f"  {'C2 (Trade $250+)':<25} {total_c2:>10,} {'€8.75':>10} {'€'+f'{euro_c2:,.2f}':>14} {pct_c2:>11.1f}%")
    print(f"  {'C3 (Trade $1,000+)':<25} {'N/A':>10} {'€35.00':>10} {'—':>14} {'—':>12}")
    print(f"  {'-'*71}")
    print(f"  {'TOTAL':<25} {'':>10} {'':>10} {'€'+f'{euro_total:,.2f}':>14} {'100.0%':>12}")


# ══════════════════════════════════════════════════════════════════════════════
# 7. FUNNEL CONVERSION RATES
# ══════════════════════════════════════════════════════════════════════════════

print_section("7. FUNNEL CONVERSION RATES (Joined → Each Conversion)")

for month in ["Jan", "Feb"]:
    print(f"\n── {month.upper()} 2026 {'─'*65}")
    for region in REGIONS:
        seg_data = merge_tofu_ab(results, month, region)
        if not seg_data:
            continue
        print(f"\n  {region}:")
        for s in seg_data:
            ebu = s["ebu"]
            al_r = s["AL"] / ebu * 100 if ebu else 0
            c1_r = s["C1"] / ebu * 100 if ebu else 0
            c2_r = s["C2"] / ebu * 100 if ebu else 0
            print(f"    {s['segment']:14} | AL: {al_r:>6.2f}% | C1: {c1_r:>6.2f}% | C2: {c2_r:>6.3f}%")


# ══════════════════════════════════════════════════════════════════════════════
# 8. KEY INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════

print_section("8. KEY INSIGHTS")

jan_r = [r for r in results if r["month"] == "Jan"]
feb_r = [r for r in results if r["month"] == "Feb"]
jan_e = sum(r["euro"] for r in jan_r)
feb_e = sum(r["euro"] for r in feb_r)
jan_ebu = sum(r["ebu"] for r in jan_r)
feb_ebu = sum(r["ebu"] for r in feb_r)
jan_al = sum(r["AL"] for r in jan_r)
feb_al = sum(r["AL"] for r in feb_r)
jan_c2 = sum(r["C2"] for r in jan_r)
feb_c2 = sum(r["C2"] for r in feb_r)

jan_c2_euro = jan_c2 * 8.75
feb_c2_euro = feb_c2 * 8.75
jan_c2_pct = jan_c2_euro / jan_e * 100 if jan_e else 0
feb_c2_pct = feb_c2_euro / feb_e * 100 if feb_e else 0

jan_cis_ebu = sum(r["ebu"] for r in jan_r if r["region"] == "CIS")
feb_cis_ebu = sum(r["ebu"] for r in feb_r if r["region"] == "CIS")

print(f"""
  HEADLINE NUMBERS
  ──────────────────────────────────────────────────────────────
  Jan 2026:  €{jan_e:,.2f} total value | €{jan_e/jan_ebu*1000:,.2f} per 1K EBU | {jan_ebu:,} EBU
  Feb 2026:  €{feb_e:,.2f} total value | €{feb_e/feb_ebu*1000:,.2f} per 1K EBU | {feb_ebu:,} EBU
  MoM:       €{feb_e-jan_e:+,.2f} ({(feb_e-jan_e)/jan_e*100:+.1f}%) | {feb_ebu-jan_ebu:+,} EBU ({(feb_ebu-jan_ebu)/jan_ebu*100:+.1f}%)

  C2 (TRADE $250+) DOMINATES VALUE
  ──────────────────────────────────────────────────────────────
  Jan: C2 = €{jan_c2_euro:,.2f} ({jan_c2_pct:.1f}% of total €)
  Feb: C2 = €{feb_c2_euro:,.2f} ({feb_c2_pct:.1f}% of total €)
  → C2 is overwhelmingly the value driver. AL and C1 are volume metrics,
    but €8.75 per $250+ trade vs €0.38 per AL means C2 dominates.

  REGIONAL SCALE
  ──────────────────────────────────────────────────────────────
  CIS = {jan_cis_ebu/jan_ebu*100:.0f}% of Jan EBU, {feb_cis_ebu/feb_ebu*100:.0f}% of Feb EBU
  CIS TOFU alone: {385376:,} (Jan) / {390909:,} (Feb) — ~67% of all Tradeit EBU
  But CIS AL claim rate (TOFU) is only ~1.6-2.3% vs NA ~4-5%.
  CIS scale compensates: sheer volume drives absolute € even at lower conversion.

  NA A/B TEST (Jan only)
  ──────────────────────────────────────────────────────────────
  Group B (2000 FP) beat Group A (1000 FP):
    AL: {ga['AL']:,} → {gb['AL']:,} ({(gb['AL']-ga['AL'])/ga['AL']*100:+.1f}%)
    C1: {ga['C1']:,} → {gb['C1']:,} ({(gb['C1']-ga['C1'])/ga['C1']*100:+.1f}%)
    €:  €{ga['euro']:,.2f} → €{gb['euro']:,.2f} ({(gb['euro']-ga['euro'])/ga['euro']*100:+.1f}%)
  Higher FP reward → more prize claims → more implicit ALs → more trades.
  But C2 was slightly lower (17 vs 19) — high-value traders aren't FP-sensitive.
  Feb consolidated to single TOFU mission (no A/B), suggesting 2000 FP was adopted.

  BOFU = PURE C2 ENGINE
  ──────────────────────────────────────────────────────────────
  BOFU users already linked + already traded. The only conversion is C2 ($250+).
  BOFU €/1K EBU is highest of any segment — but small audience.
  Real volume opportunity: improve TOFU → C2 funnel (currently <0.1% of joined).

  UNTRACKED VALUE (OPPORTUNITY)
  ──────────────────────────────────────────────────────────────
  Trade $1,000+ (€35.00) and Trade 5 (€0.18) are NOT in current missions.
  If added as challenge steps, they could significantly increase € per user:
    Example: if 10% of C2 users also hit $1,000+ → ~{int(feb_c2 * 0.1)} users × €35 = €{feb_c2 * 0.1 * 35:,.0f}
""")

print("=" * 90)
print("  Analysis complete. Primary metric: € Value (not OVU).")
print("  NSM headline: 30-day rolling Total Partner Value / EBU × 1,000")
print("  Script: analysis/tradeit_nsm_analysis.py")
print("=" * 90)
