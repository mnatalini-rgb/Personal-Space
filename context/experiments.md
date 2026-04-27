# Experiments Log

Monthly experiment cadence. Each experiment targets a specific funnel stage (TOFU / MOFU / BOFU) or advertising metric.

---

## Engagement Engine — First Test (Winline BOFU)

**Type**: Multi-variant notification experiment
**Partner**: Winline
**Funnel stage**: BOFU
**Status**: Completed — results available

### Hypothesis

Sending AI-generated, psychologically-framed activity notifications to users stuck on a specific mission challenge will increase task completion rates among already-engaged (BOFU) users.

### How It Works

- Monitors user progress through mission tasks
- Identifies users stuck on a specific challenge
- Sends a personalised notification with AI-generated copy (unique per send to avoid repetition)
- Four psychological frameworks tested as notification hooks

### Test Design

| Framework | Hook Type |
|-----------|-----------|
| Progress Completion | Near-miss framing — "you're almost there" |
| Live Reward Rush | Urgency — limited time, act now |
| Reward Motivation | Focus on what the user stands to gain |
| Competitive Pressure | Social comparison — others are completing this |

Target: Winline BOFU users completing medium-barrier deposit/bet challenges (e.g. deposit ≥3,000 RUB, bet ≥1,000 RUB)

### Results

| Framework | CTR |
|-----------|-----|
| Progress Completion | 10.6% |
| Urgency / Live Reward Rush | 9.4% |
| Skill | 7.8% |
| Competitive Pressure | 7.4% |

**Overall task completion uplift**: ~+0.2 percentage points

### Conclusions

- Reminders work — but modestly on average. Small uplift but meaningful at scale.
- **Psychological framing matters significantly** — Progress and Urgency outperform Skill and Competitive Pressure by a meaningful margin
- Most effective for **medium-barrier BOFU actions** (deposit/bet tasks) where users are already engaged with the brand
- **Not effective for TOFU** — cannot move cold or unlinked users
- Declining reach in Day 7 / Day 10 reminders is driven by **user attrition** (inactivity), not completions

### Strategic Implications

- EE is a **BOFU retention tool**, not an acquisition tool
- Prioritise **Progress** and **Urgency/Reward Rush** frameworks in all future deployments
- Value scales with the size of the engaged user base — most applicable to partners with meaningful BOFU depth (currently: Winline)

---

## January / February 2026 — Brand Integrations (TOFU)

### Experiment: Mystery Box — Account Linkage Uplift

**Type**: A/B test (50/50 split)
**Partner**: Winline (first test of this mechanic — Winline only)
**Funnel stage**: TOFU
**Status**: Completed — results available
**Note**: Mystery Box applied as a **mission-end bonus for account linkage**. See March 2026 experiments for the follow-up with Tradeit using a different logic (per-challenge, not mission-end).

#### Problem

In long-term partnerships, account linkage rates decline over time, limiting partner value and reducing the number of users entering the funnel.

#### Hypothesis

Applying a "mystery reward" framework will use curiosity and variable-reward psychology to increase motivation for account linking. Users perceive it as a free, low-effort opportunity with potential upside — increasing activation relative to a known fixed reward.

#### Test Design

| Group | Description | Reward |
|-------|-------------|--------|
| Control | Standard linkage mission | Fixed reward: 500 FP |
| Variant | Mystery Box linkage mission | Random reward from 5 tiers (see below) |

**Variant reward tiers (equal distribution — uncapped due to time constraints):**

| Tier | Reward | Share |
|------|--------|-------|
| 1 | Premium Monthly Sub | 24% |
| 2 | 1,000 FP | 26% |
| 3 | 250 FP | 25% |
| 4 | 500 FP | 25% |

#### Results

| Group | Activated | Completed | Completion Rate |
|-------|-----------|-----------|----------------|
| Control | 147,105 | 1,854 | 1.36% |
| Variant | 146,131 | 2,955 | 2.19% |

**Uplift: +61% relative lift (+0.83pp absolute) in account linkage rate.**

User quality and volume were comparable between groups — positive signal is clean.

#### Costs

| Mission | Completions Paid | Cost |
|---------|-----------------|------|
| Variant (Mystery Box) | 2,028 | $616.08 + $5K (prize pool) |
| Control | 1,864 | $739 |

Note: Equal reward distribution across all tiers (including highest-value) inflated costs. This was due to time constraints preventing calibrated weighting.

#### Compliance Note

