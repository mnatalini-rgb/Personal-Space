# Hardware Ad Targeting — Storage & Scoping One-Pager

**Owner:** Moritz Natalini · Ads & Partnerships
**Engineer:** Egor
**Sprint:** Next (Q2 2026)
**Status:** Scoping
**Dependencies:** Legal sign-off (LEGD-8214), Peripheral data collection (live)

---

## Problem

We collect hardware telemetry from 193K+ unique users across 152 countries via the FACEIT Client — but this data only lives in raw CSV exports and internal dashboards. It cannot be used for ad targeting, audience segmentation, or partner reporting because:

1. **No structured storage** — raw CSVs in BQ exports, not a normalised serving table
2. **No ad-system integration** — no pipeline to surface hardware segments to GAM, Prebid, or direct sales
3. **No consent gating** — Legal (LEGD-8214) has not yet confirmed whether advertising use requires separate opt-in

Endemic hardware brands (Logitech, Razer, SteelSeries, Corsair) want to reach esports audiences based on what they own — and what they don't (conquest). We can't serve this today.

---

## Goal

Build a normalised hardware data layer that enables ad targeting by peripheral brand, CPU vendor, and hardware profile — gated on user consent and Legal approval.

### Success Metrics
- Normalised hardware table populated for all released countries (IN, TR, IT, Tier 3)
- ≥5 audience segments queryable (brand-owner, conquest, CPU vendor, gaming-grade, core-count)
- Ad-system export spec ready for GAM key-value injection or Prebid bidder params
- Consent flag implemented — no data exported without `advertising_use_allowed = true`

---

## What Already Exists

| Asset | Location | What It Does |
|---|---|---|
| Raw hardware CSVs | `data/brand_integrations/faceit-events user_client_hardware_details_v2 *.csv` | ~1.4M rows, weekly exports: CPU, cores, peripheral brand, OEM, device type, user_id, country |
| ETL + normalisation script | `scripts/aggregate_peripheral_csv.py` | `normalize_brand()`, `normalize_mobo()`, `extract_cpu_brand()`, `is_gaming_brand()`, `GAMING_BRANDS` set, country tier classification |
| Aggregated JSON | `scripts/peripheral_dashboard_data.json`, `peripheral_aggregated.json` | Per-country metrics: unique systems, CPU splits, brand counts, gaming penetration |
| Peripheral dashboard | `analysis/peripheral-data-dashboard.html` | Visualises collected hardware data by country, brand, tier |
| CDP exports | `data/brand_integrations/faceit_snowflake_analytics rep__cdp_service__user_events *.csv` | User-level event data from Snowflake — joinable on user_id |
| Legal ticket | `docs/legal-ticket-hardware-data-compliance.md` | LEGD-8214 — 14 questions for Legal on consent, GDPR, ePrivacy, profiling |

### Data Points Collected (via FACEIT Client, 1x/week)

| Field | Example | Fill Rate |
|---|---|---|
| CPU Make & Model | Intel Core i5-12500H | ~100% |
| CPU Cores | 12 | ~100% |
| Motherboard / OEM | ASUS, Lenovo, Monster | ~100% |
| Peripheral Brand | Logitech, Razer, SteelSeries | ~85% |
| Peripheral Type | Mouse, Keyboard | ~100% |
| Country | TR, IN, IT, DE, FR | ~100% |

---

## Proposed Solution

### Phase 1 — Normalised Storage (Week 1-2)

Build a serving table in BigQuery (or Snowflake) with one row per user, updated weekly.

**Proposed schema:**

```
user_id                     STRING    -- FACEIT user ID (join key to CDP)
cpu_vendor                  STRING    -- AMD / Intel / Unknown
cpu_cores_bucket            STRING    -- 4 / 6 / 8 / 12 / 16 / 20+
mobo_brand                  STRING    -- Normalised OEM (ASUS, Lenovo, Dell, Monster...)
peripheral_brands           ARRAY     -- Normalised peripheral brands [{brand, device_type}]
owns_logitech               BOOLEAN   -- Convenience flag
owns_razer                  BOOLEAN   -- Convenience flag
owns_steelseries            BOOLEAN   -- Convenience flag
gaming_peripheral_flag      BOOLEAN   -- Any peripheral in GAMING_BRANDS set
country                     STRING    -- ISO country code
last_collected_at           TIMESTAMP -- Most recent hardware scan
advertising_use_allowed     BOOLEAN   -- Consent flag (default FALSE until Legal confirms)
```

**Normalisation rules:** Reuse `normalize_brand()`, `normalize_mobo()`, `extract_cpu_brand()` from `scripts/aggregate_peripheral_csv.py`. Deduplicate per user — keep most recent scan per week.

### Phase 2 — Audience Primitives (Week 2-3)

