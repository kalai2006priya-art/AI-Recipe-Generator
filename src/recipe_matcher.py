"""
recipe_matcher.py
-----------------
Matching and ranking engine for Tamil Nadu traditional cuisine.

Features:
- Category filtering: Breakfast, Lunch, Snacks, Sweets, Dinner, All
- Diet filtering: Vegetarian, Non-Vegetarian, All
- High-precision matching against bilingual ingredients
- Smart relevance scoring prioritizing dishes that consume user's ingredients
"""

from typing import Dict, List, Optional
import pandas as pd
from src.ingredient_utils import match_ingredients


def calculate_recipe_match(user_ingredients: List[str], recipe_ingredients: List[str]) -> Dict:
    """Calculates match statistics between user ingredients and recipe requirements."""
    if not recipe_ingredients or not user_ingredients:
        return {
            "matched": [],
            "missing": recipe_ingredients,
            "match_percentage": 0.0,
            "user_utilization": 0.0,
            "matched_count": 0,
            "required_count": len(recipe_ingredients)
        }

    matched, missing = match_ingredients(user_ingredients, recipe_ingredients)

    matched_count = len(matched)
    required_count = len(recipe_ingredients)
    user_count = len(user_ingredients)

    match_pct = round((matched_count / required_count) * 100, 1) if required_count > 0 else 0.0
    user_util_pct = round((matched_count / user_count) * 100, 1) if user_count > 0 else 0.0

    return {
        "matched": matched,
        "missing": missing,
        "match_percentage": match_pct,
        "user_utilization": user_util_pct,
        "matched_count": matched_count,
        "required_count": required_count
    }


# Mapping of mandatory hero ingredients for each Tamil Nadu recipe.
# A recipe will ONLY qualify if at least ONE of its hero ingredients is provided by the user.
HERO_INGREDIENTS = {
    # Breakfast
    "tn_b1": ["idli rice", "urad dal", "rice"],                    # Soft Malligai Poo Idli
    "tn_b2": ["dosa rice", "urad dal", "dosa batter"],             # Crispy Golden Plain Dosa
    "tn_b3": ["raw rice", "moong dal", "rice"],                    # South Indian Ven Pongal
    "tn_b4": ["urad dal"],                                         # Crispy Medu Vada (Ulundu Vadai)
    "tn_b5": ["raw rice", "coconut milk", "coconut", "rice"],      # Chettinad Aappam
    "tn_b6": ["wheat flour", "potato"],                            # Poori with Potato Masala
    "tn_b7": ["coconut", "green chilli"],                          # White Coconut Chutney
    "tn_b8": ["tomato", "onion"],                                  # Spicy Tomato Onion Chutney
    "tn_b9": ["rava"],                                             # Traditional Rava Upma
    "tn_b10": ["curd", "raw rice", "rava"],                        # Instant Soft Mor Dosa (Curd Dosa)

    # Lunch
    "tn_l1": ["toor dal", "drumstick", "sambar powder"],           # Authentic Murungakkai Sambar
    "tn_l2": ["tomato", "black pepper", "cumin", "tamarind"],      # Thakkali Milagu Rasam
    "tn_l3": ["garlic", "shallot", "sundakkai vathal", "tamarind"], # Chettinad Poondu Vatha Kulambu
    "tn_l4": ["brinjal", "shallot", "tamarind"],                   # Ennai Kathirikai Kulambu
    "tn_l5": ["potato"],                                           # Crispy Urulaikizhangu Roast
    "tn_l6": ["seeraga samba rice", "chicken", "biryani"],         # Dindigul Thalappakatti Biryani
    "tn_l7": ["rice", "curd"],                                     # South Indian Curd Rice (Thayir Sadam)
    "tn_l8": ["rice", "lemon juice"],                              # Traditional Lemon Rice
    "tn_l9": ["chicken"],                                          # Chettinad Spicy Chicken Gravy
    "tn_l10": ["fish", "tamarind"],                                # Village Style Meen Kulambu
    "tn_l11": ["curd", "coconut"],                                 # Traditional Tamil Mor Kuzhambu

    # Snacks
    "tn_s1": ["chana dal"],                                        # Crispy Masala Vadai
    "tn_s2": ["besan", "onion", "potato"],                         # Onion & Potato Bajji
    "tn_s3": ["white chana"],                                      # Navaratri White Chana Sundal
    "tn_s4": ["curd", "urad dal"],                                 # South Indian Thayir Vadai

    # Sweets
    "tn_sw1": ["raw rice", "moong dal", "jaggery", "rice"],        # Sakkarai Pongal
    "tn_sw2": ["rava", "sugar", "ghee"],                           # Rava Kesari
    "tn_sw3": ["raw rice", "milk", "sugar", "rice"],               # Creamy Paal Payasam
    "tn_sw4": ["besan", "sugar", "ghee"],                          # Ghee Mysore Pak

    # Dinner
    "tn_d1": ["parotta", "egg"],                                   # Madurai Style Kothu Parotta
    "tn_d2": ["wheat flour", "carrot", "beans", "potato"],         # Chapati with Veg Kurma
    "tn_d3": ["dosa batter", "egg"],                               # Street Style Muttai Dosa
    "tn_d4": ["curd", "semiya"],                                   # Traditional Thayir Semiya
}


