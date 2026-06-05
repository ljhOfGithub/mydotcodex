---
name: team-i18n
description: Execute internationalization audit and implementation. Use when the user invokes /team-i18n or asks for Team i18n Implementation team workflow guidance.
---

# Team i18n Implementation

Execute internationalization audit and implementation.

## Target: the user-provided target or request
Options: specific files | "audit" for full compliance check

## Workflow Phases

### Phase 1: Audit (Parallel)
- **Internationalization Expert**: i18n coverage, untranslated strings, locale handling
- **Code Standards Specialist**: Inline styles / hardcoded text detection

### Phase 2: Implementation (Sequential)
- **Fullstack Developer**: Apply i18n wrapping and locale plumbing

### Phase 3: Validation (Parallel)
- **QA Testing**: Verify translations across supported locales
- **Cross Platform Specialist**: Test across devices and browsers
- **Accessibility Compliance Checker**: RTL layout and language accessibility

## Generic i18n Principles

- **All user-facing text routes through a translation layer** — never hardcode display strings in templates or code
- **Language detection order**: URL param → cookie → localStorage → browser → default
- **Locale state is persisted** — selection survives reload
- **Dynamic content uses the same translation layer** as static — no inline literals
- **RTL languages get `dir="rtl"`** at the document level when active
- **Pluralization and date/number formatting** use a locale-aware library (Intl, ICU, etc.)

## Audit Checklist

### Templates / Views
- [ ] All visible text passes through translation
- [ ] No hardcoded literals in JSX/templates
- [ ] Icons/emojis kept outside translatable spans
- [ ] No inline styles that break RTL mirroring

### Code
- [ ] Dynamic strings use the translation API
- [ ] String concatenation replaced with templated translations
- [ ] No date/number formatting via raw `toString()`

### Assets
- [ ] Images with text have language alternates or use real text overlays
- [ ] Fonts support target scripts (CJK, Arabic, etc.)

## Output Format

```
## i18n Compliance Report

### Summary
- Files audited: [count]
- Compliance score: [%]
- Issues: [count] (auto-fixable: [count])

### Issues by Severity

#### Critical
- [file:line] — [issue] — [fix]

#### Warning
- [file:line] — [unwrapped text]

#### Info
- [file:line] — [best practice]

### RTL Testing Required
- [file/page] — [reason]

### Next Steps
1. [action]
```
