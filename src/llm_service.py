"""
llm_service.py
--------------
Bilingual LLM-powered recipe generator and customization using Google Gemini AI.
Enforces strict ingredient constraints:
- Uses ONLY user-provided ingredients + allowed pantry staples
- Rejects unprovided main ingredients
- Returns structured JSON validated programmatically
"""

import os
import json
import re
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()


def call_gemini_api(prompt: str) -> Optional[str]:
    """
    Calls Google Gemini REST API using the configured GEMINI_API_KEY.
    Cascades through high-throughput models (gemini-flash-lite-latest, gemini-flash-latest, etc.).
    Returns the generated text string or None on failure.
    """
    if not GEMINI_API_KEY:
        return None

    candidate_models = [
        "gemini-flash-lite-latest",
        "gemini-flash-latest",
        "gemini-2.5-flash"
    ]

    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,  # Low temperature for strict adherence to ingredients
                "maxOutputTokens": 1024
            }
        }

        try:
            resp = requests.post(url, json=payload, timeout=4.5)
            if resp.status_code == 200:
                result = resp.json()
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip()
        except Exception:
            continue

    return None


def parse_recipe_json(raw_text: str) -> Optional[Dict]:
    """Extracts and parses JSON object from LLM response text."""
    if not raw_text:
        return None

    cleaned = raw_text.strip()

    # If wrapped in markdown code fence: ```json ... ```
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()
    else:
        # Find first { and last }
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            cleaned = cleaned[start:end+1]

    try:
        return json.loads(cleaned)
    except Exception:
        return None


def parse_recipe_list_json(raw_text: str) -> List[Dict]:
    """Extracts and parses a JSON array of recipe objects from LLM response."""
    if not raw_text:
        return []

    cleaned = raw_text.strip()
    match = re.search(r"```(?:json)?\s*(\[.*?\]|\{.*?\})\s*```", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()
    else:
        start_arr = cleaned.find("[")
        end_arr = cleaned.rfind("]")
        if start_arr != -1 and end_arr != -1 and end_arr > start_arr:
            cleaned = cleaned[start_arr:end_arr+1]
        else:
            start_obj = cleaned.find("{")
            end_obj = cleaned.rfind("}")
            if start_obj != -1 and end_obj != -1 and end_obj > start_obj:
                cleaned = cleaned[start_obj:end_obj+1]

    try:
        data = json.loads(cleaned)
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict)]
        elif isinstance(data, dict):
            if "recipes" in data and isinstance(data["recipes"], list):
                return [d for d in data["recipes"] if isinstance(d, dict)]
            return [data]
    except Exception:
        pass
    return []


def build_offline_ingredient_recipe(user_ingredients: List[str], servings: int = 2, lang: str = "en") -> Dict:
    """
    Builds a deterministic, authentic culinary recipe exclusively using
    user's provided ingredients + allowed pantry staples.
    """
    user_str_en = ", ".join(user_ingredients)
    has_meat = any(m in [u.lower() for u in user_ingredients] for m in ["chicken", "mutton", "fish", "egg"])
    diet = "Non-Vegetarian" if has_meat else "Vegetarian"

    # Dish naming centered on ingredients
    main_items = [u.title() for u in user_ingredients[:3]]
    recipe_name_en = f"Tawa {' '.join(main_items)} Roast"
    recipe_name_ta = f"சுவையான {' '.join(user_ingredients[:3])} வறுவல்"

    ings_with_qty = [f"{servings * 100}g {u.title()}" for u in user_ingredients]
    ings_with_qty.extend([
        "2 tbsp Cooking Oil",
        "1/2 tsp Mustard Seeds",
        "1/2 tsp Turmeric Powder",
        "1 sprig Curry Leaves",
        "Salt to taste",
        "1/4 cup Water (if needed)"
    ])

    steps_en = [
        f"1. Clean and chop {', '.join(user_ingredients)} into uniform pieces.",
        "2. Heat 2 tbsp oil in a pan; crackle mustard seeds and curry leaves.",
        f"3. Add {user_ingredients[0]} with a pinch of turmeric and salt. Sauté on medium flame.",
    ]
    if len(user_ingredients) > 1:
        steps_en.append(f"4. Add {', '.join(user_ingredients[1:])} and cook until tender and roasted through.")
    steps_en.append(f"5. Adjust seasoning with salt and pepper. Serve hot!")

    steps_ta = [
        f"1. {', '.join(user_ingredients)} ஆகியவற்றை நன்றாகக் கழுவி நறுக்கிக் கொள்ளவும்.",
        "2. கடாயில் எண்ணெய் ஊற்றி கடுகு, கருவேப்பிலை தாளிக்கவும்.",
        f"3. நறுக்கிய {user_ingredients[0]}, மஞ்சள் தூள், உப்பு சேர்த்து மிதமான தீயில் வதக்கவும்.",
        "4. மற்ற பொருட்களையும் சேர்த்து சுருள வதக்கி சூடாகப் பரிமாறவும்!"
    ]

    return {
        "recipe_name": recipe_name_en,
        "recipe_name_ta": recipe_name_ta,
        "provided_ingredients": user_ingredients,
        "pantry_ingredients": ["oil", "mustard", "turmeric", "curry leaf", "salt", "water"],
        "missing_ingredients": [],
        "used_ingredients": user_ingredients + ["oil", "mustard", "turmeric", "curry leaf", "salt"],
        "ingredients_with_quantities": ings_with_qty,
        "steps": steps_en if lang == "en" else steps_ta,
        "steps_ta": steps_ta,
        "cooking_time": 20,
        "difficulty": "Easy",
        "diet": diet,
        "category": "Lunch",
        "valid": True
    }


