# PRD: Brand Takeover Improvements

| Field | Value |
|---|---|
| **Author** | Moritz Natalini |
| **Date** | 2026-04-01 |
| **Status** | Draft |
| **Stakeholders** | Engineering (Irene), Design (JB/SM), Sales (Adam Goh), Data (Egor), Commercial (SM) |
| **Product Area** | Brand Integrations |

---

## 1. Background & Context

Brand Takeover is FACEIT's ladder-based sponsorship format — a geo-exclusive, full-event takeover that sits between Missions (performance) and traditional advertising (awareness). Each event delivers 9–20 brand impressions per unique player. Key features include Drops, Account Linkage, Match Skin, Prize Expiration, and Rewarded Video (currently in testing with Logitech).

Following the March 2026 Logitech Brand Takeover (the 3rd BT), a retro surfaced several operational and product issues that need to be addressed before scaling Brand Takeover as a repeatable commercial product. These fall into three categories:

1. **Reporting & Data Quality** — incorrect data sent to the agency, no geo breakdown, lack of 3P tracking capabilities
2. **Operational Process** — internal miscommunication, unclear design R&R, geo-restriction testing gaps, backoffice access issues
3. **Product Iteration** — Rewarded Video needs A/B testing with proper experiment design; CTR collection needs improvement

This document captures all improvement items and defines the experiment design for Rewarded Video testing.

---

## 2. Problem Statement

**Who**: Sales team (Adam Goh), agency partners, internal ops (JB/SM), PM (MN)

**Problem**: Brand Takeover is commercially promising but operationally fragile. The March retro exposed gaps in data accuracy, internal communication, and measurement capabilities that undermine partner trust and limit our ability to sell confidently.

**Impact**:
- Incorrect data sent to agency **twice** — erodes partner confidence
- No geo-level reporting — agencies need granular breakdowns; we can't provide them
- No impression pixel / 3P tracking — limits what we can promise in pre-sale and prevents independent verification
- Unclear internal design R&R — caused confusion and delays when client requested redesign
- Rewarded Video untested at scale — can't price or sell without validated claim-rate data
- CTR collection is unreliable — undermines performance narrative

---

## 3. Goal & Success Metrics

| Metric | Current | Target | Measurement Method |
|---|---|---|---|
| Reporting accuracy | Data sent incorrectly (2 incidents in 1 event) | Zero data corrections post-delivery | QA checklist before agency send |
| Geo-level reporting | Not available | Full geo breakdown in NSM dashboard | BQ query + dashboard update |
| Rewarded Video claim rate | Unknown (testing phase) | Statistically significant result across variants | A/B/C experiment (see §4) |
| CTR collection reliability | Inconsistent | Consistent, automated collection per event | Engineering fix + QA process |
| 3P tracking capability | Not documented | BE Ad Spec published (pre/post sale) | SM to create spec document |
| Pre-launch QA pass rate | Ad-hoc | 100% checklist completion before go-live | Process doc + Jira template |

**NSM Connection**: Brand Takeover drives OVU/1K EBU via brand impressions and account linkage. Improving data quality and measurement directly increases partner confidence → renewal rate → portfolio value.

---

## 4. Proposed Solution

### 4a. Rewarded Video A/B/C Experiment

**Objective**: Determine whether Rewarded Video increases the drop claim rate, and whether video rotation outperforms a single video.

| Variant | Description |
|---|---|
| **Control** | No Rewarded Video — standard drop claim flow |
| **V1: Single Video** | One video creative shown at the drop claim moment |
| **V2: Video Rotation** | Multiple video creatives in rotation at the drop claim moment |

**Primary Metric**: **Claim Rate** — % of eligible users who claim the drop after being exposed to the variant

**Secondary Metrics**:
- Video completion rate (V1, V2 only)
- Time-to-claim
- Return visit rate (do RV users come back more?)
- Partner impression uplift (does RV add incremental brand impressions?)

**Traffic Split**: 33% / 33% / 34% (Control / V1 / V2)

**Duration**: Minimum 2 weeks or until n >= 5,000 per variant (whichever is longer)

**Geo**: Run on next available Brand Takeover event (coordinate with Adam Goh on partner selection)

**Feature Flag**: `exp_REWARDED_VIDEO_BRAND_TAKEOVER` with values `control`, `single_video`, `rotation`

### 4b. CTR Collection Improvement

**Problem**: CTR data is collected inconsistently across Brand Takeover events. Some events have no CTR data at all.

**Fix**:
- Standardise CTR tracking on all clickable Brand Takeover surfaces (match skin, ladder banner, drop notification, mission card)
- Implement server-side event logging (not client-side only) to eliminate data loss
- Add CTR as a required field in the post-event reporting template

### 4c. Reporting & Data Quality

**Problem**: Agency received incorrect data twice. No geo breakdown available. No 3P tracking capabilities documented.

**Fixes**:

| Issue | Owner | Action | Status |
|---|---|---|---|
| Incorrect data sent twice + lack of communication | MN | NSM dashboard now the single source of truth; add geo-level breakdown | In progress |
| Agency needs geo-level data | MN | Add geo breakdown requirement to product roadmap | To do |
| Impressions pixel — where to add | MN | Discovery: map all Brand Takeover surfaces where impression pixels could fire | To do |
| BE Ad Spec for pre/post sale | SM | Create slide specifying 3P tracking capabilities and limitations — keep it simple | To do |
| Backoffice access issue (Thu 12 Mar) | MN | Bug addressed — confirmed fix prevents recurrence | Resolved |
| Lack of internal communication | MN | Addressed — retro action items distributed | Resolved |
| Design R&R confusion on client redesign requests | JB/SM | Create doc for pre/post sale design requests with dedicated resource justification and LOE | To do |
| Unavailable test link due to geo restrictions | JB | Nice to have — not necessary as long as logged-in preview link and/or screenshots are available for approval prior to launch | Won't fix |
| Event launched with incorrect region (Fri 20 Mar) | MN | Retro with Irene — ensure it doesn't happen again | In progress |
| UTM links not applied + miscommunication on what's doable | MN | Events are not ad-served — cleared up. Document UTM capabilities in BE Ad Spec | To do |

