# PRD: Mission Conversion Pathways

| Field | Value |
|---|---|
| **Author** | Moritz Natalini |
| **Date** | 2026-04-22 |
| **Status** | Draft |
| **Stakeholders** | Engineering (Isabel), Design (Anouk, Kerrin), Commercial, Activation Ops |
| **Product Area** | Brand Integrations |

---

## 1. Background & Context

FACEIT Missions are the primary brand integration product for driving verified user actions for partners. They work as 1:1 task-based competitions where users complete a series of in-game challenges to earn rewards. Missions run across all major partnerships (Winline, Tradeit, WhiteMarket, PaySafe) and are the top driver of Account Linkages (AL) and downstream conversions (KYC, deposits, trades).

**Current mission structure is strictly sequential.** Users complete challenges in a fixed, pre-determined order — typically: Play a match → Link account → Partner conversion action (deposit, trade, etc.). Each challenge must be completed before the next becomes available.

This model was partially validated through the Mission Chain experiment (Dec 2025), which showed that **sequential unlocking produces a positive lift** over flat missions. However, March 2026 data reveals a systemic problem: **gaming challenges convert at ~90%, while partner conversion challenges sit at 1–2%** across all partners and geos. This 40x drop-off between gaming and partner actions is the #1 bottleneck across all partnerships.

The progressive commitment model (tiered missions: low → medium → high value) is validated and shows strong late-funnel completion (67–99% once users pass the initial partner conversion). But the rigid sequential structure means users hit the hardest conversion step — account linkage or first partner action — with no agency over their path and no sense of overall progression beyond the immediate next task.

**Prior experiments that inform this PRD:**

| Experiment | Key Finding | Implication |
|---|---|---|
| Mystery Box (Jan/Feb 2026) | +61% AL uplift; lower downstream quality | Gamification works for TOFU but can dilute value |
| Trust Modal (Mar 2026) | Keeping modal nearly doubles AL step completion | Trust signals are critical — must be preserved |
| Mission Chain (Dec 2025) | Sequential unlock improves completion vs flat | Progression matters, but doesn't address 40x drop-off |
| Conversion Ladder (Nov/Dec 2025) | 67–78% late-funnel completion once users pass AL | The funnel works — it just needs a wider top |
| March 2026 Review | Gaming ~90%, partner 1–2%, reward leakage 294K | Structure is the bottleneck, not user willingness |

---

## 2. Problem Statement

**Who**: FACEIT users participating in branded missions across all partners.

**Problem**: The current sequential mission structure forces users through a rigid challenge order. Users who are willing to engage with partner actions later in the mission cannot progress past the early partner-conversion gate. This creates a massive single-point bottleneck: ~98% of users who complete gaming challenges never complete the first partner conversion challenge. Users have no visibility into what lies ahead and no sense of overall progress, which reduces motivation to push through harder challenges.

**Impact**:

| Data Point | Value |
|---|---|
| Gaming → partner drop-off | 40x across all partnerships (March 2026) |
| Winline: gaming completions → AL | 286K → 4,741 (1.7%) |
| Tradeit: joined → gaming → trade | 678K → 597K (88%) → 14K (2.4%) |
| Tradeit reward leakage | 294K users with expired, unclaimed rewards |
| Winline_KZ deposit bottleneck | 82K gaming → 358 deposits (0.4%) |

Partner value is concentrated in a tiny fraction of mission participants. The funnel is too narrow at the partner conversion gate. If even a 5% relative lift in AL could be achieved across all partners, that represents thousands of additional linkages per month and significant incremental €/1K EBU.

### 2a. Data Deep Dive: Winline BOFU Conversion Gap (April 2026)

A cross-platform analysis of Snowflake CDP data (Winline user events), BigQuery FACEIT user data (`dim__users`), and BQ campaign data (`UserMissions`, `Campaigns`) reveals that the mission conversion problem is not about reach — it's about partner task conversion among users who are already engaged.

#### Step 1: CDP Cohort Overlap

| Cohort | Users | Definition |
|---|---|---|
| Depositing on Winline (`last_dep` events, 3 months) | 152,939 | Users who actively deposit on Winline |
| Mission-active on FACEIT (`task_*` events, 3 months) | 16,414 | Users who complete at least one FACEIT mission partner task |
| **Both** (deposit + partner task) | 13,819 (9.0%) | Users captured by both funnels |
| **Deposit only** (deposit, no partner task) | 139,120 (91.0%) | Winline depositors with no CDP mission partner task events |
| **Mission only** (partner task, no deposit) | 2,595 | Possible new converts driven by mission engagement |

Initial reading: only 9% of depositors appear in CDP mission events. But CDP `task_*` events track **partner task completions** specifically — not all mission activity. The question is whether the remaining 91% are truly disengaged, or whether they participate in missions but don't complete partner tasks.

#### Step 2: FACEIT Activity (BQ dim__users)

Of the 139,120 deposit-only users:

| Recency Bucket | Users | % of Cohort |
|---|---|---|
| Active last 30 days (match played) | 45,664 | 32.8% |
| Active 31–90 days | 16,813 | 12.1% |
| Active 91–365 days | 18,498 | 13.3% |
| Churned (>1 year or never matched) | 58,145 | 41.8% |

