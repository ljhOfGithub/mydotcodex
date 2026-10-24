---
name: tradingview-indicator-to-binary-strategy
description: Convert a user-provided TradingView/Pine indicator into a Pine Script strategy that has only two position states, full position and flat, and forces liquidation on the last backtest bar. Use when the user provides TV/Pine indicator code or indicator rules and asks to make it a strategy, especially with requirements like "只有全仓和空仓", "只满仓和清仓", "最新一天卖出", "最后一天清仓", or "方便回测收益率".
---

# TradingView Indicator To Binary Strategy

## Overview

Use this skill to turn a TradingView indicator into a Pine v5 strategy suitable for backtesting. Keep the output conservative: preserve the indicator's signal math where possible, but force position management into a binary state machine.

## Workflow

1. Read the user's indicator code or rule description and identify:
   - long entry condition
   - clear/exit condition
   - any filters that should remain as filters rather than position sizing rules
   - indicator plots, alerts, and inputs worth preserving
2. Prefer creating a new standalone `.pine` file when working in a repo and the user did not explicitly ask to edit an existing file.
3. Convert `indicator(...)` to `strategy(...)` with these defaults:
   - Pine v5 unless the user explicitly asks for another version
   - `default_qty_type=strategy.percent_of_equity`
   - `default_qty_value=100`
   - `pyramiding=0`
   - `process_orders_on_close=true`
4. Keep only full-position and flat states. Remove or avoid partial exits, add-ons, scale-outs, `qty_percent`, tiered take profits, and separate position-size tracking unless the user explicitly asks for them.
5. Add final-bar liquidation and final-bar entry guard as separate concepts:
   - define `isFinalBar = barstate.islast`
   - prevent new entries when `isFinalBar`
   - close any open position on `isFinalBar`, typically with `strategy.close_all(comment="Final sell")`
6. Preserve useful plots and labels only when they help inspect signals. Do not let visuals complicate the trading state machine.
7. Explain that local checks can inspect file content and required constructs, but TradingView is the final authority for Pine compilation and backtest behavior.

## Pine Pattern

Use this skeleton when the user's indicator supplies `longCondition` and `exitCondition` equivalents:

```pine
//@version=5
strategy("Name - Full/Flat Strategy",
     overlay=true,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     pyramiding=0,
     process_orders_on_close=true)

// Keep original indicator inputs and calculations here.

isFinalBar = barstate.islast
canEnter = not isFinalBar

if longCondition and canEnter and strategy.position_size <= 0
    strategy.entry("Long", strategy.long)

if exitCondition and strategy.position_size > 0
    strategy.close("Long", comment="Clear")

if isFinalBar and strategy.position_size != 0
    strategy.close_all(comment="Final sell")
```

For reversal-style indicators, ensure the final bar does not both close and reopen. Compute `longCondition`, `exitCondition`, `isFinalBar`, and `canEnter` explicitly instead of burying them in one compound expression.

## Guardrails

- Do not claim the strategy has been fully validated unless it was actually compiled in TradingView.
- Do not invent broker/account configuration, API keys, or live-trading setup.
- Do not leak secrets from user files or environment variables.
- Keep changes small and easy to review.
- If behavior changes in an existing strategy file, add or describe focused checks for the changed constructs.
- If using `input.time`, use a compile-time constant millisecond literal for the default value; Pine v5 rejects `timestamp(...)` in places that require a `const int`.
