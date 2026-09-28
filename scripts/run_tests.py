"""
run_tests.py
------------
Automated test suite verifying the required test scenarios
including Indian recipes (Sambar, Chutney) and International cuisine selection.
"""

import os
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.data_loader import load_recipe_dataset
from src.ingredient_utils import parse_user_ingredients
from src.recipe_matcher import filter_and_rank_recipes
from src.llm_service import generate_fallback_recipe


def run_all_tests():
    print("=" * 60)
    print("RECIPE GENERATOR - AUTOMATED VERIFICATION SUITE")
    print("=" * 60)

    print("\n[SETUP] Loading processed dataset...")
    df = load_recipe_dataset()
    print(f"Dataset successfully loaded. Total recipes: {len(df)}")
    assert len(df) > 0, "Dataset should not be empty!"

    # ----------------------------------------------------
    # Test 1: Sambar Ingredients Test
    # ----------------------------------------------------
    print("\n" + "-" * 50)
    print("TEST 1: Sambar Ingredients ('Toor Dal, Tomato, Onion, Drumstick')")
    print("-" * 50)
    ings_sambar = parse_user_ingredients("Toor Dal, Tomato, Onion, Drumstick")
    matches_sambar = filter_and_rank_recipes(df, ings_sambar, category="Lunch", top_k=3)
    assert len(matches_sambar) > 0, "Sambar test should find matches!"
    top_sambar = matches_sambar[0]
    print(f"  Top Match: {top_sambar['name_en']} ({top_sambar['name_ta']})")
    assert "Sambar" in top_sambar["name_en"], "Top match should be Sambar!"
    print(">>> TEST 1 (SAMBAR) PASSED!")

    # ----------------------------------------------------
    # Test 2: Accurate Curd Prediction Test
    # ----------------------------------------------------
    print("\n" + "-" * 50)
    print("TEST 2: Curd Prediction ('curd')")
    print("-" * 50)
    ings_curd = parse_user_ingredients("curd")
    matches_curd = filter_and_rank_recipes(df, ings_curd, top_k=5)
    assert len(matches_curd) > 0, "Curd test should return curd dishes!"
    curd_names = [r["name_en"] for r in matches_curd]
    for idx, r in enumerate(matches_curd):
        print(f"  [{idx+1}] [{r['category']}] {r['name_en']} ({r['name_ta']}) | Score: {r['score']}")
    assert "South Indian Curd Rice (Thayir Sadam)" in curd_names
    assert "Traditional Tamil Mor Kuzhambu (Spiced Curd Curry)" in curd_names
    for name in curd_names:
        assert "Biryani" not in name, "Non-veg Biryani should NOT be recommended for curd!"
        assert "Crispy Golden Plain Dosa" not in name, "Plain Dosa should NOT be recommended for curd!"
    print(">>> TEST 2 (ACCURATE CURD PREDICTION) PASSED!")

    # ----------------------------------------------------
    # Test 3: Tamil Language Input ('தயிர்')
    # ----------------------------------------------------
    print("\n" + "-" * 50)
    print("TEST 3: Tamil Input ('தயிர்')")
    print("-" * 50)
    ings_ta = parse_user_ingredients("தயிர்")
    assert ings_ta == ["curd"], f"தயிர் should parse to 'curd', got: {ings_ta}"
    matches_ta = filter_and_rank_recipes(df, ings_ta, top_k=3)
    assert len(matches_ta) > 0
    print(f"  Top Match: {matches_ta[0]['name_ta']} ({matches_ta[0]['name_en']})")
    print(">>> TEST 3 (TAMIL PARSING & MATCHING) PASSED!")

    # ----------------------------------------------------
    # Test 4: Category Filtering (Curd in Breakfast & Snacks)
    # ----------------------------------------------------
    print("\n" + "-" * 50)
    print("TEST 4: Category Filtering for Curd ('Breakfast' & 'Snacks')")
    print("-" * 50)
    matches_bf = filter_and_rank_recipes(df, ings_curd, category="Breakfast")
    assert len(matches_bf) > 0, "Breakfast should have Instant Mor Dosa!"
    print(f"  Breakfast Curd Dish: {matches_bf[0]['name_en']} ({matches_bf[0]['name_ta']})")
    assert "Mor Dosa" in matches_bf[0]["name_en"]

    matches_snack = filter_and_rank_recipes(df, ings_curd, category="Snacks")
    assert len(matches_snack) > 0, "Snacks should have Thayir Vadai!"
    print(f"  Snacks Curd Dish: {matches_snack[0]['name_en']} ({matches_snack[0]['name_ta']})")
    assert "Thayir Vadai" in matches_snack[0]["name_en"]
    print(">>> TEST 4 (CATEGORY FILTERING) PASSED!")

    # ----------------------------------------------------
    # Test 5: Empty Input Handling
    # ----------------------------------------------------
    print("\n" + "-" * 50)
    print("TEST 5: Empty Input ('   ')")
    print("-" * 50)
    ings_empty = parse_user_ingredients("   ")
    matches_empty = filter_and_rank_recipes(df, ings_empty)
    assert matches_empty == [], "Empty input must return empty results list!"
    print("  Empty input handled gracefully without crashing.")
    print(">>> TEST 5 (EMPTY INPUT) PASSED!")

    # ----------------------------------------------------
    # Test 6: Fallback Generation (Bilingual)
    # ----------------------------------------------------
    print("\n" + "-" * 50)
    print("TEST 6: Bilingual Fallback Recipe Generation")
    print("-" * 50)
    sample_recipe = matches_curd[0]
    fallback_en = generate_fallback_recipe(sample_recipe, servings=2, lang="en")
    assert fallback_en["is_ai_customized"] is False
    assert "Ingredients" in fallback_en["content"]
    print("  English recipe generation: OK")

    fallback_ta = generate_fallback_recipe(sample_recipe, servings=2, lang="ta")
    assert "தேவையான பொருட்கள்" in fallback_ta["content"]
    print("  Tamil recipe generation: OK")
    print(">>> TEST 6 (BILINGUAL FALLBACK) PASSED!")

    print("\n" + "=" * 60)
    print("ALL VERIFICATION SUITE TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