45,664 are active gamers. Their profile is near-identical to mission-engaged users:

| Attribute | Deposit-only (active 30d, n=45,664) | Deposit + Mission (active 30d, n=11,785) |
|---|---|---|
| Verified | 69.1% | 71.8% |
| Premium subscriber | 10.2% | 14.5% |
| Median account age | 5 years 2 months | ~5 years |
| Primary country | RU (dominant) | RU (dominant) |

The two cohorts are **demographically near-identical**. The gap is not profile-based.

#### Step 3: BOFU Mission Activation (BQ UserMissions — the key finding)

Winline runs a tiered mission structure based on funnel stage. The deposit-only cohort (already linked, already deposited) is exposed to **FTD** and **WHALE** tier BOFU missions. Cross-referencing the 45,664 active-30d deposit-only users against BQ `UserMissions` for FTD + WHALE campaigns (Feb–Apr 2026):

| Segment | Users | % of Active-30d |
|---|---|---|
| **Activated BOFU mission + played matches (EBU)** | **43,904** | **96.2%** |
| Activated BOFU mission, no progress | 883 | 1.9% |
| Never activated any BOFU mission | 871 | 1.9% |

**96.2% of these users are already in BOFU missions and actively playing matches.** They are EBU. They complete gaming challenges. They just don't complete the partner conversion tasks (deposits, bets).

Gaming task completion distribution among the 44,787 who activated:

| Tasks Completed | Users | % |
|---|---|---|
| 0 (activated, no progress) | 883 | 2.0% |
| 1 task | 5,915 | 13.2% |
| 2 tasks | 7,784 | 17.4% |
| 3 tasks | 12,896 | 28.8% |
| 4 tasks | 12,599 | 28.1% |
| 5 tasks | 4,709 | 10.5% |
| All tasks (incl. partner) | 65 | 0.1% |

87% complete at least one gaming task. 56.9% complete 3 or more. **But only 65 users (0.1%) complete all tasks including partner tasks.** The gaming engagement is strong — the partner conversion gate is the blocker.

> **Footnote — Conscious engagement, not passive auto-enrollment**: The first challenge in every Winline BOFU mission is "Play 1 match" — any match auto-enrolls the user. This raises the question of whether the 43,904 EBU users are genuinely engaging or just passively counted. Validation: cross-referencing `UserMissions` task status shows **43,905 of these users have `status = 'complete'` on the gaming task**, meaning they claimed the reward. Claiming requires the user to see the mission, open it, and interact with the UI to collect. This is conscious engagement — they saw the mission, collected the gaming reward, looked at the partner tasks (Deposit 3,000 RUB / Bet 5,000 RUB), and chose not to proceed. Only 882 were passively auto-enrolled without claiming.

#### Step 4: Challenge Staleness (BQ Campaigns — compounding the problem)

Analysis of Winline campaign configurations across Feb, Mar, and Apr 2026 reveals that **BOFU partner challenges are identical month over month:**

| Tier | Partner Challenge | Feb | Mar | Apr |
|---|---|---|---|---|
| **FTD** | Внесите депозит на сумму 3000 рублей (Deposit 3,000 RUB) | ✓ | ✓ | ✓ |
| | Совершите ставки на сумму 5000 руб, коэфф. 1.3 (Bet 5,000 RUB @ 1.3 odds) | ✓ | ✓ | ✓ |
| **WHALE** | Внесите депозит на сумму 5000 рублей (Deposit 5,000 RUB) | ✓ | ✓ | ✓ |
| | Совершите ставки на сумму 25 000 руб, коэфф. 1.3 (Bet 25,000 RUB @ 1.3 odds) | ✓ | ✓ | ✓ |

Same copy, same amounts, same minimum odds — three months running. Users who didn't convert on "Deposit 3,000 RUB" in February see the identical ask in March and April. **The mission product gives them no new reason to convert.**

#### Step 5: FTD vs WHALE Tier Split (BQ UserMissions)

| Tier | Users | Partner Tasks Completed | Rate (tasks/users) | Partner Ask |
|---|---|---|---|---|
| FTD | 105,625 | 48,113 | 45.6% | Deposit 3,000 RUB + Bet 5,000 RUB |
| WHALE | 52,269 | 20,063 | 38.4% | Deposit 5,000 RUB + Bet 25,000 RUB |

WHALE converts 7pp lower — expected given the 5x higher bet threshold (25,000 vs 5,000 RUB). Note: rates include the users who DO convert (the "deposit + mission" CDP cohort); the deposit-only non-converting tail is the vast majority.

#### Step 6: Cross-Mission Engagement (BQ UserMissions)

Of the 43,905 conscious BOFU users (active-30d, claimed gaming reward):

| Segment | Users | % |
|---|---|---|
| Also complete Premium/Beta Monthly missions | 13,241 | 30.2% |
| Only appear in Winline BOFU missions | 30,664 | 69.8% |

Two distinct sub-populations:
- **30.2% are mission grinders** — they actively seek out and complete FACEIT missions (Premium Monthly has 21 challenges). They engage with the mission format. They still skip Winline partner tasks. **The partner ask is the problem, not mission engagement.**
- **69.8% are Winline-BOFU-only** — they don't engage with missions elsewhere. They likely only "participate" because auto-enrollment + easy gaming reward claim. **Discovery and activation are weak for this segment.**

