"""
app.py
------
Production-Grade AI Recipe Generator & Cooking Assistant.
Vibrant, Modern, Professional Food-Tech UI/UX Redesign.

Design System:
- Color Palette: Warm Orange/Coral (#FF6B35), Golden Yellow (#FFB703), Fresh Green (#2A9D8F), Off-White (#FFF9F3), Dark Charcoal (#242424).
- Modern Hero Section (Ingredients ➜ AI ➜ Recipes flow)
- Premium Ingredient Input Card with Voice Recognition & Quick Clickable Chips
- Modern Recipe Cards with dish icons, badges, time, servings, category, and "View Recipe →"
- Visually Separated Numbered Steps (01, 02, 03...) on Recipe Detail
- Interactive Step-by-Step Cooking Mode with Voice Narration
- In-App AI Video Reel Player
- "💡 You May Also Need" Compact Recommendation Section
- 100% Strict Bilingual Language Isolation (English by default, zero Tamil in English mode)
- Complete elimination of Markdown code blocks via render_html
"""

import datetime
import re
import streamlit as st
import pandas as pd
from src.data_loader import load_recipe_dataset
from src.ingredient_utils import parse_user_ingredients, is_pantry_ingredient, get_tamil_ingredient_name
from src.recipe_matcher import filter_and_rank_recipes
from src.recipe_validator import validate_recipe
from src.llm_service import (
    customize_recipe_with_llm,
    generate_multiple_ingredient_recipes
)
from src.ingredient_suggester import get_compact_ingredient_suggestions
from src.translations import t
from src.auth import login_user, register_user, toggle_favorite, get_favorites
from src.voice_service import render_voice_input_button, generate_recipe_audio

