/**
 * FACEIT Dashboard Data Automation
 * ================================
 * Unified Apps Script that queries BigQuery daily and serves JSON to all 3 dashboards:
 *   - NSM (Brand Integrations)
 *   - Peripherals (Hardware Data)
 *   - Skin Vault (Experiment)
 *
 * Runs under: m.natalini@efg.gg (no service account needed)
 * Deployed as: Web App (doGet returns JSON)
 * Trigger: Daily time-driven (6-7 AM UTC)
 *
 * Setup:
 *   1. Create new Google Sheet → Extensions → Apps Script
 *   2. Paste this file as Code.gs
 *   3. Enable BigQuery Advanced Service: Services → + → BigQuery API
 *   4. Deploy → Web App → Execute as "Me", Access "Anyone with link"
 *   5. Add trigger: Triggers → + → refreshAll → Time-driven → Day timer → 6-7am
 *   6. Copy the Web App URL and set it in each dashboard HTML
 */

// ══════════════════════════════════════════════
// CONFIGURATION
// ══════════════════════════════════════════════

const CONFIG = {
  // BQ Projects
  NSM_PROJECT: 'business-intelligence-prod',
  EVENTS_PROJECT: 'faceit-events-prod-2',

  // Partner Org IDs
  PARTNERS: {
    TRADEIT: '976fe92b-0998-4a2a-86a6-f655bbab8f07',
    WINLINE: '397f5239-ab93-484d-9f94-4231b0cfa48e',
    WINLINE_BY: 'a8f12da7-d377-4b9f-aedf-a33cb1283b20',
    WINLINE_KZ: 'b5efeb75-4f23-494e-bc85-9319c1a87c75',
    WHITEMARKET: 'db18537b-4172-4813-b089-36490c1553b7'
  },

  // Peripheral countries
  PERIPHERAL_COUNTRIES: ['IN', 'TR', 'IT'],

  // DAU values (from product brief — not BQ tracking DAU)
  PERIPHERAL_DAU: { IN: 3349, TR: 80537, IT: 5002 },

  // Gaming brands list for penetration calc
  GAMING_BRANDS: [
    'razer', 'logitech', 'steelseries', 'corsair', 'hyperx',
    'asus', 'asustek', 'msi', 'roccat', 'glorious',
    'ducky', 'endgame gear', 'zowie', 'finalmouse', 'pulsar'
  ],

  // Sheet tab names
  SHEETS: {
    NSM: 'NSM_Data',
    PERIPHERALS: 'Peripheral_Data',
    SKIN_VAULT: 'SkinVault_Data',
    LOG: 'Refresh_Log'
  }
};

// ══════════════════════════════════════════════
// WEB APP ENDPOINT (doGet)
// ══════════════════════════════════════════════

/**
 * Serves JSON data to dashboards.
 * Usage:
 *   ?dashboard=nsm          → NSM data
 *   ?dashboard=peripherals  → Peripheral data
 *   ?dashboard=skinvault    → Skin Vault data
 *   ?dashboard=all          → Everything
 *   ?dashboard=status       → Last refresh timestamps
 */