Define queryable audience segments:

| Segment | Logic | Use Case |
|---|---|---|
| `owns_brand_X` | `peripheral_brands` contains brand X | "Show ad to Logitech users" |
| `not_owns_brand_X` | `peripheral_brands` does NOT contain brand X | Conquest targeting for Razer |
| `cpu_vendor_intel` / `cpu_vendor_amd` | `cpu_vendor = 'Intel'` / `'AMD'` | Intel campaign targeting |
| `gaming_grade` | `gaming_peripheral_flag = true` | Premium hardware audience |
| `core_count_high` | `cpu_cores_bucket IN ('16', '20+')` | Performance/enthusiast segment |
| `budget_setup` | `gaming_peripheral_flag = false AND cpu_cores_bucket IN ('4', '6')` | Budget hardware audience |

### Phase 3 — Ad System Integration (Week 3-4, gated on Legal)

Surface segments to ad delivery. Two options (decide with AdOps):

**Option A — Client-side key-values (fast, lower privacy bar)**
- Inject `googletag.pubads().setTargeting('hw_brand', 'logitech')` on page load
- Requires frontend repo changes (where Fuse.js / Prebid loads)
- Exposes attributes client-side — review with Legal

**Option B — Server-side audiences (preferred, privacy-safe)**
- Create GAM audience lists from BQ serving table
- Upload via GAM API or manual CSV import
- Data never leaves FACEIT systems — only audience membership is used for ad selection
- Requires AdOps setup in GAM console

---

## Scope

### In Scope
- Normalised BigQuery/Snowflake table + weekly ETL job
- Audience segment definitions + sizing queries
- Consent flag column + integration point for consent store
- Ad-system export spec (GAM key-values or audience lists)
- Documentation for AdOps handoff

### Out of Scope
- Legal/Privacy policy changes (owned by Legal — LEGD-8214)
- Frontend ad tag changes (owned by frontend team, separate ticket)
- Advertiser pricing or sales packaging
- Hardware data collection changes (already stable at 1x/week)

---

## Dependencies & Risks

| Dependency | Owner | Status | Risk |
|---|---|---|---|
| Legal sign-off (LEGD-8214) | Legal / Privacy | 🟡 Open — submitted 26 Mar | **Blocker** for Phase 3. Phase 1-2 can proceed (internal only) |
| Consent store integration | Platform team | ❓ TBD | Need `advertising_use_allowed` flag joinable by user_id |
| Frontend ad tag access | Frontend / AdOps | ❓ TBD | Required only for Option A (client-side key-values) |
| GAM admin access | AdOps | ❓ TBD | Required only for Option B (server-side audiences) |

**Key risk:** Legal may require explicit opt-in for advertising use. If so, initial audience sizes will be small until consent adoption grows. Mitigate by launching internal-only (Phase 1-2) while consent flow is built.

---

## Rollout Plan

| Phase | What | When | Gated On |
|---|---|---|---|
| Phase 1 | Normalised storage table + ETL | Sprint 1 (Week 1-2) | Nothing — can start immediately |
| Phase 2 | Audience primitives + sizing | Sprint 1 (Week 2-3) | Phase 1 complete |
| Phase 3 | Ad-system integration | Sprint 2 | Legal sign-off (LEGD-8214) + consent flag |
| Pilot | Single partner test (TR or IN) | Sprint 2-3 | Phase 3 + partner agreement |

---

## Reference Materials

- **Peripherals product brief:** `docs/product_briefs/Peripherals Initiatives.md`
- **Legal ticket:** `docs/legal-ticket-hardware-data-compliance.md`
- **ETL script:** `scripts/aggregate_peripheral_csv.py`
- **Peripheral dashboard:** `analysis/peripheral-data-dashboard.html`
- **CDP docs:** `docs/product_documentation/CDP for AI docs.md`
- **Ad context:** `context/advertising.md`
- **Aggregated data:** `scripts/peripheral_dashboard_data.json`

---

## Open Questions

1. **BigQuery or Snowflake?** — Where does the normalised table live? (CDP exports are in Snowflake, but BQ has the raw hardware CSVs)
2. **Consent UX** — What does the opt-in flow look like? Client setting? Web preference centre? Need design input.
3. **Minimum audience threshold** — What's the minimum segment size before we expose it to advertisers? (Suggest ≥5K unique users per country)
4. **GAM or Prebid?** — Which ad-system path does AdOps prefer for first integration?
5. **Refresh cadence** — Weekly ETL matches collection cadence. Is that sufficient for ad targeting, or do advertisers expect real-time?

---

## Updates

- **2026-03-30 15:30** — One-pager created. Egor assigned for next sprint scoping. Legal ticket LEGD-8214 open, gating Phase 3.