def filter_and_rank_recipes(
    df: pd.DataFrame,
    user_ingredients: List[str],
    category: str = "All",
    diet: str = "All",
    max_time: Optional[int] = None,
    prioritize_food_waste: bool = False,
    top_k: int = 10,
    strict_validation: bool = False
) -> List[Dict]:
    """Filters Tamil Nadu recipe dataset and ranks matches by culinary relevance."""
    if df.empty or not user_ingredients:
        return []

    filtered_df = df.copy()

    # 1. Meal Category Filter (Breakfast, Lunch, Snacks, Sweets, Dinner)
    if category and category != "All" and "all" not in category.lower() and "அனைத்தும்" not in category:
        cat_lower = category.lower()
        if "breakfast" in cat_lower or "காலை" in cat_lower:
            filtered_df = filtered_df[filtered_df["category"] == "Breakfast"]
        elif "lunch" in cat_lower or "மதிய" in cat_lower:
            filtered_df = filtered_df[filtered_df["category"] == "Lunch"]
        elif "snack" in cat_lower or "சிற்றுண்டி" in cat_lower:
            filtered_df = filtered_df[filtered_df["category"] == "Snacks"]
        elif "sweet" in cat_lower or "இனிப்பு" in cat_lower:
            filtered_df = filtered_df[filtered_df["category"] == "Sweets"]
        elif "dinner" in cat_lower or "இரவு" in cat_lower:
            filtered_df = filtered_df[filtered_df["category"] == "Dinner"]

    # 2. Diet Filter
    if diet and diet != "All" and "all" not in diet.lower() and "அனைத்தும்" not in diet:
        if "veg" in diet.lower() or "சைவம்" in diet:
            filtered_df = filtered_df[filtered_df["diet"] == "Vegetarian"]
        elif "non" in diet.lower() or "அசைவம்" in diet:
            filtered_df = filtered_df[filtered_df["diet"] == "Non-Vegetarian"]

    # 3. Max Time Filter
    if max_time is not None and max_time > 0:
        filtered_df = filtered_df[filtered_df["time_mins"] <= max_time]

    if filtered_df.empty:
        return []

    candidate_results = []
    user_str = " ".join(user_ingredients).lower()
    user_has_meat = any(m in user_str for m in ["chicken", "mutton", "fish", "prawn", "crab", "meat", "egg"])

    from src.ingredient_utils import SYNONYMS, is_ingredient_match

    for _, row in filtered_df.iterrows():
        # Never recommend non-veg dishes if user gave vegetarian ingredients
        if not user_has_meat and row.get("diet") == "Non-Vegetarian":
            continue

        recipe_id = row.get("id", "")
        recipe_ing_list = row["ingredients_list"]

        # STRICT HERO QUALIFICATION RULE:
        # A dish MUST have at least one of its core hero ingredients supplied by user!
        # Incidental garnishes (salt, mustard, oil, turmeric, curry leaf) will NEVER match a dish on their own.
        heroes = HERO_INGREDIENTS.get(recipe_id, [x.lower() for x in recipe_ing_list[:2]])
        has_hero_match = any(
            is_ingredient_match(u_ing, h_ing)
            for u_ing in user_ingredients
            for h_ing in heroes
        )

        if not has_hero_match:
            continue

        match_info = calculate_recipe_match(user_ingredients, recipe_ing_list)

        if match_info["matched_count"] > 0:
            name_en_lower = row["name_en"].lower()
            name_ta_text = row["name_ta"]

            # Title Match Check (Hero Ingredient in Dish Name)
            has_title_match = False
            for u_ing in user_ingredients:
                u_clean = u_ing.lower()
                if u_clean in name_en_lower:
                    has_title_match = True
                    break
                syns = SYNONYMS.get(u_clean, [])
                if any(s in name_en_lower or s in name_ta_text for s in syns):
                    has_title_match = True
                    break

            # Count matches against hero ingredients
            matched_hero_count = sum(
                1 for h in heroes
                if any(is_ingredient_match(u, h) for u in user_ingredients)
            )

            from src.recipe_validator import validate_recipe
            validation = validate_recipe(row.to_dict(), user_ingredients)

            # High-Precision Culinary Scoring Formula
            score = 100.0  # Base qualification score for possessing hero ingredient
            score += (matched_hero_count * 50.0)
            score += (match_info["matched_count"] * 20.0)
            score += (match_info["user_utilization"] * 0.5)
            score += (match_info["match_percentage"] * 0.4)

            # Huge bonus if 100% of non-pantry ingredients are supplied (0 missing major ingredients)
            if validation["valid"]:
                score += 150.0

            # Extra bonus if user's ingredient is explicitly in the dish title
            if has_title_match:
                score += 80.0

            candidate_results.append({
                "id": row["id"],
                "name_en": row["name_en"],
                "name_ta": row["name_ta"],
                "category": row["category"],
                "diet": row["diet"],
                "time_mins": row["time_mins"],
                "difficulty": row["difficulty"],
                "match_percentage": match_info["match_percentage"],
                "user_utilization": match_info["user_utilization"],
                "matched_ingredients": match_info["matched"],
                "missing_ingredients": match_info["missing"],
                "missing_major_ingredients": validation["missing_ingredients"],
                "is_fully_valid": validation["valid"],
                "matched_count": match_info["matched_count"],
                "required_count": match_info["required_count"],
                "ingredients_en": row["ingredients_en"],
                "ingredients_ta": row["ingredients_ta"],
                "instructions_en": row["instructions_en"],
                "instructions_ta": row["instructions_ta"],
                "score": round(score, 2)
            })

    if strict_validation:
        candidate_results = [r for r in candidate_results if r["is_fully_valid"]]

    if not candidate_results:
        return []

    if prioritize_food_waste:
        candidate_results.sort(
            key=lambda x: (x["is_fully_valid"], x["user_utilization"], x["score"]),
            reverse=True
        )
    else:
        candidate_results.sort(
            key=lambda x: (x["is_fully_valid"], x["score"], x["match_percentage"]),
            reverse=True
        )

    return candidate_results[:top_k]
