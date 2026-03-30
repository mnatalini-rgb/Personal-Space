# Brand Integrations — Product Context

## What It Is

Brand Integrations is a performance-oriented monetisation product line. Unlike traditional advertising (which sells awareness or clicks), Brand Integrations drives **verified user actions** for partners. Partners pay for outcomes, not impressions.

This is why deals are **long-term partnerships**, not one-off campaigns. The depth of integration — CRM connectivity, account linkage, CDP segmentation — requires trust, setup time, and ongoing data sharing between FACEIT and the partner.

---

## Product Suite

### Missions
- **Type**: 1:1 task-based competition
- **Duration**: Typically 1 month
- **Activation time**: 5 working days
- **Primary KPI**: Engagement + User Acquisition (account linkage, conversions)
- **Key features**: Account Linkage, Prize Expiration, Customer Data Platform (CDP)
- **How it works**: Users auto-join when active on platform (play a match). They complete a series of in-game tasks to earn prizes. Tasks can be gated behind account linkage.
- **Multiple missions** from different advertisers can run concurrently (no geo exclusivity constraint).

### Brand Takeover
- **Type**: Ladder-based competition (individual & group)
- **Duration**: 3 or 7 days (typically weekly)
- **Activation time**: 5 working days
- **Primary KPI**: Brand Impressions (9–20 per unique player per event, depending on geo, duration, drops, match skin)
- **Key features**: Drops, Account Linkage, Match Skin, Prize Expiration, Rewarded Video (in testing)
- **Geo-exclusive**: Cannot run two Brand Takeovers in the same geo simultaneously (same match would count points for both).
- **How it works**: Users auto-join when active. Post-match modal notifies them. Rankings update throughout the event. Prizes distributed by rank 24h after event ends.

### Drops
- **Part of**: Brand Takeover (add-on feature, not standalone)
- **Purpose**: Increase engagement and Brand Impressions during a Branded Event (each drop = 3 brand impressions)
- **Distribution**: Random, post-match (via "rider" component + activity notification). Algorithm favours more active players and broad distribution.
- **Claim window**: 12 hours. Unclaimed drops re-enter the prize pool.
- **Top Tier Drops**: Rare, time-specific drops to incentivise daily engagement throughout the event.

---

## The Partner Model

### Why Long-Term Partnerships
Partners sign long-term deals because:
1. **CRM integration takes time** — FACEIT integrates with the partner's CRM to receive enriched user data back post-linkage. Integration takes up to 2 weeks including testing.
2. **Data agreements are bespoke** — specific data points (e.g. KYC status, deposit events) are agreed upfront per partnership.
3. **KPIs are bespoke** — partners agree a primary KPI at deal start (e.g. "110K first-time deposits for Winline RU").
4. **The value compounds** — as users move down the funnel over time, later conversions (C2, C3) deliver higher-value outcomes for the partner.

### Partner Accounts

#### Winline
- **Category**: Betting platform
- **Geos**: Russia (primary, biggest market), Belarus (BY) and Kazakhstan (KZ) are much smaller
- **Contract year**: Y3 — starting March/April. This is the final year of the contract.
- **Y1–Y2 KPI**: First-Time Deposit (FTD). Target example: 110K FTDs in RU.
- **Y3 KPI**: TBC. Strategy shift — stopped counting FTDs. Focus has moved to the **bottom of the funnel** (BOFU) where strong engagement has been observed. Mission performance data (Y1–Y3) to be added later.
- **Funnel**: Account Linkage → KYC → FTD (C2) → deeper deposit/betting milestones (C3)

**NSM Values per Conversion Point (Winline)**

| Conversion Point | € Value |
|-----------------|---------|
| Account Linkage | €4.33 |
| KYC | €8.66 |
| First Time Deposit | €121.10 |
| Second Deposit | €4.33 |

**Winline Custom Tasks** (bottom-of-funnel BOFU engagement, task IDs mapped to event types):

| Task ID | Event Type | Description |
|---------|-----------|-------------|
| 867 | task_first_dep_500 | First deposit ≥ 500 RUB |
| 874 | task_dep_3000 | Deposit ≥ 3,000 RUB |
| 875 | task_bet_5000 | Bet ≥ 5,000 RUB |
| 876 | task_bet_25000 | Bet ≥ 25,000 RUB |
| 869 | task_bet_1000 | Bet ≥ 1,000 RUB |
| 889 | task_dep_5000 | Deposit ≥ 5,000 RUB |
| 1118 | task_dep_1111 | Deposit amount 1,111 RUB |
| 1119 | task_dep_2222 | Deposit amount 2,222 RUB |
| 1120 | task_bet_4444 | Bet amount 4,444 RUB |
| 1121 | task_bet_5555 | Bet amount 5,555 RUB |
| 1148 | task_bet_3333 | Bet amount 3,333 RUB |

