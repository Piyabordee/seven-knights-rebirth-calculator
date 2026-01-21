# วิธีดึงข้อมูลตัวละครจาก GameWith

เอกสารนี้อธิบายวิธีดึงค่าจาก [GameWith](https://gamewith.net/sevenknights-rebirth/) มาใส่ใน character JSON files

---

## 📋 Character JSON Structure Pattern

### โครงสร้างมาตรฐานสำหรับไฟล์ตัวละคร (characters/*.json)

```json
{
    "// ===== Metadata (ขึ้นต้นด้วย _) =====": "",
    "_character": "ชื่อตัวละคร",
    "_rarity": "legend",
    "_class": "magic | balance | defense | warrior",
    "_source": "URL ที่อ้างอิง (GameWith)",
    "_element": "Fire | Water | Earth | Light | Dark",
    
    "// ===== Passive Skills (ใช้กับทุกสกิล) =====": "",
    "BUFF_ATK": 0.00,
    "CRIT_DMG": 0.00,
    "WEAK_DMG": 0.00,
    "DMG_AMP_BUFF": 0.00,
    
    "// ===== Skills =====": "",
    "_skills": {
        "skill2": {
            "_name": "ชื่อสกิลบน (ภาษาอังกฤษ)",
            "SKILL_DMG": 0.00,
            "SKILL_HITS": 1,
            "Ignore_DEF": 0.00,
            "Bonus_DMG_HP_Target": 0.00,
            "Cap_ATK_Percent": 0.00,
            "DEF_REDUCE": 0.00,
            "DMG_AMP_DEBUFF": 0.00
        },
        "skill1": {
            "_name": "ชื่อสกิลล่าง (ภาษาอังกฤษ)",
            "SKILL_DMG": 0.00,
            "SKILL_HITS": 1,
            "Ignore_DEF": 0.00,
            "Bonus_DMG_HP_Target": 0.00,
            "Cap_ATK_Percent": 0.00
        }
    },
    
    "// ===== Notes =====": "",
    "_notes": [
        "บันทึกข้อมูลเพิ่มเติม เช่น ATK_BASE, Transcend values"
    ]
}
```

### กฎการใช้งาน:

1. **Metadata** (ขึ้นต้นด้วย `_`): ไม่ถูกนำไปคำนวณ ใช้อ้างอิงเท่านั้น
2. **Passive Skills**: ค่าที่ใช้ได้กับทุกสกิล (วางนอก `_skills`)
3. **Skills**: แยก `skill1` (ล่าง) และ `skill2` (บน)
4. **ค่าเริ่มต้น**: ถ้าสกิลไม่มีค่าใด ให้ใส่ `0.00`
5. **การรวมค่า**: Calculator จะ ADD ค่า (Character Passive + Skill + User Config)
6. **ใช้ค่า Enhanced เสมอ**: ยึดค่าหลัง Skill Enhancement เป็นหลัก (เช่น 470% แทน 390%)

---

## URL Pattern

```
https://gamewith.net/sevenknights-rebirth/[ID]
```

ตัวอย่าง: Miho = `https://gamewith.net/sevenknights-rebirth/70610`

---

## ค่าที่ต้องดึงจาก GameWith Skill Page

### Skill Properties (ใส่ใน `_skills.skill1` หรือ `_skills.skill2`)

| ข้อมูลใน GameWith | ตัวแปร | ตัวอย่าง |
|-------------------|--------|----------|
| "Deals damage equal to **X%** of [Type] Attack **N time(s)**" | `SKILL_DMG`, `SKILL_HITS` | 55%, 3 hits |
| "Additional damage equal to **X%** upon Weakness Hit" | รวมเข้า `WEAK_DMG` (ในสกิล) | 85% |
| "Ignores **X%** of the enemy's Defense" | `Ignore_DEF` | 40% |
| "Deals additional damage equal to **X%** of target's Max HP" | `Bonus_DMG_HP_Target` | 7% |
| "(Capped at **X%** of Attack)" | `Cap_ATK_Percent` | 100% |
| "Defense Reduction by **X%**" | `DEF_REDUCE` | 29% |
| "Physical/Magic Vulnerability by **X%**" | `DMG_AMP_DEBUFF` | 22% |

### Passive Properties (ใส่นอก `_skills`)

| ข้อมูลใน GameWith | ตัวแปร | ตัวอย่าง |
|-------------------|--------|----------|
| "Attack Boost by **X%**" | `BUFF_ATK` | 25% |
| "Weakness Hit Damage Boost by **X%**" | `WEAK_DMG` | 23% |
| "Magic/Physical Damage Boost by **X%**" | `DMG_AMP_BUFF` | 35% |
| "Crit Damage Boost by **X%**" | `CRIT_DMG` | 40% |

---

## ค่าที่ต้องสมมุติ/กรอกเอง

| ตัวแปร | ที่มา |
|--------|-------|
| `ATK_CHAR` | หน้าสถิติตัวละคร |
| `ATK_PET` | หน้า Pet |
| `CRIT_DMG` | Stats + Gear |
| `DEF_Target` | ข้อมูล Boss/ศัตรู |
| `Ignore_DEF` | Stats + Gear |
| `DMG_AMP_BUFF` | Ring, Leader Skill, Buff จากตัวอื่น |

---

## ตัวอย่าง: การแปลงข้อมูล GameWith → JSON

### Yeonhee (ตัวอย่างมาตรฐาน)

**จาก GameWith:**
```
Passive: Otherworldly Insight
- Attack Boost by 25% for 3 turn(s)

Skill 2: Eternal Slumber
- Deals damage equal to 55% of Magic Attack 3 time(s)
- Ignores 40% of the enemy's Defense

Skill 1: Calamitous Gesture  
- Deals damage equal to 51% of Magic Attack 3 time(s)
- Deals additional damage equal to 7% of target's Max HP
  (Capped at 100% of Attack)
```

**แปลงเป็น yeonhee.json:**
```json
{
    "_character": "Yeonhee",
    "_rarity": "legend",
    "_class": "magic",
    "_element": "Dark",
    "BUFF_ATK": 25.00,
    "_skills": {
        "skill2": {
            "_name": "Eternal Slumber (สกิลบน)",
            "SKILL_DMG": 55.00,
            "SKILL_HITS": 3,
            "Ignore_DEF": 40.00,
            "Bonus_DMG_HP_Target": 0.00,
            "Cap_ATK_Percent": 0.00
        },
        "skill1": {
            "_name": "Calamitous Gesture (สกิลล่าง)",
            "SKILL_DMG": 51.00,
            "SKILL_HITS": 3,
            "Ignore_DEF": 0.00,
            "Bonus_DMG_HP_Target": 7.00,
            "Cap_ATK_Percent": 100.00
        }
    }
}
```

---

## ตัวอย่างเพิ่มเติม

### Miho Skill 2: Overconfident Blow

**ข้อความจาก GameWith:**
```
Passive: Opportunist
- Weakness Hit Damage Boost by 23%

Skill 2: Overconfident Blow
- Deals damage equal to 160% of Magic Attack 1 time(s)
- Increases Damage: To 185% of Magic Attack
- Adds Damage: Deals additional damage equal to 85% upon Weakness Hit

Skill 1: Violent Dance
- Magic Vulnerability by 22% for 2 turn(s)
```

**แปลงเป็น miho.json:**
```json
{
    "_character": "Miho",
    "_rarity": "legend",
    "_class": "magic",
    "_element": "Dark",
    "WEAK_DMG": 23.00,
    "_skills": {
        "skill2": {
            "_name": "Overconfident Blow (สกิลบน)",
            "SKILL_DMG": 160.00,
            "SKILL_HITS": 1,
            "Ignore_DEF": 0.00
        },
        "skill1": {
            "_name": "Violent Dance (สกิลล่าง)",
            "SKILL_DMG": 0.00,
            "SKILL_HITS": 1,
            "DMG_AMP_DEBUFF": 22.00
        }
    },
    "_notes": [
        "Skill 2: 160% → 185% (Transcend), +85% on Weakness"
    ]
}
```

---

## เคล็ดลับ

1. **ใช้ค่า Enhanced เสมอ**: ให้ยึดค่าหลัง Skill Enhancement (ค่า "Increases to X%") เป็นค่าหลักในไฟล์ JSON
   - ✅ ถูก: `"SKILL_DMG": 470.00` (Enhanced)
   - ❌ ผิด: `"SKILL_DMG": 390.00` (Base)
   - บันทึกหมายเหตุ: `"*** ค่าทั้งหมดเป็น Enhanced แล้ว ***"`

2. **Transcend Effects**: ถ้ามีค่าพิเศษจาก Transcendence (T2, T4, T6) ให้บันทึกไว้ใน `_notes`
   - ตัวอย่าง: "T6: Crit Rate +100%", "T4: +24% Crit Damage"

3. **Debuff Skills**: ถ้าสกิลเป็นบัฟ/ดีบัฟอย่างเดียว (ไม่มีดาเมจ) ให้ใส่ `SKILL_DMG: 0.00`

4. **Weakness Bonus**: ถ้ามี "Additional damage upon Weakness Hit" ให้บันทึกไว้ใน `_notes` (ยังไม่รองรับ auto-calculate)

5. **Element Advantage**: ไม่ต้องใส่ใน JSON (คำนวณแยก)

> **หมายเหตุ:** "Increases Damage: To 185%" คือค่าหลัง Transcend ให้ใช้ค่านั้นแทนถ้า Transcend แล้ว
