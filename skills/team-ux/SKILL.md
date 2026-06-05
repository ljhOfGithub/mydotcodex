---
name: team-ux
description: Design and audit end-to-end user experience (UI + journey + consistency + cross-platform). Use when the user invokes /team-ux or asks for Team UX team workflow guidance.
---

# Team UX

Design and audit end-to-end user experience (UI + journey + consistency + cross-platform).

## Target: the user-provided target or request
Options: "audit" | "journey <name>" | "component <name>" | "redesign <page>"

## Workflow Phases

### Phase 1: Discovery (Parallel)
- **User Journey Specialist**: Map flow, identify friction and drop-off
- **UX Consistency Specialist**: Style / component drift, design-token violations
- **Cross-Platform Specialist**: Mobile / tablet / desktop parity
- **UI/UX Specialist**: Component-level usability

### Phase 2: Design (Sequential)
- **UI/UX Specialist**: Propose changes

### Phase 3: Implement (Sequential)
- **UI/UX Specialist**: Apply changes via the project's component system

## Generic UX Principles

- **Components from a shared design system** — no one-off styled elements
- **Safe dynamic rendering** — never inject untrusted HTML; use the framework's safe primitives
- **i18n by default** — every visible string routes through the translation layer
- **Consistent state visibility** — auth state, loading, errors expressed the same way everywhere
- **Mobile-first responsive** — primary breakpoint is small, then enhance for larger
- **Progressive enhancement** — core flow works without JS-heavy features when possible
- **Loading states for every async operation** — never leave the user staring at a blank screen

## Output Format

```
## UX Report

### Friction Points
- [step] — [issue] — [proposed fix]

### Consistency Violations
- [component] — [violates token / pattern]

### Cross-Platform Issues
- [breakpoint] — [issue]

### Implemented
- [change]

### Deferred (Needs Stakeholder Input)
- [change] — [decision needed]
```