**CDP Data — All Partners (all-time since Y1)**

> **Important caveats** (apply to all partners):
> 1. This reflects users who linked their account and the CDP events recorded. It does NOT represent performance driven by FACEIT campaigns — users may have already been active customers before linking.
> 2. Data spans multiple years. Not all linked users are still active on FACEIT.
> 3. Attributable campaign performance will be documented separately once Mission performance data is available.

Source: `data/brand_integrations/faceit_snowflake_analytics rep__cdp_service__user_events 2026-03-13T1619.csv`

---

**Tradeit**

| Event Type | Distinct Users |
|-----------|---------------|
| Account Linkage (tradeit) | 343,295 |
| User passes identification | 249,015 |
| Trade (any) | 103,311 |
| Trade ≥$5 | 38,633 |
| Notification | 30,987 |
| Trade ≥$250 | 12,229 |
| Buy | 6,705 |
| Sell or Buy | 4,769 |
| Sell | 3,936 |
| Trade ≥$1,000 | 1,443 |
| Sell or Buy ≥$200 | 438 |
| Trade ≥$500 | 41 |

---

**WhiteMarket**

| Event Type | Distinct Users |
|-----------|---------------|
| Account Linkage (whitemarket) | 627,255 |
| Email confirmed | 494,554 |
| Deposit success | 38,433 |
| Deal buy | 31,084 |
| KYC passed | 25,708 |
| Deal sell | 5,411 |
| Deal buy ≥$200 | 1,061 |
| Deal buy ≥$500 | 351 |

---

**Winline — Russia (RU)**

| Event Type | Distinct Users |
|-----------|---------------|
| Account Linkage | 369,107 |
| Registration | 368,996 |
| Identification (KYC) | 285,647 |
| Legal | 232,352 |
| First Deposit | 206,700 |
| First Bet | 199,670 |
| Last Deposit | 153,300 |
| Second Deposit | 85,187 |
| First Deposit (post-bind) | 36,878 |
| CRM signal 0 | 8,874 |
| Reactivated Deposit | 3,202 |

Custom task completions (BOFU):

| Task | Distinct Users |
|------|---------------|
| task_dep_3000 (≥3,000 RUB deposit) | 27,727 |
| task_bet_5000 (≥5,000 RUB bet) | 20,116 |
| task_dep_5000 (≥5,000 RUB deposit) | 12,034 |
| task_bet_25000 (≥25,000 RUB bet) | 7,623 |
| task_dep (generic deposit) | 8,675 |
| task_bet (generic bet) | 4,240 |
| task_first_dep_500 (first dep ≥500 RUB) | 3,571 |
| task_bet_2500 (≥2,500 RUB bet) | 3,569 |
| task_dep_1111 | 1,199 |
| task_bet_1000 (≥1,000 RUB bet) | 1,097 |
| task_dep_2222 | 798 |
| task_bet_4444 | 168 |
| task_bet_5555 | 75 |
| task_bet_3333 | 41 |

---

**Winline — Belarus (BY)**

| Event Type | Distinct Users |
|-----------|---------------|
| Account Linkage (winline_by) | 13,728 |
| Registration | 13,729 |
| Identification (KYC) | 5,166 |
| First Deposit | 4,749 |
| First Bet | 4,585 |
| Last Deposit | 4,748 |
| Last Bet | 4,584 |
| First Deposit (post-bind) | 2,700 |
| CRM signal 0 | 2,677 |
| CRM signal 1 | 1,655 |
| Reactivated Deposit | 19 |

---

**Winline — Kazakhstan (KZ)**

| Event Type | Distinct Users |
|-----------|---------------|
| Account Linkage (winline_kz) | 25,187 |
| Registration | 25,135 |
| Identification (KYC) | 5,970 |
| First Deposit | 4,203 |
| First Bet | 4,693 |
| Last Deposit | 4,201 |
| Last Bet | 4,693 |
| First Deposit (post-bind) | 1,990 |
| CRM signal 0 | 2,515 |
| CRM signal 1 | 434 |
| Reactivated Deposit | 47 |

#### Tradeit
- **Category**: Skin trading platform
- **Contract year**: Y2 — contract just signed
- **KPIs**: Account Linkage (via Steam) and trades
- **Geos**: North America, CIS, MENA, APAC (Y2 contract)
- **Notes**: Steam account linkage is the primary acquisition mechanism; trade activity is the downstream conversion

