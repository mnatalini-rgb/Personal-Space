# Localisation — Mission Copy Experiment Design

**Owner**: Moritz Natalini | **Date**: April 2026 | **Status**: Ready for implementation

---

## Objective

Validate that localising mission copy (titles, challenge descriptions, CTAs) into users' local language increases mission completion rate. This is a **copy-only test** — reward values, mission structure, and UX remain constant. No engineering required.

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

CIS missions running in Russian consistently outperform in gaming engagement (+4.8pp). MENA and LATAM geos — significant Tradeit audiences — receive English-only copy. The inventory team meeting (March 2026) explicitly recommended "localise reward copy" as a growth lever for geo expansion.

**The partner challenge bottleneck is the critical question.** Gaming completion is high regardless of language (~88–92%). The hypothesis is that language friction disproportionately affects partner challenges, where precise comprehension of the required action matters more (e.g., "Link your account", "Trade any item", "Trade $250+").

**A complication:** RU partner completion (1.7%) is actually *lower* than EN (2.4%) despite higher gaming completion. This may reflect audience differences (CIS users have different betting/trading behaviour) rather than language effects. The experiment controls for this by comparing before/after within the same geo, not across geos.

---

## Hypothesis

Providing mission copy (titles, challenge descriptions, CTAs) in the user's local language will increase the **partner challenge completion rate by ≥15% relative lift** in target geos, compared to English-only copy from the prior campaign cycle.

**Rationale**: Language friction adds cognitive load to mission comprehension. Users in non-English geos must interpret challenge requirements through a second language, which may reduce clarity on what's required — particularly for partner conversion challenges where understanding the specific action matters ("Link your account", "Trade any item", "Trade $250+").

---

## Decisions (all resolved)

| # | Decision | Resolution | Rationale |
|---|---|---|---|
| 1 | **Partner** | Tradeit | Most diverse geo footprint (EU, CIS, MENA, LATAM). Already runs 16 geo-specific campaign variants. Single partner reduces confounds. |
| 2 | **Languages** | Phase 1: Portuguese (Brazil/LATAM), Turkish (MENA). Phase 2: Arabic, Spanish. | Portuguese and Turkish cover the highest-volume non-English Tradeit geos. Arabic requires RTL support validation. |
| 3 | **Sample size** | ~53K users per geo minimum (see calculation below) | Detectable effect: 15% relative lift on ~2% base rate, 80% power, 95% confidence. |
| 4 | **Translation** | Professional translation, not automated | Copy must be culturally appropriate. Partner-specific terminology (trade, deposit) needs precise local phrasing. Budget via Activation Ops vendor. |
| 5 | **Split mechanism** | Geo-level before/after | Month 1 = English (baseline, already have historical data). Month 2 = localised copy. Compare MoM within the same geo, using non-test geos as a control reference for seasonality. |
| 6 | **Timing** | Next Tradeit monthly campaign cycle | Align with standard Tradeit campaign refresh. Translations must be ready before campaign setup. |

---

## Experiment Design

### Approach: Geo-level before/after with control reference

This is **not** a user-level A/B test. Campaigns are configured per geo with specific copy. We compare performance before and after localising, using unaffected geos as a seasonality control.

| Phase | Duration | Treatment Geos | Control Reference | What we measure |
|---|---|---|---|---|
| **Baseline** | Prior month (existing data) | EN-only copy in LATAM + MENA/Turkey | All other EN geos | Completion rates by challenge type |
| **Treatment** | 1 full campaign cycle (1 month) | Localised copy (PT-BR in LATAM, TR in Turkey) | Same EN geos (unchanged) | Completion rates by challenge type |

**Why this works:** Tradeit campaigns run monthly. We already have baseline data from previous EN-only months. The treatment is swapping copy in target geos. Non-test EN geos (EU, NA) serve as a seasonality control — if their rates stay flat while treatment geos move, the effect is attributable to localisation.

**Why not user-level A/B:** The mission system assigns campaigns per geo, not per user. Creating parallel EN + localised campaigns within the same geo is possible but would require engineering support for user-level bucketing. The geo-level approach ships immediately with zero engineering.

### Copy elements to localise

- Mission title
- Challenge descriptions (the action the user must complete)
- CTAs (e.g., "Link your account", "Start trading")
- Reward descriptions (name/label, not value)
- Progress and completion messages

