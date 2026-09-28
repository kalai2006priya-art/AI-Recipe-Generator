"""
download_and_preprocess.py
--------------------------
Downloads and preprocesses both Indian and International recipe datasets.

Features:
- Includes 3,700+ authentic Indian recipes (Sambar, Chutney, Rasam, Dosa, Biryani, Curries, etc.)
- Includes 2,000+ International recipes (Italian, Continental, Mexican, Asian, etc.)
- Allows users to filter by Cuisine: Indian, Italian, Mexican, Continental, Asian, or All.
- Cleans and normalizes ingredients for fast Python matching.
- Generates clean instructions for both datasets.
- Saves combined dataset to data/processed_recipes.csv.
"""

import ast
import os
import re
import urllib.request
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
INDIAN_CSV_PATH = os.path.join(DATA_DIR, "indian_recipes_raw.csv")
GLOBAL_CSV_PATH = os.path.join(DATA_DIR, "global_recipes_raw.csv")
PROCESSED_CSV_PATH = os.path.join(DATA_DIR, "processed_recipes.csv")

# Public Dataset URLs
INDIAN_DATASET_URL = "https://raw.githubusercontent.com/Pkaran26/recipe-ingredient-rag-pipeline/main/Cleaned_Indian_Food_Dataset.csv"
GLOBAL_DATASET_URL = "https://raw.githubusercontent.com/josephrmartinez/recipe-dataset/main/13k-recipes.csv"

# Common non-vegetarian keywords
NON_VEG_KEYWORDS = [
    "chicken", "beef", "pork", "meat", "bacon", "ham", "turkey",
    "lamb", "fish", "salmon", "tuna", "shrimp", "prawn", "crab",
    "lobster", "anchovy", "prosciutto", "pancetta", "sausage", "veal", "duck", "mutton"
]

MEASUREMENTS = [
    "cup", "cups", "tablespoon", "tablespoons", "tbsp", "teaspoon", "teaspoons", "tsp",
    "pound", "pounds", "lb", "lbs", "ounce", "ounces", "oz", "gram", "grams", "g",
    "kg", "kilogram", "ml", "pinch", "pinches", "clove", "cloves", "slice", "slices",
    "can", "cans", "package", "packages", "bunch", "bunches", "sprig", "sprigs",
    "small", "medium", "large", "chopped", "diced", "minced", "sliced", "fresh",
    "freshly", "ground", "crushed", "grated", "divided", "optional", "to taste", "as required"
]


