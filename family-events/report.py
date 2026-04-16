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
    "Theatre & Shows": "#7c3aed",
    "Museums & Learning": "#2563eb",
    "Outdoor & Parks": "#16a34a",
    "Sports & Swimming": "#0891b2",
    "Soft Play & Indoor": "#f97316",
    "Farms & Animals": "#65a30d",
    "Seasonal": "#db2777",
}

CATEGORY_EMOJIS = {
    "Theatre & Shows": "🎭",
    "Museums & Learning": "🏛️",
    "Outdoor & Parks": "🌳",
    "Sports & Swimming": "🏊",
    "Soft Play & Indoor": "🎪",
    "Farms & Animals": "🐄",
    "Seasonal": "🎃",
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
    color = CATEGORY_COLORS.get(cat, "#2563eb")
    emoji = CATEGORY_EMOJIS.get(cat, "📌")
    
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
    <details class="event-row {age_classes}" data-cat="{escape(cat)}" data-new="{is_new}" data-date="{start_raw}">
      <summary class="row-main">
        <div class="r-cat" title="{escape(cat)}" style="background-color: {color}">{emoji}</div>
        <div class="r-title">{title}</div>
        <div class="r-venue">{venue}</div>
        <div class="r-date">{date_str}</div>
        <div class="r-age">{age}</div>
        <a href="{link}" class="r-book" target="_blank" rel="noopener" onclick="event.stopPropagation()">Book &rarr;</a>
      </summary>
      <div class="row-details">
        <p class="d-desc">{desc}</p>
        <div class="d-meta">
          <span>📍 {address}</span>
          <span>💷 {price}</span>
          <span>🚇 {distance} from E3</span>
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
    # Summary banner prep
    new_events = [e for e in events if e.get("is_new")]
    new_count = len(new_events)
    
    cat_counts = defaultdict(int)
    for e in new_events:
        cat_counts[e.get("category", "Other")] += 1
        
    summary_parts = []
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        summary_parts.append(f"{count} {cat.split('&')[0].strip().lower()}")
    summary_text = f"{new_count} new events this week: " + ", ".join(summary_parts) if new_count else "No new events this week."

    # Group ALL events by category
    grouped_all = defaultdict(list)
    for event in sorted(events, key=lambda x: x.get("start") or ""):
        grouped_all[event.get("category", "Museums & Learning")].append(event)

    all_sections = []
    for category in CATEGORY_ORDER:
        cat_events = grouped_all.get(category, [])
        if not cat_events:
            continue
        rows = "\n".join([_row(e) for e in cat_events])
        all_sections.append(f"""
            <div class="cat-group" data-cat="{escape(category)}">
                <h3>{escape(category)} <span class="count">{len(cat_events)}</span></h3>
                <div class="rows-container">{rows}</div>
            </div>
        """)

    # New events rows
    new_rows_html = "\n".join([_row(e) for e in sorted(new_events, key=lambda x: x.get("start") or "")])

    # Static events grid
    static_items = []
    for e in static_events:
        cat = e.get("category", "Museums & Learning")
        color = CATEGORY_COLORS.get(cat, "#2563eb")
        emoji = CATEGORY_EMOJIS.get(cat, "📌")
        venue = escape(e.get("venue") or e.get("title") or "Unknown")
        link = escape(e.get("url") or "#")
        static_items.append(f"""
            <a href="{link}" class="static-item" target="_blank" rel="noopener" data-cat="{escape(cat)}">
                <span class="s-icon" style="background-color: {color}">{emoji}</span>
                <span class="s-venue">{venue}</span>
            </a>
        """)
    static_grid = f"<div class=\"static-grid\">{''.join(static_items)}</div>"

    failed_note = (
        f"<div class='warning'>⚠️ <strong>Warning:</strong> Failed to fetch from: {escape(', '.join(failed_sources))}</div>"
        if failed_sources else ""
    )

    # Filter pills
    pills = []
    for cat in CATEGORY_ORDER:
        color = CATEGORY_COLORS.get(cat, "#000")
        pills.append(f'<button class="pill active" data-cat="{escape(cat)}" style="--c:{color}">{escape(cat)}</button>')

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Family Events Digest</title>
  <style>
    :root {{
      --bg: #f4f4f5; --surface: #ffffff; --text: #18181b; --muted: #71717a; 
      --border: #e4e4e7; --accent: #2563eb; --radius: 8px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg); color: var(--text); line-height: 1.5;
      -webkit-font-smoothing: antialiased; padding: 16px;
    }}
    .container {{ max-width: 1000px; margin: 0 auto; }}
    
    /* Header & Summary */
    .summary-banner {{
      background: #18181b; color: #fff; padding: 16px 20px; border-radius: var(--radius);
      margin-bottom: 20px; font-weight: 500; font-size: 1.1rem;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .warning {{
      background: #fef2f2; color: #991b1b; padding: 12px 16px; border-radius: var(--radius);
      border: 1px solid #f87171; margin-bottom: 20px; font-size: 0.95rem;
    }}
    
    /* Filters */
    .filters {{
      background: var(--surface); padding: 16px; border-radius: var(--radius);
      border: 1px solid var(--border); margin-bottom: 24px;
    }}
    .filter-group {{ margin-bottom: 16px; }}
    .filter-group:last-child {{ margin-bottom: 0; }}
    .filter-title {{ font-size: 0.85rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }}
    
    .pills {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .pill {{
      appearance: none; background: transparent; border: 1px solid var(--border);
      padding: 6px 12px; border-radius: 99px; font-size: 0.9rem; font-weight: 500;
      color: var(--muted); cursor: pointer; transition: all 0.2s;
    }}
    .pill.active {{ background: var(--c); border-color: var(--c); color: #fff; }}
    
    .age-toggles {{ display: flex; gap: 8px; background: #f4f4f5; padding: 4px; border-radius: 99px; width: fit-content; }}
    .age-btn {{
      appearance: none; border: none; background: transparent; padding: 6px 16px;
      border-radius: 99px; font-size: 0.95rem; font-weight: 600; color: var(--muted);
      cursor: pointer; transition: 0.2s;
    }}
    .age-btn.active {{ background: #fff; color: var(--text); box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    
    /* Sections */
    section {{ margin-bottom: 32px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }}
    section.transparent {{ background: transparent; border: none; overflow: visible; }}
    section > summary {{
      font-size: 1.25rem; font-weight: 700; padding: 16px; cursor: pointer;
      list-style: none; display: flex; align-items: center; gap: 8px;
      background: #fafafa; border-bottom: 1px solid var(--border); margin-bottom: 0;
    }}
    section.transparent > summary {{ background: transparent; border: none; padding: 0; margin-bottom: 16px; font-size: 1.4rem; }}
    
    section > summary::-webkit-details-marker {{ display: none; }}
    section > summary::before {{ content: '▸'; font-size: 1.2rem; transition: transform 0.2s; }}
    section[open] > summary::before {{ transform: rotate(90deg); }}
    
    .section-content {{ padding: 16px; }}
    section.transparent .section-content {{ padding: 0; }}
    
    h3.bucket-title {{ font-size: 1.1rem; color: var(--muted); margin: 24px 0 12px; border-bottom: 1px solid var(--border); padding-bottom: 4px; }}
    h3.bucket-title:first-child {{ margin-top: 0; }}
    
    .cat-group h3 {{ font-size: 1.1rem; margin: 20px 0 12px; display: flex; align-items: center; gap: 8px; }}
    .cat-group:first-child h3 {{ margin-top: 0; }}
    .count {{ background: var(--border); font-size: 0.8rem; padding: 2px 8px; border-radius: 99px; color: var(--muted); font-weight: 600; }}
    
    /* Rows */
    .rows-container {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }}
    .event-row {{ border-bottom: 1px solid var(--border); transition: background 0.15s; }}
    .event-row:last-child {{ border-bottom: none; }}
    .event-row:hover {{ background: #fafafa; }}
    
    .row-main {{
      display: grid; grid-template-columns: auto 1fr; gap: 8px 12px; padding: 12px 16px;
      cursor: pointer; list-style: none; align-items: center;
    }}
    .row-main::-webkit-details-marker {{ display: none; }}
    
    .r-cat {{
      width: 28px; height: 28px; border-radius: 6px; display: flex;
      align-items: center; justify-content: center; font-size: 0.9rem; grid-row: span 2;
    }}
    .r-title {{ font-weight: 600; font-size: 1.05rem; grid-column: 2; line-height: 1.2; }}
    .r-venue {{ color: var(--muted); font-size: 0.9rem; grid-column: 2; }}
    .r-date {{ font-size: 0.9rem; color: #059669; font-weight: 500; grid-column: 2; }}
    .r-age {{ font-size: 0.85rem; color: var(--muted); background: var(--bg); padding: 2px 8px; border-radius: 4px; justify-self: start; grid-column: 2; }}
    .r-book {{
      background: var(--text); color: #fff; text-decoration: none; padding: 6px 12px;
      border-radius: 6px; font-size: 0.85rem; font-weight: 600; text-align: center;
      grid-column: 2; justify-self: start; transition: opacity 0.2s;
    }}
    .r-book:hover {{ opacity: 0.8; }}
    
    /* Desktop Row Layout */
    @media (min-width: 768px) {{
      .row-main {{
        grid-template-columns: 28px minmax(200px, 1.5fr) minmax(150px, 1fr) 140px 80px 80px;
        gap: 16px;
      }}
      .r-cat {{ grid-row: 1; }}
      .r-title, .r-venue, .r-date, .r-age, .r-book {{ grid-column: auto; grid-row: 1; align-self: center; }}
      .r-venue {{ color: var(--text); font-size: 0.95rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
      .r-age {{ justify-self: center; }}
      .r-book {{ justify-self: end; }}
    }}
    
    .row-details {{ padding: 16px; background: #fafafa; border-top: 1px dashed var(--border); font-size: 0.95rem; }}
    .d-desc {{ margin-bottom: 12px; color: #3f3f46; max-width: 800px; }}
    .d-meta {{ display: flex; flex-wrap: wrap; gap: 16px; font-size: 0.85rem; color: var(--muted); }}
    .d-source {{ margin-left: auto; font-style: italic; }}
    
    /* Static Grid */
    .static-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }}
    .static-item {{
      display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--surface);
      border: 1px solid var(--border); border-radius: var(--radius); text-decoration: none;
      color: var(--text); font-weight: 500; font-size: 0.95rem; transition: border-color 0.2s;
    }}
    .static-item:hover {{ border-color: var(--muted); }}
    .s-icon {{ width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; color: #fff; }}
    
    footer {{ text-align: center; color: var(--muted); font-size: 0.85rem; margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--border); }}
  </style>
</head>
<body>
  <main class="container">
    <div class="summary-banner">
      ✨ {summary_text}
    </div>
    
    {failed_note}
    
    <div class="filters">
      <div class="filter-group">
        <div class="filter-title">Filter by Category</div>
        <div class="pills" id="cat-pills">
          {''.join(pills)}
        </div>
      </div>
      <div class="filter-group">
        <div class="filter-title">Filter by Age</div>
        <div class="age-toggles" id="age-toggles">
          <button class="age-btn active" data-age="all">Both Kids</button>
          <button class="age-btn" data-age="5">Julian (5)</button>
          <button class="age-btn" data-age="2">Andy (2)</button>
        </div>
      </div>
    </div>
    
    <details class="transparent" id="sec-new" open>
      <summary>🔥 New This Week</summary>
      <div class="section-content" id="new-buckets">
        <div id="b-weekend">
          <h3 class="bucket-title">This Weekend</h3>
          <div class="rows-container"></div>
        </div>
        <div id="b-next">
          <h3 class="bucket-title">Next Week</h3>
          <div class="rows-container"></div>
        </div>
        <div id="b-later">
          <h3 class="bucket-title">Later / Undated</h3>
          <div class="rows-container"></div>
        </div>
      </div>
      <!-- Hidden container to hold rows before JS sorts them -->
      <div id="new-raw" style="display:none;">{new_rows_html}</div>
    </details>
    
    <details class="transparent" id="sec-all">
      <summary>📚 All Events ({len(events)})</summary>
      <div class="section-content" id="all-events">
        {''.join(all_sections)}
      </div>
    </details>
    
    <details class="transparent" id="sec-static">
      <summary>📌 Always Available ({len(static_events)})</summary>
      <div class="section-content">
        {static_grid}
      </div>
    </details>
    
    <footer>
      Auto-generated • Last updated: {datetime.now().strftime('%d %b %Y %H:%M')}
    </footer>
  </main>

  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      // 1. Group NEW events by time
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
      if(!rawRows.length) document.getElementById('new-buckets').innerHTML = '<p style="color:var(--muted)">No new events this week.</p>';
      
      // 2. Filtering Logic
      const pills = document.querySelectorAll('.pill');
      const ageBtns = document.querySelectorAll('.age-btn');
      
      let activeCats = new Set(Array.from(pills).map(p => p.getAttribute('data-cat')));
      let activeAge = 'all';
      
      function applyFilters() {{
        const allRows = document.querySelectorAll('.event-row');
        allRows.forEach(row => {{
          const cat = row.getAttribute('data-cat');
          const isCatMatch = activeCats.has(cat);
          
          let isAgeMatch = true;
          if (activeAge !== 'all') {{
            isAgeMatch = row.classList.contains('age-' + activeAge);
          }}
          
          row.style.display = (isCatMatch && isAgeMatch) ? '' : 'none';
        }});
        
        // Hide empty category groups in All Events
        document.querySelectorAll('.cat-group').forEach(group => {{
          const cat = group.getAttribute('data-cat');
          const hasVisibleRows = Array.from(group.querySelectorAll('.event-row')).some(r => r.style.display !== 'none');
          group.style.display = (!activeCats.has(cat) || !hasVisibleRows) ? 'none' : '';
        }});
        
        // Filter static items by category
        document.querySelectorAll('.static-item').forEach(item => {{
          const cat = item.getAttribute('data-cat');
          item.style.display = activeCats.has(cat) ? '' : 'none';
        }});
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
    }});
  </script>
</body>
</html>"""
    output_path.write_text(html, encoding="utf-8")
