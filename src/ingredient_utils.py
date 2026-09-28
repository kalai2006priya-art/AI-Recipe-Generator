"""
ingredient_utils.py
-------------------
Bilingual ingredient normalization and matching supporting both
Tamil (தமிழ்) and English inputs.

Features:
- Translates Tamil ingredient names to canonical normalized tokens
- Normalizes English ingredients (singularization, measurement stripping)
- Comprehensive Tamil kitchen dictionary & English culinary synonyms
"""

import re
from typing import List, Tuple

COMMON_MEASUREMENTS = [
    "cup", "cups", "tbsp", "tablespoon", "tablespoons", "tsp", "teaspoon", "teaspoons",
    "g", "gram", "grams", "kg", "kilogram", "ml", "liter", "liters", "oz", "ounce", "ounces",
    "lb", "pound", "pounds", "pinch", "pinches", "slice", "slices", "piece", "pieces",
    "chopped", "diced", "sliced", "fresh", "grated", "boiled", "fried", "powder", "paste",
    "as required", "to taste", "தேக்கரண்டி", "கப்", "மேஜைக்கரண்டி", "சிட்டிகை"
]

TAMIL_TO_ENGLISH_MAP = {
    "தக்காளி": "tomato",
    "வெங்காயம்": "onion",
    "சின்ன வெங்காயம்": "shallot",
    "உருளைக்கிழங்கு": "potato",
    "உருளை": "potato",
    "பச்சை மிளகாய்": "green chilli",
    "வரமிளகாய்": "red chilli",
    "மிளகாய்": "chilli",
    "பூண்டு": "garlic",
    "இஞ்சி": "ginger",
    "புளி": "tamarind",
    "தேங்காய்": "coconut",
    "தேங்காய்ப்பால்": "coconut milk",
    "துவரம் பருப்பு": "toor dal",
    "துவரம்பருப்பு": "toor dal",
    "பருப்பு": "toor dal",
    "பாசிப்பருப்பு": "moong dal",
    "கடலைப்பருப்பு": "chana dal",
    "உளுத்தம் பருப்பு": "urad dal",
    "உளுந்து": "urad dal",
    "பொட்டுக்கடலை": "roasted gram",
    "சாம்பார் பொடி": "sambar powder",
    "சாம்பார் தூள்": "sambar powder",
    "மஞ்சள்தூள்": "turmeric",
    "மஞ்சள்": "turmeric",
    "கடுகு": "mustard",
    "சீரகம்": "cumin",
    "மிளகு": "pepper",
    "பெருங்காயம்": "asafoetida",
    "கருவேப்பிலை": "curry leaf",
    "கருவேப்பிலை": "curry leaf",
    "கொத்தமல்லி": "coriander",
    "கொத்தமல்லி தழை": "coriander",
    "நெய்": "ghee",
    "எண்ணெய்": "oil",
    "நல்லெண்ணெய்": "sesame oil",
    "அரிசி": "rice",
    "பச்சரிசி": "raw rice",
    "புழுங்கல் அரிசி": "boiled rice",
    "இட்லி அரிசி": "idli rice",
    "சீரக சம்பா": "seeraga samba rice",
    "சீரக சம்பா அரிசி": "seeraga samba rice",
    "ரவை": "rava",
    "சேமியா": "semiya",
    "கோதுமை": "wheat flour",
    "கோதுமை மாவு": "wheat flour",
    "கடலை மாவு": "besan",
    "முருங்கைக்காய்": "drumstick",
    "கத்திரிக்காய்": "brinjal",
    "முட்டைக்கோஸ்": "cabbage",
    "பீன்ஸ்": "beans",
    "கேரட்": "carrot",
    "வெண்டைக்காய்": "okra",
    "சுண்டைக்காய்": "sundakkai vathal",
    "சுண்டைக்காய் வத்தல்": "sundakkai vathal",
    "கொண்டைக்கடலை": "white chana",
    "வெள்ளை கொண்டைக்கடலை": "white chana",
    "வெல்லம்": "jaggery",
    "சர்க்கரை": "sugar",
    "பால்": "milk",
    "தயிர்": "curd",
    "மோர்": "curd",
    "தயிர் சாதம்": "curd",
    "தயிர் வடை": "curd",
    "மோர் குழம்பு": "curd",
    "மோர் தோசை": "curd",
    "தயிர் தோசை": "curd",
    "தயிர் சேமியா": "curd",
    "அரிசி மாவு": "rice flour",
    "தோசை மாவு": "dosa batter",
    "இட்லி மாவு": "idli batter",
    "வெள்ளரிக்காய்": "cucumber",
    "முட்டை": "egg",
    "சிக்கன்": "chicken",
    "கோழி": "chicken",
    "மீன்": "fish",
    "மட்டன்": "mutton",
    "பரோட்டா": "parotta",
    "பன்னீர்": "paneer",
    "முந்திரி": "cashew",
    "திராட்சை": "raisin",
    "ஏலக்காய்": "cardamom",
    "சோம்பு": "fennel",
    "வெந்தயம்": "fenugreek",
    "உப்பு": "salt"
}

