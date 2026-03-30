## **Product One‑Pager: Play Interstitial — Pre‑Roll Video for FACEIT**

**Owner**: [Moritz Natalini](mailto:m.natalini@efg.gg) | **Contributors**: [Kerrin Meek](mailto:k.meek@efg.gg), [William Seghers](mailto:w.seghers@efg.gg) | **Date**: March 2026 | **Status**: Discovery — *Seeking approval to run behavioural tolerance test*

---

## 1. Overview

Play Interstitial introduces premium video ad inventory at the most engaged moment of the FACEIT experience — immediately before a player queues for a match. The format delivers **up to 60 seconds of video ads** (as many slots as fit) per match for free users, creating a high‑value pre‑roll product that fills the video inventory gap left by Watch's sunset and gives the Commercial team a path to **shift streaming budgets from YouTube/Twitch back to FACEIT**.

---

## 2. Problem Statement

### The Watch Gap

When **Watch** (FACEIT's streaming platform) was sunset, Commercial lost its primary vehicle for selling high‑value instream video on a FACEIT‑owned property. Video campaign budgets — previously running on Watch — were redirected to **YouTube and Twitch** pre‑rolls, where FACEIT competes with every other advertiser for the same generic gaming audience.

At the same time:

- **Free users generate server costs with no ad revenue** — every competitive match requires significant infrastructure (game servers, anti‑cheat, matchmaking). Flo's original ask: *"How do we monetise free users to offset these costs?"*
- **FACEIT's audience is uniquely valuable** — verified competitive gamers at their moment of highest engagement, with demographic data, geo targeting, and anti‑cheat–verified identity. YouTube and Twitch cannot offer this.
- **No premium video format exists on FACEIT today** — display ads and outstream remnant (Primis, ~$21K/month) don't command pre‑roll CPMs.

### The Opportunity

Play Interstitial is the path to **bring video budgets back to FACEIT** — not by replicating a streaming platform, but by offering something better: a captive, high‑intent, verified gaming audience with guaranteed viewability at a natural pause point.

---

## 3. Solution

Serve **VAST‑based pre‑roll video ads** in a full‑screen interstitial placement shown to free users before they queue for a match.

### Ad Density & Rationale

| Parameter | Spec | Rationale |
|:--|:--|:--|
| **Ad pod per match** | Up to **60 seconds** total | As many slots as fit within 60s. 1 minute of ads per ~45 minutes of gameplay = **1.3 minutes per hour** — less than **a quarter** of the ad density Commercial wanted for Watch (6 min/hr of streaming) |
| **Max length per slot** | 15–30 seconds | Industry standard pre‑roll length |
| **Frequency** | 1 ad pod per match | Natural placement at the moment of highest intent |
| **Eligible users** | Free users only | Subscribers skip ads — creates a premium conversion lever |

The pod fills dynamically — at launch most pods will contain 1–2 shorter creatives. The 60‑second cap leaves headroom to scale inventory as demand grows, without changing the player experience. And the ad density is defensible:

- **FACEIT (proposed)**: 1 min ads / 45 min match = **2.2% ad density**
- **Watch (historical)**: 6 min ads / 60 min streaming = **10% ad density**
- **YouTube**: 2–4 min ads / 60 min viewing = **3–7% ad density**
- **Twitch**: 3+ min ads / 60 min viewing = **5%+ ad density**

FACEIT's proposed ad density is **well below** every major streaming platform.

### Why Maximise Inventory Potential

William's insight: *"I'd rather have a feature with 10M impressions at 10% fill rate, than 1M impressions at 100% fill rate. In the first scenario I still have 90% of potential that's not filled yet."*

A 60‑second pod maximises **inventory potential**. Even at modest fill rates, the total addressable inventory is large enough to attract programmatic demand and justify dedicated sales effort.

### Technical Approach — Hybrid Format

Our placement is unique: there is **no video content** for the ad to precede. The user experience is a full‑screen interstitial, but we serve ads via **VAST tags** — the same protocol used by YouTube, Twitch, and every major SSP/DSP.

This hybrid gives us the best of both worlds:

- **Interstitial UX** → 95%+ viewability, natural pause point, premium feel for direct‑sold campaigns
- **Pre‑roll ad tech (VAST)** → access to the full programmatic demand pool (Google ADX, Magnite, Xandr, Index), higher fill rates, competitive auction pressure

**How to position it:**
- To **direct advertisers / agencies**: *"Premium gaming interstitial — 95% viewability, 1/match frequency, verified competitive gaming audience."*
- To **programmatic partners / SSPs**: *"VAST‑compliant instream pre‑roll inventory"* — to maximise fill.
- To **Commercial (Steve, Mandar)**: *"Pre‑roll that captures budget currently going to YouTube/Twitch gaming campaigns."*

---

## 4. Revenue Model

All numbers below are derived from the [Business Case Calculations spreadsheet](https://docs.google.com/spreadsheets/d/1EqqmNj3TMF4cC7XYQ_mz4LHlMG-QVA7c0fsbMDgPklk/edit?usp=sharing). Every figure can be traced back to a specific cell with formula. William's framework: *"Show a big number of potential. Higher inventory, lower fill rate."*

### 4a. Inventory Sizing — ~37M ad pods / ~111M impressions per month

| Input | Value | Source / Calculation |
|:--|--:|:--|
| **Monthly free finished match sessions (incl. Russia)** | **36,994,576** | [Looker](https://efgdata.cloud.looker.com/x/ppIcoKxQKKrJKCwCWs2dRE) — Feb 2026, free users only |
| **Ad pods per match** | **1** | 1 pod (up to 60s) per match session |
| **Total monthly ad pods** | **~37.0M** | = Monthly sessions (spreadsheet col E, Grand Total row 196) |
| **Total monthly impressions** | **~111.0M** | = Pods × 3 (3 ads per pod, avg 20s each within 60s cap) |
| — of which **Tier 1** (DE, US, FR, GB, ES, CA, IT, AU) | 2,843,125 (7.7%) | 8 countries (spreadsheet row 192) |
| — of which **Tier 2** (PL, RO, FI, PT, NL, DK + 27 more) | 9,379,848 (25.4%) | 33 countries (spreadsheet row 193) |
| — of which **Tier 3** (KZ, UA, TR, BY + 142 more) | 12,597,276 (34.1%) | 146 countries (spreadsheet row 194) |
| — of which **Russia** | 12,174,327 (32.9%) | Separate — limited ad server availability (spreadsheet row 195) |

Each ad pod can contain **up to 60 seconds of video ads**. We model **3 impressions per pod** (average 3×20s creatives within the 60s cap). Revenue is calculated on impressions (pods × 3), while fill rate and subs model apply at the pod level.

### 4b. Inventory Value — What This Is Worth at 100% Fill

*This is the ceiling — the number that shows Commercial why this product is worth dedicated sales effort.*

| Tier | Monthly Impressions | CPM | Monthly Revenue | Annual Revenue |
|:--|--:|--:|--:|--:|
| **Tier 1** (8 countries) | 8,529,375 | $15 | $127,941 | **$1,535,288** |
| **Tier 2** (33 countries) | 28,139,544 | $10 | $281,395 | **$3,376,745** |
| **Tier 3** (146 countries) | 37,791,828 | $5 | $188,959 | **$2,267,510** |
| **Russia** | 36,522,981 | $2 | $73,046 | **$876,552** |
| **Total** | **110,983,728** | | **$671,341** | **$8,056,094** |

**The full inventory potential is ~$8.1M/year** — before fill rate.

### 4c. Ad Revenue Scenarios — Paid Fill

The base case assumes **20% fill rate** on Tier 1 and Tier 2, and **10% fill** on Tier 3 and Russia. CPMs vary by tier to reflect advertiser willingness to pay. (Spreadsheet: Scenario Comparison rows 202–204.)

| Scenario | Fill Rate | CPM Assumption | T1 Annual | T2 Annual | T3 Annual | RU Annual | **Total Ad Revenue** |
|:--|:--|:--|--:|--:|--:|--:|--:|
| **Conservative (Year 1)** | 20% T1/T2, 10% T3/RU | T1 $15, T2 $10, T3 $5, RU $2 | $307,058 | $675,349 | $226,751 | $87,655 | **$1.3M** |
| **Mid Case** | 20% T1/T2, 10% T3/RU | T1 $20, T2 $15, T3 $5, RU $2 | $409,410 | $1,013,024 | $226,751 | $87,655 | **$1.7M** |
| **100% Fill Ceiling** | 100% all tiers | T1 $15, T2 $10, T3 $5, RU $2 | $1,535,288 | $3,376,745 | $2,267,510 | $876,552 | **$8.1M** |

*Calculation: Revenue = Impressions × Fill Rate ÷ 1,000 × CPM × 12, where Impressions = Pods × 3 (3 ads per pod). All formulas in spreadsheet.*

Every **1 percentage point increase** in blended fill rate ≈ **$81K/year** in incremental ad revenue (at Conservative CPMs).

### 4d. Subscription Revenue Upside (House Ads)

Unfilled ad pods serve **house ads** promoting FACEIT Premium subscriptions. This applies to **all** users including Russia (house ads don't require GAM). This creates a secondary revenue stream.

| Step | Value | Calculation |
|:--|--:|:--|
| Total pods (all users incl. Russia) | 36,994,576/month | Spreadsheet Grand Total, col E row 196 |
| Unfilled pods (~87% average) | ~32.1M/month | Total pods minus filled pods (spreadsheet col K) |
| Subs conversion rate | 0.05% | Spreadsheet col L |
| Gross new subscribers | ~16,000/month | Unfilled × 0.05% |
| Cannibalisation (50%) | ~8,000/month | 50% would have subscribed anyway |
| **Net incremental subs** | **~8,000/month** | Spreadsheet col M |
| Revenue per subscriber | $7.30/month | FACEIT Premium monthly price |
| **Monthly subs revenue** | **~$58,500** | |
| **Annual subs revenue** | **~$702K** | Spreadsheet col O, Grand Total |

**Combined Year 1 estimate (Conservative): ~$1.3M ad revenue + ~$702K subs upside = ~$2.0M/year.** Subs revenue is shown separately because it depends on house ad creative effectiveness and conversion assumptions.

### 4e. Why Unfilled Inventory = Opportunity, Not Risk

| Metric | Year 1 (Conservative) |
|:--|:--|
| Total addressable ad pods | ~37.0M pods/month |
| Year 1 filled (paid ads, Conservative) | ~4.9M pods/month |
| **Unfilled (available for future demand)** | **~32.1M pods/month** |
| **Blended paid fill rate** | **~13.3%** |
| Unfilled pods serving house ads | ~32.1M pods/month |

This means **~87% of inventory remains available** for future demand — as the sales team scales, as programmatic demand matures, and as we add partners. The unfilled pods aren't wasted: they serve house ads that drive ~$702K/year in incremental subscription revenue.

---

## 5. Commercial Budget Shift — How Streaming Money Moves to FACEIT

### The Current State

When Watch was sunset, Commercial redirected video budgets to YouTube and Twitch pre‑rolls. These campaigns target "gamers" broadly — but FACEIT's audience is a **verified subset** that YouTube/Twitch cannot isolate:

| Dimension | YouTube/Twitch | FACEIT Play Interstitial |
|:--|:--|:--|
| **Audience** | Self‑reported "gaming interest" | Anti‑cheat verified competitive gamers |
| **Targeting** | Contextual (channels, topics) | Deterministic (geo, game, rank, hardware) |
| **Viewability** | 65–70% (YouTube average) | **95%+** (full‑screen, sound‑on, unskippable) |
| **Attention quality** | Passive (lean‑back viewing) | **Active** (queuing for a match — highest intent moment) |
| **Ad density** | 3–7% of viewing time | **2.2%** of gameplay time |
| **SOV** | Shared with 5–10 other advertisers | **100% SOV** per ad slot |
| **Fraud risk** | Bot traffic, view farming | **Anti‑cheat verified users** — near-zero fraud |

### How Budget Shifts (Mechanics)

1. **Agency media plans** allocate budget to "Gaming" or "Esports" verticals. Currently this goes to YouTube Gaming, Twitch pre‑roll, and ESL event sponsorship.

2. **FACEIT Play Interstitial enters the media plan** as a new line item: same VAST‑based buying workflow, same verification partners (IAS, DoubleVerify), same DSP integrations — zero friction for the agency.

3. **Budget reallocates** from lower‑performing YouTube/Twitch lines (where FACEIT gamers are a needle in a haystack) to FACEIT (where every impression reaches a verified competitive gamer).

4. **Steve / Commercial team** can pitch this as: *"You're already spending $X to reach gamers on YouTube. We'll give you the same format (VAST pre‑roll) with 95% viewability, 100% SOV, anti‑cheat verified audience, and deterministic targeting — at a competitive CPM."*

### What Extent of Budget Can Move?

| Source | Estimated Annual Spend on Gaming Video | Shiftable to FACEIT | Notes |
|:--|--:|--:|:--|
| ESL event video campaigns | €2–5M | 10–20% | Campaigns that target "esports fans" broadly can partially redirect to FACEIT pre‑roll |
| YouTube Gaming pre‑rolls | €3–10M (top gaming advertisers) | 5–15% | Agencies running gaming verticals can add FACEIT as a premium line |
| Twitch pre‑rolls | €1–3M | 5–10% | Twitch's audience overlaps heavily with FACEIT's |
| **New direct sales** (Adam, Domenik) | n/a | €200–500K | Brand Takeover clients (Logitech, etc.) upsold to video |

**Conservative Year 1 estimate: ~$1.3M in ad revenue** (20% fill T1/T2, 10% fill T3/RU — per Section 4c) **+ ~$702K in subscription upside** from house ads. As fill rate scales and programmatic demand matures, the $8.1M ceiling (100% fill) provides significant headroom.

### Mid‑Roll / Content Chaser (William's Suggestion)

William proposed following the ad with a short piece of video content — ESL event highlights, FACEIT features, recent releases — to create a "pre‑roll + content" experience.

**Assessment:**

| Consideration | Analysis |
|:--|:--|
| **IAB classification** | Adding content after the ad technically qualifies the placement as "instream" (ad before content the user requested), which can unlock higher programmatic CPMs |
| **User experience** | Adds 10–15s to queue time. Acceptable if content is genuinely valuable (match tips, esports highlights) — risky if it feels like filler |
| **Recommendation** | **Phase 2 experiment** — test content chasers (10s ESL highlights) vs ad‑only and measure queue abandonment + CPM lift. Don't gate Phase 0/1 on this |

---

## 6. Competitive Landscape

| Platform | Format | CPM Range | Audience Verification | Viewability |
|:--|:--|:--|:--|:--|
| **Roblox** | Rewarded + interstitial video | $8–$15 | Age‑gated, limited | ~80% |
| **YouTube Gaming** | Pre‑roll (VAST) | $8–$25 | Contextual only | 65–70% |
| **Twitch** | Pre‑roll / mid‑roll | $10–$30 | Contextual only | 65–75% |
| **FACEIT (proposed)** | **Pre‑roll (VAST) in interstitial** | **$10–$25** | **Anti‑cheat verified** | **95%+** |

Roblox scaled video ads to **$100M+ in 2025** by partnering with Google for programmatic access to 151M daily gamers. FACEIT targets an older, higher‑LTV audience (18–34 competitive gamers vs Roblox's 13–24 skew) — the same DSP budgets apply.

---

## 7. Success Metrics

**Primary KPI**: Incremental Ad Revenue per User

**Secondary KPIs**:
- Video completion rate ≥ 95%
- Viewability ≥ 95%
- Fill rate (track trend, not target — per William's philosophy)

**Guardrails** (must not deteriorate):
- Matches started per user
- Ad‑block activation rate
- Premium subscription conversion
- Player sentiment (NPS / qualitative)

---

## 8. Rollout Plan

### Phase 0: Behaviour Validation (Current Ask)

Run an A/B test with **internal campaigns** (house ads, sub promotions) in US/NA to validate that 1 forced video pod/match does not harm engagement — before introducing real ads.

**Player journey:**
1. User presses **Find Match**
2. Short video pod plays (≤ 60s — Phase 0 uses 1 internal creative, ~15s) with countdown UI
3. Matchmaking begins

Full UX flow available in [FigJam](https://www.figma.com/board/PRwDAnFVQpYASGFeg0E8b7/Video-Interstitial-Play?node-id=17-12019&t=3J3hDAFIXcXzNRrf-4)

### Phase 1: Limited Monetised Rollout
- Selected Tier 2 markets, solo players only
- Direct sales + PMP deals (Adam, Domenik)
- 1–2 ad slots active within the 60s cap

### Phase 2: Tier 1 Expansion + Programmatic
- Tier 1 markets with direct advertisers
- Open programmatic via VAST / prebid (Publift or Mobalytics stack)
- Test content chaser (mid‑roll experiment)
- Scale to full 60s pod where demand supports it

### Phase 3: Full Commercial Rollout
- All geos including Russia (house ads where GAM is limited, programmatic where available)
- Full programmatic + direct hybrid
- Party player support

---

## 9. Technical Requirements

| Requirement | Detail |
|:--|:--|
| **VAST 4.2 compliance** | XML ad responses, multi‑bitrate media files, full tracking events (impression, quartiles, complete, error) |
| **Ad pod support** | Sequential serving of multiple creatives up to 60s total in a single ad break |
| **Pre‑caching** | Video assets pre‑loaded during UI navigation to eliminate latency at match start |
| **Frequency capping** | Server‑side, 1 pod per user per match (not per day — clarified) |
| **Measurement integration** | IAS or DoubleVerify for brand safety + viewability verification (table stakes for premium CPMs) |
| **Macro support** | `[CACHEBUSTING]`, `[TIMESTAMP]`, `[CONTENTPLAYHEAD]` for dynamic VAST values |
| **Russia handling** | Serve house ads where GAM is unavailable; serve programmatic where available at $2 CPM |

---

## 10. Risks & Mitigations

| Risk | Mitigation |
|:--|:--|
| Player frustration (60s is noticeable) | Phase 0 starts with 1 short creative (~15s). Pod length scales with demand, not day 1. Strict max 60s. |
| Party player complexity | Phase 1 targets solo players only |
| Technical latency | Pre‑cached video assets + Phase 0 validates load times |
| New player disruption | Excluded until first match played |
| Low initial fill rate | Expected and acceptable (see Section 4c). Unfilled = future growth runway. |
| IAB "no content" classification | Hybrid approach: sell as interstitial (direct) and instream (programmatic). Content chaser in Phase 2 addresses formally. |
| Ad‑block risk | Monitor ad‑block activation as guardrail. 1/match frequency is dramatically lower than typical web ad load. |
| No Match found | User won't see any ads again for the rest of the day |

---

## Appendix

1. **Business Case Calculations spreadsheet** — [link](https://docs.google.com/spreadsheets/d/1EqqmNj3TMF4cC7XYQ_mz4LHlMG-QVA7c0fsbMDgPklk/edit?usp=sharing). All revenue numbers in Section 4 trace back to this file. Column mapping:
   - Col A: Tier | Col B: Country | Col C: Monthly Sessions | Col D: Unique Users
   - Col E: Ad Pods/Month (=C) | Col F: Impressions/Month (=E×3) | Col G: Fill Rate | Col H: Filled Impressions (=F×G) | Col I: CPM
   - Col J: Monthly Ad Rev (=H/1000×I) | Col K: Annual Ad Rev (=J×12)
   - Col L: House Ads unfilled pods (=E×(1−G)) | Col M: Subs conversion (=L×0.05%) | Col N: Cannibalisation (=M×50%)
   - Col O: Monthly Subs Rev (=N×7.30) | Col P: Annual Subs Rev (=O×12) | Col Q: Monthly Total | Col R: Annual Total
2. **Key assumptions**: 1 ad pod per match; 3 impressions per pod (3×20s avg creatives within 60s cap); up to 60s per pod; 20% paid fill rate T1/T2, 10% T3/RU; $7.30/month subscriber value; 50% cannibalisation on house ad–driven subs
3. **Session data**: Feb 2026 Looker export — 36,994,576 monthly sessions across all geos (free users, finished matchmaking matches)
4. Watch historical ad density: 6 min ads / 60 min streaming
5. FACEIT proposed ad density: 1 min ads / 45 min gameplay
6. Roblox case study: $100M+ in video ad revenue (2025), programmatic partnership with Google
