from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
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
    "animal", "animals", "zoo", "farm", "nature", "bluey", "peppa",
    "paw patrol", "interactive", "easter", "halloween", "christmas",
    "meet and greet", "trail", "tour", "school holiday", "school holidays",
]
EXCLUDE_KEYWORDS = ["18+", "adults only", "over 16", "late night", "lates", "margaritas"]

NAV_JUNK = [
    "skip to", "menu", "cookie", "log in", "search", "footer",
    "navigation", "breadcrumb", "accept all", "sign up", "buy tickets",
]

DATE_PATTERNS = [
    r"\b(?:mon|tue|wed|thu|thur|thurs|fri|sat|sun)\s+\d{1,2}(?:st|nd|rd|th)?\s+[a-z]+\s+\d{4}\b",
    r"\b\d{1,2}(?:st|nd|rd|th)?\s+[a-z]+\s+\d{4}\b",
    r"\b[a-z]+\s+\d{1,2},\s*\d{4}\b",
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
]

EVENT_HINTS = [
    "event", "events", "meet and greet", "tour", "trail", "festival", "show",
    "session", "special", "workshop", "tickets", "easter", "summer", "christmas",
    "halloween", "father's day", "grandparents' day", "party", "circus",
]

_ATTRACTION_SOURCES = [
    {
        "scraper": "garden_museum",
        "name": "Garden Museum",
        "url": "https://www.gardenmuseum.org.uk/whats-on/",
        "api_url": "https://www.gardenmuseum.org.uk/wp-json/wp/v2/posts?per_page=100",
        "family_url": "https://www.gardenmuseum.org.uk/learn/families/",
        "address": "5 Lambeth Palace Rd, London SE1 7LB",
        "distance_from_e3": "~7 miles",
        "default_category": "Museums & Learning",
        "cost": "Check venue",
    },
    {
        "scraper": "hertfordshire_zoo",
        "name": "Hertfordshire Zoo",
        "url": "https://hertfordshirezoo.com/events/",
        "api_url": "https://hertfordshirezoo.com/wp-json/wp/v2/posts?per_page=100",
        "feed_url": "https://hertfordshirezoo.com/feed",
        "address": "Harpenden Rd, Wheathampstead, St Albans AL4 8QH",
        "distance_from_e3": "~35 miles",
        "default_category": "Farms & Animals",
        "cost": "Check venue",
    },
    {
        "scraper": "omd_farm",
        "name": "Old MacDonald's Farm",
        "url": "https://omdfarm.co.uk/special-events",
        "address": "Weald Rd, Brentwood CM14 5AY",
        "distance_from_e3": "~20 miles",
        "default_category": "Farms & Animals",
        "cost": "Included with admission",
    },
    {
        "scraper": "cedars_nature_centre",
        "name": "Cedars Nature Centre",
        "url": "https://www.cedarsnaturecentre.co.uk/",
        "sitemap_url": "https://www.cedarsnaturecentre.co.uk/event-pages-sitemap.xml",
        "address": "Cedars Park, Theobalds Ln, Waltham Cross EN8 8RU",
        "distance_from_e3": "~15 miles",
        "default_category": "Farms & Animals",
        "cost": "Check venue",
    },
    {
        "scraper": "gtka",
        "name": "Go To Kids Activities",
        "url": "https://gtka.co.uk/",
        "api_url": "https://gtka.co.uk/wp-json/wp/v2/posts?per_page=100",
        "feed_url": "https://gtka.co.uk/feed",
        "address": "Various locations",
        "distance_from_e3": "Varies",
        "default_category": "Farms & Animals",
        "cost": "Check venue",
    },
    {
        "scraper": "exotic_explorers",
        "name": "Exotic Explorers",
        "url": "https://exoticexplorers.co.uk/events",
        "address": "Essex based",
        "distance_from_e3": "Varies",
        "default_category": "Farms & Animals",
        "cost": "Check website",
    },
    {
        "scraper": "epping_forest",
        "name": "Visit Epping Forest",
        "url": "https://www.visiteppingforest.org/events",
        "address": "Epping Forest, Essex",
        "distance_from_e3": "~15 miles",
        "default_category": "Outdoor & Parks",
        "cost": "Check venue",
    },
]


