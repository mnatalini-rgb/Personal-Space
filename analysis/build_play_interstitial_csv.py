#!/usr/bin/env python3
"""
Build the Play Interstitial Business Case CSV with formula references.
Every computed cell shows =FORMULA(...) instead of a hardcoded value.

Data sources:
- NEW: faceit fact__daily_active_players 2026-03-18T1519.csv (monthly sessions by country)
- OLD: Play Inter Biz Case - Calculations.csv (unique users per country)
- Tier country - Sheet1.csv (tier classification)

Key changes from v2:
- Ad pod = up to 60s — modeled as 3 impressions per pod (3×20s avg creative)
- Revenue based on IMPRESSIONS (pods × 3), not pods
- Russia INCLUDED in inventory value at $2 CPM, 10% fill
- Monthly sessions from new data (Feb 2026, free users only)
- All computed cells use =FORMULA notation
- Subs model unchanged (based on unfilled pods, not impressions)
"""

import csv
import re
from collections import OrderedDict

# --- CONFIG ---
PODS_PER_USER_PER_MONTH = 28  # 1 pod per daily session x 28 days
IMPRESSIONS_PER_POD = 3       # 3×20s avg creatives within a 60s pod
FILL_RATE_T1_T2 = 0.20
FILL_RATE_T3 = 0.10
FILL_RATE_RU = 0.10
CPM_T1_LOW, CPM_T1_MID, CPM_T1_HIGH = 10, 15, 20
CPM_T2_LOW, CPM_T2_MID, CPM_T2_HIGH = 10, 15, 20
CPM_T3 = 5
CPM_RU = 2
HOUSE_ADS_FILL = 0.80
SUBS_CONV = 0.0005
SUBS_CANNIBALISATION = 0.50
SUB_PRICE = 7.30

# --- ISO → Country name mapping (for tier lookup) ---
ISO_TO_COUNTRY = {
    'AU': 'Australia', 'CA': 'Canada', 'FR': 'France', 'DE': 'Germany',
    'IT': 'Italy', 'ES': 'Spain', 'GB': 'United Kingdom', 'US': 'United States',
    'AT': 'Austria', 'BE': 'Belgium', 'HR': 'Croatia', 'CY': 'Cyprus',
    'CZ': 'Czechia', 'DK': 'Denmark', 'EE': 'Estonia', 'FO': 'Faroe Islands',
    'FI': 'Finland', 'GR': 'Greece', 'HU': 'Hungary', 'IS': 'Iceland',
    'IE': 'Ireland', 'JP': 'Japan', 'JO': 'Jordan', 'LV': 'Latvia',
    'LI': 'Liechtenstein', 'LT': 'Lithuania', 'NL': 'Netherlands',
    'NZ': 'New Zealand', 'NO': 'Norway', 'PL': 'Poland', 'PT': 'Portugal',
    'RO': 'Romania', 'SA': 'Saudi Arabia', 'RS': 'Serbia', 'SG': 'Singapore',
    'SK': 'Slovakia', 'SI': 'Slovenia', 'KR': 'South Korea', 'SE': 'Sweden',
    'CH': 'Switzerland', 'AE': 'United Arab Emirates',
    'RU': 'Russia',
    # Tier 3 (subset of large ones)
    'AL': 'Albania', 'DZ': 'Algeria', 'AR': 'Argentina', 'AM': 'Armenia',
    'AZ': 'Azerbaijan', 'BH': 'Bahrain', 'BD': 'Bangladesh', 'BY': 'Belarus',
    'BO': 'Bolivia', 'BA': 'Bosnia and Herzegovina', 'BR': 'Brazil',
    'BN': 'Brunei', 'BG': 'Bulgaria', 'KH': 'Cambodia', 'CL': 'Chile',
    'CN': 'China', 'CO': 'Colombia', 'CR': 'Costa Rica', 'DO': 'Dominican Republic',
    'EC': 'Ecuador', 'EG': 'Egypt', 'SV': 'El Salvador', 'GE': 'Georgia',
    'GH': 'Ghana', 'GL': 'Greenland', 'GU': 'Guam', 'GT': 'Guatemala',
    'GG': 'Guernsey', 'HN': 'Honduras', 'HK': 'Hong Kong', 'IN': 'India',
    'ID': 'Indonesia', 'IQ': 'Iraq', 'IM': 'Isle of Man', 'IL': 'Israel',
    'JM': 'Jamaica', 'JE': 'Jersey', 'KZ': 'Kazakhstan', 'XK': 'Kosovo',
    'KW': 'Kuwait', 'KG': 'Kyrgyzstan', 'LA': 'Laos', 'LB': 'Lebanon',
    'LY': 'Libya', 'LU': 'Luxembourg', 'MO': 'Macao', 'MY': 'Malaysia',
    'MT': 'Malta', 'MQ': 'Martinique', 'MU': 'Mauritius', 'MX': 'Mexico',
    'MD': 'Moldova', 'MC': 'Monaco', 'MN': 'Mongolia', 'ME': 'Montenegro',
    'MA': 'Morocco', 'MM': 'Myanmar (Burma)', 'NP': 'Nepal', 'NC': 'New Caledonia',
    'NI': 'Nicaragua', 'NG': 'Nigeria', 'MK': 'North Macedonia', 'OM': 'Oman',
    'PK': 'Pakistan', 'PS': 'Palestine', 'PA': 'Panama', 'PY': 'Paraguay',
    'PE': 'Peru', 'PH': 'Philippines', 'PR': 'Puerto Rico', 'QA': 'Qatar',
    'ZA': 'South Africa', 'LK': 'Sri Lanka', 'SY': 'Syria', 'TW': 'Taiwan',
    'TJ': 'Tajikistan', 'TZ': 'Tanzania', 'TH': 'Thailand', 'TN': 'Tunisia',
    'TR': 'Turkiye', 'TM': 'Turkmenistan', 'UA': 'Ukraine', 'UY': 'Uruguay',
    'UZ': 'Uzbekistan', 'VE': 'Venezuela', 'VN': 'Vietnam', 'ZM': 'Zambia',
    'KY': 'Cayman Islands', 'PF': 'French Polynesia',
}

