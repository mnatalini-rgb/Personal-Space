# Information Architecture Proposal — Ads & Partnerships Hub

**Author**: Moritz Natalini · Dir. PM  
**Date**: 3 April 2026  
**Status**: Draft — ready for review  

---

## Problem

Today there are **13 HTML pages** and **58+ markdown documents** across `analysis/`, `docs/`, `context/`, `Experiments/`, and root. They have almost no cross-navigation. The current `index.html` links to only 5 of 13 dashboards and hasn't been updated since 19 March. The Productivity Dashboard already links to 7 dashboards via project cards, but it's not the entry point. Users (i.e. you) have to remember URLs or dig through file trees.

### What exists today

| # | Source File | Category | Has nav back? |
|---|---|---|---|
| 1 | `docs/decisions/productivity-dashboard.html` | Project Tracking / Todo | No |
| 2 | `docs/decisions/roadmap-dashboard.html` | Roadmap (Internal + Stakeholder) | → NSM, → Productivity |
| 3 | `analysis/nsm-dashboard.html` | NSM Metrics | → Roadmap |
| 4 | `analysis/tradeit-nsm-dashboard.html` | Partner Metrics | No |
| 5 | `analysis/skin-vault-dashboard.html` | Experiment | No |
| 6 | `analysis/prebid-experiment-results.html` | Experiment | No |
| 7 | `analysis/prebid-slides.html` | Experiment (slides) | No |
| 8 | `analysis/prebid-slides-print.html` | Experiment (print) | No |
| 9 | `analysis/peripheral-data-dashboard.html` | UX Research Brief | No |
| 10 | `weekly-plan.html` | Weekly Updates | No |
| 11 | `weekly-plan-16-21-mar-2026.html` | Weekly Updates (archived) | No |
| 12 | `weekly-plan-23-28-mar-2026.html` | Weekly Updates (archived) | No |
| 13 | `index.html` | Hub (outdated) | N/A |

### Markdown docs (key groups)

| Directory | Count | Contains |
|---|---|---|
| `docs/product_briefs/` | 9 | PRDs, experiment conclusions, scoping docs |
| `docs/product_documentation/` | 7 | Product specs (Missions, Brand Takeover, CDP, Drops, etc.) |
| `docs/stakeholder_updates/` | 12 | Quarterly reviews, weekly updates, meeting preps, BCG |
| `docs/templates/` | 6 | Slide templates, Slack templates, PRD template |
| `context/` | 12 | Business context, metrics, team, experiments, yearly review |
| `reference/` | 1 | NSM framework |
| `Experiments/` | 6 | Monthly experiment reports (PDF + MD) |
| `SQL/` | 3 dirs | Queries, results, schemas (8 schema docs) |

---

## Moritz's 6 Categories (from user request)

1. **Weekly Updates** — Slack updates with releases
2. **Roadmap** — Stakeholder view + Internal sprint view
3. **NSM & Partner Metrics** — NSM framework, partner performance, competitions (Missions, Brand Takeovers)
4. **Experiments** — A/B tests, Prebid evaluation, Skin Vault, monthly experiment reports
5. **Project Tracking & Todo** — Productivity Dashboard (16 projects, tasks, goals)
6. **Quarterly Business Reviews** — Q1/Q2 reviews, leadership decks

---

## Proposed Architecture: Hub-and-Spoke

### Design decision: Rebuild `index.html` as the hub

**Why not enhance the Productivity Dashboard?**  
The Productivity Dashboard is itself a spoke — it's the Project Tracking tool. Making it the hub would overload it with navigation concerns that don't belong in a task manager. Instead, `index.html` becomes the **entry point** that links to all spokes including the Productivity Dashboard.

**Why `index.html`?**  
- It's what GitHub Pages serves at `/` — natural entry point
- Already exists (just outdated)
- Every spoke can link back to `/` or `/index.html` — simple, universal

### Hub design

