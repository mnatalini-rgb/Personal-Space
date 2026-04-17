## **Problem**

Interstitial ads deliver the highest CPMs due to their strong impact (high visibility and CTR).  
However, they are also highly intrusive. Increasing interstitial inventory volume risks:

* user frustration and churn  
* reduced session depth  
* long-term CPM degradation due to poorer user experience

As a result, we cannot safely grow revenue by increasing interstitial frequency.

## **Product Goal**

Increase revenue from interstitial ads without increasing inventory volume, by improving ad quality and advertiser value.

## **Proposed Solution**

Maintain the same interstitial inventory size, but increase CPMs by upgrading the creative format.

Specifically:

* Replace static image interstitials with video interstitials  
* Leverage video’s higher impact to drive stronger advertiser outcomes (viewability, CTR, brand lift)

## **Format Options Considered**

* [Bumper video](https://support.google.com/displayvideo/answer/7245674?hl=en) ads (short, non-skippable)  
* Skippable video interstitials

Given the intrusiveness of the format, skippable video is the preferred starting point to balance revenue uplift with user experience.

## **Constraints & UX Principles**

### Skip behaviour

Video interstitials must allow users to skip or close the ad to avoid excessive disruption.

There is no single hard industry rule, but clear convergence around skip timing:

* Major platforms (YouTube, Google Ad Manager, video networks) typically allow skipping after \~5 seconds  
* Skip offset is usually configurable and agreed between buyer and seller  
* IAB guidelines recommend balancing advertiser needs with user experience rather than enforcing a fixed standard

## **MVP Definition**

Skippable video interstitial with a 5-second unskippable segment, after which a clear *Skip* or *Close* control is shown.

This:

* aligns with established user expectations (YouTube-like behaviour)  
* preserves advertiser impact in the opening seconds  
* reduces risk to retention compared to fully unskippable formats

### Confirmed Flow (April 2026)

Homepage → **Play** → **Find a Match** → **Video Interstitial Modal** → System searches for a match.

The ad plays **before** the matchmaking queue starts (not during), to avoid user perception of longer wait times. Once the video completes, the match search begins automatically.

### MVP UX Requirements

| Element | Spec |
|:--|:--|
| **Sound** | Sound-on by default (user-initiated action). User can mute manually. |
| **Display** | Full-screen interstitial overlay — user cannot interact with the page behind it |
| **Remaining time** | UI element showing remaining video duration |
| **Skip** | 1 skip per day. After the daily skip is used, the skip button transitions to an **"Upgrade"** button (premium upsell) |
| **Onboarding** | No ads on the first match. Ads begin from the **2nd match onward** to build user momentum |
| **Communication** | Clear upfront UI explaining the ad will play with sound, the duration, and the skip mechanics |

### Future: Smart Skip System (Post-MVP)

A context-aware skip system could offer additional free skips based on the user's state — e.g., after losing a match or filing a report. This accounts for the player's mental state and creates a more scalable, user-respectful pattern. **Not in MVP scope.**

## **Further Testing & Iteration**

After MVP validation, explore:

* Shorter skip offsets (e.g. 3 seconds) for very short videos (10–15s)  
* Persistent *Skip* or *Close* controls for high-frequency users  
* Format comparison:  
  * static interstitial vs video  
  * bumper vs skippable video  
* Creative length and format sensitivity

Goal: identify the best CPM uplift without measurable UX degradation.

## **Success Metrics**

### Primary metrics

* Viewability  
* CTR  
* CPM uplift vs static interstitial baseline

### **Secondary metric**

* Net revenue (CPM × fill × impressions)

### **Guardrail metrics**

* User dwell time on the platform  
* Number of matches played per session  
* Session abandonment rate (if available)

## Discovery & Design

Initial UX explorations and format concepts:  
[https://www.figma.com/design/QpjhKpg2hE9Dp71CcvqNpC/Ad-formats-2025?node-id=6270-180511\&t=SZAYYwdXfTmKbSNU-1](https://www.figma.com/design/QpjhKpg2hE9Dp71CcvqNpC/Ad-formats-2025?node-id=6270-180511&t=SZAYYwdXfTmKbSNU-1)

Play Interstitial concept board (April 2026):  
[https://www.figma.com/board/PRwDAnFVQpYASGFeg0E8b7/Video-Interstitial-Play?node-id=0-1\&t=iw9eKdWDLP2J8MZ9-1](https://www.figma.com/board/PRwDAnFVQpYASGFeg0E8b7/Video-Interstitial-Play?node-id=0-1&t=iw9eKdWDLP2J8MZ9-1)

## Experiment & Validation Plan ~~(Next Step)~~ — Completed

**Status**: Experiment concluded 14 April 2026. Go-to-market agreed 15 April 2026.

* A/B test ran 16 March – 14 April 2026 (31 days, 6.47M impressions, 184 countries)
* **Retention guardrail: PASSED** — variant +0.3% vs control (not statistically significant)
* 70.4% video completion rate (GAM); 83.3% full-15s on FE events
* 0.37% CTR → 23,698 clicks → 320 Premium subscriptions (46 direct, 274 view-through)

**Decision**: Move to production. Commercial team owns GTM.

Full experiment report: `skippable-video-dashboard.pdf`

**Experiment tracking**:  
[Mixpanel Board — Play Interstitial Experiment](https://mixpanel.com/project/137688/view/12355/app/boards#id=11052829&edited-bookmark=uxPweTDqbXsg)

