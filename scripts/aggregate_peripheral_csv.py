#!/usr/bin/env python3
"""
Aggregate peripheral hardware CSV into per-country dashboard data objects.
Outputs JSON that can be injected into the peripheral dashboard HTML.

CSV columns (from header):
  0: Client Hardware Details V2 Manufacturer (Device/BT/USB manufacturer - often empty in col 0)
  1: Client Hardware Details V2 Manufacturer (CPU manufacturer/model)
  2: Client Hardware Details V2 Cores
  3: Client Hardware Details V2 Manufacturer (BT/USB peripheral manufacturer)
  4: Client Hardware Details V2 Device Name (mouse/keyboard)
  5: Client Hardware Details V2 Date
  6: Client Hardware Details V2 User ID
  7: New Tracking Session V1 Country
"""
import csv
import json
import sys
from collections import Counter, defaultdict

# Gaming brands for penetration calculation
GAMING_BRANDS = {
    'logitech', 'razer', 'steelseries', 'corsair', 'hyperx',
    'roccat', 'glorious', 'zowie', 'benq', 'endgame gear',
    'pulsar', 'lamzu', 'finalmouse', 'vaxee', 'ninjutso',
    'ducky', 'wooting', 'cherry', 'xtrfy', 'mad catz',
    'turtle beach', 'astro', 'asus', 'asustek',
    'msi', 'cooler master', 'thermaltake', 'bloody',
    'a4tech', 'redragon', 'fantech', 'varmilo', 'leopold',
    'darmoshark', 'attack shark', 'keychron', 'akko',
    'dragonborn', 'dareu', 'mountain', 'gwolves',
    'lethal gaming gear', 'corepad', 'artisan', 'logi',
}

# Released countries whitelist — ONLY these 91 countries have the feature deployed
# 90 Tier 3 countries + Italy (IT) which was in the initial release alongside TR and IN
RELEASED_COUNTRIES = {
    'AL', 'AM', 'AR', 'AZ', 'BA', 'BD', 'BG', 'BH', 'BN', 'BO',
    'BR', 'BY', 'CL', 'CN', 'CO', 'CR', 'DO', 'DZ', 'EC', 'EG',
    'GE', 'GG', 'GH', 'GL', 'GT', 'GU', 'HK', 'HN', 'ID', 'IL',
    'IM', 'IN', 'IQ', 'IT', 'JE', 'JM', 'KG', 'KH', 'KW', 'KY',
    'KZ', 'LA', 'LB', 'LK', 'LU', 'LY', 'MA', 'MC', 'MD', 'ME',
    'MK', 'MM', 'MN', 'MO', 'MQ', 'MT', 'MU', 'MX', 'MY', 'MZ',
    'NC', 'NG', 'NI', 'NP', 'OM', 'PA', 'PE', 'PF', 'PH', 'PK',
    'PR', 'PS', 'PY', 'QA', 'SV', 'SY', 'TH', 'TJ', 'TM', 'TN',
    'TR', 'TW', 'TZ', 'UA', 'UY', 'UZ', 'VE', 'VN', 'XK', 'ZA',
    'ZM',
}

# Early-release countries (initial pilot — IT, TR, IN)
EARLY_RELEASE = {'IT', 'TR', 'IN'}

# Tier classification (no Tier 1/2 distinction — feature only released in Tier 3 + early release)
# Keeping a simple classification for dashboard grouping
TIER_1 = set()   # Not released in any Tier 1 markets (except IT which moved to early-release)
TIER_2 = set()   # Not released in any Tier 2 markets
RUSSIA = set()   # Not released in Russia

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else '/Users/moritznatalini/Desktop/Master_Product_Folder/data/brand_integrations/faceit-events user_client_hardware_details_v2 2026-03-25T2056.csv'

def classify_tier(country):
    if country in EARLY_RELEASE:
        return 'Early Release'
    else:
        return 'Tier 3'

def is_gaming_brand(brand):
    if not brand:
        return False
    bl = brand.lower().strip()
    for gb in GAMING_BRANDS:
        if gb in bl:
            return True
    return False

