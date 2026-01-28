# How to Extract Character Data from GameWith

This document explains how to extract values from [GameWith](https://gamewith.net/sevenknights-rebirth/) and convert them to character JSON files.

> **📌 For AI Agents:** This guide explains GameWith → JSON conversion for adding new characters.

---

## 🔄 Workflow: Adding New Characters (Modern Approach)

### High-Level Steps:

```
1. Extract data from GameWith
   ↓
2. Create JSON file in characters/
   ↓
3. Decide: Special Logic needed?
   ├─ No → Done (uses standard formula)
   └─ Yes → Create logic/[name].py
            ↓
         4. Register in character_registry.py
            ↓
         5. Update docs/SHOWCASES.md (if needed)
```

### Characters Requiring Special Logic:

| Mechanic | Example Character | Special Fields |
|----------|-----------------|----------------|
| HP Alteration | Freyja | `HP_Alteration` |
| Lost HP Bonus | Ryan | `Lost_HP_Bonus`, `WEAK_SKILL_DMG`, `Target_HP_Percent` |
| HP Condition Bonus | Klahan | `HP_Above_50_Bonus`, `HP_Below_50_Bonus` |
| HP-Based Damage | Espada, Yeonhee | `Bonus_DMG_HP_Target`, `Cap_ATK_Percent` |
| Dual Scaling (ATK+DEF) | Biscuit | `SKILL_DMG_DEF`, `DEF_CHAR`, `DEF_PET` |
| Castle Mode | Sun Wukong | Special min crits calculation |

---

## 📋 Character JSON Structure Pattern

### Standard structure for character files (characters/*.json)

```json
{
    "// ===== Metadata (prefixed with _) =====": "",
    "_character": "Character Name",
    "_rarity": "legend",
    "_class": "magic | balance | defense | warrior",
    "_source": "Reference URL (GameWith)",
    "_element": "Fire | Water | Earth | Light | Dark",

    "// ===== Passive Skills (applies to all skills) =====": "",
    "BUFF_ATK": 0.00,
    "CRIT_DMG": 0.00,
    "WEAK_DMG": 0.00,
    "DMG_AMP_BUFF": 0.00,

    "// ===== Skills =====": "",
    "_skills": {
        "skill2": {
            "_name": "Top Skill Name (English)",
            "SKILL_DMG": 0.00,
            "SKILL_HITS": 1,
            "Ignore_DEF": 0.00,
            "Bonus_DMG_HP_Target": 0.00,
            "Cap_ATK_Percent": 0.00,
            "DEF_REDUCE": 0.00,
            "DMG_AMP_DEBUFF": 0.00
        },
        "skill1": {
            "_name": "Bottom Skill Name (English)",
            "SKILL_DMG": 0.00,
            "SKILL_HITS": 1,
            "Ignore_DEF": 0.00,
            "Bonus_DMG_HP_Target": 0.00,
            "Cap_ATK_Percent": 0.00
        }
    },

    "// ===== Notes =====": "",
    "_notes": [
        "Additional info like ATK_BASE, Transcend values"
    ]
}
```

### Usage Rules:

1. **Metadata** (prefixed with `_`): Not used in calculations, reference only
2. **Passive Skills**: Values applied to all skills (outside `_skills`)
3. **Skills**: Separate `skill1` (bottom) and `skill2` (top)
4. **Default values**: Use `0.00` if skill doesn't have a specific value
5. **Value merging**: Calculator ADDs values (Character Passive + Skill + User Config)
6. **Always use Enhanced values**: Use post-Skill Enhancement values (e.g. 470% instead of 390%)

---

## URL Pattern

```
https://gamewith.net/sevenknights-rebirth/[ID]
```

Example: Miho = `https://gamewith.net/sevenknights-rebirth/70610`

---

## Values to Extract from GameWith Skill Page

### Skill Properties (place in `_skills.skill1` or `_skills.skill2`)

| GameWith Text | Variable | Example |
|----------------|----------|---------|
| "Deals damage equal to **X%** of [Type] Attack **N time(s)**" | `SKILL_DMG`, `SKILL_HITS` | 55%, 3 hits |
| "Additional damage equal to **X%** upon Weakness Hit" | Add to `WEAK_DMG` (in skill) | 85% |
| "Ignores **X%** of the enemy's Defense" | `Ignore_DEF` | 40% |
| "Deals additional damage equal to **X%** of target's Max HP" | `Bonus_DMG_HP_Target` | 7% |
| "(Capped at **X%** of Attack)" | `Cap_ATK_Percent` | 100% |
| "Defense Reduction by **X%**" | `DEF_REDUCE` | 29% |
| "Physical/Magic Vulnerability by **X%**" | `DMG_AMP_DEBUFF` | 22% |

### Passive Properties (place outside `_skills`)

| GameWith Text | Variable | Example |
|----------------|----------|---------|
| "Attack Boost by **X%**" | `BUFF_ATK` | 25% |
| "Weakness Hit Damage Boost by **X%**" | `WEAK_DMG` | 23% |
| "Magic/Physical Damage Boost by **X%**" | `DMG_AMP_BUFF` | 35% |
| "Crit Damage Boost by **X%**" | `CRIT_DMG` | 40% |
| "Bonus Crit Damage Boost by **X%**" | `Bonus_Crit_DMG` | 85% (Auto-maps to `CRIT_DMG`) |

> **⚠️ Important:** `Bonus_Crit_DMG` is automatically auto-added to `CRIT_DMG` (no special logic needed)

---

## Values to Assume/Fill In

| Variable | Source |
|--------|--------|
| `ATK_CHAR` | Character stats page |
| `ATK_PET` | Pet page |
| `CRIT_DMG` | Stats + Gear |
| `DEF_Target` | Boss/Enemy data |
| `Ignore_DEF` | Stats + Gear |
| `DMG_AMP_BUFF` | Ring, Leader Skill, Buffs from others |

---

## Examples: Converting GameWith → JSON

### Yeonhee (Standard Example)

**From GameWith:**
```
Passive: Otherworldly Insight
- Attack Boost by 25% for 3 turn(s)

Skill 2: Eternal Slumber
- Deals damage equal to 55% of Magic Attack 3 time(s)
- Ignores 40% of the enemy's Defense

Skill 1: Calamitous Gesture
- Deals damage equal to 51% of Magic Attack 3 time(s)
- Deals additional damage equal to 7% of target's Max HP
  (Capped at 100% of Attack)
```

**Convert to yeonhee.json:**
```json
{
    "_character": "Yeonhee",
    "_rarity": "legend",
    "_class": "magic",
    "_element": "Dark",
    "BUFF_ATK": 25.00,
    "_skills": {
        "skill2": {
            "_name": "Eternal Slumber (Top)",
            "SKILL_DMG": 55.00,
            "SKILL_HITS": 3,
            "Ignore_DEF": 40.00,
            "Bonus_DMG_HP_Target": 0.00,
            "Cap_ATK_Percent": 0.00
        },
        "skill1": {
            "_name": "Calamitous Gesture (Bottom)",
            "SKILL_DMG": 51.00,
            "SKILL_HITS": 3,
            "Ignore_DEF": 0.00,
            "Bonus_DMG_HP_Target": 7.00,
            "Cap_ATK_Percent": 100.00
        }
    }
}
```

---

## 🌟 Special Mechanics Examples

Examples of characters with special mechanics requiring additional logic:

### Biscuit - Dual Scaling (ATK + DEF)

**GameWith:**
```
Skill 2: Leap Attack
- Deals damage equal to 115% of Magic Attack 1 time(s)
- Additional damage equal to 135% of Defense
```

**JSON:**
```json
{
    "_character": "Biscuit",
    "_rarity": "legend",
    "_class": "support",
    "_element": "Dark",
    "_skills": {
        "skill2": {
            "_name": "Leap Attack (Top)",
            "SKILL_DMG": 115.00,
            "SKILL_HITS": 1,
            "SKILL_DMG_DEF": 135.00
        }
    },
    "_notes": [
        "Dual Scaling: Calculates ATK part + DEF part separately",
        "DEF part uses SKILL_DMG_DEF (135%)",
        "System prompts for DEF_CHAR and DEF_PET during calculation"
    ]
}
```

**Action:** Handler already exists in `character_registry.py`

---

### Freyja - HP Alteration

**GameWith:**
```
Passive: Queen's Authority
- Reduces target's HP to 39%
```

**JSON:**
```json
{
    "_character": "Freyja",
    "_rarity": "legend",
    "_class": "magic",
    "_element": "Light",
    "HP_Alteration": 39.00,
    "_notes": [
        "HP Alteration: Directly reduces target HP to X%",
        "Damage = HP_Target × (100 - HP_Alteration) / 100",
        "Logic in logic/freyja.py"
    ]
}
```

**Action:** Handler already exists in `character_registry.py`

---

### Ryan - Lost HP Bonus

**GameWith:**
```
Passive: Gale Slash
- Increases damage based on target's lost HP
- Max bonus: +50%
- Additional damage upon Weakness Hit: +270%
```

**JSON:**
```json
{
    "_character": "Ryan",
    "_rarity": "legend",
    "_class": "attack",
    "_element": "Dark",
    "Lost_HP_Bonus": 50.00,
    "WEAK_SKILL_DMG": 270.00,
    "_notes": [
        "Lost HP Bonus: Damage increases as target loses HP",
        "Max bonus at 50% when target HP ≤ 50%",
        "Weakness Extra: Additional damage on weakness hit",
        "Logic in logic/ryan.py"
    ]
}
```

**Action:** Handler already exists in `character_registry.py`

---

## Additional Examples (Standard Characters)

### Miho Skill 2: Overconfident Blow

**From GameWith:**
```
Passive: Opportunist
- Weakness Hit Damage Boost by 23%

Skill 2: Overconfident Blow
- Deals damage equal to 160% of Magic Attack 1 time(s)
- Increases Damage: To 185% of Magic Attack
- Adds Damage: Deals additional damage equal to 85% upon Weakness Hit

Skill 1: Violent Dance
- Magic Vulnerability by 22% for 2 turn(s)
```

**Convert to miho.json:**
```json
{
    "_character": "Miho",
    "_rarity": "legend",
    "_class": "magic",
    "_element": "Dark",
    "WEAK_DMG": 23.00,
    "_skills": {
        "skill2": {
            "_name": "Overconfident Blow (Top)",
            "SKILL_DMG": 160.00,
            "SKILL_HITS": 1,
            "Ignore_DEF": 0.00
        },
        "skill1": {
            "_name": "Violent Dance (Bottom)",
            "SKILL_DMG": 0.00,
            "SKILL_HITS": 1,
            "DMG_AMP_DEBUFF": 22.00
        }
    },
    "_notes": [
        "Skill 2: 160% → 185% (Transcend), +85% on Weakness"
    ]
}
```

---

## 🎯 AI Agent Instructions

### When Adding New Characters:

1. **Check character mechanics:**
   - Read skill descriptions from GameWith carefully
   - Any HP Alteration, Lost HP Bonus, HP Condition, Dual Scaling?

2. **For Standard Characters (no special logic):**
   - Create JSON following template above
   - Fill in all values found in GameWith
   - Done! (Nothing else needed)

3. **For Special Mechanics (must create logic):**
   - Create JSON with special fields
   - Create `logic/[name].py` file
   - Implement handler function
   - Register in `character_registry.py` with `@register_character("name")`
   - Update `AGENTS.md` and `docs/SHOWCASES.md`

4. **Verify correctness:**
   - Run `python test_all_characters.py` to test
   - Check handler is called correctly

---

## Tips & Tricks

1. **Always use Enhanced values**: Use post-Skill Enhancement values (the "Increases to X%" value) as primary value in JSON
   - ✅ Correct: `"SKILL_DMG": 470.00` (Enhanced)
   - ❌ Wrong: `"SKILL_DMG": 390.00` (Base)
   - Note: `"*** All values are Enhanced ***"`

2. **Transcend Effects**: If there are special values from Transcendence (T2, T4, T6), note them in `_notes`
   - Example: "T6: Crit Rate +100%", "T4: +24% Crit Damage"

3. **Debuff Skills**: If skill is buff/debuff only (no damage), use `SKILL_DMG: 0.00`

4. **Weakness Bonus**: If there's "Additional damage upon Weakness Hit", note as `WEAK_SKILL_DMG` (for characters with special logic)

5. **Element Advantage**: Don't include in JSON (calculated separately)

6. **NEW: Registry Pattern**: After refactor, no need to modify `main.py` to add new characters
   - Simply register in `character_registry.py`
   - System will find handler automatically

7. **Test Suite**: Use `test_all_characters.py` to verify character works correctly

> **Note:** "Increases Damage: To 185%" means post-Transcend value, use that value if Transcended

---

## 📚 References

- **AGENTS.md** - Main documentation for AI Agents
- **calculator/character_registry.py** - Registry pattern implementation
- **calculator/logic/** - Special logic examples
