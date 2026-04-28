# Play Interstitial — Video Creative Specifications (Desktop)

**Product**: FACEIT Play Interstitial (Pre-Match Skippable Video)
**Platform**: Desktop web only (PC gaming audience)
**Ad Server**: Google Ad Manager (GAM)
**Protocol**: VAST 4.2

---

## Placement Overview

| Parameter | Spec |
|:--|:--|
| **Trigger** | User clicks "Find Match" → full-screen video overlay before matchmaking begins |
| **Display** | Full-screen interstitial overlay (desktop browser) |
| **Sound** | Sound-on by default (user-initiated action) |
| **Skip** | Skippable after 5 seconds (1 free skip/day per user) |
| **Viewability** | 95%+ (full-screen, user-initiated, cannot interact behind overlay) |
| **Frequency** | 1 ad pod per match |
| **Eligible users** | Free users only (subscribers are ad-free) |

---

## Video Creative Requirements

### Format & Encoding

| Parameter | Requirement | Notes |
|:--|:--|:--|
| **File format** | H.264 / MP4 (required) | WebM accepted as secondary; MP4 must always be included |
| **Audio codec** | AAC or MP3 | AAC preferred |
| **VAST version** | 4.2 | Linear video; VAST redirect supported |
| **SSL** | Required | All assets and tracking URLs must be HTTPS |

### Resolution & Aspect Ratio

| Parameter | Requirement | Notes |
|:--|:--|:--|
| **Aspect ratio** | 16:9 | Standard desktop widescreen; no letterboxing or pillarboxing |
| **Recommended resolution** | 1920×1080 (1080p) | Full HD — matches typical desktop display |
| **Minimum resolution** | 1280×720 (720p) | Below 720p will appear low-quality on desktop |
| **Frame rate** | Up to 30 fps | 24fps or 25fps also accepted |

### File Size & Bitrate

| Parameter | Requirement | Notes |
|:--|:--|:--|
| **Max file size** | 10 MB per creative | GAM hard limit |
| **Recommended bitrate** | 2,000–3,500 kbps | For 1080p desktop delivery |
| **Minimum bitrate** | 1,000 kbps | Must include at least one mediafile ≤1,000 kbps per GAM requirements |
| **Multi-bitrate** | Recommended | Provide 3 files: low (~700 kbps / 360p), medium (~1,500 kbps / 720p), high (~3,000 kbps / 1080p) — per IAB VAST 4.2 best practice |

### Duration

| Parameter | Requirement | Notes |
|:--|:--|:--|
| **Recommended length** | 15 seconds | Industry standard; highest completion rates |
| **Accepted range** | 6–30 seconds per creative | Shorter creatives = higher VCR |
| **Unskippable window** | First 5 seconds | User can skip after 5s; first 5s are guaranteed |
| **Max ad pod** | 60 seconds total | Multiple creatives can fill a pod sequentially |

---

## Click-Through & Companion

| Parameter | Requirement | Notes |
|:--|:--|:--|
| **Click-through URL** | Required | Must open in new tab (`target="_blank"`) |
| **CTA overlay** | Optional | Rendered by VAST `<CompanionAds>` or custom UI; appears after skip timer |
| **Companion banner** | Not supported at launch | May be added in future phases |

---

## Tracking & Measurement

| Event | Supported |
|:--|:--|
| Impression | ✅ |
| Start (0%) | ✅ |
| First Quartile (25%) | ✅ |
| Midpoint (50%) | ✅ |
| Third Quartile (75%) | ✅ |
| Complete (100%) | ✅ |
| Skip | ✅ |
| Click-through | ✅ |
| Error | ✅ |
| Mute / Unmute | ✅ |

**Verification**: IAS and DoubleVerify compatible for brand safety and viewability measurement.

**Required VAST macros**:
- `[CACHEBUSTING]`
- `[TIMESTAMP]`
- `[CONTENTPLAYHEAD]`

---

## Submission Checklist

- [ ] MP4 (H.264) file included — mandatory
- [ ] 1080p resolution (1920×1080), 16:9 aspect ratio
- [ ] File size ≤ 10 MB
- [ ] At least one mediafile ≤ 1,000 kbps included
- [ ] Audio track present (AAC preferred)
- [ ] All URLs HTTPS (SSL-compliant)
- [ ] Click-through URL set with `target="_blank"`
- [ ] VAST 4.2 tag validated (use [Google VAST Inspector](https://googleads.github.io/googleads-ima-html5/vsi/))
- [ ] Duration: 6–30 seconds

---

## Quick Reference Card (for agencies)

```
Format:       MP4 (H.264) — required
Resolution:   1920×1080 (min 1280×720)
Aspect Ratio: 16:9
Max File Size: 10 MB
Bitrate:      2,000–3,500 kbps (include one ≤1,000 kbps)
Duration:     15s recommended (6–30s accepted)
Audio:        AAC, sound-on by default
Skip:         After 5 seconds
Protocol:     VAST 4.2, SSL required
Click:        Opens new tab
```

---

*Sources: Google Ad Manager / Authorized Buyers specifications, IAB VAST 4.2 Digital Video Ad Format Guidelines, Google Ads VAST requirements. All specs aligned to desktop web delivery.*
