# Matches (DataMart)

**Table**: `business-intelligence-prod.DataMart.Matches`
**Partition Key**: `created_at` (TIMESTAMP) _(learned 2026-02-23)_
**Grain**: One row per match

## Key Columns

| Column | Type | Description |
|--------|------|-------------|
| match_id | STRING | Primary key |
| created_at | TIMESTAMP | Match creation time |
| updated_at | TIMESTAMP | |
| started_at | TIMESTAMP | |
| finished_at | TIMESTAMP | |
| organizer_id | STRING | |
| match_type | STRING | |
| entity_id | STRING | |
| entity_name | STRING | |
| game | STRING | Game identifier; CS2 uses 'cs2' _(learned 2026-02-23)_ |
| region | STRING | |
| device | STRING | |
| game_label | STRING | |
| state | STRING | |
| states | REPEATED STRING | |
| calculate_elo | BOOLEAN | |
| winner | STRING | |
| cancellation_reason | STRING | |
| no_checkins | REPEATED STRING | |
| no_votes | REPEATED STRING | |
| no_captain_picks | REPEATED STRING | |
| manual_overrides | REPEATED STRING | |
| afks | REPEATED STRING | |
| leavers | REPEATED STRING | |
| queue_id | STRING | |
| manual_result | BOOLEAN | |
| rounds | INTEGER | |
| community_server_id | STRING | |
| demos | REPEATED STRING | |
| duration | INTEGER | Seconds |
| source | STRING | |

## Nested Structure: Captain Picks

```
captain_picks (RECORD)
├── total_picks (INTEGER)
├── ended_at (TIMESTAMP)
└── pick_order[] (REPEATED)
    ├── faction (STRING)
    ├── user_id (STRING)
    ├── faction_order (INTEGER)
    └── match_order (INTEGER)
```

## Nested Structure: Teams & Players

```
teams[] (REPEATED)
├── faction (STRING)
├── team_id (STRING)
├── team_name (STRING)
├── win_probability (FLOAT)
├── team_type (STRING)
├── community_id (STRING)
├── size (INTEGER)
├── composition (STRING)
├── elo_avg (FLOAT)
├── elo_stddev (FLOAT)
├── elo_min (INTEGER)
├── elo_max (INTEGER)
├── elo_matches_avg (FLOAT)
├── elo_matches_min (INTEGER)
├── elo_matches_max (INTEGER)
├── elo_matches_sum (INTEGER)
├── matches_avg (FLOAT)
├── matches_min (INTEGER)
├── matches_max (INTEGER)
├── matches_sum (INTEGER)
├── parties[] (REPEATED)
│   ├── party_id (STRING)
│   ├── size (INTEGER)
│   ├── memberships (STRING)
│   ├── queue_duration (FLOAT)
│   ├── elo_avg (FLOAT)
│   ├── elo_stddev (FLOAT)
│   ├── elo_min (INTEGER)
│   ├── elo_max (INTEGER)
│   ├── elo_matches_avg (FLOAT)
│   ├── elo_matches_min (INTEGER)
│   ├── elo_matches_max (INTEGER)
│   ├── elo_matches_sum (INTEGER)
│   ├── matches_avg (FLOAT)
│   ├── matches_min (INTEGER)
│   ├── matches_max (INTEGER)
│   ├── matches_sum (INTEGER)
│   └── users[] (REPEATED)
│       ├── user_id (STRING)
│       ├── elo (INTEGER)
│       ├── memberships[] (REPEATED STRING)
│       └── elo_matches (INTEGER)
```

**To count unique players**: UNNEST teams → parties → users, then COUNT(DISTINCT user_id)

## Nested Structure: Results

```
results[] (REPEATED)
├── round (INTEGER)
├── duration_secs (INTEGER)
├── first_half_score_faction1 (INTEGER)
├── first_half_score_faction2 (INTEGER)
├── second_half_score_faction1 (INTEGER)
├── second_half_score_faction2 (INTEGER)
├── score_faction1 (INTEGER)
├── score_faction2 (INTEGER)
└── winner (STRING)
```

## Nested Structure: User Match Tags

```
user_match_tags[] (REPEATED)
├── user_id (STRING)
├── round (INTEGER)
├── match_state (STRING)
├── timestamp (TIMESTAMP)
├── tag (STRING)
└── source (STRING)
```

| Column | Type | Description |
|--------|------|-------------|
| match_id | STRING | Primary key |
| created_at | TIMESTAMP | Match creation time |
| updated_at | TIMESTAMP | |
| started_at | TIMESTAMP | |
| finished_at | TIMESTAMP | |
| organizer_id | STRING | |
| match_type | STRING | |
| entity_id | STRING | |
| entity_name | STRING | |
| game | STRING | Game identifier; CS2 uses 'cs2' _(learned 2026-02-23)_ |
| region | STRING | |
| device | STRING | |
| game_label | STRING | |
| state | STRING | |
| states | REPEATED STRING | |
| calculate_elo | BOOLEAN | |
| winner | STRING | |
| cancellation_reason | STRING | |
| no_checkins | REPEATED STRING | |
| no_votes | REPEATED STRING | |
| no_captain_picks | REPEATED STRING | |
| afks | REPEATED STRING | |
| leavers | REPEATED STRING | |
| queue_id | STRING | |
| duration | INTEGER | Seconds |
| source | STRING | |

## Nested Structure: Teams & Players

```
teams[] (REPEATED)
├── faction (STRING)
├── team_id (STRING)
├── team_name (STRING)
├── team_type (STRING)
├── elo_avg (FLOAT)
├── parties[] (REPEATED)
│   ├── party_id (STRING)
│   └── users[] (REPEATED)
│       ├── user_id (STRING)
│       ├── elo (INTEGER)
│       ├── memberships[] (REPEATED STRING)
│       └── elo_matches (INTEGER)
```

**To count unique players**: UNNEST teams → parties → users, then COUNT(DISTINCT user_id)

## Nested Structure: Results

```
results[] (REPEATED)
├── round (INTEGER)
├── duration_secs (INTEGER)
├── score_faction1 (INTEGER)
├── score_faction2 (INTEGER)
└── winner (STRING)
```

## Nested Structure: User Match Tags

```
user_match_tags[] (REPEATED)
├── user_id (STRING)
├── round (INTEGER)
├── match_state (STRING)
├── timestamp (TIMESTAMP)
└── tag (STRING)
```

## Business Context

- Matches are created when initiated; finished_at is populated when completed
- Each match can have multiple teams (e.g., faction1, faction2)
- Each team contains parties (squads); each party contains individual players
- Players within a match have elo ratings and membership affiliations

## Query Optimization

**CRITICAL**: Table is partitioned on `created_at`, NOT `finished_at`.
- Always filter on `created_at` with literal dates in the outer WHERE clause for partition pruning
- This enables **partition pruning** before UNNEST, reducing full-table scans from 126GB → 3-5GB
- Example: `WHERE created_at >= TIMESTAMP('2026-02-15')` enables partition pruning before UNNEST

**Row Multiplication Risk**: When unnesting all three levels (teams → parties → users), each row expands by the Cartesian product of nested arrays. Example: 1 match with 2 teams × 3 parties × 5 users = 30 output rows.

## Gotchas

- `finished_at` can be NULL for unfinished/cancelled matches — filter carefully
- `created_at` and `finished_at` are usually close but not identical; use `created_at` for partition pruning
- Player IDs appear across multiple matches (same player plays many games); use COUNT(DISTINCT user_id) for weekly unique player counts