function doGet(e) {
  const dashboard = (e && e.parameter && e.parameter.dashboard) || 'all';
  let data = {};

  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();

    if (dashboard === 'status') {
      data = getRefreshStatus_(ss);
    } else if (dashboard === 'nsm' || dashboard === 'all') {
      data.nsm = readSheetAsJson_(ss, CONFIG.SHEETS.NSM);
    }
    if (dashboard === 'peripherals' || dashboard === 'all') {
      data.peripherals = readSheetAsJson_(ss, CONFIG.SHEETS.PERIPHERALS);
    }
    if (dashboard === 'skinvault' || dashboard === 'all') {
      data.skinvault = readSheetAsJson_(ss, CONFIG.SHEETS.SKIN_VAULT);
    }

    data.buildTimestamp = new Date().toISOString();

    return ContentService
      .createTextOutput(JSON.stringify(data))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ error: err.message, timestamp: new Date().toISOString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ══════════════════════════════════════════════
// MASTER REFRESH (triggered daily)
// ══════════════════════════════════════════════

function refreshAll() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const log = [];

  log.push('=== Dashboard Refresh Started: ' + new Date().toISOString() + ' ===');

  try {
    log.push('Refreshing NSM...');
    refreshNSM_(ss);
    log.push('  ✓ NSM done');
  } catch (err) {
    log.push('  ✗ NSM failed: ' + err.message);
  }

  try {
    log.push('Refreshing Peripherals...');
    refreshPeripherals_(ss);
    log.push('  ✓ Peripherals done');
  } catch (err) {
    log.push('  ✗ Peripherals failed: ' + err.message);
  }

  try {
    log.push('Refreshing Skin Vault...');
    refreshSkinVault_(ss);
    log.push('  ✓ Skin Vault done');
  } catch (err) {
    log.push('  ✗ Skin Vault failed: ' + err.message);
  }

  log.push('=== Refresh Complete: ' + new Date().toISOString() + ' ===');

  // Write log
  writeLog_(ss, log);
}

// ══════════════════════════════════════════════
// NSM REFRESH
// ══════════════════════════════════════════════

