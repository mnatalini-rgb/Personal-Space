# IP History (Service)

**Table**: `business-intelligence-prod.IPHistoryService.Users`
**Grain**: One row per user, containing an array of historical geolocations and IPs.

| Column | Type | Description |
|--------|------|-------------|
| _id | STRING | Unique user identifier (UUID) |
| created_at | TIMESTAMP | Document creation time |
| geo_locations[] | REPEATED RECORD | Nested list of all recorded IP/Geo logins |
| geo_locations.created_at | TIMESTAMP | When this specific login was recorded |
| geo_locations.country_code | STRING | ISO country code for the login |
| geo_locations.ip_address | STRING | IP address used for the login |
| updated_at | TIMESTAMP | Last update time for the document |

## Business Logic
- **Comprehensive History**: Unlike `DataMart.Users`, which limits IPs to the 11 most recent, this table contains the full historical log in the `geo_locations` array.
- **Querying**: To count distinct IPs or countries, you MUST use `UNNEST(geo_locations)`.
- **Joins**: Join to other tables using `_id` (this maps to `user_id` in DataMart).

## Example Query
```sql
SELECT
    _id AS user_id,
    COUNT(DISTINCT g.ip_address) AS num_ips
FROM `business-intelligence-prod.IPHistoryService.Users`
CROSS JOIN UNNEST(geo_locations) AS g
GROUP BY 1
```
