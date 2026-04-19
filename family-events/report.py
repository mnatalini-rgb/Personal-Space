from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime
from html import escape

CATEGORY_ORDER = [
    "Theatre & Shows",
    "Museums & Learning",
    "Outdoor & Parks",
    "Sports & Swimming",
    "Soft Play & Indoor",
    "Farms & Animals",
    "Seasonal",
]

CATEGORY_COLORS = {
    "Theatre & Shows": "139, 92, 246",
    "Museums & Learning": "59, 130, 246",
    "Outdoor & Parks": "16, 185, 129",
    "Sports & Swimming": "14, 165, 233",
    "Soft Play & Indoor": "245, 158, 11",
    "Farms & Animals": "132, 204, 22",
    "Seasonal": "236, 72, 153",
}

CATEGORY_SVGS = {
    "Theatre & Shows": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 0 1 10 10c0 5.5-4.5 10-10 10S2 17.5 2 12 7.5 2 12 2z"/><path d="M8 10h.01"/><path d="M16 10h.01"/><path d="M10 15c.67.67 1.33 1 2 1s1.33-.33 2-1"/></svg>',
    "Museums & Learning": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 22h16"/><path d="M4 18h16"/><path d="M6 18v-8"/><path d="M10 18v-8"/><path d="M14 18v-8"/><path d="M18 18v-8"/><path d="M12 2L2 10h20L12 2z"/></svg>',
    "Outdoor & Parks": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22v-6"/><path d="M12 16a6 6 0 0 1-6-6c0-3.3 2.7-6 6-6s6 2.7 6 6a6 6 0 0 1-6 6z"/></svg>',
    "Sports & Swimming": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12c2.5 0 5 2 7.5 2s5-2 7.5-2 5 2 7.5 2"/><path d="M2 17c2.5 0 5 2 7.5 2s5-2 7.5-2 5 2 7.5 2"/><path d="M12 7c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3z"/></svg>',
    "Soft Play & Indoor": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="8" y="13" width="8" height="8" rx="2"/></svg>',
    "Farms & Animals": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V10z"/><path d="M3 10V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4"/><path d="M8 2v4"/><path d="M16 2v4"/></svg>',
    "Seasonal": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M2 12h20"/><path d="m4.9 4.9 14.2 14.2"/><path d="m19.1 4.9-14.2 14.2"/></svg>',
}

def _fmt_dt(value: str | None) -> str:
    if not value:
        return "Date TBC"
    try:
        return datetime.fromisoformat(value).strftime("%a %d %b, %H:%M")
    except Exception:
        return value

def _get_age_tags(age_str: str | None) -> str:
    if not age_str:
        return "age-2 age-5"
    s = age_str.lower()
    if "all" in s or "family" in s:
        return "age-2 age-5"
    
    tags = set()
    nums = [int(n) for n in re.findall(r'\d+', s)]
    
    if not nums:
        if "toddler" in s or "baby" in s or "babies" in s:
            tags.add("age-2")
    else:
        if "+" in s:
            if nums[0] <= 2: tags.add("age-2")
            if nums[0] <= 5: tags.add("age-5")
        elif "-" in s or "to" in s:
            if len(nums) >= 2:
                if nums[0] <= 2 <= nums[1]: tags.add("age-2")
                if nums[0] <= 5 <= nums[1]: tags.add("age-5")
        elif "under" in s:
            if nums[0] > 2: tags.add("age-2")
            if nums[0] > 5: tags.add("age-5")
        else:
            if 2 in nums: tags.add("age-2")
            if 5 in nums: tags.add("age-5")
            
    if not tags:
        return "age-2 age-5"
    return " ".join(tags)