def _get_window() -> tuple[datetime, datetime]:
    now = datetime.now()
    return now, now + timedelta(days=WINDOW_DAYS)


def _is_family(text: str) -> bool:
    lowered = (text or "").lower()
    if any(x in lowered for x in EXCLUDE_KEYWORDS):
        return False
    return any(x in lowered for x in KIDS_KEYWORDS)


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = date_parser.parse(value, fuzzy=True, dayfirst=True)
    except Exception:
        return None
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)
    return dt


def _normalise_date(value: str | None) -> str | None:
    dt = _parse_dt(value)
    return dt.isoformat() if dt else None


def _find_date(text: str) -> str | None:
    if not text:
        return None
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        dt = _parse_dt(match.group(0))
        if dt:
            return dt.isoformat()
    dt = _parse_dt(text)
    return dt.isoformat() if dt else None


def _infer_category(text: str, default: str = "Farms & Animals") -> str:
    lowered = (text or "").lower()
    if any(x in lowered for x in ["theatre", "show", "puppet", "performance", "stage"]):
        return "Theatre & Shows"
    if any(x in lowered for x in ["museum", "gallery", "learning", "workshop", "story"]):
        return "Museums & Learning"
    if any(x in lowered for x in ["park", "outdoor", "garden", "nature"]):
        return "Outdoor & Parks"
    if any(x in lowered for x in ["farm", "animal", "zoo", "petting"]):
        return "Farms & Animals"
    return default


def _make_event(
    venue: str,
    title: str,
    description: str,
    start: str | None,
    url: str,
    address: str,
    distance: str,
    cost: str = "Check venue",
    category: str | None = None,
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
        "category": category or _infer_category(description),
        "source": venue,
        "is_new": False,
    }


def _fetch_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=30, headers=HEADERS)
    resp.raise_for_status()
    return BeautifulSoup(resp.content, "html.parser")


def _strip_html(value: str | None) -> str:
    if not value:
        return ""
    return BeautifulSoup(value, "html.parser").get_text(" ", strip=True)


def _within_window(date_iso: str | None, start_window: datetime, end_window: datetime) -> bool:
    dt = _parse_dt(date_iso)
    if not dt:
        return False
    return start_window <= dt <= end_window


def _looks_like_event(text: str) -> bool:
    lowered = (text or "").lower()
    return any(hint in lowered for hint in EVENT_HINTS)


def _extract_links(url: str, fragment: str | None = None) -> set[str]:
    soup = _fetch_soup(url)
    links: set[str] = set()
    for link in soup.find_all("a", href=True):
        href = urljoin(url, str(link.get("href", "")))
        if not href.startswith("http"):
            continue
        if fragment and fragment not in href:
            continue
        links.add(href.rstrip("/"))
    return links


def _try_add_event(
    node,
    url: str,
    venue: str,
    address: str,
    distance: str,
    seen: set[str],
    start_window: datetime,
    end_window: datetime,
    always_relevant: bool,
    cost: str,
    default_category: str,
    link_substring: str | None = None,
) -> dict | None:
    link = node.find("a", href=True) if getattr(node, "name", None) != "a" else node
    if not link:
        return None

    href = urljoin(url, str(link.get("href", "")))
    if not href.startswith("http") or href in seen:
        return None
    if link_substring and link_substring not in href:
        return None

    text = " ".join(node.stripped_strings)
    if len(text) < 15:
        return None
    if not always_relevant and not _is_family(text):
        return None

    title_el = node.find(["h1", "h2", "h3", "h4"]) if getattr(node, "name", None) != "a" else None
    title = (title_el or link).get_text(" ", strip=True) if (title_el or link) else "Family event"
    if not title or len(title) < 3:
        return None
    if any(x in title.lower() for x in NAV_JUNK):
        return None

    date_iso = _find_date(text)
    if not _within_window(date_iso, start_window, end_window):
        return None

    seen.add(href)
    return _make_event(
        venue=venue,
        title=title,
        description=text,
        start=date_iso,
        url=href,
        address=address,
        distance=distance,
        cost=cost,
        category=default_category,
    )


