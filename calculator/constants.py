"""
7k Rebirth Damage Calculator - Constants
ค่าคงที่ที่ใช้ในระบบการคำนวณดาเมจ
"""

from decimal import Decimal

# DEF Modifier - ตัวคูณ DEF ในระบบ (ยืนยันจากการทดสอบ)
DEF_MODIFIER = Decimal("0.00214135")

# ATK_BASE ตามสายและ Rarity (6 ดาว+5)
# สาย: attack, magic, support, defense, balance

ATK_BASE = {
    "legend": {
        "attack": Decimal("1500"),    # สายโจมตี
        "magic": Decimal("1500"),     # สายเวท
        "support": Decimal("1095"),   # สายซัพพอร์ต
        "defense": Decimal("727"),    # สายป้องกัน
        "balance": Decimal("1306"),   # สายสมดุล
    },
    "rare": {
        "attack": Decimal("1389"),
        "magic": Decimal("1389"),
        "support": Decimal("1035"),
        "defense": Decimal("704"),
        "balance": Decimal("1238"),
    }
}

# DEF_BASE ตามสายและ Rarity (6 ดาว+5)
DEF_BASE = {
    "legend": {
        "attack": Decimal("571"),     # สายโจมตี
        "magic": Decimal("571"),      # สายเวท
        "support": Decimal("675"),    # สายซัพพอร์ต
        "defense": Decimal("892"),    # สายป้องกัน
        "balance": Decimal("659"),    # สายสมดุล
    },
    "rare": {
        "attack": Decimal("533"),
        "magic": Decimal("533"),
        "support": Decimal("632"),
        "defense": Decimal("818"),
        "balance": Decimal("616"),
    }
}

# HP_BASE ตามสายและ Rarity (6 ดาว+5)
HP_BASE = {
    "legend": {
        "attack": Decimal("3362"),    # สายโจมตี
        "magic": Decimal("3362"),     # สายเวท
        "support": Decimal("4458"),   # สายซัพพอร์ต
        "defense": Decimal("4825"),   # สายป้องกัน
        "balance": Decimal("3693"),   # สายสมดุล
    },
    "rare": {
        "attack": Decimal("3174"),
        "magic": Decimal("3174"),
        "support": Decimal("4248"),
        "defense": Decimal("4572"),
        "balance": Decimal("3529"),
    }
}


def get_atk_base(rarity: str, char_class: str) -> Decimal:
    """
    ดึงค่า ATK_BASE ตาม Rarity และ Class
    rarity: "legend" หรือ "rare"
    char_class: "attack", "magic", "support", "defense", "balance"
    """
    rarity = rarity.lower()
    char_class = char_class.lower()
    
    if rarity in ATK_BASE and char_class in ATK_BASE[rarity]:
        return ATK_BASE[rarity][char_class]
    
    # Default to legend magic
    return Decimal("1500")


def get_def_base(rarity: str, char_class: str) -> Decimal:
    """
    ดึงค่า DEF_BASE ตาม Rarity และ Class
    rarity: "legend" หรือ "rare"
    char_class: "attack", "magic", "support", "defense", "balance"
    """
    rarity = rarity.lower()
    char_class = char_class.lower()
    
    if rarity in DEF_BASE and char_class in DEF_BASE[rarity]:
        return DEF_BASE[rarity][char_class]
    
    # Default to legend attack/magic
    return Decimal("571")


def get_hp_base(rarity: str, char_class: str) -> Decimal:
    """
    ดึงค่า HP_BASE ตาม Rarity และ Class
    rarity: "legend" หรือ "rare"
    char_class: "attack", "magic", "support", "defense", "balance"
    """
    rarity = rarity.lower()
    char_class = char_class.lower()
    
    if rarity in HP_BASE and char_class in HP_BASE[rarity]:
        return HP_BASE[rarity][char_class]
    
    # Default to legend attack/magic
    return Decimal("3362")