def _row(event: dict) -> str:
    cat = event.get("category", "Museums & Learning")
    color = CATEGORY_COLORS.get(cat, "59, 130, 246")
    svg = CATEGORY_SVGS.get(cat, CATEGORY_SVGS["Museums & Learning"])
    
    title = escape(event.get("title") or "Untitled")
    venue = escape(event.get("venue") or "Unknown")
    date_str = _fmt_dt(event.get("start"))
    age = escape(event.get("age") or "All ages")
    link = escape(event.get("url") or "#")
    price = escape(event.get("cost") or "Unknown")
    address = escape(event.get("address") or "")
    distance = escape(event.get("distance") or "")
    source = escape(event.get("source") or "")
    desc = escape(event.get("description") or "No description provided.")
    
    is_new = str(event.get("is_new", False)).lower()
    start_raw = event.get("start") or ""
    age_classes = _get_age_tags(event.get("age"))
    
    return f"""
    <details class="event-row {age_classes}" data-cat="{escape(cat)}" data-new="{is_new}" data-date="{start_raw}" style="--c: {color};">
      <summary class="row-main">
        <div class="r-cat-circle" style="background: rgba(var(--c), 0.1); color: rgb(var(--c));" title="{escape(cat)}">
          {svg}
        </div>
        <div class="r-content">
          <div class="r-title">{title}</div>
          <div class="r-venue">{venue}</div>
        </div>
        <div class="r-meta">
          <div class="r-date">{date_str}</div>
          <div class="r-age">{age}</div>
        </div>
        <a href="{link}" class="r-book" target="_blank" rel="noopener" onclick="event.stopPropagation()">Book</a>
      </summary>
      <div class="row-details">
        <p class="d-desc">{desc}</p>
        <div class="d-meta">
          <span class="d-pill">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
            {address}
          </span>
          <span class="d-pill">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
            {price}
          </span>
          <span class="d-pill">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
            {distance}
          </span>
          <span class="d-source">Source: {source}</span>
        </div>
      </div>
    </details>
    """

def _sub_row(event: dict) -> str:
    cat = event.get("category", "Museums & Learning")
    color = CATEGORY_COLORS.get(cat, "59, 130, 246")
    
    title = escape(event.get("title") or "Untitled")
    date_str = _fmt_dt(event.get("start"))
    age = escape(event.get("age") or "All ages")
    link = escape(event.get("url") or "#")
    price = escape(event.get("cost") or "Unknown")
    address = escape(event.get("address") or "")
    distance = escape(event.get("distance") or "")
    source = escape(event.get("source") or "")
    desc = escape(event.get("description") or "No description provided.")
    
    is_new = str(event.get("is_new", False)).lower()
    start_raw = event.get("start") or ""
    age_classes = _get_age_tags(event.get("age"))
    
    return f"""
    <details class="event-row {age_classes}" data-cat="{escape(cat)}" data-new="{is_new}" data-date="{start_raw}" style="--c: {color};">
      <summary class="sub-row-main">
        <div class="r-content">
          <div class="r-title">{title}</div>
        </div>
        <div class="r-meta">
          <div class="r-date">{date_str}</div>
          <div class="r-age">{age}</div>
        </div>
        <a href="{link}" class="r-book" target="_blank" rel="noopener" onclick="event.stopPropagation()">Book</a>
      </summary>
      <div class="row-details">
        <p class="d-desc">{desc}</p>
        <div class="d-meta">
          <span class="d-pill">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
            {address}
          </span>
          <span class="d-pill">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
            {price}
          </span>
          <span class="d-pill">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
            {distance}
          </span>
          <span class="d-source">Source: {source}</span>
        </div>
      </div>
    </details>
    """

