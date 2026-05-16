# GameWith Data Sourcing

> How character data flows from the GameWith website into the calculator's JSON files.
> For the full extraction guide, see [[GAMEWITH_GUIDE]].

---

## When to Read This

**Trigger:** Adding a new character, updating an existing character's stats, or understanding why a character's data might be wrong.

**Read With:**
- `GAMEWITH_GUIDE.md` [[GAMEWITH_GUIDE]] — step-by-step extraction instructions
- `docs/reference/config-reference.md` [[docs/reference/config-reference]] — field names and types

---

## Data Pipeline

```
GameWith website
    │
    ▼  Manual extraction (see [[GAMEWITH_GUIDE]])
    │
Character stats (passives, skills, special fields)
    │
    ▼  Manual JSON creation
    │
calculator/characters/[name].json
    │
    ▼  config_loader.py loads at runtime
    │
Merged into damage calculation
```

## Why GameWith

[GameWith](https://gamewith.net/sevenknights-rebirth/) is the primary data source because:
- Maintains up-to-date character stats after game patches
- Provides structured data (passive values, skill multipliers, special effects)
- Covers all character rarities and classes

The calculator's accuracy depends on correct data extraction. A single wrong passive value propagates through the entire damage formula.

## Character JSON Structure

Each `characters/[name].json` file contains:

- **Metadata** (prefix `_`): `_character`, `_rarity`, `_class`, `_element`, `_skills`, `_source`
- **Config fields**: passive bonuses (`WEAK_DMG`, `CRIT_DMG`, `DMG_AMP_BUFF`, etc.)
- **Skill definitions**: inside `_skills` object with `_name`, `SKILL_DMG`, `SKILL_HITS`
- **Special fields**: character-specific fields like `HP_Alteration`, `Lost_HP_Bonus`

See [[docs/reference/config-reference]] for the complete field reference.

## Data Verification

After creating or updating a character JSON:
1. Run the calculator and compare output against in-game screenshots
2. Cross-reference with [[docs/SHOWCASES]] for known-good values
3. Run `pytest calculator/tests/` to catch config loading errors

---

Related: [[GAMEWITH_GUIDE]] | [[docs/reference/config-reference]] | [[docs/SHOWCASES]] | [[docs/architecture/module-system]]