function refreshNSM_(ss) {
  const project = CONFIG.NSM_PROJECT;
  const partnerIds = Object.values(CONFIG.PARTNERS);
  const partnerIdList = partnerIds.map(id => '"' + id + '"').join(', ');

  const partnerCaseWhen = `
    CASE
      WHEN organizer.id = "${CONFIG.PARTNERS.TRADEIT}" THEN "Tradeit"
      WHEN organizer.id = "${CONFIG.PARTNERS.WINLINE}" THEN "Winline"
      WHEN organizer.id = "${CONFIG.PARTNERS.WINLINE_BY}" THEN "Winline_BY"
      WHEN organizer.id = "${CONFIG.PARTNERS.WINLINE_KZ}" THEN "Winline_KZ"
      WHEN organizer.id = "${CONFIG.PARTNERS.WHITEMARKET}" THEN "WhiteMarket"
    END`;

  // Q1: EBU per partner YTD
  const ebuYtd = runBQ_(project, `
    WITH partner_campaigns AS (
      SELECT _id as campaign_id, ${partnerCaseWhen} as partner
      FROM \`business-intelligence-prod.CampaignService.Campaigns\`
      WHERE organizer.id IN (${partnerIdList})
        AND schedule.start_date >= "2026-01-01"
    ),
    per_partner AS (
      SELECT pc.partner, COUNT(DISTINCT um.user_id) as ebu
      FROM \`business-intelligence-prod.CampaignService.UserMissions\` um
      JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
      GROUP BY pc.partner
    ),
    winline_all AS (
      SELECT "Winline_All" as partner, COUNT(DISTINCT um.user_id) as ebu
      FROM \`business-intelligence-prod.CampaignService.UserMissions\` um
      JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
      WHERE pc.partner IN ("Winline", "Winline_BY", "Winline_KZ")
    ),
    total AS (
      SELECT "Portfolio" as partner, COUNT(DISTINCT um.user_id) as ebu
      FROM \`business-intelligence-prod.CampaignService.UserMissions\` um
      JOIN (SELECT campaign_id FROM partner_campaigns) pc ON um.campaign_id = pc.campaign_id
    )
    SELECT * FROM per_partner
    UNION ALL SELECT * FROM winline_all
    UNION ALL SELECT * FROM total
    ORDER BY ebu DESC
  `);

  // Q2: Weekly EBU per partner
  const weeklyEbuByPartner = runBQ_(project, `
    WITH partner_campaigns AS (
      SELECT _id as campaign_id, ${partnerCaseWhen} as partner
      FROM \`business-intelligence-prod.CampaignService.Campaigns\`
      WHERE organizer.id IN (${partnerIdList})
        AND schedule.start_date >= "2026-01-01"
    )
    SELECT
      FORMAT_DATE("%Y-%m-%d", DATE_TRUNC(DATE(um.created_at), WEEK(MONDAY))) as week_start,
      pc.partner,
      COUNT(DISTINCT um.user_id) as weekly_ebu
    FROM \`business-intelligence-prod.CampaignService.UserMissions\` um
    JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
    WHERE um.created_at >= "2026-01-01"
    GROUP BY week_start, pc.partner
    ORDER BY week_start, pc.partner
  `);

  // Q3: Weekly deduplicated total EBU
  const weeklyEbuDedup = runBQ_(project, `
    WITH partner_campaigns AS (
      SELECT _id as campaign_id
      FROM \`business-intelligence-prod.CampaignService.Campaigns\`
      WHERE organizer.id IN (${partnerIdList})
        AND schedule.start_date >= "2026-01-01"
    )
    SELECT
      FORMAT_DATE("%Y-%m-%d", DATE_TRUNC(DATE(um.created_at), WEEK(MONDAY))) as week_start,
      COUNT(DISTINCT um.user_id) as weekly_ebu_dedup
    FROM \`business-intelligence-prod.CampaignService.UserMissions\` um
    JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
    WHERE um.created_at >= "2026-01-01"
    GROUP BY week_start
    ORDER BY week_start
  `);

  // Q4: Mission completions by challenge per partner per month
  const missionCompletions = runBQ_(project, `
    WITH partner_campaigns AS (
      SELECT _id as campaign_id, technical_name, ${partnerCaseWhen} as partner
      FROM \`business-intelligence-prod.CampaignService.Campaigns\`
      WHERE organizer.id IN (${partnerIdList})
        AND schedule.start_date >= "2026-01-01"
    )
    SELECT
      pc.partner,
      pc.technical_name as campaign_technical_name,
      FORMAT_DATE("%Y-%m", DATE(um.updated_at)) as month,
      um.name as challenge_name,
      COUNT(*) as completions,
      COUNT(DISTINCT um.user_id) as unique_users
    FROM \`business-intelligence-prod.CampaignService.UserMissions\` um
    JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
    WHERE um.status = "complete"
    GROUP BY pc.partner, pc.technical_name, month, challenge_name
    ORDER BY pc.partner, month, completions DESC
  `);

  // Q5: Weekly mission completions
  const weeklyMissionCompletions = runBQ_(project, `
    WITH partner_campaigns AS (
      SELECT _id as campaign_id, technical_name, ${partnerCaseWhen} as partner
      FROM \`business-intelligence-prod.CampaignService.Campaigns\`
      WHERE organizer.id IN (${partnerIdList})
        AND schedule.start_date >= "2026-01-01"
    )
    SELECT
      FORMAT_DATE("%Y-%m-%d", DATE_TRUNC(DATE(um.updated_at), WEEK(MONDAY))) as week_start,
      pc.partner,
      um.name as challenge_name,
      COUNT(*) as completions,
      COUNT(DISTINCT um.user_id) as unique_users
    FROM \`business-intelligence-prod.CampaignService.UserMissions\` um
    JOIN partner_campaigns pc ON um.campaign_id = pc.campaign_id
    WHERE um.status = "complete"
      AND um.updated_at >= "2026-01-01"
    GROUP BY week_start, pc.partner, challenge_name
    ORDER BY week_start, pc.partner, completions DESC
  `);

  // Q6: Reward claims
  const rewardClaims = runBQ_(project, `
    WITH partner_campaigns AS (
      SELECT _id as campaign_id, technical_name, ${partnerCaseWhen} as partner
      FROM \`business-intelligence-prod.CampaignService.Campaigns\`
      WHERE organizer.id IN (${partnerIdList})
        AND schedule.start_date >= "2026-01-01"
    )
    SELECT
      pc.partner,
      pc.technical_name as campaign_technical_name,
      FORMAT_DATE("%Y-%m", DATE(ur.created_at)) as month,
      ur.status as reward_status,
      COUNT(*) as cnt,
      COUNT(DISTINCT ur.user_id) as unique_users
    FROM \`business-intelligence-prod.CampaignService.UserRewards\` ur
    JOIN partner_campaigns pc ON ur.campaign_id = pc.campaign_id
    GROUP BY pc.partner, pc.technical_name, month, reward_status
    ORDER BY pc.partner, month, cnt DESC
  `);

  // Assemble and write
  const nsmData = {
    ebuYtd: ebuYtd,
    weeklyEbuByPartner: weeklyEbuByPartner,
    weeklyEbuDedup: weeklyEbuDedup,
    missionCompletions: missionCompletions,
    weeklyMissionCompletions: weeklyMissionCompletions,
    rewardClaims: rewardClaims,
    refreshTimestamp: new Date().toISOString()
  };

  writeJsonToSheet_(ss, CONFIG.SHEETS.NSM, nsmData);
}

