from __future__ import annotations

import requests

REQUEST_HEADERS = {"User-Agent": "family-events-aggregator/1.0", "Accept": "application/json"}
AREAS = ["east-london", "central-london"]
MAX_PAGES = 5


def _is_age_suitable(age_str: str) -> bool:
    lowered = (age_str or "").lower()
    if not lowered:
        return True
    suitable = [
        "all ages", "under 3", "under 5", "under 6", "under 8",
        "under 15", "under 17", "0-", "1-", "2-", "2+", "3+",
        "age 0", "age 1", "age 2", "age 3", "age 4", "age 5",
        "toddler", "baby", "family",
    ]
    if any(s in lowered for s in suitable):
        return True
    exclude = ["age 7-", "age 8-", "age 9-", "age 10", "age 11", "age 12", "adults"]
    if any(e in lowered for e in exclude):
        return False
    return True


def _map_category(cat: str) -> str:
    mapping = {
        "Museums & Galleries": "Museums & Learning",
        "Workshops & Classes": "Museums & Learning",
        "Sports & Adventure": "Sports & Swimming",
        "Indoor Play": "Soft Play & Indoor",
        "Outdoor Fun": "Outdoor & Parks",
        "Seasonal & Holiday": "Seasonal",
        "Animals & Nature": "Farms & Animals",
        "Theatre & Shows": "Theatre & Shows",
    }
    return mapping.get(cat, "Museums & Learning")


def fetch_kids_in_london_events() -> tuple[list[dict], list[str]]:
    out = []
    errors = []
    seen_urls = set()

    for area in AREAS:
        page = 1
        while page <= MAX_PAGES:
            url = f"https://kidsinlondon.com/api/activities?area={area}&page={page}"
            try:
                response = requests.get(url, timeout=20, headers=REQUEST_HEADERS)
                if response.status_code >= 400:
                    raise RuntimeError(f"HTTP {response.status_code}")
                data = response.json()
                items = data.get("data", [])
                if not items:
                    break
                for item in items:
                    item_url = item.get("url", "")
                    if item_url in seen_urls:
                        continue
                    seen_urls.add(item_url)

                    age_str = item.get("age", "")
                    if not _is_age_suitable(age_str):
                        continue

                    out.append({
                        "venue": item.get("venue") or "Kids In London",
                        "title": item.get("title", ""),
                        "description": item.get("summary", ""),
                        "start": None,
                        "end": None,
                        "url": item_url,
                        "address": item.get("area", "London"),
                        "distance": "Varies",
                        "age": age_str or "Family",
                        "cost": item.get("price", "Check venue"),
                        "category": _map_category(item.get("category", "")),
                        "source": "Kids In London",
                    })

                meta = data.get("meta", {})
                if page >= meta.get("last_page", 1):
                    break
                page += 1
            except Exception as exc:
                errors.append(f"Kids In London ({area} p{page}): {exc}")
                break

    return out, errors
