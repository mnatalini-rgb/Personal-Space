# fact__claimed_tournament_rewards

**Table**: `business-intelligence-prod.dbt_user.fact__claimed_tournament_rewards`
**Grain**: One row per user per tournament per reward type
**Partition**: Unknown — `event_date` (DATE) is the likely candidate but unconfirmed.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| primary_key | INTEGER | Surrogate key |
| event_date | DATE | Date the reward was recorded |
| tournament_id | STRING | Tournament ID. Joins to `DataMart.Tournaments.id` and `DataMart.Matches.entity_id` |
| user_id | STRING | User who received the reward. Joins to `DataMart.Users.user_id` |
| rank | INTEGER | User's finishing placement in the tournament |
| reward_type | STRING | Type of reward. Known value: `'points'` |
| faceit_points_awarded | FLOAT | FACEIT Points recorded for this placement |
| faceit_points_claimed | FLOAT | FACEIT Points actually claimed by the user |
| cash_prize | FLOAT | Cash prize amount (if applicable) |
| custom_prize_awarded | STRING | Custom/physical prize description (if applicable) |
| expected_price | FLOAT | Expected monetary value of the prize |

## ⚠️ Critical Gotcha: `faceit_points_awarded` is the placement-level prize, NOT the per-user payout

`faceit_points_awarded` appears to record the **total prize pool amount for that placement tier**, not the actual FP credited to the individual user. In team tournaments, this value is **not divided by team size**.

For example, if 1st place wins 5,000 FP and has 5 players, each player's row shows `faceit_points_awarded = 5000` — but the actual payout per player is 1,000 FP.

**Evidence** _(learned 2026-03-12)_: A month-by-month comparison against `TransactionsService.TransactionHistory` (the source of truth for actual FP credits) shows `faceit_points_awarded` consistently overstates actual FP by a factor of ~1.7x across all months (Feb 2025 – Feb 2026). The ratio is stable, consistent with average team sizes of ~5 players where not all are in the rewards table. See `sql/queries/2026-03-12_rewards_vs_transactions_comparison.sql`.

**If you need actual FP paid out**, use `TransactionsService.TransactionHistory` filtered to `currency = 'faceit_points'` and `entity.type = 'user'`.

## Joins

- `tournament_id` → `DataMart.Tournaments.id` (many:1)
- `tournament_id` → `DataMart.Matches.entity_id` (many:many, via tournament)
- `user_id` → `DataMart.Users.user_id` (many:1)

## Notes

- `faceit_points_claimed` may differ from `faceit_points_awarded` if a user hasn't claimed their reward yet, though the relationship between these two columns and the actual transaction amount is unclear.
- The comparison query is at: `sql/queries/2026-03-12_rewards_vs_transactions_comparison.sql`
- Results: `results/raw/2026-03-12_rewards_vs_transactions_comparison.csv`