// ══════════════════════════════════════════════
// PERIPHERALS REFRESH
// ══════════════════════════════════════════════

function refreshPeripherals_(ss) {
  const project = CONFIG.EVENTS_PROJECT;
  const countries = CONFIG.PERIPHERAL_COUNTRIES;
  const result = {};

  for (const country of countries) {
    result[country.toLowerCase()] = queryPeripheralCountry_(project, country);
  }

  // Compute "all" aggregate
  result.all = aggregatePeripheralData_(result);

  // Add DAU (manual, from product brief)
  for (const country of countries) {
    result[country.toLowerCase()].dau = CONFIG.PERIPHERAL_DAU[country] || 0;
  }
  result.all.dau = Object.values(CONFIG.PERIPHERAL_DAU).reduce((a, b) => a + b, 0);

  const peripheralData = {
    datasets: result,
    refreshTimestamp: new Date().toISOString()
  };

  writeJsonToSheet_(ss, CONFIG.SHEETS.PERIPHERALS, peripheralData);
}

function queryPeripheralCountry_(project, country) {
  // Uses the efficient pre-filter + INNER JOIN pattern to avoid timeouts

  // Q1: Summary stats
  const summary = runBQ_(project, `
    WITH session_country AS (
      SELECT DISTINCT tracking_session_id
      FROM \`faceit-events-prod-2.user.new_tracking_session_v1\`
      WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 60 DAY)
        AND country = "${country}"
    ),
    hw AS (
      SELECT h.tracking_session_id, h.cpu.name as cpu_name,
             h.device.manufacturer as device_mfr, h.device.name as device_name,
             h.cpu.cores as cpu_cores
      FROM \`faceit-events-prod-2.user.client_hardware_details_v2\` h,
           UNNEST(h.bluetooth_and_usb_devices) AS device
      WHERE h.event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    )
    SELECT
      COUNT(*) as totalRows,
      COUNT(DISTINCT hw.tracking_session_id) as uniqueSystems,
      ROUND(100.0 * SUM(CASE WHEN REGEXP_CONTAINS(LOWER(hw.cpu_name), r'amd|ryzen') THEN 1 ELSE 0 END) / COUNT(*), 1) as cpuAmd,
      ROUND(100.0 * SUM(CASE WHEN REGEXP_CONTAINS(LOWER(hw.cpu_name), r'intel') THEN 1 ELSE 0 END) / COUNT(*), 1) as cpuIntel,
      ROUND(100.0 * SUM(CASE WHEN LOWER(hw.device_name) = 'keyboard' THEN 1 ELSE 0 END) / COUNT(*), 1) as keyboardPct,
      ROUND(100.0 * SUM(CASE WHEN LOWER(hw.device_name) = 'mouse' THEN 1 ELSE 0 END) / COUNT(*), 1) as mousePct
    FROM hw
    INNER JOIN session_country sc ON hw.tracking_session_id = sc.tracking_session_id
  `);

  // Q2: Gaming penetration
  const gamingBrandsList = CONFIG.GAMING_BRANDS.map(b => '"' + b + '"').join(', ');
  const gaming = runBQ_(project, `
    WITH session_country AS (
      SELECT DISTINCT tracking_session_id
      FROM \`faceit-events-prod-2.user.new_tracking_session_v1\`
      WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 60 DAY)
        AND country = "${country}"
    ),
    hw AS (
      SELECT h.tracking_session_id, device.manufacturer as mfr
      FROM \`faceit-events-prod-2.user.client_hardware_details_v2\` h,
           UNNEST(h.bluetooth_and_usb_devices) AS device
      WHERE h.event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    )
    SELECT
      ROUND(100.0 * SUM(CASE WHEN LOWER(hw.mfr) IN (${gamingBrandsList}) THEN 1 ELSE 0 END) / COUNT(*), 1) as gamingPenetration
    FROM hw
    INNER JOIN session_country sc ON hw.tracking_session_id = sc.tracking_session_id
  `);

  // Q3: Top peripheral brands
  const topPeripherals = runBQ_(project, `
    WITH session_country AS (
      SELECT DISTINCT tracking_session_id
      FROM \`faceit-events-prod-2.user.new_tracking_session_v1\`
      WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 60 DAY)
        AND country = "${country}"
    ),
    hw AS (
      SELECT h.tracking_session_id,
             CASE
               WHEN TRIM(device.manufacturer) = '' OR device.manufacturer IS NULL THEN '(Empty/Generic)'
               WHEN REGEXP_CONTAINS(LOWER(device.manufacturer), r'standart sistem|standard system') THEN 'Standard System'
               WHEN REGEXP_CONTAINS(LOWER(device.manufacturer), r'steelseries|arctis pro|steel series') THEN 'SteelSeries'
               WHEN REGEXP_CONTAINS(LOWER(device.manufacturer), r'asustek|asus') THEN 'ASUS'
               ELSE INITCAP(TRIM(device.manufacturer))
             END as brand
      FROM \`faceit-events-prod-2.user.client_hardware_details_v2\` h,
           UNNEST(h.bluetooth_and_usb_devices) AS device
      WHERE h.event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    )
    SELECT brand as name, COUNT(*) as count
    FROM hw
    INNER JOIN session_country sc ON hw.tracking_session_id = sc.tracking_session_id
    GROUP BY brand
    ORDER BY count DESC
    LIMIT 10
  `);

  // Q4: Top motherboard / OEM
  const topMobo = runBQ_(project, `
    WITH session_country AS (
      SELECT DISTINCT tracking_session_id
      FROM \`faceit-events-prod-2.user.new_tracking_session_v1\`
      WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 60 DAY)
        AND country = "${country}"
    ),
    hw AS (
      SELECT h.tracking_session_id,
             CASE
               WHEN TRIM(h.device.manufacturer) = '' OR h.device.manufacturer IS NULL THEN '(Empty/Generic)'
               WHEN REGEXP_CONTAINS(LOWER(h.device.manufacturer), r'asustek|asus') THEN 'ASUS'
               WHEN REGEXP_CONTAINS(LOWER(h.device.manufacturer), r'micro-star|micro star') THEN 'MSI'
               WHEN REGEXP_CONTAINS(LOWER(h.device.manufacturer), r'system manufacturer|to be filled') THEN 'Sys Mfg'
               WHEN REGEXP_CONTAINS(LOWER(h.device.manufacturer), r'monster') THEN 'Monster (TR)'
               WHEN REGEXP_CONTAINS(LOWER(h.device.manufacturer), r'casper') THEN 'Casper (TR)'
               ELSE INITCAP(TRIM(h.device.manufacturer))
             END as brand
      FROM \`faceit-events-prod-2.user.client_hardware_details_v2\` h
      WHERE h.event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    )
    SELECT brand as name, COUNT(*) as count
    FROM hw
    INNER JOIN session_country sc ON hw.tracking_session_id = sc.tracking_session_id
    GROUP BY brand
    ORDER BY count DESC
    LIMIT 10
  `);

  // Q5: CPU core counts
  const coreCounts = runBQ_(project, `
    WITH session_country AS (
      SELECT DISTINCT tracking_session_id
      FROM \`faceit-events-prod-2.user.new_tracking_session_v1\`
      WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 60 DAY)
        AND country = "${country}"
    ),
    hw AS (
      SELECT h.tracking_session_id, h.cpu.cores as cores
      FROM \`faceit-events-prod-2.user.client_hardware_details_v2\` h
      WHERE h.event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
        AND h.cpu.cores IS NOT NULL AND h.cpu.cores > 0
    )
    SELECT CONCAT(CAST(hw.cores AS STRING), ' Cores') as cores, COUNT(*) as count
    FROM hw
    INNER JOIN session_country sc ON hw.tracking_session_id = sc.tracking_session_id
    GROUP BY hw.cores
    ORDER BY count DESC
    LIMIT 8
  `);

  const s = (summary && summary.length > 0) ? summary[0] : {};
  const g = (gaming && gaming.length > 0) ? gaming[0] : {};

  return {
    totalRows: Number(s.totalRows) || 0,
    uniqueSystems: Number(s.uniqueSystems) || 0,
    cpuAmd: Number(s.cpuAmd) || 0,
    cpuIntel: Number(s.cpuIntel) || 0,
    keyboardPct: Number(s.keyboardPct) || 0,
    mousePct: Number(s.mousePct) || 0,
    gamingPenetration: Number(g.gamingPenetration) || 0,
    topPeripherals: (topPeripherals || []).map(r => ({ name: r.name, count: Number(r.count) })),
    topMobo: (topMobo || []).map(r => ({ name: r.name, count: Number(r.count) })),
    coreCounts: (coreCounts || []).map(r => ({ cores: r.cores, count: Number(r.count) }))
  };
}

