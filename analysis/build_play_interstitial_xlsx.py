#!/usr/bin/env python3
"""
Build Play Interstitial Business Case spreadsheet (.xlsx) matching
the One Pager column structure (A–R).

Model: pods = sessions (1 pod per match), impressions = pods × 3.
Data: Feb 2026 free users only (37.3M sessions, 1.5M players).

Uses xlsxwriter to write both formulas AND cached values so Google Sheets
can read the file correctly.
"""

import csv
import xlsxwriter
import math

# --- Data files ---
DATA_FILE = '/Users/moritznatalini/Desktop/Master_Product_Folder/data/brand_integrations/faceit fact__daily_active_players 2026-03-24T1038.csv'
TIER_FILE = '/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/Tier country  - Sheet1.csv'
OUTPUT = '/Users/moritznatalini/Desktop/Master_Product_Folder/data/brand_integrations/Play Inter Biz Case - Calculations.xlsx'

# --- Assumptions ---
IMPRESSIONS_PER_POD = 3       # 3×20s avg creatives within a 60s pod
FILL_RATE_T1_T2 = 0.20       # 20% paid fill rate
FILL_RATE_T3 = 0.10          # 10% fill rate
FILL_RATE_RU = 0.10          # 10% fill rate at $2 CPM
CPM_T1 = 15                  # Conservative
CPM_T2 = 10                  # Conservative
CPM_T3 = 5
CPM_RU = 2
SUBS_CONV = 0.0005           # 0.05%
SUBS_CANNIBALISATION = 0.50
SUB_PRICE = 7.30

# --- ISO → Country name mapping ---
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
    'MK': 'North Macedonia', 'XK': 'Kosovo',
    'IR': 'Iran', 'PK': 'Pakistan',
    # Additional from data
    'AX': 'Åland Islands', 'RE': 'Réunion', 'CI': "Côte d'Ivoire",
    'SN': 'Senegal', 'AD': 'Andorra', 'AO': 'Angola', 'MR': 'Mauritania',
    'TG': 'Togo', 'TD': 'Chad', 'DJ': 'Djibouti', 'GA': 'Gabon',
    'CW': 'Curaçao', 'TT': 'Trinidad and Tobago', 'MG': 'Madagascar',
    'BS': 'Bahamas', 'GP': 'Guadeloupe', 'ET': 'Ethiopia', 'AW': 'Aruba',
    'ZW': 'Zimbabwe', 'AF': 'Afghanistan', 'MF': 'Saint Martin',
    'BQ': 'Bonaire', 'GI': 'Gibraltar', 'GN': 'Guinea', 'BJ': 'Benin',
    'CD': 'DR Congo', 'ML': 'Mali', 'PM': 'Saint Pierre and Miquelon',
    'TL': 'Timor-Leste', 'GF': 'French Guiana', 'BM': 'Bermuda',
    'CV': 'Cape Verde', 'CM': 'Cameroon', 'GY': 'Guyana', 'SM': 'San Marino',
    'SR': 'Suriname', 'NE': 'Niger', 'YE': 'Yemen', 'BB': 'Barbados',
    'VU': 'Vanuatu', 'BT': 'Bhutan', 'PG': 'Papua New Guinea',
    'DM': 'Dominica', 'AG': 'Antigua and Barbuda', 'LR': 'Liberia',
    'BF': 'Burkina Faso', 'BL': 'Saint Barthélemy', 'BZ': 'Belize',
    'VI': 'US Virgin Islands', 'RW': 'Rwanda', 'NA': 'Namibia',
    'SD': 'Sudan', 'UG': 'Uganda', 'CU': 'Cuba', 'KE': 'Kenya',
    'MV': 'Maldives',
}

# ---- Load tier classification ----
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
    iso_upper = iso.upper().strip()
    if iso_upper == 'RU':
        return 'Russia'
    country = ISO_TO_COUNTRY.get(iso_upper, '')
    if country in tiers:
        return tiers[country]
    return 'Tier 3'