def _generic_card_scrape(
    url: str,
    venue: str,
    address: str,
    distance: str,
    always_relevant: bool = False,
    selectors: list[str] | None = None,
    cost: str = "Check venue",
    default_category: str = "Farms & Animals",
    link_substring: str | None = None,
) -> list[dict]:
    soup = _fetch_soup(url)
    events: list[dict] = []
    seen: set[str] = set()
    start_window, end_window = _get_window()

    exact_selectors = selectors or [
        "article", ".card", ".event-card", ".event-item", ".event-listing",
        ".listing-item", ".grid-item", ".teaser", ".promo", ".event",
        ".listing", ".result-item", "[data-event]",
    ]
    all_selectors = exact_selectors if selectors else exact_selectors + [
        "[class*=card]", "[class*=event]", "[class*=listing]",
        "[class*=teaser]", "[class*=promo]", "[class*=result]",
    ]

    for sel in all_selectors:
        for node in soup.select(sel):
            event = _try_add_event(
                node=node,
                url=url,
                venue=venue,
                address=address,
                distance=distance,
                seen=seen,
                start_window=start_window,
                end_window=end_window,
                always_relevant=always_relevant,
                cost=cost,
                default_category=default_category,
                link_substring=link_substring,
            )
            if event:
                events.append(event)

    if not events and not selectors:
        for link in soup.find_all("a", href=True):
            container = link.parent if link.parent else link
            event = _try_add_event(
                node=container,
                url=url,
                venue=venue,
                address=address,
                distance=distance,
                seen=seen,
                start_window=start_window,
                end_window=end_window,
                always_relevant=always_relevant,
                cost=cost,
                default_category=default_category,
                link_substring=link_substring,
            )
            if event:
                events.append(event)

    return events


def _parse_wordpress_posts(
    cfg: dict,
    *,
    family_links: set[str] | None = None,
    always_relevant: bool = False,
) -> list[dict]:
    resp = requests.get(cfg["api_url"], timeout=30, headers=HEADERS)
    resp.raise_for_status()
    posts = resp.json()
    if not isinstance(posts, list):
        raise RuntimeError("Unexpected WordPress API response")

    events: list[dict] = []
    seen: set[str] = set()
    start_window, end_window = _get_window()
    family_urls = {link.rstrip("/") for link in (family_links or set())}

    for post in posts:
        title = _strip_html(post.get("title", {}).get("rendered"))
        content = _strip_html(post.get("content", {}).get("rendered"))
        excerpt = _strip_html(post.get("excerpt", {}).get("rendered"))
        link = str(post.get("link") or "").strip()
        if not title or not link or link in seen:
            continue

        description = excerpt or content or title
        combined = " ".join([title, description, content]).strip()
        in_family_links = link.rstrip("/") in family_urls
        if not always_relevant and not in_family_links and not _is_family(combined):
            continue

        date_iso = _find_date(combined)
        if not _within_window(date_iso, start_window, end_window):
            continue

        seen.add(link)
        events.append(_make_event(
            venue=cfg["name"],
            title=title,
            description=description or combined,
            start=date_iso,
            url=link,
            address=cfg["address"],
            distance=cfg["distance_from_e3"],
            cost=cfg.get("cost", "Check venue"),
            category=_infer_category(combined, cfg.get("default_category", "Farms & Animals")),
        ))

    return events


