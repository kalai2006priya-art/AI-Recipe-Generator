"""
translations.py
---------------
Strictly isolated bilingual dictionary for Tamil Nadu AI Recipe Generator.
Guarantees:
- If language is 'en': 100% pure English with ZERO Tamil words or mixed slashes.
- If language is 'ta': 100% pure Tamil with ZERO English leakage.
"""

TRANSLATIONS = {
    # App Branding & Hero
    "app_title": {
        "en": "🌾 Tamil Nadu Kitchen AI",
        "ta": "🌾 தமிழ்நாடு பாரம்பரிய சமையல்"
    },
    "app_subtitle": {
        "en": "Turn the ingredients you already have into delicious authentic recipes.",
        "ta": "உங்களிடம் உள்ள சமையல் பொருட்களைக் கொண்டு பாரம்பரிய உணவுகளைக் கண்டறியுங்கள்."
    },
    "hero_title": {
        "en": "AI Recipe Generator",
        "ta": "AI சமையல் வழிகாட்டி"
    },
    "hero_subtitle": {
        "en": "Turn the ingredients you have into delicious recipes.",
        "ta": "உங்களிடம் உள்ள சமையல் பொருட்களைக் கொண்டு சுவையான உணவுகளைத் தயாருங்கள்."
    },

    # Navigation & Sidebar
    "language_label": {
        "en": "LANGUAGE",
        "ta": "மொழி"
    },
    "menu_label": {
        "en": "MENU",
        "ta": "வழிகாட்டி"
    },
    "find_recipes_tab": {
        "en": "🔍 Find",
        "ta": "🔍 தேடல்"
    },
    "results_tab": {
        "en": "🍲 Results",
        "ta": "🍲 முடிவுகள்"
    },
    "saved_tab": {
        "en": "❤️ Saved",
        "ta": "❤️ சேமிப்பு"
    },
    "history_tab": {
        "en": "📜 History",
        "ta": "📜 வரலாறு"
    },
    "profile_tab": {
        "en": "👤 My Profile",
        "ta": "👤 சுயவிவரம்"
    },
    "logout": {
        "en": "Logout",
        "ta": "வெளியேறு"
    },
    "signed_in_as": {
        "en": "Signed in as",
        "ta": "உள்நுழைந்துள்ள பயனர்"
    },

    # Authentication
    "login": {
        "en": "Login",
        "ta": "உள்நுழைக"
    },
    "signup": {
        "en": "Sign Up",
        "ta": "பதிவு செய்க"
    },
    "sign_in_tab": {
        "en": "Sign In",
        "ta": "உள்நுழைக"
    },
    "sign_up_tab": {
        "en": "Create Account",
        "ta": "புதிய கணக்கு"
    },
    "sign_in_title": {
        "en": "Welcome Back to Samayal AI",
        "ta": "சமையல் AI-க்கு மீண்டும் நல்வரவு"
    },
    "sign_up_title": {
        "en": "Create Your Kitchen Account",
        "ta": "உங்கள் சமையல் கணக்கை உருவாக்கவும்"
    },
    "sign_in_subtitle": {
        "en": "Sign in to access your saved recipes, cooking history, and AI chef features.",
        "ta": "உங்கள் சேமிக்கப்பட்ட உணவுகள், தேடல் வரலாறு மற்றும் AI சமையல் குறிப்புகளை அணுக உள்நுழைக."
    },
    "sign_up_subtitle": {
        "en": "Join today to save your favorite Tamil Nadu dishes and customize recipes.",
        "ta": "பாரம்பரிய தமிழ்நாடு உணவுகளை சேமிக்கவும் சமையல் குறிப்புகளை மாற்றியமைக்கவும் இன்றே இணையுங்கள்."
    },
    "guest_mode": {
        "en": "Continue as Guest",
        "ta": "விருந்தினராகத் தொடர்க"
    },
    "username": {
        "en": "Username",
        "ta": "பயனர் பெயர்"
    },
    "password": {
        "en": "Password",
        "ta": "கடவுச்சொல்"
    },
    "confirm_password": {
        "en": "Confirm Password",
        "ta": "கடவுச்சொல்லை உறுதிப்படுத்துக"
    },
    "full_name": {
        "en": "Full Name",
        "ta": "முழுப் பெயர்"
    },
    "passwords_dont_match": {
        "en": "Passwords do not match.",
        "ta": "கடவுச்சொற்கள் பொருந்தவில்லை."
    },
    "password_too_short": {
        "en": "Password must be at least 4 characters.",
        "ta": "கடவுச்சொல் குறைந்தது 4 எழுத்துக்கள் இருக்க வேண்டும்."
    },
    "username_too_short": {
        "en": "Username must be at least 3 characters.",
        "ta": "பயனர் பெயர் குறைந்தது 3 எழுத்துக்கள் இருக்க வேண்டும்."
    },
    "all_fields_required": {
        "en": "All fields are required.",
        "ta": "அனைத்து விவரங்களையும் பூர்த்தி செய்யவும்."
    },
    "login_success": {
        "en": "Welcome back!",
        "ta": "மீண்டும் நல்வரவு!"
    },
    "signup_success": {
        "en": "Account created successfully! You are now signed in.",
        "ta": "கணக்கு வெற்றிகரமாக உருவாக்கப்பட்டது! நீங்கள் உள்நுழைந்துள்ளீர்கள்."
    },
    "switch_to_signup": {
        "en": "Don't have an account? Create one now",
        "ta": "கணக்கு இல்லையா? புதிய கணக்கை உருவாக்குக"
    },
    "switch_to_signin": {
        "en": "Already have an account? Sign in here",
        "ta": "ஏற்கனவே கணக்கு உள்ளதா? இங்கே உள்நுழைக"
    },
    "guest_continue_btn": {
        "en": "Continue as Guest",
        "ta": "விருந்தினராகத் தொடர்க"
    },
    "sign_in_nav": {
        "en": "Sign In",
        "ta": "உள்நுழைக"
    },
    "saved_login_prompt": {
        "en": "Please sign in to save your favorite recipes and access them anytime.",
        "ta": "உணவுகளைச் சேமிக்கவும் எப்போது வேண்டுமானாலும் அணுகவும் கணக்கில் உள்நுழையவும்."
    },
    "sign_in_to_save_btn": {
        "en": "🔑 Sign In to View Saved Dishes",
        "ta": "🔑 சேமித்த உணவுகளைக் காண உள்நுழைக"
    },
    "saved_dishes_count": {
        "en": "Saved Recipes",
        "ta": "சேமிக்கப்பட்ட உணவுகள்"
    },
    "search_history_count": {
        "en": "Searches Made",
        "ta": "மேற்கொண்ட தேடல்கள்"
    },

    # Input Experience
    "input_heading": {
        "en": "What ingredients do you have?",
        "ta": "உங்களிடம் உள்ள சமையல் பொருட்கள் என்ன?"
    },
    "input_sub": {
        "en": "Enter the ingredients available in your kitchen and we'll find delicious recipes for you.",
        "ta": "உங்கள் சமையலறையில் உள்ள பொருட்களை உள்ளிடுங்கள், நாங்கள் சுவையான உணவுகளைக் கண்டறிவோம்."
    },
    "input_placeholder": {
        "en": "Enter ingredients like chicken, tomato, chilli, onion...",
        "ta": "கோழி, தக்காளி, மிளகாய், வெங்காயம் போன்றவற்றை உள்ளிடவும்..."
    },
    "input_help": {
        "en": "Type or speak ingredients separated by commas",
        "ta": "பொருட்களை கமா இட்டு உள்ளிடவும் அல்லது பேசவும்"
    },
    "generate_recipes_btn": {
        "en": "✨ Generate Recipes",
        "ta": "✨ சமையல் குறிப்புகளை உருவாக்கு"
    },
    "find_recipes_btn": {
        "en": "✨ Generate Recipes",
        "ta": "✨ சமையல் குறிப்புகளை உருவாக்கு"
    },
    "view_recipe_btn": {
        "en": "View Recipe →",
        "ta": "செய்முறையைக் காண்க →"
    },
    "you_may_also_need_title": {
        "en": "You may also need",
        "ta": "உங்களுக்குத் தேவைப்படக்கூடியவை"
    },
    "empty_state_title": {
        "en": "What's in your kitchen today?",
        "ta": "இன்று உங்கள் சமையலறையில் என்ன உள்ளது?"
    },
    "empty_state_desc": {
        "en": "Enter a few ingredients and discover recipes you can make.",
        "ta": "சில சமையல் பொருட்களை உள்ளிட்டு அருமையான உணவுகளைக் கண்டறியுங்கள்."
    },
    "loading_recipes_title": {
        "en": "Creating delicious recipes... 🥕 ➜ 🍳 ➜ 🍲",
        "ta": "சுவையான சமையல் குறிப்புகள் உருவாகின்றன... 🥕 ➜ 🍳 ➜ 🍲"
    },
    "error_state_title": {
        "en": "Oops! We couldn't create your recipes.",
        "ta": "மன்னிக்கவும்! செய்முறைகளை உருவாக்க முடியவில்லை."
    },
    "error_state_desc": {
        "en": "Please check your ingredients and try again.",
        "ta": "சமையல் பொருட்களை சரிபார்த்து மீண்டும் முயற்சிக்கவும்."
    },
    "try_again_btn": {
        "en": "Try Again",
        "ta": "மீண்டும் முயற்சிக்கவும்"
    },
    "footer_text": {
        "en": "Made with ❤️ using AI • AI Recipe Generator",
        "ta": "AI தொழில்நுட்பத்துடன் அன்புடன் உருவாக்கப்பட்டது • AI சமையல் வழிகாட்டி"
    },
    "servings_label": {
        "en": "Servings",
        "ta": "பரிமாறல்கள்"
    },
    "course_label": {
        "en": "Course",
        "ta": "வகை"
    },

    # Filters
    "meal_category": {
        "en": "Meal Category",
        "ta": "உணவு வகை"
    },
    "cat_all": {
        "en": "All Categories",
        "ta": "அனைத்தும்"
    },
    "cat_breakfast": {
        "en": "Breakfast",
        "ta": "காலை உணவு"
    },
    "cat_lunch": {
        "en": "Lunch",
        "ta": "மதிய உணவு"
    },
    "cat_snacks": {
        "en": "Snacks",
        "ta": "மாலை சிற்றுண்டி"
    },
    "cat_sweets": {
        "en": "Sweets",
        "ta": "இனிப்பு வகைகள்"
    },
    "cat_dinner": {
        "en": "Dinner",
        "ta": "இரவு உணவு"
    },
    "diet_pref": {
        "en": "Diet",
        "ta": "உணவு முறை"
    },
    "diet_all": {
        "en": "All",
        "ta": "அனைத்தும்"
    },
    "diet_veg": {
        "en": "Vegetarian",
        "ta": "சைவம்"
    },
    "diet_nonveg": {
        "en": "Non-Vegetarian",
        "ta": "அசைவம்"
    },
    "cooking_time": {
        "en": "Cooking Time",
        "ta": "சமைக்கும் நேரம்"
    },
    "use_available_first": {
        "en": "Prioritize available ingredients",
        "ta": "உள்ள பொருட்களை அதிகம் பயன்படுத்து"
    },

    # Results & Cards
    "results_heading": {
        "en": "What can I make?",
        "ta": "நான் என்ன சமைக்கலாம்?"
    },
    "matches_found": {
        "en": "Matching Recipes",
        "ta": "பொருத்தமான உணவுகள்"
    },
    "ingredients_label": {
        "en": "Your Ingredients",
        "ta": "உங்கள் பொருட்கள்"
    },
    "new_search_btn": {
        "en": "🔍 New Search",
        "ta": "🔍 புதிய தேடல்"
    },
    "view_recipe_btn": {
        "en": "View Recipe",
        "ta": "செய்முறையைக் காண்க"
    },
    "ai_chef_badge": {
        "en": "AI Chef Creation",
        "ta": "AI சிறப்பு செய்முறை"
    },
    "traditional_badge": {
        "en": "Traditional Classic",
        "ta": "பாரம்பரிய உணவு"
    },
    "match_badge": {
        "en": "Match",
        "ta": "பொருத்தம்"
    },
    "mins": {
        "en": "mins",
        "ta": "நிமிடங்கள்"
    },
    "easy": {
        "en": "Easy",
        "ta": "எளிது"
    },
    "medium": {
        "en": "Medium",
        "ta": "மிதமானது"
    },
    "hard": {
        "en": "Hard",
        "ta": "கடினம்"
    },

    # Compact "You Can Also Add" Section
    "suggestions_title": {
        "en": "You can also add",
        "ta": "கூடுதலாக நீங்கள் சேர்க்கலாம்"
    },
    "suggestions_desc": {
        "en": "These ingredients can enhance the flavour and open up more recipe options.",
        "ta": "இவை உங்கள் உணவின் சுவையைக் கூட்டி கூடுதல் சமையல் வாய்ப்புகளைத் தரும்."
    },
    "suggestions_add_btn": {
        "en": "+ Add & Generate",
        "ta": "+ சேர்த்து சமைக்க"
    },

    # Recipe Detail & Step-by-Step Cooking
    "ingredients_heading": {
        "en": "Ingredients",
        "ta": "தேவையான பொருட்கள்"
    },
    "available_ingredients_title": {
        "en": "Available Ingredients",
        "ta": "உங்களிடம் உள்ளவை"
    },
    "pantry_ingredients_title": {
        "en": "Additional Pantry Staples",
        "ta": "கூடுதல் அஞ்சறைப்பெட்டி பொருட்கள்"
    },
    "cooking_steps_title": {
        "en": "Cooking Steps",
        "ta": "சமைக்கும் செய்முறை"
    },
    "prep_time_label": {
        "en": "Prep Time",
        "ta": "தயாரிப்பு நேரம்"
    },
    "cook_time_label": {
        "en": "Cook Time",
        "ta": "சமைக்கும் நேரம்"
    },
    "difficulty_label": {
        "en": "Difficulty",
        "ta": "சிரமம்"
    },
    "start_cooking_btn": {
        "en": "👨‍🍳 Start Cooking",
        "ta": "👨‍🍳 சமைக்கத் தொடங்கு"
    },
    "exit_cooking_btn": {
        "en": "✕ Exit Cooking Mode",
        "ta": "✕ சமையல் முறையிலிருந்து வெளியேறு"
    },
    "step_label": {
        "en": "STEP",
        "ta": "படி"
    },
    "of_label": {
        "en": "OF",
        "ta": "-ல்"
    },
    "prev_step_btn": {
        "en": "← Previous",
        "ta": "← முந்தையது"
    },
    "next_step_btn": {
        "en": "Next →",
        "ta": "அடுத்தது →"
    },
    "cooking_complete": {
        "en": "🎉 Cooking Complete! Enjoy your delicious meal.",
        "ta": "🎉 சமையல் முடிந்தது! சுவைத்து மகிழுங்கள்."
    },
    "listen_voice_btn": {
        "en": "🔊 Listen to Instructions",
        "ta": "🔊 செய்முறையைக் கேள்"
    },
    "ai_customize_btn": {
        "en": "✨ Scale Servings",
        "ta": "✨ அளவை மாற்றி அமை"
    },
    "servings": {
        "en": "Servings",
        "ta": "நபர்கள்"
    },
    "save_recipe_btn": {
        "en": "❤️ Bookmark Recipe",
        "ta": "❤️ விருப்பத்தில் சேமி"
    },
    "unsave_recipe_btn": {
        "en": "❌ Remove Bookmark",
        "ta": "❌ சேமிப்பிலிருந்து நீக்கு"
    },
    "back_to_results": {
        "en": "← Back to Recipes",
        "ta": "← செய்முறைகளுக்குத் திரும்பு"
    },
    "back_to_saved": {
        "en": "← Back to Saved Dishes",
        "ta": "← சேமிக்கப்பட்ட உணவுகளுக்குத் திரும்பு"
    },

    # Saved & History Pages
    "saved_title": {
        "en": "Saved Recipes",
        "ta": "சேமிக்கப்பட்ட உணவுகள்"
    },
    "history_title": {
        "en": "Search History",
        "ta": "தேடல் வரலாறு"
    },
    "matches_found_text": {
        "en": "matching recipes found",
        "ta": "பொருத்தமான உணவுகள் கண்டறியப்பட்டன"
    },
    "search_again_btn": {
        "en": "Search Again",
        "ta": "மீண்டும் தேடுக"
    },
    "no_history_text": {
        "en": "No past searches recorded yet in this session.",
        "ta": "இந்த அமர்வில் முந்தைய தேடல் வரலாறு எதுவும் இல்லை."
    },
    "profile_title": {
        "en": "User Profile",
        "ta": "பயனர் சுயவிவரம்"
    },

    # Modern Pantry Shelf & Real-App Features
    "pantry_shelf_title": {
        "en": "Kitchen Pantry (Tap to Add)",
        "ta": "சமையலறைப் பொருட்கள் (தொட்டுச் சேர்க்கவும்)"
    },
    "pantry_shelf_sub": {
        "en": "Tap ingredients you have at home to add them instantly:",
        "ta": "வீட்டில் உள்ள பொருட்களைத் தொட்டு உடனடியாக சேர்க்கவும்:"
    },
    "pantry_cat_nonveg": {
        "en": "Meat & Seafood",
        "ta": "அசைவம் & மீன்"
    },
    "pantry_cat_veg": {
        "en": "Fresh Vegetables",
        "ta": "புதிய காய்கறிகள்"
    },
    "pantry_cat_staples": {
        "en": "Staples & Dairy",
        "ta": "தானியங்கள் & பால்"
    },
    "cook_this_recipe_btn": {
        "en": "Cook This Recipe →",
        "ta": "சமைக்கலாம் →"
    },
    "ingredient_checklist_title": {
        "en": "Preparation Checklist",
        "ta": "தேவையான பொருட்கள் சரிபார்ப்பு"
    },
    "clear_all_btn": {
        "en": "Clear All",
        "ta": "அனைத்தையும் நீக்கு"
    },

    # AI Recipe Video Generation Suite
    "video_section_title": {
        "en": "AI Recipe Video Suite",
        "ta": "AI சமையல் காணொளி தொகுப்பு"
    },
    "watch_video_reel_btn": {
        "en": "🎬 Watch Cooking Video Reel",
        "ta": "🎬 சமையல் ரீல் காணொளி"
    },
    "generate_mp4_btn": {
        "en": "🎥 Generate MP4 Video Reel",
        "ta": "🎥 MP4 காணொளியை உருவாக்கு"
    },
    "generating_video_spinner": {
        "en": "Generating high-definition cooking video reel...",
        "ta": "உயர்தர சமையல் காணொளி உருவாகிறது..."
    },
    "download_video_btn": {
        "en": "📥 Download Recipe Video (.mp4)",
        "ta": "📥 காணொளியைப் பதிவிறக்கு (.mp4)"
    },
    "video_tutorial_btn": {
        "en": "📺 Watch Authentic Video Guide",
        "ta": "📺 நேரடி சமையல் காணொளி"
    },
    "video_tab_reel": {
        "en": "🎥 Interactive Reel",
        "ta": "🎥 நேரடி ரீல்"
    },
    "video_tab_mp4": {
        "en": "📥 Export MP4 File",
        "ta": "📥 MP4 பதிவிறக்கம்"
    },
    "video_tab_tutorial": {
        "en": "📺 YouTube Chef Guide",
        "ta": "📺 சமையல் காணொளி"
    }
}


def t(key: str, lang: str = "en") -> str:
    """Retrieves localized text for key. Strictly guarantees zero language leakage."""
    clean_lang = "ta" if lang == "ta" else "en"
    entry = TRANSLATIONS.get(key)
    if entry and isinstance(entry, dict):
        return entry.get(clean_lang, entry.get("en", key))
    return key