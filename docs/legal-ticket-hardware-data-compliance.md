# Legal Review Request: User Hardware Data — Collection Compliance & Advertising Use

**Requested by:** Moritz Natalini — Director of Product, Monetisation
**Date:** 26 March 2026
**Priority:** High
**Team:** Legal / Privacy

---

## Summary

The Product team is collecting user hardware and peripheral data via the FACEIT Client. We need Legal to assess:

1. **Whether our current data collection is compliant** under GDPR and other applicable privacy regulations
2. **What we need to do (consent, disclosures, etc.) to use this data for advertising purposes** — specifically for peripheral brand targeting, hardware-based audience segmentation, and advertiser reporting

---

## Context

### What data we collect

The FACEIT Client already captures the following hardware telemetry from users' machines:

| Data Point | Example | Fill Rate |
|---|---|---|
| CPU Make & Model | Intel Core i5-12500H, AMD Ryzen 5 5600G | ~100% |
| Motherboard / OEM / System Manufacturer | ASUS, Gigabyte, Monster, Lenovo | ~100% |
| Peripheral Device Type | Mouse, Keyboard | ~100% |
| Peripheral Brand | Logitech, Razer, SteelSeries, Corsair | ~85% |

### Scale

- **193,000 unique users** across **152 countries** (as of Mar 2026)
- Data is collected **once per week** while the FACEIT Client is running
- Each user typically generates ~2 records (keyboard + mouse)

### Current use

Today this data is used **internally only** for product research — understanding what hardware our users have to inform profile feature design decisions. It is not surfaced to users, advertisers, or any third party.

### Proposed advertising use

We want to explore using this data for monetisation:

1. **Audience segmentation for advertisers** — e.g., "users with Logitech peripherals", "users with AMD CPUs", "budget vs premium hardware setups"
2. **Brand targeting** — serving peripheral brand ads to users who don't already own that brand (conquest targeting)
3. **Aggregated reporting to advertisers** — e.g., "X% of your ad impressions were served to users with gaming-grade peripherals"
4. **Potential profile display** — showing hardware setup on user profiles (with user control/consent)

---

## Questions for Legal

### A. Current Collection

1. **Is our current collection of hardware telemetry via the FACEIT Client covered by the existing Terms of Service and Privacy Policy?** If not, what changes are needed?
2. **Do we need explicit user consent (opt-in) for this data collection**, or is it covered under legitimate interest given the client already runs on their machine?
3. **Are there jurisdiction-specific concerns?** We have significant user populations in Turkey (largest), Ukraine, Brazil, Kazakhstan, Argentina, Russia, and EU (Germany, France, Italy, UK). Do any of these require special handling?
4. **Data classification** — Is peripheral brand/hardware data considered personal data under GDPR? It's device-level data tied to a user account.

### B. Advertising Use

5. **What consent mechanism is required to use hardware data for ad targeting?** Do we need a separate opt-in for advertising use beyond collection consent?
6. **Can we share aggregated (non-PII) hardware data with advertisers** in reporting? e.g., "35% of impressions served to Logitech users" — does this require consent?
7. **Can we use hardware data for audience segmentation in our ad server** without sharing raw data externally? (Data stays within FACEIT systems, only used to select which ads to show.)
8. **Do we need to update the Privacy Policy** to explicitly mention hardware data collection and its use for advertising?
9. **ePrivacy / cookie-like consent** — Since the FACEIT Client reads device hardware info (not cookies, but local device data), does this fall under ePrivacy Directive requirements in the EU?
10. **Profiling under GDPR Art. 22** — Does building hardware-based audience segments constitute automated profiling that triggers additional obligations?

### C. User Controls

11. **What user controls do we need to provide?** Options we're considering:
    - Opt-out of hardware data collection entirely
    - Opt-out of advertising use specifically (allow collection for product but not ads)
    - Granular control (choose which data points to share)
12. **Right to deletion** — If a user requests data deletion under GDPR Art. 17, does this extend to aggregated/anonymised hardware data already used in reporting?

### D. Implementation Timeline Considerations

13. **Can we proceed with internal product use (profile feature design) while the advertising compliance is being assessed?** We'd like to avoid blocking product work.
14. **What's the minimum viable consent flow** that would allow us to begin testing hardware-based ad targeting with a limited partner pilot?

---

## Supporting Materials

- **Dashboard with full data breakdown**: [Peripheral Initiative Dashboard](https://mnatalini-rgb.github.io/Personal-Space/peripheral-data-dashboard.html) — includes country/tier splits, brand landscape, data collection overview
- **Data fields documentation**: Available in the dashboard Section A
- **Current Privacy Policy**: [link TBD — Legal to confirm current version]
- **FACEIT Client data collection docs**: [link TBD — Engineering to provide]

---

## Desired Outcome

A written Legal opinion covering:

1. ✅ / ❌ Whether current hardware data collection is compliant as-is
2. A list of required actions (consent changes, policy updates, user controls) to enable advertising use
3. Any jurisdiction-specific blockers we need to address before scaling
4. Recommended timeline and sequencing for compliance work

---

*Please reach out to Moritz Natalini for any follow-up questions or to schedule a walkthrough of the data and proposed use cases.*
