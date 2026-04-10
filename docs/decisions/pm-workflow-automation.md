# PM Workflow Automation — Pipeline Design

**Author**: Moritz Natalini · Dir. PM  
**Date**: 3 April 2026  
**Status**: Proposal — ready for review  

---

## Problem

Today, every initiative goes through ~10 stages from idea to release note. Each stage requires manual data entry across disconnected tools: Productivity Dashboard, Roadmap Dashboard, Jira, experiment tracking, monthly releases page, weekly slide, QBR document, and Slack. A single initiative means updating 5-7 tools manually. This creates:

- **Double-entry**: Same information typed into multiple places
- **Drift**: Tools get out of sync (e.g. Jira ticket "Done" but Roadmap still shows "In Progress")
- **Friction**: Steps get skipped because they're tedious (Slack release notes, QBR references)
- **Fragility**: The process lives in Moritz's head, not in a system

## Goal

Reduce the 11-step workflow to **1 trigger + AI-assisted cascading + continuous sync**, where creating a project in the Productivity Dashboard kicks off everything downstream automatically or semi-automatically.

---

## The 11-Step Pipeline

### Overview

```
Step 1:  Create Project (Productivity Dashboard)
  ↓ auto
Step 2:  Generate Tasks (Productivity Dashboard todo)
  ↓ auto
Step 3:  Add Stakeholder Card (Roadmap → Stakeholder tab)
  ↓ auto
Step 4:  Add Sprint Chips (Roadmap → Internal Sprint tab)
  ↓ auto
Step 5:  Create Jira Ticket (for Scrum Master)
  ↓ auto
Step 5.5: Sync on Update (bi-directional doc ↔ card sync)
  ↓ on Jira "Done"
Step 6:  Move to Experiment Phase (track results)
  ↓ manual review
Step 7:  Generate Weekly Update (Friday slide)
  ↓ on ship/completion
Step 8:  Publish to Monthly Releases Page (interactive reference)
  ↓ auto
Step 9:  Generate QBR Reference (quarterly review)
  ↓ auto
Step 10: Post Release Note (Slack #bet-ads-partnerships)
```

### Visual Flow Diagram

→ See **`docs/decisions/workflow-pipeline-diagram.html`** for the interactive version (hosted on GitHub Pages).

### Automation Classification

| Step | Trigger | Executor | Automation Level |
|---|---|---|---|
| 1. Create Project | Manual (Moritz) | Productivity Dashboard UI | **Manual** — the entry point |
| 2. Generate Tasks | On project creation | AI assistant | **Automated** — AI generates default tasks from project type |
| 3. Stakeholder Card | On project creation | AI assistant + Dashboard JS | **Automated** — cascade from project data |
| 4. Sprint Chips | On project creation | AI assistant + Dashboard JS | **Semi-auto** — AI suggests, Moritz confirms sprint/assignee |
| 5. Jira Ticket | On project creation | `jira-cli` via shell | **Automated** — AI creates ticket from project brief |
| 5.5 Sync on Update | Doc/card/meeting-note change detected | AI assistant | **Automated** — AI detects changes, propagates to all linked surfaces |
| 6. Experiment Phase | Jira ticket → "Done" | Manual check / `refresh-roadmap.sh` | **Semi-auto** — Jira refresh detects "Done", AI prompts for experiment setup |
| 7. Weekly Update | Every Friday | AI assistant | **Semi-auto** — AI drafts from project state, Moritz reviews |
| 8. Monthly Releases Page | On project ship/experiment complete | AI assistant + Dashboard JS | **Semi-auto** — AI adds release/experiment entry, Moritz reviews |
| 9. QBR Reference | On project completion | AI assistant | **Semi-auto** — AI drafts QBR entry from results, Moritz reviews |
| 10. Slack Release Note | On project ship/completion | AI assistant + webhook | **Semi-auto** — AI drafts Block Kit JSON, posts via webhook after approval |

---

## Implementation Design — Per Step

### Step 1: Create Project (MANUAL — entry point)

**Current state**: No `addProject()` UI. Projects added via `SEED_PROJECTS` or JSON import.

**Required change**: Add a "New Project" button to the Productivity Dashboard that opens a modal form.

**Form fields**:
| Field | Type | Maps to |
|---|---|---|
| Name | text | `project.name` |
| Description | textarea | `project.description` |
| Priority | select (P0-P3) | `project.priority` |
| Target Date | date | `project.targetDate` |
| Area | select (advertising / brand_integrations / infrastructure) | `project.area` (new field) |
| Team Members | multi-select | `project.assignees` (new field) |
| Initiative Color | color picker | `project.color` (from INITIATIVE_COLORS) |

**On submit**: 
1. Creates project in localStorage (`productivity_projects`)
2. Fires `CustomEvent('project-created', { detail: projectData })` 
3. AI assistant picks up the event context to cascade steps 2-5

**Who builds this**: Delegated task (visual-engineering category) — single-file HTML edit to `productivity-dashboard.html`.

---

### Step 2: Generate Tasks (AUTOMATED)

**How it works**: When Moritz creates a project and asks the AI to "cascade" it (or we trigger automatically), the AI generates a default task set based on the project's area and priority.

**Task templates by area**:

**Brand Integrations**:
```
- [ ] Write product brief / one-pager
- [ ] Define success metrics (NSM targets)
- [ ] Design review with Anouk
- [ ] Backend scoping with Isabel/Egor
- [ ] Frontend scoping with Teodor/Omar
- [ ] Jira epic creation
- [ ] Partner alignment (if applicable)
- [ ] Launch → experiment setup
- [ ] Experiment analysis
- [ ] Results → stakeholder comms
```

