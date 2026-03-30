# Inventory Team Meeting — Prep Notes

> **Date**: Wed 26 March 2026
> **Duration**: 45 min (15 + 30)
> **Audience**: Isaure, Archil, Kilian, Joanna, Pol, Giang
> **Context**: Same team that received the Brand Product Lineup doc. They know the products — this meeting goes deeper.

---

## Part I: DP Inventory Evolution & 2027 Commercial Strategy (15 min)

### Objective
Update the team on what's changed, what's new, and what's coming — so they can match advertiser briefs to the right product.

### Talking Points

**1. What's refreshed since last session**

- **Play Interstitial** — One-Pager is current (Mar 2026). Key numbers to reference:
  - 37M ad pods/month (111M impressions), 185 countries
  - Inventory value ceiling: $8.1M/year at 100% fill
  - Year 1 conservative: $1.3M ad rev + $702K subs upside = ~$2.0M
  - Status: awaiting approval, design review with Flo on 28 March
  - ⚠️ **Not yet available for sale** — don't include in briefs until approved
  - Reference: `onePager_ Play Interstitial.md`

- **Rewarded Video** — Now in testing with Logitech (3rd Brand Takeover, March 2026). Natural add-on to BT — video on top of sponsorship at the drop claim moment
  - ⚠️ Limited availability — discuss with you (Moritz) before pitching

- **Peripheral Targeting** — Live in India (2,853 records), Turkey (80.5K DAU) releasing this week
  - 33.7% of records match gaming brands (Logitech 15.5%, Razer 12%)
  - Killer use case: "Reach users who DON'T own a Logitech mouse" — conquest targeting
  - Rollout: India → Turkey → Tier 2 EU → Tier 1 (gated on privacy review)
  - ⚠️ Not yet available for sale

- **Skin Vault** — Experiment live (top 300 profiles, 50/50 split). CPC to Tradeit
  - ⚠️ In experiment, not for general sale

**2. What advertisers are buying now (active partners)**

| Partner | Product | Deal Size | Status |
|---|---|---|---|
| Winline | Missions + AL + CDP | €2.4M (2025) | Year 3, ongoing |
| Tradeit | Missions + Skin Vault | €500K | Year 2, expanding geos |
| WhiteMarket | Missions + AL | €1M | Year 3, BOFU focus |
| PaySafe | Missions + AL | €300K | Signing |
| Logitech | Brand Takeover (×4) + Rewarded Video | — | Via Adam Goh, in 2026 planning |

**3. Quick reminder: product-to-brief matching**
- Reference the Quick Reference table in `brand-product-lineup-inventory-team.md` (they have this doc)
- Emphasise: Brand Takeover is **geo-exclusive**, Missions are **not**
- New capability coming: **Peripheral Targeting** opens endemic hardware brands as a new vertical

**4. 2027 strategic context (light touch)**
- BCG commercial strategy review underway — projecting €11.7-30.8M B2B revenue by 2030 (vs €3.4M today)
- Key growth levers: more brands on Missions (currently 4, capacity for 7 before cannibalization), new products (Play Interstitial, Peripheral Targeting), new verticals (PaySafe = first non-gaming/betting partner)
- Don't go deep here — just signal that the strategic direction is "more inventory types, more verticals, more geos"

---

## Part II: Unlocking Full Potential — Winline & Tradeit Case Studies (30 min)

### Objective
Show the team HOW FACEIT's technical infrastructure (Account Linkage + CDP) drives measurable conversions — using Winline and Tradeit as complementary proof points. Winline shows funnel depth (CDP-driven late-stage conversion). Tradeit shows scale breadth (geo expansion + reward experimentation).

### Case Study A: Winline — Deep-Funnel CDP Proof Point

#### Opening Frame

> "Every platform can sell impressions. What makes FACEIT's Brand Integrations unique is that we can prove conversions — not clicks, not views, but verified deposits, KYC completions, and bets. Let me show you how with Winline."

#### 1. The Winline Funnel (March 2026 data)

Walk through the conversion ladder using real numbers:

```
386K users joined (Play 1 Match)
  → 366K completed gaming mission (92.7%)
    → 4,741 connected Winline account (1.7% — THE BOTTLENECK)
      → 268 verified identity / KYC (1.1% of AL)
        → 207 deposited 500 RUB (77% of KYC)
          → 8,368 deposited 3000 RUB (from different tier — 11.4%)
            → 6,450 placed bet (78.1% of depositors)
```

**Key insight**: Once users pass account linkage, late-funnel completion is 67-78%. The product works — the gate is at the AL step.

#### 2. How Account Linkage Works (Technical Demo)

