# Module System & Registry Pattern

> How the calculator's modules are organized and how to extend the system with new characters.

---

## Overview

The codebase follows a modular architecture where each module has a single responsibility. Character-specific logic is handled through a **Registry Pattern** — characters self-register handlers via decorators, so `main.py` never needs modification when new characters are added.

## Module Map

```
calculator/
├── main.py                  # Orchestrator — ties all modules together
├── character_registry.py    # Registry + 6 registered handlers
├── config_loader.py         # JSON loading, merging, weapon sets
├── constants.py             # ATK_BASE, DEF_BASE, HP_BASE lookup tables
├── damage_calc.py           # Pure calculation functions (no I/O)
├── menu.py                  # CLI menu interactions (input())
├── display.py               # Output formatting (print())
├── atk_compare_mode.py      # ATK Comparison mode (standalone)
├── logic/                   # Special character logic modules
│   ├── biscuit.py           # Dual Scaling (ATK + DEF)
│   ├── espada.py            # HP-Based multi-scenario
│   ├── freyja.py            # HP Alteration
│   ├── klahan.py            # HP Condition Bonus
│   ├── ryan.py              # Lost HP Bonus + Weakness Extra
│   └── sun_wukong.py        # Castle Mode (min crits)
├── characters/              # Character data (JSON)
│   └── monster/             # Monster presets
└── config.json              # User's live configuration
```

## Dependency Direction

```
main.py
  ├── imports → character_registry.py → logic/*.py
  ├── imports → config_loader.py → characters/*.json, config.json
  ├── imports → damage_calc.py → constants.py
  ├── imports → menu.py → config_loader.py
  └── imports → display.py → damage_calc.py, config_loader.py
```

Key rule: `damage_calc.py` and `constants.py` have **zero imports** from other project modules — they are pure computation with no I/O.

## Component Reference

| Module | Responsibility | Lines of Code |
|--------|---------------|---------------|
| `main.py` | Orchestrates flow: mode → character → skill → calc → display | ~250 |
| `character_registry.py` | Stores `@register_character()` handlers; routes to correct logic | ~380 |
| `config_loader.py` | Loads JSON, filters metadata, merges configs, applies weapon sets | ~127 |
| `damage_calc.py` | 7 pure math functions using `Decimal` | ~146 |
| `constants.py` | ATK_BASE, DEF_BASE, HP_BASE dicts + lookup functions | ~129 |
| `menu.py` | Interactive CLI menus (mode, character, skill selection) | ~161 |
| `display.py` | All `print()` functions for formatted output | ~320 |

## Registry Pattern

### How it works

1. Each character with special logic defines a handler function
2. The handler is registered via `@register_character("name")` decorator
3. `main.py` calls `get_character_handler(char_name)` — returns the handler or `None`
4. If a handler exists and returns `True`, the character's special logic runs instead of the standard pipeline

### Handler Protocol

Every handler follows the `CharacterHandler` protocol — a consistent signature:

```python
def handle_character(
    total_atk: Decimal,
    skill_dmg: Decimal,
    crit_dmg: Decimal,
    weak_dmg: Decimal,
    dmg_amp_buff: Decimal,
    dmg_amp_debuff: Decimal,
    dmg_reduction: Decimal,
    eff_def: Decimal,
    skill_hits: int,
    hp_target: Decimal,
    config: dict[str, Any],       # Special fields for this character
    char_meta: dict[str, Any],    # Character metadata
    skill_config: dict[str, Any], # Selected skill config
    monster_preset: dict[str, Any] | None,  # Castle mode preset
) -> bool:  # Return True if handled, False to fall through
```

Handlers can have additional keyword arguments (e.g., Biscuit accepts `def_char` and `def_pet`).

### Currently Registered Characters

| Name | Handler | Condition to activate |
|------|---------|----------------------|
| `biscuit` | `handle_biscuit` | Always active |
| `espada` | `handle_espada` | `Bonus_DMG_HP_Target > 0` |
| `freyja` | `handle_freyja` | `HP_Alteration > 0` and not both-skills mode |
| `klahan` | `handle_klahan` | `HP_Above_50_Bonus > 0` or `HP_Below_50_Bonus > 0` |
| `ryan` | `handle_ryan` | `Lost_HP_Bonus > 0` and not both-skills mode |
| `sun_wukong` | `handle_sun_wukong` | Castle mode (monster preset loaded) |

## How to Extend: Adding a New Character

### Standard character (no special logic)

1. Create `calculator/characters/[name].json` following the template in [[GAMEWITH_GUIDE]]
2. Done — the character uses the default calculation pipeline automatically

### Character with special logic

1. Create `calculator/characters/[name].json` with required special fields
2. Create `calculator/logic/[name].py` with calculation and display functions
3. In `character_registry.py`, add a handler decorated with `@register_character("name")`
4. **Do NOT modify `main.py`** — the registry handles routing
5. Update [[docs/SHOWCASES]] if the character has a special mechanic
6. Add tests in `calculator/tests/`

For detailed character JSON structure, see [[GAMEWITH_GUIDE]] and [[docs/reference/config-reference]].

---

Related: [[docs/architecture/damage-pipeline]] | [[docs/reference/config-reference]] | [[GAMEWITH_GUIDE]]
