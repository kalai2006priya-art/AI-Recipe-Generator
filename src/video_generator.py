"""
video_generator.py
------------------
Engine for generating high-definition MP4 cooking video reels (720x720)
for recipes using PIL (Pillow) and OpenCV.

Features:
- Animated title hero slide with duration & difficulty badges.
- Ingredient breakdown slide with bulleted items.
- Step-by-step cooking slides with real-time progress meters.
- Completion outro slide.
- Native bilingual typography support (English & Tamil via Nirmala font).
"""

import os
import re
import tempfile
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from src.video_reel_widget import extract_cooking_steps


def _get_font(font_size: int, is_tamil: bool = False, bold: bool = False):
    """Loads appropriate system font with fallback."""
    if is_tamil:
        try:
            return ImageFont.truetype("Nirmala.ttc", font_size)
        except Exception:
            try:
                return ImageFont.truetype("ARIALUNI.TTF", font_size)
            except Exception:
                pass
    
    font_name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(font_name, font_size)
    except Exception:
        try:
            return ImageFont.truetype("segoeui.ttf", font_size)
        except Exception:
            return ImageFont.load_default()


def _wrap_text(text: str, max_chars_per_line: int = 34) -> List[str]:
    """Wraps text cleanly across multiple lines."""
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    
    for word in words:
        if current_len + len(word) + 1 <= max_chars_per_line:
            current_line.append(word)
            current_len += len(word) + 1
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_len = len(word)
            
    if current_line:
        lines.append(" ".join(current_line))
        
    return lines[:6]