def generate_ingredient_constrained_recipe(
    user_ingredients: List[str],
    servings: int = 2,
    lang: str = "en"
) -> Dict:
    """
    Generates recipe strictly respecting user's available ingredients using Gemini AI.
    Follows exact constraints from Requirement 6 & 7:
    - ONLY user-provided ingredients used as main/non-pantry ingredients
    - NEVER substitute unrelated ingredients
    - NEVER introduce missing major ingredients
    - Programmatically validates returned recipe
    """
    from src.recipe_validator import validate_recipe

    user_ing_str = ", ".join(user_ingredients)

    prompt = f"""You are an ingredient-constrained recipe generator.

The user's available ingredients are the ONLY ingredients that may be used as main/non-pantry ingredients.

Generate a recipe that uses the provided ingredients.

Never substitute unrelated ingredients.

Never introduce missing major ingredients.

Never generate a recipe just because it is a common recipe.

If no suitable recipe can be created from the available ingredients, return:
'No suitable recipe found with the provided ingredients.'

Do not silently add missing ingredients.

USER'S AVAILABLE INGREDIENTS:
{user_ing_str}

ALLOWED BASIC PANTRY INGREDIENTS (ONLY THESE MAY BE ASSUMED):
salt, water, cooking oil, mustard seeds, cumin seeds, turmeric powder, black pepper, red chilli powder, coriander powder, curry leaves, asafoetida.

DO NOT use or assume rice, rava, wheat flour, dosa batter, dal, paneer, potato, onion, garlic, ginger, meat, or vegetables UNLESS listed in USER'S AVAILABLE INGREDIENTS above.

RETURN STRICT JSON FORMAT ONLY (NO MARKDOWN TEXT, ONLY RAW JSON):
{{
  "recipe_name": "Descriptive Recipe Name in English",
  "recipe_name_ta": "Recipe Name in Tamil",
  "provided_ingredients": ["exact user ingredients used"],
  "pantry_ingredients": ["allowed pantry items used"],
  "missing_ingredients": [],
  "used_ingredients": ["all ingredients in recipe"],
  "ingredients_with_quantities": [
    "quantity and ingredient 1",
    "quantity and ingredient 2"
  ],
  "steps": [
    "Step 1 instructions",
    "Step 2 instructions"
  ],
  "steps_ta": [
    "செய்முறை படி 1",
    "செய்முறை படி 2"
  ],
  "cooking_time": 20,
  "difficulty": "Easy",
  "diet": "Non-Vegetarian or Vegetarian",
  "category": "Breakfast or Lunch or Snacks or Dinner",
  "valid": true
}}
"""

    raw_response = call_gemini_api(prompt)

    if raw_response:
        if "no suitable recipe found" in raw_response.lower():
            return {
                "recipe_name": "No Suitable Recipe Found",
                "valid": False,
                "rejection_reason": "No suitable recipe can be created with the provided ingredients alone."
            }

        parsed = parse_recipe_json(raw_response)
        if parsed and isinstance(parsed, dict):
            # PROGRAMMATIC VALIDATION
            validation = validate_recipe(parsed, user_ingredients)
            if validation["valid"]:
                parsed["valid"] = True
                parsed["provided_ingredients"] = validation["provided_ingredients"]
                parsed["pantry_ingredients"] = validation["pantry_ingredients"]
                parsed["missing_ingredients"] = []
                parsed["used_ingredients"] = validation["used_ingredients"]
                return parsed

            # If invalid (e.g. Gemini added an unprovided major ingredient), try one strict retry
            retry_prompt = prompt + f"""
IMPORTANT CORRECTION:
Your previous attempt '{validation["recipe_name"]}' was INVALID because it added unprovided major ingredients: {validation["missing_ingredients"]}.
You MUST completely eliminate these unprovided ingredients. ONLY use: {user_ing_str} and allowed pantry items (salt, oil, water, turmeric, pepper, cumin, mustard, curry leaves).
"""
            raw_retry = call_gemini_api(retry_prompt)
            if raw_retry:
                parsed_retry = parse_recipe_json(raw_retry)
                if parsed_retry and isinstance(parsed_retry, dict):
                    val_retry = validate_recipe(parsed_retry, user_ingredients)
                    if val_retry["valid"]:
                        parsed_retry["valid"] = True
                        parsed_retry["provided_ingredients"] = val_retry["provided_ingredients"]
                        parsed_retry["pantry_ingredients"] = val_retry["pantry_ingredients"]
                        parsed_retry["missing_ingredients"] = []
                        parsed_retry["used_ingredients"] = val_retry["used_ingredients"]
                        return parsed_retry

    # Deterministic fallback centered strictly on user's ingredients
    fallback = build_offline_ingredient_recipe(user_ingredients, servings, lang)
    val_fallback = validate_recipe(fallback, user_ingredients)
    fallback["valid"] = val_fallback["valid"]
    return fallback


