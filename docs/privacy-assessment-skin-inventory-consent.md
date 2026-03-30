# Privacy Assessment Request: User Consent for Skin Inventory Display on Profiles

**Requested by:** Moritz Natalini — Director of Product, Monetisation
**Date:** 26 March 2026
**Priority:** High
**Team:** Privacy

---

## Summary

We are building a feature that allows users to **display their CS2 skin inventory on their FACEIT profile**. Legal has reviewed the concept and confirmed no legal blockers — they've directed us to Privacy to define the **consent model** required before we can proceed with implementation.

---

## Context

### What the feature does

Users would be able to showcase their CS2 skin inventory on their FACEIT profile page. This involves:

1. **Reading the user's Steam inventory** — retrieving skin data (item name, condition, rarity) via Steam API
2. **Displaying skins on the FACEIT profile** — visible to other users browsing that profile
3. **Potential monetisation layer** — skin valuation data could be used for advertising targeting (e.g., users with high-value inventories as an audience segment for skin marketplace partners like Tradeit, WhiteMarket)

### What data is involved

| Data Point | Source | Sensitivity |
|---|---|---|
| Skin item names & conditions | Steam API (user's public/private inventory) | Tied to user account |
| Estimated skin values | Third-party pricing APIs | Derived data |
| Inventory size / total value | Calculated | Could reveal spending habits |
| Steam account link | Existing FACEIT-Steam integration | Already collected |

### Current state

- FACEIT already has Steam account linkage for most users (required for matchmaking)
- Steam inventory visibility is controlled by the user's Steam privacy settings
- We do **not** currently read or store skin inventory data

### Legal guidance received

Legal has reviewed and confirmed:
- No fundamental legal blockers to the feature
- **Consent is the key requirement** — Privacy team to define what consent mechanism is needed

---

## Questions for Privacy

### A. Consent Model

1. **What type of consent is required?** Options we see:
   - **Opt-in toggle** — User explicitly enables "Show my skins on profile" (our assumption)
   - **Granular consent** — Separate consents for (a) reading inventory, (b) displaying publicly, (c) using for advertising
   - **Layered consent** — Basic display opt-in + separate advertising use opt-in

2. **When should consent be collected?**
   - At feature launch via a prompt/modal?
   - In profile settings (passive — user finds it)?
   - During a specific user flow (e.g., when visiting their profile for the first time after launch)?

3. **What must the consent notice include?** Please provide guidance on required disclosures:
   - What data we access
   - How it will be displayed
   - Who can see it
   - How it may be used beyond display (advertising, if applicable)

### B. Data Handling

4. **Can we cache/store skin inventory data**, or must we fetch it live from Steam each time? Storage implications for GDPR data minimisation.

5. **If a user revokes consent, what's the required deletion timeline?** Immediate removal from profile — but do we also need to purge cached inventory data?

6. **Derived data (valuations, segments)** — If we calculate a user's total inventory value for advertising segmentation, does revoking display consent also require deleting derived data?

### C. Advertising Use

7. **Can advertising use of skin data share the same consent as profile display**, or does it require a separate, explicit consent? (e.g., "We may also use your inventory data to show you relevant offers")

8. **If separate consent is required for advertising**, can we implement it as a two-tier model?
   - Tier 1: Display skins on profile (basic consent)
   - Tier 2: Use inventory data for personalised advertising (enhanced consent)

### D. Edge Cases

9. **Minors** — FACEIT has users under 18. Are there additional consent requirements for displaying their inventory/spending data publicly?

10. **Third-party data** — Skin pricing comes from third-party APIs. Any privacy implications of combining Steam data with third-party valuation data to create a "portfolio value"?

11. **Default state** — Should the feature default to OFF (opt-in) or ON (opt-out)? Our assumption is opt-in, but confirming.

---

## Proposed User Flow (for Privacy review)

```
User visits Profile Settings
  → Sees new "Skin Vault" section
  → Toggle: "Show my skin inventory on my profile"
  → Consent text: [TBD — need Privacy guidance on wording]
  → User enables → FACEIT reads Steam inventory → Displays on profile
  → User can disable at any time → Inventory removed from profile immediately
```

---

## Desired Outcome

1. **Approved consent model** — what type, when, and what disclosures
2. **Consent copy guidance** — what the notice must say (we'll draft, Privacy to approve)
3. **Data handling rules** — storage, retention, deletion on revocation
4. **Advertising use ruling** — same consent or separate consent required
5. **Timeline** — any dependencies on policy updates before we can ship

---

*Moritz Natalini is available for a walkthrough of the feature design and Skin Vault dashboard. Please reach out to schedule.*
