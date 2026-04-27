# CMP Optimisation — Non-TCF Geo Experiment Design

**Owner**: Moritz Natalini | **Date**: April 2026 | **Status**: In setup — awaiting Teo confirmation on key-value implementation

---

## Objective

Validate that replacing the TCF 2.2-compliant CMP with Publift's **NoCMP Fuse flavour** in non-GDPR geos increases ad revenue (RPV / eCPM), by removing unnecessary consent friction that suppresses programmatic fill and targeting.

---

## Context

FACEIT currently deploys the same TCF 2.2 CMP (via Publift/Fuse) **globally** — including geos where GDPR does not apply. The TCF consent wall adds user friction and reduces the share of users who grant full ad consent. In non-EEA markets, this consent enforcement is not legally required and may be actively suppressing:

- **Consent rate** → fewer users consenting → less targetable inventory
- **Fill rate** → lower bid density from DSPs that require consent signals
- **eCPM** → reduced competition for non-consented impressions

**Publift YTD 2026 baseline** (Jan – Apr):

| Region | YTD Revenue | YTD Impressions | eCPM | % of Total |
|---|---|---|---|---|
| EEA (GDPR applies) | $66,217 | 591M | $0.11 | 43.8% |
| Non-EEA | $85,102 | 760M | $0.11 | 56.2% |
| **Total** | **$151,319** | **1.35B** | **$0.11** | 100% |

Non-EEA represents 56% of revenue. Even a modest RPV uplift in these geos has meaningful impact at scale.

**Publift's recommendation:** Use the **NoCMP flavour of Fuse** outside GDPR regions. When NoCMP is enabled, two versions of fuse.js run:
- **Within EEA:** Fuse checks for CMP/consent signals (no change)
- **Outside EEA:** Fuse does not check or enforce any CMP logic

---

## Hypothesis

Replacing the TCF 2.2 CMP with Publift's NoCMP Fuse variant in non-GDPR geos will increase **RPV by ≥15%** by improving consent signal quality, fill rate, and eCPM — without any legal compliance risk.

**Rationale:** TCF consent walls in non-GDPR markets add friction with no legal benefit. Users who dismiss or reject the consent prompt become non-consented impressions — worth significantly less in programmatic auctions. Removing the wall means all users are treated as consentable by default, increasing targetable inventory and bid competition.

---

## Experiment Design

### Approach: User-level A/B test with GAM key-value tracking

| | Control | Variant |
|---|---|---|
| **CMP** | Current TCF 2.2 CMP (Fuse standard) | NoCMP Fuse flavour (no consent wall) |
| **Geos** | 7 non-EEA geos (see below) | Same 7 geos |
| **Split** | 50% of traffic | 50% of traffic |
| **Key-value in GAM** | `cmp_test=control` | `cmp_test=variant` |
| **Duration** | 3–4 weeks (targeting 2 weeks minimum for significance) | |

### Split mechanism

FACEIT front-end assigns users to experiment groups and:
1. Sets a **GAM key-value** (`cmp_test=control` or `cmp_test=variant`) to track revenue by group in Ad Manager
2. Sets a **GA parameter** to track page views by group in Google Analytics

RPV is computed by combining GAM revenue (by key-value) with GA page views (by experiment group).

> **Open question for Teo:** Can our experiment tool (Fugly) pass a key-value to GAM via the ad tag? If yes, this is the simplest setup. If not, we implement custom logic on the page to set the key-value based on experiment assignment.

> **Open question for Teo:** Can we pass Publift's UUID into our experiment bucketing, or is it simpler to use our own bucketing and just pass the key-value?

### Publift's NoCMP setup

Per Publift's integration team (Hijas):
- NoCMP is a **Fuse configuration**, not a code change on our side
- Publift activates NoCMP for specified geos
- FACEIT's role: assign users to groups and set the GAM key-value so we can attribute revenue by variant
- Publift does **not** change ad delivery logic — same demand, same floors, same setup. Only the CMP enforcement changes.

---

## Experiment Geos

Selected for: high impression volume, meaningful revenue, no GDPR/TCF legal requirement, geographic diversity.

| # | Country | YTD Revenue | YTD Impressions | eCPM | Daily Imp (est.) | Region |
|---|---|---|---|---|---|---|
| 1 | **Brazil** | $4,890 | 59.0M | $0.08 | ~504K | LATAM |
| 2 | **Türkiye** | $1,795 | 40.7M | $0.04 | ~348K | MENA |
| 3 | **Uzbekistan** | $3,869 | 38.9M | $0.10 | ~333K | CIS |
| 4 | **Australia** | $2,196 | 27.7M | $0.08 | ~237K | APAC |
| 5 | **Ukraine** | $2,493 | 102.8M | $0.02 | ~879K | CIS |
| 6 | **Argentina** | $2,087 | 29.6M | $0.07 | ~253K | LATAM |
| 7 | **Kazakhstan** | $1,542 | 23.7M | $0.07 | ~202K | CIS |
| | **Total** | **$18,872** | **322.5M** | **$0.06** | **~2.76M** | |