def build_offline_ingredient_recipe_variations(
    user_ingredients: List[str],
    count: int = 3,
    servings: int = 2,
    lang: str = "en"
) -> List[Dict]:
    """
    Builds distinct authentic culinary recipe variations exclusively using
    user's provided ingredients + allowed pantry staples.
    """
    from src.recipe_validator import validate_recipe
    from src.ingredient_utils import get_tamil_ingredient_name

    has_meat = any(m in [u.lower() for u in user_ingredients] for m in ["chicken", "mutton", "fish", "egg"])
    diet = "Non-Vegetarian" if has_meat else "Vegetarian"
    items_title = " ".join([u.title() for u in user_ingredients[:3]])
    items_ta = " ".join([get_tamil_ingredient_name(u) for u in user_ingredients[:3]])
    user_ings_ta = [get_tamil_ingredient_name(u) for u in user_ingredients]

    templates = [
        {
            "name_en": f"Spicy {items_title} Roast",
            "name_ta": f"காரசாரமான {items_ta} வறுவல்",
            "desc": f"A rich and spicy traditional pan roast infused with curry leaves and cracked pepper.",
            "prep_time": 10,
            "cooking_time": 20,
            "difficulty": "Easy",
            "category": "Main Course",
            "style": "roast"
        },
        {
            "name_en": f"Tawa {items_title} Pepper Stir-Fry",
            "name_ta": f"தவா {items_ta} மிளகு வதக்கல்",
            "desc": f"Crisp pan-tossed stir fry sautéed with mustard, cumin, and freshly crushed black pepper.",
            "prep_time": 8,
            "cooking_time": 15,
            "difficulty": "Easy",
            "category": "Sides",
            "style": "stir_fry"
        },
        {
            "name_en": f"Homestyle {items_title} Masala Gravy",
            "name_ta": f"நாட்டுப்புற {items_ta} மசாலா குழம்பு",
            "desc": f"Comforting homestyle simmered gravy bursting with authentic South Indian rustic aromas.",
            "prep_time": 12,
            "cooking_time": 25,
            "difficulty": "Medium",
            "category": "Lunch",
            "style": "gravy"
        },
        {
            "name_en": f"Chettinad Style {items_title} Sukka",
            "name_ta": f"செட்டிநாடு {items_ta} சுக்கா",
            "desc": f"Dry sautéed aromatic specialty loaded with fragrant roasted spices and curry leaves.",
            "prep_time": 10,
            "cooking_time": 22,
            "difficulty": "Easy",
            "category": "Dinner",
            "style": "sukka"
        }
    ]

    results = []
    for tmpl in templates[:count]:
        ings_qty = [f"{servings * 100}g {u.title()}" for u in user_ingredients]
        ings_qty.extend([
            "2 tbsp Cooking Oil",
            "1/2 tsp Mustard Seeds",
            "1/2 tsp Cumin Seeds",
            "1/2 tsp Turmeric Powder",
            "1 tsp Black Pepper Powder",
            "1 sprig Curry Leaves",
            "Salt to taste"
        ])
        if tmpl["style"] == "gravy":
            ings_qty.append("1 cup Water")

        steps_en = [
            f"1. Prep and wash {', '.join(user_ingredients)} thoroughly.",
            "2. Heat oil in a pan; crackle mustard seeds, cumin seeds, and fresh curry leaves.",
            f"3. Add {user_ingredients[0]} along with turmeric powder and salt. Sauté on medium flame."
        ]
        if len(user_ingredients) > 1:
            steps_en.append(f"4. Add remaining ingredients ({', '.join(user_ingredients[1:])}) and cook until tender.")
        if tmpl["style"] == "gravy":
            steps_en.append("5. Pour water, cover, and simmer for 10 minutes until thick and flavorful.")
        else:
            steps_en.append("5. Sprinkle freshly ground black pepper and roast until crisp and fragrant.")
        steps_en.append("6. Remove from flame and serve piping hot!")

        steps_ta = [
            f"1. {', '.join(user_ings_ta)} ஆகியவற்றை நன்கு கழுவி நறுக்கி வைக்கவும்.",
            "2. கடாயில் எண்ணெய் ஊற்றி கடுகு, சீரகம், கருவேப்பிலை தாளிக்கவும்.",
            f"3. நறுக்கிய {user_ings_ta[0]}, மஞ்சள் தூள் மற்றும் உப்பு சேர்த்து வதக்கவும்.",
            "4. மற்ற பொருட்களையும் சேர்த்து நன்கு வெந்து மணம் வரும் வரை கிளறி இறக்கவும்."
        ]

        rec = {
            "recipe_name": tmpl["name_en"],
            "recipe_name_ta": tmpl["name_ta"],
            "description": tmpl["desc"],
            "prep_time": tmpl["prep_time"],
            "cooking_time": tmpl["cooking_time"],
            "difficulty": tmpl["difficulty"],
            "diet": diet,
            "category": tmpl["category"],
            "provided_ingredients": user_ingredients,
            "pantry_ingredients": ["oil", "mustard", "cumin", "turmeric", "pepper", "curry leaf", "salt"],
            "missing_ingredients": [],
            "used_ingredients": user_ingredients + ["oil", "mustard", "cumin", "turmeric", "pepper", "curry leaf", "salt"],
            "ingredients_with_quantities": ings_qty,
            "steps": steps_en if lang == "en" else steps_ta,
            "steps_ta": steps_ta,
            "valid": True
        }
        val = validate_recipe(rec, user_ingredients)
        if val["valid"]:
            rec["valid"] = True
            results.append(rec)

    return results