#### Step 7: Historical Partner Conversion Trend (BQ UserMissions × Campaigns)

All Winline partner task completions, monthly, since May 2024:

| Period | Users Exposed | Partner Tasks Completed | Rate |
|---|---|---|---|
| 2024 Q2–Q4 avg | ~175K | ~17K | 9.5% |
| 2025 H1 avg | ~360K | ~33K | 9.2% |
| 2025 H2 avg | ~357K | ~25K | 6.9% |
| 2026 Q1 avg | ~412K | ~29K | 6.9% |
| **2026 YTD avg** | **404K** | **27K** | **6.7%** |

**Partner completion rate is declining** — from ~9.5% in mid-2024 to 6.7% in 2026. The user base nearly tripled (175K → 404K) but completions didn't scale proportionally. More users see the same stale challenges, and conversion erodes. This is partner value erosion in real time, compounding the challenge staleness problem (Step 4).

#### Step 8: Shop & Economy Engagement (BQ dim__user_shop_order_history)

Cross-referencing the 43,905 conscious BOFU users against FACEIT shop order history (2026):

| Segment | Users | % | Profile |
|---|---|---|---|
| **Shop buyer + Monthly mission grinder** | 12,589 | 28.7% | Power users — grind missions, spend FP, still skip partner tasks |
| **Shop buyer only** (no Monthly missions) | 24,005 | 54.7% | FP-motivated — earn and spend FP in the shop, don't seek out missions |
| **Monthly grinder only** (no shop) | 652 | 1.5% | Mission grinders who don't spend FP (tiny) |
| **Neither** | 6,659 | 15.2% | Minimal platform engagement beyond WL BOFU |

**83.3% of conscious BOFU users are active FP spenders in the shop.** They earn FACEIT Points from gaming challenges and spend them. They are economically engaged with the platform — the FP economy motivates them. But the current FP reward for "Play 1 match" is insufficient to push them through the partner task barrier.

Context from FP transaction data (2026 YTD): MISSION is the #1 FP source (1.18B FP to 1.1M users), and 166K users made PURCHASE transactions (shop spending). These BOFU users are part of the FP earning-spending loop — they just don't earn enough from partner task completion to justify the effort.

**What they buy** (BQ `fact__shop_order`, 2026 YTD):

| Category | Buyers | FP Spent | What it tells us |
|---|---|---|---|
| Profile customization (cards, frames, bundles) | 60K+ | 831M FP | #1 spend — users care about FACEIT identity/status |
| Tradeit codes | 7.7K | 123M FP | Users voluntarily pay FP for partner value |
| CS2 Skins | 3.7K | 119M FP | High-ticket items (~32K FP avg) for dedicated spenders |
| Steam codes | 3.4K | 82M FP | Digital codes are valued |

Profile customization dominates — cards, avatar frames, and bundles account for more FP spending than all game items combined. Notably, 7.7K users **buy Tradeit codes with FP** in the shop — they'll voluntarily pay for partner value, but won't complete Winline partner tasks that reward FP. The incentive is pointed the wrong way.

**Implication for nonlinear missions**: Reward design matters as much as structure. Exclusive profile items (cards, frames) and high-value shop items tied to partner task completion or milestone rewards would align with what these users actually spend on. Raw FP alone is insufficient — the reward needs to be something they can't get from gaming challenges alone.

#### Summary: Three Structural Problems, One Reward Signal

The original assumption — that 139K depositors "ignore missions" — is wrong. The data shows:

1. **Partner task conversion failure (primary)**: 43,904 active users are in BOFU missions, consciously engaging (claiming gaming rewards), but only 65 (0.1%) complete partner tasks. The 40x gaming→partner drop-off applies to BOFU just as much as TOFU.

2. **Challenge staleness (compounding)**: Identical partner tasks month over month provide zero incremental motivation. Users who passed on "Deposit 3,000 RUB" once see the same ask again. No progressive difficulty, no alternative paths, no escalating incentives.

3. **Declining conversion trend (accelerating)**: Partner completion rates fell from ~9.5% to 6.7% over 18 months while the user base tripled. The problem is getting worse, not plateauing. Without structural change, this trend continues.

4. **Reward-effort mismatch (new)**: 83.3% of these users actively spend FP in the shop — they are economically motivated. But current partner task rewards don't justify the effort of depositing 3,000–5,000 RUB. The FP economy works; the partner task reward structure doesn't leverage it.

Additionally, the 70/30 split between BOFU-only users and mission grinders suggests two intervention paths: (a) better partner task design and rewards for the grinders who already love missions, and (b) better discovery and activation mechanics for the BOFU-only segment.

These are the problems Mission Conversion Pathways aims to solve: give users agency over when and how they approach partner tasks, provide visible progression that rewards breadth of engagement, and create a structure where challenge variety and milestone rewards give new reasons to convert each month.

