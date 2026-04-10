# Q1 2026 Quarterly Review — Discussion Prep

**Session:** Thu 16 April, 45 min (in-person)
**Audience:** Product Leadership (William Seghers + peers)
**Format:** 2-pager already shared — this is your talk track

---

## Part 1: Talking Points & Narrative

### Opening (2 min) — Set the Frame

> "Q1 answered the question we set at the start of the year: *can we measure what a user is worth to a partner and use that to steer the business?* The answer is yes. €650K in partner value from 3 active partners, with a framework that tells us exactly where the money comes from and where it leaks."

**Key framing move:** Position this quarter as *foundational* — not a revenue number to be judged in isolation, but the first quarter where the measurement infrastructure exists to make every future quarter better.

---

### Section 1: The Model Works (5 min)

**Lead with the NSM story, not the number.**

Talk track:
- "For the first time, leadership can see per-partner ROI backed by Finance-confirmed costs. This isn't a PM dashboard — it's the operating model."
- €649,876 Total Partner Value on a 30-day rolling window. 3 active partners. 2.28M unique users exposed. 25% conversion rate.
- "The important thing isn't the €650K. It's that we know *why* it's €650K and what levers move it."

**Transition:** "The measurement is in place. Now let me show you what we learned by using it."

---

### Section 2: What We Learned — The Experiments (10 min)

**Mystery Box** — the headline:
- Strongest account linkage lever ever tested. CIS went from 2% to 13.6%. MENA hit 22.3%. Even NA (hardest market) moved from 5.4% to 7.7%.
- "But this isn't a pure win. The conversion quality question is real — 294K expired Tradeit rewards, 40× drop from mission completion to partner conversion. We drove volume, now we need to tighten the funnel."
- **Show you're ahead of the objection:** "This is exactly why we're *not* scaling Mystery Box to Winline yet — our highest-value partner at 85% of portfolio value. We need to prove C1/C2 quality first."

**Trust Modal** — the quick win:
- Among users who reach the AL step, keeping the modal doubles completion (5.34% vs 2.75%, p<0.001, +€416/cohort).
- "A UX decision, not an engineering effort. Zero code, measurable partner value."
- Net recommendation: keep the modal. The full-population trade-off (higher AL rate but 48% lower quality) supports targeted use.

**Mission Chain** — the behavioural design proof:
- +94.7% relative uplift in mission completion when missions unlock sequentially vs. allowing retroactive credit.
- "This validates that *how* we structure the conversion flow matters as much as *what* we offer."

**Prebid Migration** — the cost story:
- Moba outperforms Publift on RPV across all tiers (+11.5% T1, +12% T2, +27.5% T3 after commission).
- Discovered Publift was inflating fill rates via a GAM placeholder. "This is why we need to own our ad tech, not rent it."
- A/B extended to include Primis outstream — decision point in Q2.

**Peripheral Expansion** — the new data asset:
- 193K users across 152 countries sharing hardware telemetry weekly.
- "No competitor in esports collects this. It opens a brand advertising vertical — Logitech, Razer, Intel — based on what users *actually own*."
- Near-zero marginal cost. Already running Logitech G branded events as the first activation.

---

### Section 3: Where It's Fragile — Be Honest (5 min)

**This is where credibility is built. Don't hide these — lead with them.**

1. **Partner concentration: Winline = 85% of value.**
   - "This isn't a pipeline problem — it's a product archetype problem. We're optimised for CIS betting. Diversifying means adapting the conversion ladder for new verticals."
   - Mitigation: PaySafe onboarding (fintech), Tradeit growth (crypto/skins), Logitech G (hardware/brand).

2. **Tradeit negative ROI (−59%).**
   - "March was a breakout month (€68.7K, 5× prior months) driven by Mystery Box + new regions. But costs are high and the reward expiry issue is real."
   - Decision point: Monitor April/May. If the Mystery Box volume doesn't convert to C1/C2, we renegotiate.

