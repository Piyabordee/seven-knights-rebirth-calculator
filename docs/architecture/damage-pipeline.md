# Damage Calculation Pipeline

> How a damage calculation flows from start to finish in the calculator.

---

## Overview

Every damage calculation follows the same pipeline: load configs → compute Total ATK → calculate RAW damage for 4 scenarios → compute Effective DEF → divide by DEF → output. Characters with special logic branch off at the final step.

## Pipeline Flow

```
1. MODE SELECTION
   └── Standard / Castle Rush / ATK Compare
       └── Castle Rush loads monster presets (overrides DEF_Target, HP_Target, etc.)

2. CHARACTER SELECTION
   └── Load characters/[name].json → split into metadata (_keys) and config

3. SKILL SELECTION
   └── Select skill1/skill2/both → extract skill-specific config

4. CONFIG MERGE (3-layer)
   └── character config + skill config + user config.json
       └── Additive keys: SUM values (SKILL_DMG, CRIT_DMG, WEAK_DMG, etc.)
       └── Mapping keys: redirect (Bonus_Crit_DMG → CRIT_DMG)
       └── Weapon set bonuses applied

5. TOTAL ATK CALCULATION
   └── (ATK_CHAR + ATK_PET + ATK_BASE × (Formation + Potential_PET)/100)
       × (1 + (BUFF_ATK + BUFF_ATK_PET)/100)

6. 4-SCENARIO RAW DAMAGE
   ├── Crit (CRIT_DMG=user, WEAK=0)
   ├── Crit + Weakness (CRIT_DMG=user, WEAK=30+WEAK_DMG)
   ├── No Crit (CRIT_DMG=100, WEAK=0)
   └── Weakness Only (CRIT_DMG=100, WEAK=30+WEAK_DMG)

7. EFFECTIVE DEF
   └── 1 + DEF_Modifier × DEF_Target × (1 + DEF_BUFF/100 - DEF_REDUCE/100)
                                       × (1 - Ignore_DEF/100)

8. FINAL DAMAGE
   └── ROUNDDOWN(RAW_DMG / Effective_DEF) × SKILL_HITS

9. OUTPUT
   ├── Standard: display 4 scenarios with kill status
   └── Special: registry handler takes over with custom logic
```

## Config Merge System

Three config layers are merged in order:

1. **Character config** — fixed values from `characters/[name].json` (passives, skill bonuses)
2. **Skill config** — values from the selected skill within the character JSON
3. **User config** — values from `config.json` (user's stats, enemy values)

### Additive Keys (values are SUMMED)

When a key appears in both character and user config, values are **added** (e.g., `SKILL_DMG`, `CRIT_DMG`, `WEAK_DMG`, etc.).

Example: Miho has passive `WEAK_DMG=23`. User config has `WEAK_DMG=35`. Final: `23 + 35 = 58`.

See [[docs/reference/config-reference]] for the full list of additive and mapping keys.

### Mapping Keys (redirected to another key)

| Source Key | Target Key | Example |
|-----------|-----------|---------|
| `Bonus_Crit_DMG` | `CRIT_DMG` | Teo: `85 + 288 = 373%` |

### Weapon Set Bonuses

Applied before merging, directly modifying the user config. See [[docs/reference/config-reference]] for full weapon set table.

## 4-Scenario System

Every character produces 4 damage outputs. This is the core of the calculator — players need to see best case, worst case, and everything in between.

| Scenario | CRIT_DMG | WEAK_DMG | Description |
|----------|----------|----------|-------------|
| Crit | User's value | 0 | Critical hit, no weakness |
| Crit + Weakness | User's value | 30 + WEAK_DMG | Best case: both modifiers |
| No Crit | 100% | 0 | Worst case: plain damage |
| Weakness Only | 100% | 30 + WEAK_DMG | Hit weakness but no crit |

The **30% base** is always added to weakness hits. This is the most common source of calculation errors.

## Special Character Branching

After step 8, the system checks the Registry:

```
handler = get_character_handler(char_name)
if handler:
    handled = handler(total_atk, skill_dmg, ...)
    if handled:
        return  # Special logic completed
# Fall through to standard 4-scenario display
```

Each handler may:
- Produce more than 4 scenarios (Espada: 8, Sun Wukong: iterates over crit counts)
- Use additional formulas (Freyja: HP Alteration, Biscuit: DEF-based damage)
- Display custom output formats

See [[docs/architecture/module-system]] for details on each registered handler.

---

Related: [[docs/architecture/module-system]] | [[docs/reference/formulas]] | [[docs/reference/config-reference]]
