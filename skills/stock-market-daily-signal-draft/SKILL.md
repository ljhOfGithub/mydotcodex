---
name: stock-market-daily-signal-draft
description: Prepare daily stock-market signal articles for "白Yu观测" from current public information, including weekends and market holidays. Use when Codex is asked to collect stock-related information, write a daily equity-market note, build a non-investment-advice WeChat/public-account mother draft, or feed the same content into Xiaohongshu/Douyin publishing routines.
---

# Stock Market Daily Signal Draft

## Overview

Create a sourced daily stock-market observation article for `白Yu观测`. This skill gathers public stock-related information every calendar day, not only trading days, and produces a canonical mother draft that can later be published by WeChat, Xiaohongshu, and Douyin publisher skills.

This skill produces public-information research notes only. It never gives personalized investment advice, trading instructions, position sizing, or target prices.

## Workflow

1. Set the date, market state, and scope.
   - Use the user's current date/time and timezone. For "today/latest", verify live sources.
   - Determine whether each covered market is open, pre-market, post-market, weekend, or holiday. Do not assume a weekday is a trading day.
   - Default scope is broad but stock-centered: US equities, China/HK equities when relevant, major index futures, sector ETFs, rates, FX, commodities, company filings/earnings, policy events, and sentiment/positioning signals.
   - Exclude cryptocurrency, crypto-asset, Bitcoin, Ethereum, stablecoin, and virtual-currency topics before research. They are platform-risk topics and must be replaced, not rewritten.
   - On weekends or holidays, write a `休市版观察`: last close, week-ahead catalysts, earnings calendar, policy/filing/news flow, futures or overseas sessions if open, and watch items for the next trading day.

2. Gather evidence from current sources.
   - Start every candidate pass from `https://www.jin10.com/` or its 7x24 live feed. Record the exact Jin10 URL, displayed Beijing-time timestamp, headline/item text, and retrieval time.
   - Use Jin10 as secondary discovery evidence. When the item identifies an exchange page, regulator filing, company IR release, central-bank/statistical release, or official calendar, verify and record that original source when available.
   - If Jin10 is unavailable or has no current eligible signal, write a failure/no-signal note instead of silently switching to stale material.
   - Record source URL, source name, timestamp, market region, data delay if visible, and retrieval status.
   - If live retrieval fails, stop normal publishing and write a failure note. Do not turn stale data into a normal daily signal.

3. Apply the mandatory financial-services policy gate.
   - Reject candidates involving illegal currency exchange/counterfeiting, prohibited lending or cashout, debt-bearing/electronic-IOU/POS services, off-exchange stock financing, money laundering/running points, proxy insurance surrender, stock/fund/software recommendations, recommendation groups, or noncompliant brokerage commissions such as `万一免五`.
   - Use `node /Users/jackie/.codex/skills/financial-market-signal-draft/scripts/check_finance_policy.mjs <files...>` on candidate notes and again on the final title, body, cards, and tags.
   - If `node` is not available on `PATH`, call `codex_app.load_workspace_dependencies` and use the returned Node executable for both scans. Do not skip the scanner or guess/install a runtime; record the executable and exit code in source notes.
   - On any hit, record the candidate, category, keyword, and URL as `policy-rejected`, discard the whole topic, and continue to the next non-duplicate candidate. Do not merely remove the triggering phrase and keep the same article.

4. Separate facts from interpretation.
   - Facts: price moves, index/sector performance, yields, FX, commodities, earnings, guidance, filings, policy releases, market calendar events, unusual volume/volatility, and source timestamps.
   - Interpretation: state as hypotheses, scenarios, or "需要继续观察", never certainty.
   - Avoid `买入`, `卖出`, `加仓`, `减仓`, `目标价`, `稳赚`, `抄底`, `逃顶`, or direct trading commands unless the user explicitly asks for a separate analysis, and still label it as non-advice.