**Why these 7:**
- **$18.9K YTD / 12.5% of total Publift revenue** — large enough to measure, small enough to limit blast radius
- **~2.76M impressions/day** → ~1.38M per variant → strong statistical power
- **No GDPR/TCF legal requirement** in any of these markets
- **Geographic diversity**: LATAM (BR, AR), CIS (UZ, UA, KZ), MENA (TR), APAC (AU)
- **Ukraine** ($0.02 eCPM) is a particularly interesting signal — 103M impressions at rock-bottom eCPM could indicate severe consent-related suppression

**Excluded geos and why:**
- **US / Canada** — state/provincial privacy laws (CCPA, CPRA, Quebec Law 25) may require consent mechanisms. Legal risk.
- **UK** — UK GDPR applies post-Brexit. TCF may still be required.
- **Switzerland** — nFADP (Swiss data protection). GDPR-adjacent. Not worth the risk.
- **EEA countries** — GDPR requires TCF. Not part of this experiment.

---

## Sample Size & Power

**Parameters:**
- Combined daily impressions: ~2.76M (~1.38M per variant)
- Combined daily revenue: ~$161 (~$80.50 per variant)
- Baseline eCPM: $0.06 (blended across 7 geos)
- Primary metric: RPV (revenue per 1K page views)

**Estimated time to significance (80% power, 95% confidence):**

| Minimum Detectable Effect | Revenue signal/day | Duration |
|---|---|---|
| ≥20% RPV uplift | ~$16/day | **~2 weeks** ✅ |
| ≥15% RPV uplift | ~$12/day | **~2–3 weeks** ✅ |
| ≥10% RPV uplift | ~$8/day | **3–4 weeks** ⚠️ |
| ≥5% RPV uplift | ~$4/day | **6+ weeks** ❌ |

**Assessment:** CMP removal typically has a large effect on consent rates and downstream revenue (15–30% is common in industry). A 3-week test should provide sufficient data. If the effect is <10%, extending to 4 weeks is feasible.

---

## Metrics Framework

### Primary KPIs (decision metrics)

| Metric | Source | How to measure | Success threshold |
|---|---|---|---|
| **RPV** (revenue per 1K page views) | GAM revenue (by key-value) ÷ GA page views (by group) | Compare control vs variant per geo and blended | ≥15% uplift in variant |
| **eCPM** | GAM reporting by key-value | Revenue / impressions × 1,000 | Positive or neutral |
| **Fill rate** | GAM reporting by geo | Filled impressions / total requests | Positive in variant |

### Guardrails (must NOT deteriorate)

| Metric | Threshold | Owner |
|---|---|---|
| Ad viewability | Must remain ≥50% (MRC standard) | Moritz |
| Page load performance | No significant regression | Teo |
| User complaints / support tickets (test geos) | No significant increase | Support |

### Observational (track, don't gate on)

| Metric | What it tells us |
|---|---|
| Consent rate (via `CMP_GDPR_CACHED = True` key-value) | How many users currently consent in control vs how the signal changes in variant |
| Impression volume per page view | Does NoCMP increase ad fill? |
| Revenue by geo (within test geos) | Which markets benefit most from CMP removal? |
| Session duration / bounce rate (GA) | Does CMP removal affect user behaviour? |

---

## Reporting & Data Sources

| Data | Source | Access |
|---|---|---|
| Revenue by experiment group | **GAM** — filter by key-value (`cmp_test=control` vs `cmp_test=variant`) | Moritz (existing GAM access) |
| Revenue by geo | **GAM** — standard geo report | Moritz |
| Page views by experiment group | **GA** — custom parameter set by FACEIT front-end | Moritz / Teo |
| Fill rate by geo | **GAM** — geo report (⚠️ cannot filter by experiment group due to GAM limitation) | Moritz |
| Consent rate | **GAM** — key-value `CMP_GDPR_CACHED` | Moritz |
| Publift dashboard | **Publift** — will NOT show geo-level data; use GAM instead | Seán (Publift) |