TIER_FILE = '/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/Tier country  - Sheet1.csv'
NEW_DATA = '/Users/moritznatalini/Desktop/Master_Product_Folder/data/brand_integrations/faceit fact__daily_active_players 2026-03-18T1519.csv'
OLD_DATA = '/Users/moritznatalini/Desktop/Master_Product_Folder/data/brand_integrations/Play Inter Biz Case - Calculations.csv'
OUTPUT = '/Users/moritznatalini/Desktop/Master_Product_Folder/data/brand_integrations/Play Inter Biz Case - Calculations.csv'

# Load tier classification
tiers = {}
with open(TIER_FILE, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        if len(row) >= 2:
            tier = row[0].strip()
            country = row[1].strip()
            tiers[country] = tier

def get_tier(iso):
    """Get tier for an ISO code. Russia = 'Russia'. Unknown = 'Tier 3'."""
    iso_upper = iso.upper().strip()
    if iso_upper == 'RU':
        return 'Russia'
    country = ISO_TO_COUNTRY.get(iso_upper, '')
    if country in tiers:
        return tiers[country]
    return 'Tier 3'

# Load new session data (monthly sessions per country)
new_sessions = {}
total_from_file = 0
with open(NEW_DATA, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header line 1
    next(reader)  # skip header line 2
    for row in reader:
        if len(row) >= 2:
            iso = row[0].strip()
            sessions_str = row[1].replace(',', '').strip()
            if iso and sessions_str:
                try:
                    sessions = int(sessions_str)
                    if iso:  # has a country code
                        new_sessions[iso.upper()] = sessions
                        total_from_file += sessions
                    elif not iso and sessions > 1000000:
                        # This is the grand total row
                        pass
                except ValueError:
                    pass

print(f"Loaded {len(new_sessions)} countries from new data, total sessions: {total_from_file:,}")

# Load old user data (unique users per country)
OLD_UNIQUE_USERS = {
    'DE': 60037, 'US': 42818, 'FR': 27113, 'GB': 22315, 'ES': 11598,
    'CA': 9510, 'AU': 5646, 'IT': 4784,
    'PL': 156508, 'FI': 29566, 'PT': 28514, 'DK': 26190, 'NL': 25111,
    'KZ': 108953, 'UA': 65704, 'TR': 65024, 'RO': 46186, 'BY': 33247,
    'XK': 31054, 'UZ': 30143, 'BR': 25976, 'SE': 24758, 'MN': 21955,
    'AR': 18613, 'CZ': 15186, 'RS': 13145, 'LT': 13037, 'LV': 10965,
    'MK': 10662, 'NO': 9411, 'HU': 9060, 'SK': 8549, 'BG': 8112,
    'KG': 7799, 'GE': 6836, 'EE': 6362, 'AT': 6287, 'HK': 5601,
    'BE': 5587, 'VN': 5532, 'MD': 5307, 'CH': 5134, 'AL': 5056,
    'SG': 4554, 'BA': 4188, 'PK': 4091, 'IL': 4080, 'IR': 3809,
    'HR': 3692, 'CN': 3481, 'AE': 3364, 'TJ': 3360, 'IN': 3321,
    'PH': 3163, 'MY': 3147, 'GR': 2971, 'AZ': 2955, 'CL': 2718,
    'TW': 2689, 'TH': 2650, 'ID': 2618, 'KR': 2383, 'DZ': 2379,
    'IE': 2322, 'LB': 2197, 'SI': 1803, 'JO': 1778, 'PE': 1658,
    'JP': 1652, 'ME': 1566, 'AM': 1435, 'PS': 1160, 'UY': 1151,
    'IS': 1008, 'SA': 928, 'MX': 894, 'IQ': 888, 'CY': 703,
    'NZ': 681, 'VE': 647, 'TN': 638, 'MA': 577, 'CO': 537,
    'EG': 441, 'LU': 422, 'BD': 397, 'SY': 386, 'KW': 348,
    'KH': 336, 'PY': 318, 'ZA': 310, 'OM': 275, 'MT': 210,
    'QA': 191, 'MM': 182, 'BN': 163, 'EC': 155, 'LI': 139,
    'BO': 119, 'MO': 107, 'DO': 94, 'BH': 94, 'CR': 91,
    'GT': 90, 'PA': 90, 'LK': 88, 'NP': 74, 'LY': 66,
    'RU': 488448,
}
old_users = OLD_UNIQUE_USERS

print(f"Loaded {len(old_users)} countries from old user data")

# --- Build the data rows ---
# Columns:
# A: Tier
# B: Country (ISO)
# C: Monthly Sessions (new data)
# D: Unique Users (old data, if available)
# E: Ad Pods/Month = C (1 ad pod per session)
# F: Impressions/Month = E * 3 (3 ads per pod, avg 20s each within 60s)
# G: Fill Rate
# H: Filled Impressions = F * G
# I: CPM
# J: Monthly Ad Rev = H / 1000 * I
# K: Annual Ad Rev = J * 12
# L: House Ads unfilled pods = E * (1 - G)
# M: Subs Conversion (0.05%) = L * 0.0005
# N: Cannibalisation (50%) = M * 0.5
# O: Monthly Subs Rev = N * 7.30
# P: Annual Subs Rev = O * 12
# Q: Monthly Total = J + O
# R: Annual Total = K + P

rows = []

# Sort by tier priority then by sessions descending
tier_order = {'Tier 1': 0, 'Tier 2': 1, 'Tier 3': 2, 'Russia': 3}

for iso, sessions in new_sessions.items():
    tier = get_tier(iso)
    users = old_users.get(iso, '')
    
    if tier == 'Tier 1':
        fill = FILL_RATE_T1_T2
        cpm = CPM_T1_MID  # Use $15 for conservative
    elif tier == 'Tier 2':
        fill = FILL_RATE_T1_T2
        cpm = CPM_T2_LOW  # Use $10 for conservative
    elif tier == 'Russia':
        fill = FILL_RATE_RU
        cpm = CPM_RU
    else:  # Tier 3
        fill = FILL_RATE_T3
        cpm = CPM_T3
    
    rows.append({
        'tier': tier,
        'iso': iso,
        'sessions': sessions,
        'users': users,
        'fill': fill,
        'cpm': cpm,
    })

# Sort
rows.sort(key=lambda r: (tier_order.get(r['tier'], 99), -r['sessions']))

# --- Write CSV with formulas ---
# We'll use Excel-style formula notation
# Row numbering: header = row 1, first data = row 2

HEADER = [
    'Tier',           # A
    'Country',        # B
    'Monthly Sessions', # C
    'Unique Users',   # D
    'Ad Pods/Month',  # E = C (1 pod per session)
    'Impressions/Month', # F = E * 3 (3 ads per pod)
    'Fill Rate',      # G
    'Filled Impressions', # H = F * G
    'CPM ($)',        # I
    'Monthly Ad Rev ($)', # J = H / 1000 * I
    'Annual Ad Rev ($)',  # K = J * 12
    'House Ads (unfilled pods)', # L = E * (1 - G)
    'Subs Conversion (0.05%)', # M = L * 0.0005
    'Cannibalisation (50%)', # N = M * 0.5
    'Monthly Subs Rev ($)', # O = N * 7.30
    'Annual Subs Rev ($)',  # P = O * 12
    'Monthly Total ($)',    # Q = J + O
    'Annual Total ($)',     # R = K + P
]

output_lines = []
output_lines.append(HEADER)

for i, r in enumerate(rows):
    row_num = i + 2  # Excel row (1-indexed, header is row 1)
    
    # Columns use Excel notation: A2, B2, C2...
    rn = str(row_num)
    
    line = [
        r['tier'],                              # A: Tier
        r['iso'],                               # B: Country
        r['sessions'],                          # C: Monthly Sessions
        r['users'] if r['users'] else '',       # D: Unique Users (old data)
        f'=C{rn}',                              # E: Ad Pods/Month = sessions
        f'=E{rn}*3',                            # F: Impressions/Month = pods * 3
        r['fill'],                              # G: Fill Rate
        f'=F{rn}*G{rn}',                        # H: Filled Impressions
        r['cpm'],                               # I: CPM
        f'=H{rn}/1000*I{rn}',                   # J: Monthly Ad Rev
        f'=J{rn}*12',                            # K: Annual Ad Rev
        f'=E{rn}*(1-G{rn})',                     # L: House Ads (unfilled pods)
        f'=L{rn}*0.0005',                        # M: Subs Conversion
        f'=M{rn}*0.5',                           # N: Cannibalisation
        f'=N{rn}*7.30',                          # O: Monthly Subs Rev
        f'=O{rn}*12',                            # P: Annual Subs Rev
        f'=J{rn}+O{rn}',                         # Q: Monthly Total
        f'=K{rn}+P{rn}',                         # R: Annual Total
    ]
    output_lines.append(line)

data_end = len(rows) + 1  # last data row number

# --- Add blank separator ---
output_lines.append([])

# --- SUBTOTALS BY TIER ---
output_lines.append(['SUBTOTALS BY TIER'] + [''] * (len(HEADER) - 1))

# For each tier, add a SUMIF row
subtotal_tiers = [
    ('Tier 1', '8 countries'),
    ('Tier 2', 'countries'),
    ('Tier 3', 'countries'),
    ('Russia', 'RU'),
]

# Count countries per tier
tier_counts = {}
for r in rows:
    tier_counts[r['tier']] = tier_counts.get(r['tier'], 0) + 1

subtotal_start = data_end + 3  # accounting for blank + header rows

for idx, (tier_name, _) in enumerate(subtotal_tiers):
    count = tier_counts.get(tier_name, 0)
    label = f'{count} countries' if tier_name != 'Russia' else 'RU'
    rn = str(subtotal_start + idx)
    
    # Use SUMIF formulas referencing the data range
    line = [
        tier_name,
        label,
        f'=SUMIF(A2:A{data_end},"{tier_name}",C2:C{data_end})',  # C: Sessions
        f'=SUMIF(A2:A{data_end},"{tier_name}",D2:D{data_end})',  # D: Users
        f'=SUMIF(A2:A{data_end},"{tier_name}",E2:E{data_end})',  # E: Pods
        f'=SUMIF(A2:A{data_end},"{tier_name}",F2:F{data_end})',  # F: Impressions
        '',  # G: Fill rate varies
        f'=SUMIF(A2:A{data_end},"{tier_name}",H2:H{data_end})',  # H: Filled Impressions
        '',  # I: CPM varies
        f'=SUMIF(A2:A{data_end},"{tier_name}",J2:J{data_end})',  # J: Monthly Ad Rev
        f'=J{rn}*12',  # K: Annual Ad Rev
        f'=SUMIF(A2:A{data_end},"{tier_name}",L2:L{data_end})',  # L: House
        f'=SUMIF(A2:A{data_end},"{tier_name}",M2:M{data_end})',  # M: Subs conv
        f'=SUMIF(A2:A{data_end},"{tier_name}",N2:N{data_end})',  # N: Cannibalisation
        f'=SUMIF(A2:A{data_end},"{tier_name}",O2:O{data_end})',  # O: Monthly Subs Rev
        f'=O{rn}*12',  # P: Annual Subs Rev
        f'=J{rn}+O{rn}',  # Q: Monthly Total
        f'=K{rn}+P{rn}',  # R: Annual Total
    ]
    output_lines.append(line)

# GRAND TOTAL
gt_rn = str(subtotal_start + len(subtotal_tiers))
grand_total_line = [
    'GRAND TOTAL',
    'All',
    f'=SUM(C{subtotal_start}:C{subtotal_start + len(subtotal_tiers) - 1})',
    f'=SUM(D{subtotal_start}:D{subtotal_start + len(subtotal_tiers) - 1})',
    f'=SUM(E{subtotal_start}:E{subtotal_start + len(subtotal_tiers) - 1})',
    f'=SUM(F{subtotal_start}:F{subtotal_start + len(subtotal_tiers) - 1})',
    '',
    f'=SUM(H{subtotal_start}:H{subtotal_start + len(subtotal_tiers) - 1})',
    '',
    f'=SUM(J{subtotal_start}:J{subtotal_start + len(subtotal_tiers) - 1})',
    f'=J{gt_rn}*12',
    f'=SUM(L{subtotal_start}:L{subtotal_start + len(subtotal_tiers) - 1})',
    f'=SUM(M{subtotal_start}:M{subtotal_start + len(subtotal_tiers) - 1})',
    f'=SUM(N{subtotal_start}:N{subtotal_start + len(subtotal_tiers) - 1})',
    f'=SUM(O{subtotal_start}:O{subtotal_start + len(subtotal_tiers) - 1})',
    f'=O{gt_rn}*12',
    f'=J{gt_rn}+O{gt_rn}',
    f'=K{gt_rn}+P{gt_rn}',
]
output_lines.append(grand_total_line)

# GRAND TOTAL EXCL RUSSIA
gt_excl_rn = str(subtotal_start + len(subtotal_tiers) + 1)
# Sum only T1+T2+T3 subtotals (skip Russia)
ru_row = subtotal_start + 3  # Russia is the 4th subtotal
t1_row = subtotal_start
t2_row = subtotal_start + 1
t3_row = subtotal_start + 2
grand_total_excl_line = [
    'TOTAL EXCL RU',
    'All excl. Russia',
    f'=C{t1_row}+C{t2_row}+C{t3_row}',       # C: Sessions
    f'=D{t1_row}+D{t2_row}+D{t3_row}',       # D: Users
    f'=E{t1_row}+E{t2_row}+E{t3_row}',       # E: Pods
    f'=F{t1_row}+F{t2_row}+F{t3_row}',       # F: Impressions
    '',                                         # G: Fill rate (varies)
    f'=H{t1_row}+H{t2_row}+H{t3_row}',       # H: Filled Impressions
    '',                                         # I: CPM (varies)
    f'=J{t1_row}+J{t2_row}+J{t3_row}',       # J: Monthly Ad Rev
    f'=J{gt_excl_rn}*12',                        # K: Annual Ad Rev
    f'=L{t1_row}+L{t2_row}+L{t3_row}',       # L: House Ads
    f'=M{t1_row}+M{t2_row}+M{t3_row}',       # M: Subs Conversion
    f'=N{t1_row}+N{t2_row}+N{t3_row}',       # N: Cannibalisation
    f'=O{t1_row}+O{t2_row}+O{t3_row}',       # O: Monthly Subs Rev
    f'=O{gt_excl_rn}*12',                      # P: Annual Subs Rev
    f'=J{gt_excl_rn}+O{gt_excl_rn}',          # Q: Monthly Total
    f'=K{gt_excl_rn}+P{gt_excl_rn}',          # R: Annual Total
]
output_lines.append(grand_total_excl_line)

# --- SCENARIO COMPARISON (ANNUAL) ---
output_lines.append([])
output_lines.append(['SCENARIO COMPARISON (ANNUAL)'] + [''] * (len(HEADER) - 1))
output_lines.append([])

scenario_header = [
    'Scenario', 'Fill Rate', 'CPM Assumption',
    'Tier 1 Annual', 'Tier 2 Annual', 'Tier 3 Annual', 'Russia Annual',
    'Total Ad Rev (Annual)', 'Subs Rev (Annual)', 'Combined (Annual)',
]
output_lines.append(scenario_header + [''] * (len(HEADER) - len(scenario_header)))

# We need to compute scenario values from the tier subtotals
# T1 impressions = F{t1_row}, T2 = F{t2_row}, T3 = F{t3_row}, RU = F{ru_row}
# Revenue = impressions / 1000 * CPM * 12
# Conservative: T1 20% fill $15 CPM, T2 20% fill $10 CPM, T3 10% fill $5 CPM, RU 10% fill $2 CPM
# Mid: T1 20% $20, T2 20% $15, T3 10% $5, RU 10% $2
# Ceiling: 100% fill, T1 $15, T2 $10, T3 $5, RU $2

sc_row_base = len(output_lines) + 1  # next row number

# Conservative
sc1_rn = str(sc_row_base)
cons_line = [
    'Conservative (Year 1)',
    '20% T1/T2 - 10% T3/RU',
    'T1 $15 / T2 $10 / T3 $5 / RU $2',
    f'=F{t1_row}*0.20/1000*15*12',
    f'=F{t2_row}*0.20/1000*10*12',
    f'=F{t3_row}*0.10/1000*5*12',
    f'=F{ru_row}*0.10/1000*2*12',
    f'=D{sc1_rn}+E{sc1_rn}+F{sc1_rn}+G{sc1_rn}',
    f'=P{gt_rn}',
    f'=H{sc1_rn}+I{sc1_rn}',
]
output_lines.append(cons_line + [''] * (len(HEADER) - len(cons_line)))

sc2_rn = str(sc_row_base + 1)
mid_line = [
    'Mid Case',
    '20% T1/T2 - 10% T3/RU',
    'T1 $20 / T2 $15 / T3 $5 / RU $2',
    f'=F{t1_row}*0.20/1000*20*12',
    f'=F{t2_row}*0.20/1000*15*12',
    f'=F{t3_row}*0.10/1000*5*12',
    f'=F{ru_row}*0.10/1000*2*12',
    f'=D{sc2_rn}+E{sc2_rn}+F{sc2_rn}+G{sc2_rn}',
    f'=P{gt_rn}',
    f'=H{sc2_rn}+I{sc2_rn}',
]
output_lines.append(mid_line + [''] * (len(HEADER) - len(mid_line)))

sc3_rn = str(sc_row_base + 2)
ceil_line = [
    '100% Fill Ceiling',
    '100% all tiers',
    'T1 $15 / T2 $10 / T3 $5 / RU $2',
    f'=F{t1_row}*1.0/1000*15*12',
    f'=F{t2_row}*1.0/1000*10*12',
    f'=F{t3_row}*1.0/1000*5*12',
    f'=F{ru_row}*1.0/1000*2*12',
    f'=D{sc3_rn}+E{sc3_rn}+F{sc3_rn}+G{sc3_rn}',
    f'=P{gt_rn}',
    f'=H{sc3_rn}+I{sc3_rn}',
]
output_lines.append(ceil_line + [''] * (len(HEADER) - len(ceil_line)))

# --- ASSUMPTIONS ---
output_lines.append([])
output_lines.append(['ASSUMPTIONS'] + [''] * (len(HEADER) - 1))
output_lines.append([])
assumptions = [
    ['Parameter', 'Value', 'Notes'],
    ['Ad pod max duration', '60 seconds', 'Up to 60s of ads per ~45 min match (as many slots as fit)'],
    ['Impressions per pod', '3', 'Average 3x20s creatives within a 60s pod'],
    ['Ad pods per user per month', '28', '1 pod per daily session x 28 days'],
    ['Monthly Sessions source', 'Feb 2026 Looker data', 'Free users, total finished matchmaking matches'],
    ['Paid fill rate (T1/T2)', '20%', 'Conservative Year 1 assumption'],
    ['Paid fill rate (T3/RU)', '10%', 'Lower demand in smaller geos; Russia at $2 CPM'],
    ['House ads fill', '80%', 'Unfilled pods serve subscription promotions'],
    ['Subs conversion rate', '0.05%', 'Of house ad viewers'],
    ['Subs cannibalisation', '50%', 'Half would have subscribed anyway'],
    ['Sub price', '$7.30/month', 'FACEIT Premium monthly price'],
    ['Russia', 'Included at $2 CPM', 'GAM limited but not fully excluded; inventory value shown'],
]
for a in assumptions:
    output_lines.append(a + [''] * (len(HEADER) - len(a)))

# --- Write output ---
with open(OUTPUT, 'w', newline='') as f:
    writer = csv.writer(f)
    for line in output_lines:
        writer.writerow(line)

print(f"\nWrote {len(output_lines)} rows to {OUTPUT}")

# --- Also compute actual values for the one-pager ---
# We need concrete numbers for the markdown doc

# Compute tier subtotals
tier_sessions = {'Tier 1': 0, 'Tier 2': 0, 'Tier 3': 0, 'Russia': 0}
tier_user_counts = {'Tier 1': 0, 'Tier 2': 0, 'Tier 3': 0, 'Russia': 0}
tier_country_counts = {'Tier 1': 0, 'Tier 2': 0, 'Tier 3': 0, 'Russia': 0}

for r in rows:
    tier_sessions[r['tier']] += r['sessions']
    tier_country_counts[r['tier']] += 1
    if r['users']:
        tier_user_counts[r['tier']] += r['users']

print("\n=== TIER SUBTOTALS ===")
total_sessions = 0
for t in ['Tier 1', 'Tier 2', 'Tier 3', 'Russia']:
    s = tier_sessions[t]
    total_sessions += s
    pct = s / sum(tier_sessions.values()) * 100
    print(f"{t} ({tier_country_counts[t]} countries): {s:>12,} sessions ({pct:.1f}%)")
print(f"{'TOTAL':35}: {total_sessions:>12,} sessions")
print(f"{'TOTAL EXCL RU':35}: {total_sessions - tier_sessions['Russia']:>12,} sessions")

# Scenario calcs
print("\n=== SCENARIO COMPARISON (ANNUAL) ===")
# Revenue = impressions / 1000 * CPM * 12, where impressions = sessions * 3
t1_cons = tier_sessions['Tier 1'] * 3 * 0.20 / 1000 * 15 * 12
t2_cons = tier_sessions['Tier 2'] * 3 * 0.20 / 1000 * 10 * 12
t3_cons = tier_sessions['Tier 3'] * 3 * 0.10 / 1000 * 5 * 12
ru_cons = tier_sessions['Russia'] * 3 * 0.10 / 1000 * 2 * 12
total_ad_cons = t1_cons + t2_cons + t3_cons + ru_cons

# Subs
total_all_sessions = sum(tier_sessions.values())
# Unfilled = total sessions * weighted unfilled rate
# Actually subs are based on ALL unfilled pods including Russia
# For simplicity: unfilled = total_sessions - filled
filled_cons = (tier_sessions['Tier 1'] * 0.20 + tier_sessions['Tier 2'] * 0.20 + 
               tier_sessions['Tier 3'] * 0.10 + tier_sessions['Russia'] * 0.10)
unfilled_cons = total_all_sessions - filled_cons
subs_gross = unfilled_cons * 0.0005
subs_net = subs_gross * 0.50
subs_rev_monthly = subs_net * 7.30
subs_rev_annual = subs_rev_monthly * 12

print(f"Conservative: T1 ${t1_cons:,.0f} + T2 ${t2_cons:,.0f} + T3 ${t3_cons:,.0f} + RU ${ru_cons:,.0f} = ${total_ad_cons:,.0f}")
print(f"Subs (annual): ${subs_rev_annual:,.0f}")
print(f"Combined: ${total_ad_cons + subs_rev_annual:,.0f}")

# Mid: T1 $20/20%, T2 $15/20%, T3 $5/10%, RU $2/10%
t1_mid = tier_sessions['Tier 1'] * 3 * 0.20 / 1000 * 20 * 12
t2_mid = tier_sessions['Tier 2'] * 3 * 0.20 / 1000 * 15 * 12
t3_mid = tier_sessions['Tier 3'] * 3 * 0.10 / 1000 * 5 * 12
ru_mid = tier_sessions['Russia'] * 3 * 0.10 / 1000 * 2 * 12
total_ad_mid = t1_mid + t2_mid + t3_mid + ru_mid
print(f"Mid: T1 ${t1_mid:,.0f} + T2 ${t2_mid:,.0f} + T3 ${t3_mid:,.0f} + RU ${ru_mid:,.0f} = ${total_ad_mid:,.0f}")
print(f"Combined: ${total_ad_mid + subs_rev_annual:,.0f}")

# Ceiling: 100% fill, T1 $15, T2 $10, T3 $5, RU $2
t1_ceil = tier_sessions['Tier 1'] * 3 * 1.0 / 1000 * 15 * 12
t2_ceil = tier_sessions['Tier 2'] * 3 * 1.0 / 1000 * 10 * 12
t3_ceil = tier_sessions['Tier 3'] * 3 * 1.0 / 1000 * 5 * 12
ru_ceil = tier_sessions['Russia'] * 3 * 1.0 / 1000 * 2 * 12
total_ad_ceil = t1_ceil + t2_ceil + t3_ceil + ru_ceil
# Subs at ceiling: 0 unfilled (but that's unrealistic, use same subs number)
print(f"Ceiling: T1 ${t1_ceil:,.0f} + T2 ${t2_ceil:,.0f} + T3 ${t3_ceil:,.0f} + RU ${ru_ceil:,.0f} = ${total_ad_ceil:,.0f}")
print(f"Combined: ${total_ad_ceil + subs_rev_annual:,.0f}")

# Inventory value table (100% fill, per-tier)
print("\n=== INVENTORY VALUE (100% fill, monthly, 3 imp/pod) ===")
for t, cpm_label in [('Tier 1', '$15'), ('Tier 2', '$10'), ('Tier 3', '$5'), ('Russia', '$2')]:
    cpm = {'Tier 1': 15, 'Tier 2': 10, 'Tier 3': 5, 'Russia': 2}[t]
    impressions = tier_sessions[t] * 3
    monthly = impressions / 1000 * cpm
    annual = monthly * 12
    print(f"{t}: {tier_sessions[t]:>12,} sessions x 3 imp = {impressions:>12,} imp x {cpm_label} CPM = ${monthly:>10,.0f}/mo = ${annual:>12,.0f}/yr")

total_inv_monthly = sum(tier_sessions[t] * 3 / 1000 * {'Tier 1': 15, 'Tier 2': 10, 'Tier 3': 5, 'Russia': 2}[t] for t in tier_sessions)
print(f"TOTAL: ${total_inv_monthly:>10,.0f}/mo = ${total_inv_monthly * 12:>12,.0f}/yr")