def _parse_rss_items(cfg: dict) -> list[dict]:
    resp = requests.get(cfg["feed_url"], timeout=30, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "xml")
    items = soup.find_all("item")
    events: list[dict] = []
    start_window, end_window = _get_window()

    for item in items:
        title = item.title.get_text(" ", strip=True) if item.title else ""
        description = _strip_html(item.description.get_text(" ", strip=True) if item.description else "")
        link = item.link.get_text(" ", strip=True) if item.link else cfg["url"]
        combined = " ".join([title, description])
        if not _is_family(combined):
            continue
        date_iso = _find_date(combined)
        if not _within_window(date_iso, start_window, end_window):
            continue
        events.append(_make_event(
            venue=cfg["name"],
            title=title,
            description=description or combined,
            start=date_iso,
            url=link,
            address=cfg["address"],
            distance=cfg["distance_from_e3"],
            cost=cfg.get("cost", "Check venue"),
            category=cfg.get("default_category", "Farms & Animals"),
        ))

    return events


def _scrape_garden_museum(cfg: dict) -> list[dict]:
    family_links = _extract_links(cfg["family_url"])
    events = _parse_wordpress_posts(cfg, family_links=family_links, always_relevant=False)
    if events:
        return events
    return _generic_card_scrape(
        url=cfg["family_url"],
        venue=cfg["name"],
        address=cfg["address"],
        distance=cfg["distance_from_e3"],
        always_relevant=True,
        cost=cfg["cost"],
        default_category=cfg["default_category"],
    )


def _scrape_hertfordshire_zoo(cfg: dict) -> list[dict]:
    events = _parse_wordpress_posts(cfg, always_relevant=False)
    archive_events = _generic_card_scrape(
        url=cfg["url"],
        venue=cfg["name"],
        address=cfg["address"],
        distance=cfg["distance_from_e3"],
        always_relevant=True,
        cost=cfg["cost"],
        default_category=cfg["default_category"],
    )
    seen = {(event["title"], event["start"], event["url"]) for event in events}
    for event in archive_events:
        key = (event["title"], event["start"], event["url"])
        if key not in seen:
            seen.add(key)
            events.append(event)
    if events:
        return events
    return _parse_rss_items(cfg)


def _scrape_omd_farm(cfg: dict) -> list[dict]:
    return _generic_card_scrape(
        url=cfg["url"],
        venue=cfg["name"],
        address=cfg["address"],
        distance=cfg["distance_from_e3"],
        always_relevant=True,
        cost=cfg["cost"],
        default_category=cfg["default_category"],
        link_substring="/special-events/",
    )


def _scrape_cedars_nature_centre(cfg: dict) -> list[dict]:
    resp = requests.get(cfg["sitemap_url"], timeout=30, headers=HEADERS)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)

    # Filter to recent event pages only (lastmod in last 12 months), cap at 50
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    cutoff = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    candidate_urls: list[str] = []
    for url_el in root.findall("ns:url", ns):
        loc_el = url_el.find("ns:loc", ns)
        lastmod_el = url_el.find("ns:lastmod", ns)
        page_url = (loc_el.text or "").strip() if loc_el is not None else ""
        if "/event-details/" not in page_url:
            continue
        lastmod = (lastmod_el.text or "").strip() if lastmod_el is not None else ""
        if lastmod and lastmod < cutoff:
            continue
        candidate_urls.append(page_url)
    candidate_urls = candidate_urls[:50]

    events: list[dict] = []
    start_window, end_window = _get_window()
    for page_url in candidate_urls:
        try:
            soup = _fetch_soup(page_url)
        except Exception:
            continue
        title_el = soup.find(["h1", "h2"])
        title = title_el.get_text(" ", strip=True) if title_el else "Cedars event"
        page_text = " ".join(soup.stripped_strings)

        time_section = ""
        about_section = ""
        match_time = re.search(r"Time\s*&\s*Location(.*?)(?:About the Event|Share This Event|Read More)", page_text, flags=re.IGNORECASE)
        if match_time:
            time_section = match_time.group(1).strip()
        match_about = re.search(r"About the Event(.*?)(?:Read More|Share This Event|Google Maps)", page_text, flags=re.IGNORECASE)
        if match_about:
            about_section = match_about.group(1).strip()

        description = " ".join(part for part in [time_section, about_section] if part).strip() or page_text
        combined = " ".join([title, description])
        date_iso = _find_date(time_section or combined)
        if not _within_window(date_iso, start_window, end_window):
            continue
        if not _is_family(combined):
            continue

        events.append(_make_event(
            venue=cfg["name"],
            title=title,
            description=description,
            start=date_iso,
            url=page_url,
            address=cfg["address"],
            distance=cfg["distance_from_e3"],
            cost=cfg["cost"],
            category=cfg["default_category"],
        ))

    return events