---

## 5. User Stories / Requirements

| # | As a... | I want to... | So that... | Priority |
|---|---|---|---|---|
| 1 | Sales lead | have a BE Ad Spec document | I can clearly communicate tracking capabilities to agencies pre-sale | Must |
| 2 | PM | see geo-level Brand Takeover data in the NSM dashboard | I can provide agencies with the granular breakdowns they require | Must |
| 3 | PM | run an A/B/C test on Rewarded Video | I can price and sell RV as a validated add-on to Brand Takeover | Must |
| 4 | PM | have reliable CTR collection across all BT surfaces | I can report accurate performance data to partners | Must |
| 5 | Agency partner | receive correct data on the first delivery | I don't lose trust in the platform | Must |
| 6 | Designer | know whose R&R redesign requests are | I don't duplicate work or miss requests | Should |
| 7 | PM | have a pre-launch QA checklist | events don't go live with wrong region or missing assets | Should |
| 8 | Sales lead | have a global test link (not geo-restricted) | I can share live previews with clients anywhere | Could |

---

## 6. Scope

### In Scope
- Rewarded Video A/B/C experiment design and execution
- CTR collection standardisation across Brand Takeover surfaces
- Geo-level reporting in NSM dashboard
- BE Ad Spec document (3P tracking capabilities/limitations)
- Pre/post sale design R&R documentation
- Pre-launch QA checklist
- UTM capability documentation

### Out of Scope
- Rewarded Video as a standalone product (remains a BT add-on)
- Rebuilding the ladder service (owned by Matchmaking team)
- New Brand Takeover formats or templates
- Programmatic ad serving for Brand Takeover (events are not ad-served)

### Future Considerations
- Impression pixel integration on Brand Takeover surfaces (pending discovery)
- Rewarded Video pricing model (dependent on experiment results)
- Automated geo-level reporting pipeline (dependent on BQ/dashboard work)

---

## 7. Technical Considerations

- **Ladder dependency**: Brand Takeover uses the ladder service owned by the Matchmaking team. Any changes to event launch flow or feature flagging require coordination.
- **Feature flag**: `exp_REWARDED_VIDEO_BRAND_TAKEOVER` needs to be implemented in the drop claim flow. Coordinate with engineering (Irene).
- **CTR tracking**: Current implementation is client-side only for some surfaces. Server-side event logging needed for reliability.
- **Geo-level data**: Available in BigQuery (`user.page_view_v1` + event context). Dashboard update requires BQ query + HTML changes to NSM dashboard.
- **3P tracking**: Brand Takeover events are NOT ad-served. This limits 3P tracking to redirect URLs, UTM parameters, and any impression pixels we manually implement. This must be clearly documented in the BE Ad Spec.

---

## 8. Dependencies & Risks

| Dependency / Risk | Impact | Mitigation |
|---|---|---|
| Matchmaking team (ladder service) | High — any ladder bug blocks event launch | Pre-launch QA checklist; escalation path to Matchmaking |
| Partner availability for RV experiment | Medium — need a willing partner for A/B/C test | Coordinate with Adam Goh; Logitech likely candidate |
| Engineering bandwidth for CTR fixes | Medium — competes with other priorities | Scope minimal viable fix first |
| Design R&R clarity | Low — process issue, not technical | JB/SM doc resolves this |
| Agency trust after data incidents | High — repeat incidents could lose the account | QA checklist + single source of truth (NSM dashboard) |

---

## 9. Open Questions

- [ ] Which Brand Takeover event will host the Rewarded Video A/B/C experiment? (Adam Goh to confirm partner)
- [ ] What video creatives are available for V2 rotation? (Design team)
- [ ] Can we implement server-side CTR tracking within the current sprint? (Engineering)
- [ ] Where exactly should impression pixels fire on Brand Takeover surfaces? (Discovery with Engineering)
- [ ] What UTM parameters are technically feasible given events are not ad-served? (Engineering)
- [ ] Should the BE Ad Spec be a living document or a one-time deliverable? (SM)

---

## 10. Appendix

### Related Documents
- [Brand Integrations Overview](../product_documentation/Brand%20Integrations%20Overview.md)
- [Brand Takeover for AI docs](../product_documentation/Brand%20Takeover%20for%20AI%20docs.md)
- [Brand Product Lineup — Inventory Team](../brand-product-lineup-inventory-team.md)
- [Drops Documentation](../product_documentation/Drops%20.md)
- [NSM Dashboard](../../analysis/nsm-dashboard.html)
- [Brand Takeover Performance Tracker (Looker)](https://efgdata.cloud.looker.com/dashboards/752)

### Retro Source
March 2026 Logitech Brand Takeover retro — full action items captured in §4c table above.

---

## Updates

**2026-04-01** — Brief created. Captured all retro items from March Logitech BT. Designed Rewarded Video A/B/C experiment (Control vs Single Video vs Rotation). Identified CTR collection and reporting gaps. Linked to productivity dashboard as proj-13 (P2).
