# Active Initiatives

These are cross-cutting strategic bets that may benefit Brand Integrations, Advertising, or both. Monetisation model is not yet finalised for either.

---

## 1. Skin Vault

### What It Is

Skin Vault exposes a FACEIT user's CS2 skin inventory on their FACEIT profile page, sourced via the **Steam API** (public inventory only). The goal is twofold:
- Let users **show off** their inventory (identity/status signal)
- Help other users **discover new skins** (browse intent)

### Origin

Two research inputs validated the concept before building:
1. **User survey** — surfaced skin display/discovery as a desired feature
2. **Fake door test** — confirmed meaningful click intent before committing to full build

### Current Status

**Ready to experiment.** Constraints shape the rollout:

- **Steam API rate limits** restrict how many profile requests can be made — cannot go 100% immediately
- **Experiment design**: Top 300 most-viewed FACEIT profiles will be enabled. **50/50 split test** to measure impact on profile traffic and engagement.
- Hypothesis: if enough traffic is proven, the surface can be monetised

### Monetisation Direction

The primary monetisation idea is **CPC with Tradeit** — users browsing skins on a profile click through to trade/buy on Tradeit. This aligns directly with Tradeit's existing FACEIT partnership (account linkage + trades KPI).

Other monetisation ideas are TBD — "the fun part" — but they require sufficient traffic first.

### Privacy Considerations

- Current experiment uses public Steam inventory only — lower privacy risk
- If rolled out to 100% of users, a **privacy review will be required**
- Privacy contact: Akkeroos Kremers

### Key Dependency

- **Richard Lancaster** (PM, Game Integrations & Track) owns the Track page where Skin Vault is releasing. Any changes to the profile surface, rollout decisions beyond the top 300, or full launch require coordination with Richard. He also owns CSStats (the 3rd-party test environment used in Moba vs Publift A/B test). **Both Richard and his designer Jon Pieto have confirmed alignment on releasing the Skin Vault experiment.**

### Open Questions

- What traffic/engagement threshold justifies moving beyond the top 300 profiles?
- What is the full monetisation roadmap beyond Tradeit CPC?
- Does this benefit Brand Integrations (Tradeit), Advertising (inventory surface), or both?
- What are the Steam API rate limit boundaries at scale?

---

## 2. Peripheral Initiative

### What It Is

FACEIT has a desktop client. The client can **detect hardware components** from the user's machine — CPU, keyboard, mouse, and device manufacturer — using a service built by Egor.

The goal is to productise these first-party signals to enable:
- **Audience targeting** — e.g. "Logitech users", "non-Logitech users", "hardware owners vs. non-owners"
- **Incrementality measurement** — holdouts / A/B testing to prove impact on units sold
- **Performance packages** for endemic peripheral/hardware brands beyond standard display or generic sponsorship

### Problem It Solves

Endemic brands (Lenovo, Logitech, etc.) value the esports audience but primarily buy for performance outcomes (product consideration → sales). Today FACEIT can only offer standard ads (reach/traffic) or Mission sponsorships (engagement) — no ability to target the right users or prove incremental sales impact. This caps budgets and leaves use cases unmet.

### Discovery — How Hardware Data Is Collected

Three options were evaluated:

| Option | Assessment |
|--------|------------|
| User agent | Insufficient — limited and inconsistent data |
| Anti-cheat | Uses limited data for legitimate interests (preventing cheating). Adding advertising data layer risks credibility of the anti-cheat tool. Not viable. |
| FACEIT Client | Best option. May require user-initiated scan (similar to Steam Hardware Survey model). |

Reference: [Steam Hardware Survey](https://store.steampowered.com/hwsurvey/) as precedent for user-consented hardware scanning.

### Current Status

- **Not yet started** from PM side — PRD in discovery phase (`docs/product_briefs/Peripherals Initiatives.md`)
- Egor has a working build
- **Planning to release Monday at 1%** — data collection phase, not yet monetised
- 4 data point types collected so far: CPU, keyboard, mouse, device manufacturer

### Example Data Collected

```json
CPU: { manufacturer: '13th gen intel(r) core(tm) i5-1345u', cores: 12, speedMax: 2496 }
Keyboard: [{ deviceName: 'keyboard', manufacturer: '' }, { deviceName: 'keyboard', manufacturer: 'logitech' }]
Mouse: [{ deviceName: 'mouse', manufacturer: 'microsoft' }, { deviceName: 'mouse', manufacturer: 'logitech' }]
Device: { manufacturer: 'dell inc.' }
```

### Monetisation Direction

Two angles:
1. **Advertising targeting** — hardware-based audience segments sold to peripheral brands (Logitech is already a Brand Takeover client via Adam Goh — natural expansion)
2. **Profile/display** — users can show off their setup (same mechanic as Skin Vault)

### Privacy Considerations

- Privacy implications are **more complex than Skin Vault** — this is hardware data passively collected from a user's machine via the client, not public data from a third-party API
- User-initiated scan model (like Steam) may be required for consent
- Anti-cheat data must remain strictly separate — mixing ad targeting signals risks credibility of the anti-cheat product
- A **privacy risk assessment will almost certainly be required** before scaling beyond 1%
- Privacy contact: Fabia (acting lead), Gina (CLO)
- No privacy review has been initiated yet

### Open Questions

- What data points will be collected at 1% rollout and what does the distribution look like?
- What is the minimum dataset needed to validate targeting value for peripheral brands?
- What is the privacy review scope — GDPR, data minimisation, consent model?
- Is the user-facing "show your setup" concept in scope or just backend targeting?
- Does Logitech (existing client) have interest in hardware-targeted segments on top of Brand Takeover?
