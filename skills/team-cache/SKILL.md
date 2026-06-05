---
name: team-cache
description: Audit and tune caching strategy for cost, latency, and consistency. Use when the user invokes /team-cache or asks for Team Cache team workflow guidance.
---

# Team Cache

Audit and tune caching strategy for cost, latency, and consistency.

## Target: the user-provided target or request
Options: cache layer name | "all"

## Workflow Phases

### Phase 1: Inventory (Parallel)
- **Cache Invalidation Coordinator**: Hit/miss rates per layer, key distribution
- **Code Optimization Specialist**: Cache-key generation paths across call sites

### Phase 2: Invariant Check (Sequential)
- **Cache Invalidation Coordinator**: Verify cache-key consistency:
  > All call sites producing the same logical request MUST generate identical cache keys.

### Phase 3: Tune (Sequential)
- **Code Optimization Specialist**: Adjust TTLs, eviction policies, key composition

## Generic Cache Invariants (NEVER VIOLATE)

- **Identical inputs produce identical keys** across every call site — the #1 source of cache bugs is two paths that should hit but don't
- **Keys exclude session/runtime noise** (user identity, timestamp, request ID) unless the value is actually user-specific
- **Mutable upstream data is read fresh, not cached as if immutable** — cache the *result*, not the *source* it's derived from
- **Invalidation has a clear trigger** — never rely on TTL alone for correctness-critical data
- **Stale-while-revalidate is opt-in**, not the default
- **Cache misses must not stampede** — single-flight or request coalescing for expensive misses

## Hit-Rate Targets (Sensible Defaults)

- Hot path (repeated reads): > 90%
- Warm path: > 70%
- Cold/long-tail: > 40%

## Output Format

```
## Cache Audit Report

### Hit Rates (Last 7 Days)
| Layer | Hit % | Miss Cost (avg) |
|-------|-------|-----------------|

### Key Generation Verification
- Call sites checked: [list]
- Key mismatches found: [N] — [details]

### Distribution
- Keys at max age / eviction: [N]
- Hot keys (top decile): [N]

### Recommendations
1. [tuning suggestion]
```
