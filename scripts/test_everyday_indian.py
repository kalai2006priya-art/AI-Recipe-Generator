import os
import sys

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

df = load_recipe_dataset()

tests = [
    ("Sambar Test", "Toor Dal, Tomato, Onion, Tamarind, Drumstick, Sambar Powder", "Indian"),
    ("Coconut Chutney Test", "Coconut, Green Chilli, Ginger, Chana Dal, Salt, Mustard", "Indian"),
    ("Tomato Chutney Test", "Tomato, Onion, Garlic, Red Chilli, Mustard", "Indian"),
    ("Rasam Test", "Tomato, Garlic, Pepper, Cumin, Tamarind", "Indian"),
    ("Dosa Test", "Rice, Urad Dal, Fenugreek", "Indian"),
    ("Biryani Test", "Basmati Rice, Onion, Tomato, Ginger, Garlic, Biryani Masala", "Indian"),
    ("Italian Pasta Test", "Tomato, Garlic, Basil, Pasta", "Italian")
]

for title, ings, cuisine in tests:
    print(f"=== {title} ===")
    parsed = parse_user_ingredients(ings)
    matches = filter_and_rank_recipes(df, parsed, cuisine=cuisine, top_k=3)
    for idx, r in enumerate(matches):
        print(f"  [{idx+1}] {r['recipe_name']}")
        print(f"      Match: {r['match_percentage']}% | Uses: {r['user_utilization']}% | Score: {r['relevance_score']}")
        print(f"      Matched: {r['matched_ingredients']}")
    print()