**Advertising**:
```
- [ ] Write product brief / one-pager
- [ ] Define success metrics (RPV, fill rate, eCPM)
- [ ] Technical scoping (ad integration)
- [ ] A/B experiment design
- [ ] Jira epic creation
- [ ] Deploy experiment
- [ ] Analyse results (minimum 2 weeks data)
- [ ] Go/no-go decision
- [ ] Rollout plan
- [ ] Results → stakeholder comms
```

**Infrastructure**:
```
- [ ] Write technical spec
- [ ] Define acceptance criteria
- [ ] Backend implementation plan
- [ ] Frontend implementation plan
- [ ] Jira ticket(s) creation
- [ ] Code review + QA
- [ ] Deploy
- [ ] Verify in production
```

**Implementation**: AI command — Moritz says "cascade [project name]" or "set up [project name]". The AI:
1. Reads the project data from the dashboard
2. Generates tasks using the template for that area
3. Adds them to `productivity_tasks` in localStorage via the dashboard's `handleAddTask()` pattern
4. Marks each task with the project's keywords for auto-linking

**Practical approach**: Since the dashboards are localStorage-based HTML files, the AI assistant can't directly write to localStorage in the browser. Instead:

**Option A — AI generates, Moritz pastes**: AI outputs tasks as a JSON snippet. Moritz copies into the dashboard's Import function. *Simple but manual.*

**Option B — AI edits SEED_TASKS directly**: AI adds tasks to the `SEED_TASKS` array in the HTML file, bumps `SEED_VERSION`, and Moritz refreshes the page. *Automated but destructive on version bump — resets localStorage.*

**Option C (Recommended) — AI edits HTML + smart merge**: AI adds tasks to a new `PENDING_TASKS` array in the HTML. On page load, the dashboard checks for pending tasks, merges them into localStorage without resetting existing data, and clears the pending array. *Automated and non-destructive.*

---

### Step 3: Add Stakeholder Card (AUTOMATED)

**How it works**: From the project data, the AI creates a stakeholder roadmap item.

**Mapping**:
| Project Field | Stakeholder Field |
|---|---|
| `name` | `initiative` |
| `area` | `area` |
| `priority` | `priority` |
| `targetDate` | `eta` (formatted as "Mon YYYY") |
| `description` | `notes` |
| — | `status` = "not_started" |
| — | `jiraKey` = null (populated in Step 5) |
| — | `id` = auto-generated "sh-N" |

**Implementation**: Same approach as Step 2 — use a `PENDING_STAKEHOLDER_ITEMS` array in the roadmap HTML that merges on page load.

---

### Step 4: Add Sprint Chips (SEMI-AUTOMATED)

