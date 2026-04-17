# Config Reference

> All configuration fields across config.json, character JSONs, and monster presets.
> Implementation: `calculator/config_loader.py`

---

## Config Merge Order

```
1. Character JSON (characters/[name].json) — fixed values, passives
2. Skill config (extracted from character JSON _skills section)
3. User config (config.json) — user's live stats
4. Monster preset (characters/monster/*.json) — overrides target values in Castle mode
5. Weapon set bonus — applied to user config before merge
```

Merge rules: additive keys are **summed**, mapping keys are **redirected**, user-only keys pass through unchanged.

---

## User Config (`config.json`)

Located at `calculator/config.json`. Edit this to match your in-game stats.

### Attack Stats

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `ATK_CHAR` | float | 4000 | Character's ATK stat shown in-game |
| `ATK_PET` | float | 371 | Pet's flat ATK bonus |
| `CRIT_DMG` | float | 256 | Critical Damage % (base 100% + bonus) |
| `Formation` | float | 21 | Formation ATK bonus % |
| `BUFF_ATK` | float | 0 | ATK buff % from skills/party |
| `BUFF_ATK_PET` | float | 17 | Pet ATK buff % |
| `Potential_PET` | float | 21 | Pet Potential ATK % |
| `DMG_AMP_BUFF` | float | 0 | Damage Amplification buff % (from ring) |

### Enemy Stats

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `DEF_Target` | float | 784 | Enemy DEF stat |
| `HP_Target` | float | 10790 | Enemy HP |
| `DMG_Reduction` | float | 0 | Enemy Damage Reduction % |
| `DEF_BUFF` | float | 0 | Enemy DEF buff % |
| `Target_HP_Percent` | float | 0 | HP% left (for Lost HP Bonus calculations) |

### Equipment

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `Weapon_Set` | int | 0-4 | Weapon set bonus (see below) |

| Weapon_Set | Name | Effect |
|-----------|------|--------|
| 0 | None | No bonus |
| 1 | Weakness | `WEAK_DMG += 35` |
| 2 | Crit | `Ignore_DEF += 15` |
| 3 | Hydra | `DMG_AMP_BUFF += 70` |
| 4 | Hydra Castle | `DMG_AMP_BUFF += 30` |

---

## Character JSON (`characters/[name].json`)

### Metadata Fields (prefix `_`)

These are filtered out during config loading and not used in calculations.

| Field | Example | Description |
|-------|---------|-------------|
| `_character` | "Biscuit" | Display name |
| `_rarity` | "legend" | Determines ATK_BASE value |
| `_class` | "support" | Determines ATK_BASE, DEF_BASE values |
| `_element` | "Dark" | Character element |
| `_source` | URL | GameWith data source |
| `_notes` | ["Enhanced"] | Notes about the data |
| `_skills` | Object | Skill definitions (see below) |

### Config Fields (used in calculations)

| Field | Type | Description |
|-------|------|-------------|
| `BUFF_ATK` | float | Character's ATK buff passive |
| `CRIT_DMG` | float | Bonus CRIT_DMG from character |
| `DMG_AMP_BUFF` | float | Character's DMG AMP buff |
| `DMG_AMP_DEBUFF` | float | Character's DMG AMP debuff on enemy |
| `WEAK_DMG` | float | Character's weakness damage bonus |
| `DEF_REDUCE` | float | Character's DEF reduction on enemy |
| `Ignore_DEF` | float | Character's DEF ignore % |

### Skill Fields (inside `_skills`)

| Field | Type | Description |
|-------|------|-------------|
| `_name` | string | Skill display name |
| `SKILL_DMG` | float | Skill damage multiplier % |
| `SKILL_HITS` | int | Number of hits |

### Special Fields (character-specific)

| Field | Character | Description |
|-------|-----------|-------------|
| `HP_Alteration` | Freyja | Target HP reduced to this % |
| `Lost_HP_Bonus` | Ryan | Max bonus % from lost HP |
| `WEAK_SKILL_DMG` | Ryan | Extra skill multiplier on weakness |
| `HP_Above_50_Bonus` | Klahan | SKILL_DMG bonus when HP >= 50% |
| `HP_Below_50_Bonus` | Klahan | SKILL_DMG bonus when HP <= 50% |
| `Bonus_DMG_HP_Target` | Espada, Yeonhee | % of target HP as damage |
| `Cap_ATK_Percent` | Espada, Yeonhee | Cap for HP-based damage as % of ATK |
| `Bonus_Crit_DMG` | Teo | Added to CRIT_DMG via mapping |
| `SKILL_DMG_DEF` | Biscuit | Skill multiplier for DEF-based damage |

---

## Monster Presets (`characters/monster/*.json`)

| File | DEF_Target | HP_Target | Mode |
|------|-----------|-----------|------|
| `castle_room1.json` | 689 | 8,650 | Castle Rush Room 1 |
| `castle_room2.json` | 784 | 10,790 | Castle Rush Room 2 |
| `normal.json` | varies | varies | Standard mode |

Monster presets override the matching fields from `config.json` when Castle Rush mode is selected.

---

## ATK_BASE Values (from `constants.py`)

Determined by character `_rarity` and `_class` from the character JSON.

| Rarity | Attack | Magic | Support | Defense | Balance |
|--------|--------|-------|---------|---------|---------|
| Legend | 1500 | 1500 | 1095 | 727 | 1306 |
| Rare | 1389 | 1389 | 1035 | 704 | 1238 |

---

## Additive Keys Reference

These keys are **summed** when merging character + user configs:

```
SKILL_DMG, CRIT_DMG, WEAK_DMG, DMG_AMP_BUFF, DMG_AMP_DEBUFF,
DEF_REDUCE, BUFF_ATK, DMG_Reduction, Ignore_DEF,
Bonus_DMG_HP_Target, Cap_ATK_Percent
```

## Mapping Keys Reference

These keys are **redirected** to a target key and added:

| Source | Target |
|--------|--------|
| `Bonus_Crit_DMG` | `CRIT_DMG` |

---

Related: [[docs/reference/formulas]] | [[docs/architecture/damage-pipeline]] | [[docs/architecture/module-system]] | [[GAMEWITH_GUIDE]]