def generate_recipe_mp4_video(
    recipe: Dict,
    lang: str = "en",
    output_path: Optional[str] = None
) -> Tuple[str, bytes]:
    """
    Renders and compiles a 720x720 MP4 cooking video reel for the given recipe.
    Returns (output_file_path, video_bytes).
    """
    is_ta = (lang == "ta")
    width, height = 720, 720
    fps = 20

    # Extract metadata
    dish_name = recipe.get("name_ta" if is_ta else "name_en", "Special Dish")
    time_mins = recipe.get("time_mins", 20)
    diff = recipe.get("difficulty", "Easy")
    diet = recipe.get("diet", "Vegetarian")
    is_veg = (diet == "Vegetarian")

    # Extract ingredients
    if is_ta:
        raw_ings = recipe.get("ingredients_ta", recipe.get("ingredients_en", ""))
    else:
        raw_ings = recipe.get("ingredients_en", "")
    
    ing_items = []
    for line in raw_ings.splitlines():
        cleaned = line.strip("- *•").strip()
        if cleaned:
            ing_items.append(cleaned)
    if not ing_items:
        ing_items = recipe.get("matched_ingredients", ["Fresh ingredients"])

    # Extract steps
    steps = extract_cooking_steps(recipe, lang)
    if not steps:
        steps = ["Prepare ingredients and cook over medium flame until fragrant." if not is_ta else "மிதமான தீயில் வாசனை வரும் வரை சமைக்கவும்."]

    # Temp file setup
    if not output_path:
        out_dir = os.path.join(tempfile.gettempdir(), "samayal_videos")
        os.makedirs(out_dir, exist_ok=True)
        safe_id = re.sub(r'[^a-zA-Z0-9_]', '', str(recipe.get("id", "dish")))
        output_path = os.path.join(out_dir, f"reel_{safe_id}_{lang}.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Fonts
    font_brand = _get_font(22, is_tamil=False, bold=True)
    font_title = _get_font(34, is_tamil=is_ta, bold=True)
    font_sub = _get_font(22, is_tamil=is_ta)
    font_body = _get_font(24, is_tamil=is_ta)
    font_badge = _get_font(18, is_tamil=is_ta, bold=True)

    # Theme colors (RGB)
    c_bg = (10, 14, 23)
    c_card = (17, 24, 38)
    c_amber = (245, 158, 11)
    c_orange = (255, 107, 0)
    c_green = (16, 185, 129)
    c_red = (239, 68, 68)
    c_white = (255, 255, 255)
    c_gray = (148, 163, 184)

    diet_color = c_green if is_veg else c_red
    diet_label = "VEGETARIAN" if is_veg else "NON-VEG"
    if is_ta:
        diet_label = "சைவம்" if is_veg else "அசைவம்"

    total_scenes = 2 + len(steps) + 1

    def render_base_canvas(scene_index: int, total_s: int):
        img = Image.new("RGB", (width, height), color=c_bg)
        d = ImageDraw.Draw(img)
        
        # Outer Card Container
        d.rounded_rectangle([25, 25, width - 25, height - 25], radius=24, fill=c_card, outline=(40, 50, 75), width=2)
        
        # Top App Badge
        d.rounded_rectangle([50, 50, 240, 88], radius=10, fill=(30, 41, 59))
        d.text((65, 58), "SAMAYAL AI", font=font_brand, fill=c_amber)
        
        # Diet Badge
        d.rounded_rectangle([width - 210, 50, width - 50, 88], radius=10, fill=(diet_color[0]//5, diet_color[1]//5, diet_color[2]//5), outline=diet_color, width=1)
        d.text((width - 195, 59), diet_label, font=font_badge, fill=diet_color)
        
        # Top Story Progress Bars
        bar_gap = 6
        avail_w = width - 100
        bar_w = (avail_w - (total_s - 1) * bar_gap) / total_s
        for idx in range(total_s):
            bx1 = 50 + idx * (bar_w + bar_gap)
            bx2 = bx1 + bar_w
            b_color = c_amber if idx <= scene_index else (51, 65, 85)
            d.rounded_rectangle([bx1, 105, bx2, 110], radius=3, fill=b_color)
            
        return img, d

    # SCENE 1: TITLE & HERO COVER
    img1, d1 = render_base_canvas(0, total_scenes)
    d1.rounded_rectangle([50, 160, 170, 280], radius=18, fill=(35, 45, 68), outline=c_amber, width=2)
    d1.text((70, 185), "COOK", font=_get_font(28, bold=True), fill=c_amber)
    d1.text((75, 225), "REEL", font=_get_font(20), fill=c_gray)
    
    title_lines = _wrap_text(dish_name, max_chars_per_line=24)
    y_text = 170
    for t_line in title_lines:
        d1.text((195, y_text), t_line, font=font_title, fill=c_white)
        y_text += 45

    d1.rounded_rectangle([50, 360, width - 50, 460], radius=16, fill=(24, 34, 53))
    time_label = f"TIME: {time_mins} MINS" if not is_ta else f"நேரம்: {time_mins} நிமிடம்"
    diff_label = f"DIFFICULTY: {diff}" if not is_ta else f"சிரமம்: {diff}"
    style_label = "TAMIL NADU AUTHENTIC" if not is_ta else "பாரம்பரிய சுவை"
    
    d1.text((80, 385), time_label, font=font_body, fill=c_amber)
    d1.text((80, 420), diff_label, font=font_sub, fill=c_gray)
    d1.text((400, 385), style_label, font=font_body, fill=c_white)
    
    d1.rounded_rectangle([50, 560, width - 50, 640], radius=16, fill=c_orange)
    cta_label = "STARTING COOKING TUTORIAL..." if not is_ta else "சமையல் தொடங்குகிறது..."
    d1.text((130, 585), cta_label, font=font_brand, fill=c_white)
    
    frame1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
    for _ in range(50):
        out.write(frame1)

    # SCENE 2: INGREDIENTS LIST
    img2, d2 = render_base_canvas(1, total_scenes)
    ing_title = "KEY INGREDIENTS" if not is_ta else "தேவையான பொருட்கள்"
    d2.text((50, 150), ing_title, font=font_title, fill=c_amber)
    
    y_ing = 220
    for idx, item in enumerate(ing_items[:6]):
        d2.rounded_rectangle([50, y_ing, width - 50, y_ing + 55], radius=12, fill=(24, 34, 53))
        d2.text((75, y_ing + 14), "✓", font=font_body, fill=c_green)
        d2.text((115, y_ing + 14), item[:38], font=font_body, fill=c_white)
        y_ing += 70

    pantry_note = "+ Basic Pantry Spices & Oil" if not is_ta else "+ அடிப்படை அஞ்சறைப்பெட்டி பொருட்கள்"
    d2.text((55, 650), pantry_note, font=font_sub, fill=c_gray)
    
    frame2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
    for _ in range(60):
        out.write(frame2)

    # SCENE 3 to N: COOKING STEPS
    for s_idx, step_text in enumerate(steps):
        img_s, d_s = render_base_canvas(2 + s_idx, total_scenes)
        
        step_header = f"STEP {s_idx + 1} OF {len(steps)}" if not is_ta else f"படி {s_idx + 1} -ல் {len(steps)}"
        d_s.rounded_rectangle([50, 150, 320, 205], radius=14, fill=(245, 158, 11, 40), outline=c_amber, width=2)
        d_s.text((75, 162), step_header, font=font_brand, fill=c_amber)
        
        d_s.rounded_rectangle([50, 240, width - 50, 570], radius=18, fill=(22, 30, 48), outline=(45, 55, 80), width=1)
        
        step_lines = _wrap_text(step_text, max_chars_per_line=30)
        y_step = 280
        for s_line in step_lines:
            d_s.text((80, y_step), s_line, font=font_title if len(step_lines) <= 3 else font_body, fill=c_white)
            y_step += 48

        tip_text = "Cook gently over medium flame" if not is_ta else "மிதமான தீயில் சமைக்கவும்"
        d_s.text((80, 520), f"💡 {tip_text}", font=font_sub, fill=c_gray)
        
        pct = (s_idx + 1) / len(steps)
        d_s.rounded_rectangle([50, 630, width - 50, 642], radius=6, fill=(30, 41, 59))
        d_s.rounded_rectangle([50, 630, 50 + int((width - 100) * pct), 642], radius=6, fill=c_green)
        
        frame_s = cv2.cvtColor(np.array(img_s), cv2.COLOR_RGB2BGR)
        for _ in range(70):
            out.write(frame_s)

    # SCENE FINAL: OUTRO
    img_out, d_out = render_base_canvas(total_scenes - 1, total_scenes)
    d_out.rounded_rectangle([80, 200, width - 80, 480], radius=22, fill=(24, 34, 53), outline=c_green, width=2)
    
    ready_title = "RECIPE READY!" if not is_ta else "உணவு தயாரானது!"
    d_out.text((220, 240), ready_title, font=_get_font(38, is_tamil=is_ta, bold=True), fill=c_green)
    
    ready_desc1 = "Garnish and serve hot." if not is_ta else "சூடாக பரிமாறி மகிழுங்கள்."
    ready_desc2 = "Enjoy authentic Tamil Nadu cuisine!" if not is_ta else "பாரம்பரிய தமிழக சுவையில் சுவைத்து மகிழுங்கள்!"
    d_out.text((160, 320), ready_desc1, font=font_title, fill=c_white)
    d_out.text((120, 390), ready_desc2, font=font_sub, fill=c_gray)
    
    d_out.text((210, 610), "MADE WITH SAMAYAL AI", font=font_brand, fill=c_amber)
    
    frame_out = cv2.cvtColor(np.array(img_out), cv2.COLOR_RGB2BGR)
    for _ in range(50):
        out.write(frame_out)

    out.release()

    with open(output_path, "rb") as f:
        video_bytes = f.read()

    return output_path, video_bytes