**Account Linkage model (unique to Tradeit)**:
Unlike other partners (Winline, WhiteMarket, PaySafe), Tradeit does **not** have an explicit "Link your account" challenge step in the mission flow. Instead:
- AL is **implicit** — users must link their Tradeit/Steam account to claim any reward from the mission
- A UI element on the mission page provides a CTA to link with a brief explanation of benefits (auto-claim, safer transactions, etc.)
- This means **every user who claims a prize has linked**, but AL is not tracked as a separate challenge completion in the mission data
- For NSM purposes, **AL ≈ "Prizes Claimed" on the first challenge** (Task 1) as a proxy — though this slightly undercounts users who link but don't claim
- All other partners gate AL as a formal challenge (explicit step in the mission), making it a distinct trackable data point

**Mission segmentation (2026)**:
Tradeit runs 3 mission segments per region, targeting users at different funnel positions:
- **TOFU ("Non-Activated / Agnostic")**: Users who haven't linked. 3 challenges: Play 1 match → Trade any item → Trade $250+
- **MOFU ("Account Linked, No Trade")**: Linked but never traded. 3 challenges: Play 1 match → Trade any item → Trade $250+
- **BOFU ("Account Linked + Trade Made")**: Already traded. 2 challenges: Play 1 match → Trade $250+

**Conversion ladder mapping (Tradeit → NSM)**:
- AL = Account Linkage (implicit via reward claim)
- C1 = First trade (any item)
- C2 = High-value trade ($250+)
- C3 = Not currently tracked (potential: $1,000+ trades or repeat trading activity)

**NSM Values per Conversion Point (Tradeit)**

| Conversion Point | € Value |
|-----------------|---------|
| Account Linkage | €0.38 |
| Trade 1 | €0.04 |
| Trade 5 | €0.18 |
| Trade 250 | €8.75 |
| Trade 1,000 | €35.00 |

#### WhiteMarket
- **Category**: Skin marketplace (historical partner)
- **Contract year**: Y3
- **Notes**: Significantly reduced budget in Y3 compared to previous years

**NSM Values per Conversion Point (WhiteMarket)**

| Conversion Point | € Value |
|-----------------|---------|
| Account Linkage | €0.38 |
| Trade 1 | €0.05 |
| Trade 5 | €0.25 |
| Trade 250 | €12.50 |
| Trade 1,000 | €50.00 |

#### WhiteBit
- **Category**: Crypto exchange / financial platform
- **Contract year**: Y1 completed — partnership ended
- **Status**: Past partner. Budget significantly reduced over time as the user base became saturated. No active contract.
- **Notes**: Relevant as historical context for crypto/financial vertical; demonstrates the saturation risk for single-geo performance campaigns

#### PaySafe
- **Category**: Financial services / digital wallet
- **Contract year**: Contract currently being signed
- **KPI**: Deposits onto the Paysafe wallet (not credit card sign-ups as initially noted)
- **Geos**: Germany, Poland, France, Spain, and the Nordics (excluding Sweden — "without SE")
- **Funnel**: Account Linkage → KYC → Deposit — provisional, awaiting partner validation
- **Notes**: Account linkage will be the primary mechanism driving conversion. Western European focus — meaningfully different geo profile from Winline (RU-heavy).

**NSM Values per Conversion Point (PaySafe)**

| Conversion Point | € Value |
|-----------------|---------|
| Account Linkage | €2.50 |
| KYC | €5.00 |
| First Time Deposit | €17.50 |

Source: `data/brand_integrations/NSM per Partner - Value.tsv`

---

## Engagement Engine

The Engagement Engine (EE) is a re-engagement feature that sends custom activity notifications to users who are stuck on a specific mission challenge. It uses psychological frameworks and AI-generated copy to prompt task completion.

### How It Works

- Monitors user progress through mission tasks
- Identifies users who are **stuck** on a specific challenge (eligible for a reminder)
- Sends a push/activity notification with AI-generated contextual copy
- The AI ensures notifications are unique — no repeat messaging — to avoid banner blindness

### Psychological Frameworks Used

| Framework | Description |
|-----------|-------------|
| Reward Motivation | Focus on what the user stands to gain |
| Live Reward Rush | Urgency framing — limited time, act now |
| Progress Completion | Near-miss framing — you're almost there |
| Competitive Pressure | Social comparison — others are completing this |

### Experiment Results (First Test — Winline BOFU)

These are the key findings from the first EE experiment, run on Winline BOFU users (existing depositors completing deposit/bet challenges):

**1. Reminders work — but modestly on average**
- Overall uplift in task completions: ~+0.2 percentage points
- Small on average, but meaningful at scale given user volumes

**2. Psychological framing significantly affects CTR**

| Framework | CTR |
|-----------|-----|
| Progress Completion | 10.6% |
| Urgency / Live Reward Rush | 9.4% |
| Skill | 7.8% |
| Competitive Pressure | 7.4% |

Progress and urgency/reward hooks consistently outperform skill and competitive pressure.