From a privacy and compliance standpoint: account linking does not involve any payment or monetary consideration from users. As there is no cost to participate, this activity does not constitute gambling.

#### Next Steps / Backlog

- Calibrate number of rewards per mission to reduce costs (weight lower tiers more heavily)
- Decide whether to enable Mystery Box as the **default mechanic for all linkage missions**
- Test Mystery Box concept vs. Drops to compare gamification approaches
- Backlog ideas: mystery value tiers, limited-time mystery bonuses, "rare drop" probabilities

---

## March 2026 — Three Experiments Running in Parallel

---

### Experiment 1: Account Linkage Flow Simplification (Tradeit) — Trust Modal

**Type**: A/B test
**Partner**: Tradeit (global)
**Feature Flag**: `exp_TRADEIT_NO_AGE_STEP_EXPERIMENT`
**Funnel stage**: TOFU
**Status**: ✅ Concluded — Winner: Control (keep trust modal)
**Launched**: 12 March 2026
**Concluded**: April 2026

#### Problem

The account linkage flow hasn't been updated in ~2 years. The trust modal was introduced when users were unfamiliar with account linking, but user familiarity has likely increased significantly since then.

#### Hypothesis

Removing the trust modal and sending users directly to the partner login/details screen will increase the account linkage rate.

**Result: Hypothesis rejected.** Keeping the trust modal significantly improves linkage-step completion. The modal acts as a trust signal that increases user willingness to complete the linkage.

#### Test Design

| Group | Description |
|-------|-------------|
| Control | Current flow — trust modal shown before partner login |
| Variant | Trust modal removed — user goes directly to partner login details |

#### Data Sources

