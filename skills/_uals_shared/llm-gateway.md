# Shared Reference: Single LLM Gateway (one chokepoint for ALL model calls)

<!--
Copyright (c) 2026 Xiangen Hu. All rights reserved.

DISCLAIMER: This skill is provided "as is", without warranty of any kind, express or
implied. It orchestrates AI agents that may read, modify, and execute code and may
incur LLM and cloud costs. Review all generated output and changes before use. The
author assumes no liability for any damages or losses arising from its use.
-->

**Project invariant.** Every LLM request in the app — help answers, content generation, eval
graders, safety probes, any future feature — goes through the **one** gateway (`callLLM()` in
`runtime/src/llm/gateway.js`). **No feature code imports or calls a provider directly.** Canonical
here; pulled into content, help, eval, ai-safety, cost via `@.claude/commands/_shared/llm-gateway.md`.

## Why one gateway (the four things it centralizes)
1. **Language consistency.** The gateway injects `Respond in {language}. Do not switch languages
   mid-answer.` for every request given a `lang`, so no caller can forget it and no answer drifts
   languages. (Pass `lang`; the directive is added centrally.)
2. **Token accounting.** Every real call records `{ userId, feature, model, prompt/completion
   tokens, cached }` to GCS for cost computation (see `/team-cost`). A cache hit costs ~0 and is
   recorded as such. No call escapes accounting because no call bypasses the gateway.
3. **Provider choice & failover.** Swap models/providers in one file; callers are unaffected
   (the `callLLM({system, user, lang, userId, feature})` signature is the contract).
4. **Caps, prompt hygiene, safety hooks.** Rate/spend caps, redaction, and refusal policy attach
   once, here — not re-implemented per feature.

## The rule, stated plainly
- ✅ `const { callLLM } = require('@uals/skill-runtime').llm; await callLLM({ system, user, lang, userId, feature });`
- ❌ `import OpenAI from 'openai'` (or any provider SDK / raw `fetch` to a provider) anywhere in feature code.
- ❌ Building the "respond in X language" line yourself — pass `lang` and let the gateway add it.

## Audit signal (violation)
Any provider SDK import, or any `fetch(`…provider-host…`)`, outside `runtime/src/llm/`.
