"""
recipe_validator.py
--------------------
Programmatic validation module ensuring strict ingredient-aware recipe generation.

Validates that:
1. Every major (non-pantry) ingredient required by the recipe was explicitly provided by the user.
2. Only allowed basic pantry items (salt, oil, water, basic spices) are accepted as defaults.
3. At least one user-provided ingredient is actively utilized.
4. Hallucinated or invented major ingredients immediately mark the recipe INVALID.
"""

from typing import Dict, List, Tuple
from src.ingredient_utils import (
    clean_single_word,
    is_pantry_ingredient,
    is_ingredient_match,
    ALLOWED_PANTRY_INGREDIENTS
)


def validate_recipe(recipe: Dict, user_ingredients: List[str]) -> Dict:
    """
    Validates whether every important ingredient used by the generated recipe
    is available in:
      1. user_ingredients OR
      2. allowed pantry ingredients

    Args:
        recipe (dict): Recipe dictionary containing 'used_ingredients' or 'ingredients'
                       or 'cleaned_ingredients_en' or 'ingredients_list'.
        user_ingredients (list): List of user-provided ingredients (e.g. ['chicken', 'chilli', 'tomato'])

    Returns:
        dict: Validation report:
        {
            "recipe_name": "...",
            "provided_ingredients": [...],
            "pantry_ingredients": [...],
            "missing_ingredients": [...],
            "used_ingredients": [...],
            "steps": [...],
            "valid": True/False,
            "rejection_reason": "..."
        }
    """
    if not recipe or not isinstance(recipe, dict):
        return {
            "recipe_name": "",
            "provided_ingredients": [],
            "pantry_ingredients": [],
            "missing_ingredients": [],
            "used_ingredients": [],
            "steps": [],
            "valid": False,
            "rejection_reason": "Empty or invalid recipe structure."
        }

    # Extract recipe name
    name = (
        recipe.get("recipe_name") or
        recipe.get("name_en") or
        recipe.get("name") or
        "Untitled Recipe"
    )

    # Extract ingredients list from various possible keys
    raw_ingredients = (
        recipe.get("used_ingredients") or
        recipe.get("ingredients") or
        recipe.get("cleaned_ingredients_en") or
        recipe.get("ingredients_list") or
        []
    )

    # If ingredients is a multiline string, split lines
    if isinstance(raw_ingredients, str):
        raw_ingredients = [
            line.strip().lstrip("-").lstrip("*").strip()
            for line in raw_ingredients.splitlines()
            if line.strip()
        ]

    # Normalize user ingredients
    clean_user_ings = [clean_single_word(u) for u in user_ingredients if u and clean_single_word(u)]

    provided_ingredients = []
    pantry_ingredients = []
    missing_ingredients = []
    used_ingredients_clean = []

    for item in raw_ingredients:
        norm_item = clean_single_word(item)
        if not norm_item:
            continue

        if norm_item not in used_ingredients_clean:
            used_ingredients_clean.append(norm_item)

        # 1. Check if allowed basic pantry ingredient
        if is_pantry_ingredient(norm_item):
            if norm_item not in pantry_ingredients:
                pantry_ingredients.append(norm_item)
            continue

        # 2. Check if user provided this ingredient
        has_user_match = any(
            is_ingredient_match(u_ing, norm_item)
            for u_ing in clean_user_ings
        )

        if has_user_match:
            if norm_item not in provided_ingredients:
                provided_ingredients.append(norm_item)
        else:
            # 3. Missing major ingredient -> INVALID!
            if norm_item not in missing_ingredients:
                missing_ingredients.append(norm_item)

    # Determine validity
    # Must have 0 missing major ingredients AND use at least 1 user ingredient
    if missing_ingredients:
        is_valid = False
        rejection_reason = f"Requires unprovided major ingredients: {', '.join(missing_ingredients)}"
    elif not provided_ingredients and clean_user_ings:
        is_valid = False
        rejection_reason = "Recipe does not utilize any of the user-provided ingredients."
    else:
        is_valid = True
        rejection_reason = ""

    # Extract steps if available
    steps = recipe.get("steps") or recipe.get("instructions_en") or []
    if isinstance(steps, str):
        steps = [s.strip() for s in steps.splitlines() if s.strip()]

    return {
        "recipe_name": name,
        "recipe_name_ta": recipe.get("recipe_name_ta", recipe.get("name_ta", "")),
        "provided_ingredients": provided_ingredients,
        "pantry_ingredients": pantry_ingredients,
        "missing_ingredients": missing_ingredients,
        "used_ingredients": used_ingredients_clean,
        "ingredients_with_quantities": recipe.get("ingredients_with_quantities", []),
        "steps": steps,
        "cooking_time": recipe.get("cooking_time", recipe.get("time_mins", 20)),
        "difficulty": recipe.get("difficulty", "Easy"),
        "diet": recipe.get("diet", "Vegetarian"),
        "category": recipe.get("category", "Main Course"),
        "valid": is_valid,
        "rejection_reason": rejection_reason
    }
