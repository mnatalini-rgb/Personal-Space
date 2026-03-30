I # Brand Integrations — Overview

**Owner**: Moritz Natalini, PM Monetisation
**Last updated**: March 2026

---

## What Is Brand Integrations?

Brand Integrations (BI) is FACEIT's performance monetisation product line. Unlike advertising — which sells impressions or awareness — BI drives **verified user actions** for partners. Partners pay for outcomes: account registrations, KYC completions, deposits, trades.

Deals are long-term partnerships, not one-off campaigns. The depth of integration (CRM connectivity, account linkage, CDP segmentation) requires trust, setup time, and bespoke data agreements between FACEIT and each partner.

Brand Integrations currently accounts for approximately **80% of total monetisation revenue**.

---

## Product Suite

### Missions

Task-based competitions that incentivise users to complete specific actions in exchange for prizes.

| Attribute | Detail |
|-----------|--------|
| Type | 1:1 task-based competition |
| Duration | Typically 1 month |
| Activation time | 5 working days |
| Primary KPI | Engagement + User Acquisition (account linkage, conversions) |
| Key features | Account Linkage, Prize Expiration, CDP |
| Concurrency | Multiple missions from different advertisers can run simultaneously — no geo exclusivity |

**How it works**: Users auto-join when active on FACEIT (play a match). They complete a series of tasks to earn prizes. Tasks can be gated behind account linkage with the partner.

---

### Brand Takeover

Ladder-based competitions that drive brand impressions through ranked engagement.

| Attribute | Detail |
|-----------|--------|
| Type | Ladder-based competition (individual & group) |
| Duration | 3 or 7 days (typically weekly) |
| Activation time | 5 working days |
| Primary KPI | Brand Impressions (9–20 per unique player per event) |
| Key features | Drops, Account Linkage, Match Skin, Prize Expiration, Rewarded Video (in testing) |
| Geo exclusivity | Cannot run two Brand Takeovers in the same geo simultaneously |

**How it works**: Users auto-join when active. A post-match modal notifies them of the event. Rankings update throughout. Prizes distributed by rank 24 hours after the event ends.

**Important dependency**: Brand Takeover uses the ladder service, owned by the **Matchmaking team** — not the BI team. Any ladder changes require cross-team coordination.

---

### Drops

An add-on feature within Brand Takeover, not a standalone product.

- Each drop = **3 brand impressions**
- Distributed randomly post-match. Algorithm favours active players but ensures broad distribution.
- **Claim window**: 12 hours. Unclaimed drops re-enter the prize pool.
- **Top Tier Drops**: Rare, time-specific drops to incentivise daily engagement throughout the event.

---

### Rewarded Video *(in testing)*

A video ad triggered at the **Drop claim moment** — the user watches a short video in exchange for receiving the drop.

- Bridges BI (performance, engagement) and standard advertising (video views)
- Creates a natural upsell: Brand Takeover clients can add video inventory without a separate campaign
- **Current test**: Logitech — 4 Brand Takeovers purchased (7-day format), currently running the 3rd (March 2026). Sold by Adam Goh.

---

## How Partners Work

### Why Long-Term Deals

1. **CRM integration takes time** — FACEIT integrates with the partner's CRM to receive enriched user data post-linkage. Integration takes up to 2 weeks including testing.
2. **Data agreements are bespoke** — specific data points (KYC status, deposit events, etc.) are agreed upfront per partnership.
3. **KPIs are bespoke** — each partner agrees a primary KPI at deal start.
4. **Value compounds** — users moving down the funnel over time deliver higher-value outcomes for the partner.

### The Conversion Funnel

FACEIT maps users to partner funnel stages using CDP data:

| Stage | Label | Typical Definition |
|-------|-------|-------------------|
| TOFU | Top of Funnel | User has not linked their FACEIT account with the partner |
| MOFU | Middle of Funnel | User has linked and/or completed KYC — but not yet converted (deposited, traded) |
| BOFU | Bottom of Funnel | User has made a first deposit, trade, or equivalent conversion |

This maps to the NSM conversion ladder: **AL → C1 → C2 → C3**

---

## Partner Accounts

### Winline

| Attribute | Detail |
|-----------|--------|
| Category | Betting platform |
| Geos | Russia (primary), Belarus (BY), Kazakhstan (KZ) |
| Contract year | Y3 — starting March/April 2026. Final year. |
| Y1–Y2 KPI | First-Time Deposit (FTD). Example target: 110K FTDs in RU. |
| Y3 KPI | TBC — strategy shift away from FTD. BOFU focus. |
| Funnel | Account Linkage → KYC → FTD → deeper deposit/betting milestones |

