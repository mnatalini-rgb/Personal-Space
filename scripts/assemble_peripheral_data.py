#!/usr/bin/env python3
import json
import sys
import re
from collections import defaultdict

Q1_FILE = sys.argv[1]
Q2_FILE = sys.argv[2]
Q3_FILE = sys.argv[3]
Q4_FILE = sys.argv[4]

EARLY_RELEASE = {'IT', 'TR', 'IN'}
KEY_COUNTRIES = ['TR', 'UA', 'BR', 'KZ', 'AR', 'IT', 'IN']

def load_json(path):
    with open(path) as f:
        text = f.read()
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON array found in {path}")
    return json.loads(match.group())

q1 = load_json(Q1_FILE)
q2 = load_json(Q2_FILE)
q3 = load_json(Q3_FILE)
q4 = load_json(Q4_FILE)

q1_by_country = {r['country']: r for r in q1}

q2_by_country = defaultdict(list)
for r in q2:
    q2_by_country[r['country']].append({'name': r['brand'], 'count': int(r['cnt'])})

q3_by_country = defaultdict(list)
for r in q3:
    q3_by_country[r['country']].append({'name': r['mobo'], 'count': int(r['cnt'])})

q4_by_country = defaultdict(list)
for r in q4:
    q4_by_country[r['country']].append({'cores': r['core_label'], 'count': int(r['cnt'])})

def build_data_object(countries, tier_label, country_code=''):
    total_rows = 0
    unique_users = set()
    cpu_amd = 0
    cpu_intel = 0
    gaming = 0
    kb = 0
    mouse = 0
    other = 0

    periph_agg = defaultdict(int)
    mobo_agg = defaultdict(int)
    core_agg = defaultdict(int)

    user_counts = []
    for cc in countries:
        if cc not in q1_by_country:
            continue
        r = q1_by_country[cc]
        tr = int(r['total_rows'])
        total_rows += tr
        unique_users.add(cc)
        user_counts.append((cc, int(r['unique_users'])))
        cpu_amd += int(r['cpu_amd'])
        cpu_intel += int(r['cpu_intel'])
        gaming += int(r['gaming_count'])
        kb += int(r['keyboard_count'])
        mouse += int(r['mouse_count'])
        other += int(r['other_count'])

        for item in q2_by_country.get(cc, []):
            periph_agg[item['name']] += item['count']
        for item in q3_by_country.get(cc, []):
            mobo_agg[item['name']] += item['count']
        for item in q4_by_country.get(cc, []):
            core_agg[item['cores']] += item['count']

    total_unique = sum(u for _, u in user_counts)
    amd_intel_total = cpu_amd + cpu_intel or 1
    device_total = kb + mouse + other or 1

    top_periph = sorted(periph_agg.items(), key=lambda x: -x[1])[:10]
    top_mobo = sorted(mobo_agg.items(), key=lambda x: -x[1])[:8]
    top_cores = sorted(core_agg.items(), key=lambda x: -x[1])[:6]

    obj = {
        'totalRows': total_rows,
        'uniqueSystems': total_unique,
        'dau': 0,
        'cpuAmd': round(100 * cpu_amd / amd_intel_total, 1),
        'cpuIntel': round(100 * cpu_intel / amd_intel_total, 1),
        'gamingPenetration': round(100 * gaming / (total_rows or 1), 1),
        'keyboardPct': round(100 * kb / device_total, 1),
        'mousePct': round(100 * mouse / device_total, 1),
        'topPeripherals': [{'name': n, 'count': c} for n, c in top_periph],
        'topMobo': [{'name': n, 'count': c} for n, c in top_mobo],
        'coreCounts': [{'cores': c, 'count': cnt} for c, cnt in top_cores],
        'dateRange': ['2026-03-12', '2026-04-22'],
        'tier': tier_label,
    }
    if country_code:
        obj['countryCode'] = country_code
    return obj

all_countries = list(q1_by_country.keys())
tier3_countries = [cc for cc in all_countries if cc not in EARLY_RELEASE]

result = {
    'allData': build_data_object(all_countries, 'All Released'),
    'trData': build_data_object(['TR'], 'Early Release', 'TR'),
    'uaData': build_data_object(['UA'], 'Tier 3', 'UA'),
    'brData': build_data_object(['BR'], 'Tier 3', 'BR'),
    'kzData': build_data_object(['KZ'], 'Tier 3', 'KZ'),
    'arData': build_data_object(['AR'], 'Tier 3', 'AR'),
    'itData': build_data_object(['IT'], 'Early Release', 'IT'),
    'inData': build_data_object(['IN'], 'Early Release', 'IN'),
    'earlyReleaseData': build_data_object(list(EARLY_RELEASE), 'Early Release'),
    'tier3Data': build_data_object(tier3_countries, 'Tier 3'),
}

print(json.dumps(result, indent=2))
