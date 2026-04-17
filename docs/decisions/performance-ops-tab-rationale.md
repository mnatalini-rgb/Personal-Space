# Performance & Ops Tab — Rationale & Weekly Review Guide

**Author**: Moritz Natalini · Dir. PM  
**Date**: 15 April 2026  
**Status**: Active  
**Dashboard**: NSM Dashboard → Winline → Performance & Ops tab

---

## 1. Why This Tab Exists

The NSM dashboard previously served two audiences well: Sales (via CDP Insights) and Leadership (via NSM + Missions). However, it lacked an operational view for the team running the partnership day-to-day. 

The existing tabs (Funnel, CDP, Missions, Rewards) each show a piece of the picture, but none synthesize what happened during the week and what actions to take next. The Performance & Ops tab provides a single surface for Monday morning reviews that connects funnel performance, cohort quality, and reward effectiveness to concrete decisions.

---

## 2. Three Audiences Model

| Audience | What they need | Dashboard Tab |
|---|---|---|
| **Sales** (pitch deals) | "We drove 112K new Winline users via FACEIT" | CDP Insights |
| **Leadership** (we're doing great) | Total value, efficiency, month-over-month growth | NSM + Missions |
| **Moritz + Team** (what to do next) | Funnel gaps → cohort quality → reward effectiveness → action items | **Performance & Ops** |

---

## 3. Tab Structure — 5 Zones

The tab is organized into five zones that guide the team from high-level signals to specific actions.

### ① Signal — WoW Scorecard (5 min)
Seven KPI cards with week-over-week deltas.
- **Cards**: AL count, KYC count, FTD count, € Value total, €/1K EBU efficiency, Total FP Cost, FACEIT-Driven Rate.
- **Format**: Each card shows This Week | Last Week | WoW% with color-coded borders (green for up, red for down).
- **Purpose**: "What changed since last Monday?" Scan for anomalies in 30 seconds.

### ② Diagnosis — Funnel · Cohort Quality · Reward Effectiveness (10 min)
Two-column breakdown of operational health.
- **Left Column**: Compact conversion funnel (EBU→AL→KYC→FTD) and a reward effectiveness summary (cost/user £0.10, redemption rate 5.2%, budget burn 6.0%, subs entries).
- **Right Column**: FACEIT-Driven acquisition rate trend line (12-month Chart.js line chart showing % of ALs where user registered Winline ≤7 days before linking), latest month / 3-month average cards, and a CDP funnel summary for the latest month.
- **Purpose**: "Where is the bottleneck and is our user quality improving?"

### ③ Weekly Trend — Last 8 Weeks (5 min)
Stacked bar chart and data table.
- **Visualization**: Stacked bar chart (AL € / KYC € / FTD €).
- **Data Table**: Columns for Week, AL, KYC, FTD, Total €, and WoW%.
- **Purpose**: "Are we trending up or down? Any week-on-week anomalies?"

### ④ Opportunities (10 min)
Four static insight cards derived from current data patterns:
1. **KYC Conversion is the Bottleneck**: Only 6.7% AL→KYC. FACEIT-driven users show 60.9% KYC vs 85.2% for pre-existing users.
2. **Same-Day Registrations = Strongest Signal**: 84.5% of FACEIT-driven users register the same day as linking.
3. **Week 1 Spike Then Decay**: Missions activate on the 1st of the month. Week 1 typically captures 40-60% of total conversions.
4. **Reward Cost is Low — Room to Experiment**: £0.10/user cost and 6% budget burn. Each FTD is worth €121.10.
- **Purpose**: "What should we be thinking about?" These serve as discussion starters rather than prescriptions.

### ⑤ Decision Log (5 min)
A localStorage-backed editable table for accountability.
- **Columns**: Date | Signal | Decision | Owner | Due | Outcome.
- **Interactivity**: Buttons to add decisions and export to CSV.
- **Purpose**: Accountability trail. Fill this during the Monday meeting and review outcomes at the start of the next session.

---

## 4. Weekly Meeting Structure

- **When**: Monday morning, ~30 minutes.
- **Who**: Moritz + direct team (partnerships ops, data analyst).
- **Cadence**: Every Monday, reviewing the prior week's data.
- **Flow**: Use the Performance & Ops tab as the agenda.
  - Scan scorecard (① 5 min)
  - Dig into diagnosis (② 10 min)
  - Check weekly trend (③ 5 min)
  - Discuss opportunities (④ 10 min)
  - Log decisions (⑤ 5 min)

---

## 5. Monthly Activation Cadence & Week Context

Missions are contractually activated on the 1st of each month and last the entire month. This creates a natural 4-week cycle reflected in the "Week Context Indicator" at the top of the tab:

- **Week 1 — "Early Read"** (blue): Missions just activated. Initial signals only. Too early for major decisions.
- **Week 2 — "Monitoring"** (amber): Patterns are emerging. Watch for anomalies compared to last month.
- **Week 3 — "Monitoring"** (amber): Solid data. Identify trends for next-month planning.
- **Week 4 — "Decision Week"** (green): Last chance to decide experiments before the next activation.

If experimentation requires development, the decision likely needs to wait until the month after next, as we need at least one week before activation for configuration changes and longer for development work. The indicator auto-computes based on the current date.

---

## 6. Data Sources

- **Missions CSV data (2026)**: Weekly conversion counts and values.
- **CDP user_events (BigQuery → CSV)**: Attribution cohort analysis (375K users, gap_days model).
- **Reward/FP data**: Cost, redemption rates, and budget allocation sourced from mission CSVs.
- **EBU**: Platform analytics.

---

## 7. Future Iterations

- **Automated Insights**: Opportunity cards will transition from static curated content to auto-computed alerts.
- **Reward Catalog Integration**: The reward section will link to a full catalog for easier decision-making.
- **Scaling**: The pattern will be replicated for Tradeit and WhiteMarket partners.
- **Shared Backend**: Migration of the decision log from localStorage to a shared database for cross-browser persistence.

---

## 8. Design Principles Applied

The tab follows eight core design principles used across the dashboard system:

1. **Audience**: Specifically built for the ops team, avoiding the generic data needs of sales or leadership.
2. **Decision**: Each zone ends with an actionable question to drive outcomes.
3. **Key Takeaway**: The scorecard surfaces WoW deltas instantly for F-pattern scanning.
4. **Reduce Clutter**: Focuses on summary metrics rather than raw data dumps.
5. **Design with Intention**: Color conveys meaning (green/red for performance, blue/amber/green for week phase).
6. **Add Context**: Data sources are cited, time periods are explicit, and the week context is auto-computed.
7. **Narrative Arc**: Follows a logical flow from Signal → Diagnosis → Trend → Opportunities → Decision.
8. **Interactivity Last**: Uses a static-first design. The decision log is the only interactive element and appears last.