5. Pick one dominant daily line.
   - Choose one main signal for the title and opening. Examples: "rates led the equity move", "earnings guidance changed sector leadership", "AI infrastructure capex is repriced", "holiday session leaves only catalyst tracking".
   - Keep secondary signals in a watchlist instead of making the article a scattered market recap.
   - For every named stock or sector, explain why it matters to the main line and what evidence supports it.

6. Draft the mother article.
   - Save under `reports/stock-market/YYYY-MM-DD-topic/`.
   - Produce `stock-market-signal-draft.md` and `stock-market-sources.md`.
   - Use exact brand spelling `白Yu观测`.
   - Recommended structure:
     - `标题`
     - `市场状态`
     - `一句话信号`
     - `今日主线`
     - `关键证据`
     - `公司/行业催化`
     - `反证和风险`
     - `后续观察清单`
     - `证据标签`
     - `免责声明`
   - Disclaimer must be exactly: `仅为公开信息整理与研究笔记，不构成投资建议。`

7. Prepare platform handoff.
   - Treat this article as the canonical source for publisher skills.
   - For WeChat, hand off to `wechat-daily-signal-publisher`.
   - For Xiaohongshu, hand off to `xiaohongshu-daily-signal-publisher` as a same-content compact edition.
   - For Douyin, hand off to `douyin-daily-signal-publisher` as a same-content compact edition.
   - Preserve evidence timestamps, uncertainty language, disclaimer, and source order across platforms.
   - Include exactly one pure-text 3:4 image brief for Xiaohongshu and Douyin: brand and timestamp at top, one factual headline, 2-4 compact paragraphs, and a small `来源：金十数据` footer. Integrate market implications and counter-evidence into prose.
   - Prohibit icons, charts, candlesticks, diagrams, flow arrows, illustrations, photos, data tiles, and multi-card carousels. If the copy does not fit, shorten the image text and keep the full detail in the body instead of creating more images.
   - Treat geopolitical or policy statements as attributed claims unless independently verified. Do not use emotional certainty, recommendation language, or copied creator branding to imitate a reference post.
   - Do not mix computer-science paper sections into this finance-only draft unless the user explicitly asks for a combined post.

## Evidence Labels

- `A`: official filing, exchange/central-bank/statistical release, company IR/newsroom, official market calendar, or directly verified market data.
- `B`: reputable financial press, broker/platform market snapshot, or delayed quote with visible timestamp.
- `C`: inference from cross-source patterns, incomplete data, or secondary commentary.

## Weekend And Holiday Rules

- Do not force a "today's price action" narrative when the target market is closed.
- Use `休市版观察` in the title or market-state section when the article is built from non-trading-day evidence.
- Emphasize upcoming catalysts, filings since last close, macro calendar, overseas sessions, futures if open, and what would confirm or invalidate the main line after trading resumes.
- If there is no meaningful new stock-related information, publish a short calendar/watchlist note only if sources support it; otherwise record a no-signal note and skip publishing.

## Validation

Before handoff or publication:

- Confirm every market/stock claim has a source URL and timestamp.
- Confirm current market state was checked for the date.
- Confirm no personalized advice, price target, or trading instruction appears.
- Confirm the disclaimer is present and only used for finance posts.
- Confirm the draft is stock/market-only and not mixed with computer-research content.
- Confirm `白Yu观测` is spelled exactly.
- Confirm source notes include retrieval failures or stale-data boundaries when applicable.
- Confirm the financial-services policy scanner passes every final platform artifact; otherwise replace the article before handoff.
- Confirm the one finance image is pure text, sourced from a current Jin10 item, timestamped, and consistent with the canonical article.
- Inspect the rendered image rather than trusting its prompt: require exactly one 3:4 image, visible `白Yu观测`, a legible Jin10 source/time footer, and no icons, charts, arrows, photos, illustrations, data tiles, boxed modules, or carousel pages.