3. **CS2 dependency: 100% of revenue from one title ecosystem.**
   - "Mobalytics proves the infrastructure works cross-title. But this is early. Real diversification comes with new EFG titles."

4. **No B2B product marketing.**
   - "We're building case studies and audience packages ourselves. This is a structural gap — I'm covering it tactically but it limits how fast we scale the partner portfolio."

---

### Section 4: Q2 — Close the Gaps, Then Scale (8 min)

**Frame Q2 as "fix before scale" — this shows discipline.**

Talk track:
- "Q1 proved the model works. Q2 is about closing the gaps we found *before* we commit to full rollout."

**Four Q2 decision points** (give them the structure):

| Decision | By When | Data Source |
|---|---|---|
| Mystery Box → Winline expansion | End of May | C1/C2 quality after funnel tightening |
| Prebid full migration (Publift → Moba) | End of June | CSStats RPV A/B (display + outstream) |
| Play Interstitial MVP scope | End of May | Phase 0 behavioural tolerance (house ads) |
| Peripheral ad targeting go/no-go | End of June | Legal sign-off (LEGD-8214) |

**Play Interstitial** — the new revenue story:
- ~37M annual free-user matchmaking sessions. Video pre-roll at 2.2% ad density (vs YouTube 3-7%, Twitch 5%+).
- Conservative Year 1: ~$1.3M paid ad revenue + $702K subscription uplift from house ads.
- "This recaptures the video budgets we lost when Watch was sunset."
- Phase 0 starts Q2: house ads to measure behavioural tolerance before any paid ads.

**PaySafe activation:**
- Fintech vertical — deposits, not bets. €2.50/AL, €5.00/KYC, €17.50/FTD.
- Germany, Poland, France, Spain, Nordics.
- "Directly addresses partner concentration risk and tests whether the playbook transfers to a non-betting archetype."

---

### Section 5: The 2026 Arc (3 min) — End with the Vision

> "Q1 proved the model works. Q2 closes the gaps and activates new inventory. H2 moves from tactics to product lines."

Three H2 themes in one sentence each:
1. **Play Interstitial** goes from experiment to commercial rollout — a new ad format category for FACEIT.
2. **Prebid ownership** means we control the auction, set floor prices, and integrate first-party data into the bid stream — revenue scales with data richness, not just traffic.
3. **Brand Integrations become a productised onboarding package** — new partners inherit validated mechanics from day one, reducing time-to-value from months to weeks.

Closing line:
> "The flywheel is: every new user generates impressions, hardware data, and conversion potential. Every new title adds inventory. Every new partner inherits proven playbooks. It compounds without proportional headcount."

---

### Timing Guide (45 min session)

| Block | Minutes | Purpose |
|---|---|---|
| Opening frame | 2 | Set the "model works" narrative |
| The model works (NSM + KPIs) | 5 | Credibility — the numbers |
| What we learned (experiments) | 10 | Depth — show rigour |
| Where it's fragile (challenges) | 5 | Honesty — build trust |
| Q2 plan (close gaps, then scale) | 8 | Forward-looking — structure |
| 2026 arc / vision | 3 | Aspiration — the payoff |
| **Q&A / Discussion** | **12** | **The real conversation** |

---

## Part 2: Anticipated Tough Questions

### Q1: "Winline is 85% of your value. What happens if they leave?"

**Why they'll ask:** Concentration risk is the most obvious vulnerability. William flagged it in the yearly review.

**Your answer:**
> "Today, Winline leaving would eliminate ~€550K of our €650K portfolio value. That's the honest answer. Here's what we're doing about it:"
>
> 1. **PaySafe onboarding in Q2** — fintech vertical, different archetype. Tests whether the playbook transfers.
> 2. **Tradeit March breakout (€68.7K)** — 5× prior months. If Mystery Box quality improves, this partner scales.
> 3. **Peripheral data vertical** — opens hardware brands (Logitech, Razer, Intel) as a new category. Zero partner overlap with betting.
> 4. **Play Interstitial** — advertising revenue that's partner-independent. Diversifies revenue stream, not just partner portfolio.
>
> "The real mitigation isn't finding another Winline — it's making the business multi-vertical so no single partner can be existential."

