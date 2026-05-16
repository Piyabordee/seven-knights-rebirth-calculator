# Testing Strategy

> How the calculator is tested: approach, conventions, coverage goals, and test file map.
> For detailed test strategy, see `calculator/tests/TEST_STRATEGY.md`.

---

## When to Read This

**Trigger:** Writing new tests, debugging test failures, or understanding test coverage expectations.

**Read With:**
- `calculator/tests/TEST_STRATEGY.md` [[calculator/tests/TEST_STRATEGY]] — full test strategy with coverage matrix
- `docs/architecture/module-system.md` [[docs/architecture/module-system]] — module responsibilities

---

## Approach

The test suite prioritizes **formula accuracy** above all else. Damage values must match in-game numbers exactly — even small deviations indicate a bug.

Testing levels (by priority):

1. **Critical — Core formulas** (`test_damage_calc.py`): Every function in `damage_calc.py` tested in isolation with known inputs/outputs
2. **High — Config merging** (`test_config_and_characters.py`): Additive key summation, mapping keys, weapon set bonuses, character JSON loading
3. **High — Special character logic** (`test_all_logic.py`): Each of the 6 special characters tested with showcase-verified values
4. **Medium — Edge cases** (`test_edge_cases.py`): Zero values, extreme values, precision boundaries, rounding behavior

---

## Test File Map

| File | Tests | Priority |
|------|-------|----------|
| `calculator/tests/test_damage_calc.py` | Core formula functions | Critical |
| `calculator/tests/test_config_and_characters.py` | Config loading, merging, weapon sets | High |
| `calculator/tests/test_all_logic.py` | All 6 special character logic modules | High |
| `calculator/tests/test_edge_cases.py` | Boundary values, zero, overflow, precision | Medium |
| `calculator/tests/test_imports.py` | Module import validation | Low |
| `calculator/tests/conftest.py` | Shared fixtures | Infrastructure |

---

## Coverage Goals

| Module | Target | Priority |
|--------|--------|----------|
| `damage_calc.py` | 100% | Critical — formulas must be exact |
| `config_loader.py` | 80% | High — merging logic is error-prone |
| Special character logic | 80% | High — verified against showcases |
| `character_registry.py` | 60% | Medium — routing logic |
| `menu.py` / `display.py` | 10-20% | Low — I/O, cosmetic |

---

## Running Tests

```bash
pytest calculator/tests/ -v                     # All tests, verbose
pytest calculator/tests/ --cov=calculator       # With coverage report
pytest calculator/tests/test_damage_calc.py -v  # Core formulas only
pytest calculator/tests/test_edge_cases.py -v   # Edge cases only
```

---

## Conventions

- **Decimal in tests:** All numeric test values use `Decimal`, matching production code
- **Named test fixtures:** Shared setup in `conftest.py` (e.g., standard configs, character data)
- **Descriptive names:** `test_<function>_<scenario>` pattern
- **Showcase verification:** Special character tests use values from [[docs/SHOWCASES]] as expected outputs

---

Related: [[docs/architecture/module-system]] | [[docs/features/character-mechanics]] | [[docs/SHOWCASES]] | [[docs/reference/formulas]]
