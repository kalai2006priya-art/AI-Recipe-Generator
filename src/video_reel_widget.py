"""
video_reel_widget.py
--------------------
Interactive HTML5 / CSS3 / Web Audio Video Reel Player.
Runs directly in the browser like an Instagram Reel / YouTube Short
with animated transitions, top story progress bars, and synchronized
audio voice narration in English or Tamil.
"""

import json
import re
import streamlit.components.v1 as components
from typing import Dict, List


def extract_cooking_steps(recipe: Dict, lang: str = "en") -> List[str]:
    """
    Robustly extracts individual cooking steps from recipe instructions or steps list.
    Handles:
    - Pre-split list in steps_list_ta / steps_list_en / steps_ta / steps
    - Numbered lines: '1. ...', '2) ...', 'Step 1: ...', 'படி 1: ...'
    - Single newlines '\n' or double newlines '\n\n'
    - Strips leading numbering and whitespace
    """
    is_ta = (lang == "ta")
    raw_list = recipe.get("steps_list_ta" if is_ta else "steps_list_en") or \
               recipe.get("steps_ta" if is_ta else "steps") or []

    if isinstance(raw_list, list) and len(raw_list) > 1:
        steps = [re.sub(r'^(?:(?:Step|படி)\s*\d+[:\.\)]\s*|\d+[\.\)]\s*)', '', str(s)).strip() for s in raw_list if str(s).strip()]
        cleaned = [s for s in steps if s]
        if cleaned:
            return cleaned

    # Look up raw instruction string
    inst_str = recipe.get("instructions_ta" if is_ta else "instructions_en") or \
               recipe.get("instructions", "") or ""

    if not inst_str.strip():
        inst_str = recipe.get("instructions_en" if is_ta else "instructions_ta") or ""

    if not inst_str.strip():
        return [
            "Prepare fresh ingredients." if not is_ta else "தேவையான பொருட்களை தயாராக வைக்கவும்.",
            "Cook over medium flame until fragrant." if not is_ta else "மிதமான தீயில் நறுமணம் வரும் வரை சமைக்கவும்.",
            "Garnish and serve hot." if not is_ta else "கொத்தமல்லி தூவி சூடாக பரிமாறவும்."
        ]

    # Split by lines first
    lines = [line.strip() for line in inst_str.splitlines() if line.strip()]
    cleaned_steps = []
    for line in lines:
        cleaned = re.sub(r'^(?:(?:Step|படி)\s*\d+[:\.\)]\s*|\d+[\.\)]\s*)', '', line).strip()
        if cleaned:
            cleaned_steps.append(cleaned)

    if len(cleaned_steps) > 1:
        return cleaned_steps

    # If it was a single paragraph, split by sentences
    if len(cleaned_steps) == 1:
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', cleaned_steps[0]) if len(s.strip()) > 8]
        if len(sentences) > 1:
            return sentences
        return cleaned_steps

    return ["Cook over medium flame until fragrant." if not is_ta else "மிதமான தீயில் வாசனை வரும் வரை சமைக்கவும்."]


