---
name: team-database
description: DB review, query optimization, and migration support. Use when the user invokes /team-database or asks for Team Database team workflow guidance.
---

# Team Database

DB review, query optimization, and migration support.

## Target: the user-provided target or request
Options: "schema" | "queries" | "migration" | "indexes"

## Workflow Phases

### Phase 1: Audit (Parallel)
- **Database Administrator**: Schema review, index coverage, query plans
- **Database Migration**: Migration safety (locking, backfill, rollback)

### Phase 2: Optimize (Sequential)
- **Database Administrator**: Apply index / query fixes

### Phase 3: Migration (Sequential, if applicable)
- **Database Migration**: Author + dry-run migration with rollback plan

## Generic Database Principles

- **Targeted queries with filters** — never scan whole tables or collections in application code
- **Indexes for filter columns** — verify with explain/profile, not assumption
- **N+1 query detection** — batch or join; avoid per-row queries in loops
- **Migrations are reversible** by default; irreversible changes need extra review
- **Long migrations run online** with chunking/throttling, not in a single transaction
- **Backfill data separately from schema change** when both are needed
- **Foreign keys / constraints enforced** at the DB level, not just application code

## Migration Safety Checklist

- [ ] Migration tested against production-sized data
- [ ] Lock duration measured and acceptable
- [ ] Backfill plan documented
- [ ] Rollback steps tested
- [ ] Monitoring / alerts in place during rollout
- [ ] Downstream consumers notified of schema change

## Output Format

```
## Database Report

### Slow Queries
| Query | Source | Latency | Fix |
|-------|--------|---------|-----|

### Index Recommendations
- [collection/table] — [fields] — [why]

### Migration Plan (if any)
- Step 1: [op] — [risk]
- Rollback: [steps]
```