| Source | URL |
|---|---|
| Feature flag exposure | [Looker: user_feature_flags_v1](https://efgdata.cloud.looker.com/explore/faceit-events/user_feature_flags_v1?toggle=fil&qid=aQ2khmca1wEqJF8JVJR6PE) |
| Account linkage outcomes | [Looker: user_account_linkage_operation_v1](https://efgdata.cloud.looker.com/explore/faceit-events/user_account_linkage_operation_v1?qid=b9q6tXQkIcbfu89ttyDxCV&toggle=fil) |

#### Results

**Metric 1 — Full-population AL rate** (all users exposed to feature flag):

| | Control (trust modal) | Variant (no trust modal) |
|---|---|---|
| Users exposed | 1,404,335 | 596,571 |
| Account linkages | 2,529 | 1,212 |
| **AL rate** | **0.1801%** | **0.2032%** |

| Statistic | Value |
|---|---|
| Absolute lift (var − control) | +0.023 pp |
| Relative lift | +12.8% |
| Z-statistic | 3.46 |
| p-value (two-tailed) | < 0.001 |
| 95% CI | [+0.010 pp, +0.037 pp] |
| Traffic split | 70.2% control / 29.8% variant |

At the full-population level, variant shows a slightly higher AL rate — suggesting the modal may be a minor barrier to *starting* the flow.

**Metric 2 — Linkage-step completion rate** (users who reached the AL step):

| | Control (trust modal) | Variant (no trust modal) |
|---|---|---|
| **AL completion rate** | **5.34%** | **2.75%** |

| Statistic | Value |
|---|---|
| Relative drop (var vs control) | −48.4% |
| Z-statistic | 17.98 |
| p-value | < 0.001 |
| € impact per cohort | +€416 (control generates more value) |
| € impact per 1K users | +€9.82 |

Among users who reached the linkage step, removing the trust modal nearly halves the completion rate.

#### Conclusions

The two metrics tell complementary stories: removing the modal may get slightly more users to *start* linking (+12.8% full-pop), but it dramatically reduces *completion* (−48.4% at the linkage step). Since partner value is driven by completed linkages that convert to deposits/trades (C1/C2), the linkage-step metric is the one that matters for NSM.

- **Recommendation: Keep the trust modal as the permanent default for all partner AL flows.**
- The € impact is significant: +€416 per cohort, +€9.82 per 1K users.
- Zero engineering cost — the modal is already the default experience.
- Finding should apply to all partners (Winline, PaySafe, WhiteMarket), not just Tradeit.

**Full write-up:** `docs/product_briefs/trust-modal-experiment-conclusion.md`

#### Next Steps

- Roll back variant. Make trust modal the permanent default.
- Apply trust modal pattern to all future partner account linkage flows (PaySafe, etc.)
- Close feature flag `exp_TRADEIT_NO_AGE_STEP_EXPERIMENT` in the feature flag system.

---

### Experiment 2: Mystery Box for Conversions (Tradeit)

**Type**: A/B test
**Partner**: Tradeit (global)
**Funnel stage**: MOFU / BOFU
**Status**: Launched 12 March 2026 — results pending

#### Context & Lineage

The original Mystery Box test (Jan/Feb 2026) was run **with Winline only**, applied as a **mission-end bonus for account linkage**. This new test is the first time the mechanic is applied:
- With **Tradeit** (not Winline)
- At a **specific challenge level** (not mission-end bonus)
- Across **two KPIs**: Account Linkage AND Trade any item

#### Problem

The Mystery Box mechanic tested with Winline was applied as a bonus reward at mission completion — awarded only after the user completed the entire Mission (all KPIs). The question is whether applying it at a specific challenge/KPI level drives deeper funnel conversions.

#### Design Changes from Previous Test

Tradeit raised specific concerns that shaped the experiment design:

- **Account Linkage stays as a prerequisite** — AL is not a separate rewarded step; it remains a pre-condition to enter the mission, as per current setup. No Mystery Box on AL.
- **No reward splitting** — giving the user too many prizes across multiple steps would confuse them and inflate advertiser budget. Mystery Box is attached to **one specific challenge only**.
- **Apples-to-apples comparison** — the test isolates a single challenge: does step X convert better with a fixed FP reward vs. a Mystery Box reward? All other steps remain unchanged.

#### Hypothesis

Attaching the Mystery Box to a specific single challenge rather than as a mission-end bonus will increase the completion rate of that challenge, while keeping the rest of the mission flow unchanged.

#### Challenges Under Test

| Challenge | Description |
|-----------|-------------|
| Account Linkage | Link FACEIT account to Tradeit |
| Trade any item | Complete a trade on Tradeit |

#### Setup

New BE feature developed to **fix reward probabilities per tier** — solving the cost control issue from the first Mystery Box experiment (previously equal distribution inflated costs).

**Reward tiers by region:**

| Tier | NA | MENA | CIS |
|------|----|------|-----|
| 1% | 1 month Premium | 1 month Premium | 1 month Premium |
| 5% | 5,000 FP | 5,000 FP | 5,000 FP |
| 80% | 1,000 FP | 500 FP | 500 FP |
| 2% | $20 | $20 | 1,550 RUB (~$20) |
| 12% | $5 | $2 | 150 RUB (~$2) |

#### Test Design

| Group | Description |
|-------|-------------|
| Control | Specific challenge rewarded with fixed FP |
| Variant | Same specific challenge rewarded with Mystery Box (same budget envelope) |

#### Results

— Results pending (launched 12 March 2026)

#### Next Steps

— To be updated once results are available.

---

### Experiment 3: Skippable Video Interstitial (Advertising)

**Type**: A/B test
**Funnel stage**: Advertising — AVU / CPM
**Status**: Completed — experiment concluded 14 April 2026. GTM handed to Commercial team (15 April 2026).
**Reference PRD**: `docs/product_briefs/PRD — Video Interstitials.md`

#### Problem

Interstitial ads deliver the highest CPMs due to strong visibility and CTR. However, they are also highly intrusive — increasing inventory volume risks user frustration and long-term CPM degradation. Revenue cannot safely grow by adding more interstitials.

#### Hypothesis

Adding a skippable video format inside the interstitial placement will increase CPM without negatively impacting user retention (measured by games played).

#### Setup

- A/B test using **games played** as the primary guardrail KPI
- The video interstitial (house ad) only shows if **no display interstitial fills** — avoids cannibalising existing paid impression delivery
- Triggered when a user **returns to the platform after a period of inactivity** (high-attention moment)

#### Format Details

| Characteristic | Detail |
|----------------|--------|
| Trigger | User return after inactivity |
| Autoplay | Sound-off |
| Skip | After 3 seconds |
| Placement | Guaranteed in-view |

#### Test Design

| Group | Description |
|-------|-------------|
| Control | Standard display interstitial |
| Variant | Skippable video interstitial (3s unskippable, then skip available) |

#### Success Metrics

- **Primary**: CPM uplift vs static interstitial baseline, Viewability, CTR
- **Guardrail**: Games played per session (must show no negative impact)

#### Results

A/B test ran 16 March – 14 April 2026 (31 days, 6.47M GAM impressions across 184 countries).

**Retention guardrail: PASSED**
- Variant: 173.3K avg daily matchmaking uniques vs Control: 172.8K (+0.3% delta, not statistically significant)
- Both groups tracked within ±1K on all 31 days with identical weekly seasonality

**Performance metrics:**
- 70.4% video completion rate (GAM weighted avg); 83.3% full-15s completion on front-end events
- 0.37% CTR — 23,698 clicks to Premium purchase page
- 320 Premium subscriptions attributed (46 direct, 274 view-through)
- 1.35% click-to-subscription conversion rate

**Regional pattern:** Tier 1 / APAC markets achieved 75–81% completion. Central Asia / Balkans dipped to 50–65% (likely device/connectivity, not content relevance).

Full experiment report: `skippable-video-dashboard.pdf`

#### Next Steps

- Experiment validated — format is safe to ship. No retention risk detected.
- Go-to-market ownership transferred to Mandar's commercial team (agreed 15 April 2026).
- Open questions on ad serving setup, sales packaging, pricing model, and trafficking sent to commercial team.
- Mandar to share full Salesforce pipeline overview.

---

## April 2026 — Data Investigation: Winline Opportunity Gap

**Type**: Cross-platform data analysis (CDP × BQ)
**Partner**: Winline
**Status**: Completed — findings integrated into Nonlinear Missions PRD
**Date**: 22 April 2026

### Objective

Quantify how many Winline depositors are active FACEIT users but never engage with missions — the "opportunity gap" that structural mission changes (nonlinear missions) could address.

### Methodology

1. Exported Winline user events from Snowflake CDP (`analytics_rep.cdp_service.user_events`)
   - `last_dep` events (deposits, last 3 months): 152,939 unique users
   - `task_*` events (mission tasks, last 3 months): 16,414 unique users
2. Computed cohort overlap locally (CSV intersection by `user_id`)
3. Cross-referenced all 155,534 unique users against BQ `business-intelligence-prod.dbt_user.dim__users` for FACEIT activity, verification, subscription, geo, language, account age
4. Batched BQ queries (8 batches of ~20K user IDs each) due to BQ Console character limits

### Key Findings

**Cohort Overlap:**

| Cohort | Users | % |
|---|---|---|
| Deposit + Mission (both) | 13,819 | 9.0% of depositors |
| Deposit only (no mission) | 139,120 | 91.0% of depositors |
| Mission only (no deposit) | 2,595 | — |

Missions capture only 9% of the depositing Winline user base.

**FACEIT Activity of Deposit-Only Users (139,120):**

| Recency | Users | % |
|---|---|---|
| Active last 30 days | 45,664 | 32.8% |
| Active 31–90 days | 16,813 | 12.1% |
| Active 91–365 days | 18,498 | 13.3% |
| Churned (>1y / never matched) | 58,145 | 41.8% |

**45,664 active FACEIT gamers deposit on Winline but never touch a mission.** Their profile (69.1% verified, 10.2% premium, median account age 5y2m, overwhelmingly RU) is near-identical to users who do engage with missions — the gap is structural, not demographic.

**Critical correction — BOFU Mission Activation (BQ UserMissions):**

Cross-referencing the 45,664 active-30d deposit-only users against BQ `UserMissions` for FTD + WHALE Winline campaigns (Feb–Apr 2026):

| Segment | Users | % of Active-30d |
|---|---|---|
| **Activated BOFU mission + played matches (EBU)** | **43,904** | **96.2%** |
| Activated, no progress | 883 | 1.9% |
| Never activated any BOFU mission | 871 | 1.9% |

**The original assumption was wrong.** These users are NOT ignoring missions — 96.2% are in BOFU missions, actively playing gaming challenges. They just don't complete the partner conversion tasks (deposit 3,000 RUB, bet 5,000 RUB). Only 65 users (0.1%) complete all tasks including partner tasks.

**Challenge staleness:** BOFU partner tasks are identical month over month (Feb = Mar = Apr). Same deposit amounts, same bet amounts, same minimum odds. Users who didn't convert in February see the exact same ask in March and April.

**Two structural problems, not a reach problem:**
1. Partner task conversion failure: 43,904 EBU users grind gaming challenges but 0.1% complete partner tasks
2. Challenge staleness: identical partner asks month over month provide zero incremental motivation

### Data Artefacts

- CDP exports: `data/brand_integrations/faceit_snowflake_analytics rep__cdp_service__user_events 2026-04-22T1016.csv` (mission users), `...T1017.csv` (deposit users)
- Cohort CSV: `data/brand_integrations/winline_cdp_cohorts_for_bq.csv`
- BQ batch queries: `data/brand_integrations/bq_batches/batch_1.sql` through `batch_8.sql`
- BQ results: `data/brand_integrations/bq-results-20260422-*.csv` (8 files)

### Implications

- The mission product's BOFU conversion problem is not about reach — 96% of active depositors are already in missions
- The problem is partner task conversion: users engage with gaming challenges but not partner tasks (0.1% completion rate)
- **Conscious engagement confirmed**: 43,905 users claimed the "Play 1 match" gaming reward (not passive auto-enrollment). They saw the mission, collected the reward, and chose not to do partner tasks.
- Challenge staleness compounds the issue: identical partner asks month over month give no new reason to convert
- **FTD vs WHALE**: WHALE tier converts 7pp lower (38.4% vs 45.6%) — higher deposit/bet thresholds reduce conversion
- **Cross-mission engagement**: 30.2% of conscious BOFU users also complete Premium Monthly missions (mission grinders who still skip partner tasks). 69.8% only appear in Winline BOFU (weak discovery/activation).
- **Historical decline**: Partner completion rates fell from ~9.5% (mid-2024) to 6.7% (2026 YTD) while user base tripled. Problem is actively worsening.
- Validates the core thesis of the Nonlinear Missions PRD: structural mission changes (user-chosen order, progression, challenge variety) could unlock conversion among 43,904 active EBU users
- 41.8% churn rate among deposit-only users represents a separate reactivation opportunity outside mission scope
- Impact at Winline C3 value of €4.33: even 5% BOFU partner task conversion = 2,195 conversions = €9,504/month
- **Shop engagement**: 83.3% of conscious BOFU users have shop orders in 2026 — they are FP-motivated and economically active. Reward-effort mismatch on partner tasks is a key lever.

### Data Artefacts (updated)

- CDP exports: `data/brand_integrations/faceit_snowflake_analytics rep__cdp_service__user_events 2026-04-22T1016.csv` (mission users), `...T1017.csv` (deposit users)
- Cohort CSV: `data/brand_integrations/winline_cdp_cohorts_for_bq.csv`
- BQ batch queries: `data/brand_integrations/bq_batches/batch_1.sql` through `batch_8.sql`
- BQ results: `data/brand_integrations/bq-results-20260422-*.csv`
- BOFU mission activation: `data/brand_integrations/bq-results-20260422-101321-1776852814220.csv`
- Gaming reward claims: `data/brand_integrations/bq-results-20260422-113626-1776857793603.csv`
- Premium Monthly users: `data/brand_integrations/bq-results-20260422-114810-1776858503585.csv`

## December 2025 — Brand Integrations

### Experiment 1: TOFU — Increasing Account Linkage Among Unresponsive Users

**Partners**: Winline (RU), Tradeit (global)
**Funnel stage**: TOFU
**Status**: Proposed / in test

#### Background

Unresponsive users show consistently low engagement. Neither brand propositions nor standard incentives have driven meaningful action from this segment so far.

#### Problem Statement

How can we encourage unresponsive, non-linked users to link their accounts with Winline or Tradeit?

#### Eligible User Pool

| Region | Active Players | WL Linked | Tradeit Linked |
|--------|---------------|-----------|---------------|
| Russia | 450K (23K premium) | 355K | — |
| Rest of World (US, CA, MENA, APAC) | 169K (152K non-subscribers) | — | 58K |

#### Hypothesis

Providing premium tokens as free rewards to non-subscribed, unresponsive users will increase account linkage rates with Winline and Tradeit and improve overall engagement in this low-activity segment.

#### Test Design

**Winline**

| Group | Description | Incentive |
|-------|-------------|-----------|
| Control | No change | None |
| Variant 1 | Incentivised with token rewards | Premium Tokens |
| Variant 2 | "Drops Case" with mixed rewards | Tokens + 3,000 FP + Cosmetic Item |

**Tradeit**

| Group | Description | Incentive |
|-------|-------------|-----------|
| Control | No change | None |
| Variant 1 | Incentivised with token rewards | Premium Tokens |
| Variant 2 | "Drops Case" with mixed rewards | TBC |

---

### Experiment 2: MOFU — Mission Chain UX Improvement

**Partner**: Winline
**Funnel stage**: MOFU
**Status**: Follow-up to POC

#### Background

A prior POC validated that the **Mission Chain** feature (chaining one mission to another via a ticket reward) has a positive impact on mission completion rates.

Current UX friction: when a user completes a mission and receives a ticket to the next, they must manually navigate to a new page to continue. This introduces unnecessary drop-off.

#### Goal

Reduce friction in the Mission Chain flow and measure the impact on engagement and conversion rates.

#### Test Design

Eligible segment: users who have already linked their accounts (linked users only)

| Group | Description |
|-------|-------------|
| Control | Users access the second Mission via the "ticket" bonus reward (current flow) |
| Variant 1 | Users see Chapters + Rewards displayed inline (reduced friction) |

---

## Moba vs. Publift — Advertising (Date TBC)

**Type**: A/B test — header bidding provider comparison
**Inventory**: FACEIT web display + video

### Hypothesis

Integrating Publift (header bidding wrapper) would outperform the existing Mobalitics managed service in yield (eCPM) and revenue by increasing competition for ad inventory.

### Results

| Metric | Mobalitics | Publift |
|--------|-----------|---------|
| eCPM | ~$0.80–0.90 | ~$1.40–1.60 |
| RPM uplift | baseline | ~+30–40% |
| Fill rate | Slightly higher | Slightly lower (offset by eCPM gain) |
| Page latency | baseline | +~150ms (negligible) |

### Conclusion

**Winner: Publift.** The managed service model (Mobalitics) was less efficient than Publift's transparent, multi-bidder environment. Publift also provided superior technical support and reporting.

### Outcome

- Full migration to Publift across all FACEIT web properties
- Further inventory segmentation within Publift dashboard recommended (sticking vs. non-sticking ad units)
- Explore Publift outstream video capabilities to replace/augment existing video providers
- Leverage Publift for Private Marketplace (PMP) deals with premium partners

---

## September 2025 — Brand Integrations

### Experiment: Mission Carousel vs. Traditional List View

**Type**: A/B test (50/50 split)
**Duration**: 14 days (1–14 September 2025)
**Audience**: Global FACEIT users, desktop web only
**Funnel stage**: TOFU / MOFU (mission discovery → activation)

#### Hypothesis

A horizontal carousel layout for missions will increase engagement (CTR) compared to a traditional list view by reducing cognitive load and highlighting featured partner content more effectively.

#### Test Design

| Group | Description |
|-------|-------------|
| Control | Standard vertical list of active missions |
| Variant | Horizontal "Featured Missions" carousel at top of Missions page, followed by condensed list |

#### Results

| Metric | Result |
|--------|--------|
| CTR (first 3 cards vs. top 3 list items) | +12.5% uplift |
| Mission Activation Rate (branded missions) | +8.2% uplift |
| Account Linkage (Winline) | +4% uplift |
| Engagement beyond card 4 in carousel | -60% drop-off vs. list view |

#### Conclusions

- The carousel is highly effective for "hero" content and driving immediate action — but only for the first few slots
- Engagement is strongly front-loaded; users rarely scroll past the first 3–4 items in a horizontal format
- Visual prominence successfully drives users toward high-value BI actions (account linkage)

#### Strategic Recommendations

- **Adopt carousel** for the "Featured" section; maintain list view for "All Missions" to preserve discoverability
- **Cap at 5 items** maximum to avoid choice paralysis and support mobile-responsive behaviour
- **Sell first 3 slots as Premium Placements** for advertisers seeking high OVU and TAVI impact
- **Next iteration**: test auto-scroll vs. manual navigation to improve deep-card engagement

---

## November / December 2025 — Brand Integrations

### Experiment: Multi-Step Conversion Ladder Mission (Winline)

**Type**: Conversion funnel experiment
**Duration**: November – December 2025
**Audience**: Active CS2 players on FACEIT, unlinked to Winline
**Funnel stage**: TOFU → MOFU → BOFU (full funnel)

#### Hypothesis

Implementing a multi-step "Conversion Ladder" mission structure (aligned to TAVI framework) will increase high-value user actions (deposits) compared to simple account-linking rewards.

#### Mission Structure

| Tier | Action | Reward |
|------|--------|--------|
| Tier 1 (AL) | Link FACEIT account to Winline | 500 FACEIT Points |
| Tier 2 (C1/C2) | Complete KYC + first deposit ≥ $10 | Exclusive Weapon Skin |
| Tier 3 (C3) | Wager $50 on specific matches | 5,000 FACEIT Points |

Promoted via platform banners and Mission tab highlights.

#### Results

| Metric | Volume | Conversion Rate |
|--------|--------|----------------|
| Total Reached | 145,000 | — |
| Account Linkage (AL) | 12,400 | 8.5% of reach |
| KYC Completion (C1) | 4,100 | 33% of AL |
| First Deposit (C2) | 2,850 | 23% of AL / 69.5% of C1 |
| Deep Conversion (C3) | 940 | 7.5% of AL |

**TAVI / OVU Impact**

| Metric | Value |
|--------|-------|
| OVU (Outcome Value Units) | $78,450 |
| OVU per 1,000 EBU | $541.03 |

#### Conclusions

- Drop-off from Linkage to Deposit is significant (77%) — but users who do convert show high retention on the partner platform
- **Tangible digital rewards** (weapon skin at Tier 2) outperformed platform currency (FACEIT Points) for mid-funnel completion — stronger driver for C1/C2 actions
- **Biggest friction point**: AL → KYC transition (67% drop-off) — KYC is the primary bottleneck in the funnel

#### Strategic Recommendations

1. **In-app KYC status** — integrate real-time partner API signal to show "KYC Pending" status on the FACEIT mission UI, reducing anxiety and drop-off
2. **Retargeting segment** — create audience of users who linked but did not deposit; run a follow-up "Recovered Mission" with a time-limited bonus
3. **Reward mix** — favour tangible digital assets (skins, cosmetics) over FACEIT Points for mid-funnel tiers
4. **Mission landing page** — shorten copy; users averaged only 4 seconds reading before clicking "Join Mission"

---

## January / February 2026 — Advertising

### Experiment: Outstream Video on Matchmaking Queue

**Type**: A/B test (50/50 split)
**Duration**: 4 weeks (15 January – 12 February 2026)
**Audience**: Free users, EU and CIS regions
**Funnel stage**: Advertising — AVU (Attention Value Units)

#### Hypothesis

Showing a 15-second outstream video ad immediately after a user joins a matchmaking queue will increase AVU by 25% with less than 2% negative impact on Queue-to-Match conversion — because user attention is highest while waiting for a game.

#### Test Design

| Group | Description |
|-------|-------------|
| Control | Standard display banners only |
| Variant | 15s outstream video unit in bottom-right of client/browser upon clicking "Play" |

#### Results

| Metric | Control | Treatment | Delta |
|--------|---------|-----------|-------|
| AVU (Attention Value Units) | baseline | +32% | ✅ Exceeded 25% target |
| Viewability Rate | 64% | 88% | +24pp |
| Video Completion Rate (VTR) | — | 72% | — |
| Queue-to-Match Conversion | baseline | -0.8% | ✅ Within <2% guardrail |
| CTR | 0.4% | 1.4% | +1pp |

#### Conclusions

- Hypothesis validated — "wait-time" video placement significantly drives AVU without harming the core matchmaking funnel
- High VTR (72%) confirms users are captive during the initial seconds of queuing
- The -0.8% conversion dip was concentrated in low-end PC users — likely resource contention when the video player initialises

#### Strategic Recommendations

- **Full rollout** to free users globally
- **Low-spec mode detection** — serve static display instead of video for low-end devices to eliminate the conversion dip
- **Test 30s units** for premium/high-value brand partners to increase eCPM (15s had strong completion, suggesting headroom)
- **Frequency cap** this placement at 3 impressions per user per day to avoid long-term fatigue

---

## March – April 2026 — Advertising

### Experiment: Prebid Outstream CSStats — Mobalytics vs Primis

**Type**: A/B test (50/50 split on CSStats.gg)
**Duration**: 25 days (Mar 30 – Apr 23, 2026; GA page views from Mar 27)
**Inventory**: Outstream video on CSStats.gg
**Funnel stage**: Advertising — RPV (Revenue Per Page View)
**Status**: Concluded — Winner: Mobalytics (+134% net RPV)
**Dashboard**: `analysis/prebid-outstream-csstats-dashboard.html`

#### Problem

CSStats.gg outstream video inventory was served by Primis, which had poor performance, low transparency, and a 20% revenue share fee. Mobalytics (Prebid, via EFG group) offered an alternative with 0% commission.

#### Hypothesis

Mobalytics (Prebid) will deliver higher Revenue Per Page View than Primis for outstream video on CSStats.gg, after accounting for Primis's 20% rev-share fee.

**Result: Hypothesis confirmed.** Mobalytics outperforms Primis by +134% on net RPV.

#### Test Design

| Group | Description |
|-------|-------------|
| Mobalytics (Prebid) | Outstream video via GAM / Mobalytics prebid wrapper (0% commission) |
| Primis | Outstream video via Primis (20% rev-share fee) |

Traffic split: 50.15% Mobalytics / 49.85% Primis (Δ 0.6% — valid). Remaining ~26% is Russia/consent/Publift noise excluded from comparison.

#### Results

| Metric | Mobalytics | Primis (Gross) | Primis (Net, −20%) | Delta (vs Net) |
|--------|-----------|----------------|---------------------|----------------|
| Total Revenue | **$184.05** | $97.76 | $78.21 | Moba +135% |
| Impressions | ~505,000 | 2,660,269 | — | Primis 5.3x more |
| eCPM | **$0.36** | $0.037 | $0.029 | Moba 9.7x higher |
| Page Views (GA) | 4,880,618 | 4,850,989 | — | ~balanced |
| **RPV (per 1K views)** | **$0.038** | $0.020 | **$0.016** | **Moba +134%** |

**US Fill Gap (key driver):** Moba served 253,371 US impressions ($125.22, 68% of total) vs Primis 499 US impressions ($0.15). This is a Primis supply-side fill issue — GA page views were balanced. Ex-US, Primis net wins by ~$19, but the US gap overwhelms.

#### Conclusions

- **Mobalytics wins clearly** on the primary metric RPV (+134% net) and total revenue (+135% net)
- US fill is the decisive factor — Primis has near-zero US inventory while Moba fills 253K impressions
- Primis's 20% rev-share fee widens the gap further (gross comparison is +88%, net is +134%)
- A hybrid approach (Moba US + Primis RoW) theoretically saves ~$19/month — not worth operational complexity
- Primis fills 5.3x more impressions but at dramatically lower eCPM ($0.037 vs $0.36) — volume can't compensate

#### Next Steps

- Ship Mobalytics as default outstream provider on CSStats
- Communicate result to EFG/Max and sunset Primis outstream
- Monitor Moba RPV post-rollout (100% traffic) for 2 weeks
- Inform Prebid Outstream FACEIT experiment design with CSStats learnings

---

## April 2026 — Advertising

### Experiment: CMP Non-TCF Geo Test (Publift)

**Type**: A/B test (user-level bucketing)
**Funnel stage**: Advertising — RPV (Revenue Per Page View)
**Status**: In Setup — pending Teo implementation
**Experiment Design**: `docs/product_briefs/cmp-nontcf-experiment-design.md`

#### Problem

FACEIT serves Publift's TCF 2.2 CMP (consent popup) globally, including in geos where GDPR does not apply. The consent flow may suppress ad yield in non-GDPR markets by blocking or delaying ad requests, reducing fill rate and eCPM.

#### Hypothesis

Removing the TCF CMP in non-GDPR geos will increase Revenue Per Page View (RPV) by ≥15%, as ad requests fire immediately without consent gating, improving fill rate and auction competition.

#### Test Design

| Group | Description |
|-------|-------------|
| Control | Current Publift Fuse CMP (TCF 2.2 consent popup) |
| Variant | Publift NoCMP Fuse variant (no consent popup) |

**Geos**: Brazil, Türkiye, Uzbekistan, Australia, Ukraine, Argentina, Kazakhstan
**Traffic**: ~2.76M impressions/day, ~$161/day
**MDE**: 15% RPV uplift detectable in 2–3 weeks
**Tracking**: GAM key-values (`cmp_test=control` / `cmp_test=variant`) for revenue attribution

#### Key Exclusions

- EEA (GDPR), UK (UK GDPR), Switzerland (nFADP)
- US/Canada (CCPA, state privacy laws, Quebec Law 25)

#### Success Metrics

- **Primary**: RPV (Revenue Per Page View) — ≥15% uplift
- **Secondary**: Fill rate, eCPM, consent rate delta
- **Guardrail**: No increase in ad quality complaints or publisher policy violations

#### Next Steps

- Teo to confirm Fugly can pass GAM key-values
- Decide bucketing approach (Publift UUID vs own)
- Implement NoCMP Fuse variant in selected geos
- Monitor for 2–3 weeks, then conclude