def generate_multiple_ingredient_recipes(
    user_ingredients: List[str],
    count: int = 3,
    servings: int = 2,
    lang: str = "en"
) -> List[Dict]:
    """
    Generates 2 to 4 distinct, authentic recipes strictly using user's provided ingredients
    plus allowed basic pantry staples. Every recipe is programmatically validated.
    """
    from src.recipe_validator import validate_recipe

    if not user_ingredients:
        return []

    user_ing_str = ", ".join(user_ingredients)

    lang_instruction = (
        "5. LANGUAGE REQUIREMENT: Output recipe names, descriptions, ingredients, and instructions ENTIRELY in English. Do NOT include any Tamil text."
        if lang == "en" else
        "5. LANGUAGE REQUIREMENT: Output recipe names, descriptions, ingredients, and instructions ENTIRELY in Tamil (தமிழ்). Do NOT include English text in instructions."
    )

    prompt = f"""You are an expert Tamil Nadu chef and strict ingredient-constrained recipe generator.

GENERATE {count} DISTINCT, AUTHENTIC RECIPES that can be made using ONLY the user's available ingredients plus allowed basic pantry staples.

STRICT CONSTRAINTS:
1. ONLY user-provided ingredients can be used as main ingredients.
2. ALLOWED BASIC PANTRY STAPLES (ONLY THESE): salt, water, cooking oil, mustard seeds, cumin seeds, turmeric powder, black pepper, red chilli powder, coriander powder, curry leaves, asafoetida.
3. NEVER introduce missing major ingredients like rice, dal, rava, wheat flour, dosa batter, potato, paneer, onion, ginger, garlic, or meat UNLESS explicitly listed below.
4. Each recipe must be a distinct dish (e.g. one roast, one stir fry, one curry).
{lang_instruction}

USER'S AVAILABLE INGREDIENTS:
{user_ing_str}

RETURN STRICT JSON ARRAY OF {count} OBJECTS ONLY (NO MARKDOWN TEXT, ONLY RAW JSON):
[
  {{
    "recipe_name": "Distinct Dish Name in English",
    "recipe_name_ta": "Dish Name in Tamil",
    "description": "Short 1-sentence appetizing description",
    "prep_time": 10,
    "cooking_time": 20,
    "difficulty": "Easy",
    "diet": "Non-Vegetarian or Vegetarian",
    "category": "Main Course or Lunch or Dinner",
    "provided_ingredients": ["exact user ingredients used"],
    "pantry_ingredients": ["allowed pantry items used"],
    "missing_ingredients": [],
    "used_ingredients": ["all ingredients in recipe"],
    "ingredients_with_quantities": [
      "quantity and ingredient 1",
      "quantity and ingredient 2"
    ],
    "steps": [
      "Step 1 instructions",
      "Step 2 instructions"
    ],
    "steps_ta": [
      "செய்முறை படி 1",
      "செய்முறை படி 2"
    ],
    "valid": true
  }}
]
"""

    valid_recipes = []
    raw_response = call_gemini_api(prompt)

    if raw_response and "no suitable recipe found" not in raw_response.lower():
        parsed_list = parse_recipe_list_json(raw_response)
        for p in parsed_list:
            if isinstance(p, dict):
                val = validate_recipe(p, user_ingredients)
                if val["valid"]:
                    p["valid"] = True
                    p["provided_ingredients"] = val["provided_ingredients"]
                    p["pantry_ingredients"] = val["pantry_ingredients"]
                    p["missing_ingredients"] = []
                    p["used_ingredients"] = val["used_ingredients"]
                    if not p.get("description"):
                        p["description"] = f"Authentic Tamil dish made with {user_ing_str}."
                    valid_recipes.append(p)
                    if len(valid_recipes) >= count:
                        break

    # If Gemini returned fewer valid recipes than requested, supplement with deterministic valid variations
    if len(valid_recipes) < count:
        fallbacks = build_offline_ingredient_recipe_variations(user_ingredients, count=count, servings=servings, lang=lang)
        existing_names = {r.get("recipe_name", "").lower() for r in valid_recipes}
        for fb in fallbacks:
            if fb["recipe_name"].lower() not in existing_names:
                valid_recipes.append(fb)
                existing_names.add(fb["recipe_name"].lower())
                if len(valid_recipes) >= count:
                    break

    return valid_recipes[:count]