```
┌─────────────────────────────────────────────────┐
│                  STICKY HEADER                   │
│  Ads & Partnerships Hub        [Quick Nav Links] │
├─────────────────────────────────────────────────┤
│                                                   │
│  ┌─ SECTION 1: Core Workflows ─────────────────┐ │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐      │ │
│  │ │ Projects │ │ Roadmap  │ │ Weekly   │      │ │
│  │ │ & Todo   │ │          │ │ Updates  │      │ │
│  │ └──────────┘ └──────────┘ └──────────┘      │ │
│  └──────────────────────────────────────────────┘ │
│                                                   │
│  ┌─ SECTION 2: Analytics & Metrics ─────────────┐ │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐      │ │
│  │ │ NSM      │ │ Tradeit  │ │ Quarterly│      │ │
│  │ │Dashboard │ │ Partner  │ │ Review   │      │ │
│  │ └──────────┘ └──────────┘ └──────────┘      │ │
│  └──────────────────────────────────────────────┘ │
│                                                   │
│  ┌─ SECTION 3: Experiments ─────────────────────┐ │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐      │ │
│  │ │ Prebid   │ │ Skin     │ │Peripheral│      │ │
│  │ │ Results  │ │ Vault    │ │ Data     │      │ │
│  │ └──────────┘ └──────────┘ └──────────┘      │ │
│  └──────────────────────────────────────────────┘ │
│                                                   │
│  ┌─ SECTION 4: Reference ──────────────────────┐  │
│  │  Product Docs  ·  Templates  ·  SQL Schemas  │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Card-to-page mapping

| Section | Card | Links to | Status indicator |
|---|---|---|---|
| **Core Workflows** | Projects & Todo | `productivity-dashboard.html` | Active projects count |
| | Roadmap | `roadmap-dashboard.html` | Current sprint label |
| | Weekly Updates | `weekly-plan.html` | Current week date |
| **Analytics & Metrics** | NSM Dashboard | `nsm-dashboard.html` | "Live" badge |
| | Tradeit Performance | `tradeit-nsm-dashboard.html` | — |
| | Quarterly Review | Google Doc link | Due date |
| **Experiments** | Prebid Evaluation | `prebid-experiment-results.html` | — |
| | Prebid Slides | `prebid-slides.html` | — |
| | Skin Vault | `skin-vault-dashboard.html` | "Live" badge |
| | Peripheral Data | `peripheral-data-dashboard.html` | — |
| **Reference** | Product Documentation | File list or sub-hub | — |
| | Templates | File list | — |
| | SQL Schemas | File list | — |

### Navigation pattern for spoke pages

Every spoke page gets a **back-to-hub bar** at the top:

```html
<nav style="...">
  <a href="/index.html">← Hub</a>
  <span> · </span>
  <span>NSM Dashboard</span>
</nav>
```

Lightweight, non-intrusive, consistent across all pages.

---

## Design System Alignment

The hub will use the **Soft UI / Clean Tech** system from the Roadmap Dashboard:

- **Font**: Inter (600 titles, 500 section headers, 400 body)
- **Background**: `#EEF2F3` (mint)
- **Surface**: `#ffffff`
- **Border radius**: `20px` containers, `12px` cards
- **Shadows**: soft (`0 2px 12px rgba(0,0,0,0.06)`)
- **Accent**: `#1A1A2E` (dark navy)

This matches the Roadmap Dashboard. The Productivity Dashboard uses a different system (`#f9fafb` bg, `8px` radius, blue accent) — that's fine, each spoke owns its own styling. The hub sets the tone.

---

## What this eliminates

| Today | After |
|---|---|
| `index.html` links to 5/13 pages | Hub links to all pages |
| No way back from spoke pages | Every spoke has back-to-hub nav |
| Must remember URLs | Single entry point at `/` |
| Productivity Dashboard tries to be hub AND task manager | Clean separation: hub = navigation, productivity = projects |
| Weekly plans are orphaned | Weekly Updates section on hub |
| QBR docs are buried in file tree | Quarterly Review card with direct link |
| Experiment dashboards are isolated | Experiments section groups them |

---

## Implementation plan

### Phase 1: Build the hub (`index.html`)
1. Rebuild `index.html` with Soft UI design system
2. 4 sections: Core Workflows, Analytics & Metrics, Experiments, Reference
3. Card grid layout (responsive, `auto-fit minmax(280px, 1fr)`)
4. Status badges where applicable (Live, current sprint, due date)
5. Sticky header with quick-nav anchor links

### Phase 2: Add back-to-hub navigation to all spokes
6. Add consistent nav bar to all 12 spoke pages
7. Format: `← Hub · [Page Name]`
8. Non-intrusive: thin bar, same font, no design system conflict

### Phase 3: Cross-linking between related spokes
9. NSM Dashboard → Tradeit Dashboard (partner tab)
10. Roadmap → Productivity Dashboard (project details)
11. Experiment pages → related project cards

### Phase 4: Weekly plan archive
12. Hub card for "Weekly Updates" shows current week, links to archive
13. Archive page lists all weekly plans chronologically

---

## Open questions

1. **Should the Reference section link directly to markdown files?** GitHub Pages can serve them, but they'd render as raw text. Alternative: render them in a simple HTML wrapper.
2. **Should archived weekly plans get their own index page?** Or just list them directly on the hub?
3. **Do you want the hub to show any live data** (e.g. "4 active P0 projects") or keep it purely navigational?
4. **QBR links**: Google Docs or local HTML? The Q1 review is a Google Doc — should the hub link externally?

---

## Next steps

Ready to implement Phase 1 (rebuild `index.html`) immediately upon your approval.
