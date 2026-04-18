# 7k Rebirth Damage Calculator — Documentation Index

> Navigation hub for all project documentation.
> Start here to find what you need.

---

## Quick Links

- [[CLAUDE]] — Project hub (AI agents read this first)
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

## Reference

| Doc | Description |
|-----|-------------|
| [[docs/reference/formulas]] | Core damage formulas with gotchas and edge cases |
| [[docs/reference/config-reference]] | All config fields across config.json, character JSONs, and monster presets |

---

## Existing Documentation

These docs are preserved outside the docs/ structure:

| Doc | Description |
|-----|-------------|
| [[README]] | User-facing: installation, usage, features, testing |
| [[GAMEWITH_GUIDE]] | How to extract character data from GameWith |
| [[docs/SHOWCASES]] | Character output examples with real calculator results |

### Test Documentation

| Doc | Description |
|-----|-------------|
| [TEST_STRATEGY.md](calculator/tests/TEST_STRATEGY.md) | Test strategy, coverage matrix, objectives |
| [TEST_SUITE_SUMMARY.md](calculator/tests/TEST_SUITE_SUMMARY.md) | Test suite overview and statistics |
| [tests/README.md](calculator/tests/README.md) | Test documentation and instructions |

---

## External Resources

- **GameWith** — [Seven Knights Rebirth](https://gamewith.net/sevenknights-rebirth/) (primary data source)
- **Formula Credits** — BelXenonZ and AcidAqua (damage calculation formulas)

---

Related: [[CLAUDE]] | [[docs/project/overview]]