- **Problem it solves**: Before AL, users could resell prize codes. Advertisers paid for leads that never converted. Fraud.
- **How it works**: 1:1 verified relationship between FACEIT user and partner platform. User links once, auto-claims all future rewards. No codes visible.
- **Integration**: ~2 weeks including testing. OAuth-based. Works across all competition types (Missions, Brand Takeover, Drops).
- **Reference**: Technical docs at `docs.faceit.com/getting-started/authentication/account-linkage/`
- **Figma flows**: Available (linked in Account Linkage doc)

#### 3. How CDP Drives Targeting & Proves ROI

- **What it is**: Partners return enriched data points via the AL integration — registration, KYC status, deposits, bets
- **What it enables**:
  - **Segmentation**: TOFU (no AL), MOFU (AL but no conversion), BOFU (AL + purchase) — WhiteMarket already uses this
  - **Custom Missions**: "Deposit 3000 RUB" mission targeted only at users who've already linked + verified → 11.4% completion vs 1.1% for cold users
  - **ROI proof**: We can tell Winline exactly: "4,741 users linked accounts, 268 completed KYC, 8,368 deposited, 6,450 placed bets"
  - **Privacy note**: Depending on country + data points, privacy assessment may be required

#### 4. € Value Attribution — The NSM Framework

Show how we translate conversions into € value for each partner:

**Winline conversion values:**

| Stage | Action | € Value per conversion | March Volume | March € Value |
|---|---|---|---|---|
| AL | Account Linkage | €4.33 | 4,741 | €20,529 |
| C1 | KYC Verification | €8.66 | 268 | €2,321 |
| C2 | First Time Deposit | €121.10 | ~8,575 | ~€1,038,433 |
| C3 | Second Deposit | €4.33 | ~6,450 | ~€27,929 |

*C2 volume estimated from deposit missions (207 + 8,368). Exact attribution requires BQ.*

> **Key message**: We don't sell impressions — we sell verified outcomes with € values attached. The NSM dashboard tracks this on a 30-day rolling basis per partner, smoothing mission activation seasonality.

#### 5. What This Means for Briefs

Connect it back to what the inventory team does:

- **When an advertiser asks for "user acquisition"** → Missions + AL. Show them the Winline funnel: 386K reached, 4.7K verified accounts
- **When they ask "how do you prove ROI?"** → CDP integration. We track the full funnel on their side. We can tell them cost-per-KYC, cost-per-deposit
- **When they say "we want deposits, not just sign-ups"** → Custom CDP missions with tiered tasks. Winline's deposit missions convert at 11.4-67.6% among connected users
- **The pitch**: "We're not a media buy. We're a performance channel with verified, fraud-proof conversions and full-funnel visibility."

---

### Case Study B: Tradeit — Geo Expansion & the Mystery Box Experiment

#### Objective
Show a different growth lever: scaling through geo expansion and reward experiments. Where Winline proves depth (full-funnel CDP), Tradeit proves breadth — what happens when you take a proven mission format and roll it across 6 regions simultaneously.

#### Opening Frame

> "Tradeit is now a Year 3 partner — they signed their contract renewal and expanded geos in March. They went from 4 regions to 6 in one month, and we tested a Mystery Box reward format that drove a 50x spike in account linkages. Let me walk through what worked and what didn't."

#### 1. Partnership Evolution

| Year | Geos | Products | Scale (monthly gaming activations) |
|---|---|---|---|
| Y1 (2024) | CIS only | Missions + AL | ~150K/month |
| Y2 (2025) | CIS, NA, APAC, MENA | Missions + AL + Skin Vault | ~350K/month |
| Y3 (Mar 2026) | CIS, NA, APAC, MENA + **EU + LATAM** | Missions + AL + Skin Vault + Mystery Box | **1.2M+ in 2 weeks** |

The EU launch alone (531K gaming activations in March) exceeded the entire CIS base from January.

#### 2. March Geo Expansion — Activation Data

| Region | Status | Gaming Activations | Trade Completions | Trade $250+ |
|---|---|---|---|---|
| **EU** | 🆕 New in March | 531K | 11,475 | 890 |
| **CIS** (all campaigns) | Ongoing + expanded | 512K | 7,948 | 156 |
| **LATAM** | 🆕 New in March | 41K | 702 | 44 |
| **NA** | Ongoing + Mystery Box | 35K | 442 | 20 |
| **APAC** | Ongoing + Mystery Box | 29K | 336 | 41 |
| **MENA** | Ongoing + Mystery Box | 13K | 387 | 10 |
| **Total** | | **~1.16M** | **~21,290** | **~1,161** |

EU is doing the heavy lifting — nearly half of all activations in its first month. LATAM is small but promising (41K in week 1+2).

#### 3. The Mystery Box Experiment

**What changed**: General missions in March included a "Mystery Box" reward format (randomised skin drops instead of fixed prizes). Ran across CIS, NA, APAC, MENA.

**Impact on account linkages**:
- Jan–Feb baseline: **~2,500 ALs/week** (organic, fixed rewards)
- March Mystery Box: **~129,000 ALs/week** — a **50x spike**

