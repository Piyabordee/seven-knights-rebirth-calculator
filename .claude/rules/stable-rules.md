# Stable Rules (Non-Negotiable)

> These rules are permanent constraints for this project.
> Do NOT relax them for any task-level prompt.
> See [[CLAUDE]] for operational rules and navigation.

---

## 1. Use `Decimal` Everywhere

Never use `float` for damage math. Import from `decimal`. Float precision causes mismatches with game values — the game's calculations are integer-based and any floating-point drift produces wrong results.

```python
from decimal import Decimal, ROUND_DOWN
```

## 2. Base Weakness is 30%

Weakness damage = `30 + WEAK_DMG`, not just `WEAK_DMG`. The 30% base is hardcoded in the game's mechanic, not from any config value. This is the #1 source of wrong results.

```python
total_weak_dmg = Decimal("30") + weak_dmg  # Always 30 + config value
```

## 3. Config Values are Additive

Character + user values get summed for additive keys (`SKILL_DMG`, `CRIT_DMG`, `WEAK_DMG`, etc.). See [[docs/reference/config-reference]] for the full list.

## 4. Damage is Per-Hit

Final damage formula produces per-hit values. Multiply by `SKILL_HITS` for totals. Never divide by hits.

## 5. ROUNDDOWN Always

Use `Decimal.quantize(Decimal("1"), rounding=ROUND_DOWN)`. This matches the game's behavior where `100.9` becomes `100`, not `101`.

## 6. Use the Registry for New Characters

Characters with special logic: create `logic/[name].py`, register with `@register_character("name")` in `character_registry.py`. Do NOT modify `main.py`. See [[docs/architecture/module-system]].

## 7. No `sys.path` Manipulation

Modules are run from `calculator/` as working directory. The `__main__` block in `main.py` handles Windows encoding — do not duplicate this elsewhere.

---

Related: [[CLAUDE]] | [[docs/reference/formulas]] | [[docs/architecture/module-system]]
