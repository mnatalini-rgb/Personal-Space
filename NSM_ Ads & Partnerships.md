# Proposed new NSM: “*Total Advertiser ROI Index”*

## **Background, Why we’re revisiting the North Star Metric** 

Our team owns two monetisation products that create advertiser value in fundamentally different ways:

**1\. Brand Integrations (Missions, Branded Event , Drops)**  
These products are performance-oriented and are built to drive *verified user actions* for partners. Because we run account linkage and operate a CDP integrated with advertiser CRM signals, we have unusually strong visibility into the full customer journey across both sides:

* On FACEIT: activation, engagement, reward claims, repeat participation  
* On the advertiser side: account creation, KYC completion, deposits/purchases, repeat deposits/purchases, retention signals

As a result, our success is best expressed through *outcome metrics* such as account linkage rate and first/second conversion events (user acquisition and downstream value).

**2\. Advertising (display \+ outstream video, including programmatic/indirect, match takeover)**  
Advertising is more traditional: we monetise user attention and inventory through measurable ad delivery and quality signals. The operating metrics are primarily:

* **Quality & performance**: viewability, CTR, video completion (where relevant)  
* **Supply & monetisation health** (especially programmatic): fill rate, eCPM, inventory coverage, unfilled impressions

These metrics reflect the “attention product” health, but they do not directly map to the same user-level outcomes we measure on Brand Integrations.

Because we operate across both a performance funnel (Brand Integrations) and an attention / inventory funnel (Advertising), our current measurement framework is fragmented: it optimises locally within each product but doesn’t provide a single, shared definition of “success” across the portfolio.

**Why revenue is not a good North Star (and what we should optimise instead)**

Revenue is an important business outcome, but it’s a weak North Star metric for product decision-making especially in advertising, because it is heavily influenced by factors that are not directly caused by product quality or user value.

Revenue fluctuates due to:

* **Sales & commercial decisions** (pricing, deal structure, discounts)  
* **Seasonality and market dynamics** (macro ad spend cycles, auction pressure, advertiser budgets)  
* **Geo and inventory mix** (different CPM baselines by region)  
* **Partner constraints and compliance** (KYC, legal, approvals) that delay outcomes independently of product  
* **Traffic shifts** (volume changes can raise revenue even when user value and advertiser value fall)

The risk is that a revenue-led NSM can reward the wrong behaviour:

* prioritising short-term monetisation over durable advertiser outcomes  
* chasing volume at the expense of quality (e.g., lower viewability inventory, lower-intent users)  
* masking underlying product issues because revenue can rise while satisfaction, retention, or outcome quality declines

Instead, a strong NSM should measure **customer value created** (i.e., advertiser value), because:

* it is more directly influenced by product changes and user experience  
* it is decomposable into levers teams can actually improve  
* it remains meaningful even when pricing or market conditions change

For Brand Integrations, “customer value” is expressed as verified actions and conversions. For Advertising, “customer value” is expressed as qualified attention and deliverable quality (e.g., viewable impressions, completion rates), which drive advertiser outcomes downstream.

## **What we need from a shared NSM across both products**

A unified NSM should:

* **Measure advertiser value, not internal revenue**  
* **Work across different activation models** (performance activations vs inventory-based delivery)  
* **Reward quality and efficiency**, not just scale  
* **Be comparable across geo-targeted activations**, by normalising against the *eligible audience* (not total DAU)  
* **Be actionable**, so each product team can clearly see what to improve (conversion ladder for BI; attention quality for Ads)

This is why we propose shifting from disconnected product metrics (AL/conversions vs CTR/viewability/fill/eCPM) toward a single metric framework that translates both products into a common “advertiser value” language, while still allowing each area to optimise through its own levers.

## **Proposed NSM: a single metric that works for Brand Integrations and Advertising (and for geo targeting)**

### **Summary**

I propose we adopt a unified North Star Metric based on Advertiser Value created per eligible audience, combining:

* **Outcome Value** from Brand Integrations (verified conversions \+ account linkage), and  
* **Attention Value** from Advertising (qualified, viewable ad exposure)

This creates one shared definition of success across the portfolio, while staying actionable for each product area.

## **1\. The core idea: normalise by *eligible audience*, not total DAU**