def normalize_brand(raw):
    """Normalize peripheral brand names for consistency."""
    if not raw or raw.strip() == '':
        return '(Empty/Generic)'
    b = raw.strip()
    bl = b.lower()
    
    # Known normalizations
    if 'standard' in bl and 'system' in bl:
        return 'Standard System'
    if bl in ('(standart sistem aygıtları)', '(cihazlar standart sistem)'):
        return 'Standard System'
    if bl in ('(standard system devices)', '(périphériques système standard)'):
        return 'Standard System'
    if 'steelseries' in bl or bl == 'aps':
        return 'SteelSeries'
    if 'logitech' in bl or bl == 'logi':
        return 'Logitech'
    if bl.startswith('razer'):
        return 'Razer'
    if 'corsair' in bl:
        return 'Corsair'
    if 'hyperx' in bl:
        return 'HyperX'
    if bl == 'semico':
        return 'Semico'
    if bl == 'compx':
        return 'Compx'
    if bl == 'microsoft':
        return 'Microsoft'
    if bl == 'sonix':
        return 'Sonix'
    if bl == 'instant':
        return 'Instant'
    if 'redragon' in bl:
        return 'Redragon'
    if 'bloody' in bl:
        return 'Bloody'
    if 'a4tech' in bl:
        return 'A4Tech'
    if bl == 'darmoshark':
        return 'Darmoshark'
    if bl == 'varmilo':
        return 'Varmilo'
    if 'sino wealth' in bl:
        return 'Sino Wealth'
    if bl == 'by tech':
        return 'By Tech'
    if bl == 'evision':
        return 'Evision'
    
    # Title-case the rest
    return b.title() if len(b) > 3 else b.upper()

def normalize_mobo(raw):
    """Normalize motherboard/OEM manufacturer names."""
    if not raw or raw.strip() == '':
        return None
    b = raw.strip()
    bl = b.lower()
    
    if bl in ('system manufacturer', 'to be filled by o.e.m.', 'default string', 'system product name'):
        return 'Sys Mfg/OEM'
    if 'asus' in bl:
        return 'ASUS'
    if bl == 'msi' or bl.startswith('micro-star'):
        return 'MSI'
    if 'gigabyte' in bl:
        return 'Gigabyte'
    if bl == 'monster notebook' or bl == 'monster':
        return 'Monster (TR)'
    if bl == 'casper' or 'casper' in bl:
        return 'Casper (TR)'
    if bl.startswith('lenovo'):
        return 'Lenovo'
    if bl.startswith('hp') or bl == 'hewlett-packard':
        return 'HP'
    if bl.startswith('acer'):
        return 'Acer'
    if bl.startswith('dell'):
        return 'Dell'
    if bl.startswith('asrock'):
        return 'ASRock'
    if 'game garaj' in bl:
        return 'Game Garaj (TR)'
    if bl.startswith('huawei'):
        return 'Huawei'
    if bl.startswith('samsung'):
        return 'Samsung'
    if bl.startswith('apple'):
        return 'Apple'
    
    return b.title() if len(b) > 3 else b.upper()

def extract_cpu_brand(cpu_str):
    """Detect AMD vs Intel from CPU string."""
    if not cpu_str:
        return 'Unknown'
    cl = cpu_str.lower()
    if 'amd' in cl:
        return 'AMD'
    elif 'intel' in cl:
        return 'Intel'
    return 'Unknown'

class CountryAggregator:
    def __init__(self):
        self.total_rows = 0
        self.user_ids = set()
        self.cpu_brand = Counter()  # AMD / Intel / Unknown
        self.device_type = Counter()  # keyboard / mouse / other
        self.peripheral_brand = Counter()
        self.mobo_brand = Counter()
        self.core_counts = Counter()
        self.gaming_count = 0
        self.dates = set()
    
    def add_row(self, row):
        self.total_rows += 1
        
        # Parse fields by index (CSV has duplicate header names)
        device_mfg = row[0].strip() if len(row) > 0 else ''
        cpu_str = row[1].strip() if len(row) > 1 else ''
        cores = row[2].strip() if len(row) > 2 else ''
        periph_mfg = row[3].strip() if len(row) > 3 else ''
        device_name = row[4].strip().lower() if len(row) > 4 else ''
        date = row[5].strip() if len(row) > 5 else ''
        user_id = row[6].strip() if len(row) > 6 else ''
        
        # User
        if user_id:
            self.user_ids.add(user_id)
        
        # Date
        if date:
            self.dates.add(date)
        
        # CPU brand
        cpu_brand = extract_cpu_brand(cpu_str)
        self.cpu_brand[cpu_brand] += 1
        
        # Device type
        if 'keyboard' in device_name:
            self.device_type['Keyboard'] += 1
        elif 'mouse' in device_name:
            self.device_type['Mouse'] += 1
        else:
            self.device_type['Other'] += 1
        
        # Peripheral brand (from column 3)
        brand = normalize_brand(periph_mfg)
        self.peripheral_brand[brand] += 1
        
        # Gaming check
        if is_gaming_brand(periph_mfg):
            self.gaming_count += 1
        
        # Motherboard / OEM (column 0 — device manufacturer)
        mobo = normalize_mobo(device_mfg)
        if mobo:
            self.mobo_brand[mobo] += 1
        
        # Core counts
        if cores and cores.isdigit():
            self.core_counts[f'{cores} Cores'] += 1
    
    def to_dict(self):
        total = self.total_rows or 1
        cpu_total = sum(self.cpu_brand.values()) or 1
        amd = self.cpu_brand.get('AMD', 0)
        intel = self.cpu_brand.get('Intel', 0)
        amd_intel_total = amd + intel or 1
        
        device_total = sum(self.device_type.values()) or 1
        kb = self.device_type.get('Keyboard', 0)
        mouse = self.device_type.get('Mouse', 0)
        
        return {
            'totalRows': self.total_rows,
            'uniqueSystems': len(self.user_ids),
            'dau': 0,  # Not available from CSV
            'cpuAmd': round(100 * amd / amd_intel_total, 1),
            'cpuIntel': round(100 * intel / amd_intel_total, 1),
            'gamingPenetration': round(100 * self.gaming_count / total, 1),
            'keyboardPct': round(100 * kb / device_total, 1),
            'mousePct': round(100 * mouse / device_total, 1),
            'topPeripherals': [
                {'name': name, 'count': count}
                for name, count in self.peripheral_brand.most_common(10)
            ],
            'topMobo': [
                {'name': name, 'count': count}
                for name, count in self.mobo_brand.most_common(8)
            ],
            'coreCounts': [
                {'cores': cores, 'count': count}
                for cores, count in self.core_counts.most_common(6)
            ],
            'dateRange': sorted(self.dates)[:1] + sorted(self.dates)[-1:] if self.dates else [],
            'tier': '',
        }

