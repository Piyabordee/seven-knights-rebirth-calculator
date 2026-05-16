# 7k Rebirth Damage Calculator — Project Hub

> Central operational hub for AI agents working on this codebase.
> For full documentation index, see [[docs/_index]].

---

## Identity

See [[docs/project/overview]] for full project identity, purpose, and stack.

---

## Read First

- [[.claude/rules/stable-rules]] — Non-negotiable project constraints (read BEFORE writing code)
- [[.claude/rules/security-rules]] — Security policy
- [[.claude/rules/coding-behavior-rules]] — Coding behavior (think first, simplicity, surgical changes)
- [[docs/_index]] — Full documentation map
- [[docs/project/overview]] — Project identity and stack
- [[README]] — User-facing introduction

---

## Quick Commands

```bash
cd calculator && python main.py                 # Run the calculator
pytest calculator/tests/ -v                     # Run all tests
pytest calculator/tests/ --cov=calculator       # Run with coverage
ruff check calculator/                          # Lint
mypy calculator/ --ignore-missing-imports       # Type check
```

---

## Stable Rules

Three rule files govern this project (all in `.claude/rules/`):

- [[.claude/rules/stable-rules]] — 7 non-negotiable project constraints. Summary:

1. Use `Decimal` everywhere (never `float`)
2. Base weakness is 30%
3. Config values are additive
4. Damage is per-hit
5. ROUNDDOWN always
6. Use the Registry for new characters
7. No `sys.path` manipulation

- [[.claude/rules/security-rules]] — Never commit secrets, never exfiltrate code, validate security impact
- [[.claude/rules/coding-behavior-rules]] — Think before coding, simplicity first, surgical changes, goal-driven execution

---

## Directory Tree (Authoritative)

```
7k-project/
├── .claude/rules/
│   ├── stable-rules.md                # Non-negotiable project constraints
│   ├── security-rules.md              # Security policy
│   └── coding-behavior-rules.md       # Coding behavior guidelines
├── CLAUDE.md                            # This file — AI agent hub
├── decisions.md                         # Design rationale & tradeoff log
├── README.md                            # User-facing introduction
├── GAMEWITH_GUIDE.md                    # Character data extraction guide
├── pyproject.toml                       # Build config (Python 3.10+, stdlib only)
├── pytest.ini                           # Test configuration
├── docs/
│   ├── _index.md                        # Navigation hub
│   ├── SHOWCASES.md                     # Character output examples
│   ├── project/overview.md              # Project identity
│   ├── architecture/
│   │   ├── module-system.md             # Module map & Registry Pattern
│   │   └── damage-pipeline.md           # End-to-end calculation flow
│   ├── features/
│   │   └── character-mechanics.md       # 6 special character mechanics
│   ├── integrations/
│   │   └── gamewith-data.md             # GameWith data sourcing workflow
│   ├── testing/
│   │   └── strategy.md                  # Test approach & conventions
│   └── reference/
│       ├── formulas.md                  # Core formulas with gotchas
│       └── config-reference.md          # All config fields
└── calculator/
    ├── main.py                          # Entry point + orchestrator
    ├── character_registry.py            # Registry + 6 handlers
    ├── config_loader.py                 # JSON loading, merging, weapon sets
    ├── constants.py                     # ATK/DEF/HP base lookup tables
    ├── damage_calc.py                   # Pure calculation functions
    ├── menu.py                          # CLI menu interactions
    ├── display.py                       # Output formatting
    ├── atk_compare_mode.py              # ATK Comparison mode
    ├── logic/                           # Special character logic (6 modules)
    ├── characters/                      # Character data JSONs (14 files)
    │   └── monster/                     # Monster presets (3 files)
    ├── config.json                      # User's live configuration
    └── tests/                           # Test suite (6 files)
```

---

## Task Routing

| Task | Read these docs first |
|------|----------------------|
| Add a standard character | `docs/reference/config-reference.md` [[docs/reference/config-reference]], `GAMEWITH_GUIDE.md` [[GAMEWITH_GUIDE]] |
| Add a character with special logic | `docs/architecture/module-system.md` [[docs/architecture/module-system]], `docs/features/character-mechanics.md` [[docs/features/character-mechanics]], `.claude/rules/stable-rules.md` [[.claude/rules/stable-rules]] |
| Fix a formula bug | `docs/reference/formulas.md` [[docs/reference/formulas]], `docs/architecture/damage-pipeline.md` [[docs/architecture/damage-pipeline]] |
| Update character data from GameWith | `docs/integrations/gamewith-data.md` [[docs/integrations/gamewith-data]], `GAMEWITH_GUIDE.md` [[GAMEWITH_GUIDE]] |
| Add or modify tests | `docs/testing/strategy.md` [[docs/testing/strategy]] |
| Understand a design choice | `decisions.md` [[decisions]] |
| Onboard to the project | `docs/project/overview.md` [[docs/project/overview]], `docs/_index.md` [[docs/_index]] |

---

## Doc Workflow

When creating or significantly modifying a feature:

1. **Feature doc** — create in `docs/features/` if non-obvious behavior
2. **Design Origin** — link to spec/plan if applicable
3. **Link here** — add entry to Documentation Map below
4. **Link related docs** — add wiki links in Related section

### Where to put docs

| Category | Path | When |
|----------|------|------|
| Feature workflow | `docs/features/` | New user-facing behavior |
| Architecture | `docs/architecture/` | Structural changes |
| Integration | `docs/integrations/` | External tool workflows |
| Testing | `docs/testing/` | Test strategy changes |
| Reference | `docs/reference/` | New constants, config options |
| Project | `docs/project/` | Known issues, project changes |

---

## Documentation Map

See [[docs/_index]] for the full documentation index with all project, architecture, feature, integration, testing, and reference docs.

---

## Key Warnings

- **Weakness base 30%** — The #1 source of wrong results. See [[docs/reference/formulas]]
- **Decimal not float** — Float precision causes mismatches with game values
- **DMG_Reduction is in RAW step** — Not after dividing by DEF. See [[docs/reference/formulas]]
- **Windows Thai encoding** — `main.py` wraps stdout/stdin with UTF-8. Only in `__main__` block.

---

Related: [[docs/_index]] | [[.claude/rules/stable-rules]] | [[.claude/rules/security-rules]] | [[.claude/rules/coding-behavior-rules]] | [[decisions]] | [[README]]
