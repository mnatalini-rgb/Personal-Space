from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup  # type: ignore[reportMissingImports]
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


def _find_date(text: str) -> str | None:
    if not text:
        return None
    try:
        return date_parser.parse(text, fuzzy=True).isoformat()
    except Exception:
        return None


def _has_date_like_text(text: str) -> bool:
    lowered = (text or "").lower()
    tokens = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "/",
        "202",
        ":",
    ]
    return any(token in lowered for token in tokens)


NAV_GARBAGE = [
    "skip to", "main content", "chevron", "cookie", "accept all",
    "our services", "menu", "log in", "sign up", "search", "footer",
    "breadcrumb", "navigation", "toggle", "close",
]


def _valid_title(title: str, text: str) -> bool:
    lowered = (title or "").strip().lower()
    if not lowered:
        return False
    if any(g in lowered for g in NAV_GARBAGE):
        return False
    if len(lowered.split()) < 4 and not _has_date_like_text(text):
        return False
    return True


def _extract_cards(url: str, venue_name: str, address: str, distance: str) -> list[dict]:
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    cards = []

    selectors = [".event-listing", ".event-item", ".card", "[data-event]", ".whats-on-item"]
    seen_links = set()
    found_structured = False

    for selector in selectors:
        for node in soup.select(selector):
            found_structured = True
            text = " ".join(node.stripped_strings)
            if len(text) < 20:
                continue
            if not is_family_relevant(text):
                continue
            link_node = node.find("a", href=True)
            if not link_node:
                continue
            href = urljoin(url, str(link_node.get("href") or ""))
            if href in seen_links:
                continue
            seen_links.add(href)
            title = as_text(link_node.get_text(strip=True)) or as_text(node.find(["h1", "h2", "h3"]))
            if not _valid_title(title, text):
                continue
            start_iso = _find_date(text)
            if start_iso:
                start, end = get_window_range()
                dt = date_parser.parse(start_iso)
                if dt < start or dt > end:
                    continue
            cards.append(
                {
                    "venue": venue_name,
                    "title": title or "Family event",
                    "description": text[:500],
                    "start": start_iso,
                    "end": None,
                    "url": href,
                    "address": address,
                    "distance": distance,
                    "age": "2-5 / family",
                    "cost": "Check venue",
                    "category": infer_category(text, default="Museums & Learning"),
                    "source": venue_name,
                }
            )

    if not found_structured:
        for link_node in soup.select("a[href]"):
            title = as_text(link_node.get_text(strip=True))
            parent = link_node.parent
            text = " ".join(parent.stripped_strings) if parent else title
            if len(text) < 20:
                continue
            if not is_family_relevant(text):
                continue
            if not _has_date_like_text(text):
                continue
            if not _valid_title(title, text):
                continue
            href = urljoin(url, str(link_node.get("href") or ""))
            if not href or href in seen_links:
                continue
            seen_links.add(href)
            start_iso = _find_date(text)
            if start_iso:
                start, end = get_window_range()
                dt = date_parser.parse(start_iso)
                if dt < start or dt > end:
                    continue
            cards.append(
                {
                    "venue": venue_name,
                    "title": title or "Family event",
                    "description": text[:500],
                    "start": start_iso,
                    "end": None,
                    "url": href,
                    "address": address,
                    "distance": distance,
                    "age": "2-5 / family",
                    "cost": "Check venue",
                    "category": infer_category(text, default="Museums & Learning"),
                    "source": venue_name,
                }
            )
    return cards


def fetch_tower_hamlets_events() -> tuple[list[dict], list[str]]:
    targets = [
        {
            "url": "https://www.towerhamlets.gov.uk/News_events/Events/Events.aspx?Calendar_List_SyndicationType=1",
            "venue": "Tower Hamlets Council",
            "address": "Tower Hamlets, London",
            "distance": "Local",
        },
        {
            "url": "https://www.ideastore.co.uk/whats-on",
            "venue": "Idea Store",
            "address": "Bow / Whitechapel / Canary Wharf / Chrisp Street",
            "distance": "Local",
        },
    ]

    out = []
    errors = []
    for target in targets:
        try:
            out.extend(
                _extract_cards(
                    target["url"],
                    target["venue"],
                    target["address"],
                    target["distance"],
                )
            )
        except Exception as exc:
            errors.append(f"{target['venue']}: {exc}")
    return out, errors
