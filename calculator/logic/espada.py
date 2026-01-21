"""
Espada Special Logic
เนื่องจาก Espada มี HP-based damage ที่ต้องคำนวณแยกและเปรียบเทียบ
"""

from decimal import Decimal
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from damage_calc import (
    calculate_total_atk,
    calculate_dmg_hp,
    calculate_cap_atk,
    calculate_final_dmg_hp,
    calculate_raw_dmg,
    calculate_effective_def,
    calculate_final_dmg,
)


def calculate_espada_damage(
    total_atk, skill_dmg, crit_dmg, weak_dmg,
    dmg_amp_buff, dmg_amp_debuff, dmg_reduction,
    effective_def, hp_target, bonus_dmg_hp, cap_atk_percent
):
    """
    คำนวณดาเมจของ Espada แบบพิเศษ
    - คำนวณ 2 กรณี: (1) ดาเมจปกติ (2) ดาเมจ HP-based
    - แสดงผลทั้ง 4 กรณี
    """
    
    # 1. HP-based damage
    dmg_hp = calculate_dmg_hp(hp_target, bonus_dmg_hp)
    cap_atk = calculate_cap_atk(total_atk, cap_atk_percent)
    final_dmg_hp = calculate_final_dmg_hp(dmg_hp, cap_atk)
    
    # 2. คริ ไม่มี HP-based
    raw_dmg_crit_no_hp = calculate_raw_dmg(
        total_atk, skill_dmg, crit_dmg, Decimal("0"),
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, Decimal("0")
    )
    final_dmg_crit_no_hp = calculate_final_dmg(raw_dmg_crit_no_hp, effective_def)
    
    # 3. คริ + HP-based
    raw_dmg_crit_with_hp = calculate_raw_dmg(
        total_atk, skill_dmg, crit_dmg, Decimal("0"),
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, final_dmg_hp
    )
    final_dmg_crit_with_hp = calculate_final_dmg(raw_dmg_crit_with_hp, effective_def)
    
    # 4. จุดอ่อน (30% base + weak_dmg) ไม่มี HP-based
    total_weak_dmg = Decimal("30") + weak_dmg
    raw_dmg_weak_no_hp = calculate_raw_dmg(
        total_atk, skill_dmg, crit_dmg, total_weak_dmg,
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, Decimal("0")
    )
    final_dmg_weak_no_hp = calculate_final_dmg(raw_dmg_weak_no_hp, effective_def)
    
    # 5. จุดอ่อน + HP-based
    raw_dmg_weak_with_hp = calculate_raw_dmg(
        total_atk, skill_dmg, crit_dmg, total_weak_dmg,
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, final_dmg_hp
    )
    final_dmg_weak_with_hp = calculate_final_dmg(raw_dmg_weak_with_hp, effective_def)
    
    return {
        "dmg_hp": dmg_hp,
        "cap_atk": cap_atk,
        "final_dmg_hp": final_dmg_hp,
        "crit_no_hp": {
            "raw": raw_dmg_crit_no_hp,
            "final": final_dmg_crit_no_hp
        },
        "crit_with_hp": {
            "raw": raw_dmg_crit_with_hp,
            "final": final_dmg_crit_with_hp
        },
        "weak_no_hp": {
            "raw": raw_dmg_weak_no_hp,
            "final": final_dmg_weak_no_hp
        },
        "weak_with_hp": {
            "raw": raw_dmg_weak_with_hp,
            "final": final_dmg_weak_with_hp
        }
    }
