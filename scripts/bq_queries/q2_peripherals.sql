-- Q2: Top peripheral brands by country (top 15 per country for tier aggregation flexibility)
WITH base AS (
  SELECT
    session.country,
    bt_usb.manufacturer AS raw_brand
  FROM `faceit-events-prod-2.user.client_hardware_details_v2` AS hw
  LEFT JOIN UNNEST(hw.bluetooth_and_usb_devices) AS bt_usb
  LEFT JOIN `faceit-events-prod-2.user.new_tracking_session_v1` AS session
    ON hw.tracking_session_id = session.tracking_session_id
  WHERE hw.event_timestamp >= '2026-03-12'
    AND hw.event_timestamp < '2026-04-23'
    AND session.country IN ('IT','TR','IN','AL','AM','AR','AZ','BA','BD','BG','BH','BN','BO','BR','BY','CL','CN','CO','CR','DO','DZ','EC','EG','GE','GG','GH','GL','GT','GU','HK','HN','ID','IL','IM','IQ','JE','JM','KG','KH','KW','KY','KZ','LA','LB','LK','LU','LY','MA','MC','MD','ME','MK','MM','MN','MO','MQ','MT','MU','MX','MY','MZ','NC','NG','NI','NP','OM','PA','PE','PF','PH','PK','PR','PS','PY','QA','SV','SY','TH','TJ','TM','TN','TW','TZ','UA','UY','UZ','VE','VN','XK','ZA','ZM')
),
normalized AS (
  SELECT
    country,
    CASE
      WHEN raw_brand IS NULL OR TRIM(raw_brand) = '' THEN '(Empty/Generic)'
      WHEN LOWER(raw_brand) LIKE '%standard%system%' THEN 'Standard System'
      WHEN LOWER(raw_brand) IN ('(standart sistem aygıtları)', '(cihazlar standart sistem)') THEN 'Standard System'
      WHEN LOWER(raw_brand) IN ('(standard system devices)', '(périphériques système standard)') THEN 'Standard System'
      WHEN LOWER(raw_brand) LIKE '%steelseries%' OR LOWER(raw_brand) = 'aps' THEN 'SteelSeries'
      WHEN LOWER(raw_brand) LIKE '%logitech%' OR LOWER(raw_brand) = 'logi' THEN 'Logitech'
      WHEN LOWER(raw_brand) LIKE 'razer%' THEN 'Razer'
      WHEN LOWER(raw_brand) LIKE '%corsair%' THEN 'Corsair'
      WHEN LOWER(raw_brand) LIKE '%hyperx%' THEN 'HyperX'
      WHEN LOWER(raw_brand) = 'semico' THEN 'Semico'
      WHEN LOWER(raw_brand) = 'compx' THEN 'Compx'
      WHEN LOWER(raw_brand) = 'microsoft' THEN 'Microsoft'
      WHEN LOWER(raw_brand) = 'sonix' THEN 'Sonix'
      WHEN LOWER(raw_brand) = 'instant' THEN 'Instant'
      WHEN LOWER(raw_brand) LIKE '%redragon%' THEN 'Redragon'
      WHEN LOWER(raw_brand) LIKE '%bloody%' THEN 'Bloody'
      WHEN LOWER(raw_brand) LIKE '%a4tech%' THEN 'A4Tech'
      WHEN LOWER(raw_brand) = 'darmoshark' THEN 'Darmoshark'
      WHEN LOWER(raw_brand) = 'varmilo' THEN 'Varmilo'
      WHEN LOWER(raw_brand) LIKE '%sino wealth%' THEN 'Sino Wealth'
      WHEN LOWER(raw_brand) = 'by tech' THEN 'By Tech'
      WHEN LOWER(raw_brand) = 'evision' THEN 'Evision'
      ELSE INITCAP(TRIM(raw_brand))
    END AS brand
  FROM base
),
counted AS (
  SELECT country, brand, COUNT(*) AS cnt
  FROM normalized
  GROUP BY country, brand
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY country ORDER BY cnt DESC) AS rn
  FROM counted
)
SELECT country, brand, cnt
FROM ranked
WHERE rn <= 15
ORDER BY country, cnt DESC
