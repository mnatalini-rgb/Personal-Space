


### **Problem**

We work with many endemic peripherals/hardware brands (e.g., Logitech) that value the esports audience but primarily buy performance outcomes (product consideration → sales). Today we mostly offer standard ads (reach/traffic) or Mission sponsorships (engagement), which limits our ability to target the right users and prove impact on units sold, so budgets stay capped and use cases go unmet.

### **Background / Opportunity**

The FACEIT PC Client gives us access to privacy-compliant first-party signals (e.g., device/manufacturer attributes and client context). If we productize these signals, we can enable:

* **Audience targeting** (e.g., "Lenovo users", "non-Lenovo users", "hardware owners vs non-owners")  
* **Incrementality measurement** (holdouts / A/B)  
* **More compelling performance packages** beyond classic display or generic sponsorship

### **Discovery** 

It's not an easy task to collect these data as:

1. **User agent**: doesn't satisfy the solution (limited and inconsistent) [Atlassian](https://efgcloud.atlassian.net/wiki/spaces/AD/pages/5346656356/Hardware+components)  
2. **Anit-cheat**: the team uses limited amount of data for legitimate interests (users not to cheat) adding this layer of data might put in jeopardy the credibility of the tool  
3. **Client**: best option so far however, we might have to use a user initiate scan like Steam does it [https://store.steampowered.com/hwsurvey/Steam-Hardware-Software-Survey-Welcome-to-Steam](https://store.steampowered.com/hwsurvey/Steam-Hardware-Software-Survey-Welcome-to-Steam) 

[Lenovo Survey](https://docs.google.com/document/d/1PvsAAbytUnfBHrqkzN_zURzHDAVDtnW4PioJiTUTq0s/edit?tab=t.0#heading=h.aojmumek9s85)

[Atlassian](https://efgcloud.atlassian.net/wiki/spaces/AD/pages/3036413957/Hardware+Component+Installed+Game+targeting)

[Atlassian](https://efgcloud.atlassian.net/wiki/spaces/AD/pages/3481436372/Hardware+Games+Detection+Logic)

### **Rollout Strategy**

**Phase 1 — India (100% rollout)**
Launch the peripheral data collection to all FACEIT users in India. India serves as a low-risk, high-volume proving ground: large user base, minimal advertiser exposure, and limited contractual sensitivity if issues arise.

**Monitoring criteria before Phase 2:**
- **Data quality**: ≥ 90% of collected records return a non-empty manufacturer field for at least one device category (keyboard, mouse, or system).
- **Client stability**: No increase in client crash rate or ANR (Application Not Responding) events attributable to the hardware scan.
- **User sentiment**: No measurable uptick in support tickets or negative feedback related to data collection / privacy concerns.
- **Collection coverage**: ≥ 70% of active client users successfully return hardware data within the first 14 days.

**Minimum observation window**: 2 weeks of stable data before proceeding.

**Phase 2 — Turkey (TR) — 80,537 DAU** ✅ LIVE at 100%
Country confirmed 17 March 2026. Released 18 March 2026. **Now live at 100% — monitoring through Friday 21 March.**

**Why Turkey:**
- 80.5K DAU — 24x India's volume, large enough to validate at scale
- Low advertiser exposure — no active peripheral brand campaigns in TR
- No GDPR/LGPD — simpler regulatory posture than EU or Brazil
- Commercially relevant for endemic brands (Logitech, Razer) — unlike CIS alternatives (Kazakhstan, Uzbekistan)

**Early TR results (18 March 2026):**
- ~32,542 TR records collected (vs 2,853 from India)
- ~1,393 unique system configs captured (1.7% of DAU)
- CPU split: AMD 49.5% / Intel 50.5% (more balanced than India's 53/47)
- Gaming brand penetration: 25.0% (vs India's 33.3%)
- Strong SteelSeries presence: 9.3% combined (vs India's 1.8%)
- Turkish local OEM brands detected: Monster (4.9%), Casper (2.7%), Game Garaj (0.6%)

**Tracking optimisation (18 March 2026):** Egor identified ~3 tracking events per user per day — redundant for hardware that doesn't change. Changed to **1 collection per user per week**. First-session collection preserved for new country rollouts.

Same monitoring criteria apply before Tier 1 expansion.

**Phase 3 — Italy (IT) — 5,002 DAU** *(next)*
Selected 18 March 2026. First Tier 1 market — small enough (5K DAU) to be low-risk, but provides Tier 1 eCPM validation.

**Why Italy:**
- 5,002 DAU — genuinely small Tier 1, minimal risk if issues arise
- EU market — validates GDPR compliance posture before larger EU rollouts
- Tier 1 eCPMs — proves the commercial value of peripheral data in premium markets
- Commercially relevant for endemic brands (Logitech, Razer have strong EU presence)
- Gated on: Phase 2 TR stability confirmed + Legal/Privacy sign-off for EU data collection

**Phase 4 — Remaining Tier 1 markets** *(gated on Phase 3 results + Legal/Privacy sign-off)*
Expand to larger monetisation markets (UK, France, Germany, US, Canada, Australia) after proven stability in Italy, confirmed data quality, and updated privacy disclosures.

---

### **Data Points available (March '26)**

CPU info {  
  manufacturer: '13th gen intel(r) core(tm) i5-1345u',  
  cores: 12,  
  speedMax: 2496  
}  
HardwareService: Collected keyboard info \[  
  { deviceName: 'keyboard', manufacturer: '' },  
  { deviceName: 'keyboard', manufacturer: 'logitech' }  
\]  
HardwareService: Collected mouse info \[  
  { deviceName: 'mouse', manufacturer: 'microsoft' },  
  { deviceName: 'mouse', manufacturer: 'logitech' }  
\]  
HardwareService: Collected device info { manufacturer: 'dell inc.' }
