# Project PHOENIX — Product Feedback on BCG Commercial Strategy Deck

**Author**: Moritz Natalini, Director of Product — Monetisation  
**Date**: 25 March 2026  
**Deck reviewed**: "(20260318) Digital Platform Strategy vClient" — 104 slides  
**Recipients**: Eugene (Evgueni Zelenyi), Simon (BCG)

---

## Purpose

This document provides slide-specific product feedback on the BCG Commercial Strategy deck. The focus is on factual misalignments between BCG's claims and actual product reality, inconsistencies within the deck itself, and assumptions that need stress-testing before external use.

Items are ordered by severity of impact on strategic conclusions.

---

## 1. Deprecated Metric Framework Referenced

**Slide 24** (thumbnail section)

The deck references the weighted OVU formula: `AL=$3, C1=$7, C2=$20, C3=$3`. This scoring model was **deprecated in March 2026**. We now use **direct euro values per conversion point**, not abstract weighted scores. The normalised metric is **€ per 1K EBU** (euro value per 1,000 Eligible BI Users), not OVU per 1K EBU.

The TAVI framework structure (BI + Advertising components, eligible audience normalisation) remains valid — only the scoring methodology changed.

**Risk**: If the deck circulates externally or to leadership referencing the old formula, it contradicts the metric framework we're actually operating against. Any projections built on OVU weights will produce different conclusions than our current € value model.

**Ask**: Replace OVU weight references with the current € value per conversion methodology. The conversion ladder stages (AL → C1 → C2 → C3) are still valid — it's the scoring system that changed.

---

## 2. Tier Classification Inconsistency

**Slides 30 and 33**

BCG's tier definitions are internally inconsistent and misaligned with our actual tier structure:

| | BCG Slide 30 | BCG Slide 33 | FACEIT Actual |
|---|---|---|---|
| **Tier 1** | US, UK, CA (3 countries) | US, UK, CA + DE, FR, IT, AU, CH | DE, US, FR, GB, ES, CA, AU, IT (8 countries) |
| **Poland** | Tier 3 | — | Tier 2 |

The deck uses two different T1 definitions across its own slides, and neither matches ours. This matters because tier classification drives CPM assumptions, ARPU projections, and revenue sizing throughout the deck.

**Risk**: Any revenue projection that depends on "Tier 1 ARPU" or "Tier 1 user base" will produce different numbers depending on which slide's definition you use — a 3-country T1 vs an 8-country T1 changes the addressable base significantly.

**Ask**: Align to a single tier definition and state it explicitly. If BCG's classification differs from ours for analytical reasons, that's fine — but it should be declared upfront and used consistently.

---

## 3. Revenue Projection Assumptions Need Stress-Testing

**Slides 14, 82, and 23**

The deck projects ~$32.2M incremental BP revenue over 3 years across 17 verticals, with a 2030 high case of €30.8M (vs 2025 baseline of €3.4M — a ~9x increase in 5 years).

Key assumptions to challenge:

- **Crypto vertical at $8M by Y3**: Extremely aggressive given regulatory volatility in EU/CIS markets, exchange collapses, and the fact that crypto advertising is banned or heavily restricted in several of our T1 geos.
- **Streaming/Kick at $5M**: BCG's own note flags this as a "single BD opportunity" — meaning one deal falling through eliminates $5M from the projection.
- **Geographic scope**: Projections assume EU+CIS only, yet the revenue figures require near-complete geo coverage for rate card realisation (see item 4 below).

For context, actual 2025 BP revenue was €3.5M, driven almost entirely by one seller (see item 10). The gap between current run-rate and projected run-rate requires a fundamentally different operating model, which the deck acknowledges but leaves as a placeholder (see item 9).

**Ask**: Provide sensitivity analysis on the top-3 verticals. What happens to the 3-year total if Crypto delivers $2M instead of $8M and Kick doesn't materialise?

---

## 4. Missions Inventory Potential Methodology

**Slides 12, 55, and 56**

The deck sizes Missions potential at €15.8M, of which only 10% (€1.6M) is currently realised. The methodology assumes **7 brands × ~€2.3M rate card × ALL geos × 12 months**.

