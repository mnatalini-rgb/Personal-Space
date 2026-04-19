from __future__ import annotations

from datetime import datetime, timedelta

WINDOW_DAYS = 120
STATE_RETENTION_DAYS = 90

TARGET_AGES = [2, 5]

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

EXCLUDE_KEYWORDS = [
    "18+",
    "adults only",
    "over 16",
]

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

SPEKTRIX_CLIENTS = [
    {
        "name": "Unicorn Theatre",
        "client_candidates": ["unicorntheatre"],
        "always_relevant": True,
        "website": "https://www.unicorntheatre.com/",
        "category": "Theatre & Shows",
        "address": "147 Tooley St, London SE1 2HZ",
        "distance_from_e3": "~35 mins",
    },
    {
        "name": "Little Angel Theatre",
        "client_candidates": ["littleangeltheatre"],
        "always_relevant": True,
        "website": "https://littleangeltheatre.com/",
        "category": "Theatre & Shows",
        "address": "14 Dagmar Passage, London N1 2DN",
        "distance_from_e3": "~40 mins",
    },
    {
        "name": "Barbican Centre",
        "client_candidates": ["barbicancentre"],
        "always_relevant": False,
        "website": "https://www.barbican.org.uk/",
        "category": "Theatre & Shows",
        "address": "Silk St, Barbican, London EC2Y 8DS",
        "distance_from_e3": "~28 mins",
    },
    {
        "name": "Discover Story Centre",
        "client_candidates": ["discover"],
        "always_relevant": True,
        "website": "https://discover.org.uk/",
        "category": "Museums & Learning",
        "address": "383-387 High St, London E15 4QZ",
        "distance_from_e3": "~28 mins",
    },
]

OPENACTIVE_ENDPOINTS = [
    "https://better-admin.org.uk/api/openactive/better/session-series",
    "https://better-admin.org.uk/api/openactive/better/scheduled-sessions",
]

OPENACTIVE_VENUE_KEYWORDS = [
    "mile end",
    "britannia leisure centre",
    "london aquatics centre",
    "lee valley riding centre",
]

RSS_FEEDS = [
    {
        "name": "British Library",
        "type": "rss",
        "url": "https://events.bl.uk/feed.rss",
        "category": "Museums & Learning",
        "address": "96 Euston Rd, London NW1 2DB",
        "distance_from_e3": "~42 mins",
    },
    {
        "name": "Water & Steam Museum",
        "type": "rss",
        "url": "https://waterandsteam.org.uk/events/feed/",
        "category": "Museums & Learning",
        "address": "Green Dragon Ln, Brentford TW8 0EN",
        "distance_from_e3": "~70 mins",
    },
    {
        "name": "Tower Hamlets Council Events",
        "type": "rss",
        "url": "https://www.towerhamlets.gov.uk/News_events/Events/Events.aspx?Calendar_List_SyndicationType=1",
        "category": "Outdoor & Parks",
        "address": "Tower Hamlets",
        "distance_from_e3": "Local",
    },
    {
        "name": "Victoria Park (Tower Hamlets)",
        "type": "rss",
        "url": "https://www.towerhamlets.gov.uk/News_events/Events/Events.aspx?TaxonomyKey=0/1/18/19/193",
        "category": "Outdoor & Parks",
        "address": "Victoria Park, London E3",
        "distance_from_e3": "Local",
    },

]

LONDON_AQUATICS_JSON = {
    "name": "London Aquatics Centre",
    "url": "https://londonaquaticscentre.org/wp-json/tribe/events/v1/events",
    "category": "Sports & Swimming",
    "address": "Queen Elizabeth Olympic Park, London E20 2ZQ",
    "distance_from_e3": "~18 mins",
}

IDEA_STORE_LOCATIONS = ["Bow", "Whitechapel", "Canary Wharf", "Chrisp Street"]

MUSEUM_SOURCES = [
    {
        "scraper": "nhm",
        "name": "Natural History Museum",
        "url": "https://www.nhm.ac.uk/whats-on.html",
        "address": "Cromwell Road, London SW7 5BD",
        "distance_from_e3": "~50 mins",
        "always_relevant": False,
    },
    {
        "scraper": "bank_of_england",
        "name": "Bank of England Museum",
        "url": "https://www.bankofengland.co.uk/museum/whats-on",
        "address": "Bartholomew Lane, London EC2R 8AH",
        "distance_from_e3": "~25 mins",
        "always_relevant": False,
    },
    {
        "scraper": "science_museum",
        "name": "Science Museum",
        "url": "https://www.sciencemuseum.org.uk/see-and-do?type=events",
        "address": "Exhibition Road, London SW7 2DD",
        "distance_from_e3": "~50 mins",
        "always_relevant": False,
    },
    {
        "scraper": "lt_museum",
        "name": "London Transport Museum",
        "url": "https://www.ltmuseum.co.uk/whats-on",
        "address": "Covent Garden Piazza, London WC2E 7BB",
        "distance_from_e3": "~35 mins",
        "always_relevant": False,
    },
    {
        "scraper": "southbank",
        "name": "Southbank Centre",
        "url": "https://www.southbankcentre.co.uk/whats-on/?artform-filter=family-young-people",
        "address": "Belvedere Road, London SE1 8XX",
        "distance_from_e3": "~35 mins",
        "always_relevant": True,
    },
    {
        "scraper": "british_museum",
        "name": "British Museum",
        "url": "https://www.britishmuseum.org/visit/family-visits",
        "address": "Great Russell St, London WC1B 3DG",
        "distance_from_e3": "~35 mins",
        "always_relevant": True,
    },
    {
        "scraper": "national_gallery",
        "name": "National Gallery",
        "url": "https://www.nationalgallery.org.uk/events?audience=families",
        "address": "Trafalgar Square, London WC2N 5DN",
        "distance_from_e3": "~35 mins",
        "always_relevant": False,
    },
    {
        "scraper": "tate",
        "name": "Tate",
        "url": "https://www.tate.org.uk/whats-on?type=families_and_children",
        "urls": [
            "https://www.tate.org.uk/whats-on?type=families_and_children&gallery_group=tate-modern",
            "https://www.tate.org.uk/whats-on?type=families_and_children&gallery_group=tate-britain",
        ],
        "address": "Bankside / Millbank, London",
        "distance_from_e3": "~30 mins",
        "always_relevant": True,
    },
    {
        "scraper": "halfmoon",
        "name": "Half Moon Theatre",
        "url": "https://www.halfmoon.org.uk/whats-on/",
        "address": "43 White Horse Rd, London E1 0ND",
        "distance_from_e3": "~15 mins",
        "always_relevant": True,
    },
]


def get_window_range() -> tuple[datetime, datetime]:
    start = datetime.now()
    end = start + timedelta(days=WINDOW_DAYS)
    return start, end


def as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        parts = [str(v) for v in value.values() if v]
        return " ".join(parts)
    if isinstance(value, list):
        parts = [as_text(item) for item in value]
        return " ".join([p for p in parts if p])
    return str(value)


def is_family_relevant(text: str) -> bool:
    lowered = (text or "").lower()
    if not lowered.strip():
        return False
    if any(ex in lowered for ex in EXCLUDE_KEYWORDS):
        return False
    if "teen" in lowered and "and teen" not in lowered and "teens" in lowered:
        return False
    return any(keyword in lowered for keyword in KIDS_KEYWORDS)


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
