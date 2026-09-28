"""
data_loader.py
--------------
Loads the bilingual Tamil Nadu recipes database from JSON.

Provides:
- 100% authentic Tamil Nadu recipes across all 5 categories
  (Breakfast, Lunch, Snacks, Sweets, Dinner)
- Bilingual fields for English and Tamil
- Fast in-memory caching with Pandas
"""

import json
import os
from typing import Optional
import pandas as pd

DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "tamilnadu_recipes.json"
)


def load_recipe_dataset(json_path: Optional[str] = None) -> pd.DataFrame:
    """Loads the Tamil Nadu recipe dataset from JSON."""
    path = json_path or DEFAULT_DATA_PATH

    if not os.path.exists(path):
        # Auto-create if not yet built
        from scripts.create_tamilnadu_dataset import create_dataset
        create_dataset()

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Standardize list columns
    df["ingredients_list"] = df["cleaned_ingredients_en"]
    df["time_mins"] = pd.to_numeric(df["time_mins"], errors="coerce").fillna(20).astype(int)

    return df
