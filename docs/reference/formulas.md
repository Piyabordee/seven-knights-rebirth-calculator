# Damage Formulas Reference

> Core formulas used in the damage calculator, with known gotchas.
> Implementation: `calculator/damage_calc.py` and `calculator/constants.py`.

---

## Constants

| Constant | Value | Location |
|----------|-------|----------|
| `DEF_MODIFIER` | `0.00214135` | `constants.py` |
| `ATK_BASE` | Varies by rarity/class (1500 for Legend Magic) | `constants.py` |
| `DEF_BASE` | Varies by rarity/class (675 for Legend Support) | `constants.py` |
| `HP_BASE` | Varies by rarity/class | `constants.py` |
| Weakness Base | `30%` (always added to WEAK_DMG) | Hardcoded in `main.py` |

---

## 1. Total ATK

```
Total_ATK = (ATK_CHAR + ATK_PET + ATK_BASE × (Formation + Potential_PET) / 100)
            × (1 + (BUFF_ATK + BUFF_ATK_PET) / 100)
```

**Implementation:** `damage_calc.py` → `calculate_total_atk()`

Notes:
- Formation and Potential_PET are percentages (e.g., 42 means 42%)
- BUFF_ATK and BUFF_ATK_PET are multiplicative, not additive to the base

---

## 2. RAW Damage

```
RAW_DMG = (Total_ATK × SKILL_DMG/100 × CRIT_DMG/100
           × (1 + WEAK_DMG/100) × (1 + DMG_AMP_BUFF/100)
           × (1 + (DMG_AMP_DEBUFF - DMG_Reduction)/100))
          + (Final_DMG_HP × CRIT_DMG/100
             × (1 + WEAK_DMG/100) × (1 + DMG_AMP_BUFF/100)
             × (1 + (DMG_AMP_DEBUFF - DMG_Reduction)/100))
```

**Implementation:** `damage_calc.py` → `calculate_raw_dmg()`

Notes:
- The second term (`Final_DMG_HP × ...`) only applies to HP-Based characters (Espada, Yeonhee)
- `Final_DMG_HP` uses the same multipliers as the ATK portion, but without `SKILL_DMG`

---

## 3. HP-Based Damage

```
DMG_HP = HP_Target × Bonus_DMG_HP_Target / 100
Cap_ATK = Total_ATK × Cap_ATK_Percent / 100
Final_DMG_HP = ROUNDDOWN(MIN(DMG_HP, Cap_ATK))  [if Cap > 0]
             = DMG_HP                              [if Cap = 0]
```

**Implementation:** `damage_calc.py` → `calculate_dmg_hp()`, `calculate_cap_atk()`, `calculate_final_dmg_hp()`

---

## 4. Effective DEF

```
Effective_DEF = 1 + DEF_Modifier × DEF_Target
                × (1 + DEF_BUFF/100 - DEF_REDUCE/100)
                × (1 - Ignore_DEF/100)
```

**Implementation:** `damage_calc.py` → `calculate_effective_def()`

Notes:
- DEF_Modifier is the constant `0.00214135`
- This always produces a value >= 1.0 (acts as a divisor)
- DEF_REDUCE reduces the target's DEF (beneficial to attacker)
- Ignore_DEF is a percentage reduction of the entire DEF term

---

## 5. Final Damage

```
Final_DMG = ROUNDDOWN(RAW_DMG / Effective_DEF) × SKILL_HITS
```

**Implementation:** `damage_calc.py` → `calculate_final_dmg()`

---

## 6. Special Formulas

### HP Alteration (Freyja)
```
Damage = HP_Target × (100 - HP_Alteration) / 100
```
Not affected by DEF. Directly reduces target HP to X%.
**Implementation:** `logic/freyja.py` → `calculate_hp_alteration_damage()`

### Lost HP Bonus (Ryan)
```
lost_hp = 100 - Target_HP_Percent
bonus = Lost_HP_Bonus × lost_hp / 100
final_damage = base_damage × (1 + bonus/100)
```
Damage scales linearly with HP lost. Max bonus = Lost_HP_Bonus value.
**Implementation:** `logic/ryan.py` → `calculate_lost_hp_multiplier()`

### HP Condition Bonus (Klahan)
```
if HP >= 50%: SKILL_DMG += HP_Above_50_Bonus
if HP <= 50%: SKILL_DMG += HP_Below_50_Bonus
```
Modifies SKILL_DMG before the standard formula.
**Implementation:** `logic/klahan.py`

### Dual Scaling (Biscuit)
```
Total_DEF = DEF_CHAR + DEF_PET + (Base_DEF_Support × 10.5 / 100)
RAW_ATK = calculate_raw_dmg(Total_ATK, SKILL_DMG, ...)
RAW_DEF = calculate_raw_dmg(Total_DEF, SKILL_DMG_DEF, ...)
Final = Final_ATK + Final_DEF
```
Two separate RAW damage calculations, summed. DEF calculation skips HP-based component.
**Implementation:** `logic/biscuit.py` → `calculate_biscuit_damage()`

### Castle Mode (Sun Wukong)
```
For c crits out of n hits:
  total_dmg = (c × dmg_crit_weak) + ((n-c) × dmg_weak_only)
  if total_dmg >= HP_Target: kill achieved with c crits
```
Iterates over possible crit counts to find minimum.
**Implementation:** `logic/sun_wukong.py` → `calculate_sun_wukong_castle_mode()`

---

## Gotchas

### Weakness Base 30%
Weakness damage is **always** `30 + WEAK_DMG`, never just WEAK_DMG. The 30% base comes from the game's mechanic, not from any config value.

```python
# In main.py
total_weak_dmg = Decimal("30") + weak_dmg  # Always 30 + config value
```

### DMG_Reduction is in RAW step
DMG_Reduction is subtracted inside the RAW damage formula (paired with DMG_AMP_DEBUFF), **not** after dividing by Effective DEF. This means it's multiplicative with all other modifiers, not additive with DEF.

### Per-Hit, Not Total
`calculate_final_dmg()` returns **per-hit** damage. Multiply by `SKILL_HITS` to get total. Never divide by hits.

### ROUNDDOWN
All final values use `Decimal.quantize(Decimal("1"), rounding=ROUND_DOWN)`. This matches the game's behavior where `100.9` becomes `100`, not `101`.

---

Related: [[docs/architecture/damage-pipeline]] | [[docs/reference/config-reference]] | [[docs/architecture/module-system]]
