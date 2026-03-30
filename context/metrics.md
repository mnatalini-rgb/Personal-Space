# Metrics Framework

> **Updated March 2026**: Total Partner Value now tracked on a **30-day rolling window** (not weekly). This smooths mission activation seasonality and aligns the metric with the ~1-month mission lifecycle. Weekly breakdowns remain available as an operational diagnostic.

## North Star Metric: Total Advertiser Value Index (TAVI)

**TAVI = α · (€ per 1K EBU) + (1 − α) · (AVU per 1K EAU)**

- **α** = strategic weighting between Brand Integrations and Advertising (start 0.5 / 0.5)
- Combines both product lines into one shared definition of advertiser value created

---

## Brand Integrations Component

### NSM: € per 1,000 Eligible BI Users (EBU)
**Total Partner Value / EBU × 1,000**

> **Tracking cadence**: 30-day rolling window, computed daily. Each day's value = sum of partner value generated in the preceding 30 calendar days. This replaces weekly bucketing to avoid noise from mission activation timing, reward expiration lags, and campaign lifecycle mismatches.

### ⚠️ DEPRECATED: Outcome Value Units (OVU)
The weighted OVU formula below is **deprecated** as of March 2026. We now use **direct € values per conversion point** (sourced from BQ + partner CRM signals). The conversion ladder structure remains — only the scoring changed from abstract weights to actual € values.

~~**OVU = 3·AL + 6·C1 + 9·C2 + 3·C3**~~

| Event | Label | € Value (current) | Legacy Weight | What it represents |
|-------|-------|--------------------|---------------|--------------------|
| Account Linkages | AL | Partner-specific (e.g. Tradeit €0.38, Winline €4.33) | ~~3~~ | User acquisition |
| First Conversion | C1 | Partner-specific (e.g. Tradeit €0.04, Winline €8.66) | ~~6~~ | KYC completion |
| Second Conversion | C2 | Partner-specific (e.g. Tradeit €8.75, Winline €121.10) | ~~9~~ | First deposit / purchase |
| Third Conversion | C3 | Partner-specific (e.g. Winline €4.33) | ~~3~~ | Deeper milestones |

### Eligible BI Users (EBU)
Users in targeted geo(s) who had at least one opportunity to engage with a brand activation (Mission/Branded Event/Drop surface impression or eligibility check).

### Secondary BI Metrics
- EBU (Eligible BI Users)
- Account Linkages (AL)
- C1, C2, C3 volumes
- Completion Rate (CR)
- Total Partner Value (€, 30-day rolling)
- Partner Efficiency (€/1K EBU, 30-day rolling)
- Total Revenue

---

## Advertising Component

### NSM: AVU per 1,000 Eligible Ad Users
**AVU / EAU × 1,000**

### Attention Value Units (AVU)
**AVU = Viewable Impressions**

### Eligible Ad Users (EAU)
Users in targeted geo(s) who had at least one ad opportunity (at least one ad request / pageview containing an ad slot).

### Secondary Advertising Metrics
- EAU
- Total Impressions
- Viewable Impressions (%)
- Average CTR
- eCPM
- Fill Rate

> Note: Fill rate and eCPM are operational diagnostics, not embedded in NSM — to avoid market pricing noise dominating the metric.

---

## MVP Approach (TAVI BI first)

Start by separating NSM between Brand Integrations and Advertising before combining:
- **TAVI BI**: How much (€) value we drove per partner?
- **Primary metric**: € per 1K EBU on a 30-day rolling window
- **Operational diagnostic**: Weekly breakdown for Monday slide updates and mission monitoring

---

## Reference Example: Winline Nov vs Dec

| Month | EBU | Total Partner Value (€) | NSM (€/1K EBU) |
|-------|-----|------------------------|-----------------|
| November | 449,825 | ~€1,089,000 | €2,421 |
| December | 391,000 | ~€1,089,000 | €2,785 |

*Values are illustrative. Actual € per conversion sourced from BQ + partner CRM signals. The 30-day rolling window smooths these monthly snapshots into a continuous trend.*

Primary driver: C2 (deposits/purchases) dominates partner value — changes in deep-funnel conversions have outsized NSM impact.

---

## Full reference
`reference/NSM_ Ads & Partnerships.md`