**GAM baseline report already created:** [Report #7398577074](https://admanager.google.com/41188963#reports/interactive/detail/report_id=7398577074)

**Known limitation:** GAM cannot filter fill rate by experiment group or differentiate between Programmatic and Direct. Fill rate analysis will be geo-level only (not split by control/variant).

---

## Implementation

### FACEIT Engineering (Teo)

| Task | Detail | Effort |
|---|---|---|
| Implement experiment split | Assign users 50/50 in test geos. Set GAM key-value (`cmp_test=control` / `cmp_test=variant`) on ad requests. | TBD |
| Set GA parameter | Pass experiment group to GA for page view tracking | TBD |
| Load correct Fuse variant | Control: standard Fuse (TCF CMP). Variant: NoCMP Fuse. Logic based on experiment group assignment. | TBD |
| **Open Q:** Can Fugly pass key-values to GAM? | If yes → use Fugly. If no → custom front-end logic. | TBD |
| **Open Q:** UUID pass-through | Can we use Publift's UUID or do we use our own bucketing? | TBD |

### Publift (Seán / Hijas)

| Task | Detail |
|---|---|
| Provide NoCMP Fuse build | Deliver the NoCMP fuse.js variant for FACEIT to deploy conditionally |
| Confirm key-value setup | Validate that `cmp_test` key-value will be picked up in GAM reporting |
| Provide GA tracking instructions | Publift to share instructions for setting up UUID/group tracking in GA |
| Review experiment setup | Final review with Hijas before activation |

### Moritz (PM / Analysis)

| Task | Detail |
|---|---|
| Confirm geos with Publift | Share this doc, align on 7 geos |
| Set up GAM reporting | Create report filtered by `cmp_test` key-value × geo |
| Pull baseline data | Pre-experiment RPV/eCPM/fill for test geos |
| Run analysis at experiment end | Compare control vs variant, write conclusion |

---

## Timeline

| Week | Action | Owner |
|---|---|---|
| **W1** | Share experiment design with Teo and Publift (Seán) | Moritz |
| **W1** | Teo confirms: Fugly key-value capability + implementation approach | Teo |
| **W1** | Publift delivers NoCMP Fuse build + GA tracking instructions | Seán / Hijas |
| **W2** | FACEIT implements experiment split + key-value + CMP conditional loading | Teo |
| **W2** | Pull baseline RPV/eCPM data for 7 test geos | Moritz |
| **W2** | Publift reviews final setup before activation | Hijas |
| **W3** | **Launch experiment** | Teo + Moritz |
| **W3** | Monitor first 48h — check key-values appearing in GAM, no anomalies | Moritz |
| **W6** | End experiment (3 weeks of data) | Moritz |
| **W6–W7** | Analysis + experiment conclusion | Moritz |

**Total time to launch: ~2 weeks.** Then 3 weeks of data collection.

---

## Rollback Plan

If variant shows:
- **RPV drops >10% relative** vs control → Kill variant immediately, revert all users to standard CMP
- **Viewability drops below 50%** → Kill variant
- **User complaints spike** in test geos → Kill variant and investigate

Rollback: Teo removes experiment split, all users get standard TCF CMP. Publift deactivates NoCMP. Same-day turnaround.

---

## Success Criteria

| Outcome | Verdict | Next step |
|---|---|---|
| RPV ≥15% uplift, guardrails pass | **Ship NoCMP** | Roll out NoCMP to all non-EEA geos. Estimated annual uplift: $12K–$15K. |
| RPV 5–15% uplift, guardrails pass | **Promising** | Extend test 2 more weeks for confidence. Consider adding more geos. |
| RPV <5% uplift or neutral | **Inconclusive** | Investigate per-geo results. May indicate consent wasn't the bottleneck. |
| RPV negative or guardrail fails | **Revert** | Revert to TCF. Investigate — possible demand-side issue with non-consented inventory. |

---

## Risks

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| TCF removal reduces bid quality in some non-EEA markets | Lower eCPM in variant for specific geos | Low | Some DSPs may prefer TCF signals even when not required. Monitor per-geo eCPM. |
| GAM key-value not firing correctly | Cannot attribute revenue to experiment group | Medium | QA in first 48h. Verify key-values appear in GAM reports before committing to 3-week run. |
| Privacy regulation changes in test geos | Legal exposure | Very low | All 7 geos currently have no TCF requirement. Monitor regulatory landscape. |
| Publift NoCMP build has bugs | Ad delivery issues in variant | Low | Publift reviews setup with Hijas before launch. Monitor fill rate and errors in first 48h. |
| Seasonality / campaign flight confounds | False positive or negative | Medium | Control group runs simultaneously — A/B design controls for seasonality by default. |

---

## References

- Publift YTD Geo Report: `/Users/moritznatalini/Downloads/FaceIT_Programmatic_Geo_YTD_2026.xlsx`
- GAM Baseline Report: [Report #7398577074](https://admanager.google.com/41188963#reports/interactive/detail/report_id=7398577074)
- Advertising Context: `context/advertising.md`
- Experiments Log: `context/experiments.md`
- Roadmap Item: `data/roadmap-data.json` → "Publift: CMP optimisation"
