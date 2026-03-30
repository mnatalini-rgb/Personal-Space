# Dashboard Automation — Google Apps Script Setup

## Overview

One Google Sheet + one Apps Script project auto-refreshes **all 3 dashboards** (NSM, Peripherals, Skin Vault) from BigQuery daily. Dashboards fetch fresh data from the Apps Script Web App endpoint.

**No service account needed** — runs under your `m.natalini@efg.gg` credentials.

---

## Architecture

```
BigQuery ──► Apps Script (daily trigger) ──► Google Sheet (data store)
                  │
                  ▼
            Web App endpoint (doGet)
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   NSM HTML   Periph HTML  Skin Vault HTML
  (fetch JSON) (fetch JSON) (fetch JSON)
```

---

## Step-by-Step Setup

### 1. Create the Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it: **"FACEIT Dashboard Automation"**

### 2. Add the Apps Script

1. In the Sheet: **Extensions → Apps Script**
2. Delete any existing code in `Code.gs`
3. Paste the entire contents of `scripts/apps-script/Code.gs`
4. **Save** (Ctrl+S)

### 3. Enable BigQuery Advanced Service

1. In Apps Script editor: click **Services** (+ icon on left sidebar)
2. Search for **BigQuery API**
3. Click **Add**
4. This enables `BigQuery.Jobs.query()` — runs under your Google account

### 4. Deploy as Web App

1. Click **Deploy → New deployment**
2. Click the gear icon → Select **Web app**
3. Configure:
   - **Description**: "Dashboard Data API v1"
   - **Execute as**: **Me** (m.natalini@efg.gg)
   - **Who has access**: **Anyone** (so GitHub Pages can fetch it)
4. Click **Deploy**
5. **Copy the Web App URL** — it looks like:
   ```
   https://script.google.com/macros/s/AKfycbx.../exec
   ```
6. Save this URL — you'll paste it into each dashboard HTML.

### 5. Set Up Daily Trigger

1. In Apps Script editor: click **Triggers** (clock icon on left)
2. Click **+ Add Trigger**
3. Configure:
   - **Function**: `refreshAll`
   - **Event source**: Time-driven
   - **Type**: Day timer
   - **Time of day**: 6am to 7am
4. Click **Save**
5. Authorize when prompted (grant BigQuery + Sheets access)

### 6. Test It

1. In the Apps Script editor, select `refreshAll` from the function dropdown
2. Click **Run**
3. Check execution log (View → Execution log) for errors
4. Verify the Sheet now has tabs: `NSM_Data`, `Peripheral_Data`, `SkinVault_Data`, `Refresh_Log`
5. Test the Web App endpoint in your browser:
   ```
   https://script.google.com/macros/s/AKfycbx.../exec?dashboard=status
   ```

### 7. Update Dashboard HTML Files

Each dashboard needs a small JS snippet to fetch data from the endpoint. See the code changes below.

---

## Dashboard Code Changes

### For ALL dashboards — add this fetch helper at the top of the `<script>` section:

```javascript
// === AUTO-REFRESH FROM APPS SCRIPT ===
const DASHBOARD_API = 'YOUR_APPS_SCRIPT_WEB_APP_URL_HERE';

async function fetchDashboardData(dashboardName) {
  try {
    const resp = await fetch(DASHBOARD_API + '?dashboard=' + dashboardName);
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    return await resp.json();
  } catch (err) {
    console.warn('Auto-refresh failed, using embedded data:', err);
    return null; // Falls back to hardcoded data
  }
}
```

### NSM Dashboard
Add at the top of the script section, before `processData()`:
```javascript
// Try to load fresh data from API, fall back to embedded BQ_DATA
(async function() {
  const fresh = await fetchDashboardData('nsm');
  if (fresh && fresh.nsm) {
    // Replace BQ_DATA with fresh API data
    Object.assign(BQ_DATA, fresh.nsm);
    BQ_DATA.buildTimestamp = fresh.buildTimestamp;
    processData(); // Re-process with fresh data
  }
})();
```

### Peripherals Dashboard
Replace the hardcoded `datasets` object init with:
```javascript
// Try to load fresh data from API
(async function() {
  const fresh = await fetchDashboardData('peripherals');
  if (fresh && fresh.peripherals && fresh.peripherals.datasets) {
    const d = fresh.peripherals.datasets;
    if (d.in) Object.assign(inData, d.in);
    if (d.tr) Object.assign(trData, d.tr);
    if (d.it) Object.assign(itData, d.it);
    if (d.all) Object.assign(allData, d.all);
    renderDashboard(allData); // Re-render with fresh data
  }
})();
```

### Skin Vault Dashboard
Similar pattern — fetch and update chart data arrays.

---

## API Reference

| Endpoint | Returns |
|----------|---------|
| `?dashboard=nsm` | NSM data (ebuYtd, weeklyEbu, missions, rewards) |
| `?dashboard=peripherals` | Peripheral data (all countries + combined) |
| `?dashboard=skinvault` | Skin Vault data (views, interactions, feedback) |
| `?dashboard=all` | Everything |
| `?dashboard=status` | Last refresh timestamps per dashboard |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "BigQuery is not defined" | Enable BigQuery Advanced Service (Step 3) |
| "Exceeded maximum execution time" | Split `refreshAll` into individual refreshes scheduled 10 min apart |
| "Permission denied on BQ" | Ensure your Google account has BQ read access to both projects |
| CORS error on dashboard | Redeploy Web App with "Anyone" access; dashboards must use the `/exec` URL |
| Stale data | Check Refresh_Log tab; re-run `refreshAll` manually from Apps Script editor |

---

## Updating DAU Values

DAU comes from the product brief, not BQ. To update:
1. Open Apps Script editor
2. Find `CONFIG.PERIPHERAL_DAU` at the top
3. Update the numbers
4. Save and re-run `refreshPeripheralsOnly()`

---

## Updating Partners

When a new partner is added:
1. Open Apps Script editor
2. Add the org ID to `CONFIG.PARTNERS`
3. Update the `partnerCaseWhen` in `refreshNSM_()`
4. Save and re-run `refreshNSMOnly()`

---

## Costs

- **Apps Script**: Free (6-minute execution limit per run; ~2-3 min for all 3 dashboards)
- **BigQuery**: Queries scan existing tables — cost depends on data volume. NSM queries scan ~MB. Peripheral queries can be heavier due to JOINs — the pre-filter pattern keeps it efficient.
- **Google Sheets**: Free

---

## Migration Path

When you get a GCP service account:
1. Switch to **GitHub Actions** (workflow YAML already designed)
2. Use `google-github-actions/auth@v3` with Workload Identity Federation
3. The BQ queries in this script can be reused directly in the shell/Python scripts
