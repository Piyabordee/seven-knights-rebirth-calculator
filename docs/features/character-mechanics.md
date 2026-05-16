# Special Character Mechanics

> How the 6 characters with non-standard damage logic differ from the standard pipeline.
> For formulas and implementation details, see [[docs/reference/formulas]].

---

## When to Read This

**Trigger:** Adding a new character with special logic, debugging a special character's output, or understanding why a character's results differ from the standard 4-scenario output.

**Read With:**
- `docs/reference/formulas.md` [[docs/reference/formulas]] — detailed formula implementations
- `docs/architecture/module-system.md` [[docs/architecture/module-system]] — how to register new handlers

---

## Overview

The standard damage pipeline produces 4 scenarios (Crit, Crit+Weakness, No Crit, Weakness Only) for every character. Six characters have mechanics that diverge from this pipeline — their handlers in `character_registry.py` intercept the flow and produce custom outputs.

Each handler follows the same pattern:
1. Check activation conditions (specific config fields must be non-zero)
2. Call dedicated calculation functions in `logic/[name].py`
3. Call dedicated display functions
4. Return `True` to signal "handled" (standard pipeline is skipped)

---

## Biscuit — Dual Scaling (ATK + DEF)

**Why special:** Biscuit scales with both ATK and DEF stats, producing two separate RAW damage calculations that are summed.

**Activation:** Always active (handler always returns `True`).

**Mechanic:**
- Calculates `Total_DEF` from `DEF_CHAR` + `DEF_PET` + base DEF bonus
- Runs `calculate_raw_dmg()` twice: once with Total_ATK/SKILL_DMG, once with Total_DEF/SKILL_DMG_DEF
- Sums both results for final damage

**Key config fields:** `DEF_CHAR`, `DEF_PET`, `SKILL_DMG_DEF`
**Logic module:** `calculator/logic/biscuit.py`
**See also:** [[docs/SHOWCASES]] for example output

---

## Espada — HP-Based Multi-Scenario

**Why special:** Espada's damage includes an HP-based component that compares Raw Damage vs HP-Based Damage for each scenario.

**Activation:** `Bonus_DMG_HP_Target > 0`

**Mechanic:**
- Calculates standard RAW damage for 4 scenarios
- Also calculates HP-based damage (`HP_Target × Bonus_DMG_HP_Target / 100`, capped at `Cap_ATK%`)
- For each scenario, outputs the **higher** of the two values

**Key config fields:** `Bonus_DMG_HP_Target`, `Cap_ATK_Percent`
**Logic module:** `calculator/logic/espada.py`
**See also:** [[docs/reference/formulas]] for HP-based damage formulas

---

## Freyja — HP Alteration

**Why special:** Freyja doesn't deal conventional damage — she directly reduces target HP to a percentage, bypassing DEF entirely.

**Activation:** `HP_Alteration > 0` and not in both-skills mode

**Mechanic:**
- Calculates `HP_Target × (100 - HP_Alteration) / 100` as the HP reduction
- Not affected by DEF, SKILL_DMG, or CRIT_DMG
- Also shows weakness-adjusted HP alteration for reference

**Key config fields:** `HP_Alteration`
**Logic module:** `calculator/logic/freyja.py`
**See also:** [[decisions]] (D004 — 4-scenario override)

---

## Klahan — HP Condition Bonus

**Why special:** Klahan's SKILL_DMG changes based on whether the target's HP is above or below 50%.

**Activation:** `HP_Above_50_Bonus > 0` or `HP_Below_50_Bonus > 0`

**Mechanic:**
- Modifies SKILL_DMG before the standard formula runs
- If HP >= 50%: `SKILL_DMG += HP_Above_50_Bonus`
- If HP <= 50%: `SKILL_DMG += HP_Below_50_Bonus`
- Then runs the standard 4-scenario calculation with modified SKILL_DMG

**Key config fields:** `HP_Above_50_Bonus`, `HP_Below_50_Bonus`
**Logic module:** `calculator/logic/klahan.py`

---

## Ryan — Lost HP Bonus + Weakness Extra

**Why special:** Ryan's damage scales with how much HP the target has lost, and he gets an extra skill multiplier on weakness hits.

**Activation:** `Lost_HP_Bonus > 0` and not in both-skills mode

**Mechanic:**
- Calculates `lost_hp = 100 - Target_HP_Percent`
- Bonus multiplier: `Lost_HP_Bonus × lost_hp / 100`
- Weakness hits also get `WEAK_SKILL_DMG` as an extra multiplier
- Damage scales linearly — max bonus equals `Lost_HP_Bonus` when target is at 0%

**Key config fields:** `Lost_HP_Bonus`, `WEAK_SKILL_DMG`, `Target_HP_Percent`
**Logic module:** `calculator/logic/ryan.py`

---

## Sun Wukong — Castle Mode (Minimum Crits)

**Why special:** Sun Wukong's Castle Mode calculates the minimum number of crits needed to kill a target, iterating over possible crit counts.

**Activation:** Castle mode (monster preset loaded) and not in both-skills mode

**Mechanic:**
- For each possible crit count `c` out of `n` hits:
  - `total_dmg = (c × dmg_crit_weak) + ((n - c) × dmg_weak_only)`
  - If `total_dmg >= HP_Target`: kill achieved with `c` crits
- Reports minimum crits needed, which is the key metric for Castle Rush planning

**Key config fields:** Standard fields + Castle mode monster presets
**Logic module:** `calculator/logic/sun_wukong.py`
**See also:** [[docs/SHOWCASES]] for example output

---

## Adding a New Special Character

1. Create `calculator/logic/[name].py` with calculation and display functions
2. In `character_registry.py`, add a handler decorated with `@register_character("name")`
3. Follow the `CharacterHandler` protocol signature
4. Check activation conditions at the start of the handler
5. Return `True` when handled, `False` to fall through to standard pipeline
6. Do NOT modify `main.py`

See [[docs/architecture/module-system]] for the full extension guide.

---

Related: [[docs/reference/formulas]] | [[docs/architecture/module-system]] | [[docs/architecture/damage-pipeline]] | [[docs/SHOWCASES]]
