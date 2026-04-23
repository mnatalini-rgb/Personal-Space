-- Q1: Basic metrics by country
-- total_rows, unique_users, cpu counts, gaming count, device type counts
WITH base AS (
  SELECT
    hw.user_id,
    session.country,
    cpu.manufacturer AS cpu_mfr,
    bt_usb.manufacturer AS periph_mfr,
    LOWER(COALESCE(bt_usb.device_name, '')) AS device_name
  FROM `faceit-events-prod-2.user.client_hardware_details_v2` AS hw
  LEFT JOIN UNNEST([hw.cpu]) AS cpu
  LEFT JOIN UNNEST(hw.bluetooth_and_usb_devices) AS bt_usb
  LEFT JOIN `faceit-events-prod-2.user.new_tracking_session_v1` AS session
    ON hw.tracking_session_id = session.tracking_session_id
  WHERE hw.event_timestamp >= '2026-03-12'
    AND hw.event_timestamp < '2026-04-23'
    AND session.country IN ('IT','TR','IN','AL','AM','AR','AZ','BA','BD','BG','BH','BN','BO','BR','BY','CL','CN','CO','CR','DO','DZ','EC','EG','GE','GG','GH','GL','GT','GU','HK','HN','ID','IL','IM','IQ','JE','JM','KG','KH','KW','KY','KZ','LA','LB','LK','LU','LY','MA','MC','MD','ME','MK','MM','MN','MO','MQ','MT','MU','MX','MY','MZ','NC','NG','NI','NP','OM','PA','PE','PF','PH','PK','PR','PS','PY','QA','SV','SY','TH','TJ','TM','TN','TW','TZ','UA','UY','UZ','VE','VN','XK','ZA','ZM')
),
classified AS (
  SELECT
    country,
    user_id,
    -- CPU classification
    CASE
      WHEN LOWER(cpu_mfr) LIKE '%amd%' THEN 'AMD'
      WHEN LOWER(cpu_mfr) LIKE '%intel%' THEN 'Intel'
      ELSE 'Unknown'
    END AS cpu_brand,
    -- Gaming brand detection (substring match like Python script)
    CASE WHEN (
      LOWER(COALESCE(periph_mfr,'')) LIKE '%logitech%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%razer%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%steelseries%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%corsair%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%hyperx%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%roccat%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%glorious%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%zowie%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%benq%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%endgame gear%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%pulsar%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%lamzu%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%finalmouse%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%vaxee%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%ninjutso%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%ducky%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%wooting%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%cherry%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%xtrfy%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%mad catz%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%turtle beach%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%astro%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%asus%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%asustek%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%msi%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%cooler master%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%thermaltake%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%bloody%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%a4tech%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%redragon%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%fantech%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%varmilo%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%leopold%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%darmoshark%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%attack shark%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%keychron%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%akko%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%dragonborn%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%dareu%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%mountain%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%gwolves%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%lethal gaming gear%'
      OR LOWER(COALESCE(periph_mfr,'')) LIKE '%corepad%' OR LOWER(COALESCE(periph_mfr,'')) LIKE '%artisan%'
      OR LOWER(COALESCE(periph_mfr,'')) = 'logi'
    ) THEN 1 ELSE 0 END AS is_gaming,
    -- Device type
    CASE
      WHEN device_name LIKE '%keyboard%' THEN 'Keyboard'
      WHEN device_name LIKE '%mouse%' THEN 'Mouse'
      ELSE 'Other'
    END AS device_type
  FROM base
)
SELECT
  country,
  COUNT(*) AS total_rows,
  COUNT(DISTINCT user_id) AS unique_users,
  SUM(CASE WHEN cpu_brand = 'AMD' THEN 1 ELSE 0 END) AS cpu_amd,
  SUM(CASE WHEN cpu_brand = 'Intel' THEN 1 ELSE 0 END) AS cpu_intel,
  SUM(is_gaming) AS gaming_count,
  SUM(CASE WHEN device_type = 'Keyboard' THEN 1 ELSE 0 END) AS keyboard_count,
  SUM(CASE WHEN device_type = 'Mouse' THEN 1 ELSE 0 END) AS mouse_count,
  SUM(CASE WHEN device_type = 'Other' THEN 1 ELSE 0 END) AS other_count
FROM classified
GROUP BY country
ORDER BY total_rows DESC