**If pushed:** "We can absorb a Winline exit if Play Interstitial and Prebid migration land on plan. The ad revenue offsets partner concentration. But short-term, yes — we'd feel it."

---

### Q2: "Mystery Box numbers are impressive, but is the quality there?"

**Why they'll ask:** The AL numbers are so high they'll suspect vanity metrics. The prep doc flags this.

**Your answer:**
> "Not yet — and that's by design. We're not scaling Mystery Box to Winline until we prove C1/C2 quality."
>
> - 294K expired Tradeit rewards signals the funnel leaks between linkage and first transaction.
> - 40× drop from gaming mission completion (~90%) to partner conversion (~1-2%).
> - Q2 priority: reward expiry reminders, shorter time-to-reward, intermediate funnel steps.
>
> "The volume lever works. Q2 is about making the quality match before we deploy it where the stakes are highest."

**If pushed on timeline:** "If C1/C2 quality doesn't improve by end of May, we don't expand Mystery Box to Winline in Q2. We won't burn our highest-value partner relationship on unproven conversion quality."

---

### Q3: "Play Interstitial — $2M sounds optimistic. What's the downside?"

**Why they'll ask:** Any new revenue projection gets scrutiny. The format is untested on FACEIT.

**Your answer:**
> "The $2M is the mid scenario. Conservative case is $1.3M paid ad revenue + $702K in subscription uplift from house ads as a 'push to subscribe' lever. The model is built country-by-country (185 markets × tier × CPM × fill rate)."
>
> "Downside risks:"
> 1. **User tolerance** — if free users bounce during matchmaking, we kill it. Phase 0 with house ads measures this before any paid ads.
> 2. **Fill rate** — programmatic video demand for esports audiences is thin in Tier 2/3. We may need PMP deals to hit fill.
> 3. **Ad density perception** — 2.2% is low vs YouTube/Twitch, but it's new for FACEIT. The format needs to feel native.
>
> "Phase 0 is the de-risk. If behavioural metrics don't hold, we don't proceed to paid. The design is explicitly a kill-gate, not a ramp."

---

### Q4: "You said 'no B2B product marketing' — why haven't you solved that?"

**Why they'll ask:** If it's been flagged as a gap, they want to know why it persists.

**Your answer:**
> "It's a structural gap, not a task gap. We need someone who speaks both product and sales — building audience packages, case studies, pitch decks — with commercial context. I'm covering it tactically:"
>
> - Built 1 case study (Winline, in progress)
> - Building 2 audience packages for Q2
> - Sharing experiment results proactively with Commercial within 48 hours
>
> "But this is PM time that should go to product work. My Q2 action plan includes building these materials ourselves, but I want to flag it: this limits how fast the partner portfolio grows."

**What you want from them:** "If there's appetite to discuss a shared resource between Product and Commercial for B2B materials, I'd welcome that conversation."

---

### Q5: "Tradeit is -59% ROI. Why keep them?"

**Why they'll ask:** Negative ROI on a partner looks bad on paper.

**Your answer:**
> "Because March changed the trajectory. €68.7K in March vs. €12-13K in Jan/Feb — that's 5× growth from Mystery Box + new regions. The question isn't 'should we keep Tradeit' — it's 'does the March trajectory hold?'"
>
> - Activation costs are front-loaded (Mystery Box rewards).
> - If users convert to C1 (first trade), the unit economics flip.
> - 294K expired rewards are a funnel leak, not a product failure — we know exactly where to fix.
>
> "Decision framework: if April/May don't show C1/C2 improvement, we renegotiate terms. If they do, Tradeit becomes the proof that our playbook works beyond betting."

---

### Q6: "Why are you building all of this infrastructure (NSM, CDP, Prebid) instead of just growing revenue?"

**Why they'll ask:** Infrastructure vs. revenue tension is classic. Especially if peers are showing bigger top-line numbers.

