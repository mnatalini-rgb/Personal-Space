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

## Experiment & Validation Plan (Next Step)

* A/B test:  
  * Control: static interstitial  
  * Test: skippable video interstitial (5s skip)  
* Validate whether revenue per user increases without negative behavioural impact