### Held constant (NOT localised)

- Reward values and types
- Mission structure and challenge order
- UX layout and design
- Partner landing pages (out of FACEIT control)
- Trust modal copy (separate experiment)

---

## Sample Size & Power

**Parameters:**
- Base rate: 2% partner challenge completion (Tradeit EN, March 2026)
- Minimum detectable effect: 15% relative lift (2.0% → 2.3%)
- Significance: α = 0.05 (two-sided)
- Power: 1 − β = 0.80

**Calculation** (two-proportion z-test):

n = (Z_α/2 + Z_β)² × [p₁(1−p₁) + p₂(1−p₂)] / (p₂ − p₁)²
n = (1.96 + 0.84)² × [0.02 × 0.98 + 0.023 × 0.977] / (0.003)²
n = 7.84 × 0.04198 / 0.000009
n ≈ **36,571 per period**

**Interpretation:** We need ~37K users joining missions in each target geo per campaign cycle. Given Tradeit's March volumes (678K EN users total), this is feasible if LATAM and Turkey each contribute ≥37K users per month. 

**Pre-flight check required:** Run the geo-sizing query below to confirm per-geo volumes before committing to launch.

### Geo-sizing query (run before launch)

```sql
-- Tradeit mission joins by geo, last 3 months
-- Replace campaign IDs with current Tradeit campaign IDs
SELECT
  u.country_iso_code,
  COUNT(DISTINCT um.user_id) AS users_joined,
  COUNT(DISTINCT CASE WHEN um.type = 'partner' AND um.status = 'complete' THEN um.user_id END) AS partner_completions,
  SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN um.type = 'partner' AND um.status = 'complete' THEN um.user_id END),
    COUNT(DISTINCT um.user_id)
  ) AS partner_completion_rate
FROM `business-intelligence-prod.CampaignService.UserMissions` um
JOIN `business-intelligence-prod.CampaignService.Campaigns` c
  ON um.campaign_id = c._id
JOIN `business-intelligence-prod.dbt_user.dim__users` u
  ON um.user_id = u.user_id
WHERE LOWER(c.organizer.name) LIKE '%tradeit%'
  AND um.created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY u.country_iso_code
ORDER BY users_joined DESC
LIMIT 30
```

This tells us: (a) which geos have enough volume, (b) what the current per-geo partner completion rate is (our baseline), (c) whether our 37K minimum is achievable.

---

## Metrics Framework

### Primary KPIs (decision metrics)

| Metric | Baseline source | Success threshold |
|---|---|---|
| Partner challenge completion rate (per geo) | Prior month EN data for same geo | ≥15% relative lift vs baseline |
| Mission completion rate (overall, per geo) | Prior month EN data | Positive or neutral |
| Challenge-to-challenge progression rate | Prior month EN data | Identify which step benefits most from localisation |

### Guardrails (must NOT deteriorate)

| Metric | Threshold | Owner |
|---|---|---|
| Gaming challenge completion rate | Must remain ≥85% (currently ~90%) | Moritz |
| Downstream conversion quality (C1/C2 among linked users) | Neutral or positive | Moritz |
| Reward claim rate | Neutral or positive | Moritz |
| User support ticket volume (localised geos) | No significant increase | Activation Ops |

### Observational (track, don't gate on)

| Metric | What it tells us |
|---|---|
| Time-to-completion per challenge | Does localisation speed up task completion? |
| Mission abandonment rate by step | Which challenge do localised users drop off at vs baseline? |
| AL completion rate by geo | Geo-specific signal for localisation impact on account linkage |
| Reward expiration rate | Does better comprehension reduce reward leakage? (Currently 7:1 on Tradeit) |
| Gaming completion rate delta (localised vs EN) | Isolates language effect on easy tasks vs hard tasks |

---

## Implementation Scope

### Engineering: None required

Campaigns are already configured per geo with specific copy. Localisation is a campaign configuration change, not a code change. No new instrumentation needed — existing BQ tables (`UserMissions`, `Campaigns`, `dim__users.country_iso_code`) already support geo-level analysis.

### Activation Ops: Primary owner

