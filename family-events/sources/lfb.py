from __future__ import annotations

import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup  # type: ignore[reportMissingImports]

WINDOW_DAYS = 120
URL = "https://www.london-fire.gov.uk/community/events-open-days/"


def _parse_date(text: str) -> datetime | None:
    """Parse LFB date strings like '4 April 2026' or '18th April 2026'."""
    cleaned = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", text.strip())
    for fmt in ("%d %B %Y", "%d %b %Y"):
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
    return None


def fetch_lfb_events() -> tuple[list[dict], list[str]]:
    """Scrape upcoming events from the LFB events page."""
    errors: list[str] = []
    events: list[dict] = []
    now = datetime.now()
    end = now + timedelta(days=WINDOW_DAYS)

    try:
        resp = requests.get(URL, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (compatible; FamilyEventsBot/1.0)"
        })
        resp.raise_for_status()
    except Exception as exc:
        return [], [f"LFB: {exc}"]

    soup = BeautifulSoup(resp.content, "html.parser")

    heading = soup.find(
        lambda tag: tag.name in ("h2", "h3") and "upcoming" in (tag.get_text() or "").lower() and "event" in (tag.get_text() or "").lower()
    )
    if not heading:
        return [], ["LFB: Could not find events heading on page"]

    current_region = ""
    for el in heading.find_all_next():
        if el.name in ("h2",) and el != heading:
            break
        if el.name == "h3":
            current_region = el.get_text(strip=True)
        elif el.name == "li":
            link = el.find("a")
            if not link:
                continue
            text = el.get_text(strip=True)
            date_match = re.match(r"(\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})\s*[-–—]", text)
            if not date_match:
                continue

            dt = _parse_date(date_match.group(1))
            if dt is None:
                continue
            if dt < now or dt > end:
                continue

            title = str(link.get("title") or link.get_text(strip=True))
            href = str(link.get("href") or "")
            full_url = href if href.startswith("http") else f"https://www.london-fire.gov.uk{href}"

            events.append({
                "venue": "London Fire Brigade",
                "title": title.strip(),
                "description": f"Free fire station event — {current_region}. Meet firefighters, see engines, try equipment.",
                "start": dt.strftime("%Y-%m-%dT10:00:00"),
                "end": dt.strftime("%Y-%m-%dT16:00:00"),
                "url": full_url,
                "address": f"Fire station — {current_region} London",
                "distance": "Varies",
                "age": "All ages",
                "cost": "Free",
                "category": "Seasonal",
                "source": "LFB",
                "is_new": False,
            })

    if not events:
        errors.append("LFB: No events found in window")

    return events, errors
