# Slack Channel Templates — #bet-ads-partnerships

> **Channel**: `#bet-ads-partnerships`
> **Goal**: Evangelise wins, share learnings, build cross-functional visibility
> **Cadence**: Post when something ships, when results land, or when a notable metric moves. Aim for 1-2 posts per week minimum.

---

## Template 1: Metric Win

Use when a KPI hits a milestone, breaks a record, or shows meaningful movement.

**When to use:** Weekly revenue hits, eCPM improvements, viewability gains, partner conversion milestones, experiment lifts.

**Tone:** Confident, data-led, forward-looking. Like Derek's DAP posts.

```
:chart_with_upwards_trend: [HEADLINE — what happened, one line]

[1-2 sentences of context — why this matters, what drove it]

The numbers:
• [Metric 1]: [value] ([delta vs. previous period or benchmark])
• [Metric 2]: [value] ([delta])
• [Metric 3]: [value] ([delta])

[Optional: what this means for partners / the business]

[Forward-looking close — what's next or what we expect]
```

**Example:**
```
:chart_with_upwards_trend: Prebid experiment: Moba outperforms Publift across all tiers

After a 3-week head-to-head (25 Feb – 16 Mar), our in-house Prebid setup via Moba delivers higher Revenue per Page View than Publift across every geo tier — even before accounting for Publift's 20% commission.

The numbers (RPV advantage after commission):
• Tier 1 (US/UK/DE/FR): +11.5%
• Tier 2 (BR/PL/TR/SE): +12.0%
• Tier 3 (rest of world): +27.5%

This means we can reduce our dependency on a managed partner while keeping (or improving) revenue per impression. Presenting full analysis to stakeholders Wed — recommending a phased migration starting with Tier 3.
```

---

## Template 2: Feature/Product Ship

Use when something goes live — an experiment launches, a new feature deploys, or a partner integration activates.

**When to use:** Experiment launches, new ad formats, partner features going live, tool deployments.

**Tone:** Clear, structured, operational. Like Liza's Shop Orders post.

```
:rocket: [WHAT SHIPPED — short description]

What's new?
• [Bullet 1 — what changed for users/partners]
• [Bullet 2 — key technical detail if relevant]
• [Bullet 3 — scope/targeting]

Why?
[1-2 sentences — the business reason, tied to a metric or partner goal]

What's next?
[What we're monitoring, what comes after this, timeline]

Questions or feedback → [channel or person]
```

**Example:**
```
:rocket: Skin Vault is live on FACEIT profiles

What's new?
• Top 300 CS2 profiles now display users' Steam inventory items on their FACEIT profile
• 50/50 A/B split — 150 profiles with Skin Vault, 150 control
• Items link to Tradeit marketplace (our monetisation partner)

Why?
Testing whether surfacing skin inventory on profiles drives meaningful traffic to Tradeit — a new revenue stream that doesn't require ad inventory or impressions.

What's next?
Monitoring CTR to Tradeit and Steam API error rates this week. If results are positive, we expand to all profiles with inventory data in April.

Questions → #bet-ads-partnerships
```

---

## Template 3: Experiment Results / Analysis

Use when you have results from a completed experiment — positive or negative. Sharing negative results builds trust and shows rigour.

**When to use:** A/B test results, campaign post-mortems, partner performance analysis, experiment conclusions.

**Tone:** Analytical, honest, actionable. Show what you learned and what you're doing about it.

```
:microscope: [EXPERIMENT NAME] — Results

**Setup:** [1 sentence — what we tested, duration, sample]
**Hypothesis:** [What we expected to happen]

Results:
• [Primary metric]: [result] ([vs. control or target])
• [Secondary metric]: [result]
• [Tertiary metric]: [result]

:white_check_mark: / :x: **Verdict:** [Confirmed / Not confirmed — 1 sentence]

What we learned:
• [Insight 1]
• [Insight 2]

Next steps:
• [What we're doing with these results]

[Link to full analysis if available]
```

**Example:**
```
:microscope: Mystery Box Experiment — Results

**Setup:** Tested whether framing mission rewards as "mystery boxes" (unknown reward) vs. standard display (known reward) affects completion rates. 4-week experiment across all active missions.
**Hypothesis:** Mystery box framing increases mission activation by 15%+ due to curiosity/gamification effect.

Results:
• Activation rate: +8.3% (mystery box vs. control) — below 15% target
• Completion rate: -2.1% (mystery box vs. control) — slight negative
• Net OVU impact: +4.7% (marginal, driven by higher activation offsetting lower completion)

:x: **Verdict:** Not confirmed. Lift exists but below threshold to justify added complexity.

What we learned:
• Curiosity framing works for activation but may hurt completion — users who don't know the reward are less motivated to finish
• The effect was strongest in Tier 3 geos where baseline engagement is lower

Next steps:
• Not rolling out globally. Will test a hybrid approach (partial reveal) in Q2 if capacity allows.
• Sharing findings with Shop & Rewards team — relevant for their lootbox planning.

Full analysis → [link]
```

---

## Posting Rhythm

| Day | What to post | Template |
|---|---|---|
| Monday | React to weekend metrics if notable (ad revenue, partner conversions) | Metric Win |
| Wednesday | Mid-week ship or experiment update if something launched | Feature Ship |
| Friday | Weekly wrap — biggest win or learning of the week | Any (pick what fits) |

**Minimum viable rhythm:** 1 post per week (Friday). Ideal: 2-3 per week.

**Rules:**
1. Every post must have at least one number
2. Never post "working on X" — only post outcomes, ships, or results
3. Tag relevant people when it involves cross-team impact (Commercial, Platform, etc.)
4. Link to docs/dashboards when available — make it easy for others to dig in
5. If something is off track or failed, share that too — builds credibility

---

## Quick Reference: Emoji Convention

| Emoji | Use for |
|---|---|
| :chart_with_upwards_trend: | Metric win, KPI milestone |
| :rocket: | Feature/product ship |
| :microscope: | Experiment results |
| :rotating_light: | Incident or urgent issue |
| :bulb: | Insight or learning |
| :handshake: | Partner-related update |
| :warning: | Risk flagged |