def build_html_report(
    events: list[dict],
    static_events: list[dict],
    output_path,
    start_range: datetime,
    end_range: datetime,
    failed_sources: list[str],
) -> None:
    now = datetime.now()
    events = [e for e in events if not e.get("start") or datetime.fromisoformat(e["start"]) >= now]
    new_events = [e for e in events if e.get("is_new")]
    new_count = len(new_events)
    
    cat_counts = defaultdict(int)
    for e in new_events:
        cat_counts[e.get("category", "Other")] += 1
        
    summary_parts = []
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        summary_parts.append(f"{count} {cat.split('&')[0].strip().lower()}")
    summary_text = f"{new_count} new events this week: " + ", ".join(summary_parts) if new_count else "No new events this week."

    grouped_all = defaultdict(list)
    for event in sorted(events, key=lambda x: x.get("start") or ""):
        grouped_all[event.get("category", "Museums & Learning")].append(event)

    all_sections = []
    for category in CATEGORY_ORDER:
        cat_events = grouped_all.get(category, [])
        if not cat_events:
            continue
            
        events_by_venue = defaultdict(list)
        for e in cat_events:
            v = e.get("venue") or "Unknown"
            events_by_venue[v].append(e)
            
        color = CATEGORY_COLORS.get(category, "59, 130, 246")
        svg = CATEGORY_SVGS.get(category, CATEGORY_SVGS["Museums & Learning"])
        
        venue_html_parts = []
        for venue_name in sorted(events_by_venue.keys()):
            v_events = events_by_venue[venue_name]
            sub_rows_html = "\n".join([_sub_row(e) for e in v_events])
            venue_html_parts.append(f"""
                <div class="venue-group" data-cat="{escape(category)}" style="--c: {color};">
                    <div class="venue-header">
                        <div class="v-cat-circle">{svg}</div>
                        <div class="v-name">{escape(venue_name)}</div>
                    </div>
                    <div class="venue-events">
                        {sub_rows_html}
                    </div>
                </div>
            """)
            
        rows_container = "\n".join(venue_html_parts)
        
        all_sections.append(f"""
            <div class="cat-group" data-cat="{escape(category)}">
                <h3 class="section-header">{escape(category).upper()} &middot; <span class="count">{len(cat_events)}</span></h3>
                <div class="rows-container">{rows_container}</div>
            </div>
        """)

    new_rows_html = "\n".join([_row(e) for e in sorted(new_events, key=lambda x: x.get("start") or "")])

    static_items = []
    for e in static_events:
        cat = e.get("category", "Museums & Learning")
        color = CATEGORY_COLORS.get(cat, "59, 130, 246")
        svg = CATEGORY_SVGS.get(cat, CATEGORY_SVGS["Museums & Learning"])
        venue = escape(e.get("venue") or e.get("title") or "Unknown")
        link = escape(e.get("url") or "#")
        static_items.append(f"""
            <a href="{link}" class="static-item" target="_blank" rel="noopener" data-cat="{escape(cat)}" style="--c:{color};">
                <div class="s-icon" style="background: rgba(var(--c), 0.1); color: rgb(var(--c));">{svg}</div>
                <div class="s-info">
                    <span class="s-venue">{venue}</span>
                    <span class="s-cat-pill" style="color: rgb(var(--c)); border-color: rgba(var(--c), 0.2)">{escape(cat)}</span>
                </div>
            </a>
        """)
    static_grid = f"<div class=\"static-grid\">{''.join(static_items)}</div>"

    failed_note = (
        f"<div class='warning'><svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z'></path><line x1='12' y1='9' x2='12' y2='13'></line><line x1='12' y1='17' x2='12.01' y2='17'></line></svg> Failed to fetch from: {escape(', '.join(failed_sources))}</div>"
        if failed_sources else ""
    )

    pills = []
    for cat in CATEGORY_ORDER:
        color = CATEGORY_COLORS.get(cat, "0, 0, 0")
        svg = CATEGORY_SVGS.get(cat, "")
        short_name = escape(cat.split(" & ")[0])
        pills.append(f'<button class="pill active" data-cat="{escape(cat)}" style="--c:{color}">{svg}{short_name}</button>')

    month_pills = ['<button class="month-btn active" data-month="all">All</button>']
    seen_months = []
    cur = start_range.replace(day=1)
    while cur <= end_range:
        label = cur.strftime("%b %Y")
        val = cur.strftime("%Y-%m")
        if val not in seen_months:
            seen_months.append(val)
            month_pills.append(f'<button class="month-btn" data-month="{val}">{label}</button>')
        if cur.month == 12:
            cur = cur.replace(year=cur.year + 1, month=1)
        else:
            cur = cur.replace(month=cur.month + 1)

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Family Events Digest</title>
  <style>
    :root {{
      --bg: #f5f5f5; 
      --surface: #ffffff; 
      --text: #171717; 
      --muted: #737373; 
      --border: #e5e5e5; 
      --radius: 12px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg); color: var(--text); line-height: 1.5;
      -webkit-font-smoothing: antialiased; padding: 24px 16px;
    }}
    .container {{ max-width: 900px; margin: 0 auto; }}
    
    /* Header & Summary */
    .summary-banner {{
      background: var(--surface); color: var(--text); padding: 16px 20px; border-radius: var(--radius);
      margin-bottom: 24px; font-weight: 500; font-size: 1rem;
      border: 1px solid var(--border);
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
      display: flex; align-items: center; gap: 12px;
    }}
    .summary-banner svg {{ color: var(--muted); }}
    
    .warning {{
      background: #fff1f2; color: #be123c; padding: 12px 16px; border-radius: var(--radius);
      border: 1px solid #fda4af; margin-bottom: 24px; font-size: 0.95rem;
      display: flex; align-items: center; gap: 8px;
    }}
    
    /* Filters */
    .filters {{
      background: var(--surface); padding: 20px; border-radius: var(--radius);
      border: 1px solid var(--border); margin-bottom: 32px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }}
    .filter-group {{ margin-bottom: 20px; }}
    .filter-group:last-child {{ margin-bottom: 0; }}
    .filter-title {{ 
      font-size: 0.75rem; font-weight: 600; color: var(--muted); 
      text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; 
    }}
    
    .cat-toggles {{ display: flex; flex-wrap: wrap; gap: 4px; background: #f5f5f5; padding: 4px; border-radius: 20px; width: fit-content; border: 1px solid var(--border); }}
    .pill {{
      display: flex; align-items: center; gap: 6px; appearance: none; border: none; background: transparent; padding: 6px 14px;
      border-radius: 99px; font-size: 0.85rem; font-weight: 600; color: var(--muted);
      cursor: pointer; transition: 0.2s;
    }}
    .pill svg {{ width: 14px; height: 14px; color: var(--muted); transition: 0.2s; display: block; }}
    .pill.active {{ background: #fff; color: rgb(var(--c)); box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .pill.active svg {{ color: rgb(var(--c)); }}
    
    .age-toggles {{ display: flex; gap: 4px; background: #f5f5f5; padding: 4px; border-radius: 99px; width: fit-content; border: 1px solid var(--border); }}
    .age-btn, .month-btn {{
      appearance: none; border: none; background: transparent; padding: 6px 16px;
      border-radius: 99px; font-size: 0.85rem; font-weight: 600; color: var(--muted);
      cursor: pointer; transition: 0.2s;
    }}
    .age-btn.active, .month-btn.active {{ background: #fff; color: var(--text); box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    
    /* Sections */
    section {{ margin-bottom: 40px; }}
    details.transparent > summary.main-summary {{ 
      font-size: 0.8rem; font-weight: 600; padding: 0; margin-bottom: 16px; 
      color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em;
      list-style: none; display: flex; align-items: center; gap: 8px; cursor: pointer;
    }}
    details.transparent > summary.main-summary::-webkit-details-marker {{ display: none; }}
    details.transparent > summary.main-summary::before {{ content: '▸'; transition: transform 0.2s; font-size: 1rem; }}
    details[open].transparent > summary.main-summary::before {{ transform: rotate(90deg); }}
    
    .section-header {{ 
      font-size: 0.75rem; color: var(--muted); margin: 32px 0 16px; 
      text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;
    }}
    .cat-group:first-child .section-header {{ margin-top: 0; }}
    
    /* Rows */
    .rows-container {{ display: flex; flex-direction: column; gap: 12px; }}
    .event-row {{ 
      background: linear-gradient(135deg, rgba(var(--c), 0.03) 0%, #ffffff 100%);
      border: 1px solid var(--border); border-radius: var(--radius); 
      overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,0.02);
      transition: box-shadow 0.2s, transform 0.2s;
    }}
    .event-row:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.05); transform: translateY(-1px); }}
    
    .row-main {{
      display: grid; grid-template-columns: auto 1fr; gap: 12px 16px; padding: 16px;
      cursor: pointer; list-style: none; align-items: center;
    }}
    .row-main::-webkit-details-marker {{ display: none; }}
    
    .r-cat-circle {{
      width: 44px; height: 44px; border-radius: 50%; display: flex;
      align-items: center; justify-content: center; grid-row: span 2;
    }}
    .r-content {{ grid-column: 2; display: flex; flex-direction: column; gap: 4px; }}
    .r-title {{ font-weight: 600; font-size: 1rem; line-height: 1.2; color: var(--text); }}
    .r-venue {{ color: var(--muted); font-size: 0.85rem; }}
    
    .r-meta {{ grid-column: 2; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
    .r-date {{ font-size: 0.8rem; color: var(--muted); display: flex; align-items: center; gap: 4px; }}
    .r-date::before {{ content: ''; display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: rgb(var(--c)); }}
    .r-age {{ font-size: 0.75rem; font-weight: 500; color: var(--muted); border: 1px solid var(--border); padding: 2px 8px; border-radius: 99px; }}
    
    .r-book {{
      background: var(--surface); color: var(--text); text-decoration: none; padding: 6px 12px;
      border-radius: 6px; font-size: 0.8rem; font-weight: 600; text-align: center;
      grid-column: 2; border: 1px solid var(--border); transition: all 0.2s; width: fit-content;
    }}
    .r-book:hover {{ background: #fafafa; border-color: #d4d4d8; }}
    
    /* Venue Grouping */
    .venue-group {{
      margin-bottom: 16px;
      border-left: 2px solid rgba(var(--c), 0.3);
      border-radius: 4px;
    }}
    .venue-group:not(:has(.event-row:not([style*="display: none"]))) {{
      display: none;
    }}
    .venue-header {{
      display: flex; align-items: center; gap: 16px;
      padding: 8px 16px 8px 12px;
      font-weight: 600; color: var(--text);
    }}
    .v-cat-circle {{
      width: 44px; height: 44px; border-radius: 50%; display: flex;
      align-items: center; justify-content: center; flex-shrink: 0;
      background: rgba(var(--c), 0.1); color: rgb(var(--c));
    }}
    .v-name {{ font-size: 1.05rem; }}
    .venue-events {{
      padding-left: 60px;
      display: flex; flex-direction: column; gap: 8px;
      padding-bottom: 8px;
    }}
    
    .sub-row-main {{
      display: grid; grid-template-columns: 1fr; gap: 12px 16px; padding: 12px 16px;
      cursor: pointer; list-style: none; align-items: center;
    }}
    .sub-row-main::-webkit-details-marker {{ display: none; }}
    .sub-row-main .r-content, .sub-row-main .r-meta, .sub-row-main .r-book {{ grid-column: 1; }}
    
    @media (min-width: 768px) {{
      .sub-row-main {{
        grid-template-columns: minmax(200px, 1fr) minmax(120px, auto) 80px;
        gap: 20px;
      }}
      .sub-row-main .r-content, .sub-row-main .r-meta, .sub-row-main .r-book {{ grid-column: auto; }}
      
      .row-main {{
        grid-template-columns: 44px minmax(200px, 1fr) minmax(120px, auto) 80px;
        gap: 20px;
      }}
      .r-cat-circle {{ grid-row: 1; }}
      .r-content, .r-meta, .r-book {{ grid-column: auto; grid-row: 1; }}
      .r-meta {{ flex-direction: column; align-items: flex-start; gap: 4px; }}
      .r-book {{ justify-self: end; }}
    }}
    
    .row-details {{ padding: 16px 16px 20px; background: rgba(0,0,0,0.01); border-top: 1px solid var(--border); font-size: 0.9rem; }}
    .d-desc {{ margin-bottom: 16px; color: #52525b; max-width: 800px; line-height: 1.6; }}
    .d-meta {{ display: flex; flex-wrap: wrap; gap: 12px; font-size: 0.8rem; color: var(--muted); align-items: center; }}
    .d-pill {{ display: flex; align-items: center; gap: 6px; background: #fff; border: 1px solid var(--border); padding: 4px 10px; border-radius: 99px; }}
    .d-pill svg {{ color: var(--muted); }}
    .d-source {{ margin-left: auto; font-style: italic; opacity: 0.7; }}
    
    /* Static Grid */
    .static-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }}
    .static-item {{
      display: flex; align-items: center; gap: 16px; padding: 16px; background: var(--surface);
      border: 1px solid var(--border); border-radius: var(--radius); text-decoration: none;
      color: var(--text); transition: transform 0.2s, box-shadow 0.2s;
      box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }}
    .static-item:hover {{ transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-color: #d4d4d8; }}
    .s-icon {{ width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
    .s-info {{ display: flex; flex-direction: column; gap: 4px; overflow: hidden; }}
    .s-venue {{ font-weight: 500; font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .s-cat-pill {{ font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; border: 1px solid; padding: 2px 6px; border-radius: 4px; width: fit-content; }}
    
    footer {{ text-align: center; color: var(--muted); font-size: 0.8rem; margin-top: 64px; padding-top: 32px; border-top: 1px solid var(--border); }}
  </style>
</head>
<body>
  <main class="container">
    <div class="summary-banner">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
      {summary_text}
    </div>
    
    {failed_note}
    
    <div class="filters">
      <div class="filter-group">
        <div class="filter-title">Categories</div>
        <div class="cat-toggles" id="cat-toggles">
          {''.join(pills)}
        </div>
      </div>
      <div class="filter-group">
        <div class="filter-title">Month</div>
        <div class="age-toggles" id="month-toggles">
          {''.join(month_pills)}
        </div>
      </div>
      <div class="filter-group">
        <div class="filter-title">Ages</div>
        <div class="age-toggles" id="age-toggles">
          <button class="age-btn active" data-age="all">Both Kids</button>
          <button class="age-btn" data-age="5">Julian (5)</button>
          <button class="age-btn" data-age="2">Andy (2)</button>
        </div>
      </div>
    </div>
    
    <details class="transparent" id="sec-new" open>
      <summary class="main-summary">NEW THIS WEEK &middot; <span class="count">{new_count}</span></summary>
      <div class="section-content" id="new-buckets">
        <div id="b-weekend">
          <div class="section-header">THIS WEEKEND</div>
          <div class="rows-container"></div>
        </div>
        <div id="b-next">
          <div class="section-header">NEXT WEEK</div>
          <div class="rows-container"></div>
        </div>
        <div id="b-later">
          <div class="section-header">LATER / UNDATED</div>
          <div class="rows-container"></div>
        </div>
      </div>
      <!-- Hidden container to hold rows before JS sorts them -->
      <div id="new-raw" style="display:none;">{new_rows_html}</div>
    </details>
    
    <details class="transparent" id="sec-all">
      <summary class="main-summary">ALL EVENTS &middot; <span class="count">{len(events)}</span></summary>
      <div class="section-content" id="all-events">
        {''.join(all_sections)}
      </div>
    </details>
    
    <details class="transparent" id="sec-static">
      <summary class="main-summary">ALWAYS AVAILABLE &middot; <span class="count">{len(static_events)}</span></summary>
      <div class="section-content">
        {static_grid}
      </div>
    </details>
    
    <footer>
      Auto-generated &middot; Last updated: {datetime.now().strftime('%d %b %Y %H:%M')}
    </footer>
  </main>

  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      const now = new Date();
      const saturday = new Date(now);
      saturday.setDate(now.getDate() + (6 - now.getDay()) % 7);
      saturday.setHours(0,0,0,0);
      
      const sunday = new Date(saturday);
      sunday.setDate(saturday.getDate() + 1);
      sunday.setHours(23,59,59,999);
      
      const nextWeekEnd = new Date(sunday);
      nextWeekEnd.setDate(sunday.getDate() + 7);
      
      const rawRows = document.querySelectorAll('#new-raw .event-row');
      const bWeekend = document.querySelector('#b-weekend .rows-container');
      const bNext = document.querySelector('#b-next .rows-container');
      const bLater = document.querySelector('#b-later .rows-container');
      
      rawRows.forEach(row => {{
        const dStr = row.getAttribute('data-date');
        if (!dStr || dStr === 'None') {{
          bLater.appendChild(row);
          return;
        }}
        const d = new Date(dStr);
        if (d >= saturday && d <= sunday) {{
          bWeekend.appendChild(row);
        }} else if (d > sunday && d <= nextWeekEnd) {{
          bNext.appendChild(row);
        }} else {{
          bLater.appendChild(row);
        }}
      }});
      
      if(!bWeekend.children.length) document.getElementById('b-weekend').style.display = 'none';
      if(!bNext.children.length) document.getElementById('b-next').style.display = 'none';
      if(!bLater.children.length) document.getElementById('b-later').style.display = 'none';
      if(!rawRows.length) document.getElementById('new-buckets').innerHTML = '<p style="color:var(--muted); font-size:0.9rem;">No new events this week.</p>';
      
      const pills = document.querySelectorAll('.pill');
      const ageBtns = document.querySelectorAll('.age-btn');
      
      let activeCats = new Set(Array.from(pills).map(p => p.getAttribute('data-cat')));
      let activeAge = 'all';
      let activeMonth = 'all';
      
      const monthBtns = document.querySelectorAll('.month-btn');

      function countVisible(selector) {{
        return Array.from(document.querySelectorAll(selector)).filter(el => el.style.display !== 'none').length;
      }}

      function updateVisibilityAndCounts() {{
        document.querySelectorAll('.venue-group').forEach(group => {{
          const visibleRows = Array.from(group.querySelectorAll('.event-row')).filter(row => row.style.display !== 'none').length;
          group.style.display = visibleRows ? '' : 'none';
        }});

        document.querySelectorAll('.cat-group').forEach(group => {{
          const visibleRows = Array.from(group.querySelectorAll('.event-row')).filter(row => row.style.display !== 'none').length;
          const countEl = group.querySelector('.section-header .count');
          if (countEl) countEl.textContent = String(visibleRows);
          group.style.display = visibleRows ? '' : 'none';
        }});

        const weekendBucket = document.getElementById('b-weekend');
        const nextBucket = document.getElementById('b-next');
        const laterBucket = document.getElementById('b-later');

        [weekendBucket, nextBucket, laterBucket].forEach(bucket => {{
          if (!bucket) return;
          const visibleRows = Array.from(bucket.querySelectorAll('.event-row')).filter(row => row.style.display !== 'none').length;
          bucket.style.display = visibleRows ? '' : 'none';
        }});

        const newCountEl = document.querySelector('#sec-new > summary .count');
        const allCountEl = document.querySelector('#sec-all > summary .count');
        const staticCountEl = document.querySelector('#sec-static > summary .count');

        if (newCountEl) newCountEl.textContent = String(countVisible('#new-buckets .event-row'));
        if (allCountEl) allCountEl.textContent = String(countVisible('#all-events .event-row'));
        if (staticCountEl) staticCountEl.textContent = String(countVisible('.static-item'));
      }}
       
      function applyFilters() {{
        const allRows = document.querySelectorAll('.event-row');
        allRows.forEach(row => {{
          const cat = row.getAttribute('data-cat');
          const isPast = row.dataset.past === 'true';
          const isCatMatch = activeCats.has(cat);
          
          let isAgeMatch = true;
          if (activeAge !== 'all') {{
            isAgeMatch = row.classList.contains('age-' + activeAge);
          }}
          
          let isMonthMatch = true;
          if (activeMonth !== 'all') {{
            const dStr = row.getAttribute('data-date');
            if (dStr && dStr !== 'None') {{
              isMonthMatch = dStr.substring(0, 7) === activeMonth;
            }} else {{
              isMonthMatch = false;
            }}
          }}
          
          row.style.display = (!isPast && isCatMatch && isAgeMatch && isMonthMatch) ? '' : 'none';
        }});
        
        document.querySelectorAll('.static-item').forEach(item => {{
          const cat = item.getAttribute('data-cat');
          item.style.display = activeCats.has(cat) ? '' : 'none';
        }});

        updateVisibilityAndCounts();
      }}
      
      pills.forEach(pill => {{
        pill.addEventListener('click', () => {{
          pill.classList.toggle('active');
          const cat = pill.getAttribute('data-cat');
          if (pill.classList.contains('active')) {{
            activeCats.add(cat);
          }} else {{
            activeCats.delete(cat);
          }}
          applyFilters();
        }});
      }});
      
      ageBtns.forEach(btn => {{
        btn.addEventListener('click', () => {{
          ageBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          activeAge = btn.getAttribute('data-age');
          applyFilters();
        }});
      }});
      
      monthBtns.forEach(btn => {{
        btn.addEventListener('click', () => {{
          monthBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          activeMonth = btn.getAttribute('data-month');
          applyFilters();
        }});
      }});

      // Hide past events
      const nowTs = Date.now();
      document.querySelectorAll('.event-row').forEach(row => {{
        const dStr = row.getAttribute('data-date');
        if (dStr && dStr !== 'None') {{
          const d = new Date(dStr);
          if (!isNaN(d) && d.getTime() < nowTs) {{
            row.dataset.past = 'true';
            row.style.display = 'none';
          }}
        }}
      }});

      applyFilters();
    }});
  </script>
</body>
</html>"""
    output_path.write_text(html, encoding="utf-8")
