from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module(module_name: str, module_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load module: {module_name}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _dedupe(events: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for event in events:
        key = (
            (event.get("venue") or "").strip().lower(),
            (event.get("title") or "").strip().lower(),
            (event.get("start") or ""),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(event)
    return out


def _count_by_source(events: list[dict]) -> dict:
    counts = {}
    for event in events:
        key = event.get("source") or "Unknown"
        counts[key] = counts.get(key, 0) + 1
    return counts


def run() -> int:
    project_dir = Path(__file__).resolve().parent
    root = project_dir.parent

    config = _load_module("config", project_dir / "config.py")
    report = _load_module("report", project_dir / "report.py")
    state = _load_module("state", project_dir / "state.py")
    spektrix = _load_module("sources_spektrix", project_dir / "sources" / "spektrix.py")
    openactive = _load_module("sources_openactive", project_dir / "sources" / "openactive.py")
    rss_ical = _load_module("sources_rss_ical", project_dir / "sources" / "rss_ical.py")
    tower_hamlets = _load_module(
        "sources_tower_hamlets", project_dir / "sources" / "tower_hamlets.py"
    )
    static_mod = _load_module("sources_static", project_dir / "sources" / "static.py")
    kids_london = _load_module("sources_kids_london", project_dir / "sources" / "kids_in_london.py")
    lfb = _load_module("sources_lfb", project_dir / "sources" / "lfb.py")

    state_path = root / "family-events" / "data" / "state.json"
    report_path = root / "family-events-report.html"

    failed_sources = []
    all_events = []

    spektrix_events, spektrix_errors = spektrix.fetch_spektrix_events(config.SPEKTRIX_CLIENTS)
    all_events.extend(spektrix_events)
    failed_sources.extend(spektrix_errors)

    openactive_events, openactive_errors = openactive.fetch_openactive_events(
        config.OPENACTIVE_ENDPOINTS, config.OPENACTIVE_VENUE_KEYWORDS
    )
    all_events.extend(openactive_events)
    failed_sources.extend(openactive_errors)

    feed_events, feed_errors = rss_ical.fetch_rss_ical_events(
        config.RSS_FEEDS, config.LONDON_AQUATICS_JSON
    )
    all_events.extend(feed_events)
    failed_sources.extend(feed_errors)

    tower_events, tower_errors = tower_hamlets.fetch_tower_hamlets_events()
    all_events.extend(tower_events)
    failed_sources.extend(tower_errors)

    kids_events, kids_errors = kids_london.fetch_kids_in_london_events()
    all_events.extend(kids_events)
    failed_sources.extend(kids_errors)

    lfb_events, lfb_errors = lfb.fetch_lfb_events()
    all_events.extend(lfb_events)
    failed_sources.extend(lfb_errors)

    all_events = _dedupe(all_events)

    state_content = state.load_state(state_path)
    _, updated_state = state.split_new_events(all_events, state_content)

    static_events = static_mod.get_static_events()
    start, end = config.get_window_range()
    report.build_html_report(
        events=all_events,
        static_events=static_events,
        output_path=report_path,
        start_range=start,
        end_range=end,
        failed_sources=failed_sources,
    )

    state.save_state(state_path, updated_state)
    print(f"Generated report: {report_path}")
    print(f"Events collected: {len(all_events)}")
    source_counts = _count_by_source(all_events)
    print("Events per source:")
    for source_name in sorted(source_counts.keys()):
        print(f" - {source_name}: {source_counts[source_name]}")
    if failed_sources:
        print("Some sources failed:")
        for err in failed_sources:
            print(f" - {err}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