SYNONYMS = {
    "toor dal": ["arhar dal", "tuvar dal", "pigeon pea", "dal"],
    "arhar dal": ["toor dal", "tuvar dal", "dal"],
    "chana dal": ["bengal gram", "gram dal", "roasted gram", "pottukadalai"],
    "moong dal": ["yellow lentil", "mung dal", "mung bean"],
    "urad dal": ["black gram", "white urad dal", "split black gram", "ulundu"],
    "besan": ["gram flour", "chickpea flour", "kadalai maavu"],
    "curd": ["yogurt", "yoghurt", "dahi", "thayir", "curds", "buttermilk", "mor", "moru", "chaas"],
    "rava": ["sooji", "semolina", "rava"],
    "semiya": ["vermicelli", "seviyan"],
    "coriander": ["cilantro", "dhania", "kothamalli"],
    "cumin": ["jeera", "seeragam"],
    "mustard": ["rai", "sarson", "mustard seed", "kadugu"],
    "fenugreek": ["methi", "vendhayam"],
    "asafoetida": ["hing", "perungayam"],
    "turmeric": ["haldi", "manjal"],
    "tamarind": ["imli", "tamarind water", "puli"],
    "chilli": ["chili", "green chilli", "red chilli", "milagai"],
    "egg": ["eggs", "boiled egg", "muttai"],
    "potato": ["potatoes", "urulai", "urulaikizhangu"],
    "onion": ["onions", "vengayam", "shallot", "chinna vengayam"],
    "shallot": ["small onion", "chinna vengayam", "pearl onion", "onion"],
    "tomato": ["tomatoes", "thakkali"],
    "coconut": ["thengai", "grated coconut"],
    "ghee": ["nei", "clarified butter"],
    "pepper": ["black pepper", "milagu"]
}


ALLOWED_PANTRY_INGREDIENTS = {
    # Basic liquids & cooking fats
    "salt", "water", "oil", "cooking oil", "vegetable oil", "refined oil",
    "sesame oil", "gingelly oil", "ghee", "clarified butter",
    # Basic whole seeds & tempering
    "mustard", "mustard seed", "mustard seeds", "kadugu", "rai",
    "cumin", "cumin seed", "cumin seeds", "jeera", "seeragam",
    "curry leaf", "curry leaves", "karuveppilai",
    "asafoetida", "hing", "perungayam",
    # Basic spice powders
    "turmeric", "turmeric powder", "haldi", "manjal",
    "pepper", "black pepper", "black pepper powder", "pepper powder", "milagu",
    "chilli powder", "red chilli powder", "kashmiri chilli powder", "milagai thool",
    "coriander powder", "dhania powder", "malli thool",
    "garam masala", "sambar powder", "rasam powder",
    # Fresh herb garnish
    "coriander", "coriander leaf", "coriander leaves", "cilantro", "kothamalli"
}


