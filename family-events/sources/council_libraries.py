from __future__ import annotations

import re
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
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

POSTCODE_RE = re.compile(r"\b([A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\b", re.IGNORECASE)
DATE_HINT_RE = re.compile(
    r"\b("
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"mondays|tuesdays|wednesdays|thursdays|fridays|saturdays|sundays|"
    r"jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec|"
    r"every|alternate|weekly|fortnightly|term-time"
    r")\b",
    re.IGNORECASE,
)
EVENTISH_KEYWORDS = [
    "story",
    "story time",
    "storytime",
    "baby bounce",
    "under 5",
    "under-5",
    "craft",
    "club",
    "reading group",
    "lego",
    "chess",
    "scrabble",
    "games",
    "colouring",
    "rhyme",
    "song",
    "drop-in",
    "drop in",
    "workshop",
    "session",
]


def _get_window_range() -> tuple[datetime, datetime]:
    start = datetime.now()
    return start, start + timedelta(days=WINDOW_DAYS)


def _clean_text(value: str | None) -> str:
    return " ".join((value or "").split())


def _html_to_text(value: str | None) -> str:
    return _clean_text(BeautifulSoup(value or "", "html.parser").get_text(" ", strip=True))


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


def _cost_from_text(text: str) -> str:
    return "Free" if "free" in (text or "").lower() else "Check venue"


def _parse_timestamp_ms(value) -> str | None:
    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(float(value) / 1000).isoformat()
    except Exception:
        return None


def _within_window(start_iso: str | None) -> bool:
    if not start_iso:
        return True
    try:
        start_dt = date_parser.parse(start_iso)
    except Exception:
        return False
    window_start, window_end = _get_window_range()
    return window_start <= start_dt <= window_end


def _make_event(
    *,
    venue: str,
    title: str,
    description: str,
    start: str | None,
    end: str | None,
    url: str,
    address: str,
    distance: str,
    age: str,
    cost: str,
    category: str,
    source: str,
) -> dict:
    return {
        "venue": venue,
        "title": title,
        "description": _clean_text(description)[:500],
        "start": start,
        "end": end,
        "url": url,
        "address": address,
        "distance": distance,
        "age": age,
        "cost": cost,
        "category": category,
        "source": source,
    }


def _looks_like_opening_hours(text: str) -> bool:
    lowered = (text or "").lower()
    weekdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    return sum(day in lowered for day in weekdays) >= 3 and "closed" in lowered


def _looks_dateish(text: str) -> bool:
    lowered = (text or "").lower()
    if DATE_HINT_RE.search(lowered):
        return True
    return bool(re.search(r"\b\d{1,2}([:/.-]\d{1,2})?\s*(am|pm)?\b", lowered))


def _is_recurring_text(text: str) -> bool:
    lowered = (text or "").lower()
    return any(
        token in lowered
        for token in [
            "every",
            "alternate",
            "weekly",
            "fortnightly",
            "term-time",
            "mondays",
            "tuesdays",
            "wednesdays",
            "thursdays",
            "fridays",
            "saturdays",
            "sundays",
        ]
    )


def _parse_freeform_date(text: str) -> str | None:
    if not text or not _looks_dateish(text):
        return None
    try:
        return date_parser.parse(text, fuzzy=True).isoformat()
    except Exception:
        return None


def _extract_postcode(text: str) -> str | None:
    match = POSTCODE_RE.search((text or "").upper())
    if not match:
        return None
    return _clean_text(match.group(1).upper())


def _extract_islington_venue(title: str) -> str:
    cleaned = _clean_text(title)
    cleaned = re.sub(r"^Islington Libraries\s*[:\-]\s*", "", cleaned, flags=re.IGNORECASE)
    if " - " in cleaned:
        prefix = cleaned.split(" - ", 1)[0].strip()
    else:
        match = re.search(r"([A-Z][A-Za-z'&\- ]+Library)", cleaned)
        prefix = match.group(1).strip() if match else "Islington Library"
    if "library" not in prefix.lower():
        return "Islington Library"
    if prefix.lower().startswith("islington"):
        return prefix
    return f"Islington {prefix}"


def _is_islington_event_candidate(title: str, text: str, start_iso: str | None) -> bool:
    combined = f"{title} {text}".lower()
    if _looks_like_opening_hours(text) and not any(keyword in combined for keyword in EVENTISH_KEYWORDS):
        return False
    if start_iso:
        return True
    return any(keyword in combined for keyword in EVENTISH_KEYWORDS)


