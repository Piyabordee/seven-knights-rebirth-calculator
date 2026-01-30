# Test Suite Documentation

This directory contains all test files for the 7k Rebirth Damage Calculator.

## 📁 Test Files

### `test_imports.py`
**Purpose:** Verify that all imports resolve correctly without `sys.path` manipulation

**What it tests:**
- Imports from `logic/` module (biscuit, espada, freyja, ryan)
- Imports from `damage_calc.py` (all calculation functions)
- Imports from `constants.py` (DEF_BASE constant)

**Expected Result:**
```
✅ All imports successful
   DEF_BASE['legend']['support'] = 675
```

**How to run:**
```bash
python calculator/tests/test_imports.py
```

---

### `test_all_logic.py`
**Purpose:** Comprehensive verification of all character logic matches showcase outputs

**What it tests:**

1. **Biscuit - DEF_BASE Import**
   - Verifies DEF_BASE['legend']['support'] = 675
   - Verifies formation bonus calculation (675 × 10.5 / 100 = 70.875)

2. **Biscuit - Full Damage Calculation**
   - Tests ATK part and DEF part separately
   - Verifies Total DEF calculation
   - Confirms dual scaling mechanics

3. **Freyja - HP Alteration**
   - HP Target: 100,000,000
   - HP Alteration: 39% (HP left at 39%)
   - **Expected Damage: 61,000,000** (must match exactly)

4. **Espada - HP-Based Damage**
   - Tests 4 scenarios: Crit/Weakness × With/Without HP
   - Verifies HP-based damage calculation
   - Confirms cap mechanics work

5. **Ryan - Lost HP Bonus**
   - Lost HP Bonus: 50% (max)
   - Target HP: 30% left
   - **Expected Bonus: +35%** (50% × (100-30)/100)

**Expected Output Summary:**
```
TEST 1: ✅ Match: True (70.875)
TEST 2: ✅ Biscuit calculation completed
TEST 3: ✅ Match: True (61,000,000)
TEST 4: ✅ Espada calculation completed
TEST 5: ✅ Ryan calculation completed
ALL TESTS COMPLETED SUCCESSFULLY
```

**How to run:**
```bash
python calculator/tests/test_all_logic.py
```

---

## 🧪 Running All Tests

Run both tests sequentially:
```bash
python calculator/tests/test_imports.py
python calculator/tests/test_all_logic.py
```

---

## ✅ Expected Test Results

| Test | Status | Verification |
|------|--------|--------------|
| Imports | ✅ PASS | All imports resolve without errors |
| Biscuit DEF_BASE | ✅ PASS | DEF_BASE['legend']['support'] = 675 |
| Biscuit Calculation | ✅ PASS | ATK + DEF dual scaling works |
| Freyja HP Alteration | ✅ PASS | Exactly 61,000,000 damage |
| Espada HP-Based | ✅ PASS | All 4 scenarios calculate correctly |
| Ryan Lost HP | ✅ PASS | Bonus = +35% (50% × 70%) |

---

## 📊 Verification Against Showcase

All test values must match the examples in `docs/SHOWCASES.md`:

- **Freyja HP Alteration:** 61,000,000 → ✅ PASS
- **Biscuit DEF Calculation:** Formation bonus = 70.875 → ✅ PASS
- **Ryan Lost HP Bonus:** +35% damage at 30% HP → ✅ PASS

---

## 🔍 Debugging Failed Tests

If a test fails:

1. **Import Errors:**
   - Check file structure is correct
   - Verify Python version is 3.10+
   - Ensure `__init__.py` exists in test directory

2. **Calculation Errors:**
   - Check formula in `damage_calc.py`
   - Verify constants in `constants.py`
   - Compare with `docs/SHOWCASES.md` expected values
   - Check Decimal precision (use `Decimal`, not `float`)

3. **Logic Errors:**
   - Check character-specific logic in `logic/*.py`
   - Verify registry registration in `character_registry.py`
   - Check config merging in `config_loader.py`

---

## 📝 Adding New Tests

When adding a new character:

1. Create test case in `test_all_logic.py`
2. Test all special mechanics (HP-based, Lost HP, etc.)
3. Verify against `docs/SHOWCASES.md`
4. Run `test_imports.py` to ensure new imports work
5. Run `test_all_logic.py` to verify logic

---

## 🚨 Important Notes

- **No `sys.path` manipulation:** Tests use proper Python imports
- **Decimal precision:** All math uses `Decimal` type
- **Registry Pattern:** Characters must be registered to work
- **Type Hints:** All test code is type-annotated