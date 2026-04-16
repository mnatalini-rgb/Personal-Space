from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path

STATE_RETENTION_DAYS = 90


def event_id(event: dict) -> str:
    seed = f"{event.get('venue','')}|{event.get('title','')}|{event.get('start','')}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def load_state(state_path: Path) -> dict:
    if not state_path.exists():
        return {"seen_event_ids": [], "seen_event_meta": {}, "last_run": None}
    try:
        content = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        return {"seen_event_ids": [], "seen_event_meta": {}, "last_run": None}
    content.setdefault("seen_event_ids", [])
    content.setdefault("seen_event_meta", {})
    content.setdefault("last_run", None)
    return content


def prune_state(content: dict) -> dict:
    cutoff = datetime.now() - timedelta(days=STATE_RETENTION_DAYS)
    meta = content.get("seen_event_meta", {})
    kept_ids = []
    kept_meta = {}
    for event_hash, iso_date in meta.items():
        try:
            dt = datetime.fromisoformat(iso_date)
        except Exception:
            continue
        if dt >= cutoff:
            kept_ids.append(event_hash)
            kept_meta[event_hash] = iso_date
    content["seen_event_ids"] = sorted(set(kept_ids))
    content["seen_event_meta"] = kept_meta
    return content


def split_new_events(events: list[dict], state_content: dict) -> tuple[list[dict], dict]:
    seen = set(state_content.get("seen_event_ids", []))
    seen_meta = dict(state_content.get("seen_event_meta", {}))

    for sid in seen:
        seen_meta.setdefault(sid, datetime.now().isoformat())

    new_events = []
    for event in events:
        eid = event_id(event)
        event["event_id"] = eid
        event["is_new"] = eid not in seen
        if event["is_new"]:
            new_events.append(event)
        seen.add(eid)
        seen_meta[eid] = datetime.now().isoformat()

    updated = {
        "seen_event_ids": sorted(seen),
        "seen_event_meta": seen_meta,
        "last_run": datetime.now().isoformat(),
    }
    updated = prune_state(updated)
    return new_events, updated


def save_state(state_path: Path, content: dict) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")