def _fetch_hackney_events() -> tuple[list[dict], list[str]]:
    url = "https://lovehackney.uk/whats-on?format=json"
    events: list[dict] = []
    errors: list[str] = []
    seen_urls: set[str] = set()

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        payload = response.json()
        for bucket in ("upcoming", "past"):
            for item in payload.get(bucket, []) or []:
                title = _clean_text(str(item.get("title") or ""))
                excerpt = _html_to_text(item.get("excerpt") or item.get("body") or "")
                categories = [str(value).strip() for value in item.get("categories") or [] if value]
                tags = [str(value).strip() for value in item.get("tags") or [] if value]
                combined_text = " ".join([title, excerpt, " ".join(categories), " ".join(tags)])
                if not title:
                    continue
                if "Families" not in categories and "Libraries" not in categories and not is_family_relevant(combined_text):
                    continue

                start_iso = _parse_timestamp_ms(item.get("startDate"))
                if not start_iso or not _within_window(start_iso):
                    continue
                end_iso = _parse_timestamp_ms(item.get("endDate"))
                event_url = urljoin("https://lovehackney.uk", str(item.get("fullUrl") or ""))
                if not event_url or event_url in seen_urls:
                    continue
                seen_urls.add(event_url)

                location = item.get("location") or {}
                venue = _clean_text(location.get("addressTitle") or "") or "Hackney Library"
                address_parts = [
                    _clean_text(location.get("addressTitle") or ""),
                    _clean_text(location.get("addressLine1") or ""),
                    _clean_text(location.get("addressLine2") or ""),
                ]
                address = ", ".join([part for part in address_parts if part]) or "Hackney, London"
                events.append(
                    _make_event(
                        venue=venue,
                        title=title,
                        description=excerpt or title,
                        start=start_iso,
                        end=end_iso,
                        url=event_url,
                        address=address,
                        distance="~25 mins",
                        age="2-5 / family",
                        cost=_cost_from_text(combined_text),
                        category=infer_category(combined_text, default="Museums & Learning"),
                        source="Hackney Libraries",
                    )
                )
    except Exception as exc:
        errors.append(f"Hackney Libraries: {exc}")

    return events, errors


def _fetch_islington_events() -> tuple[list[dict], list[str]]:
    url = (
        "https://directory.islington.gov.uk/kb5/islington/directory/results.action?"
        "qt=library+children&familychannelnew=0&sorttype=relevance"
    )
    base_url = "https://directory.islington.gov.uk/kb5/islington/directory/"
    events: list[dict] = []
    errors: list[str] = []
    seen_urls: set[str] = set()

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if "just a moment" in soup.get_text(" ", strip=True).lower():
            raise RuntimeError("Cloudflare challenge blocked request")

        result_nodes: list = []
        seen_nodes: set[int] = set()
        for selector in ["div.results li", "main li", "#content li", ".results li", "li"]:
            for node in soup.select(selector):
                if not node.find("h3") or not node.find("a", href=True):
                    continue
                node_id = id(node)
                if node_id in seen_nodes:
                    continue
                seen_nodes.add(node_id)
                result_nodes.append(node)

        for node in result_nodes:
            title_node = node.find("h3")
            link_node = title_node.find("a", href=True) if title_node else node.find("a", href=True)
            if not title_node or not link_node:
                continue

            title = _clean_text(title_node.get_text(" ", strip=True))
            event_url = urljoin(base_url, str(link_node.get("href") or ""))
            if not title or not event_url or event_url in seen_urls:
                continue

            text_parts = [_clean_text(part) for part in node.stripped_strings]
            if text_parts and text_parts[0] == title:
                text_parts = text_parts[1:]
            body_text = _clean_text(" ".join(text_parts))
            if not is_family_relevant(f"{title} {body_text}"):
                continue

            date_text = next((part for part in text_parts if _looks_dateish(part)), "")
            start_iso = _parse_freeform_date(date_text)
            if start_iso:
                try:
                    start_dt = date_parser.parse(start_iso)
                    now, window_end = _get_window_range()
                    if _is_recurring_text(date_text) and start_dt < now:
                        start_iso = None
                    elif start_dt < now or start_dt > window_end:
                        continue
                except Exception:
                    start_iso = None

            if not _is_islington_event_candidate(title, body_text, start_iso):
                continue

            postcode = None
            maps_link = node.find("a", href=re.compile(r"maps\.google\.co\.uk", re.IGNORECASE))
            if maps_link:
                postcode = _extract_postcode(maps_link.get_text(" ", strip=True)) or _extract_postcode(
                    str(maps_link.get("href") or "")
                )
            postcode = postcode or _extract_postcode(body_text)
            address = f"Islington {postcode}" if postcode else "Islington, London"
            description = body_text or title

            seen_urls.add(event_url)
            events.append(
                _make_event(
                    venue=_extract_islington_venue(title),
                    title=title,
                    description=description,
                    start=start_iso,
                    end=None,
                    url=event_url,
                    address=address,
                    distance="~35 mins",
                    age="2-5 / family",
                    cost=_cost_from_text(description),
                    category=infer_category(f"{title} {description}", default="Museums & Learning"),
                    source="Islington Libraries",
                )
            )
    except Exception as exc:
        errors.append(f"Islington Libraries: {exc}")

    return events, errors


