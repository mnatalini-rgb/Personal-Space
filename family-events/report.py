from __future__ import annotations

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


def _fmt_dt(value: str | None) -> str:
    if not value:
        return "Date TBC"
    try:
        return datetime.fromisoformat(value).strftime("%a %d %b %Y, %H:%M")
    except Exception:
        return value


def _card(event: dict) -> str:
    badge = '<span class="badge">NEW</span>' if event.get("is_new") else ""
    price = escape(event.get("cost") or "Unknown")
    age = escape(event.get("age") or "All ages")
    venue = escape(event.get("venue") or "Unknown venue")
    title = escape(event.get("title") or "Untitled event")
    link = escape(event.get("url") or "#")
    address = escape(event.get("address") or "")
    distance = escape(event.get("distance") or "")
    source = escape(event.get("source") or "")
    return f"""
    <article class=\"event-card\">
      <div class=\"event-head\">
        <h3>{title}</h3>
        {badge}
      </div>
      <p class=\"meta\"><strong>{venue}</strong></p>
      <p class=\"meta\">🗓 {_fmt_dt(event.get('start'))}</p>
      <p class=\"meta\">👶 {age} &nbsp; • &nbsp; 💷 {price}</p>
      <p class=\"meta\">📍 {address} &nbsp; • &nbsp; 🚇 {distance} from E3</p>
      <p class=\"meta source\">Source: {source}</p>
      <p><a href=\"{link}\" target=\"_blank\" rel=\"noopener\">View details</a></p>
    </article>
    """


def build_html_report(
    events: list[dict],
    static_events: list[dict],
    output_path,
    start_range: datetime,
    end_range: datetime,
    failed_sources: list[str],
) -> None:
    grouped = defaultdict(list)
    for event in sorted(events, key=lambda x: x.get("start") or ""):
        grouped[event.get("category", "Museums & Learning")].append(event)

    total_new = len([e for e in events if e.get("is_new")])

    sections = []
    for category in CATEGORY_ORDER:
        cat_events = grouped.get(category, [])
        if not cat_events:
            continue
        cards = "\n".join([_card(e) for e in cat_events])
        sections.append(
            f"""
            <section class=\"category\" style=\"--cat:{CATEGORY_COLORS.get(category, '#2563eb')}\">
              <h2>{escape(category)} <span>{len(cat_events)}</span></h2>
              <div class=\"grid\">{cards}</div>
            </section>
            """
        )

    static_cards = "\n".join([_card(e) for e in static_events])
    failed_note = (
        "<div class='warning'><strong>Some sources failed:</strong> "
        + escape(", ".join(failed_sources))
        + "</div>"
        if failed_sources
        else ""
    )

    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
  <title>Family Events This Week</title>
  <style>
    :root {{ --bg:#f8fafc; --card:#fff; --text:#0f172a; --muted:#475569; --new:#dc2626; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:var(--bg); color:var(--text); }}
    .container {{ max-width:980px; margin:0 auto; padding:16px; }}
    header {{ background:linear-gradient(120deg,#7c3aed,#06b6d4); color:#fff; padding:20px; border-radius:16px; }}
    h1 {{ margin:0 0 8px; font-size:1.6rem; }}
    .sub {{ opacity:.95; margin:4px 0; }}
    .category {{ margin-top:20px; }}
    .category h2 {{ display:flex; justify-content:space-between; align-items:center; margin:0 0 10px; padding:8px 10px; border-left:6px solid var(--cat); background:#e2e8f0; border-radius:8px; font-size:1.1rem; }}
    .grid {{ display:grid; gap:10px; grid-template-columns:1fr; }}
    .event-card {{ background:var(--card); border:1px solid #e2e8f0; border-radius:12px; padding:12px; box-shadow:0 2px 6px rgba(15,23,42,.05); }}
    .event-head {{ display:flex; justify-content:space-between; gap:8px; align-items:flex-start; }}
    .event-head h3 {{ margin:0; font-size:1rem; line-height:1.3; }}
    .meta {{ margin:6px 0; color:var(--muted); font-size:.92rem; }}
    .source {{ font-size:.8rem; }}
    a {{ color:#1d4ed8; text-decoration:none; font-weight:600; }}
    .badge {{ background:var(--new); color:#fff; font-size:.72rem; padding:3px 8px; border-radius:999px; font-weight:700; }}
    .warning {{ margin-top:14px; padding:10px; border-radius:8px; background:#fff7ed; color:#9a3412; border:1px solid #fdba74; }}
    footer {{ margin:24px 0 8px; text-align:center; color:#64748b; font-size:.85rem; }}
    @media (min-width: 760px) {{ .grid {{ grid-template-columns:repeat(2,1fr); }} }}
  </style>
</head>
<body>
  <main class=\"container\">
    <header>
      <h1>Family Events This Week</h1>
      <p class=\"sub\">{start_range.strftime('%d %b %Y')} → {end_range.strftime('%d %b %Y')}</p>
      <p class=\"sub\"><strong>{total_new} new activities found</strong> for Julian (5) & Andy (2)</p>
    </header>
    {failed_note}
    {''.join(sections)}
    <section class=\"category\" style=\"--cat:#334155\">
      <h2>Always Available <span>{len(static_events)}</span></h2>
      <div class=\"grid\">{static_cards}</div>
    </section>
    <footer>Auto-generated by GitHub Actions • Last updated: {datetime.now().strftime('%d %b %Y %H:%M')}</footer>
  </main>
</body>
</html>"""
    output_path.write_text(html, encoding="utf-8")