**NSM Values (Winline)**

| Conversion Point | € Value |
|-----------------|---------|
| Account Linkage | €4.33 |
| KYC | €8.66 |
| First Time Deposit | €121.10 |
| Second Deposit | €4.33 |

**BOFU Custom Tasks** (task IDs mapped to betting/deposit events):

| Task | Description |
|------|-------------|
| task_first_dep_500 | First deposit ≥ 500 RUB |
| task_dep_3000 | Deposit ≥ 3,000 RUB |
| task_bet_5000 | Bet ≥ 5,000 RUB |
| task_bet_25000 | Bet ≥ 25,000 RUB |
| task_bet_1000 | Bet ≥ 1,000 RUB |
| task_dep_5000 | Deposit ≥ 5,000 RUB |
| task_dep_1111 | Deposit amount 1,111 RUB |
| task_dep_2222 | Deposit amount 2,222 RUB |
| task_bet_4444 | Bet amount 4,444 RUB |
| task_bet_5555 | Bet amount 5,555 RUB |
| task_bet_3333 | Bet amount 3,333 RUB |

**CDP Snapshot — Winline RU** *(all-time since Y1 — see attribution caveats below)*

| Event | Distinct Users |
|-------|---------------|
| Account Linkage | 369,107 |
| KYC | 285,647 |
| First Deposit | 206,700 |
| First Bet | 199,670 |
| Second Deposit | 85,187 |
| First Deposit (post-bind) | 36,878 |

Top BOFU task completions: dep_3000 (27,727), bet_5000 (20,116), dep_5000 (12,034), bet_25000 (7,623)

**CDP Snapshot — Winline BY / KZ** *(smaller geos)*

| Event | BY | KZ |
|-------|----|----|
| Account Linkage | 13,728 | 25,187 |
| KYC | 5,166 | 5,970 |
| First Deposit | 4,749 | 4,203 |
| First Deposit (post-bind) | 2,700 | 1,990 |

---

### Tradeit

| Attribute | Detail |
|-----------|--------|
| Category | Skin trading platform |
| Contract year | Y2 — recently signed |
| KPIs | Account Linkage (via Steam) and trades |
| Geos | TBC — new geos included in Y2 |
| Funnel | Account Linkage → identification → trades |

**NSM Values (Tradeit)**

| Conversion Point | € Value |
|-----------------|---------|
| Account Linkage | €0.38 |
| Trade 1 | €0.04 |
| Trade 5 | €0.18 |
| Trade 250 | €8.75 |
| Trade 1,000 | €35.00 |

**CDP Snapshot — Tradeit** *(all-time)*

| Event | Distinct Users |
|-------|---------------|
| Account Linkage | 343,295 |
| Identification | 249,015 |
| Trade (any) | 103,311 |
| Trade ≥$5 | 38,633 |
| Trade ≥$250 | 12,229 |
| Trade ≥$1,000 | 1,443 |

---

### WhiteMarket

| Attribute | Detail |
|-----------|--------|
| Category | Skin marketplace |
| Contract year | Y3 — significantly reduced budget vs prior years |
| Funnel | Account Linkage → email confirm → deposit → trades |

**NSM Values (WhiteMarket)**

| Conversion Point | € Value |
|-----------------|---------|
| Account Linkage | €0.38 |
| Trade 1 | €0.05 |
| Trade 5 | €0.25 |
| Trade 250 | €12.50 |
| Trade 1,000 | €50.00 |

**CDP Snapshot — WhiteMarket** *(all-time)*

| Event | Distinct Users |
|-------|---------------|
| Account Linkage | 627,255 |
| Email confirmed | 494,554 |
| Deposit success | 38,433 |
| Deal buy | 31,084 |
| KYC passed | 25,708 |

---

### PaySafe

| Attribute | Detail |
|-----------|--------|
| Category | Financial services / digital wallet |
| Contract year | Being signed (March 2026) |
| KPI | Deposits onto the Paysafe wallet |
| Geos | Germany, Poland, France, Spain, Nordics (excl. Sweden) |
| Funnel | Account Linkage → KYC → Deposit *(provisional — awaiting partner validation)* |

**NSM Values (PaySafe)**

| Conversion Point | € Value |
|-----------------|---------|
| Account Linkage | €2.50 |
| KYC | €5.00 |
| First Time Deposit | €17.50 |

---

### WhiteBit *(past partner)*

