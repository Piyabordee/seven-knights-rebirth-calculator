# 7k Rebirth Damage Calculator — Documentation Index

> Navigation hub for all project documentation.
> Start here to find what you need.

---

## Quick Links

- [[CLAUDE]] — Project hub (AI agents read this first)
- [[.claude/rules/stable-rules]] — Non-negotiable project constraints
- [[.claude/rules/security-rules]] — Security policy
- [[.claude/rules/coding-behavior-rules]] — Coding behavior guidelines
- [[decisions]] — Design rationale & tradeoff log
- [[README]] — User-facing introduction and installation

---

## Project

| Doc | Description |
|-----|-------------|
| [[docs/project/overview]] | What this project is, its purpose, stack, and development context |

## Architecture

| Doc | Description |
|-----|-------------|
| [[docs/architecture/module-system]] | Module responsibilities, Registry Pattern, and how to add new characters |
| [[docs/architecture/damage-pipeline]] | End-to-end calculation flow: config merge → 4 scenarios → display |

## Features

| Doc | Description |
|-----|-------------|
| [[docs/features/character-mechanics]] | 6 special character mechanics: activation conditions, formulas, and logic modules |

## Integrations

| Doc | Description |
|-----|-------------|
| [[docs/integrations/gamewith-data]] | GameWith data sourcing: how character data flows from website to JSON |

## Testing

| Doc | Description |
|-----|-------------|
| [[docs/testing/strategy]] | Test approach, conventions, coverage goals, and test file map |

## Reference

| Doc | Description |
|-----|-------------|
| [[docs/reference/formulas]] | Core damage formulas with gotchas and edge cases |
| [[docs/reference/config-reference]] | All config fields across config.json, character JSONs, and monster presets |

---

## Existing Documentation

These docs are preserved outside the standard category structure:

| Doc | Description |
|-----|-------------|
| [[README]] | User-facing: installation, usage, features, testing |
| [[GAMEWITH_GUIDE]] | How to extract character data from GameWith |
| [[docs/SHOWCASES]] | Character output examples with real calculator results |
| [[decisions]] | Design rationale and tradeoff log |

### Test Documentation

| Doc | Description |
|-----|-------------|
| `calculator/tests/TEST_STRATEGY.md` [[calculator/tests/TEST_STRATEGY]] | Detailed test strategy, coverage matrix, objectives |
| `calculator/tests/TEST_SUITE_SUMMARY.md` [[calculator/tests/TEST_SUITE_SUMMARY]] | Test suite overview and statistics |
| `calculator/tests/README.md` [[calculator/tests/README]] | Test documentation and instructions |

---

## External Resources

- **GameWith** — [Seven Knights Rebirth](https://gamewith.net/sevenknights-rebirth/) (primary data source)
- **Formula Credits** — BelXenonZ and AcidAqua (damage calculation formulas)

---
Related: [[CLAUDE]] | [[docs/project/overview]] | [[decisions]]
