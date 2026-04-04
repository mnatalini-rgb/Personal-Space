How ## **Product One‑Pager: Play Interstitial — Pre‑Roll Video for FACEIT**

**Owner**: [Moritz Natalini](mailto:m.natalini@efg.gg) | **Contributors**: [Kerrin Meek](mailto:k.meek@efg.gg), [William Seghers](mailto:w.seghers@efg.gg) | **Date**: March 2026 | **Status**: Discovery — *Seeking approval to run behavioural tolerance test*

---

## 1. Overview

Play Interstitial introduces premium video ad inventory at the most engaged moment of the FACEIT experience — immediately before a player queues for a match. The format delivers up to **3 × 30‑second ad slots** (90 seconds total) per match for free users, creating a high‑value pre‑roll product that fills the video inventory gap left by Watch's sunset and gives the Commercial team a path to **shift streaming budgets from YouTube/Twitch back to FACEIT**.

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
| **Ad slots per match** | Up to **3** (ad pod) | 90 seconds of ads per ~45 minutes of gameplay = **2 minutes per hour** — exactly **half** the ad density Commercial wanted for Watch (6 min/hr of streaming) |
| **Max length per slot** | 30 seconds | Industry standard pre‑roll length |
| **Total ad time** | Up to 90 seconds | Competitive with YouTube pre‑roll (15–30s per video, but users watch 10–20 videos/session) |
| **Frequency** | 1 ad pod per match | Natural placement at the moment of highest intent |
| **Eligible users** | Free users only | Subscribers skip ads — creates a premium conversion lever |

### Why 3 Slots is the Right Number

William's insight: *"I'd rather have a feature with 10M impressions at 10% fill rate, than 1M impressions at 100% fill rate. In the first scenario I still have 90% of potential that's not filled yet."*

3 slots maximises **inventory potential**. Even at modest fill rates, the total addressable inventory is large enough to attract programmatic demand and justify dedicated sales effort. And the ad density is defensible:

- **FACEIT (proposed)**: 2 min ads / 60 min gameplay = **3.3% ad density**
- **Watch (historical)**: 6 min ads / 60 min streaming = **10% ad density**
- **YouTube**: 2–4 min ads / 60 min viewing = **3–7% ad density**
- **Twitch**: 3+ min ads / 60 min viewing = **5%+ ad density**

FACEIT's proposed ad density is **at or below** every major streaming platform.

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

## 4. Inventory Value — The Big Number

William's framework: *"Show a big number of potential. Higher inventory, lower fill rate."*

### Inputs

| Input | Value | Source |
|:--|:--|:--|
| Monthly matches (free users, globally) | **~15M** | ~45M impressions ÷ 3 matches/user estimate. Based on existing appendix data |
| Ad slots per match | **3** | Proposed ad pod |
| **Total monthly inventory** | **~45M ad slots** | 15M matches × 3 slots |
| Tier 1 share (~40%) | ~18M slots | US, UK, DE, FR, etc. |
| Tier 2 share (~35%) | ~15.75M slots | PL, TR, UA, KZ, etc. |
| Tier 3 share (~25%) | ~11.25M slots | Remaining geos (excl. Russia) |

### Scenario A — Inventory Value (Maximum Potential)

*What this inventory is worth if we could fill every slot.* This is the ceiling — the number that shows Commercial why this product is worth dedicated sales effort.

| Tier | Monthly Slots | CPM | Monthly Revenue | Annual Revenue |
|:--|--:|--:|--:|--:|
| **Tier 1** | 18,000,000 | $15 | $270,000 | **$3,240,000** |
| **Tier 2** | 15,750,000 | $10 | $157,500 | **$1,890,000** |
| **Tier 3** | 11,250,000 | $5 | $56,250 | **$675,000** |
| **Total** | **45,000,000** | | **$483,750** | **$5,805,000** |

**The full inventory potential is ~$5.8M/year** — before fill rate.

### Scenario B — Realistic Case (Year 1)

If Steve starts moving budget from ESL/Socials to FACEIT, with additional programmatic sales and potentially Winline in Tier 3:

| Lever | Fill Rate | Monthly Revenue | Annual Revenue |
|:--|--:|--:|--:|
| **Tier 1** (direct + programmatic) | 25% | $67,500 | $810,000 |
| **Tier 2** (programmatic + PMPs) | 15% | $23,625 | $283,500 |
| **Tier 3** (programmatic remnant) | 10% | $5,625 | $67,500 |
| **Video Ads Subtotal** | | **$96,750** | **$1,161,000** |
| **Incremental Subs** (upsell in ad slots) | | | **$800,000** |
| **Total Year 1** | | | **~$2.0M** |

**Realistic Year 1 target: ~€1M ARR in ad revenue** + subs upside. With 75%+ of inventory still unfilled, the growth runway is massive.

### Scenario C — Why Unfilled Inventory = Opportunity, Not Risk

| Metric | Value |
|:--|:--|
| Total addressable inventory | 45M slots/month |
| Year 1 filled (Scenario B) | ~7.5M slots/month |
| **Unfilled** | **~37.5M slots/month** |
| **Fill rate** | **~17%** |

This means **83% of inventory remains available** for future demand — as the sales team scales, as programmatic demand matures, and as we add partners. Every percentage point of fill rate improvement = ~$57K/year in incremental revenue.

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
| **Ad density** | 3–7% of viewing time | **3.3%** of gameplay time |
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

**Conservative Year 1 estimate: €500K–€1M in shifted/new video budget**, growing as fill rate scales and programmatic demand matures.

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
2. Short video pod plays (≤ 90s across up to 3 slots — Phase 0 uses 1 internal creative)
3. Matchmaking begins

Full UX flow available in [FigJam](https://www.figma.com/board/PRwDAnFVQpYASGFeg0E8b7/Video-Interstitial-Play?node-id=17-12019&t=3J3hDAFIXcXzNRrf-4)

### Phase 1: Limited Monetised Rollout
- Selected Tier 2 markets, solo players only
- Direct sales + PMP deals (Adam, Domenik)
- 1–2 ad slots active

### Phase 2: Tier 1 Expansion + Programmatic
- Tier 1 markets with direct advertisers
- Open programmatic via VAST / prebid (Publift or Mobalytics stack)
- Test content chaser (mid‑roll experiment)
- Scale to full 3‑slot pod where demand supports it

### Phase 3: Full Commercial Rollout
- All geos (excl. Russia — GAM constraint)
- Full programmatic + direct hybrid
- Party player support

---

## 9. Technical Requirements

| Requirement | Detail |
|:--|:--|
| **VAST 4.2 compliance** | XML ad responses, multi‑bitrate media files, full tracking events (impression, quartiles, complete, error) |
| **Ad pod support** | Sequential serving of up to 3 creatives in a single ad break |
| **Pre‑caching** | Video assets pre‑loaded during UI navigation to eliminate latency at match start |
| **Frequency capping** | Server‑side, 1 pod per user per match (not per day — clarified) |
| **Measurement integration** | IAS or DoubleVerify for brand safety + viewability verification (table stakes for premium CPMs) |
| **Macro support** | `[CACHEBUSTING]`, `[TIMESTAMP]`, `[CONTENTPLAYHEAD]` for dynamic VAST values |
| **Russia exclusion** | GAM does not operate in Russia — exclude from all programmatic setups |

---

## 10. Risks & Mitigations

| Risk | Mitigation |
|:--|:--|
| Player frustration (90s is long) | Phase 0 starts with 1 slot (30s). Pod length scales with demand, not day 1. Strict max 90s. |
| Party player complexity | Phase 1 targets solo players only |
| Technical latency | Pre‑cached video assets + Phase 0 validates load times |
| New player disruption | Excluded until first match played |
| Low initial fill rate | Expected and acceptable (see Section 4C). Unfilled = future growth runway. |
| IAB "no content" classification | Hybrid approach: sell as interstitial (direct) and instream (programmatic). Content chaser in Phase 2 addresses formally. |
| Ad‑block risk | Monitor ad‑block activation as guardrail. 1/match frequency is dramatically lower than typical web ad load. |

---

## Appendix

1. Full data available [here](https://docs.google.com/spreadsheets/d/1nN-b8SML75S3W8Ai4tJIwVFL0CQlm0lCqzkEB43o5Jk/edit?gid=0#gid=0)
2. Watch historical ad density: 6 min ads / 60 min streaming
3. FACEIT proposed ad density: 2 min ads / 60 min gameplay (3 × 30s per ~45 min match)
4. Roblox case study: $100M+ in video ad revenue (2025), programmatic partnership with Google