def download_datasets():
    """Downloads both raw datasets if not already present."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(INDIAN_CSV_PATH):
        print(f"Downloading Indian Food Dataset from:\n  {INDIAN_DATASET_URL}")
        urllib.request.urlretrieve(INDIAN_DATASET_URL, INDIAN_CSV_PATH)
        print("Indian dataset downloaded.")
    else:
        print("Indian dataset already exists.")

    if not os.path.exists(GLOBAL_CSV_PATH):
        print(f"Downloading Global Recipe Dataset from:\n  {GLOBAL_DATASET_URL}")
        urllib.request.urlretrieve(GLOBAL_DATASET_URL, GLOBAL_CSV_PATH)
        print("Global dataset downloaded.")
    else:
        print("Global dataset already exists.")


def sanitize_text(text: str) -> str:
    """Removes unicode fractions and cleans whitespace."""
    if not isinstance(text, str):
        return ""
    replacements = {
        "¼": "1/4", "½": "1/2", "¾": "3/4", "⅓": "1/3", "⅔": "2/3",
        "⅛": "1/8", "⅜": "3/8", "⅝": "5/8", "⅞": "7/8", "–": "-", "—": "-",
        "’": "'", "‘": "'", "“": '"', "”": '"', "…": "..."
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return " ".join(text.split()).strip()


def clean_ingredient_item(raw_item: str) -> str:
    """Cleans an individual ingredient string into a canonical normalized name."""
    text = sanitize_text(raw_item).lower()
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"[\d/\\,\.\-\:\*\+]", " ", text)

    words = text.split()
    filtered = [w for w in words if w not in MEASUREMENTS and len(w) > 1]
    result = " ".join(filtered).strip()

    # Singularization
    if result.endswith("tomatoes"):
        result = result[:-2]
    elif result.endswith("potatoes"):
        result = result[:-2]
    elif result.endswith("onions"):
        result = result[:-1]
    elif result.endswith("eggs"):
        result = result[:-1]
    elif result.endswith("carrots"):
        result = result[:-1]
    elif result.endswith("leaves"):
        result = result[:-3] + "f"
    elif result.endswith("chilies") or result.endswith("chillies"):
        result = "chilli"
    elif result.endswith("s") and not result.endswith("ss") and not result.endswith("us"):
        result = result[:-1]

    return result


def categorize_cuisine(cuisine_raw: str, recipe_name: str) -> str:
    """Groups cuisine into standard categories: Indian, Italian, Mexican, Continental, Asian, Other."""
    text = f"{cuisine_raw} {recipe_name}".lower()
    if any(k in text for k in [
        "indian", "tamil", "kerala", "karnataka", "andhra", "chettinad", "punjabi",
        "bengali", "maharashtrian", "rajasthani", "gujarati", "goan", "sambar",
        "chutney", "rasam", "dosa", "idli", "biryani", "paneer", "dal", "curry", "roti", "paratha"
    ]):
        return "Indian"
    elif "italian" in text or "pasta" in text or "pizza" in text or "risotto" in text:
        return "Italian"
    elif "mexican" in text or "taco" in text or "salsa" in text or "burrito" in text:
        return "Mexican"
    elif any(k in text for k in ["asian", "thai", "chinese", "japanese", "korean", "noodle"]):
        return "Asian"
    elif any(k in text for k in ["continental", "american", "burger", "sandwich", "steak", "roast"]):
        return "Continental"
    else:
        return "Continental"


def generate_indian_instruction_template(recipe_name: str, ingredients_str: str) -> str:
    """Creates a sensible, realistic cooking instruction template for Indian recipes."""
    name_lower = recipe_name.lower()

    if "sambar" in name_lower:
        return (
            "1. Wash and pressure cook toor dal with a pinch of turmeric until soft and mushy.\n"
            "2. In a large pot, boil the vegetables with tamarind extract, turmeric, sambar powder, and salt until tender.\n"
            "3. Add the cooked mashed dal to the simmering vegetable broth and mix well. Let it simmer for 5-7 minutes.\n"
            "4. In a small pan, heat ghee or oil; add mustard seeds, dry red chillies, asafoetida (hing), and fresh curry leaves.\n"
            "5. Pour the aromatic tempering into the sambar, garnish with fresh coriander, and serve hot with rice or idli/dosa!"
        )
    elif "chutney" in name_lower or "pachadi" in name_lower:
        return (
            "1. Heat 1 teaspoon of oil in a pan; roast the dal (urad or chana dal), green chillies, ginger, and main ingredients until fragrant.\n"
            "2. Allow the sautéed ingredients to cool to room temperature.\n"
            "3. Transfer to a blender jar, add salt to taste and a little water, then grind into a smooth or slightly coarse paste.\n"
            "4. Heat a teaspoon of oil in a small pan, crackle mustard seeds, urad dal, and curry leaves.\n"
            "5. Pour the hot tempering over the chutney, mix well, and serve with idli, dosa, or rice!"
        )
    elif "rasam" in name_lower:
        return (
            "1. In a pot, cook crushed tomatoes, green chillies, tamarind extract, turmeric, and rasam powder with 2 cups of water.\n"
            "2. Simmer on medium heat until the raw smell of tamarind goes away (about 7-8 minutes).\n"
            "3. Add cooked dal water (optional) and salt; bring to a gentle froth (do not boil vigorously).\n"
            "4. Temper mustard seeds, cumin seeds, crushed garlic, and curry leaves in hot ghee.\n"
            "5. Pour over the rasam, garnish generously with fresh coriander, and serve hot!"
        )
    elif any(k in name_lower for k in ["biryani", "pulao", "rice"]):
        return (
            "1. Wash and soak basmati rice for 20-30 minutes, then drain.\n"
            "2. Heat ghee/oil in a heavy-bottomed pot. Add whole spices (bay leaf, cloves, cinnamon, cardamom) and sauté onions until golden brown.\n"
            "3. Add ginger-garlic paste, chopped tomatoes, spice powders, and the main vegetables or meat. Sauté for 5 minutes.\n"
            "4. Add the drained rice, required water (1:1.5 ratio), salt, and mint/coriander leaves.\n"
            "5. Cover with a tight lid and cook on low heat for 15-20 minutes until the rice is fragrant, fluffy, and tender."
        )
    elif any(k in name_lower for k in ["curry", "masala", "kurma", "gravy"]):
        return (
            "1. Heat oil in a pan, add cumin seeds and finely chopped onions; sauté until translucent and light golden.\n"
            "2. Add ginger-garlic paste and sauté until the raw aroma disappears.\n"
            "3. Add tomato puree or chopped tomatoes with turmeric, chilli powder, and coriander powder; cook until oil separates.\n"
            "4. Add the main ingredients and water as needed for desired gravy consistency; cover and simmer for 10-15 minutes.\n"
            "5. Stir in a pinch of garam masala and fresh coriander leaves before serving hot with chapati, paratha, or rice."
        )
    else:
        return (
            "1. Clean, peel, and chop all required vegetables and ingredients into uniform pieces.\n"
            "2. Heat oil in a pan, add whole spices or aromatics, and sauté gently on medium flame.\n"
            "3. Add the prepared ingredients along with ground spices and salt; stir well to coat.\n"
            "4. Cook covered on medium-low heat, stirring occasionally, until tender and cooked through.\n"
            "5. Adjust seasoning, garnish with fresh herbs, and serve hot!"
        )


def infer_cooking_time(instructions: str) -> int:
    """Extracts cooking time in minutes from instruction text."""
    matches = re.findall(r"(\d+)\s*(?:minutes|minute|mins|min)\b", instructions.lower())
    if matches:
        times = [int(m) for m in matches if 5 <= int(m) <= 120]
        if times:
            return max(times)
    length = len(instructions)
    if length < 250:
        return 15
    elif length < 600:
        return 30
    else:
        return 45


def infer_meal_type(title: str, ingredients_str: str) -> str:
    """Infers meal type (Breakfast, Lunch, Dinner, Snack)."""
    t = title.lower()
    if any(k in t for k in ["dosa", "idli", "upma", "pongal", "pancake", "waffle", "toast", "oatmeal", "breakfast", "poori"]):
        return "Breakfast"
    elif any(k in t for k in ["chutney", "dip", "samosa", "pakoda", "vada", "snack", "bite", "cookie", "appetizer"]):
        return "Snack"
    elif any(k in t for k in ["biryani", "pulao", "curry", "sambar", "dal", "gravy", "roast", "pasta", "dinner", "kurma"]):
        return "Dinner"
    elif any(k in t for k in ["rice", "salad", "sandwich", "wrap", "soup", "lunch", "kootu", "poriyal"]):
        return "Lunch"
    return "Any"


def infer_diet(cleaned_ingredients: str) -> str:
    """Classifies recipe as Vegetarian or Non-Vegetarian."""
    ing_lower = cleaned_ingredients.lower()
    for meat in NON_VEG_KEYWORDS:
        if re.search(r"\b" + re.escape(meat) + r"\b", ing_lower):
            return "Non-Vegetarian"
    return "Vegetarian"


def calculate_difficulty(total_time: int, ingredient_count: int) -> str:
    if total_time <= 30 and ingredient_count <= 6:
        return "Easy"
    elif total_time <= 60 and ingredient_count <= 10:
        return "Medium"
    else:
        return "Complex"


def process_datasets():
    """Merges Indian and Global recipes with unified schema."""
    print("Loading Indian dataset...")
    df_ind = pd.read_csv(INDIAN_CSV_PATH)
    print(f"Indian dataset raw rows: {len(df_ind)}")

    # Clean Indian dataset
    df_ind = df_ind.dropna(subset=["TranslatedRecipeName", "Cleaned-Ingredients"]).copy()
    df_ind["recipe_name"] = df_ind["TranslatedRecipeName"].apply(sanitize_text)
    df_ind = df_ind.drop_duplicates(subset=["recipe_name"])

    # Clean ingredients
    def clean_ind_ings(val):
        if not isinstance(val, str):
            return ""
        items = val.split(",")
        cleaned = [clean_ingredient_item(it) for it in items]
        cleaned = [x for x in cleaned if len(x) > 1]
        return ", ".join(dict.fromkeys(cleaned))

    df_ind["cleaned_ingredients"] = df_ind["Cleaned-Ingredients"].apply(clean_ind_ings)
    df_ind["ingredients_raw"] = df_ind["TranslatedIngredients"].apply(
        lambda s: "\n".join(f"- {sanitize_text(x)}" for x in str(s).split(",") if x.strip())
    )

    df_ind["cuisine"] = df_ind.apply(
        lambda r: categorize_cuisine(str(r.get("Cuisine", "")), r["recipe_name"]),
        axis=1
    )
    df_ind["cuisine_detail"] = df_ind["Cuisine"].fillna("Indian").astype(str).str.strip()

    # Instructions
    df_ind["instructions"] = df_ind.apply(
        lambda r: generate_indian_instruction_template(r["recipe_name"], r["cleaned_ingredients"]),
        axis=1
    )

    df_ind["total_time"] = pd.to_numeric(df_ind["TotalTimeInMins"], errors="coerce").fillna(35).astype(int)
    # Ensure minimum time 10 mins, cap at 90 mins
    df_ind["total_time"] = df_ind["total_time"].apply(lambda t: 30 if t <= 0 or t > 180 else t)

    df_ind["ingredient_count"] = df_ind["cleaned_ingredients"].apply(
        lambda s: len([x for x in s.split(",") if x.strip()])
    )
    df_ind = df_ind[(df_ind["ingredient_count"] >= 2) & (df_ind["ingredient_count"] <= 16)].copy()

    df_ind["meal_type"] = df_ind.apply(lambda r: infer_meal_type(r["recipe_name"], r["cleaned_ingredients"]), axis=1)
    df_ind["diet"] = df_ind["cleaned_ingredients"].apply(infer_diet)
    df_ind["difficulty"] = df_ind.apply(lambda r: calculate_difficulty(r["total_time"], r["ingredient_count"]), axis=1)
    df_ind["servings"] = 2

    # Now load Global dataset
    print("Loading Global dataset...")
    df_glob = pd.read_csv(GLOBAL_CSV_PATH)
    df_glob = df_glob.dropna(subset=["Title", "Cleaned_Ingredients", "Instructions"]).copy()
    df_glob["recipe_name"] = df_glob["Title"].apply(sanitize_text)
    df_glob = df_glob.drop_duplicates(subset=["recipe_name"])
    df_glob["instructions"] = df_glob["Instructions"].apply(sanitize_text)
    df_glob = df_glob[df_glob["instructions"].str.len() >= 30]

    def parse_glob_ings(val):
        items = re.findall(r"'([^']*)'", str(val)) or str(val).split(",")
        cleaned = [clean_ingredient_item(it) for it in items]
        cleaned = [x for x in cleaned if len(x) > 1]
        return ", ".join(dict.fromkeys(cleaned))

    df_glob["cleaned_ingredients"] = df_glob["Cleaned_Ingredients"].apply(parse_glob_ings)
    df_glob["ingredients_raw"] = df_glob["Ingredients"].apply(
        lambda val: "\n".join(f"- {sanitize_text(x)}" for x in re.findall(r"'([^']*)'", str(val)) if x.strip())
    )
    df_glob["cuisine"] = df_glob["recipe_name"].apply(lambda name: categorize_cuisine("Continental", name))
    df_glob["cuisine_detail"] = df_glob["cuisine"]
    df_glob["total_time"] = df_glob["instructions"].apply(infer_cooking_time)
    df_glob["ingredient_count"] = df_glob["cleaned_ingredients"].apply(
        lambda s: len([x for x in s.split(",") if x.strip()])
    )
    df_glob = df_glob[(df_glob["ingredient_count"] >= 2) & (df_glob["ingredient_count"] <= 15)]
    df_glob["meal_type"] = df_glob.apply(lambda r: infer_meal_type(r["recipe_name"], r["cleaned_ingredients"]), axis=1)
    df_glob["diet"] = df_glob["cleaned_ingredients"].apply(infer_diet)
    df_glob["difficulty"] = df_glob.apply(lambda r: calculate_difficulty(r["total_time"], r["ingredient_count"]), axis=1)
    df_glob["servings"] = 2

    # Take 3,500 Indian recipes + 2,500 Global recipes
    sample_ind = df_ind.copy()
    sample_glob = df_glob.sample(n=min(2500, len(df_glob)), random_state=42)

    cols = [
        "recipe_name", "cleaned_ingredients", "ingredients_raw", "instructions",
        "total_time", "meal_type", "diet", "servings", "difficulty",
        "ingredient_count", "cuisine", "cuisine_detail"
    ]

    combined_df = pd.concat([sample_ind[cols], sample_glob[cols]], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=["recipe_name"])

    combined_df.to_csv(PROCESSED_CSV_PATH, index=False, encoding="utf-8")
    print(f"Combined processed recipes saved to: {PROCESSED_CSV_PATH}")
    print(f"Total recipes: {len(combined_df)}")
    print("Cuisine Breakdown:")
    print(combined_df["cuisine"].value_counts().to_dict())

    # Check Sambar & Chutney presence
    sambar_count = len(combined_df[combined_df["recipe_name"].str.contains("sambar", case=False, na=False)])
    chutney_count = len(combined_df[combined_df["recipe_name"].str.contains("chutney", case=False, na=False)])
    print(f"Sambar recipes count: {sambar_count}")
    print(f"Chutney recipes count: {chutney_count}")


if __name__ == "__main__":
    download_datasets()
    process_datasets()