# Page Configuration
st.set_page_config(
    page_title="RecipeAI - AI Recipe Generator",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def render_html(html_code: str):
    """
    Renders raw HTML safely in Streamlit, stripping all leading indentation
    and empty lines to permanently prevent CommonMark from interpreting HTML
    as an indented code block.
    """
    clean_lines = [line.strip() for line in html_code.strip().splitlines() if line.strip()]
    st.markdown("\n".join(clean_lines), unsafe_allow_html=True)


# ==============================================================================
# VIBRANT FOOD-TECH DESIGN SYSTEM (WARM LIGHT THEME)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* BASE APP & WARM LIGHT BACKGROUND */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: #FFF9F3 !important;
        color: #242424 !important;
    }

    /* TOP HEADER PADDING & NO CLIPPING */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 1.2rem !important;
        z-index: 10 !important;
    }
    .block-container {
        padding-top: 2.2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1240px !important;
    }

    /* HIDE STREAMLIT LINK ANCHORS & DEPLOY BUTTONS */
    [data-testid="stHeaderActionElements"],
    a.header-anchor,
    a.anchor-link,
    .stMarkdown a[href^="#"],
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a,
    #MainMenu, footer, .stDeployButton {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }

    /* TYPOGRAPHY */
    h1, h2, h3, h4, h5, h6 {
        color: #242424 !important;
        font-weight: 800 !important;
        line-height: 1.3 !important;
    }
    p, span, div {
        color: inherit;
    }

    /* TOP NAVIGATION HEADER (WARM TRANSLUCENT) */
    .top-app-bar {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 18px;
        padding: 0.85rem 1.4rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    }
    .brand-title {
        font-size: 1.35rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }
    .brand-subtitle {
        font-size: 0.72rem;
        color: #888888;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* HERO SECTION */
    .hero-banner {
        background: linear-gradient(135deg, #FFF0E5 0%, #FFFDF9 60%, #FFFFFF 100%);
        border: 1px solid #FFE2CC;
        border-radius: 20px;
        padding: 2.2rem 2.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 24px rgba(255, 107, 53, 0.08);
        position: relative;
        overflow: hidden;
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #242424;
        letter-spacing: -0.02em;
        margin: 0;
        line-height: 1.2;
    }
    .hero-title span {
        color: #FF6B35;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #555555;
        margin-top: 0.5rem;
        line-height: 1.5;
        max-width: 650px;
    }
    .hero-flow {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: #FFFFFF;
        border: 1px solid #FFD9C2;
        border-radius: 9999px;
        padding: 0.45rem 1.1rem;
        margin-top: 1.1rem;
        font-size: 0.88rem;
        font-weight: 700;
        color: #FF6B35;
        box-shadow: 0 2px 8px rgba(255, 107, 53, 0.1);
    }

    /* PREMIUM CARD CONTAINER */
    .premium-card {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 20px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    }
    .card-heading {
        font-size: 1.25rem;
        font-weight: 800;
        color: #242424;
        margin-bottom: 0.3rem;
    }
    .card-subtitle {
        font-size: 0.9rem;
        color: #666666;
        margin-bottom: 1.1rem;
        line-height: 1.45;
    }

    /* RECIPE GRID CARD */
    .recipe-food-card {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.07);
        border-radius: 18px;
        padding: 1.5rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    .recipe-food-card:hover {
        transform: translateY(-4px);
        border-color: #FFB703;
        box-shadow: 0 10px 28px rgba(255, 107, 53, 0.14);
    }
    .dish-card-banner {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.8rem;
    }
    .dish-icon-badge {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        background: #FFF0E5;
        border: 1px solid #FFD9C2;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
    }
    .dish-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #242424;
        margin-top: 0.4rem;
        margin-bottom: 0.3rem;
        line-height: 1.35;
    }
    .dish-meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
        font-size: 0.84rem;
        color: #666666;
        margin-top: 0.3rem;
        margin-bottom: 0.6rem;
    }
    .dish-desc {
        font-size: 0.88rem;
        color: #555555;
        line-height: 1.5;
        margin-bottom: 0.8rem;
    }
    .dish-ingredients-box {
        background: #F8FAFC;
        border-radius: 10px;
        padding: 0.6rem 0.85rem;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
        font-size: 0.84rem;
        border: 1px solid #E2E8F0;
        color: #334155;
    }

    /* BADGES */
    .badge {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .badge-ai {
        background: #EEF2FF;
        color: #4F46E5;
        border: 1px solid #C7D2FE;
    }
    .badge-trad {
        background: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
    }
    .badge-veg {
        background: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }
    .badge-nonveg {
        background: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FECACA;
    }
    .badge-match {
        background: #F0FDF4;
        color: #166534;
        font-weight: 800;
        border: 1px solid #BBF7D0;
    }

    /* YOU MAY ALSO NEED BANNER */
    .sugg-bar {
        background: #FFFFFF;
        border: 1px solid #FFE2CC;
        border-radius: 16px;
        padding: 1.2rem 1.6rem;
        margin-top: 1.6rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 4px 16px rgba(255, 107, 53, 0.08);
    }
    .sugg-title {
        font-size: 1.05rem;
        color: #242424;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .sugg-items {
        color: #FF6B35;
        font-weight: 800;
        margin-left: 6px;
    }
    .sugg-desc {
        font-size: 0.88rem;
        color: #666666;
        margin-top: 0.4rem;
        line-height: 1.45;
    }

    /* STEP INSTRUCTIONS */
    .step-card {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.07);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        display: flex;
        gap: 14px;
        align-items: flex-start;
    }
    .step-number-pill {
        min-width: 38px;
        height: 38px;
        border-radius: 10px;
        background: #FFF0E5;
        color: #FF6B35;
        font-size: 0.95rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #FFD9C2;
    }
    .step-content {
        font-size: 0.95rem;
        color: #242424;
        line-height: 1.55;
        flex: 1;
        padding-top: 4px;
    }

    /* INGREDIENT PILL (DETAIL PAGE) */
    .ing-detail-pill {
        background: #F8FAFC;
        padding: 0.65rem 0.95rem;
        border-radius: 10px;
        margin-bottom: 0.45rem;
        font-size: 0.92rem;
        color: #242424;
        border: 1px solid #E2E8F0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* INTERACTIVE COOKING ASSISTANT */
    .cooking-box {
        background: #FFFFFF;
        border: 2px solid #FFD9C2;
        border-radius: 20px;
        padding: 2.2rem 2.6rem;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.12);
    }
    .step-badge {
        font-size: 0.86rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        color: #FF6B35;
        text-transform: uppercase;
        background: #FFF0E5;
        padding: 0.35rem 0.85rem;
        border-radius: 8px;
        border: 1px solid #FFD9C2;
    }
    .step-text {
        font-size: 1.35rem;
        font-weight: 700;
        color: #242424;
        line-height: 1.65;
        margin-top: 1.4rem;
        margin-bottom: 1.8rem;
    }

    /* STREAMLIT INPUTS */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #242424 !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
    }
    .stTextInput input:focus {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15) !important;
    }
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        color: #242424 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
    }

    /* STREAMLIT BUTTONS */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.65rem 1.4rem !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 4px 14px rgba(255, 107, 53, 0.3) !important;
    }
    .stButton button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(255, 107, 53, 0.4) !important;
    }
    .stButton button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #242424 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.4rem !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
    }
    .stButton button[kind="secondary"]:hover {
        background: #FFF5EE !important;
        border-color: #FF6B35 !important;
        color: #FF6B35 !important;
    }

    /* TOP NAVBAR BUTTONS - IDENTICAL UNIFORM SIZE (ONE SIZE FOR ALL) */
    div[data-testid="stHorizontalBlock"]:first-of-type div.stButton > button {
        height: 44px !important;
        min-height: 44px !important;
        max-height: 44px !important;
        padding: 0 8px !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 12px !important;
        box-sizing: border-box !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type div.stButton > button div[data-testid="stMarkdownContainer"] p {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        margin: 0 !important;
        padding: 0 !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        line-height: 1 !important;
    }

    /* FOOTER */
    .app-footer {
        text-align: center;
        padding: 2.2rem 1rem 1rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(0, 0, 0, 0.06);
        color: #888888;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_dataset():
    """Cached recipe dataset loader."""
    return load_recipe_dataset()


def init_session_state():
    """State initialization."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "en"
    if "user" not in st.session_state:
        st.session_state["user"] = {"username": "guest", "full_name": "Guest Chef"}
    if "ingredient_input" not in st.session_state:
        st.session_state["ingredient_input"] = ""
    if "results" not in st.session_state:
        st.session_state["results"] = []
    if "selected_recipe" not in st.session_state:
        st.session_state["selected_recipe"] = None
    if "active_nav" not in st.session_state:
        st.session_state["active_nav"] = "finder"
    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "customized_recipe" not in st.session_state:
        st.session_state["customized_recipe"] = None
    if "audio_bytes" not in st.session_state:
        st.session_state["audio_bytes"] = None
    if "cooking_mode" not in st.session_state:
        st.session_state["cooking_mode"] = False
    if "current_step_idx" not in st.session_state:
        st.session_state["current_step_idx"] = 0
    if "show_video_reel" not in st.session_state:
        st.session_state["show_video_reel"] = False


# ==============================================================================
# TOP APP NAVIGATION BAR (CLEAN MODERN CONSUMER HEADER)
# ==============================================================================
def render_top_app_bar():
    """Renders the sleek, sticky real-app top navigation header."""
    lang = st.session_state["lang"]
    current_nav = st.session_state["active_nav"]
    user = st.session_state["user"]
    results_count = len(st.session_state["results"])

    col_brand, col_nav = st.columns([1.8, 6.2])

    with col_brand:
        app_name_str = "RecipeAI" if lang == "en" else "சமையல் AI"
        sub_tag_str = "Smart Kitchen Assistant" if lang == "en" else "பாரம்பரிய சமையல் வழிகாட்டி"
        render_html(f"""
        <div style="display: flex; align-items: center; gap: 8px; padding-top: 4px;">
            <span style="font-size: 1.8rem;">🍴</span>
            <div>
                <div class="brand-title">{app_name_str}</div>
                <div class="brand-subtitle">{sub_tag_str}</div>
            </div>
        </div>
        """)

    with col_nav:
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            if st.button(t("find_recipes_tab", lang), key="top_nav_finder", use_container_width=True, type="primary" if current_nav == "finder" else "secondary"):
                st.session_state["active_nav"] = "finder"
                st.session_state["cooking_mode"] = False
                st.session_state["show_video_reel"] = False
                st.rerun()
        with c2:
            res_label = f"{t('results_tab', lang)}" + (f" ({results_count})" if results_count > 0 else "")
            if st.button(res_label, key="top_nav_results", use_container_width=True, type="primary" if current_nav == "results" else "secondary"):
                st.session_state["active_nav"] = "results"
                st.session_state["cooking_mode"] = False
                st.session_state["show_video_reel"] = False
                st.rerun()
        with c3:
            if st.button(t("saved_tab", lang), key="top_nav_saved", use_container_width=True, type="primary" if current_nav == "saved" else "secondary"):
                st.session_state["active_nav"] = "saved"
                st.session_state["cooking_mode"] = False
                st.session_state["show_video_reel"] = False
                st.rerun()
        with c4:
            if st.button(t("history_tab", lang), key="top_nav_history", use_container_width=True, type="primary" if current_nav == "history" else "secondary"):
                st.session_state["active_nav"] = "history"
                st.session_state["cooking_mode"] = False
                st.session_state["show_video_reel"] = False
                st.rerun()
        with c5:
            target_lang = "ta" if lang == "en" else "en"
            lang_btn_text = "🌐 தமிழ்" if lang == "en" else "🌐 English"
            if st.button(lang_btn_text, key="top_lang_toggle", use_container_width=True):
                st.session_state["lang"] = target_lang
                st.rerun()
        with c6:
            is_guest = not user or user.get("username") == "guest"
            if is_guest:
                auth_btn_label = f"🔑 {t('sign_in_nav', lang)}"
                if st.button(auth_btn_label, key="top_auth_btn", use_container_width=True, type="primary" if current_nav == "auth" else "secondary"):
                    st.session_state["active_nav"] = "auth"
                    st.session_state["cooking_mode"] = False
                    st.session_state["show_video_reel"] = False
                    st.rerun()
            else:
                user_display = user.get("username", "chef")
                if len(user_display) > 8:
                    user_display = user_display[:7] + "…"
                if st.button(f"👤 {user_display}", key="top_profile_btn", use_container_width=True, type="primary" if current_nav == "profile" else "secondary"):
                    st.session_state["active_nav"] = "profile"
                    st.session_state["cooking_mode"] = False
                    st.session_state["show_video_reel"] = False
                    st.rerun()

    render_html("<hr style='border: none; border-top: 1px solid rgba(0,0,0,0.06); margin: 0.8rem 0 1.4rem 0;'>")


# ==============================================================================
# SEARCH EXECUTION ENGINE
# ==============================================================================
def execute_recipe_search(input_str: str, selected_cat: str, selected_diet: str, max_time: int, prioritize_waste: bool, lang: str):
    """Core search pipeline with strict ingredient constraints & multi-recipe variations."""
    df = get_dataset()
    cleaned_ings = parse_user_ingredients(input_str)

    if not cleaned_ings:
        st.warning("Please enter at least one valid ingredient." if lang == "en" else "குறைந்தது ஒரு சமையல் பொருளாவது உள்ளிடவும்.")
        return

    main_ings = [i for i in cleaned_ings if not is_pantry_ingredient(i)]

    if len(main_ings) == 0:
        st.warning(
            "You only provided basic pantry items (salt, water, etc.). Please add key ingredients like vegetables, rice, lentils, or meat."
            if lang == "en" else
            "அடிப்படை அஞ்சறைப்பெட்டி பொருட்களை மட்டுமே உள்ளிட்டுள்ளீர்கள். காய்கறி, அரிசி, அல்லது அசைவப் பொருட்களை உள்ளிடவும்."
        )
        return

    if len(main_ings) == 1:
        single_item = main_ings[0].title()
        notice = (
            f"Only one ingredient was provided ('{single_item}'). Please add 2–3 more ingredients for better recipe suggestions."
            if lang == "en" else
            f"ஒரே ஒரு சமையல் பொருள் மட்டுமே வழங்கப்பட்டுள்ளது ('{single_item}'). சிறந்த செய்முறைப் பரிந்துரைகளுக்கு மேலும் 2-3 பொருட்களைச் சேர்க்கவும்."
        )
        st.session_state["low_input_notice"] = notice
        st.session_state["results"] = []
        st.session_state["search_query_display"] = input_str
        st.session_state["user_ingredients"] = cleaned_ings
        st.session_state["selected_recipe"] = None
        st.session_state["cooking_mode"] = False
        st.session_state["show_video_reel"] = False
        st.session_state["active_nav"] = "results"
        st.rerun()
        return

    st.session_state["low_input_notice"] = None
    st.session_state["user_ingredients"] = cleaned_ings
    st.session_state["search_query_display"] = input_str

    with st.spinner("Creating delicious recipes... 🥕 ➜ 🍳 ➜ 🍲" if lang == "en" else "சுவையான சமையல் குறிப்புகள் உருவாகின்றன... 🥕 ➜ 🍳 ➜ 🍲"):
        db_results = filter_and_rank_recipes(
            df=df,
            user_ingredients=cleaned_ings,
            category=selected_cat,
            diet=selected_diet,
            max_time=max_time,
            prioritize_food_waste=prioritize_waste,
            top_k=5,
            strict_validation=True
        )

        results = list(db_results)

        desired_ai_count = max(2, 4 - len(results))
        ai_recipes = generate_multiple_ingredient_recipes(
            user_ingredients=cleaned_ings,
            count=desired_ai_count,
            lang=lang
        )

        existing_titles = {r["name_en"].lower() for r in results}
        for rec in ai_recipes:
            title_to_check = rec.get("recipe_name", "").lower()
            if rec.get("valid") and title_to_check not in existing_titles:
                name_en_val = rec.get("recipe_name", "Chef's Special")
                name_ta_val = rec.get("recipe_name_ta", name_en_val)
                ai_card = {
                    "id": f"ai_gen_{len(results)}",
                    "name_en": name_en_val,
                    "name_ta": name_ta_val,
                    "description": rec.get("description", f"Authentic dish cooked using {', '.join(cleaned_ings)}."),
                    "category": rec.get("category", selected_cat if selected_cat != "All" else "Main Course"),
                    "diet": rec.get("diet", "Non-Vegetarian" if any(m in cleaned_ings for m in ["chicken", "mutton", "fish", "egg"]) else "Vegetarian"),
                    "time_mins": rec.get("cooking_time_mins", 25),
                    "difficulty": "Medium",
                    "ingredients_en": "\n".join(rec.get("ingredients_en", [])),
                    "ingredients_ta": "\n".join(rec.get("ingredients_ta", [])),
                    "instructions_en": "\n\n".join(rec.get("steps_en", [])),
                    "instructions_ta": "\n\n".join(rec.get("steps_ta", [])),
                    "steps_list_en": rec.get("steps_en", []),
                    "steps_list_ta": rec.get("steps_ta", []),
                    "matched_ingredients": cleaned_ings,
                    "missing_ingredients": ["Salt", "Oil", "Water", "Spices"],
                    "match_score": 1.0,
                    "is_ai_generated": True
                }
                results.append(ai_card)
                existing_titles.add(title_to_check)

        st.session_state["results"] = results
        st.session_state["selected_recipe"] = None
        st.session_state["cooking_mode"] = False
        st.session_state["show_video_reel"] = False
        st.session_state["active_nav"] = "results"

        # Log history
        now_str = datetime.datetime.now().strftime("%b %d, %H:%M")
        st.session_state["history"].insert(0, {
            "query": input_str,
            "timestamp": now_str,
            "matches_count": len(results),
            "category": selected_cat
        })
        st.rerun()


# ==============================================================================
# SCREEN 1: RECIPE FINDER (HERO & PREMIUM INGREDIENT INPUT)
# ==============================================================================
def render_recipe_finder_page():
    """Main recipe discovery dashboard with Hero, Premium Input Card, and Quick Chips."""
    lang = st.session_state["lang"]

    # 1. BEAUTIFUL TOP HERO BANNER
    hero_title_text = t("hero_title", lang)
    hero_sub_text = t("hero_subtitle", lang)

    render_html(f"""
    <div class="hero-banner">
        <div class="hero-title">
            🍲 {hero_title_text}
        </div>
        <div class="hero-subtitle">
            {hero_sub_text}
        </div>
        <div class="hero-flow">
            <span>🛒 Ingredients</span>
            <span>➜</span>
            <span>🤖 AI Chef</span>
            <span>➜</span>
            <span>✨ Delicious Recipes</span>
        </div>
    </div>
    """)

    # 2. PREMIUM INGREDIENT INPUT CARD
    render_html(f"""
    <div class="premium-card">
        <div class="card-heading">
            {t('input_heading', lang)}
        </div>
        <div class="card-subtitle">
            {t('input_sub', lang)}
        </div>
    </div>
    """)

    with st.container():
        # Voice input button (Styled circular microphone)
        render_voice_input_button(lang=lang)

        # Main Input Field
        user_input = st.text_input(
            "Input",
            value=st.session_state.get("ingredient_input", ""),
            placeholder=t('input_placeholder', lang),
            label_visibility="collapsed",
            help="Example: chicken, tomato, onion, chilli" if lang == "en" else "எடுத்துக்காட்டு: கோழி, தக்காளி, வெங்காயம், மிளகாய்"
        )
        st.session_state["ingredient_input"] = user_input

        # 3. QUICK INGREDIENT CHIPS (Click to append/add)
        quick_chips = [
            ("🍅 Tomato" if lang == "en" else "🍅 தக்காளி", "tomato"),
            ("🥔 Potato" if lang == "en" else "🥔 உருளை", "potato"),
            ("🧅 Onion" if lang == "en" else "🧅 வெங்காயம்", "onion"),
            ("🌶️ Chilli" if lang == "en" else "🌶️ மிளகாய்", "chilli"),
            ("🥕 Carrot" if lang == "en" else "🥕 கேரட்", "carrot"),
            ("🍗 Chicken" if lang == "en" else "🍗 கோழி", "chicken"),
            ("🥚 Egg" if lang == "en" else "🥚 முட்டை", "egg"),
            ("🧄 Garlic" if lang == "en" else "🧄 பூண்டு", "garlic"),
            ("🌿 Curry Leaves" if lang == "en" else "🌿 கருவேப்பிலை", "curry leaf"),
            ("🧀 Paneer" if lang == "en" else "🧀 பன்னீர்", "paneer"),
            ("🍚 Rice" if lang == "en" else "🍚 சாதம்", "rice"),
            ("🥛 Curd" if lang == "en" else "🥛 தயிர்", "curd")
        ]

        render_html(f"""
        <div style="font-size: 0.85rem; font-weight: 700; color: #555555; margin-top: 0.6rem; margin-bottom: 0.4rem;">
            {'Tap to quickly add ingredients:' if lang == 'en' else 'விரைவாக சேர்க்க கிளிக் செய்யவும்:'}
        </div>
        """)

        # 2 rows of clickable chips
        row1_cols = st.columns(6)
        for idx, (label, token) in enumerate(quick_chips[:6]):
            with row1_cols[idx]:
                if st.button(label, key=f"quick_chip_r1_{idx}", use_container_width=True):
                    current = st.session_state.get("ingredient_input", "")
                    toks = parse_user_ingredients(current)
                    if token not in toks:
                        st.session_state["ingredient_input"] = f"{current.rstrip(',')}, {token}" if current.strip() else token
                        st.rerun()

        row2_cols = st.columns(6)
        for idx, (label, token) in enumerate(quick_chips[6:]):
            with row2_cols[idx]:
                if st.button(label, key=f"quick_chip_r2_{idx}", use_container_width=True):
                    current = st.session_state.get("ingredient_input", "")
                    toks = parse_user_ingredients(current)
                    if token not in toks:
                        st.session_state["ingredient_input"] = f"{current.rstrip(',')}, {token}" if current.strip() else token
                        st.rerun()

        # Removable active ingredient pills
        current_tokens = parse_user_ingredients(user_input)
        if current_tokens:
            st.write("")
            chip_cols = st.columns(min(len(current_tokens) + 1, 8))
            for i, tok in enumerate(current_tokens[:7]):
                with chip_cols[i]:
                    if st.button(f"{tok.title()} ✕", key=f"active_chip_{tok}_{i}", use_container_width=True):
                        remaining = [t for j, t in enumerate(current_tokens) if j != i]
                        st.session_state["ingredient_input"] = ", ".join(remaining)
                        st.rerun()
            with chip_cols[-1]:
                if st.button(t("clear_all_btn", lang), key="btn_clear_all", use_container_width=True):
                    st.session_state["ingredient_input"] = ""
                    st.rerun()

        st.write("")

        # Filter Pills Row
        f1, f2, f3, f4 = st.columns([2, 1.4, 1.4, 1.2])
        with f1:
            cat_options = [
                t("cat_all", lang),
                t("cat_breakfast", lang),
                t("cat_lunch", lang),
                t("cat_snacks", lang),
                t("cat_sweets", lang),
                t("cat_dinner", lang)
            ]
            selected_cat = st.selectbox(t("meal_category", lang), cat_options, index=0)

        with f2:
            diet_options = [
                t("diet_all", lang),
                t("diet_veg", lang),
                t("diet_nonveg", lang)
            ]
            selected_diet = st.selectbox(t("diet_pref", lang), diet_options, index=0)

        with f3:
            time_options = ["Any" if lang == "en" else "அனைத்தும்", "15 mins", "30 mins", "45 mins"]
            selected_time_str = st.selectbox(t("cooking_time", lang), time_options, index=0)
            max_time = 15 if "15" in selected_time_str else (30 if "30" in selected_time_str else (45 if "45" in selected_time_str else None))

        with f4:
            st.write("")
            st.write("")
            prioritize_waste = st.checkbox(t("use_available_first", lang), value=False)

        st.write("")

        # Prominent Vibrant Orange Search Button: "✨ Generate Recipes"
        btn_generate_text = t("generate_recipes_btn", lang)
        if st.button(btn_generate_text, type="primary", use_container_width=True, key="btn_primary_search"):
            execute_recipe_search(user_input, selected_cat, selected_diet, max_time, prioritize_waste, lang)

    # 4. EMPTY STATE & POPULAR COMBINATIONS
    if not user_input.strip():
        render_html(f"""
        <div class="premium-card" style="margin-top: 1.5rem; text-align: center; background: linear-gradient(135deg, #FFFFFF 0%, #FFFDF9 100%);">
            <div style="font-size: 2.8rem; margin-bottom: 0.5rem;">🍳</div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #242424; margin-bottom: 0.3rem;">
                {t('empty_state_title', lang)}
            </div>
            <div style="color: #666666; font-size: 0.92rem; margin-bottom: 1.2rem;">
                {t('empty_state_desc', lang)}
            </div>
        </div>
        """)

        p1, p2, p3, p4 = st.columns(4)
        with p1:
            lbl1 = "🍗 Chicken + Tomato" if lang == "en" else "🍗 கோழி + தக்காளி"
            if st.button(lbl1, use_container_width=True, key="quick_c1"):
                st.session_state["ingredient_input"] = "chicken, tomato, chilli"
                execute_recipe_search("chicken, tomato, chilli", "All", "All", None, False, lang)
        with p2:
            lbl2 = "🥚 Egg + Onion" if lang == "en" else "🥚 முட்டை + வெங்காயம்"
            if st.button(lbl2, use_container_width=True, key="quick_c2"):
                st.session_state["ingredient_input"] = "egg, onion, chilli"
                execute_recipe_search("egg, onion, chilli", "All", "All", None, False, lang)
        with p3:
            lbl3 = "🥔 Potato + Onion" if lang == "en" else "🥔 உருளை + வெங்காயம்"
            if st.button(lbl3, use_container_width=True, key="quick_c3"):
                st.session_state["ingredient_input"] = "potato, onion, chilli"
                execute_recipe_search("potato, onion, chilli", "All", "All", None, False, lang)
        with p4:
            lbl4 = "🍚 Rice + Curd" if lang == "en" else "🍚 சாதம் + தயிர்"
            if st.button(lbl4, use_container_width=True, key="quick_c4"):
                st.session_state["ingredient_input"] = "rice, curd"
                execute_recipe_search("rice, curd", "All", "All", None, False, lang)


# ==============================================================================
# SCREEN 2: RECIPE SEARCH RESULTS (MODERN FOOD-TECH CARDS GRID)
# ==============================================================================
def render_search_results_page():
    """Displays 3-5 distinct recipes in a modern 2-column food card grid."""
    lang = st.session_state["lang"]
    results = st.session_state["results"]
    query_str = st.session_state.get("search_query_display", "")
    low_input_notice = st.session_state.get("low_input_notice")
    user_ings = st.session_state.get("user_ingredients", [])

    # Results Header
    col_t1, col_t2 = st.columns([4, 1.2])
    with col_t1:
        st.markdown(f"### {t('results_heading', lang)} ({len(results)})")
        if query_str:
            st.markdown(f"**{t('ingredients_label', lang)}:** `{query_str}`")
    with col_t2:
        if st.button(f"{t('new_search_btn', lang)}", use_container_width=True):
            st.session_state["active_nav"] = "finder"
            st.rerun()

    render_html("<hr style='border: none; border-top: 1px solid rgba(0,0,0,0.06); margin: 0.6rem 0 1.2rem 0;'>")

    if low_input_notice:
        st.warning(f"⚠️ {low_input_notice}")

    # ERROR / EMPTY STATE
    if not results:
        render_html(f"""
        <div class="premium-card" style="text-align: center; max-width: 600px; margin: 2rem auto;">
            <div style="font-size: 3rem; margin-bottom: 0.8rem;">🍲</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #242424; margin-bottom: 0.5rem;">
                {t('error_state_title', lang)}
            </div>
            <div style="color: #666666; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">
                {t('error_state_desc', lang)}
            </div>
        </div>
        """)
        c_e1, c_e_btn, c_e2 = st.columns([1, 1.5, 1])
        with c_e_btn:
            if st.button(f"🔄 {t('try_again_btn', lang)}", type="primary", use_container_width=True):
                st.session_state["active_nav"] = "finder"
                st.rerun()
        return

    # Render Recipes in a Modern 2-Column Responsive Grid
    for i in range(0, len(results), 2):
        row_recipes = results[i:i+2]
        cols = st.columns(2, gap="medium")

        for c_idx, r in enumerate(row_recipes):
            actual_idx = i + c_idx
            dish_name = r["name_en"] if lang == "en" else r["name_ta"]
            diet_class = "badge-veg" if r["diet"] == "Vegetarian" else "badge-nonveg"
            diet_icon = "🟢" if r["diet"] == "Vegetarian" else "🔴"
            source_badge_class = "badge-ai" if r.get("is_ai_generated") else "badge-trad"
            source_badge_text = t("ai_chef_badge", lang) if r.get("is_ai_generated") else t("traditional_badge", lang)
            desc_text = r.get("description", "")
            matched_str = ", ".join(r.get("matched_ingredients", [])) if r.get("matched_ingredients") else "Standard"

            dish_icon = "🍗" if any(m in dish_name.lower() for m in ["chicken", "mutton"]) else ("🐟" if "fish" in dish_name.lower() else ("🥚" if "egg" in dish_name.lower() else "🍲"))

            with cols[c_idx]:
                with st.container():
                    desc_html = f"<div class='dish-desc'>{desc_text}</div>" if desc_text else ""
                    card_html = f"""
                    <div class="recipe-food-card">
                        <div>
                            <div class="dish-card-banner">
                                <div class="dish-icon-badge">{dish_icon}</div>
                                <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                                    <span class="badge {diet_class}">{diet_icon} {r['diet']}</span>
                                    <span class="badge {source_badge_class}">{source_badge_text}</span>
                                    <span class="badge badge-match">✓ 100% Match</span>
                                </div>
                            </div>
                            <div class="dish-title">{dish_name}</div>
                            <div class="dish-meta-row">
                                <span>⏱️ {r['time_mins']} {t('mins', lang)}</span>
                                <span>•</span>
                                <span>👥 4 {t('servings_label', lang)}</span>
                                <span>•</span>
                                <span>🍳 {r.get('category', 'Main Course')}</span>
                            </div>
                            {desc_html}
                            <div class="dish-ingredients-box">
                                <span style="color: #166534; font-weight: 700;">✓ {t('available_ingredients_title', lang)}:</span> {matched_str}
                            </div>
                        </div>
                    </div>
                    """
                    render_html(card_html)

                    # View Recipe Button
                    btn_view_label = f"{t('view_recipe_btn', lang)}"
                    if st.button(btn_view_label, key=f"btn_cook_{actual_idx}", use_container_width=True, type="primary"):
                        st.session_state["selected_recipe"] = r
                        st.session_state["nav_source"] = "results"
                        st.session_state["active_nav"] = "detail"
                        st.session_state["cooking_mode"] = False
                        st.session_state["current_step_idx"] = 0
                        st.session_state["customized_recipe"] = None
                        st.session_state["audio_bytes"] = None
                        st.session_state["show_video_reel"] = False
                        st.rerun()

                    st.write("")

    # =========================================================================
    # "💡 YOU MAY ALSO NEED" RECOMMENDATION BAR
    # =========================================================================
    sugg_data = get_compact_ingredient_suggestions(user_ings, results, lang=lang, max_items=3)
    if sugg_data and sugg_data.get("items"):
        render_html(f"""
        <div class="sugg-bar">
            <div class="sugg-title">
                <span>💡</span> <span>{t('you_may_also_need_title', lang)}:</span>
                <span class="sugg-items">{sugg_data['display_str']}</span>
            </div>
            <div class="sugg-desc">{sugg_data['reason']}</div>
        </div>
        """)

        col_sugg_l, col_sugg_btn = st.columns([3.5, 1.5])
        with col_sugg_btn:
            btn_txt = f"{t('suggestions_add_btn', lang)}"
            if st.button(btn_txt, key="btn_add_and_generate", use_container_width=True, type="primary"):
                current_input = st.session_state.get("ingredient_input", "").strip()
                query_display = st.session_state.get("search_query_display", "").strip()
                base_str = current_input or query_display or ", ".join(user_ings)

                sugg_tokens = sugg_data.get("raw_tokens", [])
                tokens_to_add = [tok for tok in sugg_tokens if tok not in user_ings]
                if not tokens_to_add and sugg_tokens:
                    tokens_to_add = sugg_tokens[:2]

                if tokens_to_add:
                    add_str = ", ".join(tokens_to_add)
                    new_input = f"{base_str.rstrip(',')}, {add_str}" if base_str else add_str
                else:
                    new_input = base_str

                st.session_state["ingredient_input"] = new_input
                execute_recipe_search(new_input, "All", "All", None, False, lang)


# ==============================================================================
# SCREEN 3: RECIPE DETAIL VIEW (PREMIUM TYPOGRAPHY & NUMBERED STEPS)
# ==============================================================================
def render_recipe_detail_page():
    """Interactive recipe detail with clean ingredients breakdown, numbered steps, video reel, and cooking assistant."""
    lang = st.session_state["lang"]
    user = st.session_state["user"]
    r = st.session_state["selected_recipe"]
    nav_source = st.session_state.get("nav_source", "results")

    if not r:
        st.session_state["active_nav"] = "results"
        st.rerun()

    dish_name = r["name_en"] if lang == "en" else r["name_ta"]
    back_label = t("back_to_results", lang) if nav_source == "results" else t("back_to_saved", lang)

    # Top Back / Save Bar
    nav_col1, nav_col2 = st.columns([4, 1.5])
    with nav_col1:
        if st.button(back_label, key="detail_back_btn"):
            st.session_state["active_nav"] = nav_source
            st.session_state["selected_recipe"] = None
            st.session_state["cooking_mode"] = False
            st.session_state["current_step_idx"] = 0
            st.session_state["show_video_reel"] = False
            st.rerun()
    with nav_col2:
        if user and user["username"] != "guest":
            favs = get_favorites(user["username"])
            is_saved = (r["name_en"] in favs) or (r["name_ta"] in favs)
            fav_label = f"❌ {t('unsave_recipe_btn', lang)}" if is_saved else f"❤️ {t('save_recipe_btn', lang)}"
            if st.button(fav_label, key="detail_fav_toggle", use_container_width=True):
                toggle_favorite(user["username"], r["name_en"], r["category"])
                st.rerun()

    # Steps list extraction
    if lang == "en":
        steps_list = r.get("steps_list_en") or [s.strip() for s in r.get("instructions_en", "").split("\n\n") if s.strip()]
    else:
        steps_list = r.get("steps_list_ta") or [s.strip() for s in r.get("instructions_ta", "").split("\n\n") if s.strip()]
    if not steps_list:
        raw_inst = r.get("instructions_en" if lang == "en" else "instructions_ta", "")
        steps_list = [s.strip() for s in raw_inst.splitlines() if s.strip()]

    # =========================================================================
    # INTERACTIVE STEP-BY-STEP COOKING MODE
    # =========================================================================
    if st.session_state.get("cooking_mode") and steps_list:
        total_steps = len(steps_list)
        cur_idx = st.session_state.get("current_step_idx", 0)

        render_html(f"""
        <div class="cooking-box">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="step-badge">{t('step_label', lang)} {cur_idx + 1} {t('of_label', lang)} {total_steps}</span>
                <span style="color: #666666; font-size: 0.95rem; font-weight: 600;">🍲 {dish_name}</span>
            </div>
            <div class="step-text">{steps_list[cur_idx]}</div>
        </div>
        """)

        st.progress((cur_idx + 1) / total_steps)

        # Voice audio for current step
        step_audio_text = f"Step {cur_idx + 1}. {steps_list[cur_idx]}"
        c_audio1, c_audio2 = st.columns([3, 1])
        with c_audio1:
            if st.button(f"🔊 {t('listen_voice_btn', lang)}", key=f"btn_step_audio_{cur_idx}"):
                with st.spinner("Preparing step audio..." if lang == "en" else "குரல் தயாராகிறது..."):
                    try:
                        audio_fp = generate_recipe_audio(step_audio_text, lang=lang)
                        st.session_state["audio_bytes"] = audio_fp.getvalue()
                    except Exception as e:
                        st.warning(f"Voice narration unavailable: {e}")
            if st.session_state.get("audio_bytes"):
                st.audio(st.session_state["audio_bytes"], format="audio/mp3")

        st.write("")

        # Controls
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 2, 1.5])
        with ctrl_col1:
            if cur_idx > 0:
                if st.button(f"{t('prev_step_btn', lang)}", key="btn_prev_step", use_container_width=True):
                    st.session_state["current_step_idx"] = cur_idx - 1
                    st.session_state["audio_bytes"] = None
                    st.rerun()
        with ctrl_col2:
            if st.button(f"{t('exit_cooking_btn', lang)}", key="btn_exit_cook", use_container_width=True):
                st.session_state["cooking_mode"] = False
                st.session_state["current_step_idx"] = 0
                st.session_state["audio_bytes"] = None
                st.rerun()
        with ctrl_col3:
            if cur_idx < total_steps - 1:
                if st.button(f"{t('next_step_btn', lang)}", key="btn_next_step", use_container_width=True, type="primary"):
                    st.session_state["current_step_idx"] = cur_idx + 1
                    st.session_state["audio_bytes"] = None
                    st.rerun()
            else:
                st.success(t("cooking_complete", lang))
        return

    # =========================================================================
    # STANDARD RECIPE DETAIL OVERVIEW CARD
    # =========================================================================
    diet_class = "badge-veg" if r["diet"] == "Vegetarian" else "badge-nonveg"
    diet_icon = "🟢" if r["diet"] == "Vegetarian" else "🔴"

    render_html(f"""
    <div class="premium-card" style="margin-top: 0.8rem; margin-bottom: 1.4rem;">
        <div style="font-size: 2.2rem; font-weight: 800; color: #242424; line-height: 1.2;">🍲 {dish_name}</div>
        <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 0.9rem; color: #666666; font-size: 0.92rem; align-items: center;">
            <span>⏱️ {r['time_mins']} {t('mins', lang)}</span>
            <span>•</span>
            <span>👥 4 {t('servings_label', lang)}</span>
            <span>•</span>
            <span>🍽️ {r.get('category', 'Main Course')}</span>
            <span>•</span>
            <span class="badge {diet_class}">{diet_icon} {r['diet']}</span>
            <span class="badge badge-match">✓ 100% Match</span>
        </div>
    </div>
    """)

    # =========================================================================
    # ACTION BAR: START COOKING
    # =========================================================================
    if st.button(f"{t('start_cooking_btn', lang)}", key="btn_start_cooking_main", type="primary", use_container_width=True):
        st.session_state["cooking_mode"] = True
        st.session_state["current_step_idx"] = 0
        st.session_state["audio_bytes"] = None
        st.rerun()

    st.write("")

    # =========================================================================
    # 2-COLUMN LAYOUT: INGREDIENTS LIST & NUMBERED COOKING STEPS
    # =========================================================================
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        # Ingredients Section
        render_html(f"""
        <div style="margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #242424; font-size: 1.35rem; font-weight: 800;">
                🛒 {t('ingredients_heading', lang)}
            </h3>
        </div>
        """)

        ing_lines = [line.strip("- *•").strip() for line in (r["ingredients_en"] if lang == "en" else r["ingredients_ta"]).splitlines() if line.strip()]
        for ing_item in ing_lines:
            render_html(f"""
            <div class="ing-detail-pill">
                <span style="color: #FF6B35; font-weight: 800; font-size: 1.1rem;">•</span>
                <span style="font-weight: 600;">{ing_item}</span>
            </div>
            """)

        st.write("")
        if r.get("matched_ingredients"):
            render_html(f"<div style='margin-top: 0.4rem;'><span style='color: #166534; font-weight: 700;'>✓ {t('available_ingredients_title', lang)}:</span> {', '.join(r['matched_ingredients'])}</div>")
        if r.get("missing_ingredients"):
            render_html(f"<div style='margin-top: 0.2rem;'><span style='color:#666666; font-size:0.86rem;'>○ {t('pantry_ingredients_title', lang)}: {', '.join(r['missing_ingredients'])}</span></div>")

    with col_right:
        # Numbered Cooking Instructions Section
        render_html(f"""
        <div style="margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #242424; font-size: 1.35rem; font-weight: 800;">
                👨‍🍳 {t('cooking_steps_title', lang)}
            </h3>
        </div>
        """)

        # Visually separated numbered cards (01, 02, 03...)
        for s_idx, step_text in enumerate(steps_list):
            step_num_str = f"{s_idx + 1:02d}"
            render_html(f"""
            <div class="step-card">
                <div class="step-number-pill">{step_num_str}</div>
                <div class="step-content">{step_text}</div>
            </div>
            """)

        render_html("<hr style='border: none; border-top: 1px solid rgba(0,0,0,0.06); margin: 1.2rem 0;'>")

        # Hands-free voice playback
        st.markdown(f"**{t('listen_voice_btn', lang)}**")
        if st.button(f"▶️ {t('listen_voice_btn', lang)}", key="btn_play_audio", use_container_width=True):
            with st.spinner("Preparing audio..." if lang == "en" else "குரல் தயாராகிறது..."):
                try:
                    inst_full_text = " ".join(steps_list)
                    speech_text = f"{dish_name}. " + inst_full_text
                    audio_fp = generate_recipe_audio(speech_text, lang=lang)
                    st.session_state["audio_bytes"] = audio_fp.getvalue()
                except Exception as e:
                    st.warning(f"Voice playback unavailable: {e}")

        if st.session_state.get("audio_bytes"):
            st.audio(st.session_state["audio_bytes"], format="audio/mp3")

        render_html("<hr style='border: none; border-top: 1px solid rgba(0,0,0,0.06); margin: 1.2rem 0;'>")

        # AI Servings Scaler
        st.markdown(f"**{t('ai_customize_btn', lang)}**")
        serv_c1, serv_c2 = st.columns([1, 2])
        with serv_c1:
            serv_count = st.selectbox(t("servings", lang), [1, 2, 3, 4, 6], index=1, key="sel_servings")
        with serv_c2:
            st.write("")
            if st.button(t("ai_customize_btn", lang), type="primary", use_container_width=True, key="btn_run_ai"):
                with st.spinner("AI Chef adapting recipe..." if lang == "en" else "AI சமையல் கலைஞர் செய்முறையைத் தயாரிக்கிறார்..."):
                    custom = customize_recipe_with_llm(
                        recipe=r,
                        user_ingredients=st.session_state.get("user_ingredients", []),
                        servings=serv_count,
                        lang=lang
                    )
                    st.session_state["customized_recipe"] = custom

    if st.session_state.get("customized_recipe"):
        st.markdown("---")
        ai_res = st.session_state["customized_recipe"]
        st.markdown(ai_res["notice"])
        st.markdown(ai_res["content"])


# ==============================================================================
# SCREEN 4: SAVED DISHES
# ==============================================================================
def render_saved_recipes_page():
    """Saved dishes screen with light food-tech styling."""
    lang = st.session_state["lang"]
    user = st.session_state["user"]

    st.markdown(f"### {t('saved_title', lang)}")
    st.write("")

    if not user or user.get("username") == "guest":
        render_html(f"""
        <div class="premium-card" style="text-align: center; max-width: 580px; margin: 2rem auto;">
            <div style="font-size: 3.2rem; margin-bottom: 0.8rem;">❤️</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: #242424; margin-bottom: 0.5rem;">{t('saved_title', lang)}</div>
            <div style="color: #666666; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.6rem;">
                {t('saved_login_prompt', lang)}
            </div>
        </div>
        """)
        c_sp1, c_sp_btn, c_sp2 = st.columns([1, 1.8, 1])
        with c_sp_btn:
            if st.button(t('sign_in_to_save_btn', lang), key="btn_saved_open_auth", type="primary", use_container_width=True):
                st.session_state["active_nav"] = "auth"
                st.session_state["cooking_mode"] = False
                st.session_state["show_video_reel"] = False
                st.rerun()
        return

    favs = get_favorites(user["username"])
    if not favs:
        st.info("You haven't saved any recipes yet! Explore dishes and tap the heart icon." if lang == "en" else "சேமிக்கப்பட்ட உணவுகள் எதுவும் இல்லை!")
        return

    df = get_dataset()
    for fav_name in favs:
        match_df = df[df["name_en"] == fav_name]
        if not match_df.empty:
            r = match_df.iloc[0].to_dict()
            dish_title = r["name_en"] if lang == "en" else r["name_ta"]
            with st.container():
                render_html(f"""
                <div class="recipe-food-card">
                    <div style="font-size: 1.25rem; font-weight: 800; color: #242424;">{dish_title}</div>
                    <div style="color: #666666; font-size: 0.9rem; margin-top: 0.2rem;">⏱️ {r['time_mins']} {t('mins', lang)} • ⚡ {r['difficulty']}</div>
                </div>
                """)
                col_d, col_b = st.columns([4, 1.2])
                with col_b:
                    if st.button(f"{t('view_recipe_btn', lang)}", key=f"btn_fav_{fav_name}", use_container_width=True, type="primary"):
                        st.session_state["selected_recipe"] = r
                        st.session_state["nav_source"] = "saved"
                        st.session_state["active_nav"] = "detail"
                        st.session_state["cooking_mode"] = False
                        st.session_state["show_video_reel"] = False
                        st.rerun()


# ==============================================================================
# SCREEN 5: SEARCH HISTORY
# ==============================================================================
def render_history_page():
    """Search history screen with full bilingual localization."""
    lang = st.session_state["lang"]
    history = st.session_state.get("history", [])

    st.markdown(f"### {t('history_title', lang)}")
    st.write("")

    if not history:
        st.info(t("no_history_text", lang))
        return

    ta_months = {
        "Jan": "ஜன", "Feb": "பிப்", "Mar": "மார்", "Apr": "ஏப்",
        "May": "மே", "Jun": "ஜூன்", "Jul": "ஜூலை", "Aug": "ஆக",
        "Sep": "செப்", "Oct": "அக்", "Nov": "நவ", "Dec": "டிச"
    }

    matches_text = t("matches_found_text", lang)
    search_again_text = t("search_again_btn", lang)

    for idx, entry in enumerate(history):
        with st.container():
            query_str = entry.get('query', '')
            query_display = query_str
            if lang == "ta":
                tokens = [tk.strip() for tk in query_str.split(",") if tk.strip()]
                ta_tokens = [get_tamil_ingredient_name(tk) for tk in tokens]
                query_display = ", ".join(ta_tokens)

            time_display = entry.get('timestamp', '')
            if lang == "ta":
                for en_m, ta_m in ta_months.items():
                    if en_m in time_display:
                        time_display = time_display.replace(en_m, ta_m)
                        break

            render_html(f"""
            <div class="recipe-food-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-weight: 700; font-size: 1.05rem; color: #242424;">🔍 "{query_display}"</div>
                    <div style="color: #888888; font-size: 0.85rem;">⏱️ {time_display}</div>
                </div>
                <div style="margin-top: 0.4rem; color: #166534; font-size: 0.88rem;">✓ {entry['matches_count']} {matches_text}</div>
            </div>
            """)
            if st.button(f"🔄 {search_again_text}", key=f"btn_hist_{idx}"):
                st.session_state["ingredient_input"] = entry["query"]
                execute_recipe_search(entry["query"], entry.get("category", "All"), "All", None, False, lang)


# ==============================================================================
# SCREEN 6: USER PROFILE
# ==============================================================================
def render_profile_page():
    """User profile overview screen with stats and session management."""
    lang = st.session_state["lang"]
    user = st.session_state.get("user")

    st.markdown(f"### {t('profile_title', lang)}")
    st.write("")

    if not user or user.get("username") == "guest":
        render_html(f"""
        <div class="premium-card" style="max-width: 620px;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="width: 58px; height: 58px; border-radius: 50%; background: #FFF0E5; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; border: 1px solid #FFD9C2;">
                    👤
                </div>
                <div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #242424;">Guest Chef</div>
                    <div style="color: #888888; font-size: 0.9rem;">@guest</div>
                </div>
            </div>
            <div style="margin-top: 1.2rem; color: #555555; font-size: 0.92rem; line-height: 1.6; border-top: 1px solid rgba(0,0,0,0.06); padding-top: 1rem;">
                {'Sign in or create an account to bookmark your favorite Tamil Nadu dishes, persist search history, and personalize your kitchen experience.' if lang == 'en' else 'உணவுகளைச் சேமிக்கவும், தேடல் வரலாற்றைப் பாதுகாக்கவும் உங்கள் கணக்கில் உள்நுழையவும் அல்லது புதிய கணக்கை உருவாக்கவும்.'}
            </div>
        </div>
        """)

        st.write("")
        col_p1, col_p2 = st.columns([1.5, 2])
        with col_p1:
            if st.button(f"🔑 {t('sign_in_nav', lang)}", key="btn_profile_goto_auth", type="primary", use_container_width=True):
                st.session_state["active_nav"] = "auth"
                st.session_state["cooking_mode"] = False
                st.session_state["show_video_reel"] = False
                st.rerun()
        return

    fav_count = len(get_favorites(user["username"]))
    history_count = len(st.session_state.get("history", []))

    render_html(f"""
    <div class="premium-card" style="max-width: 620px;">
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 4px 14px rgba(255, 107, 53, 0.3);">
                👨‍🍳
            </div>
            <div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #242424;">{user['full_name']}</div>
                <div style="color: #FF6B35; font-size: 0.92rem; font-weight: 600;">@{user['username']} • Active Chef</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 1.4rem; padding-top: 1.2rem; border-top: 1px solid rgba(0,0,0,0.06);">
            <div style="background: #FFF9F3; padding: 1rem; border-radius: 12px; border: 1px solid #FFE2CC; text-align: center;">
                <div style="font-size: 1.6rem; font-weight: 800; color: #FF6B35;">{fav_count}</div>
                <div style="color: #666666; font-size: 0.85rem; font-weight: 600; margin-top: 4px;">❤️ {t('saved_dishes_count', lang)}</div>
            </div>
            <div style="background: #F0FDF4; padding: 1rem; border-radius: 12px; border: 1px solid #BBF7D0; text-align: center;">
                <div style="font-size: 1.6rem; font-weight: 800; color: #166534;">{history_count}</div>
                <div style="color: #666666; font-size: 0.85rem; font-weight: 600; margin-top: 4px;">🔍 {t('search_history_count', lang)}</div>
            </div>
        </div>
        <div style="margin-top: 1.2rem; color: #666666; font-size: 0.88rem; line-height: 1.6;">
            🍲 System: <b>AI Recipe Generator</b><br>
            🌐 Active Language: <b>{'English' if lang == 'en' else 'தமிழ்'}</b>
        </div>
    </div>
    """)

    st.write("")
    c_btn1, c_btn2, c_btn3 = st.columns([1.5, 1.5, 1.2])
    with c_btn1:
        if st.button(t("saved_tab", lang), key="btn_profile_saved", use_container_width=True):
            st.session_state["active_nav"] = "saved"
            st.session_state["cooking_mode"] = False
            st.session_state["show_video_reel"] = False
            st.rerun()
    with c_btn2:
        if st.button(t("find_recipes_tab", lang), key="btn_profile_finder", use_container_width=True):
            st.session_state["active_nav"] = "finder"
            st.session_state["cooking_mode"] = False
            st.session_state["show_video_reel"] = False
            st.rerun()
    with c_btn3:
        if st.button(f"🚪 {t('logout', lang)}", key="btn_logout_profile", use_container_width=True):
            st.session_state["user"] = {"username": "guest", "full_name": "Guest Chef"}
            st.session_state["active_nav"] = "finder"
            st.rerun()


# ==============================================================================
# SCREEN 7: SIGN IN & SIGN UP (AUTHENTICATION)
# ==============================================================================
def render_auth_page():
    """Clean food-tech authentication screen (Sign In & Sign Up)."""
    lang = st.session_state["lang"]
    user = st.session_state.get("user")

    if user and user.get("username") != "guest":
        st.session_state["active_nav"] = "profile"
        st.rerun()

    col_l, col_center, col_r = st.columns([1, 2.2, 1])

    with col_center:
        app_name_str = "RecipeAI Kitchen" if lang == "en" else "சமையல் AI சமையலறை"
        render_html(f"""
        <div class="premium-card" style="text-align: center; background: linear-gradient(135deg, #FFF0E5 0%, #FFFFFF 100%); border: 1px solid #FFE2CC;">
            <div style="width: 64px; height: 64px; margin: 0 auto 1rem auto; border-radius: 50%; background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); display: flex; align-items: center; justify-content: center; font-size: 2.2rem; box-shadow: 0 4px 14px rgba(255, 107, 53, 0.3);">
                🍲
            </div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #242424; line-height: 1.2;">
                {app_name_str}
            </div>
            <div style="color: #666666; font-size: 0.92rem; margin-top: 0.5rem; line-height: 1.5;">
                {t('sign_in_subtitle', lang)}
            </div>
        </div>
        """)

        auth_tab1, auth_tab2 = st.tabs([f"🔑 {t('sign_in_tab', lang)}", f"✨ {t('sign_up_tab', lang)}"])

        with auth_tab1:
            render_html(f"""
            <div style="margin: 0.8rem 0 1rem 0; font-size: 1.15rem; font-weight: 700; color: #242424;">
                {t('sign_in_title', lang)}
            </div>
            """)

            with st.form("form_signin", clear_on_submit=False):
                signin_username = st.text_input(
                    f"👤 {t('username', lang)}",
                    key="input_signin_user",
                    placeholder="e.g. chef_kavitha"
                )
                signin_password = st.text_input(
                    f"🔒 {t('password', lang)}",
                    type="password",
                    key="input_signin_pass",
                    placeholder="••••••••"
                )
                st.write("")
                submit_signin = st.form_submit_button(
                    f"🔑 {t('sign_in_tab', lang)}",
                    type="primary",
                    use_container_width=True
                )

            if submit_signin:
                if not signin_username or not signin_password:
                    st.error(t('all_fields_required', lang))
                else:
                    success, user_data, msg = login_user(signin_username, signin_password)
                    if success and user_data:
                        st.session_state["user"] = user_data
                        st.session_state["active_nav"] = "finder"
                        st.toast(f"{t('login_success', lang)} {user_data.get('full_name', '')}!", icon="👋")
                        st.rerun()
                    else:
                        st.error(msg)

            st.write("")
            render_html("<div style='text-align: center; color: #888888; font-size: 0.85rem; margin: 0.5rem 0;'>─── OR ───</div>")
            if st.button(f"👤 {t('guest_continue_btn', lang)}", key="btn_signin_continue_guest", use_container_width=True):
                st.session_state["user"] = {"username": "guest", "full_name": "Guest Chef"}
                st.session_state["active_nav"] = "finder"
                st.rerun()

        with auth_tab2:
            render_html(f"""
            <div style="margin: 0.8rem 0 1rem 0; font-size: 1.15rem; font-weight: 700; color: #242424;">
                {t('sign_up_title', lang)}
            </div>
            """)

            with st.form("form_signup", clear_on_submit=False):
                signup_fullname = st.text_input(
                    f"📛 {t('full_name', lang)}",
                    key="input_signup_fullname",
                    placeholder="e.g. Kavitha Raman"
                )
                signup_username = st.text_input(
                    f"👤 {t('username', lang)}",
                    key="input_signup_user",
                    placeholder="e.g. chef_kavitha"
                )
                signup_password = st.text_input(
                    f"🔒 {t('password', lang)}",
                    type="password",
                    key="input_signup_pass",
                    placeholder="••••••••"
                )
                signup_confirm = st.text_input(
                    f"🔒 {t('confirm_password', lang)}",
                    type="password",
                    key="input_signup_confirm",
                    placeholder="••••••••"
                )
                st.write("")
                submit_signup = st.form_submit_button(
                    f"✨ {t('sign_up_tab', lang)}",
                    type="primary",
                    use_container_width=True
                )

            if submit_signup:
                if not signup_fullname or not signup_username or not signup_password or not signup_confirm:
                    st.error(t('all_fields_required', lang))
                elif len(signup_username.strip()) < 3:
                    st.error(t('username_too_short', lang))
                elif len(signup_password) < 4:
                    st.error(t('password_too_short', lang))
                elif signup_password != signup_confirm:
                    st.error(t('passwords_dont_match', lang))
                else:
                    reg_ok, reg_msg = register_user(signup_username, signup_password, signup_fullname)
                    if reg_ok:
                        login_ok, user_data, _ = login_user(signup_username, signup_password)
                        if login_ok and user_data:
                            st.session_state["user"] = user_data
                            st.session_state["active_nav"] = "finder"
                            st.toast(t('signup_success', lang), icon="🎉")
                            st.rerun()
                        else:
                            st.success(t('signup_success', lang))
                    else:
                        st.error(reg_msg)

            st.write("")
            render_html("<div style='text-align: center; color: #888888; font-size: 0.85rem; margin: 0.5rem 0;'>─── OR ───</div>")
            if st.button(f"👤 {t('guest_continue_btn', lang)}", key="btn_signup_continue_guest", use_container_width=True):
                st.session_state["user"] = {"username": "guest", "full_name": "Guest Chef"}
                st.session_state["active_nav"] = "finder"
                st.rerun()


# ==============================================================================
# MAIN ROUTING CONTROLLER
# ==============================================================================
def main():
    """Main application router."""
    init_session_state()
    render_top_app_bar()

    active_page = st.session_state["active_nav"]

    if active_page == "finder":
        render_recipe_finder_page()
    elif active_page == "results":
        render_search_results_page()
    elif active_page == "detail":
        render_recipe_detail_page()
    elif active_page == "saved":
        render_saved_recipes_page()
    elif active_page == "history":
        render_history_page()
    elif active_page == "profile":
        render_profile_page()
    elif active_page == "auth":
        render_auth_page()


if __name__ == "__main__":
    main()
