"""
voice_service.py
----------------
Handles live Web Speech API Voice Input (Speech-to-Text) and Text-to-Speech audio
with 100% strict language isolation (zero Tamil in English mode, zero English in Tamil mode).
"""

import io
import re
import streamlit.components.v1 as components
from gtts import gTTS


def render_voice_input_button(lang: str = "en"):
    """
    Renders an interactive Web Speech API microphone widget strictly matching the selected language.
    Live speech updates the Streamlit ingredient input field in real time.
    """
    is_ta = (lang == "ta")
    speech_lang = "ta-IN" if is_ta else "en-IN"
    btn_idle_label = "🎤 குரல் உள்ளீடு" if is_ta else "🎤 Voice Input"
    btn_active_label = "🔴 கேட்டுக்கொண்டிருக்கிறேன்..." if is_ta else "🔴 Listening..."
    btn_stop_label = "⏹ நிறுத்து" if is_ta else "⏹ Stop"
    status_listen = "கேட்டுக்கொண்டிருக்கிறேன்... பேசுங்கள்" if is_ta else "Listening... speak now"
    unsupported_msg = "இந்த உலாவியில் குரல் அறிதல் ஆதரிக்கப்படவில்லை." if is_ta else "Speech recognition not supported in this browser. Please use Chrome or Edge."
    denied_msg = "மைக்ரோஃபோன் அனுமதி மறுக்கப்பட்டது." if is_ta else "Microphone access denied. Please allow microphone in browser settings."

    html_code = f"""
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
        }}
        body {{
            background: transparent;
            overflow: hidden;
        }}
        .voice-bar {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 2px 0 6px 0;
        }}
        .voice-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 18px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid #E5E7EB;
            background: #FFFFFF;
            color: #242424;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            outline: none;
            user-select: none;
        }}
        .voice-btn:hover {{
            background: #FFF5EE;
            border-color: #FF6B35;
            color: #FF6B35;
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(255, 107, 53, 0.15);
        }}
        .voice-btn.active {{
            background: linear-gradient(135deg, #FF6B35 0%, #E85924 100%) !important;
            color: #FFFFFF !important;
            border-color: #FF6B35 !important;
            animation: pulse-ring 1.5s infinite;
        }}
        @keyframes pulse-ring {{
            0% {{ box-shadow: 0 0 0 0 rgba(255, 107, 53, 0.6); }}
            70% {{ box-shadow: 0 0 0 8px rgba(255, 107, 53, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(255, 107, 53, 0); }}
        }}
        .stop-btn {{
            display: none;
            padding: 8px 14px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
            background: #F3F4F6;
            color: #4B5563;
            border: 1px solid #D1D5DB;
            cursor: pointer;
        }}
        .stop-btn:hover {{
            background: #E5E7EB;
            color: #111827;
        }}
        .live-preview {{
            font-size: 12px;
            color: #FF6B35;
            font-weight: 600;
        }}
            font-style: italic;
            max-width: 250px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .err-msg {{
            font-size: 12px;
            color: #F87171;
            font-weight: 500;
        }}
    </style>
    </head>
    <body>
    <div class="voice-bar">
        <button id="micBtn" class="voice-btn" onclick="toggleListening()">
            <span id="btnIcon">🎤</span> <span id="btnText">{btn_idle_label}</span>
        </button>
        <button id="stopBtn" class="stop-btn" onclick="stopListening()">
            {btn_stop_label}
        </button>
        <span id="livePreview" class="live-preview"></span>
        <span id="errTxt" class="err-msg" style="display: none;"></span>
    </div>

    <script>
    let recognition = null;
    let isListening = false;
    const speechLang = "{speech_lang}";

    function findStreamlitInput() {{
        try {{
            const pdoc = window.parent.document;
            return pdoc.querySelector('input[data-testid="stTextInputRootElement"] input') ||
                   pdoc.querySelector('input[aria-label="Input"]') ||
                   pdoc.querySelector('div[data-testid="stTextInput"] input') ||
                   pdoc.querySelector('input[type="text"]');
        }} catch (e) {{
            return null;
        }}
    }}

    function updateReactInput(element, newText) {{
        if (!element) return;
        element.focus();
        const lastValue = element.value;
        element.value = newText;
        const tracker = element._valueTracker;
        if (tracker) {{
            tracker.setValue(lastValue);
        }}
        element.dispatchEvent(new Event('input', {{ bubbles: true }}));
        element.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }}

    function toggleListening() {{
        if (isListening) {{
            stopListening();
        }} else {{
            startListening();
        }}
    }}

    function startListening() {{
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const micBtn = document.getElementById('micBtn');
        const stopBtn = document.getElementById('stopBtn');
        const btnText = document.getElementById('btnText');
        const livePreview = document.getElementById('livePreview');
        const errTxt = document.getElementById('errTxt');

        if (!SpeechRecognition) {{
            errTxt.style.display = 'inline';
            errTxt.innerText = "{unsupported_msg}";
            return;
        }}

        try {{
            recognition = new SpeechRecognition();
            recognition.lang = speechLang;
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.maxAlternatives = 1;

            recognition.onstart = function() {{
                isListening = true;
                micBtn.classList.add('active');
                btnText.innerText = "{btn_active_label}";
                stopBtn.style.display = 'inline-flex';
                errTxt.style.display = 'none';
            }};

            recognition.onresult = function(event) {{
                let finalTranscript = '';
                let interimTranscript = '';

                for (let i = event.resultIndex; i < event.results.length; ++i) {{
                    if (event.results[i].isFinal) {{
                        finalTranscript += event.results[i][0].transcript;
                    }} else {{
                        interimTranscript += event.results[i][0].transcript;
                    }}
                }}

                if (interimTranscript) {{
                    livePreview.innerText = `"${{interimTranscript}}"`;
                }}

                if (finalTranscript) {{
                    livePreview.innerText = '';
                    const inputEl = findStreamlitInput();
                    if (inputEl) {{
                        let currentVal = inputEl.value.trim();
                        let cleanFinal = finalTranscript.trim();
                        cleanFinal = cleanFinal.charAt(0).toUpperCase() + cleanFinal.slice(1);

                        let updatedVal = '';
                        if (currentVal) {{
                            if (currentVal.endsWith(',')) {{
                                updatedVal = `${{currentVal}} ${{cleanFinal}}`;
                            }} else {{
                                updatedVal = `${{currentVal}}, ${{cleanFinal}}`;
                            }}
                        }} else {{
                            updatedVal = cleanFinal;
                        }}
                        updateReactInput(inputEl, updatedVal);
                    }}
                }}
            }};

            recognition.onerror = function(event) {{
                errTxt.style.display = 'inline';
                if (event.error === 'not-allowed') {{
                    errTxt.innerText = "{denied_msg}";
                }} else {{
                    errTxt.innerText = "Mic: " + event.error;
                }}
                stopListening();
            }};

            recognition.onend = function() {{
                stopListening();
            }};

            recognition.start();

        }} catch (err) {{
            errTxt.style.display = 'inline';
            errTxt.innerText = err.message;
            stopListening();
        }}
    }}

    function stopListening() {{
        isListening = false;
        if (recognition) {{
            try {{ recognition.stop(); }} catch(e) {{}}
            recognition = null;
        }}

        const micBtn = document.getElementById('micBtn');
        const stopBtn = document.getElementById('stopBtn');
        const btnText = document.getElementById('btnText');
        const livePreview = document.getElementById('livePreview');

        if (micBtn) micBtn.classList.remove('active');
        if (stopBtn) stopBtn.style.display = 'none';
        if (btnText) btnText.innerText = "{btn_idle_label}";
        if (livePreview) livePreview.innerText = '';
    }}
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=48)
    return html_code


def generate_recipe_audio(text: str, lang: str = "en") -> io.BytesIO:
    """
    Converts recipe text to an MP3 audio buffer using gTTS.
    Cleans markdown formatting symbols before speaking.
    """
    clean_text = re.sub(r"[#\*\_\-\`]", " ", text)
    clean_text = " ".join(clean_text.split()).strip()

    if len(clean_text) > 800:
        clean_text = clean_text[:800] + "..."

    target_lang = "ta" if lang == "ta" else "en"

    tts = gTTS(text=clean_text, lang=target_lang, slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp