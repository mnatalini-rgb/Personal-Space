from __future__ import annotations

from datetime import datetime
from datetime import timedelta

import requests
from dateutil import parser as date_parser

WINDOW_DAYS = 28
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


def _collect_events(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ["items", "results", "value", "Events", "events"]:
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _parse_start(event: dict) -> str | None:
    candidates = [
        event.get("firstInstanceDateTime"),
        event.get("firstInstanceDateTimeUtc"),
        event.get("instanceStart"),
        event.get("start"),
        event.get("startDate"),
        event.get("StartDate"),
    ]
    instances = event.get("instances") or event.get("Instances") or []
    if isinstance(instances, list) and instances:
        first = instances[0] or {}
        candidates.extend(
            [
                first.get("start"),
                first.get("startDate"),
                first.get("instanceStart"),
            ]
        )
    for value in candidates:
        if not value:
            continue
        try:
            return date_parser.parse(str(value)).isoformat()
        except Exception:
            continue
    return None


def fetch_spektrix_events(venues: list[dict]) -> tuple[list[dict], list[str]]:
    start, end = get_window_range()
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")
    out = []
    errors = []

    for venue in venues:
        loaded = False
        last_error = None
        always_relevant = bool(venue.get("always_relevant", False))
        for client in venue.get("client_candidates", []):
            url = (
                f"https://system.spektrix.com/{client}/api/v3/events"
                f"?instanceStart_from={start_str}&instanceStart_to={end_str}"
            )
            try:
                response = requests.get(url, timeout=20)
                if response.status_code >= 400:
                    raise RuntimeError(f"HTTP {response.status_code}")
                events = _collect_events(response.json())
                loaded = True
                for raw in events:
                    title = as_text(raw.get("name") or raw.get("Name") or raw.get("title"))
                    description = as_text(raw.get("description") or raw.get("Description"))
                    age_guide = as_text(raw.get("attribute_AgeGuide") or raw.get("ageGuidance"))
                    age_category = as_text(raw.get("attribute_AgeCategory"))
                    full_text = f"{title} {description}"
                    age_text = f"{age_guide} {age_category}".strip()
                    if not always_relevant and not is_family_relevant(f"{full_text} {age_text}"):
                        continue
                    start_iso = _parse_start(raw)
                    if not start_iso:
                        continue
                    try:
                        dt = datetime.fromisoformat(start_iso)
                        if dt < start or dt > end:
                            continue
                    except Exception:
                        continue
                    event_id = raw.get("id") or raw.get("Id") or raw.get("eventId")
                    event_url = venue.get("website") or raw.get("url")
                    out.append(
                        {
                            "venue": venue.get("name"),
                            "title": title,
                            "description": description,
                            "start": start_iso,
                            "end": None,
                            "url": event_url or f"https://system.spektrix.com/{client}",
                            "address": venue.get("address"),
                            "distance": venue.get("distance_from_e3"),
                            "age": age_text or as_text(raw.get("tags")) or "2-5 / family",
                            "cost": as_text(raw.get("fromPrice") or raw.get("price")) or "Check venue",
                            "category": venue.get("category") or infer_category(full_text),
                            "source": f"Spektrix ({client})",
                        }
                    )
                if events:
                    break
            except Exception as exc:
                last_error = str(exc)

        if not loaded:
            errors.append(f"Spektrix {venue.get('name')}: {last_error or 'No data'}")
    return out, errors