| Task | Detail | Effort |
|---|---|---|
| Commission translations | Send copy brief to translation vendor. Include: mission titles, challenge descriptions, CTAs, reward labels. Context: gaming/esports, partner is Tradeit (skin trading platform). | 1 week lead time |
| Review translations | QA translated copy with native speakers if available internally. Verify partner-specific terms (e.g., "trade" in Portuguese = "trocar" or "negociar"?) | 2–3 days |
| Create localised campaign variants | Duplicate existing EN campaign configs for target geos. Replace copy with translated versions. Same rewards, same structure, same targeting. | 1 day per geo |
| Launch + monitor | Launch localised campaigns at the start of the next monthly cycle. Monitor for first 48h (no anomalies in join rates or errors). | Ongoing |

### Commercial: Notification only

- Inform Tradeit that we're localising mission copy in select geos. No partner action required — copy changes are on FACEIT side. Tradeit partner landing pages remain unchanged (out of scope).

### Moritz: Analysis

- Run geo-sizing query pre-launch to confirm volume
- Pull baseline data from prior month
- Run comparison analysis at end of campaign cycle
- Write experiment conclusion

---

## Timeline

| Week | Action | Owner |
|---|---|---|
| **W1** | Run geo-sizing query, confirm target geos have ≥37K users/month | Moritz |
| **W1** | Send copy brief to translation vendor (PT-BR, Turkish) | Activation Ops |
| **W2** | Receive translations, QA review | Activation Ops |
| **W2** | Pull baseline data for target geos from current/prior month | Moritz |
| **W3** | Create localised campaign variants in mission config | Activation Ops |
| **W3** | Notify Tradeit (Commercial) | Commercial |
| **W3–W4** | Campaign start of month: launch localised campaigns | Activation Ops |
| **W7** | Campaign end: pull results | Moritz |
| **W8** | Analysis + experiment conclusion write-up | Moritz |

**Total time to launch: ~3 weeks** (1 week translation, 1 week QA + baseline, 1 week campaign setup). Then 1 full campaign cycle (4 weeks) to collect data.

---

## Rollback Plan

If localised campaigns show:
- **Gaming completion drops >5pp** vs baseline → Revert to EN copy immediately (same-day campaign swap)
- **Partner completion drops >20% relative** vs baseline → Revert to EN copy
- **Support ticket spike** in localised geos → Revert and investigate translation quality

Rollback is instant: Activation Ops swaps campaign copy back to EN. No engineering rollback needed.

---

## Success Criteria

| Outcome | Verdict | Next step |
|---|---|---|
| Partner completion ≥15% relative lift, guardrails pass | **Ship** | Roll out to all non-EN geos. Add Arabic, Spanish in Phase 2. |
| Partner completion 5–15% lift, guardrails pass | **Promising** | Extend to 1 more campaign cycle for confidence. Consider Phase 2 languages. |
| Partner completion <5% lift or neutral | **Inconclusive** | Review translation quality. Consider user-level A/B for higher sensitivity. |
| Any guardrail fails | **Revert** | Revert to EN. Investigate root cause before retry. |

---

## Risks

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| Translation quality is poor / culturally inappropriate | Negative user experience, lower completion | Medium | Professional translation + native speaker QA. Don't use automated translation. |
| Target geos have insufficient volume (<37K users) | Can't reach statistical significance in one cycle | Medium | Run geo-sizing query first. If volume is low, extend to 2 campaign cycles or add more geos. |
| Seasonality confounds the before/after comparison | False positive or false negative | Medium | Use non-test EN geos as a seasonality control. If control geos also move ±X%, adjust the treatment effect. |
| Partner landing page remains in English, breaking the experience | Users click localised CTA but land on EN page — jarring | High | Out of scope for Phase 1. Note in conclusion if this limits the measured effect. Could be even bigger with end-to-end localisation. |
| RTL layout issues with Arabic copy | Broken UI in Arabic geos | Low | Phase 1 skips Arabic — starts with PT-BR and Turkish (both LTR). Arabic is Phase 2 after RTL validation. |

---

## References

- March 2026 Mission Review: `docs/product_briefs/march-mission-review-2026.md`
- Inventory Team Meeting Prep (geo expansion notes): `docs/stakeholder_updates/inventory-team-meeting-prep-26mar.md`
- Brand Integrations Context: `context/brand-integrations.md`
- Experiments Log: `context/experiments.md`
- Mission Conversion Pathways PRD: `docs/product_briefs/nonlinear-missions-prd.md` (Section 2a data)
