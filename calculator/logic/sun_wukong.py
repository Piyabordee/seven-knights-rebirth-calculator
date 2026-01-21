"""
Sun Wukong Special Logic - Castle Mode Calculator
- โหมดตีปราสาท: คำนวณว่าต้องติดคริขั้นต่ำกี่ครั้งถึงมอนจะตาย
- สมมติ: hit ที่ไม่ติดคริ จะติดจุดอ่อนเสมอ
"""

from decimal import Decimal, ROUND_DOWN
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
) -> dict:
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
    
    hp = int(hp_target)
    n = skill_hits
    dmg_weak = dmg_weak_only_per_hit
    dmg_crit = dmg_crit_weak_per_hit
    
    # ดาเมจรวมถ้าติดแต่จุดอ่อน (0 crit)
    total_weak_only = dmg_weak * n
    
    # ดาเมจรวมถ้าติดคริทุก hit (ติดจุดอ่อนด้วยทุก hit)
    total_all_crit = dmg_crit * n
    
    # หาจำนวนคริขั้นต่ำ
    # สมมติ: ทุก hit ติดจุดอ่อน แต่บาง hit ติดคริด้วย
    # c hit = ติดจุดอ่อน+คริ (dmg_crit)
    # (n-c) hit = ติดแค่จุดอ่อน (dmg_weak)
    min_crits_needed = -1  # -1 = ไม่ต้องคริเลย
    can_kill = False
    damage_scenarios = []
    
    for c in range(n + 1):
        weak_only_hits = n - c  # hit ที่ติดแค่จุดอ่อน
        crit_weak_hits = c      # hit ที่ติดคริ+จุดอ่อน
        total_dmg = (crit_weak_hits * dmg_crit) + (weak_only_hits * dmg_weak)
        is_kill = total_dmg >= hp
        
        damage_scenarios.append({
            "crit_count": c,
            "weak_count": n,  # ทุก hit ติดจุดอ่อน
            "total_damage": total_dmg,
            "is_kill": is_kill
        })
        
        if is_kill and min_crits_needed == -1:
            min_crits_needed = c
            can_kill = True
    
    # ถ้าติดคริทุก hit ก็ยังฆ่าไม่ได้
    if not can_kill and total_all_crit >= hp:
        can_kill = True
        min_crits_needed = n
    
    return {
        "skill_name": skill_name,
        "skill_hits": skill_hits,
        "hp_target": hp,
        "dmg_weak_only_per_hit": dmg_weak_only_per_hit,
        "dmg_crit_weak_per_hit": dmg_crit_weak_per_hit,
        "total_weak_only": total_weak_only,
        "total_all_crit": total_all_crit,
        "total_weakness": total_weakness,
        "min_crits_needed": min_crits_needed,
        "can_kill": can_kill,
        "damage_scenarios": damage_scenarios
    }


def print_castle_mode_results(results: dict):
    """แสดงผลลัพธ์ Castle Mode"""
    
    skill_name = results["skill_name"]
    hits = results["skill_hits"]
    hp = results["hp_target"]
    dmg_weak = results["dmg_weak_only_per_hit"]
    dmg_crit = results["dmg_crit_weak_per_hit"]
    total_weak = results["total_weak_only"]
    total_crit = results["total_all_crit"]
    min_crits = results["min_crits_needed"]
    can_kill = results["can_kill"]
    weakness = results["total_weakness"]
    
    print("\n" + "=" * 60)
    print(f"  🐵 Sun Wukong Castle Mode - {skill_name} 🏰")
    print("=" * 60)
    
    print(f"\n  📊 สกิล: {skill_name}")
    print(f"  🎯 จำนวน Hits: {hits}")
    print(f"  ❤️  HP เป้าหมาย: {hp:,}")
    print(f"  💧 Weakness Bonus: +{weakness}% (30% base + {weakness - 30}%)")
    
    print("\n" + "-" * 60)
    print("  📈 ดาเมจต่อ Hit")
    print("-" * 60)
    print(f"  ติดจุดอ่อน (ไม่คริ): {dmg_weak:,} / hit")
    print(f"  ติดคริ + จุดอ่อน:    {dmg_crit:,} / hit")
    print(f"  ส่วนต่าง:            +{dmg_crit - dmg_weak:,} / hit")
    
    print("\n" + "-" * 60)
    print("  🎲 ตารางดาเมจตามจำนวนคริ")
    print("-" * 60)
    print(f"  {'คริ':>4}  {'จุดอ่อน':>6}  {'ดาเมจรวม':>12}  {'ผลลัพธ์':>10}")
    print("  " + "-" * 42)
    
    for scenario in results["damage_scenarios"]:
        c = scenario["crit_count"]
        w = scenario["weak_count"]
        d = scenario["total_damage"]
        is_kill = scenario["is_kill"]
        
        status = "☠️ ตาย" if is_kill else "❌ รอด"
        marker = " ⬅️ MIN" if c == min_crits and can_kill else ""
        
        print(f"  {c:>4}  {w:>6}  {d:>12,}  {status:>10}{marker}")
    
    print("\n" + "=" * 60)
    if can_kill:
        if min_crits == 0:
            print(f"  ✅ ไม่ต้องคริเลย! แค่ติดจุดอ่อนก็ตาย ({total_weak:,} >= {hp:,})")
        else:
            print(f"  ⚔️  ต้องติดคริขั้นต่ำ: {min_crits} ครั้ง จาก {hits} hits")
            remaining_weak_only = hits - min_crits
            min_dmg = (min_crits * dmg_crit) + (remaining_weak_only * dmg_weak)
            print(f"      = จุดอ่อน {hits} hit (แต่ {min_crits} hit ติดคริด้วย) = {min_dmg:,} ดาเมจ")
    else:
        shortfall = hp - total_crit
        print(f"  ❌ ติดคริทุก hit ก็ยังฆ่าไม่ได้!")
        print(f"     ดาเมจสูงสุด: {total_crit:,} / HP: {hp:,}")
        print(f"     ขาดอีก: {shortfall:,}")
    print("=" * 60)
