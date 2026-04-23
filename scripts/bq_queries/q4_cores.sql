-- Q4: Core count distribution by country (top 8 per country)
WITH base AS (
  SELECT
    session.country,
    cpu.cores
  FROM `faceit-events-prod-2.user.client_hardware_details_v2` AS hw
  LEFT JOIN UNNEST([hw.cpu]) AS cpu
  LEFT JOIN UNNEST(hw.bluetooth_and_usb_devices) AS bt_usb
  LEFT JOIN `faceit-events-prod-2.user.new_tracking_session_v1` AS session
    ON hw.tracking_session_id = session.tracking_session_id
  WHERE hw.event_timestamp >= '2026-03-12'
    AND hw.event_timestamp < '2026-04-23'
    AND session.country IN ('IT','TR','IN','AL','AM','AR','AZ','BA','BD','BG','BH','BN','BO','BR','BY','CL','CN','CO','CR','DO','DZ','EC','EG','GE','GG','GH','GL','GT','GU','HK','HN','ID','IL','IM','IQ','JE','JM','KG','KH','KW','KY','KZ','LA','LB','LK','LU','LY','MA','MC','MD','ME','MK','MM','MN','MO','MQ','MT','MU','MX','MY','MZ','NC','NG','NI','NP','OM','PA','PE','PF','PH','PK','PR','PS','PY','QA','SV','SY','TH','TJ','TM','TN','TW','TZ','UA','UY','UZ','VE','VN','XK','ZA','ZM')
    AND cpu.cores IS NOT NULL
    AND cpu.cores > 0
),
counted AS (
  SELECT
    country,
    CONCAT(CAST(cores AS STRING), ' Cores') AS core_label,
    COUNT(*) AS cnt
  FROM base
  GROUP BY country, cores
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY country ORDER BY cnt DESC) AS rn
  FROM counted
)
SELECT country, core_label, cnt
FROM ranked
WHERE rn <= 8
ORDER BY country, cnt DESC
