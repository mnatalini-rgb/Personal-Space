from __future__ import annotations

import re
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup  # type: ignore[reportMissingImports]
from dateutil import parser as date_parser

WINDOW_DAYS = 120
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}

KIDS_KEYWORDS = [
    "baby", "babies", "toddler", "under 5", "under-5", "0-5", "2-5", "3+",
    "family", "children", "child", "kids", "all ages", "storytime", "rhyme",
    "craft", "sensory", "little", "young", "half term", "half-term",
]
EXCLUDE_KEYWORDS = ["18+", "adults only", "over 16", "late night", "lates"]


def _get_window() -> tuple[datetime, datetime]:
    now = datetime.now()
    return now, now + timedelta(days=WINDOW_DAYS)


def _is_family(text: str) -> bool:
    lowered = (text or "").lower()
    if any(x in lowered for x in EXCLUDE_KEYWORDS):
        return False
    return any(x in lowered for x in KIDS_KEYWORDS)


def _find_date(text: str) -> str | None:
    if not text:
        return None
    try:
        return date_parser.parse(text, fuzzy=True, dayfirst=True).isoformat()
    except Exception:
        return None


def _infer_category(text: str) -> str:
    lowered = (text or "").lower()
    if any(x in lowered for x in ["theatre", "show", "puppet", "performance", "stage"]):
        return "Theatre & Shows"
    if any(x in lowered for x in ["park", "outdoor", "nature", "garden"]):
        return "Outdoor & Parks"
    return "Museums & Learning"


def _make_event(
    venue: str, title: str, description: str, start: str | None,
    url: str, address: str, distance: str, cost: str = "Check venue",
) -> dict:
    return {
        "venue": venue,
        "title": title,
        "description": description[:500],
        "start": start,
        "end": None,
        "url": url,
        "address": address,
        "distance": distance,
        "age": "2-5 / family",
        "cost": cost,
        "category": _infer_category(description),
        "source": venue,
        "is_new": False,
    }


def _fetch_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=30, headers=HEADERS)
    resp.raise_for_status()
    return BeautifulSoup(resp.content, "html.parser")


NAV_JUNK = [
    "skip to", "menu", "cookie", "log in", "search", "footer",
    "navigation", "breadcrumb", "accept all", "sign up",
]


def _try_add_event(
    node, url: str, venue: str, address: str, distance: str,
    seen: set, start_window: datetime, end_window: datetime,
    always_relevant: bool, cost: str,
) -> dict | None:
    link = node.find("a", href=True) if node.name != "a" else node
    if not link:
        return None
    href = urljoin(url, str(link.get("href", "")))
    if href in seen or not href.startswith("http"):
        return None

    text = " ".join(node.stripped_strings)
    if len(text) < 15:
        return None
    if not always_relevant and not _is_family(text):
        return None

    title_el = node.find(["h2", "h3", "h4"]) if node.name != "a" else None
    title = (title_el or link).get_text(strip=True) if (title_el or link) else "Family event"
    if not title or len(title) < 3:
        return None
    if any(x in title.lower() for x in NAV_JUNK):
        return None

    seen.add(href)
    date_iso = _find_date(text)
    if date_iso:
        try:
            dt = date_parser.parse(date_iso)
            if dt < start_window or dt > end_window:
                return None
        except Exception:
            pass

    return _make_event(
        venue=venue, title=title, description=text,
        start=date_iso, url=href, address=address,
        distance=distance, cost=cost,
    )


def _generic_card_scrape(
    url: str, venue: str, address: str, distance: str,
    always_relevant: bool = False,
    selectors: list[str] | None = None,
    cost: str = "Check venue",
) -> list[dict]:
    """Generic card-based scraper with link-scanning fallback."""
    soup = _fetch_soup(url)
    events: list[dict] = []
    seen: set[str] = set()
    start_window, end_window = _get_window()

    exact_selectors = selectors or [
        "article", ".card", ".event-card", ".event-item", ".event-listing",
        ".whats-on-item", ".listing-item", "[data-event]", ".grid-item",
        ".teaser", ".promo", ".node--type-event", ".views-row",
        ".event", ".listing", ".result-item",
    ]

    partial_selectors = [
        "[class*=card]", "[class*=event]", "[class*=listing]",
        "[class*=teaser]", "[class*=promo]", "[class*=result]",
    ]

    for sel in exact_selectors + partial_selectors:
        for node in soup.select(sel):
            ev = _try_add_event(
                node, url, venue, address, distance, seen,
                start_window, end_window, always_relevant, cost,
            )
            if ev:
                events.append(ev)

    if not events:
        for link in soup.find_all("a", href=True):
            parent = link.parent
            container = parent if parent else link
            ev = _try_add_event(
                container, url, venue, address, distance, seen,
                start_window, end_window, always_relevant, cost,
            )
            if ev:
                events.append(ev)

    return events