function aggregatePeripheralData_(countryData) {
  const countries = Object.keys(countryData);
  const all = {
    totalRows: 0, uniqueSystems: 0,
    cpuAmd: 0, cpuIntel: 0,
    keyboardPct: 0, mousePct: 0,
    gamingPenetration: 0,
    topPeripherals: [],
    topMobo: [],
    coreCounts: []
  };

  // Sum totals
  for (const c of countries) {
    all.totalRows += countryData[c].totalRows;
    all.uniqueSystems += countryData[c].uniqueSystems;
  }

  // Weighted averages for percentages (weighted by totalRows)
  let totalWeight = 0;
  for (const c of countries) {
    const w = countryData[c].totalRows;
    totalWeight += w;
    all.cpuAmd += countryData[c].cpuAmd * w;
    all.cpuIntel += countryData[c].cpuIntel * w;
    all.keyboardPct += countryData[c].keyboardPct * w;
    all.mousePct += countryData[c].mousePct * w;
    all.gamingPenetration += countryData[c].gamingPenetration * w;
  }
  if (totalWeight > 0) {
    all.cpuAmd = Math.round(all.cpuAmd / totalWeight * 10) / 10;
    all.cpuIntel = Math.round(all.cpuIntel / totalWeight * 10) / 10;
    all.keyboardPct = Math.round(all.keyboardPct / totalWeight * 10) / 10;
    all.mousePct = Math.round(all.mousePct / totalWeight * 10) / 10;
    all.gamingPenetration = Math.round(all.gamingPenetration / totalWeight * 10) / 10;
  }

  // Merge top lists (sum counts across countries, re-sort, take top 10)
  all.topPeripherals = mergeTopLists_(countries.map(c => countryData[c].topPeripherals), 'name', 10);
  all.topMobo = mergeTopLists_(countries.map(c => countryData[c].topMobo), 'name', 10);
  all.coreCounts = mergeTopLists_(countries.map(c => countryData[c].coreCounts), 'cores', 8);

  return all;
}

