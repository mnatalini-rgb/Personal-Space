# Bans

**Table**: `business-intelligence-prod.SheriffApi.Bans`
**Grain**: One row per ban
**Source system**: SheriffApi

## Business Context

 Primary use: checking whether a ban was removed (false positive detection)
 A ban is considered a **false positive** when `removedBy IS NOT NULL AND removedBy != 'service'`
 When a ban expires naturally, `removedBy` is set to `'service'`

## Schema

| Column | Type | Description |
|--------|------|-------------|
| _class | STRING | |
| _id | STRING | |
| createdAt | TIMESTAMP | |
| createdBy | STRING | |
| endsAt | TIMESTAMP | |
| expired | BOOLEAN | |
| game | STRING | |
| lastModified | TIMESTAMP | |
| nickname | STRING | |
| protectedBan | BOOLEAN | |
| reason | STRING | |
| reasonType | STRING | |
| removedBy | STRING | Who/what removed the ban. `'service'` = expired naturally. Other values = manually removed (false positive) |
| startsAt | TIMESTAMP | |
| type | STRING | |
| userId | STRING | |
| version | INTEGER | |
| game | STRING | Game identifier; may differ from Matches table _(learned 2026-02-23)_ |

## Common Queries

### False positive rate
```sql
SELECT
  COUNT(*) AS total_bans,
  COUNTIF(removedBy IS NOT NULL AND removedBy != 'service') AS false_positives,
  ROUND(COUNTIF(removedBy IS NOT NULL AND removedBy != 'service') / COUNT(*) * 100, 2) AS false_positive_pct
FROM `business-intelligence-prod.SheriffApi.Bans`
WHERE createdAt >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
```

## Open Questions

<!-- Fill these in as you learn more — helps me write better queries -->
- What are the possible values for `type`? (temp/permanent/other?)
- What are the possible values for `reasonType`?
- What does `_class` represent?
- Does `protectedBan = TRUE` mean it can't be removed?
- Is `createdBy` an admin user ID, a system name, or something else?
- What's the relationship between `endsAt` and `expired`? (Is `expired` computed, or set independently?)