> **Methodology**: CDP user event exports (Snowflake → CSV, April 2026) joined with BQ `business-intelligence-prod.dbt_user.dim__users` via `user_id` (155,534 users, 100% match rate). BOFU mission activation from BQ `business-intelligence-prod.CampaignService.UserMissions` for FTD + WHALE campaign IDs (Feb–Apr 2026). Challenge configurations from BQ `business-intelligence-prod.CampaignService.Campaigns` (unnested missions array). Cross-mission engagement from Premium/Beta Monthly campaign IDs. Historical trend from all Winline campaigns joined via `organizer.name`. Shop engagement from BQ `business-intelligence-prod.dbt_user.dim__user_shop_order_history`. FP economy from BQ `business-intelligence-prod.dbt_user.fact__faceit_point_transactions`.

---

## 3. Goal & Success Metrics

| Metric | Current | Target | Measurement Method |
|---|---|---|---|
| Partner challenge completion rate (primary) | 1–2% (all partners) | +20% relative lift | BQ: `UserMissions` completion by challenge type |
| Account Linkage rate | 1.7% (WL), 2.4% (Tradeit) | +15% relative lift | BQ: `UserMissions` + `user_account_linkage_operation_v1` |
| Mission overall completion rate | ~5–10% (full mission) | +10% relative lift | BQ: `UserMissions` 100% completion |
| Reward claim rate | 14% (Tradeit Mar 2026) | +25% relative lift | BQ: `UserRewards` claimed vs expired |

**Guardrails (must not deteriorate):**

| Metric | Threshold |
|---|---|
| Gaming challenge completion rate | Must remain ≥85% |
| Downstream conversion quality (C1/C2 rates among linked users) | Neutral or positive |
| Partner satisfaction / reporting integrity | No regression in campaign analytics |

**NSM Connection**: Mission Conversion Pathways aims to widen the partner conversion bottleneck — the gate between TOFU gaming engagement and MOFU/BOFU partner actions. By increasing partner task completion rates, total partner value (€) per 1K EBU increases directly. Each incremental AL is worth €0.38–€4.33 depending on partner; each C2 is worth €8.75–€121.10. A 15% relative lift on Winline AL alone (4,741 → ~5,452 monthly) = ~€3,078 incremental monthly partner value on AL alone.

**BOFU opportunity (Section 2a data)**: The data reveals a larger problem than TOFU conversion alone. 43,904 active Winline BOFU users are already in missions, playing gaming challenges month after month, but only 0.1% complete partner tasks. These users are EBU — they inflate the denominator of €/1K EBU without generating partner value. Converting even a small fraction on BOFU partner tasks (C2/C3) directly improves partner efficiency. At Winline C3 value of €4.33, a 5% BOFU partner task completion rate across the 43,904 active EBU users = 2,195 incremental conversions = €9,504/month. Challenge staleness (identical asks month over month) compounds this — progressive challenge variety and reward rebalancing would give users new reasons to convert.

---

## 4. Proposed Solution

The data (Section 2a) reveals that the mission conversion problem has two distinct faces requiring different interventions:

- **TOFU**: New/unlinked users hit a hard sequential gate (AL) and drop off. This is a **structure** problem — nonlinear order and visibility help.
- **BOFU**: Linked, depositing users consciously engage with missions but refuse partner tasks. This is a **value exchange** problem — challenge variety, progressive asks, and reward calibration help.

The proposed solution addresses both through three pillars:

### Pillar 1: Nonlinear Structure (primarily TOFU)

Replace the rigid sequential mission structure with user-chosen challenge order:

1. **All challenges visible from the start.** Users see the full mission map — gaming challenges, partner challenges, and reward milestones — when they first engage with the mission.

2. **Users choose which challenges to complete in any order.** No hard gating between challenge types. A user can play a match, then link their account, then play another match, then trade — or do all gaming first and partner actions later.

3. **A progression system provides gamified advancement.** Users see their overall progression through the mission via a visual tracker (progress bar, tier map, or mission board). Completing any challenge advances the progression meter.

**Why this helps TOFU**: Addresses the core 40x drop-off — users aren't blocked by a single hard gate (AL). They can warm up with easier tasks and approach partner actions when ready. Full visibility prevents the 294K abandoned-before-discovery problem (Tradeit, March 2026). Validated by Mission Chain experiment (sequential unlocking lifts completion) and Mystery Box (gamified visibility drives engagement).

**Why this alone doesn't help BOFU**: The 43,904 active BOFU users already see all 3 challenges (play match, deposit, bet). They're not blocked — they're choosing not to act. Reordering the same stale ask doesn't change their decision.

### Pillar 2: Progressive Partner Challenges & Rotation (primarily BOFU)

Replace static, identical monthly partner tasks with progressive difficulty and monthly rotation:

1. **Progressive partner asks within a mission.** Instead of jumping directly to "Deposit 3,000 RUB", introduce a lower entry point: Deposit 500 RUB → Deposit 1,500 RUB → Deposit 3,000 RUB. Each step is its own challenge with its own reward. Users build commitment incrementally.

   > **Data rationale**: The NO KYC and NO FTD tiers already ask for 500 RUB deposits — and those tiers are earlier in the funnel. FTD users who already deposited once are asked to 6x their commitment (500 → 3,000) with no intermediate step. Progressive asks mirror the conversion ladder logic that already works for tiered missions (67–99% late-funnel completion once users pass the initial gate).