function mergeTopLists_(lists, keyField, limit) {
  const merged = {};
  for (const list of lists) {
    for (const item of list) {
      const key = item[keyField];
      if (!merged[key]) merged[key] = { count: 0 };
      merged[key][keyField] = key;
      merged[key].count += item.count;
    }
  }
  return Object.values(merged)
    .sort((a, b) => b.count - a.count)
    .slice(0, limit);
}

// ══════════════════════════════════════════════
// SKIN VAULT REFRESH
// ══════════════════════════════════════════════

function refreshSkinVault_(ss) {
  const project = CONFIG.EVENTS_PROJECT;

  // Q1: Page views — top profiles + totals
  const pageViews = runBQ_(project, `
    SELECT
      page_view.url as url,
      COUNT(*) as total_events,
      COUNT(DISTINCT user_id) as unique_users
    FROM \`faceit-events-prod-2.user.page_view_v1\`
    WHERE page_view.url LIKE '%/skins%'
      AND event_timestamp >= TIMESTAMP("2026-03-17")
    GROUP BY url
    ORDER BY total_events DESC
  `);

  // Q2: Interactions by action + item type
  const interactions = runBQ_(project, `
    SELECT
      skin_vault_interaction.action as action,
      skin_vault_interaction.inventory_item_type as item_type,
      COUNT(DISTINCT user_id) as unique_users,
      COUNT(*) as total_events
    FROM \`faceit-events-prod-2.user.skin_vault_interaction_v1\`
    WHERE event_timestamp >= TIMESTAMP("2026-03-17")
    GROUP BY action, item_type
    ORDER BY unique_users DESC
  `);

  // Q3: Feedback
  const feedback = runBQ_(project, `
    SELECT
      feedback_collector.name as name,
      feedback_collector.feedback_type as feedback_type,
      feedback_collector.feedback_text as feedback_text
    FROM \`faceit-events-prod-2.user.feedback_collector_v1\`
    WHERE feedback_collector.name LIKE '%skin_vault%'
      AND event_timestamp >= TIMESTAMP("2026-03-17")
    ORDER BY event_timestamp DESC
  `);

  // Process page views
  let totalPageViews = 0;
  const profileViews = {};
  const localeViews = {};

  for (const row of (pageViews || [])) {
    const events = Number(row.total_events);
    totalPageViews += events;

    // Extract player slug and locale from URL
    const urlMatch = (row.url || '').match(/faceit\.com\/(\w+)\/players\/([^\/]+)/);
    if (urlMatch) {
      const locale = urlMatch[1];
      const player = urlMatch[2];
      profileViews[player] = (profileViews[player] || 0) + events;
      localeViews[locale] = (localeViews[locale] || 0) + events;
    }
  }

  const uniqueProfilesViewed = Object.keys(profileViews).length;
  const topProfiles = Object.entries(profileViews)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20)
    .map(([name, count]) => ({ name, count }));

  const localeBreakdown = Object.entries(localeViews)
    .sort((a, b) => b[1] - a[1])
    .map(([locale, count]) => ({ locale: locale.toUpperCase(), count }));

  // Process interactions
  const actionSummary = {};
  const itemTypeBreakdown = {};
  for (const row of (interactions || [])) {
    const action = row.action || 'unknown';
    const itemType = (row.item_type || '').replace('INVENTORY_ITEM_TYPE_', '') || 'none';
    const users = Number(row.unique_users);
    const events = Number(row.total_events);

    if (!actionSummary[action]) actionSummary[action] = { unique_users: 0, total_events: 0 };
    actionSummary[action].unique_users += users;
    actionSummary[action].total_events += events;

    if (itemType !== 'none') {
      if (!itemTypeBreakdown[itemType]) itemTypeBreakdown[itemType] = {};
      if (!itemTypeBreakdown[itemType][action]) itemTypeBreakdown[itemType][action] = 0;
      itemTypeBreakdown[itemType][action] += users;
    }
  }

  // Process feedback
  const sentimentCounts = {};
  const viewerBreakdown = {};
  const freeTextResponses = [];
  for (const row of (feedback || [])) {
    const type = row.feedback_type || 'unknown';
    sentimentCounts[type] = (sentimentCounts[type] || 0) + 1;

    const viewer = (row.name || '').includes('owner') ? 'owner' : 'visitor';
    viewerBreakdown[viewer] = (viewerBreakdown[viewer] || 0) + 1;

    if (row.feedback_text && row.feedback_text.trim()) {
      freeTextResponses.push({ viewer, sentiment: type, text: row.feedback_text });
    }
  }

  const skinVaultData = {
    kpis: {
      totalPageViews: totalPageViews,
      uniqueProfilesViewed: uniqueProfilesViewed,
      cohortSize: 300,
      uniqueTabClickers: actionSummary['tab_click'] ? actionSummary['tab_click'].unique_users : 0,
      feedbackSubmissions: (feedback || []).length
    },
    topProfiles: topProfiles,
    localeBreakdown: localeBreakdown,
    funnel: Object.entries(actionSummary).map(([action, data]) => ({
      action, unique_users: data.unique_users, total_events: data.total_events
    })).sort((a, b) => b.unique_users - a.unique_users),
    itemTypeBreakdown: itemTypeBreakdown,
    sentiment: sentimentCounts,
    viewerBreakdown: viewerBreakdown,
    freeTextResponses: freeTextResponses,
    refreshTimestamp: new Date().toISOString()
  };

  writeJsonToSheet_(ss, CONFIG.SHEETS.SKIN_VAULT, skinVaultData);
}

