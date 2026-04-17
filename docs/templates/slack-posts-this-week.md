# This Week's Slack Posts — #bet-ads-partnerships

> **Week of 16 March 2026**
> Copy-paste ready. Adjust numbers if you have updated data.

---

## Post 1: Prebid Experiment Results (post after Wed presentation)

```
:chart_with_upwards_trend: Prebid experiment: in-house setup outperforms managed partner across all geo tiers

We ran a 3-week head-to-head comparison (25 Feb – 16 Mar) between our in-house Prebid stack (via Moba) and our current managed partner (Publift) for display and outstream video ads.

The results — Revenue per Page View after Publift's 20% commission:
• Tier 1 (US, UK, DE, FR, etc.): Moba +11.5%
• Tier 2 (BR, PL, TR, SE, etc.): Moba +12.0%
• Tier 3 (rest of world): Moba +27.5%

What this means:
We can run our own programmatic stack at equal or better revenue efficiency while removing the managed partner margin. This gives us full control over ad quality, header bidding config, and partner selection.

Next steps:
Recommending a phased migration — Tier 3 first (lowest risk, highest upside), then Tier 2, then Tier 1. Full rollout target: end of Q2.

Full analysis deck available — reach out if you want a walkthrough.
```

---

## Post 2: Skin Vault Launch (post now or tomorrow)

```
:rocket: Skin Vault is live on FACEIT CS2 profiles

What's new?
• Top 300 CS2 profiles now display the user's Steam inventory directly on their FACEIT profile page
• Running as a 50/50 A/B test — 150 profiles with Skin Vault visible, 150 control
• Clicking an item takes users to Tradeit's marketplace — our monetisation partner for this feature

Why are we doing this?
We're testing a new revenue channel: can surfacing skin data on high-traffic profiles drive meaningful referral traffic to a trading partner? If it works, this opens a monetisation path that doesn't consume ad inventory.

What's next?
• Monitoring: CTR from profile → Tradeit, Steam API reliability, user engagement with the inventory widget
• First results expected by end of this week
• If positive, expanding to all users with inventory data in April

Questions or feedback → #bet-ads-partnerships
```

---

## Post 3: Peripherals Initiative (post when Turkey release is confirmed)

```
:rocket: Peripherals data collection: India validated, expanding to Turkey

What happened?
India (Phase 1) has been live for 2 weeks. First data analysis on 2,853 records:
• Top brands detected: Logitech (15.5%), Razer (12.0%), Microsoft (4.9%)
• 33.7% of records match recognized gaming brands (Logitech, Razer, SteelSeries, Corsair, etc.)
• Device split: Keyboard 55.7%, Mouse 44.2%
• CPU: AMD 53.3%, Intel 46.7%
• Data quality: 95.2% non-generic manufacturer data — clean enough for production

Why Turkey next?
• 80.5K DAU — 24x India's volume, big enough to validate at scale
• Low advertiser risk — no active peripheral campaigns in TR
• No GDPR/LGPD — simpler regulatory posture
• Commercially relevant for endemic brands (Logitech, Razer targeting)

What's next?
• Turkey release deploying today/tomorrow
• First Turkey data analysis as soon as records flow
• Comparing brand distribution: India vs Turkey
• If stable, next stop is a Tier 2 EU market (Poland — 163K DAU)
```

---

## Post 4: Friday Weekly Wrap (post Friday)

```
:bulb: Ads & Partnerships — Week of 16 March

This week in one line: Prebid experiment confirms we should bring programmatic in-house. Two new features live and collecting data.

Highlights:
• :chart_with_upwards_trend: Prebid results presented — Moba beats Publift on RPV across all geo tiers (+11-27%). Recommending phased migration.
• :rocket: Skin Vault live on 300 profiles — first CTR data coming in, monitoring Tradeit referral traffic
• :rocket: Peripherals data collection live in India — validating hardware data quality before Tier 2 expansion
• :warning: Play Interstitial at risk — design review with Flo on 28 March. Timeline depends on design feedback turnaround.
• :white_check_mark: Mystery Box + Logitech Branded Event experiments fully analyzed and documented

Next week:
• Prebid: align on migration timeline with eng
• Skin Vault: first week of CTR data analysis
• Peripherals: share hardware distribution data if schema validated
• Play Interstitial: prep one-pager for Flo meeting
```

---

## Post 5: Skippable Video Interstitial Results (DRAFT — post after Mandar's CPM calculation)

> **Blocked on:** Mandar's CPM/revenue uplift forecast. Once available, add a "Revenue projection" line to the Results block before posting.

```
:microscope: Skippable Video Interstitial — Results

**Setup:** A/B test on our existing overlay interstitial — replacing static display with a skippable video (3s unskippable, then skip). 31 days, 6.47M impressions, 184 countries. House ad (Premium subscription CTA) — no paid cannibalisation.
**Hypothesis:** Video format increases CPM potential without negatively impacting user retention.

Results:
• Retention guardrail: +0.3% (variant vs control) — not significant. PASSED.
• Video completion rate: 70.4% (GAM weighted) / 83.3% full-15s (FE)
• CTR: 0.37% — 23,698 clicks to Premium purchase page
• Premium subs attributed: 320 (46 direct, 274 view-through)
• Regional: Tier 1 / APAC 75–81% completion. Central Asia / Balkans 50–65% (device quality).
• Revenue uplift forecast: [TBD — pending Mandar's CPM calculation]

:white_check_mark: **Verdict:** Confirmed. No retention risk. Format is safe to ship — video completion and CTR both clear green thresholds.

What we learned:
• Users tolerate skippable video interstitials well — 83% watch the full 15s when they interact
• The "only fire when display doesn't fill" logic means every video impression is incremental, not cannibalising existing paid inventory
• Low-completion geos correlate with device quality, not content — geo-targeting adjustments may be worth it for paid campaigns

Next steps:
• GTM ownership transferred to Mandar's commercial team (agreed Apr 15)
• Open questions sent to commercial: ad serving setup (VAST vs GAM), sales packaging, pricing model, trafficking ops
• Mandar sharing full Salesforce pipeline overview

Full report → skippable-video-experiment-report.html
Interactive dashboard → skippable-video-dashboard.html
```

---

## Posting Schedule This Week

| Day | Post | Status |
|---|---|---|
| Tue/Wed | Skin Vault launch | Ready to post |
| Wed/Thu | Prebid results (after presentation) | Ready — adjust if presentation feedback changes the narrative |
| Thu/Fri | Peripherals update | Post once data is validated with Egor |
| Friday | Weekly wrap | Ready to post |