def main():
    print(f"Reading CSV: {CSV_PATH}", file=sys.stderr)
    
    # Per-country aggregators
    country_aggs = defaultdict(CountryAggregator)
    all_agg = CountryAggregator()
    
    row_count = 0
    skipped_countries = Counter()
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(f"Header: {header}", file=sys.stderr)
        
        for row in reader:
            if len(row) < 8:
                continue
            country = row[7].strip().upper()
            if not country:
                continue
            
            if country not in RELEASED_COUNTRIES:
                skipped_countries[country] += 1
                continue
            
            country_aggs[country].add_row(row)
            all_agg.add_row(row)
            row_count += 1
            
            if row_count % 200000 == 0:
                print(f"  Processed {row_count:,} rows...", file=sys.stderr)
    
    print(f"Total rows processed: {row_count:,}", file=sys.stderr)
    print(f"Countries included: {len(country_aggs)}", file=sys.stderr)
    if skipped_countries:
        print(f"Skipped {sum(skipped_countries.values()):,} rows from {len(skipped_countries)} non-released countries:", file=sys.stderr)
        for cc, cnt in skipped_countries.most_common(10):
            print(f"  {cc}: {cnt:,}", file=sys.stderr)
    
    # Build output
    result = {
        'all': all_agg.to_dict(),
        'countries': {},
        'country_summary': []
    }
    
    for country_code in sorted(country_aggs.keys(), key=lambda c: country_aggs[c].total_rows, reverse=True):
        agg = country_aggs[country_code]
        data = agg.to_dict()
        data['tier'] = classify_tier(country_code)
        data['countryCode'] = country_code
        result['countries'][country_code] = data
        result['country_summary'].append({
            'code': country_code,
            'tier': classify_tier(country_code),
            'rows': agg.total_rows,
            'uniqueUsers': len(agg.user_ids),
        })
    
    # Print summary to stderr
    print("\n--- Country Summary ---", file=sys.stderr)
    print(f"{'Country':<6} {'Tier':<8} {'Rows':>12} {'Unique Users':>14}", file=sys.stderr)
    print("-" * 44, file=sys.stderr)
    for cs in result['country_summary']:
        print(f"{cs['code']:<6} {cs['tier']:<8} {cs['rows']:>12,} {cs['uniqueUsers']:>14,}", file=sys.stderr)
    
    # Tier aggregation
    tier_aggs = defaultdict(CountryAggregator)
    # Re-read? No — we'll aggregate from country results
    tier_rows = defaultdict(int)
    tier_users = defaultdict(set)
    for cc, agg in country_aggs.items():
        tier = classify_tier(cc)
        tier_rows[tier] += agg.total_rows
        tier_users[tier].update(agg.user_ids)
    
    print("\n--- Tier Summary ---", file=sys.stderr)
    for tier in ['Early Release', 'Tier 3']:
        if tier_rows[tier] > 0:
            print(f"{tier}: {tier_rows[tier]:>12,} rows, {len(tier_users[tier]):>10,} unique users", file=sys.stderr)
    
    # Output JSON to stdout
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
