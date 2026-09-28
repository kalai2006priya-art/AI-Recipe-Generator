# Project Workflow: Tamil Nadu Traditional Recipe Generator
## திட்ட செயல்முறை வரைபடம் மற்றும் முழுமையான தரவு ஓட்டம்

This document details the complete end-to-end architecture, data flow, and control logic of the **Tamil Nadu Recipe Generator from Ingredients** application.

---

## 1. High-Level System Architecture

```
                                  ┌───────────────────────────┐
                                  │           USER            │
                                  │   (Speak or Type Input)   │
                                  └─────────────┬─────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 │                                                             │
                 ▼ (Voice)                                                     ▼ (Text)
   ┌───────────────────────────┐                                 ┌───────────────────────────┐
   │    HTML5 Web Speech API   │                                 │   Streamlit Input Field   │
   │  Mic Input: ta-IN / en-IN │                                 │  "தக்காளி, வெங்காயம்..."  │
   └─────────────┬─────────────┘                                 └─────────────┬─────────────┘
                 │ (Transcript Transferred)                                    │
                 └──────────────────────────────┬──────────────────────────────┘
                                                │
                                                ▼
                                 ┌───────────────────────────┐
                                 │   SESSION & AUTH STATE    │
                                 │      (src/auth.py)        │
                                 │  Logged In / Guest Mode   │
                                 │  SQLite DB (data/users.db)│
                                 └──────────────┬────────────┘
                                                │
                                                ▼
                                 ┌───────────────────────────┐
                                 │  BILINGUAL NORMALIZATION  │
                                 │ (src/ingredient_utils.py) │
                                 │  Tamil & English Mapping  │
                                 │  "தக்காளி" -> "tomato"    │
                                 └──────────────┬────────────┘
                                                │
                                                ▼
                                 ┌───────────────────────────┐
                                 │  CATEGORY FILTER & MATCH  │
                                 │  (src/recipe_matcher.py)  │
                                 │  Matches 29 TN Dishes     │
                                 │  - Breakfast / Lunch /    │
                                 │    Snacks / Sweets / Dinner│
                                 │  Calculates Match % & Util│
                                 └──────────────┬────────────┘
                                                │
                                                ▼
                                 ┌───────────────────────────┐
                                 │     RECIPE SELECTION      │
                                 │  User clicks recipe card  │
                                 │  Can bookmark (❤️ Save)   │
                                 └──────────────┬────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 │                                                             │
                 ▼                                                             ▼
   ┌───────────────────────────┐                                 ┌───────────────────────────┐
   │      AI VOICE (TTS)       │                                 │    RECIPE CUSTOMIZATION   │
   │  (src/voice_service.py)   │                                 │    (src/llm_service.py)   │
   │  gTTS converts steps to   │                                 │  Gemini 2.5 Flash /       │
   │  Tamil/English MP3 audio  │                                 │  Authentic Fallback Mode  │
   └───────────────────────────┘                                 └───────────────────────────┘
```

---

## 2. Step-by-Step Execution Journey

### Step 1: User Access & Authentication
1. User visits the web app at `http://localhost:8501`.
2. The user can either:
   - **Log in** with existing credentials.
   - **Register** a new account (username, password, full name). Passwords are encrypted using SHA-256 and stored in `data/users.db`.
   - **Continue as Guest** for instant, frictionless browsing.
3. Once in the app, the user can toggle the interface language between **தமிழ்** and **English** at any time.

---

### Step 2: Ingredient Input (Voice or Text)
1. **Voice Input (Speech-to-Text)**:
   - Particularly designed for users who cannot easily type or read.
   - User clicks the **"🎤 தமிழ் குரல் உள்ளீடு (Speak Ingredients)"** button.
   - The browser's Web Speech API activates using `ta-IN` (Tamil) or `en-IN` (English).
   - As the user speaks (`"தக்காளி வெங்காயம் பூண்டு"`), speech is transcribed and copied directly into the search box.
2. **Text Input**:
   - Alternatively, users type comma-separated ingredients directly in the text box (e.g. `பருப்பு, தக்காளி, வெங்காயம், முருங்கைக்காய்`).

---

### Step 3: Bilingual Text Preprocessing
1. The input string is passed to `src/ingredient_utils.py`.
2. Tamil words are recognized and matched with South Indian culinary synonyms:
   - `துவரம் பருப்பு` $\rightarrow$ `toor dal`
   - `வெங்காயம்` $\rightarrow$ `onion`
   - `தக்காளி` $\rightarrow$ `tomato`
   - `முருங்கைக்காய்` $\rightarrow$ `drumstick`
3. Quantities, units, and extra spaces are removed.
4. Output is a normalized list of tokens ready for high-speed matching.

---

### Step 4: Category Filtering & Deterministic Match Engine
1. User selects a category filter pill:
   - **All (அனைத்தும்)**
   - **Breakfast (காலை உணவு)**
   - **Lunch (மதிய உணவு)**
   - **Snacks (மாலை சிற்றுண்டி)**
   - **Sweets (இனிப்பு வகைகள்)**
   - **Dinner (இரவு உணவு)**
2. `filter_and_rank_recipes()` searches `data/tamilnadu_recipes.json`:
   - Categorizes dishes according to authentic meal times.
   - Computes:
     $$\text{Ingredient Match \%} = \left(\frac{\text{Matched Recipe Ingredients}}{\text{Total Recipe Ingredients}}\right) \times 100$$
     $$\text{Pantry Utilization \%} = \left(\frac{\text{Matched Ingredients}}{\text{User's Total Entered Ingredients}}\right) \times 100$$
   - Partitions ingredients into **Available (`✓`)** and **Missing (`○`)**.
3. Results are ordered and displayed as recipe cards.

---

### Step 5: Multi-Page Navigation to Dedicated Recipe Detail Page
1. User clicks **"👉 View Full Recipe & Cook"** on any recipe card.
2. The application navigates to a dedicated **Next Page** (`render_recipe_detail_page()`), clearing the search list for an uncluttered reading experience.
3. The dedicated page features:
   - **"⬅️ Back to Search Results"** button to return smoothly to the results list.
   - Dish Hero banner with cooking time, difficulty, diet, and match percentage badges.
   - Clean 2-column layout: Left column for pantry match breakdown and ingredient quantities; Right column for step-by-step instructions.
4. **AI Voice Audio Player**:
   - `src/voice_service.py` calls `gTTS` to generate natural speech audio in English or Tamil.
   - The user clicks Play on the embedded audio widget to listen hands-free while cooking.

---

### Step 6: AI Customization (Gemini 2.5 Flash) & Offline Fallback
1. If the user clicks **"✨ AI மூலம் தனிப்பயனாக்கு (Customize with AI)"**:
   - If `GEMINI_API_KEY` is provided, Gemini 2.5 Flash adjusts the quantities for the specified servings, suggests smart Tamil pantry substitutes for missing items, and provides authentic chef tips.
   - If no API key is provided, the **Offline Fallback Engine** immediately renders the original authentic recipe without throwing an error or crashing.

---

### Step 7: Bookmarking & Favorites
1. Logged-in users can click **"❤️ பிடித்தவை (Favorite)"** on any recipe.
2. The recipe is saved to SQLite (`favorites` table).
3. Clicking the **"❤️ Saved Recipes (சேமிக்கப்பட்டவை)"** tab displays all bookmarked dishes for quick access anytime.