# ---- Load data ----
rows = []
with open(DATA_FILE, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # header line 1
    next(reader)  # header line 2
    for row in reader:
        if len(row) >= 3:
            iso = row[0].strip()
            sessions_str = row[1].replace(',', '').strip()
            players_str = row[2].replace(',', '').strip()
            if iso and sessions_str:
                try:
                    sessions = int(sessions_str)
                    players = int(players_str) if players_str else 0
                    if sessions > 0:
                        tier = get_tier(iso)
                        rows.append({
                            'tier': tier,
                            'iso': iso,
                            'sessions': sessions,
                            'players': players,
                        })
                except ValueError:
                    pass

# Sort by tier priority then sessions DESC
tier_order = {'Tier 1': 0, 'Tier 2': 1, 'Tier 3': 2, 'Russia': 3}
rows.sort(key=lambda r: (tier_order.get(r['tier'], 99), -r['sessions']))

print(f"Loaded {len(rows)} countries")

# Count per tier
tier_counts = {}
tier_sessions = {}
for r in rows:
    tier_counts[r['tier']] = tier_counts.get(r['tier'], 0) + 1
    tier_sessions[r['tier']] = tier_sessions.get(r['tier'], 0) + r['sessions']

for t in ['Tier 1', 'Tier 2', 'Tier 3', 'Russia']:
    print(f"  {t}: {tier_counts.get(t, 0)} countries, {tier_sessions.get(t, 0):,} sessions")
print(f"  TOTAL: {sum(tier_sessions.values()):,} sessions")

# ---- Assign fill rate and CPM per tier ----
def get_fill_cpm(tier):
    if tier == 'Tier 1':
        return FILL_RATE_T1_T2, CPM_T1
    elif tier == 'Tier 2':
        return FILL_RATE_T1_T2, CPM_T2
    elif tier == 'Russia':
        return FILL_RATE_RU, CPM_RU
    else:  # Tier 3
        return FILL_RATE_T3, CPM_T3

# ---- Build XLSX ----
wb = xlsxwriter.Workbook(OUTPUT)

# Formats
header_fmt = wb.add_format({
    'bold': True, 'bg_color': '#D9E1F2', 'border': 1,
    'text_wrap': True, 'valign': 'vcenter', 'align': 'center',
    'font_size': 10,
})
num_fmt = wb.add_format({'num_format': '#,##0', 'font_size': 10})
pct_fmt = wb.add_format({'num_format': '0%', 'font_size': 10})
dollar_fmt = wb.add_format({'num_format': '$#,##0', 'font_size': 10})
dollar2_fmt = wb.add_format({'num_format': '$#,##0.00', 'font_size': 10})
text_fmt = wb.add_format({'font_size': 10})
tier_fmt = wb.add_format({'font_size': 10, 'bold': False})
subtotal_fmt = wb.add_format({
    'bold': True, 'bg_color': '#E2EFDA', 'border': 1,
    'num_format': '#,##0', 'font_size': 10,
})
subtotal_dollar = wb.add_format({
    'bold': True, 'bg_color': '#E2EFDA', 'border': 1,
    'num_format': '$#,##0', 'font_size': 10,
})
subtotal_text = wb.add_format({
    'bold': True, 'bg_color': '#E2EFDA', 'border': 1,
    'font_size': 10,
})
grand_fmt = wb.add_format({
    'bold': True, 'bg_color': '#FCE4D6', 'border': 1,
    'num_format': '#,##0', 'font_size': 10,
})
grand_dollar = wb.add_format({
    'bold': True, 'bg_color': '#FCE4D6', 'border': 1,
    'num_format': '$#,##0', 'font_size': 10,
})
grand_text = wb.add_format({
    'bold': True, 'bg_color': '#FCE4D6', 'border': 1,
    'font_size': 10,
})
scenario_header_fmt = wb.add_format({
    'bold': True, 'bg_color': '#D9E1F2', 'border': 1,
    'text_wrap': True, 'font_size': 10,
})
scenario_fmt = wb.add_format({'font_size': 10, 'border': 1})
scenario_dollar = wb.add_format({
    'font_size': 10, 'border': 1, 'num_format': '$#,##0',
})
assumption_header = wb.add_format({
    'bold': True, 'bg_color': '#D9E1F2', 'font_size': 10, 'border': 1,
})
assumption_fmt = wb.add_format({'font_size': 10})
section_header = wb.add_format({
    'bold': True, 'font_size': 12, 'bottom': 2,
})

# ---- HEADERS (Row 0 in xlsxwriter = Row 1 in Excel) ----
# Columns: A=Tier, B=Country, C=Monthly Sessions, D=Unique Users,
# E=Ad Pods/Month, F=Impressions/Month, G=Fill Rate, H=Filled Impressions,
# I=CPM, J=Monthly Ad Rev, K=Annual Ad Rev, L=House Ads (unfilled pods),
# M=Subs Conversion, N=Cannibalisation, O=Monthly Subs Rev,
# P=Annual Subs Rev, Q=Monthly Total, R=Annual Total

HEADERS = [
    'Tier',                          # A
    'Country',                       # B
    'Monthly Sessions',              # C
    'Unique Users',                  # D
    'Ad Pods/Month',                 # E
    'Impressions/Month',             # F
    'Fill Rate',                     # G
    'Filled Impressions',            # H
    'CPM ($)',                       # I
    'Monthly Ad Rev ($)',            # J
    'Annual Ad Rev ($)',             # K
    'House Ads\n(unfilled pods)',    # L
    'Subs Conversion\n(0.05%)',      # M
    'Cannibalisation\n(50%)',        # N
    'Monthly Subs Rev ($)',          # O
    'Annual Subs Rev ($)',           # P
    'Monthly Total ($)',             # Q
    'Annual Total ($)',              # R
]

ws = wb.add_worksheet('Play Inter Biz Case')

# Column widths
col_widths = [8, 6, 16, 14, 16, 18, 10, 18, 8, 18, 18, 18, 16, 16, 18, 18, 18, 18]
for i, w in enumerate(col_widths):
    ws.set_column(i, i, w)

# Write headers (row 0 = Excel row 1)
for c, h in enumerate(HEADERS):
    ws.write(0, c, h, header_fmt)
ws.freeze_panes(1, 0)  # Freeze header row

# ---- DATA ROWS (row 1+ in xlsxwriter = row 2+ in Excel) ----
for i, r in enumerate(rows):
    row_xl = i + 1  # xlsxwriter row (0-indexed)
    rn = i + 2       # Excel row number (1-indexed)
    
    fill, cpm = get_fill_cpm(r['tier'])
    
    # Cached computed values
    pods = r['sessions']       # E = C
    impressions = pods * 3     # F = E * 3
    filled_imp = impressions * fill  # H = F * G
    monthly_ad_rev = filled_imp / 1000 * cpm  # J = H/1000 * I
    annual_ad_rev = monthly_ad_rev * 12  # K = J * 12
    unfilled_pods = pods * (1 - fill)  # L = E * (1-G)
    subs_conv = unfilled_pods * SUBS_CONV  # M = L * 0.0005
    cannibalisation = subs_conv * SUBS_CANNIBALISATION  # N = M * 0.5
    monthly_subs_rev = cannibalisation * SUB_PRICE  # O = N * 7.30
    annual_subs_rev = monthly_subs_rev * 12  # P = O * 12
    monthly_total = monthly_ad_rev + monthly_subs_rev  # Q = J + O
    annual_total = annual_ad_rev + annual_subs_rev  # R = K + P
    
    # A: Tier
    ws.write(row_xl, 0, r['tier'], tier_fmt)
    # B: Country ISO
    ws.write(row_xl, 1, r['iso'], text_fmt)
    # C: Monthly Sessions (data)
    ws.write(row_xl, 2, r['sessions'], num_fmt)
    # D: Unique Users (data)
    ws.write(row_xl, 3, r['players'], num_fmt)
    # E: Ad Pods/Month = C (formula + cached)
    ws.write_formula(row_xl, 4, f'=C{rn}', num_fmt, pods)
    # F: Impressions/Month = E * 3 (formula + cached)
    ws.write_formula(row_xl, 5, f'=E{rn}*3', num_fmt, impressions)
    # G: Fill Rate (data)
    ws.write(row_xl, 6, fill, pct_fmt)
    # H: Filled Impressions = F * G (formula + cached)
    ws.write_formula(row_xl, 7, f'=F{rn}*G{rn}', num_fmt, filled_imp)
    # I: CPM (data)
    ws.write(row_xl, 8, cpm, dollar_fmt)
    # J: Monthly Ad Rev = H/1000 * I (formula + cached)
    ws.write_formula(row_xl, 9, f'=H{rn}/1000*I{rn}', dollar_fmt, monthly_ad_rev)
    # K: Annual Ad Rev = J * 12 (formula + cached)
    ws.write_formula(row_xl, 10, f'=J{rn}*12', dollar_fmt, annual_ad_rev)
    # L: House Ads unfilled pods = E * (1 - G) (formula + cached)
    ws.write_formula(row_xl, 11, f'=E{rn}*(1-G{rn})', num_fmt, unfilled_pods)
    # M: Subs Conversion = L * 0.0005 (formula + cached)
    ws.write_formula(row_xl, 12, f'=L{rn}*0.0005', num_fmt, subs_conv)
    # N: Cannibalisation = M * 0.5 (formula + cached)
    ws.write_formula(row_xl, 13, f'=M{rn}*0.5', num_fmt, cannibalisation)
    # O: Monthly Subs Rev = N * 7.30 (formula + cached)
    ws.write_formula(row_xl, 14, f'=N{rn}*7.30', dollar_fmt, monthly_subs_rev)
    # P: Annual Subs Rev = O * 12 (formula + cached)
    ws.write_formula(row_xl, 15, f'=O{rn}*12', dollar_fmt, annual_subs_rev)
    # Q: Monthly Total = J + O (formula + cached)
    ws.write_formula(row_xl, 16, f'=J{rn}+O{rn}', dollar_fmt, monthly_total)
    # R: Annual Total = K + P (formula + cached)
    ws.write_formula(row_xl, 17, f'=K{rn}+P{rn}', dollar_fmt, annual_total)

data_last_row = len(rows) + 1  # Last data Excel row number
print(f"Data rows: 2 to {data_last_row} (Excel), {len(rows)} countries")

# ---- BLANK ROW + SUBTOTALS ----
blank_row = len(rows) + 1  # xlsxwriter row
ws.write(blank_row, 0, '', text_fmt)

# Section header
section_row = blank_row + 1
ws.write(section_row, 0, 'SUBTOTALS BY TIER', section_header)

# Subtotal rows
subtotal_tiers = ['Tier 1', 'Tier 2', 'Tier 3', 'Russia']
subtotal_start_xl = section_row + 1  # xlsxwriter row
subtotal_excel_rows = {}  # tier → Excel row number

for idx, tier_name in enumerate(subtotal_tiers):
    xl_row = subtotal_start_xl + idx
    rn = xl_row + 1  # Excel row number
    subtotal_excel_rows[tier_name] = rn
    count = tier_counts.get(tier_name, 0)
    label = f'{count} countries' if tier_name != 'Russia' else 'RU'
    
    # Compute cached subtotals
    tier_data = [r for r in rows if r['tier'] == tier_name]
    fill, cpm = get_fill_cpm(tier_name)
    c_sum_sessions = sum(r['sessions'] for r in tier_data)
    c_sum_players = sum(r['players'] for r in tier_data)
    c_sum_pods = c_sum_sessions  # E = C
    c_sum_impressions = c_sum_pods * 3
    c_sum_filled = c_sum_impressions * fill
    c_sum_monthly_ad = c_sum_filled / 1000 * cpm
    c_sum_annual_ad = c_sum_monthly_ad * 12
    c_sum_unfilled = c_sum_pods * (1 - fill)
    c_sum_subs_conv = c_sum_unfilled * SUBS_CONV
    c_sum_cannibal = c_sum_subs_conv * SUBS_CANNIBALISATION
    c_sum_monthly_subs = c_sum_cannibal * SUB_PRICE
    c_sum_annual_subs = c_sum_monthly_subs * 12
    c_sum_monthly_total = c_sum_monthly_ad + c_sum_monthly_subs
    c_sum_annual_total = c_sum_annual_ad + c_sum_annual_subs
    
    # A: Tier name
    ws.write(xl_row, 0, tier_name, subtotal_text)
    # B: Label
    ws.write(xl_row, 1, label, subtotal_text)
    # C: Sessions SUMIF
    ws.write_formula(xl_row, 2,
        f'=SUMIF($A$2:$A${data_last_row},"{tier_name}",C$2:C${data_last_row})',
        subtotal_fmt, c_sum_sessions)
    # D: Users SUMIF
    ws.write_formula(xl_row, 3,
        f'=SUMIF($A$2:$A${data_last_row},"{tier_name}",D$2:D${data_last_row})',
        subtotal_fmt, c_sum_players)
    # E: Pods SUMIF
    ws.write_formula(xl_row, 4,
        f'=SUMIF($A$2:$A${data_last_row},"{tier_name}",E$2:E${data_last_row})',
        subtotal_fmt, c_sum_pods)
    # F: Impressions SUMIF
    ws.write_formula(xl_row, 5,
        f'=SUMIF($A$2:$A${data_last_row},"{tier_name}",F$2:F${data_last_row})',
        subtotal_fmt, c_sum_impressions)
    # G: Fill rate (blank — varies)
    ws.write(xl_row, 6, '', subtotal_text)
    # H: Filled Impressions SUMIF
    ws.write_formula(xl_row, 7,
        f'=SUMIF($A$2:$A${data_last_row},"{tier_name}",H$2:H${data_last_row})',
        subtotal_fmt, c_sum_filled)
    # I: CPM (blank — varies)
    ws.write(xl_row, 8, '', subtotal_text)
    # J: Monthly Ad Rev SUMIF
    ws.write_formula(xl_row, 9,
        f'=SUMIF($A$2:$A${data_last_row},"{tier_name}",J$2:J${data_last_row})',
        subtotal_dollar, c_sum_monthly_ad)
    # K: Annual Ad Rev = J * 12
    ws.write_formula(xl_row, 10, f'=J{rn}*12', subtotal_dollar, c_sum_annual_ad)
    # L: House Ads SUMIF
    ws.write_formula(xl_row, 11,
        f'=SUMIF($A$2:$A${data_last_row},"{tier_name}",L$2:L${data_last_row})',
        subtotal_fmt, c_sum_unfilled)
    # M: Subs Conversion SUMIF
    ws.write_formula(xl_row, 12,
        f'=SUMIF($A$2:$A${data_last_row},"{tier_name}",M$2:M${data_last_row})',
        subtotal_fmt, c_sum_subs_conv)
    # N: Cannibalisation SUMIF
    ws.write_formula(xl_row, 13,
        f'=SUMIF($A$2:$A${data_last_row},"{tier_name}",N$2:N${data_last_row})',
        subtotal_fmt, c_sum_cannibal)
    # O: Monthly Subs Rev SUMIF
    ws.write_formula(xl_row, 14,
        f'=SUMIF($A$2:$A${data_last_row},"{tier_name}",O$2:O${data_last_row})',
        subtotal_dollar, c_sum_monthly_subs)
    # P: Annual Subs Rev = O * 12
    ws.write_formula(xl_row, 15, f'=O{rn}*12', subtotal_dollar, c_sum_annual_subs)
    # Q: Monthly Total = J + O
    ws.write_formula(xl_row, 16, f'=J{rn}+O{rn}', subtotal_dollar, c_sum_monthly_total)
    # R: Annual Total = K + P
    ws.write_formula(xl_row, 17, f'=K{rn}+P{rn}', subtotal_dollar, c_sum_annual_total)

# ---- GRAND TOTAL ----
gt_xl = subtotal_start_xl + len(subtotal_tiers)
gt_rn = gt_xl + 1  # Excel row
st_first = subtotal_excel_rows['Tier 1']
st_last = subtotal_excel_rows['Russia']

# Compute grand total cached values
gt_sessions = sum(tier_sessions.values())
gt_players = sum(r['players'] for r in rows)
gt_pods = gt_sessions
gt_impressions = gt_pods * 3
gt_filled = sum(tier_sessions[t] * 3 * get_fill_cpm(t)[0] for t in subtotal_tiers)
gt_monthly_ad = sum(tier_sessions[t] * 3 * get_fill_cpm(t)[0] / 1000 * get_fill_cpm(t)[1] for t in subtotal_tiers)
gt_annual_ad = gt_monthly_ad * 12
gt_unfilled = sum(tier_sessions[t] * (1 - get_fill_cpm(t)[0]) for t in subtotal_tiers)
gt_subs_conv = gt_unfilled * SUBS_CONV
gt_cannibal = gt_subs_conv * SUBS_CANNIBALISATION
gt_monthly_subs = gt_cannibal * SUB_PRICE
gt_annual_subs = gt_monthly_subs * 12
gt_monthly_total = gt_monthly_ad + gt_monthly_subs
gt_annual_total = gt_annual_ad + gt_annual_subs

ws.write(gt_xl, 0, 'GRAND TOTAL', grand_text)
ws.write(gt_xl, 1, 'All', grand_text)
ws.write_formula(gt_xl, 2, f'=SUM(C{st_first}:C{st_last})', grand_fmt, gt_sessions)
ws.write_formula(gt_xl, 3, f'=SUM(D{st_first}:D{st_last})', grand_fmt, gt_players)
ws.write_formula(gt_xl, 4, f'=SUM(E{st_first}:E{st_last})', grand_fmt, gt_pods)
ws.write_formula(gt_xl, 5, f'=SUM(F{st_first}:F{st_last})', grand_fmt, gt_impressions)
ws.write(gt_xl, 6, '', grand_text)
ws.write_formula(gt_xl, 7, f'=SUM(H{st_first}:H{st_last})', grand_fmt, gt_filled)
ws.write(gt_xl, 8, '', grand_text)
ws.write_formula(gt_xl, 9, f'=SUM(J{st_first}:J{st_last})', grand_dollar, gt_monthly_ad)
ws.write_formula(gt_xl, 10, f'=J{gt_rn}*12', grand_dollar, gt_annual_ad)
ws.write_formula(gt_xl, 11, f'=SUM(L{st_first}:L{st_last})', grand_fmt, gt_unfilled)
ws.write_formula(gt_xl, 12, f'=SUM(M{st_first}:M{st_last})', grand_fmt, gt_subs_conv)
ws.write_formula(gt_xl, 13, f'=SUM(N{st_first}:N{st_last})', grand_fmt, gt_cannibal)
ws.write_formula(gt_xl, 14, f'=SUM(O{st_first}:O{st_last})', grand_dollar, gt_monthly_subs)
ws.write_formula(gt_xl, 15, f'=O{gt_rn}*12', grand_dollar, gt_annual_subs)
ws.write_formula(gt_xl, 16, f'=J{gt_rn}+O{gt_rn}', grand_dollar, gt_monthly_total)
ws.write_formula(gt_xl, 17, f'=K{gt_rn}+P{gt_rn}', grand_dollar, gt_annual_total)

# ---- GRAND TOTAL EXCL RUSSIA ----
gt_excl_xl = gt_xl + 1
gt_excl_rn = gt_excl_xl + 1
t1r = subtotal_excel_rows['Tier 1']
t2r = subtotal_excel_rows['Tier 2']
t3r = subtotal_excel_rows['Tier 3']

excl_sessions = gt_sessions - tier_sessions.get('Russia', 0)
excl_players = gt_players - sum(r['players'] for r in rows if r['tier'] == 'Russia')
excl_pods = excl_sessions
excl_impressions = excl_pods * 3
excl_filled = sum(tier_sessions[t] * 3 * get_fill_cpm(t)[0] for t in ['Tier 1', 'Tier 2', 'Tier 3'])
excl_monthly_ad = sum(tier_sessions[t] * 3 * get_fill_cpm(t)[0] / 1000 * get_fill_cpm(t)[1] for t in ['Tier 1', 'Tier 2', 'Tier 3'])
excl_annual_ad = excl_monthly_ad * 12
excl_unfilled = sum(tier_sessions[t] * (1 - get_fill_cpm(t)[0]) for t in ['Tier 1', 'Tier 2', 'Tier 3'])
excl_subs_conv = excl_unfilled * SUBS_CONV
excl_cannibal = excl_subs_conv * SUBS_CANNIBALISATION
excl_monthly_subs = excl_cannibal * SUB_PRICE
excl_annual_subs = excl_monthly_subs * 12
excl_monthly_total = excl_monthly_ad + excl_monthly_subs
excl_annual_total = excl_annual_ad + excl_annual_subs

ws.write(gt_excl_xl, 0, 'TOTAL EXCL RU', grand_text)
ws.write(gt_excl_xl, 1, 'All excl. Russia', grand_text)
ws.write_formula(gt_excl_xl, 2, f'=C{t1r}+C{t2r}+C{t3r}', grand_fmt, excl_sessions)
ws.write_formula(gt_excl_xl, 3, f'=D{t1r}+D{t2r}+D{t3r}', grand_fmt, excl_players)
ws.write_formula(gt_excl_xl, 4, f'=E{t1r}+E{t2r}+E{t3r}', grand_fmt, excl_pods)
ws.write_formula(gt_excl_xl, 5, f'=F{t1r}+F{t2r}+F{t3r}', grand_fmt, excl_impressions)
ws.write(gt_excl_xl, 6, '', grand_text)
ws.write_formula(gt_excl_xl, 7, f'=H{t1r}+H{t2r}+H{t3r}', grand_fmt, excl_filled)
ws.write(gt_excl_xl, 8, '', grand_text)
ws.write_formula(gt_excl_xl, 9, f'=J{t1r}+J{t2r}+J{t3r}', grand_dollar, excl_monthly_ad)
ws.write_formula(gt_excl_xl, 10, f'=J{gt_excl_rn}*12', grand_dollar, excl_annual_ad)
ws.write_formula(gt_excl_xl, 11, f'=L{t1r}+L{t2r}+L{t3r}', grand_fmt, excl_unfilled)
ws.write_formula(gt_excl_xl, 12, f'=M{t1r}+M{t2r}+M{t3r}', grand_fmt, excl_subs_conv)
ws.write_formula(gt_excl_xl, 13, f'=N{t1r}+N{t2r}+N{t3r}', grand_fmt, excl_cannibal)
ws.write_formula(gt_excl_xl, 14, f'=O{t1r}+O{t2r}+O{t3r}', grand_dollar, excl_monthly_subs)
ws.write_formula(gt_excl_xl, 15, f'=O{gt_excl_rn}*12', grand_dollar, excl_annual_subs)
ws.write_formula(gt_excl_xl, 16, f'=J{gt_excl_rn}+O{gt_excl_rn}', grand_dollar, excl_monthly_total)
ws.write_formula(gt_excl_xl, 17, f'=K{gt_excl_rn}+P{gt_excl_rn}', grand_dollar, excl_annual_total)

# ---- SCENARIO COMPARISON ----
sc_blank = gt_excl_xl + 2
ws.write(sc_blank, 0, 'SCENARIO COMPARISON (ANNUAL)', section_header)

sc_header_row = sc_blank + 1
sc_headers = [
    'Scenario', 'Fill Rate', 'CPM Assumption',
    'T1 Annual ($)', 'T2 Annual ($)', 'T3 Annual ($)', 'RU Annual ($)',
    'Total Ad Rev ($)', 'Subs Rev ($)', 'Combined ($)',
]
for c, h in enumerate(sc_headers):
    ws.write(sc_header_row, c, h, scenario_header_fmt)

t1_imp_ref = f'F{t1r}'  # Tier 1 impressions
t2_imp_ref = f'F{t2r}'  # Tier 2 impressions
t3_imp_ref = f'F{t3r}'  # Tier 3 impressions
ru_imp_ref = f'F{subtotal_excel_rows["Russia"]}'  # Russia impressions

subs_annual_ref = f'P{gt_rn}'  # Grand Total annual subs rev

# Compute scenario cached values
t1_imp = tier_sessions.get('Tier 1', 0) * 3
t2_imp = tier_sessions.get('Tier 2', 0) * 3
t3_imp = tier_sessions.get('Tier 3', 0) * 3
ru_imp = tier_sessions.get('Russia', 0) * 3

# Conservative: 20% T1@$15, 20% T2@$10, 10% T3@$5, 10% RU@$2
cons_t1 = t1_imp * 0.20 / 1000 * 15 * 12
cons_t2 = t2_imp * 0.20 / 1000 * 10 * 12
cons_t3 = t3_imp * 0.10 / 1000 * 5 * 12
cons_ru = ru_imp * 0.10 / 1000 * 2 * 12
cons_total_ad = cons_t1 + cons_t2 + cons_t3 + cons_ru
cons_combined = cons_total_ad + gt_annual_subs

sc1_xl = sc_header_row + 1
sc1_rn = sc1_xl + 1
ws.write(sc1_xl, 0, 'Conservative (Year 1)', scenario_fmt)
ws.write(sc1_xl, 1, '20% T1/T2, 10% T3/RU', scenario_fmt)
ws.write(sc1_xl, 2, 'T1 $15 / T2 $10 / T3 $5 / RU $2', scenario_fmt)
ws.write_formula(sc1_xl, 3, f'={t1_imp_ref}*0.20/1000*15*12', scenario_dollar, cons_t1)
ws.write_formula(sc1_xl, 4, f'={t2_imp_ref}*0.20/1000*10*12', scenario_dollar, cons_t2)
ws.write_formula(sc1_xl, 5, f'={t3_imp_ref}*0.10/1000*5*12', scenario_dollar, cons_t3)
ws.write_formula(sc1_xl, 6, f'={ru_imp_ref}*0.10/1000*2*12', scenario_dollar, cons_ru)
ws.write_formula(sc1_xl, 7, f'=D{sc1_rn}+E{sc1_rn}+F{sc1_rn}+G{sc1_rn}', scenario_dollar, cons_total_ad)
ws.write_formula(sc1_xl, 8, f'={subs_annual_ref}', scenario_dollar, gt_annual_subs)
ws.write_formula(sc1_xl, 9, f'=H{sc1_rn}+I{sc1_rn}', scenario_dollar, cons_combined)

# Mid Case: 20% T1@$20, 20% T2@$15, 10% T3@$5, 10% RU@$2
mid_t1 = t1_imp * 0.20 / 1000 * 20 * 12
mid_t2 = t2_imp * 0.20 / 1000 * 15 * 12
mid_t3 = t3_imp * 0.10 / 1000 * 5 * 12
mid_ru = ru_imp * 0.10 / 1000 * 2 * 12
mid_total_ad = mid_t1 + mid_t2 + mid_t3 + mid_ru
mid_combined = mid_total_ad + gt_annual_subs

sc2_xl = sc1_xl + 1
sc2_rn = sc2_xl + 1
ws.write(sc2_xl, 0, 'Mid Case', scenario_fmt)
ws.write(sc2_xl, 1, '20% T1/T2, 10% T3/RU', scenario_fmt)
ws.write(sc2_xl, 2, 'T1 $20 / T2 $15 / T3 $5 / RU $2', scenario_fmt)
ws.write_formula(sc2_xl, 3, f'={t1_imp_ref}*0.20/1000*20*12', scenario_dollar, mid_t1)
ws.write_formula(sc2_xl, 4, f'={t2_imp_ref}*0.20/1000*15*12', scenario_dollar, mid_t2)
ws.write_formula(sc2_xl, 5, f'={t3_imp_ref}*0.10/1000*5*12', scenario_dollar, mid_t3)
ws.write_formula(sc2_xl, 6, f'={ru_imp_ref}*0.10/1000*2*12', scenario_dollar, mid_ru)
ws.write_formula(sc2_xl, 7, f'=D{sc2_rn}+E{sc2_rn}+F{sc2_rn}+G{sc2_rn}', scenario_dollar, mid_total_ad)
ws.write_formula(sc2_xl, 8, f'={subs_annual_ref}', scenario_dollar, gt_annual_subs)
ws.write_formula(sc2_xl, 9, f'=H{sc2_rn}+I{sc2_rn}', scenario_dollar, mid_combined)

# 100% Fill Ceiling: T1@$15, T2@$10, T3@$5, RU@$2
ceil_t1 = t1_imp * 1.0 / 1000 * 15 * 12
ceil_t2 = t2_imp * 1.0 / 1000 * 10 * 12
ceil_t3 = t3_imp * 1.0 / 1000 * 5 * 12
ceil_ru = ru_imp * 1.0 / 1000 * 2 * 12
ceil_total_ad = ceil_t1 + ceil_t2 + ceil_t3 + ceil_ru
ceil_combined = ceil_total_ad + gt_annual_subs

sc3_xl = sc2_xl + 1
sc3_rn = sc3_xl + 1
ws.write(sc3_xl, 0, '100% Fill Ceiling', scenario_fmt)
ws.write(sc3_xl, 1, '100% all tiers', scenario_fmt)
ws.write(sc3_xl, 2, 'T1 $15 / T2 $10 / T3 $5 / RU $2', scenario_fmt)
ws.write_formula(sc3_xl, 3, f'={t1_imp_ref}*1.0/1000*15*12', scenario_dollar, ceil_t1)
ws.write_formula(sc3_xl, 4, f'={t2_imp_ref}*1.0/1000*10*12', scenario_dollar, ceil_t2)
ws.write_formula(sc3_xl, 5, f'={t3_imp_ref}*1.0/1000*5*12', scenario_dollar, ceil_t3)
ws.write_formula(sc3_xl, 6, f'={ru_imp_ref}*1.0/1000*2*12', scenario_dollar, ceil_ru)
ws.write_formula(sc3_xl, 7, f'=D{sc3_rn}+E{sc3_rn}+F{sc3_rn}+G{sc3_rn}', scenario_dollar, ceil_total_ad)
ws.write_formula(sc3_xl, 8, f'={subs_annual_ref}', scenario_dollar, gt_annual_subs)
ws.write_formula(sc3_xl, 9, f'=H{sc3_rn}+I{sc3_rn}', scenario_dollar, ceil_combined)

# ---- ASSUMPTIONS ----
assum_blank = sc3_xl + 2
ws.write(assum_blank, 0, 'ASSUMPTIONS', section_header)

assumptions = [
    ['Parameter', 'Value', 'Notes'],
    ['Ad pod max duration', '60 seconds', 'Up to 60s of ads per ~45 min match'],
    ['Impressions per pod', '3', '3x20s avg creatives within a 60s pod'],
    ['Ad pods per match', '1', '1 pod per match session (= 1 pod per session)'],
    ['Monthly Sessions source', 'Feb 2026 Looker/BQ', 'Free users only, finished matchmaking matches'],
    ['Paid fill rate (T1/T2)', '20%', 'Conservative Year 1 assumption'],
    ['Paid fill rate (T3/RU)', '10%', 'Lower demand in smaller geos; Russia at $2 CPM'],
    ['House ads fill', '80%', 'Unfilled pods serve subscription promotions'],
    ['Subs conversion rate', '0.05%', 'Of house ad viewers'],
    ['Subs cannibalisation', '50%', 'Half would have subscribed anyway'],
    ['Sub price', '$7.30/month', 'FACEIT Premium monthly price'],
    ['Russia', 'Included at $2 CPM', 'GAM limited but not fully excluded'],
]

for i, a_row in enumerate(assumptions):
    xl_row = assum_blank + 1 + i
    fmt = assumption_header if i == 0 else assumption_fmt
    for c, val in enumerate(a_row):
        ws.write(xl_row, c, val, fmt)

# ---- Print summary ----
print(f"\n=== ONE PAGER VERIFICATION ===")
print(f"Total sessions (incl Russia): {gt_sessions:,}")
print(f"Total sessions (excl Russia): {excl_sessions:,}")
print(f"Total ad pods: {gt_pods:,}")
print(f"Total impressions: {gt_impressions:,}")
print(f"")
print(f"Tier 1 ({tier_counts.get('Tier 1', 0)} countries): {tier_sessions.get('Tier 1', 0):,} sessions ({tier_sessions.get('Tier 1', 0)/gt_sessions*100:.1f}%)")
print(f"Tier 2 ({tier_counts.get('Tier 2', 0)} countries): {tier_sessions.get('Tier 2', 0):,} sessions ({tier_sessions.get('Tier 2', 0)/gt_sessions*100:.1f}%)")
print(f"Tier 3 ({tier_counts.get('Tier 3', 0)} countries): {tier_sessions.get('Tier 3', 0):,} sessions ({tier_sessions.get('Tier 3', 0)/gt_sessions*100:.1f}%)")
print(f"Russia (1 country): {tier_sessions.get('Russia', 0):,} sessions ({tier_sessions.get('Russia', 0)/gt_sessions*100:.1f}%)")
print(f"")
print(f"One Pager says: ~37M pods / ~111M impressions")
print(f"Spreadsheet:    {gt_pods:,} pods / {gt_impressions:,} impressions")
print(f"")
print(f"=== SCENARIO COMPARISON (ANNUAL) ===")
print(f"Conservative: ${cons_total_ad:,.0f} ad + ${gt_annual_subs:,.0f} subs = ${cons_combined:,.0f}")
print(f"Mid Case:     ${mid_total_ad:,.0f} ad + ${gt_annual_subs:,.0f} subs = ${mid_combined:,.0f}")
print(f"100% Ceiling: ${ceil_total_ad:,.0f} ad + ${gt_annual_subs:,.0f} subs = ${ceil_combined:,.0f}")
print(f"")
print(f"One Pager says:")
print(f"  Conservative: ~$1.3M ad + ~$702K subs = ~$2.0M")
print(f"  Mid:          ~$1.7M")
print(f"  Ceiling:      ~$8.1M ad")

# Row reference summary for One Pager
print(f"\n=== ROW REFERENCES FOR ONE PAGER ===")
print(f"Grand Total row: {gt_rn} (Excel)")
for t in subtotal_tiers:
    print(f"  {t} subtotal: row {subtotal_excel_rows[t]}")
print(f"Grand Total Excl RU: row {gt_excl_rn}")

wb.close()
print(f"\n✅ Wrote {OUTPUT}")