def _scrape_nhm(cfg: dict) -> list[dict]:
    """Natural History Museum — Next.js, try __NEXT_DATA__ first, then cards."""
    url = cfg["url"]
    soup = _fetch_soup(url)

    next_data = soup.find("script", id="__NEXT_DATA__")
    if next_data and next_data.string:
        import json
        try:
            data = json.loads(next_data.string)
            props = data.get("props", {}).get("pageProps", {})
            events_data = (
                props.get("events")
                or props.get("items")
                or props.get("data", {}).get("events")
                or []
            )
            if isinstance(events_data, list) and events_data:
                events = []
                start_w, end_w = _get_window()
                for item in events_data:
                    title = item.get("title") or item.get("name") or ""
                    desc = item.get("description") or item.get("summary") or title
                    text = f"{title} {desc}"
                    if not _is_family(text):
                        continue
                    slug = item.get("slug") or item.get("url") or ""
                    link = slug if slug.startswith("http") else urljoin(url, slug)
                    date_str = item.get("startDate") or item.get("date") or ""
                    date_iso = _find_date(str(date_str))
                    events.append(_make_event(
                        venue=cfg["name"], title=title, description=text,
                        start=date_iso, url=link, address=cfg["address"],
                        distance=cfg["distance_from_e3"],
                    ))
                if events:
                    return events
        except (json.JSONDecodeError, KeyError):
            pass

    return _generic_card_scrape(
        url=url, venue=cfg["name"], address=cfg["address"],
        distance=cfg["distance_from_e3"], always_relevant=False,
    )


def _scrape_bank_of_england(cfg: dict) -> list[dict]:
    """Bank of England Museum — server-rendered cards."""
    return _generic_card_scrape(
        url=cfg["url"], venue=cfg["name"], address=cfg["address"],
        distance=cfg["distance_from_e3"], always_relevant=False,
        cost="Free",
    )


def _scrape_science_museum(cfg: dict) -> list[dict]:
    """Science Museum — Drupal, server-rendered."""
    return _generic_card_scrape(
        url=cfg["url"], venue=cfg["name"], address=cfg["address"],
        distance=cfg["distance_from_e3"], always_relevant=False,
    )


def _scrape_lt_museum(cfg: dict) -> list[dict]:
    """London Transport Museum — may need headers for 403."""
    return _generic_card_scrape(
        url=cfg["url"], venue=cfg["name"], address=cfg["address"],
        distance=cfg["distance_from_e3"], always_relevant=False,
    )


def _scrape_southbank(cfg: dict) -> list[dict]:
    """Southbank Centre — family filter URL, always relevant."""
    return _generic_card_scrape(
        url=cfg["url"], venue=cfg["name"], address=cfg["address"],
        distance=cfg["distance_from_e3"], always_relevant=True,
    )


def _scrape_british_museum(cfg: dict) -> list[dict]:
    """British Museum — family visits page, always relevant."""
    return _generic_card_scrape(
        url=cfg["url"], venue=cfg["name"], address=cfg["address"],
        distance=cfg["distance_from_e3"], always_relevant=True,
    )


def _scrape_national_gallery(cfg: dict) -> list[dict]:
    """National Gallery — use /events for listings."""
    return _generic_card_scrape(
        url=cfg["url"], venue=cfg["name"], address=cfg["address"],
        distance=cfg["distance_from_e3"], always_relevant=False,
    )


def _scrape_tate(cfg: dict) -> list[dict]:
    """Tate — Django, family filter, London only."""
    events = []
    for gallery_url in cfg.get("urls", [cfg["url"]]):
        events.extend(_generic_card_scrape(
            url=gallery_url, venue=cfg["name"], address=cfg["address"],
            distance=cfg["distance_from_e3"], always_relevant=True,
        ))
    return events


_SCRAPERS = {
    "nhm": _scrape_nhm,
    "bank_of_england": _scrape_bank_of_england,
    "science_museum": _scrape_science_museum,
    "lt_museum": _scrape_lt_museum,
    "southbank": _scrape_southbank,
    "british_museum": _scrape_british_museum,
    "national_gallery": _scrape_national_gallery,
    "tate": _scrape_tate,
}


def fetch_museum_events(sources: list[dict]) -> tuple[list[dict], list[str]]:
    """Fetch events from all configured museum sources."""
    all_events: list[dict] = []
    errors: list[str] = []

    for cfg in sources:
        scraper_key = cfg.get("scraper", "")
        scraper_fn = _SCRAPERS.get(scraper_key)
        if not scraper_fn:
            errors.append(f"{cfg['name']}: unknown scraper '{scraper_key}'")
            continue
        try:
            events = scraper_fn(cfg)
            all_events.extend(events)
        except Exception as exc:
            errors.append(f"{cfg['name']}: {exc}")

    return all_events, errors
