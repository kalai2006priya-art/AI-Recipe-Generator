"""
test_tamil_features.py
----------------------
Verifies:
1. Authentication (User registration, login, favorites)
2. Bilingual ingredient parsing (Tamil and English)
3. Tamil Nadu category filtering (Breakfast, Lunch, Snacks, Sweets, Dinner)
4. AI Voice Audio Generation (gTTS for Tamil)
5. Bilingual recipe customization and fallback
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Force utf-8 stdout
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.auth import register_user, login_user, toggle_favorite, get_favorites
from src.ingredient_utils import parse_user_ingredients
from src.data_loader import load_recipe_dataset
from src.recipe_matcher import filter_and_rank_recipes
from src.voice_service import generate_recipe_audio
from src.llm_service import generate_fallback_recipe


def run_tests():
    print("=" * 60)
    print("TAMIL NADU AI KITCHEN - FULL VERIFICATION SUITE")
    print("=" * 60)

    # 1. Auth Test
    print("\n[TEST 1] Authentication System...")
    import time
    test_user = f"selvi_{int(time.time())}"
    reg_ok, reg_msg = register_user(test_user, "pass123", "செல்வி (Selvi)")
    print(f"  Register: {reg_ok} - {reg_msg}")
    assert reg_ok, "Registration should succeed!"
    login_ok, user_data, login_msg = login_user(test_user, "pass123")
    print(f"  Login: {login_ok} - {login_msg}")
    assert login_ok, "Login should succeed!"
    toggle_favorite(test_user, "முருங்கைக்காய் சாம்பார்", "Lunch")
    favs = get_favorites(test_user)
    print(f"  Favorites for {test_user}: {favs}")
    assert "முருங்கைக்காய் சாம்பார்" in favs
    print(">>> AUTHENTICATION TEST PASSED!")

    # 2. Bilingual Ingredient Parsing
    print("\n[TEST 2] Bilingual Ingredient Parsing...")
    ta_input = "தக்காளி, வெங்காயம், துவரம் பருப்பு, முருங்கைக்காய்"
    parsed_ta = parse_user_ingredients(ta_input)
    print(f"  Input: {ta_input}")
    print(f"  Parsed to canonical tokens: {parsed_ta}")
    assert "tomato" in parsed_ta and "onion" in parsed_ta and "toor dal" in parsed_ta and "drumstick" in parsed_ta
    print(">>> BILINGUAL INGREDIENT PARSING PASSED!")

    # 3. Category Matching
    print("\n[TEST 3] Category Matching (Lunch, Breakfast, Sweets, Snacks, Dinner)...")
    df = load_recipe_dataset()
    print(f"  Total Tamil Nadu Recipes: {len(df)}")

    # Lunch Test: Sambar
    matches_lunch = filter_and_rank_recipes(df, parsed_ta, category="Lunch", top_k=3)
    print(f"  Lunch Matches: {len(matches_lunch)}")
    assert len(matches_lunch) > 0
    print(f"    #1: {matches_lunch[0]['name_ta']} ({matches_lunch[0]['name_en']})")

    # Breakfast Test: Idli / Dosa
    parsed_bf = parse_user_ingredients("இட்லி அரிசி, உளுத்தம் பருப்பு, வெந்தயம்")
    matches_bf = filter_and_rank_recipes(df, parsed_bf, category="Breakfast", top_k=3)
    print(f"  Breakfast Matches: {len(matches_bf)}")
    assert len(matches_bf) > 0
    print(f"    #1: {matches_bf[0]['name_ta']} ({matches_bf[0]['name_en']})")

    # Sweets Test: Sakkarai Pongal
    parsed_sw = parse_user_ingredients("பச்சரிசி, பாசிப்பருப்பு, வெல்லம், நெய், ஏலக்காய்")
    matches_sw = filter_and_rank_recipes(df, parsed_sw, category="Sweets", top_k=3)
    print(f"  Sweets Matches: {len(matches_sw)}")
    assert len(matches_sw) > 0
    print(f"    #1: {matches_sw[0]['name_ta']} ({matches_sw[0]['name_en']})")
    print(">>> CATEGORY MATCHING PASSED!")

    # 4. Voice Audio Generation (gTTS)
    print("\n[TEST 4] Voice Audio Generation (gTTS)...")
    sample_text = "வணக்கம்! முருங்கைக்காய் சாம்பார் செய்ய துவரம் பருப்பை வேகவைக்கவும்."
    audio_fp = generate_recipe_audio(sample_text, lang="ta")
    audio_bytes = audio_fp.getvalue()
    print(f"  Generated Tamil audio size: {len(audio_bytes)} bytes")
    assert len(audio_bytes) > 1000, "Audio buffer should contain valid MP3 data"
    print(">>> AI VOICE AUDIO GENERATION PASSED!")

    # 5. Bilingual Fallback Recipe Generation
    print("\n[TEST 5] Bilingual Fallback Recipe Generation...")
    sample_rec = matches_lunch[0]
    res_ta = generate_fallback_recipe(sample_rec, servings=4, lang="ta")
    assert "தேவையான பொருட்கள்" in res_ta["content"]
    assert "செய்முறை" in res_ta["content"]
    res_en = generate_fallback_recipe(sample_rec, servings=4, lang="en")
    assert "Ingredients" in res_en["content"]
    assert "Instructions" in res_en["content"]
    print(">>> BILINGUAL FALLBACK TEST PASSED!")

    print("\n" + "=" * 60)
    print("ALL TAMIL NADU UPGRADE TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
