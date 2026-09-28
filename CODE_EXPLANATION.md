# Code Explanation Guide: Tamil Nadu Recipe Generator from Ingredients
## தமிழ்நாடு பாரம்பரிய சமையல் குறிப்புகள் & AI சமையல் வழிகாட்டி

Welcome to the **Code Explanation Guide**! This document is written in clear, structured language for a 3rd-year CSE-AIML student to confidently understand, explain, and defend every file in the codebase during project presentations, code reviews, and viva examinations.

---

## Table of Contents
1. [Project Overview & Architecture](#project-overview--architecture)
2. [File 1: `app.py` (Modern Bilingual Web Interface)](#file-1-apppy)
3. [File 2: `src/auth.py` (User Authentication & Bookmarks)](#file-2-srcauthpy)
4. [File 3: `src/translations.py` (Bilingual Localization System)](#file-3-srctranslationspy)
5. [File 4: `src/voice_service.py` (Speech-to-Text & Text-to-Speech)](#file-4-srcvoice_servicepy)
6. [File 5: `src/ingredient_utils.py` (Bilingual Ingredient Processing)](#file-5-srcingredient_utilspy)
7. [File 6: `src/recipe_matcher.py` (Category Filtering & Match Engine)](#file-6-srcrecipe_matcherpy)
8. [File 7: `src/llm_service.py` (Gemini 2.5 AI & Offline Fallback)](#file-7-srcllm_servicepy)
9. [File 8: `data/tamilnadu_recipes.json` (Authentic Regional Dataset)](#file-8-datatamilnadu_recipesjson)
10. [File 9: `scripts/test_tamil_features.py` (Automated Test Suite)](#file-9-scriptstest_tamil_featurespy)

---

## Project Overview & Architecture

The application is an AI-assisted recipe recommendation and generation system dedicated to **Authentic Tamil Nadu Traditional Cuisine**. It addresses household food waste, promotes accessibility for non-readers through voice interaction, and adheres to strict software engineering principles:

- **Mathematical Determinism & Fast Search**: Python algorithms and JSON indices handle 100% of ingredient parsing, categorization, and match calculations.
- **Accessibility & Voice**: 
  - **Speech-to-Text (STT)**: Uses Web Speech API (`ta-IN` / `en-IN`) so users can speak their ingredients into the microphone.
  - **Text-to-Speech (TTS)**: Uses `gTTS` (Google Text-to-Speech) to generate audio files that read recipe instructions out loud.
- **Bilingual Support**: Dynamic one-click switching between **தமிழ்** and **English** across all buttons, titles, recipes, and voice prompts.
- **Data Persistence**: SQLite database (`data/users.db`) manages user accounts with SHA-256 password hashing and personalized recipe bookmarks.
- **Generative AI Role**: Google Gemini 2.5 Flash is strictly confined to recipe customization (portion scaling, missing ingredient substitutions, and chef tips), backed by an offline fallback mode.

---

## File 1: `app.py`

### 1. What is this file?
`app.py` is the main frontend application built using **Streamlit**. It integrates authentication, voice capture, category navigation, recipe cards, audio playback, and LLM customization into a mobile-friendly user interface.

### 2. Why do we need it?
Users require an intuitive, attractive web application where they can log in, switch languages, talk to the app via microphone, filter by meal categories (Breakfast, Lunch, Snacks, Sweets, Dinner), view recipe cards with pantry utilization badges, and listen to spoken instructions.

### 3. Key Components & Functions:
- **Authentication State Control**: Renders modern Login/Signup tabs if the user is not authenticated, with a "Continue as Guest" option and instant language toggle.
- **Pure English Default & 1-Click Tamil Switch**: The app opens in 100% pure English by default. Clicking `🇮🇳 தமிழ் (Tamil)` flips every label, category, recipe title, and instruction into 100% pure Tamil, and vice versa.
- **Multi-Page Routing (Dedicated Recipe Page)**:
  - When a dish is chosen from the results list, the application navigates away from search results to a dedicated **Next Page** (`render_recipe_detail_page()`).
  - Contains full ingredients, instructions, AI customization, AI Voice player, and prominent `⬅️ Back to Search Results` navigation buttons.
- **Top Navigation Bar**: Buttons for 🍳 Recipe Finder, ❤️ Saved Recipes, 👤 Profile, and 🌐 Language Switcher.
- **Voice Microphone Widget**: Integrates `src/voice_service.py` to embed HTML5 microphone buttons for speaking ingredients in English or Tamil.
- **Category Filter Pills**: Quick-filter dropdown for All, Breakfast, Lunch, Snacks, Sweets, and Dinner.
- **Audio Recipe Player**: Reads the recipe steps out loud using `gTTS` audio streams.
- **AI Customization Drawer**: Calls Google Gemini 2.5 Flash for customized portion scaling, culinary substitutions, and tips.

---

## File 2: `src/auth.py`

### 1. What is this file?
`auth.py` handles database initialization, user registration, credential verification, and bookmark management using Python's built-in `sqlite3` module.

### 2. Why do we need it?
To give the application a real-world app feel with personal user accounts, persistent logins, and a bookmarking system for favorite dishes without relying on external cloud databases.

### 3. Key Functions:
- `init_db()`: Creates two tables if they do not exist:
  - `users`: `id`, `username`, `password_hash`, `full_name`, `created_at`.
  - `favorites`: `id`, `username`, `recipe_id`, `recipe_name`, `category`, `added_at`.
- `hash_password(password: str) -> str`: Produces a cryptographic `SHA-256` hexadecimal digest for safe password storage.
- `register_user(username, password, full_name)`: Validates input lengths, checks for existing usernames, and inserts new records.
- `login_user(username, password)`: Hashes the incoming password and compares it against the stored hash in the database.
- `add_favorite()`, `remove_favorite()`, `get_favorites()`: CRUD helper functions for managing a user's saved dishes.

---

## File 3: `src/translations.py`

### 1. What is this file?
`translations.py` is a centralized bilingual dictionary containing English and Tamil equivalents for every UI label, button, placeholder, notification, and category name.

### 2. Why do we need it?
Hardcoding English strings makes localization clumsy and bug-prone. With `translations.py`, changing languages is as simple as calling:
```python
get_text("search_button", lang="ta") # Returns: "🔍 சமையல் குறிப்புகளைக் கண்டுபிடி"
get_text("search_button", lang="en") # Returns: "🔍 Find Recipes"
```

### 3. Key Functions:
- `get_text(key: str, lang: str = "en") -> str`: Retrieves the localized string for any key, defaulting gracefully to English if the Tamil key is not defined.
- `CATEGORIES`: List of all supported meal categories: `All`, `Breakfast`, `Lunch`, `Snacks`, `Sweets`, `Dinner`.

---

## File 4: `src/voice_service.py`

### 1. What is this file?
`voice_service.py` contains the voice accessibility features of the project:
1. **Speech-to-Text (STT)**: A custom HTML5 / JavaScript component utilizing the browser's native `webkitSpeechRecognition`.
2. **Text-to-Speech (TTS)**: A Python service using `gTTS` (Google Text-to-Speech) to generate audio bytes for recipe reading.

### 2. Why do we need it?
To make the application accessible to non-readers, senior citizens, and busy cooks whose hands are covered in flour or spices:
- They can speak their ingredients into the microphone in Tamil (`ta-IN`) or Indian English (`en-IN`).
- They can listen to recipe preparation steps through spoken audio rather than reading small text on a screen.

### 3. Key Functions:
- `render_speech_to_text_component(lang: str = "ta-IN")`: Embeds an interactive microphone button into the Streamlit UI. Recognizes spoken words, displays a transcript modal, and allows instant copying into the ingredient box.
- `generate_recipe_audio(recipe_title, instructions, lang="ta") -> bytes`: Assembles recipe text and invokes `gTTS(text=..., lang=lang, slow=False)`, returning an in-memory MP3 byte stream for `st.audio`.

---

## File 5: `src/ingredient_utils.py`

### 1. What is this file?
`ingredient_utils.py` is a bilingual natural language text normalizer tailored for South Indian culinary terms.

### 2. Why do we need it?
Users type ingredients in various languages and forms (`"தக்காளி"`, `"tomato"`, `"tomatoes"`, `"1 cup chopped onions"`). This file maps Tamil terms and English synonyms to canonical culinary tokens.

### 3. Key Mappings & Functions:
- `TAMIL_TO_ENGLISH_MAP`: Maps Tamil words to canonical tokens:
  - `"தக்காளி"` $\rightarrow$ `"tomato"`
  - `"வெங்காயம்"` $\rightarrow$ `"onion"`
  - `"துவரம் பருப்பு"` $\rightarrow$ `"toor dal"`
  - `"தேங்காய்"` $\rightarrow$ `"coconut"`
- `clean_ingredient_text(text: str)`: Strips quantities, units (`tsp`, `cups`, `கிராம்`), special characters, and plural suffixes.
- `parse_user_ingredients(raw_input: str)`: Splits comma-separated ingredients, normalizes both Tamil and English tokens, and produces clean search terms.
- `ingredient_matches(user_ing, recipe_ing)`: Employs substring matching and culinary synonym matching to verify if a user's item satisfies a recipe requirement.

---

## File 6: `src/recipe_matcher.py`

### 1. What is this file?
`recipe_matcher.py` is the mathematical matching engine. It filters recipes by meal category and dietary preference, calculates match percentages, and identifies missing ingredients.

### 2. Why do we need it?
To provide instant, deterministic, and explainable recipe recommendations without relying on unpredictable LLM prompts.

### 3. Key Functions:
- `match_recipe(user_ingredients, recipe)`:
  - Loops over recipe ingredients.
  - Determines available ingredients (`✓`) and missing ingredients (`○`).
  - Computes:
    $$\text{Match \%} = \left(\frac{\text{Matched Required Ings}}{\text{Total Required Ings}}\right) \times 100$$
    $$\text{User Pantry Utilization \%} = \left(\frac{\text{Matched Ings}}{\text{User Ings Count}}\right) \times 100$$
- `filter_and_rank_recipes(user_ingredients, recipes, category="All", diet="Any", min_match_pct=0.0)`:
  - Filters by category (`Breakfast`, `Lunch`, `Snacks`, `Sweets`, `Dinner`).
  - Filters by diet (`Vegetarian`, `Non-Vegetarian`).
  - Sorts candidates by highest Match Percentage.

---

## File 7: `src/llm_service.py`

### 1. What is this file?
`llm_service.py` integrates the Google Gemini 2.5 Flash Generative AI model with an offline fallback mechanism.

### 2. Why do we need it?
When an API key is available, the LLM customizes the dish for specific serving sizes, adapts instructions for missing items, and provides chef tips. If the API key is not present or the internet is disconnected, the module provides structured fallback recipes without crashing.

### 3. Key Functions:
- `get_gemini_client()`: Initializes `genai.Client(api_key=...)`.
- `customize_recipe_with_llm(recipe, user_ingredients, servings=2, language="ta")`:
  - Formulates bilingual system and user prompts instructing Gemini to output structured sections: Title, Ingredients, Instructions, Chef Tip, and Substitutions in either Tamil or English.
- `generate_fallback_recipe(recipe, user_ingredients, servings=2, language="ta")`:
  - Deterministically formats the dataset recipe with scaled quantities and calculated match data when offline.

---

## File 8: `data/tamilnadu_recipes.json`

### 1. What is this file?
A curated JSON dataset containing 29 authentic Tamil Nadu traditional dishes spanning all 5 meal courses:
- **Breakfast**: Idli (இட்லி), Dosa (தோசை), Ven Pongal (வெண் பொங்கல்), Medu Vada (மெது வடை), Appam (ஆப்பம்), Poori Masala (பூரி கிழங்கு), Rava Upma (ரவா உப்புமா)...
- **Lunch**: Drumstick Sambar (முருங்கைக்காய் சாம்பார்), Tomato Rasam (தக்காளி மிளகு ரசம்), Vatha Kuzhambu (பூண்டு வத்தக் குழம்பு), Ennai Kathirikai (எண்ணெய் கத்திரிக்காய்), Dindigul Biryani (திண்டுக்கல் பிரியாணி), Chettinad Chicken (செட்டிநாடு சிக்கன் வறுவல்)...
- **Snacks**: Masala Vadai (பருப்பு மசால் வடை), Vazhaipoo Vadai (வாழைப்பூ வடை), Onion Pakoda (வெங்காய பக்கோடா), Sundal (சுண்டல்)...
- **Sweets**: Sakkarai Pongal (சர்க்கரை பொங்கல்), Rava Kesari (ரவா கேசரி), Paal Payasam (பால் பாயாசம்), Mysore Pak (மைசூர் பாக்)...
- **Dinner**: Madurai Kothu Parotta (மதுரை கொத்து பரோட்டா), Chapati Vegetable Kurma (சப்பாத்தி காய்கறி குருமா), Muttai Dosa (முட்டை தோசை)...

---

## File 9: `scripts/test_tamil_features.py`

### 1. What is this file?
An automated Python test suite that validates every layer of the system:
1. SQLite Database & Password Hashing.
2. Bilingual Ingredient Normalization (English & Tamil).
3. Recipe Category Matching & Ranking.
4. Voice Text-to-Speech (gTTS) Audio Generation.
5. Offline LLM Fallback Generation.
