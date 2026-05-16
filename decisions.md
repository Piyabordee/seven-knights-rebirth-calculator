# Design Decisions Log

> Persistent record of key design choices, their rationale, and what to preserve when changing them.
> Add entries here when making non-obvious architectural or behavioral decisions.

---

## D001: Decimal over Float for Damage Math

**Decision:** Use `decimal.Decimal` for all mathematical operations in the calculator.

**Rationale:** The game's damage formulas are integer-based. Floating-point arithmetic produces precision drift (e.g., `0.1 + 0.2 != 0.3` in float). Since players verify calculator output against in-game numbers, any drift is a correctness failure. `Decimal` provides exact decimal arithmetic at the cost of verbosity.

**Tradeoff accepted:** Slower computation and more verbose code vs. exact precision. Performance is irrelevant for this CLI tool (single calculation at a time).

**Preserve when:** Any future refactor or optimization must not introduce `float` in the calculation pipeline. Display formatting may use string conversion, but all math stays `Decimal`.

---

## D002: Registry Pattern for Character Logic

**Decision:** Character-specific logic is handled via a Registry Pattern (`@register_character` decorator) rather than if/elif chains in `main.py`.

**Rationale:** Adding new characters with special mechanics previously required modifying `main.py`, increasing merge conflict risk and coupling. The Registry Pattern isolates each character's logic in its own module (`logic/[name].py`) while keeping `main.py` stable.

**Tradeoff accepted:** More files and indirection vs. a single dispatch function. The tradeoff favors maintainability since characters are added independently.

**Preserve when:** New characters with special logic must create a `logic/[name].py` and register via decorator. Do not add conditional branching to `main.py`.

---

## D003: Additive Config Merge

**Decision:** Config keys like `SKILL_DMG`, `CRIT_DMG`, `WEAK_DMG` are **summed** (character value + user value) rather than overwritten.

**Rationale:** The game's damage system stacks character passives with equipment/buff values additively. If Miho has `WEAK_DMG=23` passive and the user equips `WEAK_DMG=35` weapon, the result is `23 + 35 = 58`. Overwriting would lose the passive.

**Tradeoff accepted:** The merge logic must maintain an explicit list of additive keys (see `config_loader.py`). Non-additive keys pass through from user config.

**Preserve when:** Adding new config keys must determine whether they are additive (sum) or passthrough. Add additive keys to the `additive_keys` list in `merge_configs()`.

---

## D004: 4-Scenario Damage Output

**Decision:** Every calculation produces 4 damage outputs: Crit, Crit+Weakness, No Crit, Weakness Only.

**Rationale:** Players need to see best case, worst case, and all combinations to make informed decisions about equipment and strategy. The game's combat system has independent crit and weakness rolls, making all 4 scenarios equally likely.

**Preserve when:** Any new calculation mode must produce these 4 scenarios unless the character's mechanic explicitly replaces them (e.g., Sun Wukong's Castle Mode).

---

## D005: Windows Thai Encoding in main.py Only

**Decision:** UTF-8 wrapping of stdout/stdin is only in `main.py`'s `__main__` block, not in other modules.

**Rationale:** The calculator uses Thai text in its CLI output. Windows console defaults to a locale-specific encoding that breaks Thai characters. Wrapping in `__main__` ensures it only applies when running as a script, not when modules are imported for testing.

**Preserve when:** Do not add encoding wrappers to other modules. If the project adds a GUI, the encoding wrapper stays in the CLI entry point only.

---

## D006: Stdlib-Only Runtime

**Decision:** No runtime dependencies — the calculator uses only Python stdlib.

**Rationale:** Target users are game players, not developers. Requiring `pip install` of dependencies is a barrier. A single `python main.py` should work on any Python 3.10+ installation.

**Tradeoff accepted:** Manual JSON handling instead of pydantic, manual Decimal formatting instead of libraries. Dev dependencies (pytest, black, mypy, ruff) are acceptable since only developers run tests.

**Preserve when:** Do not add runtime dependencies to the calculator without strong justification and user approval.

---

Related: [[CLAUDE]] | [[docs/architecture/module-system]] | [[docs/reference/formulas]]