// ══════════════════════════════════════════════
// BIGQUERY HELPER
// ══════════════════════════════════════════════

function runBQ_(projectId, sql) {
  const request = {
    query: sql,
    useLegacySql: false,
    timeoutMs: 120000 // 2 min timeout
  };

  let queryResults = BigQuery.Jobs.query(request, projectId);

  // Handle pagination for large results
  const jobId = queryResults.jobReference.jobId;
  let rows = queryResults.rows || [];
  let pageToken = queryResults.pageToken;

  while (pageToken) {
    const page = BigQuery.Jobs.getQueryResults(projectId, jobId, { pageToken: pageToken });
    rows = rows.concat(page.rows || []);
    pageToken = page.pageToken;
  }

  // Convert BigQuery row format to plain objects
  const fields = queryResults.schema.fields;
  return rows.map(row => {
    const obj = {};
    for (let i = 0; i < fields.length; i++) {
      const val = row.f[i].v;
      obj[fields[i].name] = val;
    }
    return obj;
  });
}

// ══════════════════════════════════════════════
// SHEET I/O HELPERS
// ══════════════════════════════════════════════

function writeJsonToSheet_(ss, sheetName, data) {
  let sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }
  sheet.clear();
  // Store as single JSON string in A1, timestamp in B1
  sheet.getRange('A1').setValue(JSON.stringify(data));
  sheet.getRange('B1').setValue(new Date().toISOString());
}