def generate_fallback_recipe(recipe: Dict, servings: int = 2, lang: str = "ta") -> Dict:
    """Generates clean structured recipe directly from dataset without calling API."""
    if lang == "ta":
        recipe_name = recipe.get("name_ta", recipe.get("name_en", ""))
        ingredients = recipe.get("ingredients_ta", recipe.get("ingredients_en", ""))
        instructions = recipe.get("instructions_ta", recipe.get("instructions_en", ""))
        tip = f"குறிப்பு: {recipe_name} சமைக்கும் போது மிதமான தீயில் பொறுமையாக வதக்கினால் சுவை மற்றும் மணம் கூடுதலாக இருக்கும்."
        sub_text = "இல்லாத பொருட்களுக்கு பதிலாக உங்கள் சமையலறையில் உள்ள சாதாரண மசாலாக்களைப் பயன்படுத்தலாம்."

        content = f"""
### 🛒 தேவையான பொருட்கள் ({servings} நபர்களுக்கு)
{ingredients}

### 👨‍🍳 சமைக்கும் செய்முறை
{instructions}

### 💡 சமையல் குறிப்பு
{tip}

### 🔄 மாற்றுப் பொருட்கள்
{sub_text}
"""
    else:
        recipe_name = recipe.get("name_en", "")
        ingredients = recipe.get("ingredients_en", "")
        instructions = recipe.get("instructions_en", "")
        tip = f"Chef's Tip: For best results with {recipe_name}, cook over medium flame and sauté aromatics until fragrant."
        sub_text = "You can substitute missing spices with everyday pantry staples."

        content = f"""
### 🛒 Ingredients (Scaled for {servings} Servings)
{ingredients}

### 👨‍🍳 Step-by-Step Instructions
{instructions}

### 💡 Chef's Cooking Tip
{tip}

### 🔄 Optional Substitutions
{sub_text}
"""

    return {
        "is_ai_customized": False,
        "content": content,
        "notice": "📋 **பாரம்பரிய செய்முறை (Authentic Recipe):**" if lang == "ta" else "📋 **Authentic Recipe:**"
    }