def is_pantry_ingredient(ingredient: str) -> bool:
    """Checks if an ingredient is an allowed basic pantry item."""
    if not ingredient:
        return False
    norm = clean_single_word(ingredient).lower()
    if norm in ALLOWED_PANTRY_INGREDIENTS:
        return True
    for p in ALLOWED_PANTRY_INGREDIENTS:
        if is_ingredient_match(norm, p):
            return True
    return False


def clean_single_word(text: str) -> str:
    """Normalizes a single ingredient token."""
    if not text:
        return ""

    text = text.strip()

    # Check direct Tamil match first
    for ta_word, en_word in TAMIL_TO_ENGLISH_MAP.items():
        if ta_word in text:
            return en_word

    # English cleaning
    t_lower = text.lower()
    t_lower = re.sub(r"[\d/\\,\.\-\:\*\+]", " ", t_lower)
    words = [w for w in t_lower.split() if w not in COMMON_MEASUREMENTS and len(w) > 1]
    cleaned = " ".join(words).strip()

    if not cleaned:
        return ""

    # Specific normalization rules (Requirement 10)
    if "chicken" in cleaned:
        return "chicken"
    if any(k in cleaned for k in ["curd", "yogurt", "yoghurt", "dahi", "thayir"]):
        return "curd"
    if cleaned in ["chillies", "chilies", "chili", "chilli"]:
        return "chilli"
    if cleaned in ["tomatoes", "tomato"]:
        return "tomato"
    if cleaned in ["potatoes", "potato"]:
        return "potato"
    if cleaned in ["onions", "onion"]:
        return "onion"
    if cleaned in ["eggs", "egg"]:
        return "egg"
    if cleaned in ["rices", "rice"]:
        return "rice"
    if cleaned in ["leaves", "leaf"]:
        return "curry leaf" if "curry" in text.lower() else "coriander"

    # Singularization
    if cleaned.endswith("tomatoes"):
        cleaned = cleaned[:-2]
    elif cleaned.endswith("potatoes"):
        cleaned = cleaned[:-2]
    elif cleaned.endswith("onions"):
        cleaned = cleaned[:-1]
    elif cleaned.endswith("eggs"):
        cleaned = cleaned[:-1]
    elif cleaned.endswith("chillies") or cleaned.endswith("chilies"):
        cleaned = "chilli"
    elif cleaned.endswith("leaves"):
        cleaned = cleaned[:-3] + "f"
    elif cleaned.endswith("s") and not cleaned.endswith("ss") and not cleaned.endswith("us"):
        cleaned = cleaned[:-1]

    return cleaned


def parse_user_ingredients(user_input: str) -> List[str]:
    """
    Parses comma, space, or newline-separated input in either Tamil or English
    and returns a list of canonical ingredient names.
    """
    if not user_input or not isinstance(user_input, str):
        return []

    # Split by comma or newline
    raw_items = re.split(r"[\,\n\r]+", user_input)
    cleaned_items = []

    for item in raw_items:
        clean = clean_single_word(item)
        if clean and clean not in cleaned_items:
            cleaned_items.append(clean)

    return cleaned_items


def is_ingredient_match(user_ing: str, recipe_ing: str) -> bool:
    """Checks if user ingredient matches recipe ingredient."""
    if not user_ing or not recipe_ing:
        return False

    u = user_ing.lower().strip()
    r = recipe_ing.lower().strip()

    if u == r:
        return True

    if re.search(r"\b" + re.escape(u) + r"\b", r) or re.search(r"\b" + re.escape(r) + r"\b", u):
        return True

    if u in SYNONYMS:
        for syn in SYNONYMS[u]:
            if syn == r or re.search(r"\b" + re.escape(syn) + r"\b", r):
                return True

    if r in SYNONYMS:
        for syn in SYNONYMS[r]:
            if syn == u or re.search(r"\b" + re.escape(syn) + r"\b", u):
                return True

    return False