- Crypto exchange. Y1 only — partnership ended.
- Budget declined over time as the FACEIT user base became saturated.
- Relevant as historical precedent for saturation risk in single-vertical performance campaigns.

---

> **CDP Data Caveats (all partners)**
> 1. CDP data reflects users who linked their account — it does NOT represent performance driven by FACEIT campaigns. Users may have been active customers before linking.
> 2. Data spans multiple years. Not all linked users are still active on FACEIT.
> 3. Attributed campaign performance (Y1–Y3 Missions data) to be added separately.

---

## Engagement Engine

The Engagement Engine (EE) sends AI-generated activity notifications to users stuck on a specific mission challenge, using psychological frameworks to prompt task completion.

### How It Works

1. Monitors user progress through mission tasks
2. Identifies users stuck on a specific challenge
3. Sends a personalised notification with AI-generated copy (unique per user to avoid repetition)

### Psychological Frameworks

| Framework | Hook |
|-----------|------|
| Progress Completion | "You're almost there" — near-miss framing |
| Live Reward Rush | Urgency — limited time, act now |
| Reward Motivation | Focus on what the user stands to gain |
| Competitive Pressure | Social comparison — others are completing this |

### Experiment Results (First Test — Winline BOFU)

| Finding | Detail |
|---------|--------|
| Overall uplift | ~+0.2 pp in task completions — modest but meaningful at scale |
| Best-performing framework | Progress Completion (10.6% CTR) |
| Second-best | Urgency / Live Reward Rush (9.4% CTR) |
| Weaker frameworks | Skill (7.8%), Competitive Pressure (7.4%) |
| Best use case | Medium-barrier BOFU actions (deposit 3k/5k RUB, bet 1k RUB) |
| Limitation | Not sufficient to move TOFU users — works for already-engaged users only |
| Declining reach over time | Driven by user attrition (inactivity), not completions |

### Strategic Position

The EE is a **BOFU retention tool**, not an acquisition tool. Its value scales with the size of the engaged user base. Winline is the primary use case; other partners need meaningful BOFU depth to benefit.

---

## Supporting Infrastructure

### Account Linkage

The foundational integration layer for all BI products.

- Creates a 1:1 relationship between a FACEIT user and the partner platform
- Enables auto-claim of prizes (no code handling required)
- Gates prize eligibility behind account creation on the partner side
- Feeds user data into the CDP post-linkage
- Eliminates code reselling — guarantees verified, fraud-proof leads for partners

**Entry points**: Mission page, Branded Event page, Drop page, Order page
**Integration time**: Up to 2 weeks including testing

---

### Customer Data Platform (CDP)

Post-linkage, user data flows into the CDP:

- Data stored per user, siloed per partner
- Partner CRM signals received (registration, KYC, deposit, bet events)
- Enables funnel-stage segmentation (TOFU / MOFU / BOFU)
- Powers **Custom Missions** — targeted missions for specific user segments

Data points received from each partner are agreed at partnership start. Privacy assessments may be required depending on country and data type.

---

## Prizes

Types of prizes used in BI products:

- Advertiser vouchers (free bets, raffle tickets, credits)
- Embedded codes in URL
- Material prizes (partner-fulfilled)
- FACEIT Points
- FACEIT Premium subscriptions
- FACEIT Skins

**Constraints**:
- FACEIT cannot run raffles (legal) — must be run on the partner side
- Prizes can be gated behind mandatory account linkage
- Configurable expiration times
- Distributed 24h after competition end (Branded Events)

---

## Loyalty / Tier Progression

Used in high-value partner campaigns to drive repeated engagement and long-term retention.

| Tier | Level |
|------|-------|
| Subscriber | Entry |
| Gold | |
| Platinum | |
| Diamond | |
| Elite | |
| Legend | Top |

Incentivises repeated deposits, weekly milestones, and long-term retention objectives.

---

## How Performance Is Measured (NSM)

Brand Integrations performance feeds into the **OVU/EBU component of TAVI**:

**OVU = 3·AL + 6·C1 + 9·C2 + 3·C3**

| Variable | Event | NSM Weight |
|----------|-------|------------|
| AL | Account Linkage | 3 |
| C1 | KYC completion | 6 |
| C2 | First deposit / purchase | 9 |
| C3 | Deeper milestones | 3 |

Full framework: `context/metrics.md`

---

## Legal & Privacy

- Missions with account linkage require a partner-specific privacy policy on the mission page
- Privacy risk assessments may be required depending on country and data points shared
- Privacy contacts: Fabia (acting lead), Akkeroos Kremers (account linkage / CDP), Gina (CLO)
