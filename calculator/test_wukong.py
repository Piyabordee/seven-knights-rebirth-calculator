"""Test Sun Wukong Castle Mode"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from decimal import Decimal
from logic.sun_wukong import calculate_sun_wukong_castle_mode, print_castle_mode_results
from damage_calc import (
    calculate_total_atk, 
    calculate_effective_def,
    calculate_dmg_hp,
    calculate_cap_atk,
    calculate_final_dmg_hp
)
from constants import ATK_BASE

# Config values from config.json
atk_char = Decimal("3927")
atk_pet = Decimal("564")
formation = Decimal("42")
potential_pet = Decimal("27")
buff_atk_pet = Decimal("21")
crit_dmg = Decimal("258")
def_target = Decimal("1461")
hp_target = Decimal("18205")
dmg_reduction = Decimal("10")

# Sun Wukong is Balance class - use ATK_BASE from "support" (1095) based on character file
atk_base = Decimal("1095")  # Balance class

# Calculate Total ATK
total_atk = calculate_total_atk(
    atk_char=atk_char,
    atk_pet=atk_pet,
    atk_base=atk_base,
    formation=formation,
    potential_pet=potential_pet,
    buff_atk=Decimal("0"),
    buff_atk_pet=buff_atk_pet
)

print(f"Total ATK: {total_atk}")

# Skill 2 (Castle Mode): Jumbo Pole: Specter
skill_dmg = Decimal("102")
skill_hits = 3
ignore_def = Decimal("40")  # Skill's Ignore DEF
weapon_set_ignore = Decimal("15")  # Crit set bonus
total_ignore_def = ignore_def + weapon_set_ignore

# HP-based damage
bonus_dmg_hp_target = Decimal("7")
cap_atk_percent = Decimal("100")

hp_dmg = calculate_dmg_hp(hp_target, bonus_dmg_hp_target)
cap = calculate_cap_atk(total_atk, cap_atk_percent)
final_dmg_hp = calculate_final_dmg_hp(hp_dmg, cap)

print(f"HP-based DMG: {hp_dmg} (cap: {cap}) -> Final: {final_dmg_hp}")

# Effective DEF
eff_def = calculate_effective_def(
    def_target=def_target,
    def_buff=Decimal("0"),
    def_reduce=Decimal("0"),
    ignore_def=total_ignore_def
)

print(f"Effective DEF: {eff_def}")

# Calculate Castle Mode
results = calculate_sun_wukong_castle_mode(
    total_atk=total_atk,
    skill_dmg=skill_dmg,
    crit_dmg=crit_dmg,
    weak_dmg=Decimal("0"),  # No WEAK_DMG from char/config
    dmg_amp_buff=Decimal("0"),
    dmg_amp_debuff=Decimal("0"),
    dmg_reduction=dmg_reduction,
    eff_def=eff_def,
    skill_hits=skill_hits,
    hp_target=hp_target,
    skill_name="Jumbo Pole: Specter (skill2)",
    final_dmg_hp=final_dmg_hp
)

print_castle_mode_results(results)
