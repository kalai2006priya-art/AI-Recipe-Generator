# Presentation & Viva Voce Guide: Tamil Nadu AI Recipe Generator
## கல்லூரி தேர்வு மற்றும் வைவாவுக்கான விரிவான கேள்வி-பதில் வழிகாட்டி

This guide provides clear, confident, student-friendly answers for 3rd-year CSE-AIML students to defend the project before internal and external examiners, professors, and industry reviewers.

---

### Q1: What is this project?
**Answer:**  
Our project is an AI-assisted, bilingual recipe recommendation and generation web application focused on **Authentic Tamil Nadu Traditional Cuisine**. Users can either type or speak the ingredients they have at home (in Tamil or English). The system calculates exact recipe matches, filters dishes across traditional meal categories (காலை உணவு, மதிய உணவு, மாலை சிற்றுண்டி, இனிப்பு, இரவு உணவு), identifies missing items, reads the preparation steps aloud using AI text-to-speech, and customizes recipes using Google Gemini 2.5 Flash.

---

### Q2: Why did you specialize in Tamil Nadu traditional cuisine instead of general global recipes?
**Answer:**  
1. **Practical Cultural Relevance**: Most generic datasets contain obscure fusion dishes that Indian households never cook. Specializing in Tamil Nadu cuisine makes the application directly useful in real daily life (sambar, rasam, kothu parotta, ven pongal, appam, payasam).
2. **Accessible Categorization**: Tamil cuisine follows structured meal timings (Breakfast, Lunch, Evening Snacks, Sweets, Dinner) with specific staple spices (mustard, curry leaves, tamarind, toor dal).
3. **Regional Inclusivity**: Many homemakers and elders in Tamil Nadu are more comfortable with Tamil terminology and spoken interaction than typing English.

---

### Q3: How does the Voice Input (Speech-to-Text) feature work for non-readers?
**Answer:**  
We integrated the **HTML5 Web Speech API** (`window.webkitSpeechRecognition`) via a custom JavaScript/HTML component rendered inside Streamlit.
- The user clicks the microphone button.
- The browser prompts for microphone access and listens in real time using locale `ta-IN` (Tamil - India) or `en-IN` (English - India).
- The spoken words (e.g., `"தக்காளி வெங்காயம் பூண்டு"`) are converted into a text transcript and copied directly to the ingredient input field.
- This empowers users who cannot read or type in English/Tamil to effortlessly operate the application.

---

### Q4: How does the AI Voice Output (Text-to-Speech) work?
**Answer:**  
We used **`gTTS` (Google Text-to-Speech)** in `src/voice_service.py`:
1. When a user opens a recipe, the recipe title, ingredient checklist, and step-by-step cooking directions are converted into clean spoken text.
2. `gTTS` synthesizes the text into an MP3 audio byte stream in memory using the corresponding language code (`ta` for Tamil, `en` for English).
3. The audio byte stream is fed directly into Streamlit's `st.audio` player. The user can hit play and listen hands-free while cooking in the kitchen.

---

### Q5: Where is Generative AI used, and where is traditional programming used?
**Answer:**  
We follow a strict, disciplined software engineering architecture:
- **Traditional Python Programming**:
  - String cleaning, lemmatization, and bilingual synonym mapping (`src/ingredient_utils.py`).
  - Database persistence, password hashing, and user authentication (`src/auth.py`).
  - Mathematical ingredient set intersection, percentage matching, and category filtering (`src/recipe_matcher.py`).
- **Generative AI (Gemini 2.5 Flash)**:
  - Used **only** at the final stage for creative adaptation: scaling ingredient quantities for 1, 2, 4, or 6 servings, suggesting substitutions for missing ingredients, and writing chef tips.

---

### Q6: Why NOT use the LLM for searching and matching recipes?
**Answer:**  
1. **No Hallucination**: LLMs are prone to inventing fake ingredients, incorrect cooking times, or unbalanced spice ratios. Traditional algorithmic matching guarantees that all recommended recipes are culinarily valid.
2. **Speed & Latency**: Python evaluates the dataset in under 5 milliseconds. An LLM prompt takes 2 to 5 seconds and requires an active internet connection.
3. **Cost & Rate Limits**: Sending hundreds of recipe comparisons to an LLM API would rapidly exhaust token limits and incur unnecessary financial costs.
4. **Deterministic Math**: LLMs cannot reliably calculate mathematical percentages. Python computes exact percentages deterministically.

---

### Q7: How is the Ingredient Match Percentage calculated?
**Answer:**  
We use two clear mathematical formulas:

1. **Recipe Match Percentage**:
   $$\text{Match \%} = \left(\frac{\text{Number of Matched Recipe Ingredients}}{\text{Total Required Recipe Ingredients}}\right) \times 100$$
   *Example*: If Chettinad Chicken requires 8 ingredients and the user has 6 of them, the match is $\frac{6}{8} \times 100 = 75\%$.

2. **Pantry Utilization Percentage (Food-Waste Metric)**:
   $$\text{Utilization \%} = \left(\frac{\text{Number of User Ingredients Used}}{\text{Total Ingredients User Entered}}\right) \times 100$$
   *Example*: If the user entered 5 items and 4 are used in the dish, utilization is $\frac{4}{5} \times 100 = 80\%$.

---

### Q8: How is User Authentication and Data Security implemented?
**Answer:**  
- We use a local **SQLite database** (`data/users.db`) with two tables: `users` and `favorites`.
- Passwords are **never stored in plain text**. We use Python's `hashlib` to compute a cryptographic `SHA-256` hash.
- On login, the entered password is hashed with SHA-256 and compared against the stored hash.
- Streamlit's `st.session_state` maintains the user session, keeping track of username, login state, and favorite recipes.

---

### Q9: What happens if there is no internet connection or no Gemini API key?
**Answer:**  
The application contains a robust **Offline Fallback Engine** (`generate_fallback_recipe()` in `src/llm_service.py`).
- If no Gemini API key is configured in `.env`, the app does not crash or throw unhandled exceptions.
- It displays a clean banner informing the user that the app is operating in offline mode.
- It presents the full authentic recipe from the local dataset with scaled quantities, calculated available/missing tags, and original step-by-step directions in Tamil or English.

---

### Q10: How does the Bilingual Translation system work?
**Answer:**  
In `src/translations.py`, we implemented a centralized dictionary storing English and Tamil strings for every UI label, button text, dialog prompt, and category name.  
When the user clicks the language toggle button in the top bar (`🌐 Switch to தமிழ்` or `🌐 Switch to English`), the language key in `st.session_state["language"]` flips, and all components instantly re-render in the chosen language.

---

### Q11: What tech stack did you use?
**Answer:**  
- **Frontend & App Framework**: Streamlit (Python)
- **Backend Language**: Python 3.10+
- **Database**: SQLite3
- **Generative AI**: Google GenAI SDK (`google-genai`, Gemini 2.5 Flash)
- **Voice Technologies**: HTML5 Web Speech API (STT) + Google Text-to-Speech `gTTS` (TTS)
- **Security**: SHA-256 cryptographic hashing (`hashlib`)
- **Data Format**: JSON (`tamilnadu_recipes.json`)