function readSheetAsJson_(ss, sheetName) {
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return null;
  const raw = sheet.getRange('A1').getValue();
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch (e) {
    return null;
  }
}

function getRefreshStatus_(ss) {
  const status = {};
  const sheets = [CONFIG.SHEETS.NSM, CONFIG.SHEETS.PERIPHERALS, CONFIG.SHEETS.SKIN_VAULT];
  for (const name of sheets) {
    const sheet = ss.getSheetByName(name);
    if (sheet) {
      status[name] = sheet.getRange('B1').getValue() || 'never';
    } else {
      status[name] = 'not created';
    }
  }
  return status;
}

function writeLog_(ss, logLines) {
  let sheet = ss.getSheetByName(CONFIG.SHEETS.LOG);
  if (!sheet) {
    sheet = ss.insertSheet(CONFIG.SHEETS.LOG);
  }
  const lastRow = Math.max(sheet.getLastRow(), 0);
  for (let i = 0; i < logLines.length; i++) {
    sheet.getRange(lastRow + 1 + i, 1).setValue(logLines[i]);
  }
}

// ══════════════════════════════════════════════
// MANUAL TRIGGERS (for testing individual dashboards)
// ══════════════════════════════════════════════

function refreshNSMOnly() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  refreshNSM_(ss);
  SpreadsheetApp.getUi().alert('NSM refresh complete!');
}

function refreshPeripheralsOnly() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  refreshPeripherals_(ss);
  SpreadsheetApp.getUi().alert('Peripherals refresh complete!');
}

function refreshSkinVaultOnly() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  refreshSkinVault_(ss);
  SpreadsheetApp.getUi().alert('Skin Vault refresh complete!');
}