2. **Monthly challenge rotation.** Partner tasks change each month — different amounts, different actions, different framing. No user should see the identical partner ask two months in a row.

   > **Data rationale**: Identical FTD/WHALE challenges across Feb, Mar, Apr 2026 (Section 2a, Step 4). Users who said no in February see the same ask in March and April. Historical partner completion rates declined from 9.5% to 6.7% over 18 months (Step 7) — staleness is compounding.

3. **Configurable challenge templates per tier.** Activation Ops can define a library of partner challenges per tier (FTD, WHALE) and rotate them monthly. This requires partner collaboration to define acceptable challenge variants.

### Pillar 3: Reward Rebalancing (TOFU + BOFU)

Align reward value with task difficulty, using the FP economy and shop data to calibrate:

1. **Milestone rewards at progression thresholds.** Instead of per-challenge-only rewards, milestone rewards (e.g., "Complete 3/5 challenges to unlock exclusive profile card") incentivise breadth of completion and create a reason to attempt partner tasks.

2. **Exclusive items for partner task completion.** Partner challenges should reward items unavailable from gaming challenges alone — exclusive profile cards, avatar frames, or limited-edition shop items. Raw FP is insufficient.

   > **Data rationale**: 83.3% of conscious BOFU users spend FP in the shop. Profile customization (cards, frames, bundles) accounts for 831M FP in spending — more than all game items combined (Step 8). Users value identity/status items. But they can earn FP from gaming challenges without doing partner tasks — the current reward structure gives them no exclusive reason to convert.

3. **Tiered reward escalation for progressive partner asks.** Lower-tier partner tasks (Deposit 500 RUB) earn a small reward. Higher tiers (Deposit 3,000 RUB) unlock significantly better items. The reward curve should match the commitment curve.

4. **Mystery Box / variable rewards on milestone completions.** Validated by the Jan/Feb 2026 experiment (+61% AL uplift). Apply the curiosity mechanic to milestone rewards, not just TOFU linkage.

### How the Pillars Work Together

| User Segment | Primary Problem | Pillar 1 (Structure) | Pillar 2 (Challenges) | Pillar 3 (Rewards) |
|---|---|---|---|---|
| **TOFU** (unlinked) | Hard sequential gate, no visibility | ✓ Primary fix | Moderate impact | ✓ Milestone rewards motivate |
| **MOFU** (linked, no deposit) | Single high-barrier partner ask | ✓ Helps | ✓ Progressive asks lower the bar | ✓ Exclusive items |
| **BOFU** (depositing, not converting) | Stale asks, weak incentives | Marginal | ✓ Primary fix — rotation + progression | ✓ Primary fix — reward rebalancing |

### 4a. Key Design Decisions

| Decision | Chosen | Rejected | Rationale |
|---|---|---|---|
| Challenge visibility | All challenges visible from start | Sequential reveal | Full visibility gives users agency. 294K users abandoned before discovering partner actions. |
| Progression system | Visual progress tracker with milestone rewards | Per-challenge-only rewards | Milestone rewards incentivise breadth. Tiered experiment showed progressive commitment works. |
| Challenge gating | No hard gating; soft recommendations | Sequential unlock | Sequential gating produces the 40x drop-off. Soft recommendations preserve guidance without blocking. |
| Partner task structure | Progressive difficulty + monthly rotation | Static identical asks | Data shows identical asks for 3 months → declining conversion. Progressive asks mirror validated conversion ladder logic. |
| Reward design | Exclusive items + tiered FP + Mystery Box milestones | FP-only per challenge | 83.3% of BOFU users spend FP on profile items. Exclusive rewards create a reason to do partner tasks that gaming can't provide. |
| AL requirement | AL required for partner reward redemption (existing mechanic) | AL as a formal gate challenge | Keeps existing auto-claim/redemption gating. Separate AL experiment tests explicit vs implicit. |

---

## 5. User Stories / Requirements

| # | As a... | I want to... | So that... | Priority |
|---|---|---|---|---|
| 1 | FACEIT user | See all available challenges when I start a mission | I know what's required and can plan my approach | Must |
| 2 | FACEIT user | Complete challenges in any order I choose | I'm not blocked by a hard conversion gate | Must |
| 3 | FACEIT user | See my overall mission progress (visual tracker) | I feel motivated by advancement and know how close I am to rewards | Must |
| 4 | FACEIT user | Receive milestone rewards at progression thresholds | I have incentive to complete more challenges beyond the minimum | Should |
| 5 | FACEIT user | Receive a soft recommendation on optimal challenge order | I have guidance without being forced | Should |
| 6 | FACEIT user | See different partner challenges each month | I have a new reason to engage rather than the same ask I already declined | Must |
| 7 | FACEIT user | Start with a lower-commitment partner task and work up | I'm not immediately asked for the hardest action | Should |
| 8 | FACEIT user | Earn exclusive profile items from milestone completions | I get something I can't earn from gaming challenges alone | Must |
| 9 | Advertiser / Partner | Track individual challenge completions and conversion funnel stages | I can measure campaign performance by funnel stage (AL, C1, C2, C3) | Must |
| 10 | Advertiser / Partner | Define a library of acceptable challenge variants for rotation | I maintain control over what actions are incentivised | Must |
| 11 | Activation Ops | Configure challenge order flexibility per mission | I can choose between nonlinear and sequential for different campaigns | Should |
| 12 | Activation Ops | Set milestone thresholds and rewards per mission | I can customize progression incentives per partner | Should |
| 13 | Activation Ops | Rotate partner challenges monthly from a template library | I don't manually reconfigure the same tasks each month | Should |
| 14 | Data team | Track challenge completion order per user | I can analyse optimal user paths and progression patterns | Must |

