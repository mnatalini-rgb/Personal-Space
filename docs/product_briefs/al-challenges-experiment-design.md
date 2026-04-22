# AL Challenges — Explicit vs Implicit Account Linkage Experiment Design

**Owner**: Moritz Natalini | **Date**: April 2026 | **Status**: Designing

---

## Objective

Validate that having an explicit Account Linkage (AL) challenge step in missions increases the AL completion rate compared to the current implicit model where AL happens silently at reward redemption.

---

## Context

FACEIT missions use two distinct AL models across partners:

**Explicit AL (Winline, WhiteMarket, PaySafe):**
- AL is a formal, visible challenge step in the mission (e.g., "Connect your Winline account").
- Users see it as a discrete task with its own reward.
- AL is tracked as a separate challenge completion in mission data.
- AL rate: 1.7% of users who completed gaming challenges (Winline, March 2026).

**Implicit AL (Tradeit):**
- AL is not a visible challenge. Users must link their account to claim any reward, but this happens at the redemption stage.
- A UI element on the mission page provides a CTA to link, but it's not tracked as a challenge completion.
- AL ≈ "Prizes Claimed" on first challenge as a proxy (slightly undercounts).
- AL is harder to measure directly because it's bundled with the reward claim action.

The two models have never been tested head-to-head. Partner-level comparisons are unreliable because Winline and Tradeit have fundamentally different partner economics, geos, and user segments. This experiment isolates the AL model variable.

**Relevant data:**

| Model | Partner | Gaming Completions | AL / Partner Action | Rate |
|---|---|---|---|---|
| Explicit AL | Winline (RU) | 366K | 4,741 AL | 1.3% of joined |
| Implicit AL | Tradeit (EN) | 597K | 14,198 trades (implies prior AL) | 2.4% of joined |

However, Tradeit's implicit model means AL and C1 (first trade) are conflated — users link AND act in the same flow. We cannot cleanly separate AL from C1 under the implicit model.

**Trust Modal finding (March 2026):** The trust modal during AL nearly doubles linkage-step completion (5.34% vs 2.75%). Trust signals are critical and must remain in both experiment groups.

---

## Hypothesis

Making Account Linkage an explicit, visible challenge step with its own reward will increase the **AL completion rate by ≥15% relative lift** compared to the current implicit (link-to-claim) model, because:

1. **Explicit framing signals value** — "Link your account" as a visible task signals that linking is worth doing and is a normal part of the experience.
2. **Dedicated reward reduces perceived cost** — A reward specifically for linking (e.g., 500 FP) makes the AL action feel rewarded, not just a gate to pass.
3. **Visible tasks get completed more** — Users are more likely to act on a visible, trackable task than an implicit pre-condition buried in the claim flow.
4. **Trust modal compounds the effect** — Explicit framing + trust modal together provide both motivation (reward) and confidence (trust signal).

---

## A/B Test Design

| Group | Treatment | Purpose |
|---|---|---|
| **A (Control)** | Implicit AL — current Tradeit model. AL happens via reward claim. CTA on mission page but no formal challenge step. | Baseline AL rate |
| **B (Variant)** | Explicit AL — "Link your Tradeit account" added as a formal challenge step with its own reward (FP). All other challenges unchanged. | Test explicit AL impact |

**Partner**: Tradeit — ideal because it currently uses implicit AL, so we're testing the addition of an explicit step.

**Target geos**: All Tradeit geos (NA, CIS, MENA) for adequate sample size.

**Variant setup details:**
- New challenge: "Link your FACEIT account to Tradeit"
- Position: After first gaming challenge (Play 1 match) and before first partner challenge (Trade any item)
- Reward for AL challenge: 500 FACEIT Points (matches existing Winline reward scale)
- Trust modal: Enabled for **both** groups (validated as beneficial — not a variable)
- All subsequent challenges remain identical between groups
- Mission structure comparison:

