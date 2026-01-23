"""
Sun Wukong Special Logic - Castle Mode Calculator
- โหมดตีปราสาท: คำนวณว่าต้องติดคริขั้นต่ำกี่ครั้งถึงมอนจะตาย
- สมมติ: hit ที่ไม่ติดคริ จะติดจุดอ่อนเสมอ
"""

from __future__ import annotations

from decimal import Decimal, ROUND_DOWN
from typing import Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from damage_calc import calculate_raw_dmg


def calculate_sun_wukong_castle_mode(
    total_atk: Decimal,
    skill_dmg: Decimal,
    crit_dmg: Decimal,
    weak_dmg: Decimal,
    dmg_amp_buff: Decimal,
    dmg_amp_debuff: Decimal,
    dmg_reduction: Decimal,
    eff_def: Decimal,
    skill_hits: int,
    hp_target: Decimal,
    skill_name: str,
    final_dmg_hp: Decimal = Decimal("0")
) -> dict[str, Any]:
    """
    คำนวณดาเมจ Sun Wukong แบบ Castle Mode:
    - คำนวณดาเมจต่อ hit แบบติดจุดอ่อนเท่านั้น (no crit)
    - คำนวณดาเมจต่อ hit แบบติดคริ+จุดอ่อน
    - คำนวณว่าต้องติดคริขั้นต่ำกี่ hit ถึงจะฆ่ามอนได้
    """
    
    # Base weakness (30%) + WEAK_DMG from config/character
    base_weakness = Decimal("30")
    total_weakness = base_weakness + weak_dmg
    
    # === ดาเมจติดจุดอ่อน (ไม่ติดคริ) ===
    # เมื่อไม่ติดคริ CRIT_DMG จะเป็น 100% (ตัวคูณ x1)
    raw_weak_only = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=Decimal("100"),  # ไม่ติดคริ = 100% (x1)
        weak_dmg=total_weakness,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=final_dmg_hp
    )
    dmg_weak_only_per_hit = int((raw_weak_only / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    # === ดาเมจติดคริ + จุดอ่อน ===
    raw_crit_weak = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=crit_dmg,
        weak_dmg=total_weakness,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=final_dmg_hp
    )
    dmg_crit_weak_per_hit = int((raw_crit_weak / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    # === หาจำนวนคริขั้นต่ำที่ต้องการ ===
    # สูตร: c ครั้งติดคริ + (n-c) ครั้งติดแค่จุดอ่อน >= HP_Target
    # c * dmg_crit + (n - c) * dmg_weak >= HP
    # c * (dmg_crit - dmg_weak) >= HP - n * dmg_weak
    # c >= (HP - n * dmg_weak) / (dmg_crit - dmg_weak)
    
    # === ดาเมจปกติ (ไม่คริ, ไม่จุดอ่อน) ===
    # WEAK_DMG = 0 (และไม่บวก base 30%), CRIT_DMG = 100%
    raw_normal = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=Decimal("100"),
        weak_dmg=Decimal("0"),  # ไม่ติดจุดอ่อนเลย
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=final_dmg_hp
    )
    dmg_normal_per_hit = int((raw_normal / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    # === หาจำนวนคริขั้นต่ำที่ต้องการ (2 กรณี) ===
    hp = int(hp_target)
    n = skill_hits
    
    # กรณี 1: Base Weakness (เดิม)
    # Fail = ติดจุดอ่อน (dmg_weak_only_per_hit)
    # Success = ติดคริ+จุดอ่อน (dmg_crit_weak_per_hit)
    min_crits_weak_base = -1
    can_kill_weak_base = False
    scenarios_weak_base = []
    
    for c in range(n + 1):
        fail_hits = n - c
        success_hits = c
        total_dmg = (success_hits * dmg_crit_weak_per_hit) + (fail_hits * dmg_weak_only_per_hit)
        is_kill = total_dmg >= hp
        
        scenarios_weak_base.append({
            "crit_count": c,
            "fail_hits": fail_hits, # Weak Only
            "total_damage": total_dmg,
            "is_kill": is_kill
        })
        
        if is_kill and min_crits_weak_base == -1:
            min_crits_weak_base = c
            can_kill_weak_base = True
            
    if not can_kill_weak_base and (n * dmg_crit_weak_per_hit) >= hp:
        can_kill_weak_base = True
        min_crits_weak_base = n

    # กรณี 2: Base Normal (ใหม่)
    # Fail = ไม่ติดอะไรเลย (dmg_normal_per_hit)
    # Success = ติดคริ+จุดอ่อน (dmg_crit_weak_per_hit) -> สมมติว่าถ้าคริ คือแม่นยำและเข้าจุดอ่อน
    min_crits_normal_base = -1
    can_kill_normal_base = False
    scenarios_normal_base = []
    
    for c in range(n + 1):
        fail_hits = n - c
        success_hits = c
        total_dmg = (success_hits * dmg_crit_weak_per_hit) + (fail_hits * dmg_normal_per_hit)
        is_kill = total_dmg >= hp
        
        scenarios_normal_base.append({
            "crit_count": c,
            "fail_hits": fail_hits, # Normal
            "total_damage": total_dmg,
            "is_kill": is_kill
        })
        
        if is_kill and min_crits_normal_base == -1:
            min_crits_normal_base = c
            can_kill_normal_base = True

    if not can_kill_normal_base and (n * dmg_crit_weak_per_hit) >= hp:
        can_kill_normal_base = True
        min_crits_normal_base = n
    
    return {
        "skill_name": skill_name,
        "skill_hits": skill_hits,
        "hp_target": hp,
        "dmg_normal_per_hit": dmg_normal_per_hit,
        "dmg_weak_only_per_hit": dmg_weak_only_per_hit,
        "dmg_crit_weak_per_hit": dmg_crit_weak_per_hit,
        "total_weakness": total_weakness,
        
        # Scenario 1: Weakness Base
        "min_crits_weak_base": min_crits_weak_base,
        "can_kill_weak_base": can_kill_weak_base,
        "scenarios_weak_base": scenarios_weak_base,
        
        # Scenario 2: Normal Base
        "min_crits_normal_base": min_crits_normal_base,
        "can_kill_normal_base": can_kill_normal_base,
        "scenarios_normal_base": scenarios_normal_base
    }


def print_castle_mode_results(results: dict[str, Any]) -> None:
    """แสดงผลลัพธ์ Castle Mode (2 Scenarios)"""
    
    skill_name = results["skill_name"]
    hits = results["skill_hits"]
    hp = results["hp_target"]
    dmg_normal = results["dmg_normal_per_hit"]
    dmg_weak = results["dmg_weak_only_per_hit"]
    dmg_crit = results["dmg_crit_weak_per_hit"]
    weakness = results["total_weakness"]
    
    print("\n" + "=" * 60)
    print(f"  🐵 Sun Wukong Castle Mode - {skill_name} 🏰")
    print("=" * 60)
    
    print(f"\n  📊 ข้อมูลทั่วไป")
    print(f"  🎯 Hits: {hits} | ❤️ HP: {hp:,}")
    print(f"  💧 Weakness: +{weakness}%")
    
    print("\n  📈 ดาเมจต่อ Hit")
    print(f"  1. ⚪ ปกติ (ไม่คริ/ไม่จุดอ่อน):   {dmg_normal:,}")
    print(f"  2. 🔵 จุดอ่อน (ไม่คริ):         {dmg_weak:,} (+{dmg_weak-dmg_normal:,})")
    print(f"  3. 🔴 คริ+จุดอ่อน (Max):       {dmg_crit:,} (+{dmg_crit-dmg_weak:,} from Weak)")
    
    # แสดงตารางเปรียบเทียบ
    print("\n" + "-" * 75)
    print("  🎲 ตารางเปรียบเทียบคริขั้นต่ำ (Minimum Crits Needed)")
    print("-" * 75)
    print(f"  {'คริ':>4} | {'[Case 1] Base=Weakness':^32} | {'[Case 2] Base=Normal':^32}")
    print(f"       | {'(Fail = 🔵 จุดอ่อน)':^32} | {'(Fail = ⚪ ปกติ)':^32}")
    print("-" * 75)
    
    scenarios_1 = results["scenarios_weak_base"]
    scenarios_2 = results["scenarios_normal_base"]
    min_1 = results["min_crits_weak_base"]
    min_2 = results["min_crits_normal_base"]
    kill_1 = results["can_kill_weak_base"]
    kill_2 = results["can_kill_normal_base"]
    
    for i in range(hits + 1):
        s1 = scenarios_1[i]
        s2 = scenarios_2[i]
        
        # Format S1
        d1 = s1["total_damage"]
        mark1 = "✅" if s1["is_kill"] else "❌"
        note1 = "🔥 MIN" if i == min_1 and kill_1 else ""
        text1 = f"{d1:,} {mark1} {note1}"
        
        # Format S2
        d2 = s2["total_damage"]
        mark2 = "✅" if s2["is_kill"] else "❌"
        note2 = "🔥 MIN" if i == min_2 and kill_2 else ""
        text2 = f"{d2:,} {mark2} {note2}"
        
        print(f"  {i:>4} | {text1:<32} | {text2:<32}")
        
    print("-" * 75)
    
    # สรุป
    print("\n  📝 สรุปผล (Conclusion)")
    
    # Case 1
    if kill_1:
        if min_1 == 0:
            msg1 = "ไม่ต้องคริเลย (แค่ติดจุดอ่อนก็ตาย)"
        else:
            msg1 = f"ต้องคริ {min_1} ครั้ง"
    else:
        msg1 = "คริทุกดอกก็ไม่ตาย (dmg ไม่พอ)"
        
    print(f"  🔵 Case 1 (ยืนจุดอ่อน): {msg1}")
    
    # Case 2
    if kill_2:
        if min_2 == 0:
            msg2 = "ไม่ต้องคริเลย (ดาเมจปกติพอฆ่าได้)"
        else:
            msg2 = f"ต้องคริ {min_2} ครั้ง"
    else:
        msg2 = "คริทุกดอกก็ไม่ตาย"
        
    print(f"  ⚪ Case 2 (หลุดจุดอ่อน): {msg2}")
    
    if kill_1 and kill_2 and min_2 > min_1:
         print(f"  ⚠️  ถ้าหลุดจุดอ่อน ต้องคริเพิ่มอีก {min_2 - min_1} ครั้ง")
         
    print("=" * 60)