---

## 6. Scope

### In Scope

**Pillar 1 — Nonlinear Structure:**
- New mission UX: all challenges visible, user-chosen completion order
- Progression tracker UI (visual progress indicator — bar, map, or board)
- Soft challenge recommendations ("Start here for best results")
- Backend support for nonlinear challenge state tracking
- Configuration option for Activation Ops to choose nonlinear vs sequential per mission

**Pillar 2 — Progressive Challenges & Rotation:**
- Progressive partner task difficulty within a single mission (e.g., 500 → 1,500 → 3,000 RUB)
- Challenge template library for Activation Ops to define per-tier partner task variants
- Monthly rotation system — auto-assign different partner challenges each month from the library
- Partner approval workflow for new challenge variants

**Pillar 3 — Reward Rebalancing:**
- Milestone reward system (configurable thresholds and rewards)
- Exclusive reward items for partner task completion (profile cards, frames, limited-edition items)
- Tiered reward escalation: higher-difficulty partner tasks earn proportionally better rewards
- Mystery Box / variable reward option on milestone completions

**Cross-cutting:**
- Analytics instrumentation: challenge order, progression events, milestone claims, reward type effectiveness

### Out of Scope
- Changes to the Account Linkage flow itself (separate experiment)
- Localisation of mission copy (separate experiment)
- Mobile app changes (web-first for MVP)
- Engagement Engine integration with nonlinear missions (future iteration)
- Partner-side changes (deposit flow UX, KYC process — outside FACEIT control)

### Future Considerations
- Engagement Engine notifications adapted for nonlinear progress ("You've completed 3/5 — only 2 more!")
- Dynamic challenge difficulty adjustment based on user segment (TOFU/MOFU/BOFU)
- Partner-specific progression templates
- Multi-mission progression (cross-mission advancement similar to Mission Chain)
- Shop integration: partner task rewards purchasable only via mission milestone (creates scarcity)

---

## 7. Technical Considerations

### Pillar 1 — Nonlinear Structure

- **Challenge state model**: Current model assumes sequential ordering (challenge N unlocks only after N-1 completes). Needs refactor to support concurrent active challenges with independent completion states. Each challenge tracks its own `status` (available → active → complete) independently.
- **Progression engine**: New component to calculate and emit progression events (% complete, milestone reached) based on weighted or unweighted challenge completions. Must support configurable weighting (e.g., partner challenges worth 2x for progression purposes).
- **Configuration schema**: Mission configuration needs a `mode` field (sequential | nonlinear | hybrid) and milestone definition schema (threshold, reward type, reward value). Hybrid mode allows some challenges to remain sequential while others are flexible.
- **Auto-claim**: Existing auto-claim mechanics (reward on challenge completion) must work for any challenge independently, not just sequentially.

### Pillar 2 — Progressive Challenges & Rotation

- **Challenge template library**: New data model to store partner-approved challenge variants per tier. Each template defines: action type (deposit, bet, trade), threshold amount, currency, minimum odds (where applicable), localised copy, and reward tier. Templates are versioned and require partner sign-off before activation.
- **Progressive challenge graph**: Within a single mission, partner challenges form a directed graph (e.g., Deposit 500 → Deposit 1,500 → Deposit 3,000). The backend must support ordered sub-sequences within an otherwise nonlinear mission. Completion of a lower-tier partner task unlocks the next tier.
- **Monthly rotation scheduler**: Automated system to assign challenge templates to upcoming campaigns. Activation Ops configures the rotation pool; the scheduler ensures no user sees the same partner challenge two consecutive months. Requires a `last_assigned_template_id` per user-tier to prevent repeats.
- **Campaign generation**: Currently campaigns are manually configured. Rotation requires either (a) auto-generating monthly campaigns from templates, or (b) a "template swap" mechanism that updates challenge details within an existing campaign shell. Option (b) is lower-risk for MVP.
- **Partner challenge validation**: Partner challenges have contractual constraints (minimum deposit amounts, odds thresholds). The template library must enforce validation rules per partner so Activation Ops cannot accidentally configure a challenge below contractual minimums.

### Pillar 3 — Reward Rebalancing

- **Milestone reward system**: Extends the existing per-challenge reward model with a new milestone layer. Milestones are defined as threshold conditions (e.g., "complete ≥3 challenges including ≥1 partner") and map to reward payloads. Must support multiple milestones per mission with escalating rewards.
- **Exclusive item integration**: Requires integration with the FACEIT Shop item catalogue to create and distribute exclusive profile items (cards, frames, bundles) as mission rewards. These items must be flagged as `mission_exclusive` to prevent purchase via FP — scarcity drives value.
- **Mystery Box on milestones**: Reuse the Mystery Box mechanic (validated +61% AL uplift, Jan/Feb 2026) for milestone reward delivery. Technical implementation already exists from the TOFU experiment; needs adaptation to trigger on milestone events rather than AL completion.
- **Tiered reward curve**: Reward values must scale with partner task difficulty. Configuration schema: `{challenge_tier: "low" | "mid" | "high", reward_type: "fp" | "item" | "mystery_box", reward_value: number, reward_item_id?: string}`. Activation Ops sets the curve per mission.
- **Reward analytics**: New BQ events to track reward type effectiveness — which reward types (FP, exclusive items, Mystery Box) drive higher partner task completion. Essential for iterating on reward calibration post-launch.

