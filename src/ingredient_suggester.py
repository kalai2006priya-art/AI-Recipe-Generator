"""
ingredient_suggester.py
-----------------------
Intelligent, compact culinary suggestion engine for "You can also add".
Provides elegant, non-intrusive recommendations with cohesive culinary rationale,
guaranteeing 100% strict language isolation (zero Tamil in English mode, zero English in Tamil mode).
"""

from typing import List, Dict, Optional
from src.ingredient_utils import clean_single_word, is_ingredient_match, is_pantry_ingredient

CULINARY_PAIRINGS = {
    "chicken": [
        ("tomato", "தக்காளி", "Adds juicy richness and tangy depth."),
        ("garlic", "பூண்டு", "Brings bold savory depth and aroma."),
        ("curry leaves", "கருவேப்பிலை", "Adds signature fragrant tempering."),
        ("onion", "வெங்காயம்", "Adds sweet caramelized body to the gravy."),
        ("ginger", "இஞ்சி", "Adds warming spice and tenderizes meat.")
    ],
    "egg": [
        ("onion", "வெங்காயம்", "Creates sweet caramelized homestyle texture."),
        ("tomato", "தக்காளி", "Adds luscious tangy coating masala."),
        ("pepper", "மிளகு", "Adds sharp pungent traditional heat.")
    ],
    "fish": [
        ("garlic", "பூண்டு", "Brings rich aroma and aids digestion."),
        ("tamarind", "புளி", "Adds authentic traditional tangy sourness."),
        ("shallot", "சின்ன வெங்காயம்", "Adds sweetness to village-style gravy.")
    ],
    "tomato": [
        ("garlic", "பூண்டு", "Brings savory depth that balances tanginess."),
        ("curry leaves", "கருவேப்பிலை", "Tempered fragrance for authentic curries."),
        ("onion", "வெங்காயம்", "Classic sweet pairing for thick gravies.")
    ],
    "onion": [
        ("tomato", "தக்காளி", "Juicy acidity balancing onion sweetness."),
        ("green chilli", "பச்சை மிளகாய்", "Crisp pungent heat for rich dishes."),
        ("curry leaves", "கருவேப்பிலை", "Traditional tempering aroma.")
    ],
    "potato": [
        ("onion", "வெங்காயம்", "Essential sweet base for south Indian roasts."),
        ("curry leaves", "கருவேப்பிலை", "Fragrant tempering for crispy fries."),
        ("garlic", "பூண்டு", "Bold roasted aroma elevating the fry.")
    ],
    "rava": [
        ("onion", "வெங்காயம்", "Sweet crunch defining traditional upma."),
        ("green chilli", "பச்சை மிளகாய்", "Sharp heat cutting through roasted rava."),
        ("carrot", "கேரட்", "Sweet crisp color and wholesome nutrition.")
    ],
    "curd": [
        ("rice", "அரிசி", "Creates comforting South Indian Curd Rice."),
        ("ginger", "இஞ்சி", "Warming digestive balance against cooling curd."),
        ("cucumber", "வெள்ளரிக்காய்", "Refreshing cooling crunch for pachadi.")
    ],
    "rice": [
        ("curd", "தயிர்", "Creates classic soothing Thayir Sadam."),
        ("lemon", "எலுமிச்சை", "Unlocks zesty Tamil Lemon Rice."),
        ("tomato", "தக்காளி", "Creates aromatic, tangy Thakkali Sadam.")
    ]
}


def get_compact_ingredient_suggestions(
    user_ingredients: List[str],
    matched_recipes: Optional[List[Dict]] = None,
    lang: str = "en",
    max_items: int = 3
) -> Optional[Dict]:
    """
    Computes a single, compact recommendation bar:
    Example output (English):
    {
        "items": ["Tomato", "Garlic", "Curry Leaves"],
        "display_str": "Tomato • Garlic • Curry Leaves",
        "reason": "These extra ingredients can improve the flavour and open up more recipe options.",
        "raw_tokens": ["tomato", "garlic", "curry leaves"]
    }
    """
    if not user_ingredients:
        return None

    clean_user = [clean_single_word(u).lower() for u in user_ingredients if u]
    chosen = []
    seen = set(clean_user)

    # 1. Match pairings
    for u_ing in clean_user:
        for key, pairings in CULINARY_PAIRINGS.items():
            if is_ingredient_match(u_ing, key) or key in u_ing:
                for en_name, ta_name, reason_en in pairings:
                    norm = clean_single_word(en_name).lower()
                    if norm not in seen and not any(is_ingredient_match(norm, x) for x in clean_user):
                        seen.add(norm)
                        chosen.append((en_name, ta_name, norm))
                        if len(chosen) >= max_items:
                            break
        if len(chosen) >= max_items:
            break

    # 2. Check missing from close database recipes
    if len(chosen) < max_items and matched_recipes:
        for r in matched_recipes:
            missing = r.get("missing_ingredients") or r.get("missing_major_ingredients") or []
            for mis in missing:
                norm = clean_single_word(mis).lower()
                if norm not in seen and not is_pantry_ingredient(norm):
                    seen.add(norm)
                    chosen.append((mis, mis, norm))
                    if len(chosen) >= max_items:
                        break
            if len(chosen) >= max_items:
                break

    # 3. Fallbacks if needed
    if len(chosen) < 2:
        fallbacks = [
            ("coriander", "கொத்தமல்லி"),
            ("garlic", "பூண்டு"),
            ("curry leaves", "கருவேப்பிலை")
        ]
        for en_name, ta_name in fallbacks:
            norm = clean_single_word(en_name).lower()
            if norm not in seen and not any(is_ingredient_match(norm, x) for x in clean_user):
                seen.add(norm)
                chosen.append((en_name, ta_name, norm))
                if len(chosen) >= max_items:
                    break

    if not chosen:
        return None

    # Strict language isolation
    if lang == "ta":
        item_names = [c[1] for c in chosen]
        reason_text = "இவை உங்கள் உணவின் சுவையைக் கூட்டி கூடுதல் சமையல் வாய்ப்புகளைத் தரும்."
    else:
        item_names = [c[0].title() for c in chosen]
        reason_text = "These ingredients can enhance the flavour and open up more recipe options."

    return {
        "items": item_names,
        "display_str": " • ".join(item_names),
        "reason": reason_text,
        "raw_tokens": [c[2] for c in chosen]
    }