def _scrape_gtka(cfg: dict) -> list[dict]:
    events = _parse_wordpress_posts(cfg, always_relevant=False)
    if events:
        return events
    return _parse_rss_items(cfg)


def _scrape_exotic_explorers(cfg: dict) -> list[dict]:
    soup = _fetch_soup(cfg["url"])
    text = " ".join(soup.stripped_strings)
    date_iso = _find_date(text)
    start_window, end_window = _get_window()
    if date_iso and _within_window(date_iso, start_window, end_window) and _is_family(text):
        return [_make_event(
            venue=cfg["name"],
            title="Animal Encounters/Displays at Fetes & Events",
            description=text,
            start=date_iso,
            url=cfg["url"],
            address=cfg["address"],
            distance=cfg["distance_from_e3"],
            cost=cfg["cost"],
            category=cfg["default_category"],
        )]
    raise RuntimeError("No dated family events found on events page")


def _scrape_epping_forest(cfg: dict) -> list[dict]:
    soup = _fetch_soup(cfg["url"])
    events: list[dict] = []
    start_window, end_window = _get_window()

    for item in soup.select(".prodListItemWrapper"):
        center = item.select_one(".centerBlock")
        if not center:
            continue

        name_el = center.select_one(".ProductName")
        title = name_el.get_text(" ", strip=True) if name_el else ""
        if not title or len(title) < 5:
            continue

        link = item.select_one("a[href*='-p']")
        href = urljoin(cfg["url"], str(link.get("href", ""))) if link else cfg["url"]

        addr_el = center.select_one(".printOnly")
        address_text = ""
        if addr_el:
            raw = addr_el.get_text(" ", strip=True)
            m = re.match(r"Address\s+(.+?)(?:\s+Telephone|\s+\S+@)", raw)
            address_text = m.group(1).strip() if m else raw

        desc_el = center.select_one(".desc")
        description = desc_el.get_text(" ", strip=True) if desc_el else title

        dates_el = center.select_one(".dates")
        date_iso = None
        if dates_el:
            dates_text = dates_el.get_text(" ", strip=True)
            m = re.search(r"From:\s*(.+?)(?:\s+to\s|$)", dates_text)
            if m:
                date_iso = _normalise_date(m.group(1).strip())

        if not _within_window(date_iso, start_window, end_window):
            continue

        events.append(_make_event(
            venue=cfg["name"],
            title=title,
            description=description,
            start=date_iso,
            url=href,
            address=address_text or cfg["address"],
            distance=cfg["distance_from_e3"],
            cost=cfg["cost"],
            category=cfg["default_category"],
        ))

    return events


_SCRAPERS = {
    "garden_museum": _scrape_garden_museum,
    "hertfordshire_zoo": _scrape_hertfordshire_zoo,
    "omd_farm": _scrape_omd_farm,
    "cedars_nature_centre": _scrape_cedars_nature_centre,
    "gtka": _scrape_gtka,
    "exotic_explorers": _scrape_exotic_explorers,
    "epping_forest": _scrape_epping_forest,
}


def fetch_attraction_events() -> tuple[list[dict], list[str]]:
    all_events: list[dict] = []
    errors: list[str] = []

    for cfg in _ATTRACTION_SOURCES:
        scraper_key = cfg.get("scraper", "")
        scraper_fn = _SCRAPERS.get(scraper_key)
        if not scraper_fn:
            errors.append(f"{cfg['name']}: unknown scraper '{scraper_key}'")
            continue
        try:
            all_events.extend(scraper_fn(cfg))
        except Exception as exc:
            errors.append(f"{cfg['name']}: {exc}")

    return all_events, errors
