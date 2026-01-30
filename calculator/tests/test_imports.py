"""Simple test to verify imports work"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from logic.biscuit import calculate_biscuit_damage
from logic.espada import calculate_espada_damage
from logic.freyja import calculate_freyja_damage
from logic.ryan import calculate_ryan_damage
from constants import DEF_BASE

print("✅ All imports successful")
print(f"   DEF_BASE['legend']['support'] = {DEF_BASE['legend']['support']}")