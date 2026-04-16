from __future__ import annotations

import re
from datetime import datetime
from datetime import timedelta

import requests
from dateutil import parser as date_parser

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
MAX_PAGES = 10
REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}


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


def _in_window(dt: datetime, start: datetime, end: datetime) -> bool:
    clean = dt.replace(tzinfo=None) if dt.tzinfo else dt
    return start <= clean <= end


def _parse_start(entry: dict) -> str | None:
    candidates = [entry.get("startDate"), entry.get("startTime")]
    schedule = entry.get("eventSchedule")
    if isinstance(schedule, list) and schedule:
        first = schedule[0]
        if isinstance(first, dict):
            candidates.extend([first.get("startDate"), first.get("startTime")])
    if isinstance(schedule, dict):
        candidates.extend([schedule.get("startDate"), schedule.get("startTime")])
    for value in candidates:
        if not value:
            continue
        try:
            return date_parser.parse(str(value)).isoformat()
        except Exception:
            continue
    return None


def _age_relevant(entry: dict, combined_text: str) -> bool:
    lowered = (combined_text or "").lower()
    if any(x in lowered for x in EXCLUDE_KEYWORDS):
        return False
    if any(x in lowered for x in KIDS_KEYWORDS):
        return True
    if any(x in lowered for x in ["junior", "youth", "years", "under", "u5", "u6"]):
        return True
    if re.search(r"\b\d+\s*[-–]\s*\d+\s*(years|yrs)\b", lowered):
        return True

    age = entry.get("ageRange")
    if isinstance(age, dict):
        min_v = age.get("minValue")
        max_v = age.get("maxValue")
        try:
            min_n = int(min_v) if min_v is not None else None
            max_n = int(max_v) if max_v is not None else None
            if min_n is not None and min_n > 5:
                return False
            if max_n is not None and max_n < 2:
                return False
            if min_n is not None or max_n is not None:
                return True
        except Exception:
            return False
    return False


def _extract_items(payload) -> tuple[list, str | None]:
    if isinstance(payload, list):
        return payload, None
    if isinstance(payload, dict):
        items = payload.get("items") or payload.get("data") or payload.get("results") or []
        next_url = payload.get("next")
        if isinstance(next_url, dict):
            next_url = next_url.get("id") or next_url.get("url")
        return (items if isinstance(items, list) else []), next_url
    return [], None


def _venue_text(item: dict) -> str:
    location_raw = item.get("location")
    place_raw = item.get("superEvent")
    location = location_raw if isinstance(location_raw, dict) else {}
    place = place_raw if isinstance(place_raw, dict) else {}
    return " ".join(
        [
            as_text(location_raw),
            as_text(location.get("name")),
            as_text(location.get("address")),
            as_text(place.get("name")),
            as_text(place_raw),
            as_text(item.get("name")),
            as_text(item.get("activity")),
        ]
    ).lower()


def _format_address(location: dict) -> str:
    """Extract human-readable address from OpenActive location object."""
    addr = location.get("address")
    if isinstance(addr, dict):
        parts = []
        for key in ["streetAddress", "addressLocality", "addressRegion", "postalCode"]:
            val = addr.get(key)
            if val:
                parts.append(str(val))
        if parts:
            return ", ".join(parts)
    name = location.get("name")
    if name:
        return str(name)
    return "Check venue"


def _format_cost(offers) -> str:
    """Extract human-readable cost from OpenActive offers."""
    if not offers:
        return "Check venue"
    if isinstance(offers, list):
        prices = []
        for offer in offers:
            if not isinstance(offer, dict):
                continue
            price = offer.get("price")
            currency = offer.get("priceCurrency", "GBP")
            name = offer.get("name", "")
            if price is not None:
                symbol = "£" if currency == "GBP" else currency + " "
                prices.append(f"{name} {symbol}{price}".strip())
        if prices:
            return " / ".join(prices)
    if isinstance(offers, dict):
        price = offers.get("price")
        if price is not None:
            return f"£{price}"
    return "Check venue"


def _format_age(entry: dict) -> str:
    """Extract human-readable age range from OpenActive entry."""
    age_range = entry.get("ageRange")
    if isinstance(age_range, dict):
        min_v = age_range.get("minValue")
        max_v = age_range.get("maxValue")
        if min_v is not None and max_v is not None:
            return f"Ages {min_v}-{max_v}"
        if min_v is not None:
            return f"Ages {min_v}+"
        if max_v is not None:
            return f"Up to age {max_v}"
    return "Kids / family"


def fetch_openactive_events(endpoints: list[str], venue_keywords: list[str]) -> tuple[list[dict], list[str]]:
    start, end = get_window_range()
    # Also reject events with dates more than 1 year in the past (stale SessionSeries)
    stale_cutoff = start - timedelta(days=365)
    out = []
    errors = []

    for endpoint in endpoints:
        url = endpoint
        visited = set()
        pages = 0
        try:
            while url and url not in visited and pages < MAX_PAGES:
                visited.add(url)
                pages += 1
                response = requests.get(url, timeout=25, headers=REQUEST_HEADERS)
                if response.status_code >= 400:
                    raise RuntimeError(f"HTTP {response.status_code}")
                items, next_url = _extract_items(response.json())
                for item in items:
                    entry = item.get("data", item) if isinstance(item, dict) else item
                    if not isinstance(entry, dict):
                        continue
                    # Skip deleted items
                    if item.get("state") == "deleted":
                        continue
                    text = _venue_text(entry)
                    if not any(vk in text for vk in venue_keywords):
                        continue

                    title = as_text(entry.get("name") or entry.get("activity"))
                    summary = as_text(entry.get("description"))
                    full_text = f"{title} {summary}"
                    if not _age_relevant(entry, full_text):
                        continue

                    start_iso = _parse_start(entry)
                    dt = None
                    if start_iso:
                        try:
                            dt = date_parser.parse(start_iso)
                        except Exception:
                            dt = None
                    # Skip events with dates more than 1 year old (stale data)
                    if dt and dt.replace(tzinfo=None) < stale_cutoff:
                        continue
                    if dt and dt.replace(tzinfo=None) > end:
                        continue

                    location_raw = entry.get("location")
                    location = location_raw if isinstance(location_raw, dict) else {}
                    out.append(
                        {
                            "venue": as_text(location.get("name")) or "Better / GLL",
                            "title": title,
                            "description": summary,
                            "start": start_iso if dt and dt.replace(tzinfo=None) >= start else None,
                            "end": None,
                            "url": as_text(entry.get("url")) or endpoint,
                            "address": _format_address(location),
                            "distance": "~20-35 mins",
                            "age": _format_age(entry),
                            "cost": _format_cost(entry.get("offers")),
                            "category": infer_category(full_text, default="Sports & Swimming"),
                            "source": "Better OpenActive (CC BY 4.0)",
                        }
                    )
                url = next_url
        except Exception as exc:
            errors.append(f"OpenActive {endpoint}: {exc}")
    return out, errors
