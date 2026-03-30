# CS2 Ingame Player Stats

**Table**: `business-intelligence-prod.dbt_user.dim__cs_ingame_player_stats`
**Partition Key**: `started_at` (TIMESTAMP, partitioned by DAY) _(learned 2026-03-12)_
**Grain**: One row per user per match (per match_round)

## Key Columns

| Column | Type | Description |
|--------|------|-------------|
| primary_key | INTEGER | Surrogate key |
| match_id | STRING | Foreign key to DataMart.Matches |
| user_id | STRING | Foreign key to DataMart.Users |
| match_type | STRING | e.g. 'championship' |
| game | STRING | e.g. 'cs2' |
| match_round | INTEGER | Round within a multi-round match |
| ingame_rounds | INTEGER | Number of in-game rounds played |
| started_at | TIMESTAMP | Match start time (**partition key**) |
| finished_at | TIMESTAMP | Match end time |
| team | STRING | Team identifier |
| steam_id_32 | STRING | Player's Steam ID (32-bit) |
| steam_id_64 | STRING | Player's Steam ID (64-bit) |
| name | STRING | Player display name |

## Combat Stats (Totals)

| Column | Type | Description |
|--------|------|-------------|
| total_kills | INTEGER | Total kills in the match |
| total_assists | INTEGER | Total assists |
| total_deaths | INTEGER | Total deaths |
| total_damage | INTEGER | Total damage dealt |
| total_headshot_kills | INTEGER | Headshot kills |
| total_objectives | INTEGER | Objective completions |
| kills | INTEGER | Kills (may differ from total_kills — unclear) |
| assists | INTEGER | Assists (may differ from total_assists — unclear) |
| deaths | INTEGER | Deaths (may differ from total_deaths — unclear) |
| score | INTEGER | Match score |
| mvps | INTEGER | MVP awards |
| rounds_won | INTEGER | Rounds won |

## Detailed Combat Stats

| Column | Type | Description |
|--------|------|-------------|
| enemy_kills | INTEGER | Kills on enemies |
| enemy_kills_ag | INTEGER | Enemy kills (aggregate?) |
| enemy_damage_dealt | INTEGER | Damage dealt to enemies |
| enemy_headshots | INTEGER | Headshots on enemies |
| enemy_1_kills | INTEGER | 1K rounds |
| enemy_2_kills | INTEGER | 2K rounds |
| enemy_3_kills | INTEGER | 3K rounds |
| enemy_4_kills | INTEGER | 4K rounds |
| enemy_5_kills | INTEGER | Ace rounds |
| clutch_kills | INTEGER | Kills in clutch situations |
| rounds_first_kills | INTEGER | First kill in a round |
| kills_pistol | INTEGER | Kills with pistols |
| kills_sniper | INTEGER | Kills with snipers |

## Economy Stats

| Column | Type | Description |
|--------|------|-------------|
| cash | INTEGER | Cash held |
| total_cash_earned | INTEGER | Lifetime cash earned in match |
| total_equipment_value | INTEGER | Total equipment purchased |
| total_kill_rewards | INTEGER | Cash earned from kills |
| helmet | INTEGER | Helmet purchases (?) |

## Utility Stats

| Column | Type | Description |
|--------|------|-------------|
| total_flashes | INTEGER | Flash grenades thrown |
| total_flash_successes | INTEGER | Successful flashes |
| total_enemies_flashed | INTEGER | Enemies flashed |
| total_utility_count | INTEGER | Total utility used |
| total_utility_damage | INTEGER | Damage from utility |
| total_utility_enemies | INTEGER | Enemies hit by utility |
| total_utility_successes | INTEGER | Successful utility uses |

## Engagement Stats

| Column | Type | Description |
|--------|------|-------------|
| total_entries | INTEGER | Entry attempts |
| total_entry_wins | INTEGER | Successful entries |
| total_live_time | INTEGER | Time alive (seconds?) |
| total_1v1s | INTEGER | 1v1 situations |
| total_1v1_wins | INTEGER | 1v1 wins |
| total_1v2s | INTEGER | 1v2 situations |
| total_1v2_wins | INTEGER | 1v2 wins |

## Per-Round Ratios

| Column | Type | Description |
|--------|------|-------------|
| kills_per_round | FLOAT | |
| enemy_kills_per_round | FLOAT | |
| deaths_per_round | FLOAT | |
| assists_per_round | FLOAT | |
| score_per_round | FLOAT | |
| damage_dealt_per_round | FLOAT | |
| clutch_kills_per_round | FLOAT | |
| headshots_per_round | FLOAT | |
| pistol_kills_per_round | FLOAT | |
| sniper_kills_per_round | FLOAT | |
| objectives_per_round | FLOAT | |
| cash_earned_per_round | FLOAT | |
| kill_rewards_per_round | FLOAT | |
| enemies_flashed_per_round | FLOAT | |
| utility_damage_per_round | FLOAT | |
| equipment_value_per_round | FLOAT | |
| flash_count_per_round | FLOAT | |
| utility_successes_per_round | FLOAT | |
| utility_count_per_round | FLOAT | |

## Derived Ratios

| Column | Type | Description |
|--------|------|-------------|
| round_survival_ratio | FLOAT | |
| kill_death_ratio | FLOAT | |
| mvp_percentage | FLOAT | |
| headshots_to_kills_ratio | FLOAT | |
| enemies_flashed_per_flash_hit | FLOAT | |
| first_kill_percentage | FLOAT | |
| enemy_2_kills_percentage | FLOAT | |
| enemy_3_kills_percentage | FLOAT | |
| enemy_4_kills_percentage | FLOAT | |
| enemy_5_kills_percentage | FLOAT | |
| round_win_percentage | FLOAT | |

## Query Optimization

**CRITICAL**: Table is partitioned by DAY on `started_at`.
- Always filter on `started_at` with literal dates for partition pruning
- Example: `WHERE started_at >= TIMESTAMP('2026-03-01')` enables partition pruning

## Joins

- `match_id` -> `DataMart.Matches.match_id`
- `user_id` -> `DataMart.Users.user_id`

## Usage in Idle Tournament Prize Farming Detection

Used to build a performance heuristic for AFK detection:
- `total_kills = 0 AND total_assists = 0 AND total_damage < (ingame_rounds * 10)` indicates a player was likely AFK/idle during the match _(learned 2026-03-12)_