def render_interactive_video_reel(recipe: Dict, lang: str = "en", height: int = 560):
    """
    Renders an in-browser interactive cooking video reel with synchronized speech synthesis.
    """
    is_ta = (lang == "ta")
    speech_lang = "ta-IN" if is_ta else "en-IN"
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

    # Extract individual cooking steps
    steps = extract_cooking_steps(recipe, lang)
    if not steps:
        steps = ["Prepare ingredients and cook over medium flame until fragrant." if not is_ta else "மிதமான தீயில் வாசனை வரும் வரை சமைக்கவும்."]

    # Step action icons
    action_icons = ["🔪", "🍳", "🍲", "🧂", "🔥", "🍽️"]

    # Build slides array
    slides = [
        {
            "type": "cover",
            "title": dish_name,
            "badge": "🟢 " + diet if is_veg else "🔴 " + diet,
            "meta": f"⏱️ {time_mins} mins • ⚡ {diff}" if not is_ta else f"⏱️ {time_mins} நிமிடம் • ⚡ {diff}",
            "speech": f"Cooking Reel for {dish_name}. Ready in {time_mins} minutes." if not is_ta else f"{dish_name} செய்முறை ரீல். சமைக்கும் நேரம் {time_mins} நிமிடம்."
        },
        {
            "type": "ingredients",
            "title": "Ingredients" if not is_ta else "தேவையான பொருட்கள்",
            "items": ing_items[:6],
            "speech": "Here are the key ingredients needed." if not is_ta else "இவை தேவையான முக்கிய பொருட்கள்."
        }
    ]

    for idx, s in enumerate(steps):
        icon = action_icons[idx % len(action_icons)]
        step_title = f"STEP {idx + 1} OF {len(steps)}" if not is_ta else f"படி {idx + 1} / {len(steps)}"
        slides.append({
            "type": "step",
            "step_num": idx + 1,
            "total_steps": len(steps),
            "icon": icon,
            "badge": step_title,
            "text": s,
            "speech": f"Step {idx + 1}. {s}" if not is_ta else f"படி {idx + 1}. {s}"
        })

    slides.append({
        "type": "outro",
        "title": "Dish is Ready!" if not is_ta else "உணவு தயாரானது!",
        "desc": "Serve piping hot and enjoy authentic flavors." if not is_ta else "சூடாக பரிமாறி சுவைத்து மகிழுங்கள்!",
        "speech": "Cooking complete! Serve hot and enjoy your delicious meal." if not is_ta else "சமையல் முடிந்தது! சூடாக பரிமாறி சுவைத்து மகிழுங்கள்."
    })

    slides_json = json.dumps(slides)

    reel_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            user-select: none;
        }}
        body {{
            background: #090D16;
            color: #F8FAFC;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }}
        .reel-player {{
            width: 100%;
            max-width: 480px;
            height: 520px;
            background: linear-gradient(145deg, #111827 0%, #0F172A 100%);
            border: 2px solid rgba(245, 158, 11, 0.4);
            border-radius: 24px;
            box-shadow: 0 12px 40px rgba(0,0,0,0.6);
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}
        /* Top Story Bars */
        .story-bars {{
            display: flex;
            gap: 4px;
            padding: 12px 16px 8px 16px;
            z-index: 10;
        }}
        .story-bar {{
            flex: 1;
            height: 4px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 2px;
            overflow: hidden;
        }}
        .story-fill {{
            width: 0%;
            height: 100%;
            background: #F59E0B;
            transition: width 0.1s linear;
        }}
        /* Top Info Row */
        .reel-top-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 16px 8px 16px;
            font-size: 0.8rem;
            color: #94A3B8;
            z-index: 10;
        }}
        .brand-pill {{
            background: rgba(245, 158, 11, 0.15);
            color: #F59E0B;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 700;
        }}
        /* Slide Content Area */
        .slide-content {{
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 24px;
            text-align: center;
            transition: opacity 0.25s ease, transform 0.25s ease;
        }}
        .cover-icon {{
            font-size: 3.5rem;
            margin-bottom: 12px;
            filter: drop-shadow(0 4px 12px rgba(245, 158, 11, 0.4));
        }}
        .cover-title {{
            font-size: 1.45rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 8px;
            line-height: 1.3;
        }}
        .cover-badge {{
            display: inline-block;
            background: rgba(16, 185, 129, 0.2);
            color: #6EE7B7;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .cover-meta {{
            font-size: 0.95rem;
            color: #94A3B8;
        }}
        /* Ingredients list in reel */
        .ings-list {{
            width: 100%;
            text-align: left;
            margin-top: 10px;
        }}
        .ing-row {{
            background: rgba(30, 41, 59, 0.7);
            padding: 8px 12px;
            border-radius: 8px;
            margin-bottom: 6px;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        /* Step slide */
        .step-pill {{
            background: #FF6B00;
            color: #FFF;
            padding: 4px 14px;
            border-radius: 9999px;
            font-weight: 800;
            font-size: 0.82rem;
            letter-spacing: 0.05em;
            margin-bottom: 16px;
        }}
        .step-instruction {{
            font-size: 1.25rem;
            font-weight: 600;
            line-height: 1.5;
            color: #F8FAFC;
        }}
        /* Outro */
        .outro-icon {{
            font-size: 3.8rem;
            margin-bottom: 12px;
        }}
        /* Controls Bottom Bar */
        .reel-controls {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 12px 16px;
            background: rgba(15, 23, 42, 0.9);
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            z-index: 10;
        }}
        .ctrl-btn {{
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: #FFF;
            padding: 8px 16px;
            border-radius: 10px;
            font-size: 0.85rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .ctrl-btn:hover {{
            background: #F59E0B;
            color: #000;
        }}
        .voice-indicator {{
            font-size: 0.78rem;
            color: #10B981;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
    </style>
    </head>
    <body>
    <div class="reel-player" id="player">
        <div class="story-bars" id="storyBars"></div>
        <div class="reel-top-info">
            <span class="brand-pill">🍲 SAMAYAL AI REEL</span>
            <span class="voice-indicator" id="voiceIndicator">🔊 Voice Narration ON</span>
        </div>
        <div class="slide-content" id="slideArea"></div>
        <div class="reel-controls">
            <button class="ctrl-btn" onclick="prevSlide()">⏮ Prev</button>
            <button class="ctrl-btn" id="playBtn" onclick="togglePlay()">⏸ Pause</button>
            <button class="ctrl-btn" onclick="nextSlide()">Next ⏭</button>
            <button class="ctrl-btn" id="voiceBtn" onclick="toggleVoice()">🔊 Audio</button>
        </div>
    </div>

    <script>
    const slides = {slides_json};
    const speechLang = "{speech_lang}";
    let currentIdx = 0;
    let isPlaying = true;
    let isVoiceActive = true;
    let slideTimer = null;
    let progressTimer = null;
    let progressVal = 0;
    const slideDuration = 4500; // 4.5s per slide

    // Initialize story bars
    const storyBars = document.getElementById('storyBars');
    slides.forEach((_, idx) => {{
        const bar = document.createElement('div');
        bar.className = 'story-bar';
        bar.innerHTML = '<div class="story-fill" id="fill-' + idx + '"></div>';
        storyBars.appendChild(bar);
    }});

    function speakText(text) {{
        if (!isVoiceActive || !('speechSynthesis' in window)) return;
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = speechLang;
        utter.rate = 1.0;
        window.speechSynthesis.speak(utter);
    }}

    function renderSlide(idx) {{
        currentIdx = idx;
        const slide = slides[idx];
        const area = document.getElementById('slideArea');
        area.style.opacity = '0';
        area.style.transform = 'translateY(8px)';

        setTimeout(() => {{
            if (slide.type === 'cover') {{
                area.innerHTML = `
                    <div class="cover-icon">🍲</div>
                    <div class="cover-title">${{slide.title}}</div>
                    <div class="cover-badge">${{slide.badge}}</div>
                    <div class="cover-meta">${{slide.meta}}</div>
                `;
            }} else if (slide.type === 'ingredients') {{
                const itemsHtml = slide.items.map(i => `<div class="ing-row"><span>✓</span> <span>${{i}}</span></div>`).join('');
                area.innerHTML = `
                    <div style="font-size:1.3rem; font-weight:800; color:#F59E0B; margin-bottom:12px;">🛒 ${{slide.title}}</div>
                    <div class="ings-list">${{itemsHtml}}</div>
                `;
            }} else if (slide.type === 'step') {{
                area.innerHTML = `
                    <div style="font-size:2.8rem; margin-bottom:12px; filter: drop-shadow(0 4px 10px rgba(245, 158, 11, 0.4));">${{slide.icon || '👨‍🍳'}}</div>
                    <div class="step-pill">${{slide.badge || ('STEP ' + slide.step_num + ' OF ' + slide.total_steps)}}</div>
                    <div class="step-instruction">${{slide.text}}</div>
                `;
            }} else if (slide.type === 'outro') {{
                area.innerHTML = `
                    <div class="outro-icon">🎉</div>
                    <div style="font-size:1.5rem; font-weight:800; color:#10B981; margin-bottom:8px;">${{slide.title}}</div>
                    <div style="color:#94A3B8; font-size:1.05rem;">${{slide.desc}}</div>
                `;
            }}
            area.style.opacity = '1';
            area.style.transform = 'translateY(0)';
            if (slide.speech) speakText(slide.speech);
        }}, 150);

        // Update story bars
        for (let i = 0; i < slides.length; i++) {{
            const fill = document.getElementById('fill-' + i);
            if (i < idx) fill.style.width = '100%';
            else if (i > idx) fill.style.width = '0%';
        }}

        startProgress();
    }}

    function getSlideDuration(idx) {{
        const s = slides[idx];
        if (!s) return 5000;
        if (s.type === 'cover') return 4500;
        if (s.type === 'ingredients') return 5500;
        if (s.type === 'outro') return 5000;
        const textLen = s.speech ? s.speech.length : (s.text ? s.text.length : 40);
        return Math.max(6000, textLen * 95 + 2000);
    }}

    function startProgress() {{
        clearInterval(progressTimer);
        clearTimeout(slideTimer);
        progressVal = 0;
        const fill = document.getElementById('fill-' + currentIdx);
        if (!isPlaying) return;

        const currentDuration = getSlideDuration(currentIdx);
        const interval = 50;
        const step = (interval / currentDuration) * 100;

        progressTimer = setInterval(() => {{
            if (!isPlaying) return;
            progressVal += step;
            if (fill) fill.style.width = Math.min(progressVal, 100) + '%';
            if (progressVal >= 100) {{
                clearInterval(progressTimer);
                if (currentIdx < slides.length - 1) {{
                    renderSlide(currentIdx + 1);
                }} else {{
                    togglePlay(); // Finish reel
                }}
            }}
        }}, interval);
    }}

    function togglePlay() {{
        isPlaying = !isPlaying;
        const btn = document.getElementById('playBtn');
        btn.innerText = isPlaying ? '⏸ Pause' : '▶ Play';
        if (isPlaying) {{
            startProgress();
        }} else {{
            clearInterval(progressTimer);
            if ('speechSynthesis' in window) window.speechSynthesis.pause();
        }}
    }}

    function prevSlide() {{
        if (currentIdx > 0) renderSlide(currentIdx - 1);
    }}

    function nextSlide() {{
        if (currentIdx < slides.length - 1) renderSlide(currentIdx + 1);
    }}

    function toggleVoice() {{
        isVoiceActive = !isVoiceActive;
        const vBtn = document.getElementById('voiceBtn');
        const vInd = document.getElementById('voiceIndicator');
        if (isVoiceActive) {{
            vBtn.innerText = '🔊 Audio';
            vInd.innerText = '🔊 Voice Narration ON';
            vInd.style.color = '#10B981';
            if (slides[currentIdx].speech) speakText(slides[currentIdx].speech);
        }} else {{
            vBtn.innerText = '🔇 Muted';
            vInd.innerText = '🔇 Voice Muted';
            vInd.style.color = '#94A3B8';
            if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        }}
    }}

    // Tap on left/right half to navigate
    document.getElementById('slideArea').addEventListener('click', (e) => {{
        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left;
        if (x < rect.width / 2) prevSlide();
        else nextSlide();
    }});

    // Start on load
    window.onload = () => {{
        renderSlide(0);
    }};
    </script>
    </body>
    </html>
    """
    components.html(reel_html, height=height)