**3. Most effective for BOFU users already engaged with the brand**
- Medium-barrier actions (e.g. deposit ≥3,000 RUB, bet ≥1,000 RUB) showed both high CTR and strong completion uplifts
- The EE is **not sufficient to move users from TOFU** — it works for users who are already active with the partner, not for cold acquisition

**4. Declining reach in later reminders = attrition, not completion**
- Fewer unique users are reached by Day 7 and Day 10 reminders
- The dominant cause is **user inactivity over time** — users disengage from FACEIT, shrinking the eligible pool
- Task completions do contribute modestly to the decline, but are not the primary driver

### Strategic Implications

- EE is a **BOFU retention tool**, not an acquisition tool — position it accordingly
- Prioritise **Progress** and **Urgency/Reward Rush** frameworks in future deployments
- Scale impact depends on eligible user pool size — EE's value grows with larger engaged user bases
- Winline is currently the primary use case; applicability to other partners depends on whether they have meaningful BOFU depth

---

## Account Linkage

Account Linkage is the foundational integration layer for Brand Integrations. It:
- Creates a 1:1 relationship between a FACEIT user and the partner platform
- Enables auto-claim of prizes (no code handling by the user)
- Gates prize eligibility behind account creation on the partner side
- Feeds data into the CDP once the user links

**Why it matters strategically:**
Before Account Linkage, users could claim codes and resell them — prizes reached the wrong audience and partner leads were low-quality. Account Linkage eliminates code reselling, guarantees account creation, and creates a verified, fraudproof lead for the partner.

**Linkage entry points**: Mission page, Branded Event page, Drop page, Order page.

**Technical integration**: Up to 2 weeks including testing.
Docs: https://docs.faceit.com/getting-started/authentication/account-linkage/#authorization

---

## Customer Data Platform (CDP)

Once a user links their account, their data flows into the CDP. The CDP:
- Stores enriched data per user, siloed per partner
- Receives data points from the partner's CRM (e.g. registration status, KYC, last deposit, last bet)
- Enables segmentation of users by their position in the **partner funnel**
- Powers **Custom Missions** — missions that target specific user segments with specific calls to action

The data points received from each partner are **agreed at partnership start** and vary by partner and country (privacy assessments may be required).

---

## Partner Funnel & Segmentation (TOFU / MOFU / BOFU)

Partners define their funnel, and FACEIT maps FACEIT users to funnel stages using enriched CDP data.

**Example: Winline (RU) — Betting Platform**

| Stage | Label | Definition |
|-------|-------|------------|
| TOFU | Top of Funnel | User has NOT linked their FACEIT account with Winline |
| MOFU | Middle of Funnel | User has linked account AND/OR passed KYC — but has NOT made a first deposit |
| BOFU | Bottom of Funnel | User has made a First-Time Deposit (FTD) |

**Conversion path**: Account Linkage → KYC → First Deposit (FTD)

This maps directly to the NSM conversion ladder:
- AL = Account Linkage (TOFU → MOFU entry)
- C1 = KYC completion (MOFU)
- C2 = First deposit (MOFU → BOFU)
- C3 = Deeper deposit/betting milestones (BOFU depth)

---

## Prizes

Prizes are the user-facing incentive that drives participation. Types:
- Advertiser vouchers (free bets, raffle tickets, credits)
- Embedded codes in URL
- Material prizes (partner-fulfilled)
- FACEIT Points
- FACEIT Premium subscriptions
- FACEIT Skins

**Important constraints**:
- FACEIT cannot run raffles (legal) — raffles must be run on the partner side
- Prizes can be gated behind mandatory account linkage
- Prizes have configurable expiration times (set by advertiser)
- Prizes distributed 24h after competition end (Branded Events)

---

## Loyalty / Tier Progression

FACEIT has a loyalty tier system used in high-value partner campaigns to drive repeated engagement and long-term retention.

**Tier ladder (ascending):**

| Tier | Notes |
|------|-------|
| Subscriber | Entry level |
| Gold | |
| Platinum | |
| Diamond | |
| Elite | |
| Legend | Top tier |

Used to incentivise:
- Repeated deposits or purchases
- Weekly engagement milestones
- Long-term partner retention objectives

---

## NSM Connection

Brand Integrations performance is measured via the **OVU / EBU component of TAVI**:

**OVU = 3·AL + 6·C1 + 9·C2 + 3·C3**

Where AL, C1, C2, C3 map directly to the partner funnel stages above.

Full framework: `context/metrics.md` and `reference/NSM_ Ads & Partnerships.md`

---

## Legal & Privacy

- Missions with account linkage require a partner-specific privacy policy displayed on the mission page
- Depending on country and data points shared, a privacy risk assessment may be required
- Example: [Winline Mission Privacy Notice](https://support.faceit.com/hc/en-us/articles/13483161419420-Winline-Mission-Privacy-Notice)
- Privacy contact: @Akkeroos Kremers
