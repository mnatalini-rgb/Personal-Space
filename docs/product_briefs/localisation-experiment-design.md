# Localisation — Mission Copy Experiment Design

**Owner**: Moritz Natalini | **Date**: April 2026 | **Status**: Designing

---

## Objective

Validate that localising mission copy (titles, challenge descriptions, CTAs) into users' local language increases mission completion rate. This is a copy-only test — reward values, mission structure, and UX remain constant.

---

## Context

Current mission copy is primarily in English, with Russian versions for CIS markets. March 2026 data shows varying completion rates across geos, with language barriers potentially contributing to the ~40x drop-off between gaming and partner challenges.

**Key observations from March 2026:**

| Observation | Data |
|---|---|
| Tradeit EN gaming completion | 87.6% (678K joined → 597K completed) |
| Tradeit RU gaming completion | 92.4% (555K joined → 512K completed) |
| Tradeit EN partner (trade) completion | 2.4% (583K joined → 14K completed) |
| Tradeit RU partner (trade) completion | 1.7% (491K joined → 8K completed) |
| MENA / LATAM geos | English-only copy despite non-native English user base |

CIS missions running in Russian consistently outperform in gaming engagement. MENA and LATAM geos — significant Tradeit audiences — receive English-only copy. The inventory team meeting (March 2026) explicitly recommended "localise reward copy" as a growth lever for geo expansion.

**The partner challenge bottleneck is the critical question.** Gaming completion is high regardless of language (~88–92%). The hypothesis is that language friction disproportionately affects partner challenges, where precise comprehension of the required action matters more (e.g., "Link your account", "Trade any item", "Trade $250+").

---

## Hypothesis

Providing mission copy (titles, challenge descriptions, CTAs) in the user's local language will increase the **mission completion rate by ≥10% relative lift** in target locales, compared to English-only copy.

**Rationale**: Language friction adds cognitive load to mission comprehension. Users in non-English geos must interpret challenge requirements through a second language, which may reduce clarity on what's required and increase drop-off — particularly for partner conversion challenges where understanding the specific action ("Link your account", "Trade any item") matters.

---

## A/B Test Design

| Group | Treatment | Purpose |
|---|---|---|
| **A (Control)** | English-only mission copy | Baseline completion rates |
| **B (Variant)** | Localised mission copy in user's primary language | Test localisation impact on completion |

**Target geos for localisation (Phase 1):**

| Geo | Language | Rationale |
|---|---|---|
| MENA | Arabic | Large Tradeit audience, currently English-only |
| LATAM | Portuguese / Spanish | Tradeit expansion geos, English-only |

**CIS (Russian)** already has localised copy and serves as a positive reference benchmark — not part of the A/B test.

**Copy elements to localise:**
- Mission title
- Challenge descriptions (the action the user must complete)
- CTAs (e.g., "Link your account", "Start trading")
- Reward descriptions (name/label, not value)
- Progress and completion messages

**Held constant (NOT localised — same across groups):**
- Reward values and types
- Mission structure and challenge order
- UX layout and design
- Partner landing pages (out of FACEIT control)
- Trust modal copy (separate UX pattern)

---

## Open Decisions

1. **Which partner?** — Tradeit is ideal (most diverse geo footprint: NA, CIS, MENA, LATAM). Single partner reduces confounds.
2. **Which languages?** — Arabic (MENA) and Portuguese (LATAM) are highest-value candidates. Turkish could be Phase 2.
3. **Sample size & duration** — Need minimum detectable effect calculation for 10% relative lift on ~2% partner challenge completion rate. Likely need 50K+ users per group per geo.
4. **Translation quality** — Professional translation vs automated? Professional strongly recommended for Phase 1 — copy must be culturally appropriate, not just linguistically correct.
5. **User segmentation** — How do we assign users to language groups? Options: geo (IP-based), browser language setting, or FACEIT platform language setting. Recommend: FACEIT platform language setting where available, geo fallback.
6. **Timing** — Align with an upcoming Tradeit campaign (next monthly cycle).

---

## Metrics Framework

### Primary KPIs (must move or stay neutral)

| Metric | What it tells us |
|---|---|
| Mission completion rate (overall) | Did localisation increase full mission completion? |
| Partner challenge completion rate | Did localisation specifically help the conversion bottleneck? |
| Challenge-to-challenge progression rate | At which step does localisation have the biggest impact? |

### Guardrails (must NOT deteriorate)

| Metric | Owner | Threshold |
|---|---|---|
| Gaming challenge completion rate | Moritz / Data | Must remain ≥85% (currently ~90%) |
| Downstream conversion quality (C1/C2 among linked users) | Moritz / Data | Neutral or positive |
| Reward claim rate | Moritz / Data | Neutral or positive |
| User support ticket volume (localised geos) | Activation Ops | No significant increase |

### Observational (track, don't gate on)

| Metric | Notes |
|---|---|
| Time-to-completion per challenge | Does localisation speed up task completion? |
| Mission abandonment rate by step | Which challenge do localised users drop off at vs control? |
| AL completion rate by geo | Geo-specific signal for localisation impact on account linkage |
| Reward expiration rate | Does better comprehension reduce reward leakage? (Currently 7:1 expiration-to-claim ratio on Tradeit) |

---

## Dependencies

| Dependency | Owner | Status |
|---|---|---|
| Professional translation (Arabic, Portuguese/Spanish) | Activation Ops / External vendor | TBD |
| CMS support for multi-language mission copy per geo | Engineering | TBD — confirm if current CMS supports per-geo copy variants |
| Sample size calculation (MDE for 10% relative lift on ~2% base) | Data (Isabel / Kerrin) | TBD |
| Tradeit campaign alignment (monthly cycle) | Activation Ops | TBD |
| BQ / Mixpanel instrumentation for geo-language segmentation | Data | TBD |

---

## References

- March 2026 Mission Review: `docs/product_briefs/march-mission-review-2026.md`
- Inventory Team Meeting Prep (geo expansion notes): `docs/stakeholder_updates/inventory-team-meeting-prep-26mar.md`
- Brand Integrations Context: `context/brand-integrations.md`
- Experiments Log: `context/experiments.md`
