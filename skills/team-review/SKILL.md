---
name: team-review
description: Execute a comprehensive code review with the full quality team working in parallel. Use when the user invokes /team-review or asks for Team Code Review team workflow guidance.
---

# Team Code Review

Execute a comprehensive code review with the full quality team working in parallel.

## Workflow Phases

### Phase 1: Parallel Automated Analysis
- **Static Code Analyzer**: Quality, complexity, maintainability metrics
- **Code Smell Detector**: Anti-patterns, duplicate code, long methods
- **Security Vulnerability Scanner**: OWASP vulnerabilities, auth issues
- **Dead Code Eliminator**: Unused code, unreachable branches
- **Code Standards Specialist**: DRY violations, style consistency

### Phase 2: Comprehensive Review
- **Code Review Automation**: Synthesizes all findings into actionable review

### Phase 3: Quality Reporting
- **Technical Debt Tracker**: Updates debt register with new findings
- **Performance Metrics Collector**: Collects and reports quality metrics

## Context

Target: the user-provided target or request (or current working directory / recent changes if not specified)

## Instructions

1. **Gather Context** — Identify target files from arguments or recent changes
2. **Launch Parallel Analysis** — Run all Phase 1 agents simultaneously; collect findings
3. **Synthesize Review** — Pass findings to Code Review Automation; generate prioritized action items
4. **Report** — Summarize findings by severity with file:line references

## Output Format

```
## Code Review Summary

### Critical Issues (must fix)
- [file:line] Description — Agent

### Errors (should fix)
- [file:line] Description — Agent

### Warnings (consider fixing)
- [file:line] Description — Agent

### Info (for awareness)
- [file:line] Description — Agent

### Action Items
1. High priority
2. Medium priority
3. Low priority

### Technical Debt Added
- [item]
```

## Agent Prompts

### Static Code Analyzer
```
Analyze code for:
- Cyclomatic complexity (flag >10)
- Cognitive complexity
- Maintainability index
- Code duplication percentage
- Lines per function (flag >50)
Return structured metrics with file:line references.
```

### Code Smell Detector
```
Identify:
- God classes/objects
- Feature envy
- Shotgun surgery
- Long parameter lists
- Primitive obsession
- Switch statements that should be polymorphism
Return each smell with severity and refactoring suggestion.
```

### Security Vulnerability Scanner
```
Scan for:
- Injection (SQL, XSS, command)
- Authentication/authorization flaws
- Sensitive data exposure
- Missing input validation
- Insecure dependencies
Reference OWASP categories in findings.
```
