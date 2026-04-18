# Project Overview

> What the 7k Rebirth Damage Calculator is, why it exists, and how it was built.

---

## Identity

| Field | Value |
|-------|-------|
| Name | 7k Rebirth Damage Calculator |
| Version | 2.2.0 |
| Type | CLI application (interactive menu-driven) |
| Stack | Python 3.10+ (stdlib only — no runtime dependencies) |
| Precision | `decimal.Decimal` for all mathematical operations |
| License | MIT |

## Purpose

A precision damage calculator for the mobile game *Seven Knights Rebirth*. It reverse-engineers the game's damage formulas to compute exact output values that match in-game numbers.

Target users: end-game players optimizing damage, guild strategists planning Castle Rush clears, and theorycrafters testing "what-if" scenarios.

## Modes

| Mode | Description |
|------|-------------|
| Standard | Uses local `config.json` for enemy/target values |
| Castle Rush | Loads monster presets (Room 1/2) with fixed DEF/HP |
| ATK Compare | Compares Total ATK between two configurations |

## Characters

11 supported characters. 6 have special damage mechanics requiring dedicated logic; 5 use the standard calculation pipeline.

| Character | Mechanic |
|-----------|----------|
| Biscuit | Dual Scaling (ATK + DEF) |
| Espada | HP-Based multi-scenario |
| Freyja | HP Alteration |
| Klahan | HP Condition Bonus |
| Ryan | Lost HP Bonus + Weakness Extra |
| Sun Wukong | Castle Mode (minimum crits) |
| Miho, Pascal, Rachel, Teo, Yeonhee | Standard formula with passive bonuses |

## Development Context

This project was built with ~90% AI assistance. The human author handles game mechanics research, logic formulation, and result verification. AI handles code architecture, implementation, refactoring, and documentation.

See [[docs/_index]] for full documentation including formulas, patterns, and extension instructions.

---

Related: [[docs/_index]] | [[docs/architecture/module-system]] | [[README]]