**Your answer:**
> "Because infrastructure *is* how we grow revenue at scale. Every partner that joins inherits the conversion ladder, the CDP signals, the measurement framework. Time-to-value goes from months to weeks."
>
> "Concrete example: Mystery Box took 2 weeks to deploy across 4 regions because the mission infrastructure already existed. Without it, that's 4 separate builds."
>
> "The Prebid migration saves ~20% commission on every ad dollar — that's immediate, recurring margin improvement with zero incremental inventory."
>
> "The alternative — growing revenue partner-by-partner with bespoke campaigns — is linear. What we're building compounds."

---

### Q7: "What's the biggest risk to your Q2 plan?"

**Why they'll ask:** Tests your self-awareness and planning rigour.

**Your answer:**
> "Play Interstitial getting stuck in design. It's our highest-impact new initiative, and it needs design + engineering alignment to move from business case to Phase 0. If it's delayed past April, I'll descope to an MVP."
>
> Second risk: "Legal review on peripheral ad targeting (LEGD-8214). Internal storage and audience sizing can proceed, but the ad-system integration gates the revenue opportunity. I've escalated the legal ticket but don't control the timeline."

---

### Q8: "How does this scale if FACEIT grows to 10M users?"

**Why they'll ask:** They want to know if you're building for scale or just for today.

**Your answer:**
> "Every layer we've built is user-count agnostic:"
>
> - **CDP** — more users = richer data, better targeting, higher partner confidence
> - **Conversion ladder** — mechanics (Mystery Box, Mission Chain, Trust Modal) work at any scale
> - **Prebid** — own the auction, more impressions = more revenue, no commission ceiling
> - **Peripheral data** — passive collection, scales linearly with Client installs
> - **NSM** — automated 30-day rolling calculation, handles any partner count
>
> "At 10M users, the incremental cost of a new partner approaches zero — they plug into existing infrastructure and get measured on the same framework from day one."

---

### Q9: "Your Q2 action plan has 5 themes from the yearly review. Are you actually doing all of them?"

**Why they'll ask:** William gave the feedback. He wants to know it landed.

**Your answer:**
> "Yes, and I'm tracking monthly checkpoints for each. Let me give you the April status:"
>
> 1. **Radical Focus** — NSM tracking is live (30-day rolling). Using TAVI to assess every new initiative before committing resources.
> 2. **Communicate & Evangelise** — Posting to #bet-ads-partnerships weekly. Filling slide 19 every week. Shared Prebid results with Commercial.
> 3. **Managing Tension** — Data-first approach. Preparing briefs before contentious meetings.
> 4. **Executive Influence** — This quarterly review itself uses the "So What → Recommendation" format throughout. Scheduling Director+ 1:1s.
> 5. **Vertical Expansion** — Logitech G branded events as first hardware activation. Building audience packages.
>
> "Target is 3.5+ average across themes by end of June. Happy to share the tracker."

---

## Quick-Reference Card (Print This)

### Three Numbers to Anchor Everything
| Number | What It Means |
|---|---|
| **€649,876** | Total Partner Value — 30-day rolling, 3 active partners |
| **25%** | Conversion rate across portfolio (AL → deposit/trade/purchase) |
| **193K** | Users sharing hardware data (152 countries) — net new data asset |

### Three Soundbites
1. "We don't report impressions anymore. We report € value generated on the partner's side."
2. "Q1 proved the model. Q2 closes the gaps. H2 scales it."
3. "Every new user compounds: impressions + hardware data + conversion potential."

### If You Only Have 30 Seconds
> "Ads & Partnerships generated €650K in measurable partner value from 3 partners in Q1. The NSM framework is now operational — for the first time, leadership can see which partners make money and which don't. We found the strongest engagement lever ever (Mystery Box), discovered we need to fix funnel quality before scaling it, and laid groundwork for two new revenue verticals (Play Interstitial, Peripheral advertising). Q2 is about closing those gaps before committing to scale."