| Step | Control (Implicit) | Variant (Explicit) |
|---|---|---|
| 1 | Play 1 match | Play 1 match |
| 2 | Trade any item (AL implicit at claim) | **Link your Tradeit account** (new explicit step) |
| 3 | Trade $250+ | Trade any item |
| 4 | — | Trade $250+ |

---

## Open Decisions

1. **AL challenge position** — After first gaming challenge (recommended) or as the very first challenge? Placing it after a gaming warm-up leverages the engagement momentum from ~90% gaming completion.
2. **AL challenge reward value** — 500 FP (Winline precedent)? Higher to compensate for the additional step? Or test reward value as a secondary variable?
3. **Sample size & duration** — Need MDE calculation for 15% relative lift. Base rate for comparison is tricky — implicit AL isn't directly measured. Use proxy: first challenge completion rate where AL is required (~2.4%). Likely need 30K+ users per group.
4. **Measurement** — How to cleanly measure AL in the implicit (control) group? Options: (a) instrument AL events separately from challenge completion, (b) proxy via first reward claim, (c) use `user_account_linkage_operation_v1` Looker data. Recommend: (c) for clean measurement.
5. **Feature flag** — Need a new flag for Tradeit mission variant with explicit AL step. Engineering to confirm feasibility.
6. **Extra challenge impact** — Variant has 4 challenges vs control's 3. Does the extra step risk reducing overall mission completion? Track as guardrail.
7. **Tradeit approval** — Tradeit's position is that AL should remain a prerequisite, not a separate rewarded step (see March experiment design notes). Need partner alignment before launch.

---

## Metrics Framework

### Primary KPIs (must move)

| Metric | What it tells us |
|---|---|
| AL completion rate | Primary: does an explicit AL step increase linking? |
| AL-to-C1 progression rate | Do explicitly linked users convert to first trade at the same quality? |
| Total AL volume (absolute count) | Even if rate is similar, does visibility drive more attempts? |

### Guardrails (must NOT deteriorate)

| Metric | Owner | Threshold |
|---|---|---|
| Gaming challenge completion rate | Moritz / Data | Must remain ≥85% |
| Downstream conversion quality (Trade rate among linked users) | Moritz / Data | Neutral or positive |
| Mission abandonment rate (at AL step) | Moritz / Data | Variant abandonment must not exceed control by >5pp |
| Reward claim rate | Moritz / Data | Neutral or positive |
| Overall mission completion rate | Moritz / Data | Variant must not drop by >10% relative (extra step impact) |

### Observational (track, don't gate on)

| Metric | Notes |
|---|---|
| Time from mission activation to AL completion | Does explicit framing speed up AL? |
| AL step drop-off rate (variant only) | What % of users who see the explicit AL challenge abandon there? |
| Mission completion rate (full) | Does adding an extra challenge reduce full-mission completion? |
| Downstream partner value (C1/C2 conversion rates) | Quality check — explicit AL should maintain or improve conversion quality |
| Trust modal interaction rate | Are there differences in trust modal engagement between groups? |
| Reward expiration rate | Does explicit AL reduce reward leakage? |

---

## Dependencies

| Dependency | Owner | Status |
|---|---|---|
| Backend: support for optional AL challenge step per mission config | Engineering | TBD |
| Feature flag setup for Tradeit A/B | Engineering | TBD |
| Tradeit partner alignment (explicit AL may change campaign expectations) | Commercial / Partner | TBD |
| Sample size calculation (MDE for 15% lift on ~2.4% base) | Data (Isabel / Kerrin) | TBD |
| AL event instrumentation (separate from reward claim events) | Data / Engineering | TBD |
| Tradeit campaign cycle alignment | Activation Ops | TBD |

---

## References

- Trust Modal Conclusion: `docs/product_briefs/trust-modal-experiment-conclusion.md`
- Tradeit AL Model: `context/brand-integrations.md` (section: "Account Linkage model — unique to Tradeit")
- March 2026 Mission Review: `docs/product_briefs/march-mission-review-2026.md`
- Experiments Log: `context/experiments.md`
- Account Linkage Product Doc: `docs/product_documentation/Account Linakge for AI docs.md`