Issues:
- The 7-brand cap correctly acknowledges cannibalization risk, but the rate card assumes **full-geo coverage** per brand, which is unrealistic. Most partners activate in 2-5 geos, not globally.
- The €2.3M per-brand rate card implies a willingness-to-pay that only Winline-tier partners have demonstrated (€2.4M in 2025). The median partner deal is €300-500k.
- The 10% realisation rate is presented as "headroom" but could equally reflect a ceiling — demand-side constraints (advertiser budgets, seasonal cycles, vertical concentration) may limit how many slots we can actually sell.

**Ask**: Model a "realistic fill" scenario — e.g., 4-5 brands at average deal sizes of €500k-€1M with partial-geo activation — alongside the theoretical maximum.

---

## 5. "Potential" ARPU Figures Are Misleading

**Slide 33**

The slide shows current vs "potential" ARPU for non-paying users:

| | Current | "Potential" | Multiple |
|---|---|---|---|
| **Tier 1** | $0.39 | $9.78 | 25x |
| **RoW** | $0.03 | $17.16 | **572x** |

The "potential" figure assumes **all impressions filled at direct-sold CPMs**. This is not achievable because:
- Direct-sold fill is demand-constrained (the deck's own slide 45 acknowledges this)
- Programmatic fill produces fundamentally lower CPMs
- RoW inventory has structurally lower demand regardless of fill
- Subscriber growth removes users from the ad-eligible pool (slide 32), and subscriber growth is concentrated in T3 where ad ARPU is already lowest

A 572x ARPU improvement in RoW would require a complete transformation of the ad market for gaming audiences in those geos.

**Risk**: If these "potential" figures are used in any board or investor context, they overstate addressable opportunity by orders of magnitude.

**Ask**: Either remove the "potential" column or clearly label it as a theoretical maximum with the assumptions stated (100% direct fill, current CPMs). Add a "realistic upside" column based on achievable fill rate improvements (e.g., 2-3x current via programmatic optimisation).

---

## 6. Mobalytics Readiness for Reward Pass

**Slides 16, 40, 41, and 45**

The deck proposes a Mobalytics "Reward Pass" launching Q2 2026 (described as similar to FACEIT Missions). However, the deck's own data undercuts readiness:

- **Slide 40**: MUV→MAU conversion declined from 19% (2022) to 10% (2025). MAU is flat/declining (555k→535k).
- **Slide 41**: Subscriber conversion is entirely concentrated in T1 (1% of MUU). RoW subscriber conversion = 0%.
- **Slide 45**: BCG explicitly states Moba has "**no capability to deliver performance and conversion BP products**." Also notes high ad density is suppressing CPMs.

Launching a Missions-equivalent product on a platform that (a) is losing conversion efficiency, (b) has zero RoW subscriber traction, and (c) lacks the technical capability to deliver conversion BP products requires significant product investment that isn't scoped in the deck.

**Ask**: What product and engineering investment is assumed before Q2 launch? Is there a dependency on FACEIT's BP infrastructure, or is this envisioned as standalone Moba build?

---

## 7. Internal Number Inconsistencies

**Slides 18 vs 19, and 62 vs 63**

Two sets of figures contradict across adjacent slides:

| Data Point | Slide A | Slide B | Delta |
|---|---|---|---|
| PUBG 3rd-party card — annual revenue | $200k (slide 18) | $350k (slide 19) | **75% difference** |
| KSA projection — revenue | $970k at 55% margin (slide 62) | $870k at 50% margin (slide 63) | **$100k / 5pp margin gap** |

These may be different scenarios or time periods, but they appear as standalone figures without context, which undermines credibility.

**Ask**: Reconcile or clearly label which figure applies in which scenario.

---

## 8. Bain MAPs Estimate vs Reality — Implications Not Addressed

**Slide 29**

The slide notes that the 2022 Bain strategy estimated 13.2M MAPs by 2027, versus the new 5YP of 2M MAPs. That's a **6.6x downgrade**.

BCG doesn't address the implications of this for their own projections. If the user base growth assumptions that underpin Bain's commercial strategy were off by 6.6x, what safeguards exist to avoid the same overestimation in BCG's revenue projections? The deck's revenue scenarios are tied to user base size, and a 2M MAP reality vs 13.2M assumed fundamentally changes the denominator.

**Ask**: Explicitly state which MAP growth assumptions BCG's revenue projections depend on, and show how the projections change under the 5YP trajectory vs a more conservative scenario.

---

## 9. Operating Model Is a Placeholder

**Slides 100-103**

The "Enhanced Operating Model" and "Short-term Plan" sections are marked as "Placeholder — to be further discussed." The footer on slide 103 references a "$57M revenue gap."

The revenue projections in the first 90 slides require a fundamentally different go-to-market capability. Leaving the operating model as a placeholder means the most critical enabler of the strategy is undefined. Without it, the projections are supply-side sizing exercises, not a strategy.

**Ask**: Prioritise completing this section before the deck is used for decision-making. At minimum: headcount plan, seller specialisation, partner pipeline targets, and timeline.

---

## 10. Single-Seller Dependency

**Slides 96-97**

The deck correctly identifies that **one person (Evgueni Zelenyi) effectively drives all FACEIT BP revenue**, supported by 2-3 partner managers with "limited upskilling." Five other lead sellers lack the product expertise to sell DP inventory.

BCG's growth projections (€30.8M high case by 2030, vs €3.4M today) require capacity that doesn't exist and isn't planned (see item 9). Scaling from 1 effective seller to the required capacity is a multi-year organisational transformation, not a Q2 quick win.

**Ask**: Include a realistic ramp timeline for seller capacity alongside the revenue projections. What does Y1 revenue look like if seller capacity is the binding constraint?

---

## 11. Product Claims Without Product Team Alignment

**Slide 87**

The slide proposes in-game food ordering from the match lobby. This is a significant engineering scope item that has not been discussed with or scoped by the product team. Including it without product team input creates expectation risk with stakeholders who read the deck.

Similarly, slide 52 notes that tournaments are "not used as a conversion tool" — rewards go to the same top players. This is a correct observation, but the deck doesn't propose a solution, which makes it a dangling insight.

**Ask**: Flag product-dependent features clearly as "requires product team scoping" rather than presenting them as part of the strategy.

---

## 12. Advertising Deprioritised Despite ARPU Dependency

**Slide 45**

Advertising is described as "not core focus," yet:
- The ARPU upside claims (slide 33) depend heavily on ad monetisation improvements
- Advertising is one of only two revenue levers (BI + Ads)
- The subscriber growth that BCG celebrates (slide 31) actively shrinks the ad-eligible audience

There's a tension in the deck between deprioritising advertising and relying on advertising ARPU improvement as a key value driver.

**Ask**: Clarify the advertising strategy position. If it's not core focus, remove or discount the ad-driven ARPU projections accordingly. If the ARPU projections are meant to be taken seriously, advertising needs a clear plan.

---

## Summary: Priority Actions

| # | Item | Severity | Action |
|---|---|---|---|
| 1 | Deprecated OVU formula | **High** | Update to current € value methodology |
| 2 | Tier inconsistency | **High** | Align to single definition, state explicitly |
| 3 | Revenue projection stress-test | **High** | Add sensitivity analysis |
| 5 | "Potential" ARPU | **High** | Relabel or add realistic scenario |
| 9 | Operating model placeholder | **High** | Complete before deck is decision-grade |
| 10 | Single-seller dependency | **High** | Add capacity ramp timeline |
| 4 | Missions potential method | **Medium** | Add realistic fill scenario |
| 6 | Moba Reward Pass readiness | **Medium** | Scope product investment required |
| 7 | Internal number inconsistencies | **Medium** | Reconcile PUBG + KSA figures |
| 8 | Bain MAPs implications | **Medium** | State MAP assumptions explicitly |
| 11 | Unscoped product claims | **Low** | Flag as requiring product scoping |
| 12 | Ads strategy tension | **Low** | Clarify positioning |

---

*This feedback is based on a product review of all 104 slides. Financial figures and market sizing are not challenged on methodology — only on internal consistency and alignment with known product reality.*
