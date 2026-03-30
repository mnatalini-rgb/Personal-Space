SELECT
  COUNT(*)             AS total_account_operations,
  COUNT(DISTINCT guid) AS distinct_users

FROM
  `faceit-events-prod-2.user.account_operation_succeeded_v2`

WHERE
  DATE(event_timestamp) BETWEEN '2026-03-02' AND '2026-03-08'
;