**But downstream conversion diluted**:

| Metric | Jan–Feb (fixed rewards) | March (Mystery Box) |
|---|---|---|
| Gaming completion | 92–94% | 88–92% |
| Trade any item (conversion) | 1.5–2.0% | 2.0–2.4% |
| Trade $250+ (high-value) | ~0.3% | ~0.1% at volume |
| ALs per week | ~2,500 | ~129,000 |

**Interpretation**: Mystery Box is an acquisition rocket — it pulls massive top-of-funnel volume. But the users it attracts are less qualified downstream. The question is whether the absolute number of conversions justifies the diluted rate.

**Answer**: Yes, in absolute terms. March delivered ~21K trade completions in 2 weeks vs ~2K/month in Jan–Feb. Volume overwhelms rate compression.

#### 4. Reward Expiration — The Biggest Funnel Leak

> **294K users had rewards expire vs 41K who actually claimed — a 7:1 ratio.**

This is Tradeit's single biggest loss. Users completed the mission, earned the reward, and then never claimed it. At scale, this means:
- 294K potential trades lost
- At even the base Trade 1 value (€0.04), that's €11,760 in uncaptured NSM value
- At the Trade 250 conversion rate (6.1%), ~18K of those could have been $250+ trades = €157,500 in unrealised value

**Recommendation**: Reward expiration reminders (push notification 24h + 2h before expiry) are the single highest-ROI product improvement across all partners.

#### 5. € Value Attribution — Tradeit March

| Stage | Action | € Value per conversion | March Volume | March € Value |
|---|---|---|---|---|
| AL | Account Linkage | €0.38 | ~1,160,000 | ~€440,800 |
| C1 | Trade any item | €0.04 | 22,368 | €895 |
| C2 | Trade $250+ (EN) | €8.75 | 1,242 | €10,868 |
| C2 | Trade >20000 RUB | €8.75 | 389 | €3,404 |
| | | | **Total** | **~€456,000** |

*Note: AL volume is estimated from gaming mission joins (proxy for account linkages). Actual AL count may differ — BQ is source of truth.*

Compare to Winline's ~€1.1M in March — Tradeit generates less per-conversion value (€0.38 vs €4.33 per AL) but compensates with 250x the volume. Different partner economics, both valid.

#### 6. What This Means for Briefs

- **When a skin trading / marketplace brand asks for scale**: Tradeit's March is the proof point — 1.2M+ users activated across 6 geos in 2 weeks. No other gaming platform can deliver this.
- **Geo expansion is a proven playbook**: Take an existing mission format, localise reward copy, launch in new geos. EU went from 0 to 531K activations in week 1.
- **Mystery Box = TOFU weapon**: If an advertiser wants account linkages at volume, Mystery Box format delivers 50x baseline. Caution: downstream quality dilutes.
- **High-value tiers self-select**: The $250+ trade mission consistently converts at 2.5x the base rate. Always include a high-value tier — it identifies your best users.
- **The pitch**: "We can take your partnership from 4 geos to 6 in one campaign cycle, with a proven mission framework that's driven 1.2M activations for Tradeit in March alone."

### Cross-Partner Patterns (Bonus if time allows)

| Pattern | Evidence |
|---|---|
| Gaming missions = 90%+ completion | All 5 partners, all geos |
| Partner conversion bottleneck = 1-2% | Tradeit 2.4%, Winline 1.7%, WM 0.9%, WL_KZ 0.4% |
| Late-funnel completion is HIGH | Winline 67-78%, WL_KZ 99.7% |
| Tiered missions outperform flat | Winline deposit tiers, Tradeit $250+ at 6.1% vs 2.4% |
| BOFU re-engagement = highest ROI | WhiteMarket BOFU = 79% of total trade value |

---

## Reference Materials to Have Open

1. **NSM Dashboard** — `https://mnatalini-rgb.github.io/Personal-Space/nsm-dashboard.html` (live, shows all 5 partners)
2. **Brand Product Lineup** — `docs/brand-product-lineup-inventory-team.md` (team already has this)
3. **March Mission Review** — `docs/product_briefs/march-mission-review-2026.md` (your data source)
4. **Play Interstitial One-Pager** — `docs/product_documentation/onePager_ Play Interstitial.md`

## Open Questions / Things to Decide Before the Meeting

1. **Do you want to share the March Mission Review directly with the team?** It has all 5 partner funnel data — powerful but detailed. Could overwhelm.
2. **How much BCG context to share?** I kept it light (just "strategic review underway, directional numbers"). The full BCG feedback doc exists but is internal.
3. **Do you want to screenshare the NSM dashboard live?** It's the most compelling way to show partner performance tracking in real time.
4. **PaySafe status** — listed as "signing" in the lineup doc. Is it confirmed enough to mention as a live example, or keep it as "incoming"?