Because both Brand Integrations and Advertising are often activated by geo, using global DAU/MAU as a denominator produces misleading results (we would penalise campaigns that run in smaller geos and inflate those running in broader geos).

Instead we define **eligible users** per product:

* **Eligible BI Users (EBU)**  
  Users in the targeted geo(s) who had at least one opportunity to engage with a brand activation (e.g., Mission/Branded Event/Drop surface impression or eligibility check).

* **Eligible Ad Users (EAU)**  
  Users in the targeted geo(s) who had at least one ad opportunity (e.g., at least one ad request / pageview containing an ad slot).

This ensures the NSM reflects product performance, not campaign coverage choices.

## 

## **2\. Define “Advertiser Value Units” for both products**

### **A. Brand Integrations: Outcome Value Units (verified, full-funnel)**

We convert the “conversion ladder” into a single score:

**Outcome Value Units (OVU) \= [Data point here](https://docs.google.com/spreadsheets/d/1VQFq8RIJgxw0s4f_voH_dhtJI9QwMYuPoHjAAr7nQ8Y/edit?gid=0#gid=0)**

* **wAL · Account Linkages** (user acquisition)   
* **\+ wK1 · Identification** (pass KYC)   
* **\+ wC1 · First Conversions** (first deposit, trade)  
* **\+ wC2 · Second Conversions** ()  
* **\+ wC3 · Third Conversions** ()

**Why ladder-based:** it captures first conversion, repeat conversion, and quality (account linkage) in one number, and aligns with how partners actually value cohorts over time. Starter weights (illustrative; calibrate with data/partner economics later):

* AL \= 3 ($3)  
* C1 \= 6 ($7)  
* C2 \= 9 ($20)  
* C3 \= 3 ($3)

**Brand Integration NSM component**: OVU per 1,000 Eligible BI Users \= OVU ÷ EBU × 1000

### **B. Advertising: Attention Value Units (qualified attention, not just clicks)**

Clicks (CTR) are useful diagnostics but are volatile and easy to game depending on placement. A more stable proxy for advertiser value is **qualified attention**, expressed as viewable delivery and (where relevant) completion.

**Attention Value Units (AVU) \= Viewable Impressions** (base)

**Advertising NSM component: AVU per 1,000 Eligible Ad Users \= AVU ÷ EAU × 1000**

(We continue to use fill-rate and eCPM as operational levers/diagnostics rather than embedding them directly into the NSM, to avoid market pricing noise dominating the metric.)

## 

## 

## 

## **3\. The unified NSM: “*Total Advertiser Value Index”***

Because each product has a different “eligible audience,” the cleanest combined NSM is a weighted index of the two normalised rates:

### **North Star Metric: Total Advertiser Value Index (TAVI)**

**TAVI \= α · (OVU per 1K EBU) \+ (1 − α) · (AVU per 1K EAU)**

Where:

* **α** is the strategic weighting between Brand Integrations and Advertising (e.g., 0.5 / 0.5 to start, or weighted by long-term strategy).

**What leadership gets:**

* one number to track overall monetisation value creation  
* plus two transparent components to understand the drivers

**What teams get:**

* **Brand Integrations can directly improve OVU via AL and conversion ladder progression**  
  **Advertising can improve AVU via viewability, completion, and inventory quality**

## **3a. MVP: “BE Total Advertiser Value”**

As these values are all theoretical and need validation, it make sense to start with separating the NSM between Brand Integration and Advertising at the start. 

* TAVI BI:  **How much ($) value we drove per partner?**

## **3b. Secondary Metrics** 

**BI** 

* **EBU**  
* **AL · Account Linkages**  
* **C1 · First Conversions** (e.g., signup/KYC/first purchase/first deposit)  
* **C2 · Second Conversions** (e.g., 2nd deposit/purchase, retention milestone)  
* **C3 · Third Conversions**   
* **CR Completion Rate**   
* **Total Revenues** 

**AD**

* **EAU**  
* **Total Impressions**  
* **Viewable Impressions (%)**  
* **Average CTR**   
* **eCPM**  
* **Fill-rate** 

## **4\. Practical examples** 

How will the NSM help us understand that we are doing? 

**Practical example: Winline Brand Integration NSM ([Nov vs Dec](https://docs.google.com/spreadsheets/d/1mU7fkEIxDX2cxBXFYrsQ1l3L2cxjLoh5avcne2ycTWw/edit?gid=540808589#gid=540808589))**

**NSM definition (Brand Integrations)**  
**OVU per 1,000 Eligible BI Users (EBU)** \= **OVU ÷ EBU × 1000**  
Where **OVU** is a weighted “conversion ladder” score: **OVU \= 3·AL \+ 6·C1 \+ 9·C2 \+ 3·C3**

* **AL** \= Account Linkages  
* **C1** \= First conversion (e.g., KYC)  
* **C2** \= Second conversion (e.g., first deposit milestone)  
* **C3** \= Third conversion (deeper milestones: higher deposits \+ betting activity)

**December (EBU \= 391,000)**

**Ladder volumes (mission completions)**

* **AL:** 2,709  
* **C1 (KYC):** 301  
* **C2 (Deposit ≥ 500 RUB):** 335  
* **C3 (deeper deposits \+ bets):** 20,883

**OVU calculation**

* 3×2,709 \= 8,127  
* 6×301 \= 1,806  
* 9×335 \= 3,015  
* 3×20,883 \= 62,649  
  **Total OVU (Dec) \= 75,597**

**NSM (Dec)**

* 75,597 ÷ 391,000 × 1000 \= **193.3 OVU / 1,000 EBU**

**November (EBU \= 449,825)**

**Ladder volumes (mission completions)**

* **AL:** 5,663  
* **C1 (KYC):** 163  
* **C2 (Deposit ≥ 500 RUB):** 207  
* **C3 (deeper deposits \+ bets):** 26,087

**OVU calculation**

* 3×5,663 \= 16,989  
* 6×163 \= 978  
* 9×207 \= 1,863  
* 3×26,087 \= 78,261  
  **Total OVU (Nov) \= 98,091**

**NSM (Nov)**

* 98,091 ÷ 449,825 × 1000 \= **218.1 OVU / 1,000 EBU**

**Comparison (Nov → Dec)**

* **NSM declined from 218.1 → 193.3**  
* Absolute change: **\-24.8 OVU / 1,000 EBU**  
* Relative change: **\-12.8%**

**Primary driver:** most OVU comes from **C3 (deeper milestones)** in both months, so changes in deeper conversions have an outsized impact on NSM.

## **Retool POC**

[NSM per Partner](https://docs.google.com/spreadsheets/d/1VQFq8RIJgxw0s4f_voH_dhtJI9QwMYuPoHjAAr7nQ8Y/edit?gid=0#gid=0)

NSM: 

* TAVI BI   
* OVU**:** conversion ladder  
* EBU: total unique users that joined a competition

Filters: 

* Organiser: Winline, WhiteMarket, Tradeit, PaySafe (soon)  
* Competition: Mission, Branded Event (later)  
* Date:   
* Country: activation countries 

Metrics:

* UU activated by challenge (KPI)  
* UU completed by challenge (KPI)  
* Completion Rate by challenge (KPI)  
* KPIs  
  * Account Linkages  
  * Conversion points  
    * First Conversions (e.g., signup/KYC/first purchase/first deposit)  
    * Second Conversions (e.g., 2nd deposit/purchase, retention milestone)  
    * Third Conversions 

* Show basic filtering (**organizer**, dates, specific mission...)  
* **Results (per partner):**  
  * Total distinct users that activated  
    * We should have total users activated per mission  
      * *The final result will be the average \+ median calculated from the data above*  
  * Total distinct users that completed 100% of the total missions that they activated  
    * *Are we interested on partial completion??*  
    * *The final result will be the average \+ median calculated from the data above*  
  * Total distinct users \+ Total revenue  
    * First conversions  
      * Linked account \--\> *Triggered from web modals in one of the partner missions?*  
      * KYC  
      * First deposit  
  * For second and third conversions, since users can trigger them several times in a period, I think we can have:  
    * Other conversions  
      * Per conversion:  
        * *Total distinct users vs Total conversions \+ Total revenue*

* *Do we have the full data of revenue per conversion in euros? (in the excel)*  
* *Do you want me to show the consider revenue per conversion in retool?*  
* *Do we have extra associated revenue per activation / completion?*

  