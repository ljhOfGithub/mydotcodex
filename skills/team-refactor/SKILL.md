---
name: team-refactor
description: Execute a large-scale, multi-pass refactor with architecture safety nets. Use when the user invokes /team-refactor or asks for Team Refactor team workflow guidance.
---

# Team Refactor

Execute a large-scale, multi-pass refactor with architecture safety nets.

## Target: the user-provided target or request
Options: directory path | module name | "current branch"

## Workflow Phases

### Phase 1: Assessment (Parallel)
- **Architecture Refactoring Specialist**: Structural issues, boundary violations
- **Code Smell Detector**: Localized anti-patterns
- **Static Code Analyzer**: Complexity hotspots, coupling metrics
- **Technical Debt Tracker**: Existing debt items in scope

### Phase 2: Plan (Sequential)
- **Architect**: Approves refactor plan, identifies blast radius
- **Refactoring Engine**: Sequences the transformations safely

### Phase 3: Execute (Sequential)
- **Refactoring Engine**: Apply transformations in safe order
- **Component Modernization Specialist**: Upgrade dated patterns where appropriate

### Phase 4: Verify (Parallel)
- **Unit Test Generator**: Regenerate tests for changed modules
- **Code Review Automation**: Diff review
- **Code Standards Specialist**: DRY/style conformance

## General Guardrails

- Refactor in small, mergeable increments — never a single monolithic PR
- Tests must remain green at every commit; do not refactor and break tests in the same change
- Preserve public API unless the refactor's goal is to change it (document explicitly)
- Keep behavior identical — characterization tests first, refactor second
- Use codemods/scripts for repetitive transforms; never hand-edit dozens of files identically

## Output Format

```
## Refactor Report: [Target]

### Scope
- Files touched: [count]
- LOC delta: [+added / -removed]

### Transformations Applied
1. [transformation] — [count of occurrences]

### Tests
- Tests: [pass/fail]
- Coverage delta: [+/- %]

### Debt Resolved
- [debt item]

### Remaining Work
1. [item]
```
