---
name: financial-market-signal-draft
description: Prepare Chinese WeChat Official Account drafts focused only on financial market signals, macro catalysts, equities, sectors, rates, commodities, and company events. Use when Codex is asked to write a market-signal daily push, summarize market movements, organize finance sources, or draft non-investment-advice commentary without computer science paper deep-reading.
---

# Financial Market Signal Draft

## Goal

Write a finance-only public-account draft with current market evidence. Do not include computer-science paper summaries unless the user explicitly asks to merge them later.

This skill produces information整理 and research notes, never personalized investment advice.

## Workflow

1. Confirm market scope.
   - Default to broad signals: major indices, rates, currencies, commodities, sector rotation, earnings/policy catalysts, and unusual volume or volatility.
   - Never select cryptocurrency, crypto-asset, stablecoin, or virtual-currency topics. Treat the whole topic as platform-risk content even when it contains no financial service or recommendation.
   - Use the user's date/time; for "today/latest", verify live sources.

2. Gather sources.
   - Use `https://www.jin10.com/` and its 7x24 live feed as the default discovery source for every finance article. Record the exact Jin10 page/item URL, displayed Beijing-time timestamp, headline, and retrieval time.
   - Treat Jin10 as a fast secondary source (`B`), not automatic primary evidence. When a Jin10 item identifies an exchange, regulator, central bank, statistics agency, company filing, or official statement, open and record that original source when available before assigning evidence `A`.
   - If the live feed exposes no stable item URL, record the live-page URL, displayed timestamp, exact item text, and a local capture or source-note excerpt so the item remains auditable.
   - Do not replace a missing current Jin10 item with stale news. If Jin10 is unavailable, record retrieval failure and stop that finance slot unless the user explicitly authorizes a different discovery source.

3. Apply the mandatory financial-services policy gate.
   - Reject any candidate whose core subject is cryptocurrency, crypto assets, Bitcoin, Ethereum, stablecoins, or virtual currencies. Do not publish, sanitize, or rewrite the topic for another platform.
   - Reject any candidate involving seeking, offering, teaching, promoting, or directing readers to illegal currency exchange/counterfeiting, prohibited lending or credit-card cashout, debt-bearing services, electronic IOUs, POS-machine sales, off-exchange stock financing, money laundering/running points, proxy insurance surrender, stock/fund/software recommendations, recommendation groups, or noncompliant brokerage commissions such as `万一免五`.
   - Run `node scripts/check_finance_policy.mjs <candidate-or-draft-files...>` before selecting the topic and again on the final title, body, cards, and tags.
   - If `node` is not available on `PATH`, call `codex_app.load_workspace_dependencies` and run the scanner with the Node executable returned by that environment. Do not skip the scan, guess a path, or install a system runtime. Record the resolved executable and exit code in source notes.
   - Exit code `2` is a hard content rejection. Record the rejected candidate, matched category, matched keyword, and source URL in source notes; abandon the entire topic and continue with the next independent candidate.
   - Do not make a rejected topic publishable by deleting a few keywords. Select a different article whose core subject is outside the prohibited service category.

4. Separate fact from interpretation.
   - Write facts first: price moves, yields, earnings, policy events, reported guidance, and source timestamps.
   - Then write interpretation as hypotheses, not certainty.
   - Avoid buy/sell/target-price language unless the user explicitly requests analysis, and still label it as non-advice.

5. Draft structure.
   - Title: market-specific and time-bound.
   - `今日总览`
   - `核心市场信号`
   - `公司/行业催化`
   - `风险与反证`
   - `后续观察清单`
   - Disclaimer: `仅为公开信息整理与研究笔记，不构成投资建议`

6. Prepare one pure-text finance image for Xiaohongshu and Douyin.
   - Produce exactly one 3:4 text page per finance article by default. Do not create a carousel, multi-card explainer, or separate data/market-transmission/risk images.
   - Render the page from a per-article `finance-card-spec.json` with `/Users/jackie/Documents/paper daily/reports/tools/render_finance_text_card.py`. Reuse this shared renderer instead of creating an ad hoc SVG, CJS, Swift, AppKit, or alternate visual template for each run. If the shared renderer fails, record the local-artifact failure; do not silently switch styles.
   - Match a restrained text-news layout: white or warm-neutral background; small `白Yu观测` brand line; visible `YYYY-MM-DD HH:mm` timestamp; one high-contrast red or dark headline; 2-4 compact paragraphs; and a small `来源：金十数据｜时间：...` footer.
   - Keep the reference-derived hierarchy observable without copying a creator identity: compact brand/category and timestamp on one line, a thin divider, a factual headline smaller than the body-dominating poster style, continuous news paragraphs, and a footer divider. Use one muted news red for the headline and paragraphs, keep metadata neutral, and avoid large unused lower-page gaps when copy can remain legible at a larger body size.
   - Use typography only. Prohibit icons, pictograms, charts, candlesticks, diagrams, flow arrows, decorative illustrations, photos, colored data tiles, and boxed infographic components.
   - Put the core facts into the single image so a reader can understand the event without opening a long caption. Integrate the market implication and counter-signal as normal sentences, not separate visual modules.
   - Separate attributed statements from verified events. Write `某机构称/文件显示` when the evidence is a statement; do not turn it into an established fact.
   - Use `快讯` or `突发` only when the source and timestamp support genuinely new information. Never use `绝境`, `暴涨在即`, `最后机会`, or similar emotional certainty as editorial voice.
   - Keep the single page scannable. If all evidence cannot fit legibly, compress the image copy and preserve detail in the canonical article/body; do not respond by generating more images.
   - Do not copy another creator's wording, logo, brand name, color system, or image composition. Reuse only the information hierarchy.

7. Evidence labels.
   - `A`: official filings, exchange/central-bank/company data, or directly verified market data.
   - `B`: reputable financial press or delayed market-data snapshot.
   - `C`: inference from cross-source patterns or incomplete data.

## Validation

Before finishing:

- Confirm all market data has source and timestamp.
- Confirm no CS paper section slipped into a finance-only draft.
- Confirm disclaimer is present.
- Confirm no personalized advice, price target, or trading instruction is presented as a recommendation.
- Confirm the policy scanner passes the final title, body, cards, and tags. Any hit requires replacing the article, not editing around the hit.
- Confirm the finance package contains one pure-text image with no icons, charts, diagrams, photos, or infographic modules.
- Confirm the image includes the Jin10 source URL or auditable live-page reference, displayed timestamp, and preserved attribution.
- Inspect the rendered finance image itself before handoff: require exactly one 3:4 image, visible brand text exactly `白Yu观测`, a legible Jin10 source/time footer, and zero icons, charts, arrows, photos, illustrations, data tiles, boxed modules, or extra carousel images. A compliant generation prompt alone does not pass this gate.
