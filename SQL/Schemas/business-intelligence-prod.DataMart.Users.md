# Users (DataMart)

**Table**: `business-intelligence-prod.DataMart.Users`
**Grain**: One row per user

| Column | Type | Description |
|--------|------|-------------|
| user_id | STRING | Primary key, UUID |
| created_at | TIMESTAMP | Account creation time |
| nickname | STRING | User's display name |
| first_name | STRING | User's first name |
| last_name | STRING | User's last name |
| email | STRING | Current email address |
| email_verified | BOOLEAN | Whether email is verified |
| email_history[] | REPEATED RECORD | Historical emails used by the account |
| faceit_points | INTEGER | User's FACEIT points balance |
| phone | STRING | Phone number |
| phone_verified | BOOLEAN | Whether phone is verified |
| country_iso_code | STRING | ISO country code |
| tags[] | REPEATED STRING | User tags |
| roles[] | REPEATED STRING | User roles |
| faceit_profile_verified | BOOLEAN | **WARNING: UNRELIABLE** (See below) |
| active_subscriptions[] | REPEATED RECORD | Current active subscriptions |
| logins[] | REPEATED RECORD | **WARNING: LIMITED** (See below) |
| geolocations[] | REPEATED RECORD | **WARNING: LIMITED** (See below) |
| last_match_finished_at | TIMESTAMP | Most recent match completion time |
| matches_finished[] | REPEATED RECORD | Summary of matches and elo per game |
| games[] | REPEATED RECORD | Detailed game registration info (incl. region, elo) |
| platforms[] | REPEATED RECORD | Connected platform accounts (Steam, etc) |

## Business Logic & Gotchas

### IP Address Limitation
- **CRITICAL**: The `logins.ip_address` and `geolocations.ip_address` fields within this table only store the **11 most recent** IP addresses for the user.
- **Action**: For a comprehensive IP history or variety analysis, do NOT use this table. Instead, use `business-intelligence-prod.IPHistoryService.Users`.

### Verification Status
- **CRITICAL**: The `faceit_profile_verified` field in this table is **not reliable** for determining current ID verification status.
- **Action**: Always join to `business-intelligence-prod.dbt_user.fact__user_verifications` and check for the most recent status of `PASSED`.

### ELO & Match Counts
- The `matches_finished` array provides a convenient summary of lifetime matches and current ELO per game, avoiding the need to UNNEST the massive Matches table for basic stats.
- For detailed game data including regions and skill levels, use the `games` array.


**Table**: `business-intelligence-prod.DataMart.Users`
**Grain**: One row per user

## Key Columns & Records

| Column | Type | Description |
|--------|------|-------------|
| user_id | STRING | Primary key, UUID |
| created_at | TIMESTAMP | Account creation time |
| logins[] | REPEATED RECORD | Contains `ip_address` and `timestamp` |
| geolocations[] | REPEATED RECORD | Contains `country_code`, `ip_address`, and `timestamp` |
| matches_finished[] | REPEATED RECORD | Summary of matches and elo per game |

## Business Logic & Gotchas

### IP Address Limitation
- **CRITICAL**: The `logins.ip_address` and `geolocations.ip_address` fields within this table only store the **11 most recent** IP addresses for the user.
- **Action**: For a comprehensive IP history or variety analysis, do NOT use this table. Instead, use `business-intelligence-prod.IPHistoryService.Users`.

### Verification Status
- **CRITICAL**: The `faceit_profile_verified` field in this table is **not reliable** for determining current ID verification status.
- **Action**: Always join to `business-intelligence-prod.dbt_user.fact__user_verifications` and check for the most recent status of `PASSED`.

### ELO & Match Counts
- The `matches_finished` array provides a convenient summary of lifetime matches and current ELO per game, avoiding the need to UNNEST the massive Matches table for basic stats.
