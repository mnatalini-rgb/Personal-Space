# BQ Schemas

Drop your table schemas and documentation here. For each table/dataset, create a file like:

```
schemas/
  users.md
  events.md
  subscriptions.md
```

## What to include in each schema file

1. **Table name** — full BQ path (e.g., `project.dataset.table`)
2. **Column definitions** — name, type, description
3. **Business context** — what this table represents, how it's populated, refresh cadence
4. **Key relationships** — how it joins to other tables (join keys, 1:many vs 1:1)
5. **Gotchas** — known quirks, null handling, timezone issues, deprecated columns

### Example format

```markdown
# users

**Table**: `myproject.core.users`
**Refresh**: Daily, ~2am UTC
**Grain**: One row per user

| Column | Type | Description |
|--------|------|-------------|
| user_id | STRING | Primary key, UUID |
| created_at | TIMESTAMP | Account creation time (UTC) |
| plan_type | STRING | Current plan: 'free', 'pro', 'enterprise' |
| is_active | BOOL | False if churned or deleted |

**Joins**: `user_id` → `events.user_id` (1:many)
**Gotchas**: `is_active` was added 2024-03; rows before that default to TRUE
```

The more context you add here, the better SQL I can write for you.