**How it works**: AI suggests sprint placement based on:
- Project priority (P0 = current or next sprint)
- Target date (work backwards from deadline)
- Team member availability (from roadmap's existing assignments)
- Omar availability (not before Sprint 2.2 / Apr 20)

**Output**: AI proposes a sprint plan:
```
Suggested sprint assignments for [Project Name]:
- Sprint 2.2 (Apr 13-24): Anouk (design), Isabel (backend scoping)
- Sprint 2.3 (Apr 27 - May 8): Teodor (frontend), Isabel (backend)
- Sprint 2.4 (May 11-22): Teodor (frontend polish), Egor (backend review)

Accept? [Y/modify]
```

**On confirmation**: AI writes chips to `PENDING_SPRINT_ASSIGNMENTS` in the roadmap HTML.

**Why semi-auto**: Sprint assignment involves judgment calls about team bandwidth, competing priorities, and dependencies that the AI shouldn't make unilaterally.

---

### Step 5: Create Jira Ticket (AUTOMATED)

**How it works**: AI constructs a `jira issue create` command from the project data.

**Command template**:
```bash
jira issue create \
  --project AD \
  --type Story \
  --summary "[Project Name]" \
  --priority [P0→Highest, P1→High, P2→Medium, P3→Low] \
  --assignee "[Scrum Master or Lead Engineer]" \
  --label "ads-partnerships" \
  --body "## Context
[Project description]

## Acceptance Criteria
[From generated tasks in Step 2]

## Links
- Product Brief: [link if exists]
- Dashboard: [link if exists]

## Priority: [P-level] | Target: [date]"
```

**Post-creation**: 
1. Capture the Jira key from command output (e.g. `AD-XXX`)
2. Update the stakeholder card's `jiraKey` field (Step 3)
3. Update the project's metadata with the Jira key

**Implementation**: Direct `jira-cli` execution via the AI assistant's bash tool. No webhook or GitHub Action needed — runs locally.

---

### Step 5.5: Sync on Update (AUTOMATED) — NEW

**Purpose**: Ensure all project surfaces stay in sync throughout a project's lifecycle. When a PRD, one-pager, meeting note, or dashboard card is updated, the AI propagates changes to all linked surfaces automatically.

**The problem this solves**: Today, updating a PRD after a meeting (e.g. adding confirmed flow, MVP spec, Figma links) requires manually updating:
- The productivity dashboard project brief (`proj-N`)
- The roadmap stakeholder card (`sh-N`)  
- Any linked documents (one-pager, PRD, meeting notes)

This is exactly the "double-entry" and "drift" problem described in the Problem section — but it happens *during* a project, not just at creation time.

**Classification**: Automated — runs continuously throughout the project lifecycle (not a one-time cascade like Steps 1-5).

**Triggers**:
| Trigger | Detection Method | Example |
|---|---|---|
| PRD or one-pager edited | AI detects file changes when user says "update my projects" or references a doc edit | Moritz updates `docs/product_briefs/PRD — Video Interstitials.md` after a meeting |
| Meeting notes shared | User shares meeting notes with AI | "Here are the notes from my meeting with Anouk, please update my projects" |
| Dashboard project card edited | AI edits `SEED_PROJECT_BRIEFS` or `SEED_PROJECTS` | Moritz asks to update proj-2 description |
| Stakeholder card edited | AI edits `SEED_STAKEHOLDER_DATA` | Moritz asks to change sh-1 status or notes |

**Sync Map — What Maps Where**:

| Source Field | → Target Field(s) |
|---|---|
| PRD/one-pager `Status` line | → `SEED_PROJECTS[proj-N].status`, `SEED_STAKEHOLDER_DATA[sh-N].status` |
| PRD/one-pager description/summary | → `SEED_PROJECT_BRIEFS['proj-N']` content section, `SEED_STAKEHOLDER_DATA[sh-N].notes` |
| PRD/one-pager success metrics | → `SEED_PROJECT_BRIEFS['proj-N']` metrics section |
| PRD/one-pager next steps | → `SEED_PROJECT_BRIEFS['proj-N']` next steps section |
| PRD/one-pager Figma/design links | → `SEED_PROJECT_BRIEFS['proj-N']` reference docs section, `SEED_PROJECTS[proj-N].links[]`, `SEED_STAKEHOLDER_DATA[sh-N].links[]` |
| Meeting notes (key decisions, updates) | → `SEED_PROJECT_BRIEFS['proj-N']` Updates log section |
| `SEED_PROJECTS[proj-N].status` | → PRD/one-pager status line, `SEED_STAKEHOLDER_DATA[sh-N].status` |
| `SEED_PROJECTS[proj-N].links[]` | → `SEED_STAKEHOLDER_DATA[sh-N].links[]` (mirror doc/Figma/dashboard links to team-facing view) |
| `SEED_STAKEHOLDER_DATA[sh-N].links[]` | → `SEED_PROJECTS[proj-N].links[]` (bi-directional — team-added links propagate back to PM view) |
| `SEED_STAKEHOLDER_DATA[sh-N].prdLink` (legacy) | → `SEED_PROJECT_BRIEFS['proj-N']` reference docs (fallback if `links[]` empty) |

**Hub Index (`index.html`) — Sync Surface**:

The hub homepage is the front door to the Product Hub. Cards on the index represent dashboards, experiments, releases, and reference docs. These drift when project state changes but the index isn't updated.

| Trigger | → index.html Update |
|---|---|
| New dashboard or experiment page created | → Add card to correct section (Live Experiments / Concluded / Releases), or update existing `href="#"` placeholder with real link |
| Experiment status changes (Live → Concluded → Shipped) | → Move card between subsections, update badge (`badge-live` → `badge-concluded` → `badge-shipped`) |
| Due date or milestone date changes | → Update badge text (e.g., "Due Apr 9" → "Discussion Apr 16") |
| New experiment or release added to portfolio | → Add new card to correct section + update section item count (`· N`) |
| Card removed or deprecated | → Remove card or move to a "Past" section + update section item count |
| Any sync action on index.html | → Update footer "Last updated" date |

**Hub Sync Checklist** (run mentally after any project surface change):

```
□ Does a card exist on index.html for this project/experiment/dashboard?
  → If not, should one be added?
□ Does the card href point to the correct file?
  → Watch for href="#" placeholders that never got updated
□ Is the badge status correct? (Live / Concluded / Shipped / Due date)
□ Is the card in the correct section? (Core Workflows / Analytics / Live Experiments / Concluded / Releases)
□ Are section item counts (· N) still accurate?
□ Is the footer "Last updated" date current?
```

**Project ↔ Document Registry**:

The AI resolves which documents belong to which project using:
1. **`docFile` field** on `SEED_PROJECTS` — points to the primary project doc
2. **`links[]` array** on both `SEED_PROJECTS` and `SEED_STAKEHOLDER_DATA` — contains all reference links (PRDs, one-pagers, Figma boards, dashboards). This is the primary link source for both PM and team views.
3. **`prdLink` field** on `SEED_STAKEHOLDER_DATA` (legacy) — points to the PRD or one-pager. Kept for backward compatibility; `links[]` takes precedence when populated.
4. **Project name matching** — fuzzy match between project name and doc title (e.g. "Play Interstitial" matches both `PRD — Video Interstitials.md` and `onePager_ Play Interstitial.md`)
5. **Explicit mapping** maintained by the AI in session context (e.g. `proj-2` → `sh-1` + `sh-7`)

**Example — the exact workflow that triggered this step**:

1. Moritz has a meeting with Anouk about Play Interstitial
2. Moritz shares meeting notes with AI: "update my projects and todo"
3. AI reads meeting notes, identifies project = Play Interstitial
4. AI updates:
   - `docs/product_briefs/PRD — Video Interstitials.md` (confirmed flow, MVP spec, A/B→A/B/C, Figma link)
   - `docs/product_documentation/onePager_ Play Interstitial.md` (status, Phase 0 rewrite, contributors, FigJam link)
   - `productivity-dashboard.html` → `SEED_PROJECT_BRIEFS['proj-2']` (full brief rewrite with flow, spec, links, update log)
   - `productivity-dashboard.html` → `SEED_PROJECTS['proj-2'].links[]` (PRD, One-Pager, Figma Board pills on card)
   - `roadmap-dashboard.html` → `SEED_STAKEHOLDER_DATA` → `sh-1.links[]`, `sh-7.links[]` (team-visible doc/Figma pills on stakeholder cards)
   - `roadmap-dashboard.html` → `SEED_STAKEHOLDER_DATA` → `sh-1.prdLink`, `sh-7.prdLink` (legacy fields, kept for backward compat)
5. All surfaces now reflect the same information — zero drift. The team sees the same links on stakeholder cards that Moritz sees on his project cards.

**Bi-directional sync rules**:
- **Doc → Cards**: When a PRD or one-pager is updated, propagate status, description, metrics, links, and next steps to all linked project cards and stakeholder items.
- **Cards → Docs**: When a project card status or description changes in a dashboard, update the corresponding doc's status line and summary.
- **Meeting Notes → All**: Meeting notes are "write-only" sources — they feed into docs and cards but are never modified by the sync process.
- **Conflict resolution**: If a field differs between doc and card, the most recently edited surface wins. The AI notes the sync in both places (e.g. "Updated from PRD edit on Apr 9").

**Implementation**: This step is **not** a PENDING array pattern like Steps 2-5. It's an AI behavioral protocol:
1. AI maintains a mental registry of project ↔ doc ↔ card mappings per session
2. When any project surface is edited, AI checks for linked surfaces
3. AI propagates changes using the Edit tool — direct file modifications
4. AI logs each sync action (what changed, where, when) in the project brief's Updates section

**Why automated (not semi-auto)**: Unlike Steps 7-10 which require narrative judgment, sync is mechanical — field A changed, update field B. No editorial decision needed. The AI should do this without asking "should I also update the roadmap card?" — the answer is always yes.

---

### Step 6: Experiment Phase (SEMI-AUTOMATED)

**How it works**: When Moritz runs `./scripts/refresh-roadmap.sh`, the output JSON shows tickets that moved to "Done". The AI:

1. Identifies newly completed tickets by comparing current vs. previous refresh
2. Prompts Moritz: "Jira AD-XXX ([Project Name]) is now Done. Ready to set up the experiment?"
3. If yes:
   - Updates stakeholder card status → "experiment"
   - Updates project status → "experiment"
   - Generates experiment tracking tasks (setup, duration, analysis)
   - Creates an experiment brief stub in `Experiments/`

**Trigger**: Moritz runs `refresh-roadmap.sh` or says "check Jira status". Not fully automated — requires a manual trigger to check.

**Future enhancement**: GitHub Action on a schedule (daily) that runs the refresh and posts a Slack notification if any tickets moved to "Done". But this requires moving the refresh script to GitHub Actions (separate effort).

---

### Step 7: Generate Weekly Update (SEMI-AUTOMATED)

**How it works**: Every Friday, Moritz says "prep my Friday slide" (existing workflow). The AI:

1. Reads all active projects from Productivity Dashboard
2. Reads recent task completions (completed this week)
3. Reads stakeholder roadmap items with status changes
4. Reads latest Jira refresh data
5. Drafts the weekly slide content using the `weekly-slide-prep.md` template

**Output**: Pre-filled weekly slide with:
- Headline KPI (AI selects most relevant based on this week's activity)
- 3-5 highlight bullets in `[WHAT] — [NUMBER] — [SO WHAT]` format
- Initiative table updates (Stage, Status, Update)

**What changes**: Nothing architectural. This is the existing "prep my Friday slide" workflow, but now it pulls from richer structured data (projects, tasks, stakeholder items) instead of Moritz verbally briefing the AI.

---

### Step 8: Monthly Releases & Experiments Page (SEMI-AUTOMATED) — NEW

**Purpose**: Replace the static monthly slide deck (currently attached to Slack messages) with an **interactive HTML page** that serves as:
- A **monthly stakeholder reference** — "here's what we shipped and learned this month"
- A **running experiment archive** — click to expand results, link to full dashboards
- A **QBR prep tool** — all shipped items are pre-formatted for quarterly review
- A **Slack attachment URL** — shareable link instead of a PDF/PPTX file

**Page**: `analysis/monthly-releases.html` (+ root copy for GitHub Pages)

**Design pattern**: Timeline + expandable cards (inspired by Linear's changelog). Monthly sections, each containing release cards and experiment result cards. Sticky sidebar for month navigation.

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  ← Hub · Monthly Releases & Experiments                  │
├──────────┬──────────────────────────────────────────────┤
│ SIDEBAR  │  MAIN CONTENT                                │
│ (sticky) │                                              │
│          │  ┌─ April 2026 ──────────────────────────┐   │
│ Apr 2026 │  │                                        │   │
│ Mar 2026 │  │  🚀 RELEASES (3)                      │   │
│ Feb 2026 │  │  ┌─────────────────────────────────┐   │   │
│ Jan 2026 │  │  │ ▸ Play Interstitial MVP          │   │   │
│          │  │  │   P0 · Advertising · Apr 18      │   │   │
│ ──────── │  │  │   Team: Teodor, Isabel, Anouk    │   │   │
│ Export   │  │  └─────────────────────────────────┘   │   │
│ [PDF]    │  │  ┌─────────────────────────────────┐   │   │
│ [JSON]   │  │  │ ▸ Skin Vault Expansion           │   │   │
│          │  │  │   P1 · Brand Integrations · Apr 9│   │   │
│ Stats    │  │  └─────────────────────────────────┘   │   │
│ 5 shipped│  │                                        │   │
│ 3 expts  │  │  🔬 EXPERIMENTS (2)                   │   │
│          │  │  ┌─────────────────────────────────┐   │   │
│          │  │  │ ▸ Mystery Box v2 — ✅ Confirmed   │   │   │
│          │  │  │   +18% AL rate · 95% confidence  │   │   │
│          │  │  │   ▾ (click to expand results)    │   │   │
│          │  │  │   ┌──────────────────────────┐   │   │   │
│          │  │  │   │ Primary: AL rate +18%     │   │   │   │
│          │  │  │   │ Secondary: C1 rate +4.2%  │   │   │   │
│          │  │  │   │ Duration: Mar 1 – Mar 28  │   │   │   │
│          │  │  │   │ Sample: 24K users          │   │   │   │
│          │  │  │   │ → Full dashboard           │   │   │   │
│          │  │  │   └──────────────────────────┘   │   │   │
│          │  │  └─────────────────────────────────┘   │   │
│          │  └────────────────────────────────────────┘   │
├──────────┴──────────────────────────────────────────────┤
│  Export: [Copy Slack Summary] [Download PDF] [JSON]      │
└─────────────────────────────────────────────────────────┘
```

**Data model** (stored in localStorage key `monthly_releases_data`):

```javascript
// Release entry — maps to existing project/stakeholder fields
{
  id: 'rel-1',
  month: '2026-04',                    // ISO month for grouping
  type: 'release',                     // 'release' | 'experiment'
  name: 'Play Interstitial MVP',       // from project.name
  projectId: 'proj-2',                 // links to productivity project
  stakeholderId: 'sh-1',              // links to roadmap stakeholder item
  area: 'advertising',                 // from project.area / stakeholder.area
  priority: 'P0',                      // from project.priority
  releaseDate: '2026-04-18',          // ISO date
  sprintId: 's2.2',                    // which sprint it shipped in
  team: ['teodor', 'isabel', 'anouk'], // team member IDs
  status: 'shipped',                   // 'planned' | 'rolling' | 'shipped'
  rolloutPct: 100,                     // 0-100, supports phased rollouts
  summary: 'Premium video ad format...', // 1-2 sentence description
  impact: '$1.3M est. Year 1 revenue', // key impact statement
  links: {
    jira: 'AD-XXX',                    // Jira key
    dashboard: 'analysis/...',         // link to detailed dashboard
    prd: 'docs/product_briefs/...',    // link to PRD
    slides: null                       // link to presentation if exists
  },
  notes: ''                            // free-text
}

// Experiment entry — extends release with experiment-specific fields
{
  id: 'exp-1',
  month: '2026-03',
  type: 'experiment',
  name: 'Mystery Box v2',
  projectId: 'proj-3',
  stakeholderId: 'sh-10',
  area: 'brand_integrations',
  priority: 'P1',
  // Experiment-specific fields
  hypothesis: 'Gamified reward framing increases AL by 15%+',
  startDate: '2026-03-01',
  endDate: '2026-03-28',
  primaryMetric: { name: 'AL rate', result: '+18%', target: '+15%' },
  secondaryMetrics: [
    { name: 'C1 conversion', result: '+4.2%', target: null },
    { name: 'Reward redemption', result: '62%', target: '50%' }
  ],
  sampleSize: '24,000 users',
  confidence: '95%',
  verdict: 'confirmed',               // 'confirmed' | 'not_confirmed' | 'inconclusive'
  verdictSummary: 'Lift exceeds target. Rolling out globally in April.',
  team: ['moritz', 'isabel'],
  links: {
    jira: 'AD-YYY',
    dashboard: 'analysis/...',
    report: 'Experiments/March Experiment (Ads).pdf'
  },
  notes: ''
}
```

**Key features**:
- **Month navigation**: Sticky sidebar with month list, click to scroll
- **Expandable cards**: Click release/experiment to show full details inline
- **Color-coded verdicts**: ✅ confirmed (green), ❌ not confirmed (red), ⚠️ inconclusive (amber)
- **Area pills**: "Advertising" / "Brand Integrations" with project colors
- **Priority badges**: P0/P1/P2 pills matching existing dashboard styling
- **Team avatars**: First-name chips showing who worked on it
- **Deep links**: Every card links to its full dashboard, PRD, Jira ticket
- **Export**: Copy as Slack-formatted summary (for posting), Download as PDF (for attaching), JSON export
- **Stats sidebar**: Monthly summary — "5 shipped, 3 experiments, 2 confirmed"
- **Auto-population**: AI adds entries when projects ship or experiments conclude (via PENDING_RELEASES array pattern)

**Integration with existing tools**:
- Reads from `productivity_projects` (project metadata, status)
- Reads from `roadmap_stakeholder_data` (stakeholder items, status)
- Links to existing dashboards (`analysis/*.html`)
- Feeds into QBR generation (Step 9 pulls from this page's data)
- Replaces PDF attachment on Slack — just share the GitHub Pages URL

**Implementation**: Same PENDING array pattern as Steps 2-4. AI writes `PENDING_RELEASES` to the HTML file; on page load, merge into localStorage `monthly_releases_data`.

---

### Step 9: Generate QBR Reference (SEMI-AUTOMATED)

**How it works**: When a project reaches "completed" or "shipped" status, the AI:

1. Pulls the release/experiment entry from the Monthly Releases page (Step 8) — metrics, team, timeline are already captured
2. Generates a QBR-ready entry using the `quarterly-review-q1-2026.md` format:
   - **What We Shipped**: 1-2 paragraph narrative (strategic level, not tactical)
   - **KPIs**: Relevant metrics from the project's experiment results
   - **Challenges/Decisions**: Any blockers encountered and how they were resolved
2. Appends to a running `docs/stakeholder_updates/qbr-q2-2026-entries.md` file
3. At quarter end, Moritz reviews and assembles into the final QBR

**Template per entry**:
```markdown
### [Project Name]

**Shipped**: [date] | **Duration**: [sprints] | **Team**: [members involved]

[1-2 paragraph narrative — why this matters to FACEIT's business, what it proves, what it enables]

| Metric | Result | Context |
|---|---|---|
| [Primary] | [value] | [vs. target or benchmark] |
| [Secondary] | [value] | [context] |

**Decision**: [what we decided based on results]
```

---

### Step 10: Post Release Note to Slack (SEMI-AUTOMATED)

**How it works**: When a project ships, the AI:

1. Selects the appropriate Slack template (Feature Ship, Experiment Results, or Metric Win)
2. Fills it with project data and results
3. Formats as a ready-to-post Slack message
4. Two delivery options:

**Option A — Copy-paste (current)**: AI outputs the formatted message, Moritz copies to Slack. *No setup required.*

**Option B — Webhook (recommended for future)**: 
1. Set up a Slack Incoming Webhook for `#bet-ads-partnerships`
2. AI constructs Block Kit JSON payload
3. Posts via `curl` to the webhook URL after Moritz confirms

**Webhook setup** (one-time):
1. Go to `https://api.slack.com/apps` → Create New App → From Scratch
2. Name: "Ads & Partnerships Bot" → Workspace: ESL FACEIT Group
3. Incoming Webhooks → Activate → Add to `#bet-ads-partnerships`
4. Copy webhook URL → save to `~/.config/slack-webhook-url` (gitignored)

**Post command**:
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"...", "blocks":[...]}' \
  "$(cat ~/.config/slack-webhook-url)"
```

---

## Implementation Phases

### Phase 0: "Add Project" UI (prerequisite)
- Add New Project modal to Productivity Dashboard
- Fields: name, description, priority, target date, area, team members, color
- Creates project in localStorage
- **Effort**: ~2 hours (visual-engineering delegation)
- **Deliverable**: Working "New Project" button

### Phase 1: The Cascade Command (Steps 1-5)
- AI command: `cascade [project]` or triggered on project creation
- Generates tasks, stakeholder card, sprint suggestions, Jira ticket
- Uses PENDING arrays for non-destructive dashboard merges
- **Effort**: ~4 hours (dashboard JS changes + AI workflow)
- **Deliverables**: 
  - Modified `productivity-dashboard.html` with PENDING_TASKS merge logic
  - Modified `roadmap-dashboard.html` with PENDING_STAKEHOLDER_ITEMS + PENDING_SPRINT_ASSIGNMENTS merge logic
  - Documented "cascade" workflow

### Phase 1.5: Sync on Update Protocol (Step 5.5)
- Define the project ↔ doc ↔ card registry (which proj-N maps to which docs and sh-N items)
- Document the sync map (which fields propagate where)
- AI behavioral protocol: on any project surface edit, check and propagate to linked surfaces
- Add `links[]` arrays to all existing projects and stakeholder items (primary link source for both PM and team views)
- Maintain `prdLink` and `docFile` fields for backward compatibility; `links[]` takes precedence
- **Effort**: ~1 hour (documentation + field backfill)
- **Deliverable**: Sync protocol documented, all existing project↔doc links populated, stakeholder cards show link pills matching productivity dashboard

### Phase 2: Jira Done → Experiment Bridge (Step 6)
- Enhance `refresh-roadmap.sh` to diff against previous state
- AI workflow for experiment setup
- **Effort**: ~2 hours
- **Deliverable**: Enhanced refresh script + experiment brief template

### Phase 3: Monthly Releases Page (Step 8) — NEW
- Build `analysis/monthly-releases.html` — interactive timeline page
- Seed with historical releases/experiments (Q1 2026 data already exists)
- PENDING_RELEASES merge logic for AI-assisted entry creation
- Add to hub (`index.html`) and back-to-hub navigation
- **Effort**: ~4 hours (visual-engineering delegation)
- **Deliverables**:
  - Working monthly releases page with sidebar nav, expandable cards, export
  - Seeded with Q1 2026 data (Prebid, Mystery Box, Skin Vault, Peripherals, etc.)
  - Root copy synced for GitHub Pages

### Phase 4: Weekly + QBR Automation (Steps 7, 9)
- Enhance "prep Friday slide" workflow to pull structured project data
- QBR generation now pulls from Monthly Releases page data (Step 8 → Step 9)
- Add QBR entry generation on project completion
- Create `qbr-q2-2026-entries.md` running file
- **Effort**: ~2 hours
- **Deliverable**: Richer weekly prep, QBR entry template

### Phase 5: Slack Integration (Step 10)
- Set up Incoming Webhook (requires Slack workspace admin or permission)
- AI formats Block Kit JSON from templates
- Monthly Releases page URL replaces PDF attachment on Slack posts
- Confirm-then-post workflow
- **Effort**: ~1 hour (+ admin approval for webhook)
- **Deliverable**: Working Slack posting via webhook

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    MORITZ (trigger)                       │
│                                                           │
│  "Create project" or "Cascade [name]"                    │
└─────────────┬─────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│                   AI ASSISTANT                            │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Task          │  │ Stakeholder  │  │ Sprint       │   │
│  │ Generator     │  │ Card Creator │  │ Suggester    │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│  ┌──────────────┐                                        │
│  │ Sync Engine   │ ← doc/card change detected             │
│  │ (Step 5.5)   │ → propagates to all linked surfaces    │
│  └──────────────┘                                        │
│         │                  │                  │            │
│         ▼                  ▼                  ▼            │
│  ┌─────────────────────────────────────────────────┐     │
│  │         PENDING ARRAYS (written to HTML)          │     │
│  │  PENDING_TASKS │ PENDING_SH │ PENDING_SPRINT     │     │
│  │                │            │ PENDING_RELEASES    │     │
│  └─────────────────────────────────────────────────┘     │
│         │                                                 │
│  ┌──────┴──────┐                                         │
│  │ jira-cli    │ → Jira AD-XXX created                   │
│  └─────────────┘                                         │
│                                                           │
│  On Friday:    On ship:        On completion:  On ship:   │
│  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌────────┐ │
│  │ Weekly    │  │ Monthly    │  │ QBR Entry│  │ Slack  │ │
│  │ Slide     │  │ Releases   │  │ Generator│  │ Post   │ │
│  │ (Step 7)  │  │ (Step 8)   │  │ (Step 9) │  │(Step10)│ │
│  └──────────┘  └─────┬──────┘  └────┬─────┘  └────────┘ │
│                       │              │                     │
│                       │    pulls from│                     │
│                       └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│                   BROWSER (merge)                         │
│                                                           │
│  Productivity      Roadmap           Monthly Releases     │
│  Dashboard         Dashboard         Page                 │
│  ┌──────────┐     ┌──────────┐      ┌──────────┐        │
│  │merge     │     │merge     │      │merge     │        │
│  │PENDING → │     │PENDING → │      │PENDING → │        │
│  │localStorage    │localStorage    │localStorage        │
│  └──────────┘     └──────────┘      └──────────┘        │
│  + Sync Engine: AI edits files directly (no PENDING)     │
└─────────────────────────────────────────────────────────┘
```

---

## Project Lifecycle Stages

Every project follows a defined lifecycle. The roadmap Gantt view uses these stages to render progress bars — each stage maps to a visual segment on the bar, giving stakeholders an at-a-glance view of where every initiative stands.

### Stage Definitions

| # | Stage | Trigger | Who | Visual |
|---|---|---|---|---|
| 1 | **In Scoping** | PM opens the project | Moritz | Lightest shade of initiative color |
| 2 | **In Development** | Design, BE, or FE starts work (Jira ticket moves to "In Progress") | Anouk / Isabel / Egor / Teodor / Omar | Medium shade |
| 3 | **Ready** | Development complete, pending release or experiment setup | Team | Full bright |
| 3a | **Experimenting** | A/B test deployed and live | Moritz + team | Full bright (striped/patterned) |
| 3a✓ | **Concluded** | Experiment results in, go/no-go decision made | Moritz | Full bright (with verdict indicator) |
| 3b | **Released** | Shipped to production (no experiment required) | Team | Full bright |
| 4 | **Completed** | Fully rolled out — either post-experiment rollout or direct release confirmed | Moritz | Full bright, entire bar filled |

### Stage Flow

```
1. In Scoping
   │  PM opens project, writes brief, defines success metrics
   │  Specifies: does this feature require experimentation? (yes/no)
   │
   ▼
2. In Development
   │  Design / Backend / Frontend work begins
   │  Signal: Jira ticket status → "In Progress"
   │
   ▼
3. Ready
   │  Dev complete. Two paths:
   │
   ├─── Experiment required ──► 3a. Experimenting
   │                                │  A/B test live, monitoring
   │                                ▼
   │                            3a✓. Concluded
   │                                │  Results analysed, decision made
   │                                │  (confirmed / not confirmed / inconclusive)
   │                                ▼
   │                            4. Completed (rollout or sunset)
   │
   └─── No experiment ─────► 3b. Released
                                    │  Shipped to production
                                    ▼
                                4. Completed
```

### Scoping Phase Details

During **In Scoping**, the PM:
1. Creates the project in the Productivity Dashboard
2. Writes the product brief / one-pager
3. Defines success metrics (tied to NSM where applicable)
4. Declares whether the feature **requires experimentation**
   - If yes: experiment hypothesis, primary metric, and success threshold are defined upfront
   - If no: feature ships directly after dev completion
5. Triggers the cascade workflow (Steps 2-5 of the pipeline)

### Data Model Impact

Each stakeholder item in the roadmap gains these fields:

```javascript
{
  // Existing fields
  id, initiative, area, priority, impact, effort, status, eta, notes, jiraKey, prdLink, dashboardLink,

  // NEW: Lifecycle fields
  stage: 'scoping',           // 'scoping' | 'development' | 'ready' | 'experimenting' | 'concluded' | 'released' | 'completed'
  requiresExperiment: false,  // declared during scoping
  startDate: '2026-04-01',   // when project entered "In Scoping"
  devStartDate: null,         // when dev/design started (from Jira or manual)
  readyDate: null,            // when dev completed
  experimentStartDate: null,  // when A/B test went live (if applicable)
  concludedDate: null,        // when experiment results were finalised (if applicable)
  releasedDate: null,         // when shipped to production
  completedDate: null         // when fully rolled out
}
```

### Gantt Progress Bar Rendering

The roadmap Gantt uses `startDate` → `eta` as the full bar width. The progress fill is split by lifecycle stage:

```
[In Scoping ░░░|In Dev ▓▓▓▓▓|Ready ████|Remaining ·····]
                                         ▲
                                      TODAY line
```

- **Filled segments** (left of today): Show completed stages in progressively darker shades
- **Faded segment** (right of today): Shows remaining planned duration
- **TODAY marker**: Vertical line across all rows, anchored to current date

### Automation Hooks

| Transition | Trigger | Automation |
|---|---|---|
| → In Scoping | PM creates project | Cascade command (Steps 1-5) |
| → In Development | Jira ticket → "In Progress" | `refresh-roadmap.sh` detects status change, updates `devStartDate` |
| → Ready | Jira ticket → "Done" | `refresh-roadmap.sh` detects, prompts PM |
| → Experimenting | PM confirms experiment setup | AI updates stage + `experimentStartDate` |
| → Concluded | PM enters results | AI updates stage + `concludedDate` + verdict |
| → Released | PM confirms ship | AI updates stage + `releasedDate` |
| → Completed | PM confirms full rollout | AI updates stage + `completedDate`, triggers Steps 8-10 |

---

## Key Design Decisions

### Why AI assistant as orchestrator (not GitHub Actions)?

| Consideration | AI Assistant | GitHub Actions |
|---|---|---|
| **Runs locally** | ✅ Has access to file system | ❌ Runs in cloud |
| **localStorage access** | Via HTML file edits (PENDING arrays) | ❌ No browser access |
| **Jira access** | ✅ Via jira-cli (already configured) | Needs secret config |
| **Slack access** | ✅ Via curl + webhook | ✅ Via webhook action |
| **Judgment calls** | ✅ Can ask Moritz, iterate | ❌ Runs unattended |
| **Context** | ✅ Knows project history, team, priorities | ❌ Stateless |
| **Latency** | Real-time | Minutes (workflow dispatch) |

**Verdict**: AI assistant is the right orchestrator for Steps 1-5 and 7-10 (interactive, needs judgment). GitHub Actions is only needed if we want unattended Jira→experiment detection (Step 6) — but that's a future enhancement.

### Why PENDING arrays instead of direct localStorage manipulation?

The dashboards run in a browser. The AI edits files on disk. There's no bridge between them — the AI can't execute JavaScript in the browser context. The PENDING array pattern solves this:

1. AI writes data to a JavaScript array in the HTML file
2. On next page load, the dashboard's `init()` function checks for pending items
3. Merges them into localStorage (additive, not destructive)
4. Clears the PENDING array (or sets a processed flag)

This is the **simplest reliable bridge** between the AI's file-editing capability and the browser's localStorage-based state.

### Why semi-automated steps?

Steps 4 (sprint assignment), 6 (experiment setup), 7 (weekly update), 8 (monthly releases), 9 (QBR entry), and 10 (Slack post) require **judgment**:
- Sprint assignment depends on team bandwidth that changes daily
- Experiment setup needs metric selection and success criteria
- Weekly updates need narrative framing, not just data dumps
- Monthly releases entries need accurate metrics and impact framing
- QBR entries need strategic positioning
- Slack posts need tone calibration

Step 5.5 (Sync on Update) is deliberately **automated**, not semi-auto, because sync is mechanical rather than editorial: when mapped field A changes, mapped field B should always be updated.

The AI drafts; Moritz confirms. This avoids automation that produces low-quality output nobody trusts.

---

## Open Questions

1. **Slack webhook permissions** — Does Moritz have permission to create an Incoming Webhook in the ESL FACEIT Group Slack workspace? If not, who approves?

2. **Jira epic vs. story** — Should the auto-created ticket be a Story (individual deliverable) or an Epic (container for sub-tasks)? Current design assumes Story. If Epic, the AI would also need to create child tickets for each task in Step 2.

3. **Sprint assignment confirmation UX** — Should the AI propose sprint assignments in chat (current design), or should the roadmap dashboard have a "Review Suggestions" panel that shows pending assignments with accept/reject buttons?

4. **Experiment template** — What fields should the experiment brief include? Current thinking: hypothesis, primary metric, secondary metrics, duration, sample size, success threshold. Does this match Moritz's mental model?

5. **Multi-quarter scope** — This design assumes Q2 sprint dates. Should the system auto-generate future quarter sprints, or is that done manually each quarter?

6. **Monthly Releases page — historical seeding** — Should the page be pre-populated with Q1 2026 data (Prebid migration, Mystery Box, Skin Vault launch, Peripheral expansion, Trust Modal, etc.) or start fresh from April?

7. **Monthly Releases page — experiment report format** — The existing experiment reports are PDFs in `Experiments/` and HTML dashboards in `analysis/`. Should the monthly page embed summary charts inline (using Chart.js) or just link to the existing dashboards?

---

## Next Steps

1. **Moritz reviews this proposal** — confirms approach, answers open questions
2. **Phase 0**: Build "Add Project" modal in Productivity Dashboard
3. **Phase 1**: Implement PENDING array merge logic + cascade command
4. **Phase 1.5**: Document sync protocol and backfill project↔doc links
5. **Phase 3**: Build Monthly Releases & Experiments interactive page
6. **Phase 5 prerequisite**: Set up Slack webhook (needs workspace permissions)
