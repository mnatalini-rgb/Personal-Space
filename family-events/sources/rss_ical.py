from __future__ import annotations

try:
    import feedparser
except ImportError:
    feedparser = None
import requests
from dateutil import parser as date_parser
from icalendar import Calendar

from datetime import datetime
from datetime import timedelta

WINDOW_DAYS = 120
KIDS_KEYWORDS = [
    "baby",
    "babies",
    "toddler",
    "under 5",
    "under-5",
    "0-5",
    "2-5",
    "3+",
    "family",
    "children",
    "child",
    "kids",
    "all ages",
    "storytime",
    "rhyme",
    "craft",
]
EXCLUDE_KEYWORDS = ["18+", "adults only", "over 16"]
REQUEST_HEADERS = {"User-Agent": "family-events-aggregator/1.0"}


def get_window_range() -> tuple[datetime, datetime]:
    start = datetime.now()
    end = start + timedelta(days=WINDOW_DAYS)
    return start, end


def as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return " ".join([str(v) for v in value.values() if v])
    if isinstance(value, list):
        return " ".join([as_text(v) for v in value if v])
    return str(value)


def is_family_relevant(text: str) -> bool:
    lowered = (text or "").lower()
    if not lowered.strip():
        return False
    if any(x in lowered for x in EXCLUDE_KEYWORDS):
        return False
    return any(x in lowered for x in KIDS_KEYWORDS)


def infer_category(text: str, default: str = "Museums & Learning") -> str:
    lowered = (text or "").lower()
    if any(x in lowered for x in ["theatre", "show", "puppet", "performance", "stage"]):
        return "Theatre & Shows"
    if any(x in lowered for x in ["museum", "library", "workshop", "science", "learn", "story"]):
        return "Museums & Learning"
    if any(x in lowered for x in ["park", "outdoor", "nature", "garden", "playground"]):
        return "Outdoor & Parks"
    if any(x in lowered for x in ["swim", "aquatic", "sport", "football", "gym", "riding"]):
        return "Sports & Swimming"
    if any(x in lowered for x in ["soft play", "indoor play", "toddler world"]):
        return "Soft Play & Indoor"
    if any(x in lowered for x in ["farm", "animal", "petting", "zoo"]):
        return "Farms & Animals"
    if any(x in lowered for x in ["christmas", "summer", "easter", "halloween", "seasonal"]):
        return "Seasonal"
    return default


def _is_within_window(dt: datetime, start: datetime, end: datetime) -> bool:
    clean = dt.replace(tzinfo=None) if dt.tzinfo else dt
    return start <= clean <= end


def _parse_date(value) -> str | None:
    if not value:
        return None
    try:
        return date_parser.parse(str(value)).isoformat()
    except Exception:
        return None


def fetch_rss_ical_events(feed_defs: list[dict], aquatics_json: dict) -> tuple[list[dict], list[str]]:
    start, end = get_window_range()
    out = []
    errors = []

    for feed_def in feed_defs:
        try:
            if feed_def.get("type") == "rss":
                if feedparser is None:
                    raise RuntimeError("feedparser not installed")
                parsed = feedparser.parse(feed_def["url"])
                for entry in parsed.entries:
                    title = as_text(getattr(entry, "title", ""))
                    link = as_text(getattr(entry, "link", ""))
                    if not title.strip() or not link.strip():
                        continue
                    if feed_def.get("name") == "British Library":
                        bl_skip = ["kickstart", "business", "ip for", "intellectual property",
                                   "profile:", "author:", "curator:"]
                        if any(kw in title.lower() for kw in bl_skip):
                            continue
                    summary = as_text(getattr(entry, "summary", ""))
                    full_text = f"{title} {summary}"
                    if not is_family_relevant(full_text):
                        continue
                    date_raw = getattr(entry, "published", None) or getattr(entry, "updated", None)
                    start_iso = _parse_date(date_raw)
                    if not start_iso:
                        continue
                    dt = date_parser.parse(start_iso)
                    if not _is_within_window(dt, start, end):
                        continue
                    out.append(
                        {
                            "venue": feed_def["name"],
                            "title": title,
                            "description": summary,
                            "start": start_iso,
                            "end": None,
                            "url": as_text(getattr(entry, "link", "")) or feed_def["url"],
                            "address": feed_def.get("address"),
                            "distance": feed_def.get("distance_from_e3", "~30 mins"),
                            "age": "2-5 / family",
                            "cost": "Check venue",
                            "category": feed_def.get("category") or infer_category(full_text),
                            "source": f"RSS ({feed_def['name']})",
                        }
                    )

            if feed_def.get("type") == "ical":
                response = requests.get(feed_def["url"], timeout=20, headers=REQUEST_HEADERS)
                response.raise_for_status()
                cal = Calendar.from_ical(response.text)
                for component in cal.walk("VEVENT"):
                    title = as_text(component.get("summary"))
                    summary = as_text(component.get("description"))
                    full_text = f"{title} {summary}"
                    if not is_family_relevant(full_text):
                        continue
                    start_value = component.get("dtstart")
                    if not start_value:
                        continue
                    start_iso = _parse_date(start_value.dt)
                    if not start_iso:
                        continue
                    dt = date_parser.parse(start_iso)
                    if not _is_within_window(dt, start, end):
                        continue
                    out.append(
                        {
                            "venue": feed_def["name"],
                            "title": title,
                            "description": summary,
                            "start": start_iso,
                            "end": _parse_date(component.get("dtend").dt) if component.get("dtend") else None,
                            "url": feed_def["url"],
                            "address": feed_def.get("address"),
                            "distance": feed_def.get("distance_from_e3", "~30 mins"),
                            "age": "2-5 / family",
                            "cost": "Check venue",
                            "category": feed_def.get("category") or infer_category(full_text),
                            "source": f"iCal ({feed_def['name']})",
                        }
                    )
        except Exception as exc:
            errors.append(f"Feed {feed_def.get('name')}: {exc}")

    try:
        response = requests.get(aquatics_json["url"], timeout=20, headers=REQUEST_HEADERS)
        response.raise_for_status()
        payload = response.json()
        events = payload.get("events") or payload.get("data") or []
        for event in events:
            title = as_text(event.get("title"))
            summary = as_text(event.get("description"))
            full_text = f"{title} {summary}"
            if not is_family_relevant(full_text):
                continue
            start_iso = _parse_date(event.get("start_date") or event.get("start_date_utc"))
            if not start_iso:
                continue
            dt = date_parser.parse(start_iso)
            if not _is_within_window(dt, start, end):
                continue
            out.append(
                {
                    "venue": aquatics_json["name"],
                    "title": title,
                    "description": summary,
                    "start": start_iso,
                    "end": _parse_date(event.get("end_date") or event.get("end_date_utc")),
                    "url": as_text(event.get("url")) or aquatics_json["url"],
                    "address": aquatics_json.get("address"),
                    "distance": aquatics_json.get("distance_from_e3"),
                    "age": "2-5 / family",
                    "cost": as_text(event.get("cost")) or "Check venue",
                    "category": aquatics_json.get("category") or infer_category(full_text),
                    "source": "London Aquatics Centre WP API",
                }
            )
    except Exception as exc:
        errors.append(f"London Aquatics Centre feed: {exc}")

    return out, errors
