# 7k Rebirth Damage Calculator — Project Hub

> Central operational hub for AI agents working on this codebase.
> For full documentation index, see [[docs/_index]].

---

## Identity

See [[docs/project/overview]] for full project identity, purpose, and stack.

---

## Read First

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

## Working Rules

1. **Use `Decimal` everywhere** — Never use `float` for damage math. Import from `decimal`.
2. **Base weakness is 30%** — Weakness damage = `30 + WEAK_DMG`, not just WEAK_DMG. See [[docs/reference/formulas]].
3. **Config values are additive** — Character + user values get summed for additive keys (SKILL_DMG, CRIT_DMG, etc.). See [[docs/reference/config-reference]].
4. **Damage is per-hit** — Final damage formula produces per-hit values. Multiply by `SKILL_HITS` for totals.
5. **ROUNDDOWN always** — Use `Decimal.quantize(Decimal("1"), rounding=ROUND_DOWN)`.
6. **Use the Registry** — New characters with special logic: create `logic/[name].py`, register with `@register_character("name")`. Do NOT modify `main.py`. See [[docs/architecture/module-system]].
7. **No `sys.path` manipulation** — Modules are run from `calculator/` as working directory.

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
| Reference | `docs/reference/` | New constants, config options |
| Project | `docs/project/` | Known issues, project changes |

---

## Documentation Map

See [[docs/_index]] for the full documentation index with all project, architecture, and reference docs.

---

## Key Warnings

- **Weakness base 30%** — The #1 source of wrong results. See [[docs/reference/formulas]]
- **Decimal not float** — Float precision causes mismatches with game values
- **DMG_Reduction is in RAW step** — Not after dividing by DEF. See [[docs/reference/formulas]]
- **Windows Thai encoding** — `main.py` wraps stdout/stdin with UTF-8. Only in `__main__` block.

---

Related: [[docs/_index]] | [[README]]
