-- Q3: Top motherboard/OEM brands by country (top 12 per country)
WITH base AS (
  SELECT
    session.country,
    device.manufacturer AS raw_mobo
  FROM `faceit-events-prod-2.user.client_hardware_details_v2` AS hw
  LEFT JOIN UNNEST([hw.device]) AS device
  LEFT JOIN UNNEST(hw.bluetooth_and_usb_devices) AS bt_usb
  LEFT JOIN `faceit-events-prod-2.user.new_tracking_session_v1` AS session
    ON hw.tracking_session_id = session.tracking_session_id
  WHERE hw.event_timestamp >= '2026-03-12'
    AND hw.event_timestamp < '2026-04-23'
    AND session.country IN ('IT','TR','IN','AL','AM','AR','AZ','BA','BD','BG','BH','BN','BO','BR','BY','CL','CN','CO','CR','DO','DZ','EC','EG','GE','GG','GH','GL','GT','GU','HK','HN','ID','IL','IM','IQ','JE','JM','KG','KH','KW','KY','KZ','LA','LB','LK','LU','LY','MA','MC','MD','ME','MK','MM','MN','MO','MQ','MT','MU','MX','MY','MZ','NC','NG','NI','NP','OM','PA','PE','PF','PH','PK','PR','PS','PY','QA','SV','SY','TH','TJ','TM','TN','TW','TZ','UA','UY','UZ','VE','VN','XK','ZA','ZM')
    AND device.manufacturer IS NOT NULL
    AND TRIM(device.manufacturer) != ''
),
normalized AS (
  SELECT
    country,
    CASE
      WHEN LOWER(raw_mobo) IN ('system manufacturer', 'to be filled by o.e.m.', 'default string', 'system product name') THEN 'Sys Mfg/OEM'
      WHEN LOWER(raw_mobo) LIKE '%asus%' THEN 'ASUS'
      WHEN LOWER(raw_mobo) = 'msi' OR LOWER(raw_mobo) LIKE 'micro-star%' THEN 'MSI'
      WHEN LOWER(raw_mobo) LIKE '%gigabyte%' THEN 'Gigabyte'
      WHEN LOWER(raw_mobo) IN ('monster notebook', 'monster') OR LOWER(raw_mobo) LIKE '%monster%' THEN 'Monster (TR)'
      WHEN LOWER(raw_mobo) LIKE '%casper%' THEN 'Casper (TR)'
      WHEN LOWER(raw_mobo) LIKE 'lenovo%' THEN 'Lenovo'
      WHEN LOWER(raw_mobo) LIKE 'hp%' OR LOWER(raw_mobo) = 'hewlett-packard' THEN 'HP'
      WHEN LOWER(raw_mobo) LIKE 'acer%' THEN 'Acer'
      WHEN LOWER(raw_mobo) LIKE 'dell%' THEN 'Dell'
      WHEN LOWER(raw_mobo) LIKE 'asrock%' THEN 'ASRock'
      WHEN LOWER(raw_mobo) LIKE '%game garaj%' THEN 'Game Garaj (TR)'
      WHEN LOWER(raw_mobo) LIKE 'huawei%' THEN 'Huawei'
      WHEN LOWER(raw_mobo) LIKE 'samsung%' THEN 'Samsung'
      WHEN LOWER(raw_mobo) LIKE 'apple%' THEN 'Apple'
      ELSE INITCAP(TRIM(raw_mobo))
    END AS mobo
  FROM base
),
counted AS (
  SELECT country, mobo, COUNT(*) AS cnt
  FROM normalized
  GROUP BY country, mobo
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY country ORDER BY cnt DESC) AS rn
  FROM counted
)
SELECT country, mobo, cnt
FROM ranked
WHERE rn <= 12
ORDER BY country, cnt DESC