### Cross-cutting

- **BQ instrumentation**: New events for challenge selection order, progression milestones, milestone reward claims, reward type, template rotation assignments, and user path analysis. Must integrate with existing `UserMissions` and `UserRewards` tables. Add `template_id` and `rotation_month` fields to campaign/mission events.
- **Trust Modal**: Must remain in the AL flow regardless of mission structure (per Trust Modal experiment conclusion).
- **CDP compatibility**: Challenge completion events must still feed CDP segmentation correctly regardless of completion order. Partner funnel stages (TOFU/MOFU/BOFU) are based on conversion status, not challenge order. Progressive partner tasks (Deposit 500 → 1,500 → 3,000) must each emit the correct CDP conversion event.
- **Performance**: Nonlinear state tracking + milestone evaluation on every challenge completion adds computation. Pre-compute milestone eligibility on challenge state change rather than evaluating on page load.

---

## 8. Dependencies & Risks

### Dependencies

| Dependency | Impact | Pillar | Mitigation |
|---|---|---|---|
| Backend challenge state refactor (sequential → nonlinear) | High | P1 | Scope MVP to one partner first (Tradeit — most diverse geos, implicit AL reduces complexity) |
| Mission UI redesign (progression tracker + milestone display) | High | P1, P3 | Work with Design (Anouk) to prototype. Use existing Mission page layout as base. |
| Activation Ops tooling (mission config UI) | Medium | P1, P2 | Phase 1: manual config via admin. Phase 2: self-serve UI. |
| Analytics instrumentation (new BQ events) | Medium | All | Data team (Isabel, Kerrin) to scope instrumentation alongside dev. |
| Partner expectations on funnel reporting | Medium | All | Ensure challenge-level reporting remains intact. Add progression-level as a new metric layer. |
| **Partner approval of challenge variants** | **High** | **P2** | Each partner must pre-approve a library of acceptable challenge variants (amounts, actions, thresholds). Winline requires Commercial lead to negotiate variant ranges. Start with low-risk variants (same action, different amounts) before introducing new action types. |
| **Exclusive reward item creation** | **Medium** | **P3** | Design (Anouk) + Shop team to create mission-exclusive profile cards, frames, and bundles. Requires lead time for asset creation. Unblock by starting with existing limited-edition items or recoloured variants of popular items. |
| **Shop/item catalogue integration** | **Medium** | **P3** | Mission reward system must read from the Shop item catalogue to assign exclusive items. Requires Shop team API support for `mission_exclusive` flag and restricted distribution. |
| **Monthly Activation Ops cadence** | **Low** | **P2** | Rotation system reduces per-campaign manual work but requires Activation Ops to maintain the template library and review monthly assignments. If understaffed, rotation defaults to auto-assign from the approved pool. |

### Risks

| Risk | Impact | Likelihood | Pillar | Mitigation |
|---|---|---|---|---|
| Users skip partner challenges entirely and only do gaming tasks | High | High | P1 | Milestone rewards gate high-value prizes behind mixed completion (e.g., "Complete ≥1 partner + ≥2 gaming challenges for bonus"). Reward structure incentivises breadth. |
| Nonlinear structure confuses users (too many options) | Medium | Medium | P1 | Soft recommendations and progressive disclosure. Limit to 5–6 challenges per mission. |
| Partner conversion quality drops (more AL but lower C1/C2) | Medium | Medium | P1, P2 | Guardrail metric: downstream quality must remain neutral. A/B test before full rollout. |
| **Progressive asks cannibalise higher-tier conversions** — users settle for "Deposit 500 RUB" and never progress to 3,000 | **High** | **Medium** | **P2** | Reward curve must make higher tiers significantly more attractive. Lower-tier partner tasks get modest rewards; the exclusive/high-value items require completing the full progressive ladder. Monitor tier-by-tier completion rates. |
| **Challenge rotation reduces partner reporting comparability** — different challenges each month makes MoM comparison harder | **Medium** | **High** | **P2** | Tag each challenge template with a `tier` and `action_type` so reporting can aggregate by tier (FTD, WHALE) and action (deposit, bet) even as specific amounts rotate. Provide partners a "template performance" dashboard. |
| **Exclusive reward items lose scarcity value** if too many are created or if users can obtain them elsewhere | **Medium** | **Low** | **P3** | Strict `mission_exclusive` flag — items cannot be purchased in shop. Rotate exclusive items seasonally. Cap the number of exclusive items per quarter. |
| **Mystery Box on milestones dilutes downstream quality** (replicating the Jan/Feb 2026 result: +61% AL but lower C2 quality) | **Medium** | **Medium** | **P3** | Apply Mystery Box to mid-funnel milestones (post-AL), not TOFU linkage. Quality guardrail on C1/C2 rates. If quality drops >10%, disable Mystery Box and revert to deterministic rewards. |
| **Rotation system technical complexity** delays MVP | **Medium** | **Medium** | **P2** | MVP: manual template assignment by Activation Ops per month (no automation). Phase 2: automated rotation scheduler. This derisks the technical delivery without losing the rotation benefit. |

