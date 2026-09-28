# 🌾 தமிழ்நாடு பாரம்பரிய சமையல் | Tamil Nadu Traditional Kitchen
### AI-Assisted Bilingual Recipe Recommendation & Generation System

> 100% Authentic Tamil Nadu Cuisine | Bilingual (தமிழ் & English) | Voice Input (Speech-to-Text) | AI Voice Output (Text-to-Speech) | User Authentication & Bookmarks | Powered by Python, Streamlit & Google Gemini.

---

## 📌 Project Overview
**தமிழ்நாடு பாரம்பரிய சமையல் (Tamil Nadu Traditional Kitchen)** is an intelligent, accessible culinary application dedicated exclusively to authentic Tamil Nadu cuisine. It enables users to discover traditional recipes using the ingredients they have at home, speak ingredients in Tamil or English via microphone, listen to step-by-step instructions read aloud by an AI voice, and scale recipe portions for family gatherings.

---

## 🌟 Key Highlights & New Features

### 1. 100% Authentic Tamil Nadu Traditional Cuisine
Comprehensive coverage across all 5 essential meal categories:
- **காலை உணவு (Breakfast)**: மல்லிகைப் பூ இட்லி, மொறுமொறு தோசை, வெண் பொங்கல், மெது வடை, ஆப்பம் தேங்காய்ப்பால், பூரி கிழங்கு மசாலா, ரவா உப்புமா, தேங்காய் சட்னி, தக்காளி சட்னி...
- **மதிய உணவு (Lunch)**: முருங்கைக்காய் சாம்பார், தக்காளி மிளகு ரசம், பூண்டு வத்தக் குழம்பு, எண்ணெய் கத்திரிக்காய் குழம்பு, உருளைக்கிழங்கு வறுவல், தலப்பாகட்டி பிரியாணி, தயிர் சாதம், எலுமிச்சை சாதம், செட்டிநாடு சிக்கன் குழம்பு, கிராமத்து மீன் குழம்பு...
- **மாலை சிற்றுண்டி (Snacks)**: மசால் வடை, வெங்காய பஜ்ஜி, கொண்டைக்கடலை சுண்டல்...
- **இனிப்பு வகைகள் (Sweets)**: கோவில் சர்க்கரை பொங்கல், நெய் ரவா கேசரி, பால் பாயாசம், நெய் மைசூர் பாக்...
- **இரவு உணவு (Dinner)**: மதுரை கொத்து பரோட்டா, சப்பாத்தி காய்கறி குருமா, காரசாரமான முட்டை தோசை...

### 2. இருமொழி ஆதரவு (Bilingual: தமிழ் & English)
- One-click language switch between **தமிழ்** and **English** for the entire interface.
- Recipe titles, ingredients, and instructions available in both languages.

### 3. Voice Input for Accessibility (குரல் வழி உள்ளீடு)
- Designed for elder family members or those who cannot read/write fluently.
- Click the microphone button and simply speak: *"தக்காளி, வெங்காயம், பருப்பு"* or *"Tomato, Onion, Dal"*.
- Speech is automatically converted into text using HTML5 Web Speech API (`ta-IN` / `en-IN`).

### 4. AI Voice Output (குரல் வழி செய்முறை - Text-to-Speech)
- Users can click **"🔊 Listen to Recipe / செய்முறையைக் கேள்"**.
- Built-in audio generation reads the step-by-step cooking method aloud in clear, natural Tamil or English.

### 5. Real Mobile-App UI with Authentication
- **Login, Sign Up, and Guest Mode**: Secure SHA-256 password storage in SQLite (`data/users.db`).
- **Saved Recipes (விருப்பத்தில் சேமி)**: Bookmark favorite recipes and access them anytime from the top navigation bar.
- **Distraction-Free Experience**: Technical dataset tables and configuration codes are hidden from the user interface.

---

## 🛠️ Technology Stack

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit | Responsive, mobile-app inspired web interface |
| **Voice Input (STT)**| Web Speech API | Real-time speech recognition in Tamil (`ta-IN`) & English (`en-IN`) |
| **AI Voice (TTS)** | `gTTS` (Google Text-to-Speech) | Native MP3 audio generation for recipe readout |
| **Authentication & Storage** | SQLite (`users.db`) | User accounts, hashed credentials & bookmarks |
| **Recipe Matching Engine** | Pure Python Algorithms | Deterministic ingredient overlap & pantry utilization |
| **Generative AI** | Google Gemini (`google-genai`) | Portion scaling, chef tips & pantry substitutions |

---

## 📂 Project Structure

```
Recipe Generator/
│
├── app.py                         # Modern bilingual Streamlit application
├── requirements.txt               # Dependencies (streamlit, pandas, gTTS, google-genai, python-dotenv)
├── .env.example                   # Gemini API key template
├── .gitignore                     # Git exclusions
│
├── data/
│   ├── tamilnadu_recipes.json     # 100% authentic bilingual Tamil Nadu recipes database
│   └── users.db                   # SQLite database for accounts and bookmarks
│
├── src/
│   ├── __init__.py                # Package initializer
│   ├── auth.py                    # User authentication & favorites management
│   ├── translations.py            # Bilingual dictionary (English & தமிழ்)
│   ├── voice_service.py           # Speech-to-Text mic component & Text-to-Speech generator
│   ├── ingredient_utils.py        # Bilingual ingredient parsing & synonym dictionary
│   ├── recipe_matcher.py          # Category-based ranking & matching algorithm
│   └── llm_service.py             # Bilingual Gemini recipe customization + offline fallback
│
├── scripts/
│   ├── create_tamilnadu_dataset.py# Script to generate authentic bilingual recipe dataset
│   └── test_tamil_features.py     # Verification suite testing auth, voice, and matching
│
├── README.md                      # Project documentation
├── CODE_EXPLANATION.md            # Line-by-line student guide for presentations
├── PROJECT_FLOW.md                # Bilingual user journey & workflow diagram
├── VIVA_NOTES.md                  # Comprehensive viva questions with voice AI concepts
└── TESTING.md                     # Test records and verification report
```

---

## 🚀 Quick Start Guide (Installation & Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/recipe-generator.git
cd recipe-generator
```

### 2. Create and Activate Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key
Copy the example environment file to create your local `.env`:
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```
Open `.env` in any text editor and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
> **Note:** If no API key is provided, the application runs automatically in **100% offline fallback mode** using the authentic local Tamil Nadu dataset! Free Gemini API keys can be obtained from [Google AI Studio](https://aistudio.google.com/).

### 5. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
The app will immediately open in your browser at **`http://localhost:8501`**.

---

## 🧪 Verification & Automated Tests

To run the verification test suite covering authentication, bilingual parsing, ingredient normalization, and recipe matching:
```bash
python scripts/run_tests.py
```
*(All tests verify with a 100% success rate).*

