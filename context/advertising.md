# Advertising — Product Context

## What It Is

Traditional advertising on FACEIT — display and outstream video ads. Monetises user attention and inventory rather than driving verified user actions (that's Brand Integrations).

## Scale & Strategic Weight

- **~2M MAU** — relatively small audience, heavily concentrated in Russia (CS2-dependent player base)
- **~20% of total monetisation revenues** vs Brand Integrations (~80%)
- Inventory is limited and geographically spread out, which constrains scale and eCPM

## Platform Constraints

- **Google Ad Manager does not operate in Russia** — Russia cannot be included in GAM-dependent tests or programmatic setups. Given that Russia is the largest user geo (~2M MAU, CS2-heavy), this is a significant structural constraint on advertising scale.

## Ad Products

### Display
Standard IAB formats sold directly and programmatically:
- 300x250 (medium rectangle)
- 970x90 (large leaderboard)
- 728x90 (leaderboard)
- Interstitial

### Outstream Video
- In-page video ads that play outside of video content
- Direct sales handled by Domenik's team
- Remnant inventory delegated to **Primis**

### Direct Sales Team
- **Domenik** — Sales Director, leads the direct sales team for both display and outstream
- Good working relationship with PM

## Current Monetisation Setup

### Display Remnant — Publift
- Monetises remnant display inventory programmatically via **Fuse.js** (Publift's frontend library)
- Currently yielding approximately **$50K/month**
- Reliable partner — responsive and transparent, notably better than typical AdTech vendors
- Account Manager: **Seán Conroy**
- Commission: **~20% on total revenue**

**Ad Refresh Issue (March 2026):**
- Publift's Fuse.js was discovered to be refreshing ads at **25 seconds** — below the industry standard of 30 seconds
- FACEIT requested an increase to 30 seconds to meet standard and keep maximum animation length within spec
- Publift confirmed fix via a **custom callback** from their support team — implementation expected early week of 17 March 2026
- Resolution in progress; no further action needed from PM side until confirmed live

**Known transparency issue:**
- Publift maintains a GAM placeholder line item for unfilled impressions — this artificially inflates the fill rate reported in the Publift dashboard
- As a result, fill rate is **not a reliable metric** for comparing Publift performance; **Revenue per Page View** is the correct evaluation metric

### Outstream Video Remnant — Primis
- Delegated to monetise remnant outstream video inventory
- Currently yielding approximately **$700/day (~$21K/month)**
- **Performance is poor** — underdelivering relative to expectations
- **Vendor issues**: slow to respond, low transparency — typical AdTech behaviour but a live problem
- Primis and Publift are not comparable: Publift is significantly better as a partner

### Prebid Testing — Mobalitics
- Testing a second prebid solution built by **Mobalitics**
- Mobalitics is a platform acquired by EFG (FACEIT's parent group)
- Mobalitics currently operates **independently from FACEIT** but sits within the same EFG digital platform group
- Active test — outcome TBD

## Key Metrics (NSM: AVU / EAU)

- **EAU** — Eligible Ad Users (users with at least one ad opportunity)
- **AVU** — Viewable Impressions (the NSM unit for advertising)
- Secondary diagnostics: Total Impressions, Viewable %, CTR, eCPM, Fill Rate

Full framework: `context/metrics.md`

## Commercial Structure

Advertising commercial is entirely separate from Brand Integrations.

| Name | Role | Notes |
|------|------|-------|
| Steve | SVP of Advertising | Commercial lead for all advertising |
| Domenik | Sales Director | Leads direct sales team (display + outstream). Good working relationship with PM. |
| Jenny | Director of Account Management | Reports to Steve. Proactive. |
| Sam | Account Manager | Reports to Jenny. Mostly executes mechanically, not very proactive. |
| Adam | Salesperson (Direct Sales) | The standout seller on Domenik's team. Gamer himself. Manages peripheral vertical — sold Logitech and Blacklyte. Also started selling Brand Takeover. Works mostly with agencies. |
| Mandar | VP of Operations & Indirect Ads | Primary PM counterpart on ad ops side |
| Jamie | AdOps | Reports to Mandar — collaborative to work with |
| Reece | AdOps | Reports to Mandar — collaborative to work with |

## Brand Takeover — The Advertising Bridge

Brand Takeover was originally created to sit between Missions (performance) and traditional advertising (awareness) — a ladder-based format that drives brand impressions, easy to explain and compare with display/video for brand advertisers and agencies.

**Why it hasn't scaled via Brand Integrations:**
- Eugene (BI commercial lead) is focused on performance clients — account linkage, conversions, CRM integration
- Performance clients are more valuable per user and more receptive to BI products
- Brand Takeover for awareness doesn't fit Eugene's client type or commercial incentives

**Why Adam is the right channel:**
- He works with agencies, who think in terms of awareness, reach, and brand impressions — exactly what Brand Takeover delivers
- Agencies find it easy to understand: it looks and feels like a sponsorship/takeover, comparable to traditional display
- He has a gamer background which adds credibility in pitches

**Current traction:**
- **Logitech** — active client, genuinely likes the product. Purchased **4 Brand Takeovers** (7-day format). Currently running the **3rd** (live as of March 2026).
- Logitech's agency has **included FACEIT in their 2026 planning** — strong signal of intent
- **Blacklyte** — also sold by Adam (peripheral vertical)

**Strategic implication:**
Adam and his agency relationships are the primary commercial driver shaping Brand Takeover's direction. The awareness use case is real but underserved internally — it needs a dedicated commercial motion separate from Eugene's performance-focused BI team.

---

## Rewarded Video

Rewarded Video is a new ad format introduced to bring standard video advertising into the Brand Takeover experience. It is currently in **active testing**.

### How It Works

- Triggered at the **Drop claim moment** — when a user goes to claim a Drop during a Brand Takeover event
- The user watches a short video ad in exchange for receiving the drop
- Bridges the gap between Brand Integrations (performance, engagement) and standard advertising (video views, brand impressions)

### Why It Matters

Brand Takeover already drives brand impressions via the ladder and match skin. Rewarded Video adds a **high-attention video touchpoint** at a moment of strong user intent (claiming a prize) — making it attractive to brand/agency clients who want video delivery alongside the sponsorship format.

It also creates a natural upsell: clients buying Brand Takeover can add video inventory on top, without needing a separate campaign.

### Current Test

- **Client**: Logitech (purchased 4 Brand Takeovers, 7-day format each)
- **Status**: 3rd Brand Takeover currently live (March 2026) — Rewarded Video being tested in this context
- **Sold by**: Adam

Test results TBD — to be updated once the campaign concludes.

## Interstitial Video Test (Overlay)

- **Status**: Launching today (16 March 2026)
- **Format**: Skippable video served on the current **overlay product**
- **Note**: This is distinct from the **Play Interstitial** — a separate initiative (see below)
- Purpose is primarily a **behavioural tolerance test** — validating whether users tolerate the format without harming engagement or increasing ad-block usage before scaling monetisation

---

## Play Interstitial

**Status**: Discovery — seeking approval to run behavioural tolerance test
**Presentation**: 28 March 2026 — key decision maker is **Fabio Floris ("Flo")**
**Owner**: Moritz Natalini | **Contributors**: Kerrin Meek, William Seghers
**Reference doc**: `docs/product_documentation/onePager_ Play Interstitial.md`

### What It Is

A short unskippable video shown to **free users only**, once per day, immediately before they queue for a match. Triggered at the highest-engagement moment on FACEIT (match start).

- Max **30 seconds**
- Frequency capped at **1 per user per day**
- **100% viewability** guaranteed
- Solo players only in Phase 1 (party player complexity deferred)
- New players excluded until first match played

### Why It Exists

The sunset of **Watch** removed FACEIT's primary source of high-value instream video inventory. Play Interstitial fills that gap while monetising the large free user base, which currently has limited monetisation opportunities despite generating significant infrastructure costs.

### Revenue Potential

| Revenue Source | Annual |
|----------------|--------|
| Video Interstitial Ads (~$15 CPM, Tier 1 + top Tier 2) | $450K |
| Incremental Premium Subscriptions | $800K |
| **Total Opportunity** | **~$1.2M/year** |

- ~45M impressions/month globally; ~18M in Tier 1 markets
- Initial monetisation via **direct sales only** (premium positioning)
- Russia excluded — GAM not available there

### Rollout Plan

| Phase | Description |
|-------|-------------|
| Phase 0 | A/B test with internal campaigns in US/NA — validate player tolerance before monetisation |
| Phase 1 | Limited monetised rollout in selected Tier 2 markets (solo players only) |
| Phase 2 | Expansion to Tier 1 with direct advertisers |
| Phase 3 | Full commercial rollout |

### Success Metrics

- **Primary KPI**: Incremental Ad Revenue per User
- **Secondary**: Video completion rate ≥95%, Viewability ≥95%
- **Guardrails**: Matches started per user, ad-block activation, premium conversion, player sentiment

### Key Risks

| Risk | Mitigation |
|------|------------|
| Player frustration | Strict FCAP (1/day), max 30s |
| Party player complexity | Phase 1 targets solo players only |
| Technical latency | Pre-cached video assets |
| New player disruption | Excluded until first match played |

### Known Issues in Doc (fix before 28th)

- ~~Inconsistency: Section 3 says "up to 30 seconds" but Section 4 and Section 7 say "max 15 seconds"~~ — **Fixed. All sections now aligned to 30 seconds.**

## Working Relationship Notes

- **Jamie and Reece** — good collaborative partners day-to-day
- **Domenik** — strong working relationship with PM
- **Adam** — key ally for Brand Takeover; his client feedback is actively shaping product direction
- **Jenny** — proactive, good to engage early on account planning
- **Sam** — tends to execute rather than initiate; works best with clear, specific requests
- **Mandar** — primary ad ops counterpart, under significant commercial pressure. When things aren't working there is a pattern of directing blame toward product (speed, inventory). Be precise about scope, constraints, and dependencies in all written communication to avoid ambiguity being read as a product gap.
