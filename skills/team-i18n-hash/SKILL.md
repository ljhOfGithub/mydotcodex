---
name: team-i18n-hash
description: Implement and audit SHA-256 hash-based i18n — the preferred i18n pattern for these apps. Use when the user invokes /team-i18n-hash or asks for Team i18n (Hash-Based) team workflow guidance.
---

# Team i18n (Hash-Based)

Implement and audit SHA-256 hash-based i18n — the preferred i18n pattern for these apps.

## Target: the user-provided target or request
Options: specific files | "audit" for full compliance check

## Workflow Phases

### Phase 1: Audit (Parallel)
- **Internationalization Expert**: Hash compliance, untranslated strings, missing wrappers
- **Code Standards Specialist**: Inline styles (break RTL), embedded `<style>` / `<script>`

### Phase 2: Implementation (Sequential)
- **Fullstack Developer**: Wrap text, generate hashes, register translations

### Phase 3: Validation (Parallel)
- **QA Testing**: Verify translations match hashes; spot-check all supported languages
- **Cross Platform Specialist**: Test on devices and browsers
- **Accessibility Compliance Checker**: RTL layout and language accessibility

## The Hash-Based Pattern

### Hash Generation
```javascript
// Hash = SHA-256 of trimmed English text, first 16 hex chars
generateHash("Continue") // => "31fbef162594de01"
generateHash("Welcome back!") // => "a7c4e9..."
```

- Source language is **English**
- Whitespace is trimmed before hashing
- Case-sensitive
- 16 hex chars (first 64 bits of SHA-256) — collision risk is acceptable for human text

### Static Text Wrapping
```html
<span data-i18n="31fbef162594de01">Continue</span>
```

- Every visible text node MUST be wrapped
- **Emojis stay outside the span**: `📚 <span data-i18n="hash">Library</span>`
- No inline styles — they break RTL flipping. Use CSS classes only.

### Dynamic Text
```javascript
const wrapped = await addText("Welcome back!");
element.innerHTML = wrapped;
// Registers the hash if new, returns <span data-i18n="...">Welcome back!</span>
```

- All dynamic strings go through `addText()` (or the project's equivalent)
- Never concatenate translated fragments — translate whole phrases

### Mandatory Script Loading

Every HTML page loads three scripts in this exact order, at the start of `<body>`:

```html
<body>
    <script src="/js/shared/i18nInit.js"></script>
    <script src="/js/shared/i18nUtils.js"></script>
    <script src="/js/i18nDynamicTranslator.js"></script>
    <!-- rest of page -->
</body>
```

### Language Detection Priority

1. URL parameter: `?lang=zh` (also accepts `?lng=`, `?language=`)
2. Cookie: `preferredLanguage` (30-day persistence)
3. localStorage: `preferredLanguage` (backup)
4. Browser language: `navigator.language`
5. Default: `'en'`

### Supported Languages

- **LTR**: en, zh, es, de, fr, it, pt, ja, ko, th, vi, ru, hi
- **RTL**: ar, he, fa, ur — applied via `dir="rtl"` at document level

### Translation Storage

Translations live in GCS (see `team-gcs`), not in the repo. The hash registry maps `hash → { en: "...", zh: "...", ... }`.

## Common Violations

- ❌ Hardcoded text in JSX/templates (most common)
- ❌ String concatenation: `"Hello, " + name` — translate the whole phrase with a placeholder
- ❌ Inline `style="..."` — breaks RTL mirroring
- ❌ Emoji inside the `<span data-i18n>` — wraps the emoji as translatable
- ❌ Script loading out of order — `i18nInit.js` must be first
- ❌ Hash that doesn't match the English source — silent translation failure
- ❌ Dynamic content built via raw `innerHTML` without `addText()`

## Audit Checklist

### HTML
- [ ] Three i18n scripts loaded in correct order at start of `<body>`
- [ ] All text wrapped in `<span data-i18n="hash">`
- [ ] Hashes match the English text exactly (case + whitespace)
- [ ] Emojis kept outside spans
- [ ] No inline styles

### JavaScript
- [ ] Dynamic text uses `addText()`
- [ ] No `innerHTML = "raw text"` — always translated first
- [ ] Hash registration calls present for new strings

### CSS
- [ ] No hardcoded text in pseudo-elements
- [ ] Logical properties used (`margin-inline-start` over `margin-left`) where possible

## Output Format

```
## i18n Compliance Report

### Summary
- Files audited: [count]
- Compliance score: [%]
- Issues: [count] (auto-fixable: [count])

### Issues by Severity

#### Critical (Breaks i18n)
- [file:line] — [issue] — [fix]

#### Warnings (Should Fix)
- [file:line] Text: "[text]" — Add: `<span data-i18n="[hash]">[text]</span>`

#### Info (Best Practice)
- [file:line] — [item]

### New Hashes to Register
| Hash | English Text |
|------|--------------|

### RTL Testing Required
- [file/page] — [reason]
```