def customize_recipe_with_llm(
    recipe: Dict,
    user_ingredients: List[str],
    servings: int = 2,
    lang: str = "ta"
) -> Dict:
    """Customizes existing recipe scaling servings with LLM."""
    recipe_name = recipe.get("name_ta" if lang == "ta" else "name_en", "")
    raw_ings = recipe.get("ingredients_ta" if lang == "ta" else "ingredients_en", "")
    raw_inst = recipe.get("instructions_ta" if lang == "ta" else "instructions_en", "")
    matched = ", ".join(recipe.get("matched_ingredients", []))
    missing = ", ".join(recipe.get("missing_ingredients", []))

    if lang == "ta":
        prompt = f"""நீங்கள் ஒரு சிறந்த பாரம்பரிய தமிழ்நாடு சமையல் கலைஞர் (Expert Tamil Chef).
தேர்வு செய்யப்பட்ட உணவை பயனருக்கு ஏற்றவாறு மாற்றி அமைத்துத் தரவும்.

உணவு விவரம்:
- பெயர்: {recipe_name}
- மூலப்பொருட்கள்:
{raw_ings}
- அடிப்படை செய்முறை:
{raw_inst}

பயனர் விவரம்:
- பயனரிடம் உள்ள பொருட்கள்: {matched}
- இல்லாத பொருட்கள்: {missing}
- சமைக்க வேண்டிய நபர்களின் எண்ணிக்கை: {servings}

கட்டளைகள்:
1. {servings} நபர்களுக்கு தேவையான அளவு பொருட்களை அளவிடவும்.
2. பயனரிடம் உள்ள பொருட்களை முன்னிலைப்படுத்தி தெளிவான எளிய தமிழ் செய்முறையைத் தரவும்.
3. ஒரு அருமையான சமையல் குறிப்பு (Chef Tip) தரவும்.

வடிவம் (Strict Markdown in Tamil):
### 🛒 தேவையான பொருட்கள் ({servings} நபர்களுக்கு)
(புல்லட் பாயிண்டுகளாக அளவுகளுடன்)

### 👨‍🍳 சமைக்கும் செய்முறை
(எண் வரிசையில் தெளிவான வழிமுறைகள்)

### 💡 சமையல் குறிப்பு (Chef Tip)
"""
    else:
        prompt = f"""You are an expert Tamil Nadu traditional chef.
Customize the selected Tamil recipe for the user's requested serving size and available ingredients.

RECIPE:
- Dish: {recipe_name}
- Original Ingredients:
{raw_ings}
- Original Instructions:
{raw_inst}

USER DETAILS:
- Available: {matched}
- Missing: {missing}
- Desired Servings: {servings}

INSTRUCTIONS:
1. Scale ingredient quantities for {servings} servings.
2. Emphasize available ingredients with clear step-by-step instructions.
3. Provide one practical chef's tip.

FORMAT (STRICT MARKDOWN):
### 🛒 Ingredients (for {servings} servings)
### 👨‍🍳 Step-by-Step Instructions
### 💡 Chef's Cooking Tip
"""

    ai_text = call_gemini_api(prompt)

    if ai_text:
        notice = "✨ **AI மூலம் மாற்றி அமைக்கப்பட்ட செய்முறை (Powered by Google Gemini AI):**" if lang == "ta" else "✨ **AI Customized Recipe (Powered by Google Gemini AI):**"
        return {
            "is_ai_customized": True,
            "content": ai_text,
            "notice": notice
        }

    return generate_fallback_recipe(recipe, servings, lang)
