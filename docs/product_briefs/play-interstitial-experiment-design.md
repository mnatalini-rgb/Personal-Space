# Play Interstitial — Phase 0 Experiment Design

**Owner**: Moritz Natalini | **Attendees**: Derek, Kerrin | **Date**: April 2026 | **Status**: Designing

---

## Objective

Validate that a pre-match video interstitial does not harm player engagement or retention before scaling to full commercial rollout. This is Phase 0 of the [Play Interstitial product](../product_documentation/onePager_%20Play%20Interstitial.md).

---

## What changed from the original plan

| Original plan (March 2026) | Updated (April 2026) |
|:--|:--|
| House ads / sub promos as placeholders | **Real advertiser inventory from day 1** |
| Sentiment tracked via NPS / support tickets | **Dany (Product Marketing B2C) owns user sentiment workstream** |
| Skip mechanic loosely defined | **Confirmed UX: "USE A FREE SKIP" button, 1/day, 3s countdown before video** |

---

## Player journey (confirmed)

1. User presses **Find Match**
2. Full-screen overlay appears: *"Finding match starts searching after the advertisement"*
3. **3-second countdown** before video starts playing (sound-on by default)
4. User can tap **"USE A FREE SKIP"** to bypass — 1 free skip per day
5. After daily skip is used, button transitions to **"Upgrade"** (premium upsell)
6. Video completes → matchmaking starts automatically
7. **No ads on the first match** — ads begin from 2nd match onward

**UX reference**: [FigJam board](https://www.figma.com/board/PRwDAnFVQpYASGFeg0E8b7/Video-Interstitial-Play?node-id=0-1&t=iw9eKdWDLP2J8MZ9-1)

---

## A/B/C test design

| Group | Treatment | Purpose |
|:--|:--|:--|
| **A (Control)** | No ads | Baseline retention & engagement |
| **B** | No ads on 1st match, ads from 2nd match onward | Test "momentum" hypothesis |
| **C** | Ads from 1st match onward | Measure worst-case behavioural impact |

**Primary question**: Does the first-match ad-free experience meaningfully improve retention vs immediate ads?

**Key implication of real ads**: We get early commercial signal (completion rates, CPM, fill) alongside behavioural data — but ad quality and creative variety must be consistent across geos to avoid confounding results.

---

## Open decisions (for Derek + Kerrin meeting)

1. **Sample size & duration** — How many users per group? Minimum experiment length for statistical significance?
2. **Targeting scope** — All free users globally, or start with specific geos/games?
3. **Solo vs party** — Solo only (onepager recommends solo for Phase 1), or include party?
4. **Ad supply source** — Direct-sold only, or open programmatic from day 1?
5. **Instrumentation** — What Mixpanel events beyond the [existing board](https://mixpanel.com/project/137688/view/12355/app/boards#id=11052829&edited-bookmark=uxPweTDqbXsg)?
6. **Dany's workstream** — What inputs does she need? Survey timing, cohort definitions, access?
7. **Geo tier for release** — Tier 1 (US, UK, DE, FR), Tier 2 (PL, TR, UA, KZ), or Tier 3? Trade-off: Tier 1 = strongest commercial signal but highest risk if engagement drops; Tier 2/3 = safer to test but weaker CPM/fill data
8. **ETAs** — Design approval → Theo brief → development → experiment live

---

## Metrics framework

### Primary KPIs (must move or stay neutral)

| Metric | What it tells us |
|:--|:--|
| Matches started per user | Core engagement — did ads reduce play frequency? |
| Session depth (matches per session) | Are users quitting earlier within a session? |
| D1 / D7 / D14 retention | Short and mid-term churn signal |

### Guardrails (must NOT deteriorate)

| Metric | Owner | Threshold |
|:--|:--|:--|
| Ad-block activation rate | Moritz / Data | No significant increase vs control |
| Premium subscription conversion | Moritz / Data | Neutral or positive (Upgrade button = potential uplift) |
| Queue abandonment rate | Moritz / Data | Users closing client during or after interstitial |
| User sentiment | Dany (Product Marketing B2C) | Survey, NPS, support ticket analysis across test groups |

### Observational (track, don't gate on)

| Metric | Notes |
|:--|:--|
| Video completion rate | Real ads — expect lower than house ads would have been; baseline TBD |
| Skip usage rate | How many users burn their daily skip, and at which match in the session |
| Skip-to-upgrade funnel | % who see Upgrade button → click → convert |
| Fill rate & eCPM | Early commercial signal with real demand |

---

## Dependencies

| Dependency | Owner | Status |
|:--|:--|:--|
| Concept design approval | Anouk + Karen | In progress |
| Guardrail metrics sign-off | Moritz + Derek + Kerrin | This meeting |
| Theo dev brief | Moritz | After design + metrics approval |
| Mixpanel instrumentation | Kerrin / Data | TBD |
| Sentiment survey design | Dany | TBD |
| Hub data automation (24h refresh) | Isabel | In progress |

---

## References

- [One-pager: Play Interstitial](../product_documentation/onePager_%20Play%20Interstitial.md)
- [PRD: Video Interstitials](PRD%20—%20Video%20Interstitials.md)
- [FigJam — UX flow](https://www.figma.com/board/PRwDAnFVQpYASGFeg0E8b7/Video-Interstitial-Play?node-id=0-1&t=iw9eKdWDLP2J8MZ9-1)
- [Mixpanel board](https://mixpanel.com/project/137688/view/12355/app/boards#id=11052829&edited-bookmark=uxPweTDqbXsg)
- [Meeting notes — 9 April 2026](../Play%20interstitial%20%20-%202026_04_09%2011_25%20CEST%20-%20Notes%20by%20Gemini.md)