def match_ingredients(user_ingredients: List[str], recipe_ingredients: List[str]) -> Tuple[List[str], List[str]]:
    """Separates recipe ingredients into matched and missing lists."""
    matched = []
    missing = []

    for r_ing in recipe_ingredients:
        has_match = any(is_ingredient_match(u_ing, r_ing) for u_ing in user_ingredients)
        if has_match:
            matched.append(r_ing)
        else:
            missing.append(r_ing)

    return matched, missing


ENGLISH_TO_TAMIL_PRIMARY_MAP = {
    "chicken": "சிக்கன்",
    "mutton": "மட்டன்",
    "fish": "மீன்",
    "egg": "முட்டை",
    "tomato": "தக்காளி",
    "onion": "வெங்காயம்",
    "shallot": "சின்ன வெங்காயம்",
    "potato": "உருளைக்கிழங்கு",
    "green chilli": "பச்சை மிளகாய்",
    "red chilli": "வரமிளகாய்",
    "chilli": "மிளகாய்",
    "garlic": "பூண்டு",
    "ginger": "இஞ்சி",
    "tamarind": "புளி",
    "coconut": "தேங்காய்",
    "coconut milk": "தேங்காய்ப்பால்",
    "toor dal": "துவரம் பருப்பு",
    "moong dal": "பாசிப்பருப்பு",
    "chana dal": "கடலைப்பருப்பு",
    "urad dal": "உளுத்தம் பருப்பு",
    "roasted gram": "பொட்டுக்கடலை",
    "sambar powder": "சாம்பார் பொடி",
    "turmeric": "மஞ்சள்தூள்",
    "mustard": "கடுகு",
    "cumin": "சீரகம்",
    "pepper": "மிளகு",
    "asafoetida": "பெருங்காயம்",
    "curry leaf": "கருவேப்பிலை",
    "coriander": "கொத்தமல்லி",
    "ghee": "நெய்",
    "oil": "எண்ணெய்",
    "sesame oil": "நல்லெண்ணெய்",
    "curd": "தயிர்",
    "milk": "பால்",
    "rice": "அரிசி",
    "idli rice": "இட்லி அரிசி",
    "dosa rice": "தோசை அரிசி",
    "raw rice": "பச்சரிசி",
    "boiled rice": "புழுங்கல் அரிசி",
    "rava": "ரவை",
    "semiya": "சேமியா",
    "parotta": "பரோட்டா",
    "paneer": "பன்னீர்",
    "lemon": "எலுமிச்சை",
    "carrot": "கேரட்",
    "beans": "பீன்ஸ்",
    "cabbage": "முட்டைக்கோஸ்",
    "brinjal": "கத்தரிக்காய்",
    "drumstick": "முருங்கைக்காய்",
    "okra": "வெண்டைக்காய்",
    "cucumber": "வெள்ளரிக்காய்",
    "cashew": "முந்திரி",
    "cardamom": "ஏலக்காய்",
    "fennel": "சோம்பு",
    "fenugreek": "வெந்தயம்",
    "salt": "உப்பு",
    "water": "தண்ணீர்"
}


def get_tamil_ingredient_name(token: str) -> str:
    """Returns the authentic Tamil name for an English ingredient token if available."""
    if not token:
        return ""
    cleaned = clean_single_word(token).lower()
    if cleaned in ENGLISH_TO_TAMIL_PRIMARY_MAP:
        return ENGLISH_TO_TAMIL_PRIMARY_MAP[cleaned]
    # Check if already in Tamil
    if re.search(r"[\u0B80-\u0BFF]", token):
        return token
    # Match synonyms
    for en_key, ta_val in ENGLISH_TO_TAMIL_PRIMARY_MAP.items():
        if is_ingredient_match(cleaned, en_key):
            return ta_val
    return token

