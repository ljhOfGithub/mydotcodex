---
name: team-architect
description: Design a new system or major component with an architecture-first workflow. Use when the user invokes /team-architect or asks for Team Architect team workflow guidance.
---

# Team Architect

Design a new system or major component with an architecture-first workflow.

## Target: the user-provided target or request

## Workflow Phases

### Phase 1: Discovery (Parallel)
Launch simultaneously:
- **Architect**: System design, patterns, integration points, scalability
- **Data Analyst**: Analytics/observability requirements
- **Security Specialist**: Threat model, auth/authz surface
- **UI/UX Specialist**: User-facing surface area (if applicable)

### Phase 2: Synthesis (Sequential)
- **Architect**: Consolidates findings into an Architecture Decision Record (ADR)

### Phase 3: Validation (Parallel)
- **Code Standards Specialist**: DRY/SOLID conformance check
- **Dependency Manager**: Required deps and licensing
- **DevOps Engineer**: Infrastructure feasibility

## General Principles

- Prefer ONE implementation of each capability; avoid parallel forks that drift
- Make integration points explicit (interfaces, contracts, schemas)
- Identify data ownership and source-of-truth boundaries up front
- Choose boring technology unless there's a reason not to
- Design for observability and rollback before scale

## Output Format

```
## Architecture Decision Record: [Target]

### Context
[Why this design is needed]

### Decision
[The architectural choice]

### Components
- [component]: [responsibility]

### Integration Points
- [system]: [interface]

### Data Flow
[Sources of truth, write paths, read paths]

### Trade-offs
- Pros: [list]
- Cons: [list]

### Open Questions
1. [question]
```