---

## 9. Open Questions

### Structure (Pillar 1)

- [ ] What is the optimal number of challenges per nonlinear mission? (5? 7? Configurable per partner?)
- [ ] Should milestone thresholds be based on challenge count or weighted by challenge type (partner challenges worth more toward progression)?
- [ ] Can Activation Ops configure hybrid missions (some challenges sequential, others flexible)?
- [ ] What's the engineering effort estimate for the backend challenge state refactor?
- [ ] What is the minimum viable progression UI? (Progress bar vs full mission map/board?)
- [ ] How does nonlinear interact with Mission Chain (multi-mission progression)? Phase 2?

### Progressive Challenges & Rotation (Pillar 2)

- [ ] What progressive deposit ladder is acceptable to Winline? (500 → 1,500 → 3,000 RUB, or different steps?) Requires Commercial input.
- [ ] How many challenge variants per tier are needed for meaningful rotation? (Minimum 3 per tier for quarterly non-repetition.)
- [ ] Can partners approve a variant range (e.g., "deposits between 500–5,000 RUB") rather than individual challenges? This would simplify the approval workflow.
- [ ] What's the rotation cadence — monthly (aligned with current campaign cadence) or bi-weekly?
- [ ] Should progressive partner asks be the default, or configurable per partner? Some partners may prefer a single direct ask.
- [ ] How do we handle users mid-mission when challenges rotate at month end? Grandfather existing missions or swap mid-flight?

### Reward Rebalancing (Pillar 3)

- [ ] What exclusive items should we create for the first mission cycle? Design team capacity and lead time needed.
- [ ] Should Mystery Box on milestones use the same probability distribution as the TOFU experiment, or a different one calibrated for BOFU?
- [ ] What's the right FP-to-exclusive-item ratio on the reward curve? (e.g., lower-tier = FP only, mid-tier = FP + common item, high-tier = exclusive item + Mystery Box)
- [ ] Can we A/B test reward types (FP-only vs exclusive items vs Mystery Box) within the same mission structure to isolate the reward effect?
- [ ] How do we prevent reward inflation over time as more exclusive items are created?

### Cross-cutting

- [x] ~~Should we MVP with a single partner?~~ → **Yes — Tradeit recommended** (most diverse geos, implicit AL, lower-value AL reduces experiment risk). Winline BOFU data (Section 2a) provides the business case; Tradeit provides the lowest-risk MVP.
- [ ] Will nonlinear missions require changes to partner campaign reporting format?
- [ ] How does the Engagement Engine adapt notifications for nonlinear progress? (Likely future scope.)
- [ ] What's the phased rollout plan? Suggested: Pillar 1 (structure) first → measure → layer Pillar 3 (rewards) → layer Pillar 2 (rotation). Or ship Pillars 1+3 together and add rotation later?

---

## 10. Appendix

**Referenced data sources:**
- BQ: `business-intelligence-prod.CampaignService.UserMissions`
- BQ: `business-intelligence-prod.CampaignService.UserRewards`
- BQ: `business-intelligence-prod.CampaignService.Campaigns`
- BQ: `business-intelligence-prod.dbt_user.dim__users` (user activity, verification, subscription, geo)
- Looker: `user_account_linkage_operation_v1`
- NSM values: `data/brand_integrations/NSM per Partner - Value.tsv`
- CDP (Snowflake): `analytics_rep.cdp_service.user_events` — Winline deposit (`last_dep`) and mission (`task_*`) events
- Cross-platform analysis: `data/brand_integrations/winline_cdp_cohorts_for_bq.csv` (155K users, cohort-tagged)
- BQ: `business-intelligence-prod.CampaignService.UserMissions` (BOFU mission activation, Feb–Apr 2026)
- BQ: `business-intelligence-prod.CampaignService.Campaigns` (challenge configurations, unnested missions array)

**Referenced documents:**
- March 2026 Mission Review: `docs/product_briefs/march-mission-review-2026.md`
- NSM Framework: `reference/NSM_ Ads & Partnerships.md`
- Trust Modal Conclusion: `docs/product_briefs/trust-modal-experiment-conclusion.md`
- Brand Integrations Context: `context/brand-integrations.md`
- Experiments Log: `context/experiments.md`
- Missions Product Doc: `docs/product_documentation/Missions for AI.md`

**NSM values per conversion point (for impact sizing):**

| Partner | AL | C1 | C2 | C3 |
|---|---|---|---|---|
| Winline | €4.33 | €8.66 | €121.10 | €4.33 |
| Tradeit | €0.38 | €0.04–€0.18 | €8.75 | €35.00 |
| WhiteMarket | €0.38 | €0.05–€0.25 | €12.50 | €50.00 |
| PaySafe | €2.50 | €5.00 | €17.50 | TBD |