def _playwright_soup(url: str) -> BeautifulSoup:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "Newham Libraries requires playwright: pip install playwright && playwright install chromium"
        ) from exc
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000, wait_until="networkidle")
        html = page.content()
        browser.close()
    return BeautifulSoup(html, "html.parser")


def _extract_newham_venue(title: str, text: str) -> str:
    combined = f"{title} {text}"
    match = re.search(r"([A-Z][A-Za-z'&\- ]+(?:Library|Libraries))", combined)
    if match:
        return _clean_text(match.group(1))
    return "Newham Library"


def _fetch_newham_events() -> tuple[list[dict], list[str]]:
    url = "https://newham.events.mylibrary.digital/"
    events: list[dict] = []
    errors: list[str] = []
    seen_urls: set[str] = set()

    try:
        soup = _playwright_soup(url)
        page_text = soup.get_text(" ", strip=True).lower()
        if any(token in page_text for token in ["access denied", "forbidden", "403", "challenge", "just a moment"]):
            raise RuntimeError("site blocked automated browser access")

        selectors = [
            "article",
            "li",
            ".event-card",
            ".event-item",
            ".listing",
            "[class*=event]",
            "[class*=card]",
        ]
        for selector in selectors:
            for node in soup.select(selector):
                link_node = node.find("a", href=True)
                if not link_node:
                    continue
                title_node = node.find(["h2", "h3", "h4"]) or link_node
                title = _clean_text(title_node.get_text(" ", strip=True))
                body_text = _clean_text(" ".join(node.stripped_strings))
                if not title or len(body_text) < 15:
                    continue
                if not is_family_relevant(f"{title} {body_text}"):
                    continue

                event_url = urljoin(url, str(link_node.get("href") or ""))
                if not event_url or event_url in seen_urls:
                    continue

                start_iso = _parse_freeform_date(body_text)
                if start_iso and not _within_window(start_iso):
                    continue

                seen_urls.add(event_url)
                venue = _extract_newham_venue(title, body_text)
                postcode = _extract_postcode(body_text)
                address = f"Newham {postcode}" if postcode else "Newham, London"
                events.append(
                    _make_event(
                        venue=venue,
                        title=title,
                        description=body_text,
                        start=start_iso,
                        end=None,
                        url=event_url,
                        address=address,
                        distance="~20 mins",
                        age="2-5 / family",
                        cost=_cost_from_text(body_text),
                        category=infer_category(f"{title} {body_text}", default="Museums & Learning"),
                        source="Newham Libraries",
                    )
                )
        if not events:
            errors.append("Newham Libraries: no family-relevant events found or page structure unavailable")
    except Exception as exc:
        errors.append(f"Newham Libraries: {exc}")

    return events, errors


def fetch_council_library_events() -> tuple[list[dict], list[str]]:
    all_events: list[dict] = []
    all_errors: list[str] = []

    for source_name, fetcher in [
        ("Hackney Libraries", _fetch_hackney_events),
        ("Islington Libraries", _fetch_islington_events),
        ("Newham Libraries", _fetch_newham_events),
    ]:
        try:
            events, errors = fetcher()
            all_events.extend(events)
            all_errors.extend(errors)
        except Exception as exc:
            all_errors.append(f"{source_name}: {exc}")

    return all_events, all_errors
