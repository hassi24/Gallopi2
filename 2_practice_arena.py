import streamlit as st
import time
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Practice Arena · Gallopi", page_icon="🎙️",
                   layout="centered", initial_sidebar_state="collapsed")

# ─────────────────────────────────────────────
# SESSION DEFAULTS
# ─────────────────────────────────────────────
defaults = {
    "nickname": "Learner", "avatar": "🐴", "streak": 7, "xp": 1240,
    "gems": 85, "energy": 4, "completed_levels": [1, 2, 3],
    "current_level": 4, "target_level": 4,
    "last_score": None, "last_feedback": None, "show_results": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
# GLOBAL CSS (shared design system)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0b141a !important;
    font-family: 'Nunito', sans-serif !important;
    color: #e8f4f8;
}
#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
[data-testid="stAppViewContainer"] { padding-bottom: 20px !important; }

.top-bar {
    position: fixed; top: 0; left: 50%; transform: translateX(-50%);
    width: 100%; max-width: 480px;
    background: #0b141a; border-bottom: 2px solid #203038;
    padding: 10px 20px; display: flex; align-items: center;
    justify-content: space-between; z-index: 9999; font-weight: 800;
}
.top-bar .metric { display:flex; align-items:center; gap:5px; font-size:15px; }
.top-bar .streak { color:#ff9600; }
.top-bar .xp { color:#1cb0f6; }

.main-wrap { max-width: 480px; margin: 0 auto; padding: 72px 16px 20px; }
.g-card {
    background: #131f24; border: 2px solid #203038;
    border-radius: 20px; padding: 20px; margin-bottom: 14px;
}

div[data-testid="stButton"] > button {
    background: #58cc02 !important; color: #fff !important;
    border: none !important; border-radius: 16px !important;
    font-family: 'Nunito', sans-serif !important; font-weight: 800 !important;
    font-size: 16px !important; padding: 14px 28px !important;
    box-shadow: 0 4px 0 #46a302 !important; width: 100% !important;
    transition: transform 0.08s, box-shadow 0.08s !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(3px) !important; box-shadow: 0 1px 0 #46a302 !important;
}
div[data-testid="stButton"] > button:hover { background: #65d900 !important; border: none !important; }

.stTextArea textarea {
    background: #131f24 !important; border: 2px solid #203038 !important;
    color: #e8f4f8 !important; border-radius: 14px !important;
    font-family: 'Nunito', sans-serif !important; font-weight: 600 !important;
    font-size: 15px !important;
}
.stTextArea textarea:focus { border-color: #1cb0f6 !important; box-shadow: none !important; }
label[data-testid="stWidgetLabel"] { color: #8a9baa !important; font-family: 'Nunito', sans-serif !important; font-weight: 700 !important; }

.meter-bar {
    height: 24px; border-radius: 50px; overflow: hidden;
    background: #203038; position: relative; margin-bottom: 8px;
}
.meter-fill {
    height: 100%; border-radius: 50px;
    transition: width 1.2s ease;
    display: flex; align-items: center; padding-left: 12px;
    font-size: 12px; font-weight: 800; color: #fff;
}

@keyframes confetti-fall {
    0%  { transform: translateY(-20px) rotate(0deg); opacity: 1; }
    100% { transform: translateY(600px) rotate(720deg); opacity: 0; }
}
.confetti-piece {
    position: fixed; top: 0; font-size: 22px;
    animation: confetti-fall 3s ease-in forwards;
    pointer-events: none; z-index: 99999;
}

.challenge-badge {
    display: inline-block; padding: 4px 12px;
    border-radius: 50px; font-size: 12px; font-weight: 800;
}

.checklist-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 14px; border-radius: 12px; margin-bottom: 8px;
    background: #0b1a20; border: 1px solid #203038;
    font-size: 13px; font-weight: 600; line-height: 1.4;
}
.checklist-item.pass { border-color: #58cc0244; }
.checklist-item.fail { border-color: #ff4b4b44; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
    <a href="/" style="font-size:22px;text-decoration:none">←</a>
    <div style="font-weight:900;font-size:16px">🎙️ Practice Arena</div>
    <div class="metric streak">🔥 {st.session_state.streak}</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LEVEL DATA
# ─────────────────────────────────────────────
LEVELS = {
    4: {
        "title": "Elevator Pitch",
        "icon": "🚀",
        "difficulty": "Intermediate",
        "xp": 125,
        "scenario": (
            "You're in an elevator with your company's CEO. "
            "You have exactly 60 seconds to pitch your project idea for a new AI-powered onboarding tool. "
            "Be concise, compelling, and clear about the business value."
        ),
        "evaluation_rubric": [
            "Clear problem statement in first 15 seconds",
            "Specific business impact or metric mentioned",
            "Confident and warm tone throughout",
            "No filler words (um, uh, like, you know)",
            "Strong call-to-action at the end",
        ],
        "prompt": (
            "You are an expert communication coach evaluating an elevator pitch for a junior employee. "
            "The scenario was: pitching a new AI-powered onboarding tool to the CEO in 60 seconds.\n\n"
            "Evaluate the following response across these dimensions:\n"
            "1. Clarity (0-100): How clear and structured is the pitch?\n"
            "2. Warmth & Tone (0-100): How confident, warm, and engaging is the delivery?\n"
            "3. Content Quality (0-100): Does it include a problem, solution, and CTA?\n"
            "4. Conciseness (0-100): Is it appropriately brief and punchy?\n\n"
            "Also identify exactly which of these 5 rubric items were met:\n"
            "- Clear problem statement in first 15 seconds\n"
            "- Specific business impact or metric mentioned\n"
            "- Confident and warm tone throughout\n"
            "- No filler words (um, uh, like, you know)\n"
            "- Strong call-to-action at the end\n\n"
            "Respond ONLY in this JSON format (no markdown):\n"
            "{\n"
            '  "clarity": 82,\n'
            '  "warmth": 75,\n'
            '  "content": 88,\n'
            '  "conciseness": 70,\n'
            '  "rubric_passed": [0, 2, 4],\n'
            '  "overall_tip": "One specific actionable improvement tip in 1-2 sentences."\n'
            "}\n\n"
            "The user's pitch:\n"
        ),
    },
    1: {
        "title": "First Impressions",
        "icon": "👋",
        "difficulty": "Beginner",
        "xp": 50,
        "scenario": "Introduce yourself to a new client you're meeting for the first time at a networking event. Make them remember you.",
        "evaluation_rubric": [
            "Clear and confident name introduction",
            "Memorable hook or unique value statement",
            "Showed genuine interest in the other person",
            "Maintained an upbeat and friendly tone",
            "Natural conversation flow (not rehearsed-sounding)",
        ],
        "prompt": (
            "You are an expert communication coach evaluating a first-impression introduction.\n\n"
            "Evaluate across: Clarity (0-100), Warmth (0-100), Content (0-100), Conciseness (0-100).\n"
            "Check which rubric items were met (indices 0-4):\n"
            "0: Clear and confident name introduction\n"
            "1: Memorable hook or unique value statement\n"
            "2: Showed genuine interest in the other person\n"
            "3: Maintained an upbeat and friendly tone\n"
            "4: Natural conversation flow\n\n"
            "Respond ONLY in JSON (no markdown):\n"
            '{"clarity":75,"warmth":80,"content":70,"conciseness":85,"rubric_passed":[0,3],"overall_tip":"Your tip here."}\n\n'
            "The user's response:\n"
        ),
    },
}

target_lid = st.session_state.get("target_level", st.session_state.current_level)
level = LEVELS.get(target_lid, LEVELS[4])

# ─────────────────────────────────────────────
# GEMINI SETUP
# ─────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def evaluate_with_gemini(user_text: str, prompt_prefix: str) -> dict:
    """Call Gemini to evaluate the user's response and return parsed scores."""
    import json

    if not GEMINI_API_KEY:
        # Fallback mock scores for demo without API key
        return {
            "clarity": 78, "warmth": 82, "content": 74, "conciseness": 85,
            "rubric_passed": [0, 2, 4],
            "overall_tip": "Try opening with a stronger hook — lead with the problem before the solution to grab attention immediately.",
        }

   
    except Exception as e:
return {
            "clarity": 70, "warmth": 65, "content": 72, "conciseness": 68,
            "rubric_passed": [0],
            "overall_tip": f"Could not reach Gemini API. Please check your GEMINI_API_KEY. Error: {str(e)[:80]}",
        }


# ─────────────────────────────────────────────
# RESULTS VIEW
# ─────────────────────────────────────────────
def render_results(scores: dict, rubric_items: list):
    passed = scores.get("rubric_passed", [])
    all_passed = len(passed) == len(rubric_items)
    overall = int((scores["clarity"] + scores["warmth"] + scores["content"] + scores["conciseness"]) / 4)
    xp_earned = int(level["xp"] * (overall / 100))

    # Confetti if perfect
    if all_passed:
        confetti_emojis = ["🎉", "⭐", "🌟", "✨", "🏆", "💎", "🎊", "🐴"]
        confetti_html = ""
        for i in range(18):
            import random
            emoji = random.choice(confetti_emojis)
            left = random.randint(2, 95)
            delay = random.uniform(0, 1.5)
            confetti_html += f'<div class="confetti-piece" style="left:{left}%;animation-delay:{delay:.1f}s">{emoji}</div>'
        st.markdown(confetti_html, unsafe_allow_html=True)

    # Overall score hero
    score_color = "#58cc02" if overall >= 80 else ("#ff9600" if overall >= 60 else "#ff4b4b")
    grade = "Excellent! 🌟" if overall >= 80 else ("Good work! 💪" if overall >= 60 else "Keep practicing! 🔄")

    st.markdown(f"""
    <div class="g-card" style="text-align:center;border-color:{score_color};
         background:linear-gradient(135deg,#131f24,#0f1e14)">
        <div style="font-size:64px;font-weight:900;color:{score_color};
                    text-shadow:0 0 24px {score_color}88">{overall}</div>
        <div style="font-size:13px;color:#4a6572;font-weight:700;margin:-6px 0 6px">OVERALL SCORE</div>
        <div style="font-size:18px;font-weight:800">{grade}</div>
        <div style="margin-top:12px;font-size:14px;font-weight:700;color:#ffd700">+{xp_earned} XP earned!</div>
    </div>
    """, unsafe_allow_html=True)

    # Metric meters
    col1, col2 = st.columns(2)
    metrics = [
        ("🎯 Clarity",    scores["clarity"],    "#1cb0f6"),
        ("💛 Warmth",     scores["warmth"],     "#ff9600"),
        ("📋 Content",    scores["content"],    "#a346ff"),
        ("✂️ Conciseness", scores["conciseness"], "#58cc02"),
    ]
    for i, (label, val, color) in enumerate(metrics):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="g-card" style="padding:14px;margin-bottom:10px">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                    <span style="font-size:12px;font-weight:700">{label}</span>
                    <span style="font-size:13px;font-weight:900;color:{color}">{val}</span>
                </div>
                <div class="meter-bar">
                    <div class="meter-fill" style="background:{color};width:{val}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Rubric checklist
    st.markdown("""
    <div style="font-size:13px;font-weight:800;color:#4a6572;text-transform:uppercase;
                letter-spacing:1.5px;margin:16px 0 10px">📋 Communication Checklist</div>
    """, unsafe_allow_html=True)

    for idx, item in enumerate(rubric_items):
        is_pass = idx in passed
        icon = "✅" if is_pass else "❌"
        cls = "pass" if is_pass else "fail"
        color = "#58cc02" if is_pass else "#ff4b4b"
        st.markdown(f"""
        <div class="checklist-item {cls}">
            <span style="font-size:18px">{icon}</span>
            <span style="color:{'#e8f4f8' if is_pass else '#ff7b7b'}">{item}</span>
        </div>
        """, unsafe_allow_html=True)

    # Tip
    tip = scores.get("overall_tip", "")
    if tip:
        st.markdown(f"""
        <div class="g-card" style="border-color:#1cb0f6;background:#0d1e26;margin-top:16px">
            <div style="font-size:13px;font-weight:800;color:#1cb0f6;margin-bottom:8px">💡 Coach's Tip</div>
            <div style="font-size:14px;font-weight:600;line-height:1.6">{tip}</div>
        </div>
        """, unsafe_allow_html=True)

    # Actions
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.last_score = None
            st.rerun()
    with col_b:
        if st.button("🏠 Back to Path", use_container_width=True):
            # Level up if score is good enough
            if overall >= 70 and target_lid not in st.session_state.completed_levels:
                st.session_state.completed_levels.append(target_lid)
                st.session_state.xp += xp_earned
                if target_lid == st.session_state.current_level:
                    st.session_state.current_level = target_lid + 1
            st.switch_page("Home.py")


# ─────────────────────────────────────────────
# MAIN PRACTICE ARENA
# ─────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

if st.session_state.show_results and st.session_state.last_score:
    render_results(st.session_state.last_score, level["evaluation_rubric"])
else:
    # Challenge card
    diff_colors = {"Beginner": "#58cc02", "Intermediate": "#ff9600", "Advanced": "#ff4b4b"}
    diff_color = diff_colors.get(level["difficulty"], "#4a6572")

    st.markdown(f"""
    <div class="g-card" style="border-color:#1cb0f6">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">
            <div style="font-size:42px">{level['icon']}</div>
            <div>
                <div style="font-size:20px;font-weight:900">{level['title']}</div>
                <div style="display:flex;gap:8px;margin-top:4px">
                    <span class="challenge-badge" style="background:{diff_color}22;color:{diff_color};border:1px solid {diff_color}44">
                        {level['difficulty']}
                    </span>
                    <span class="challenge-badge" style="background:#ffd70022;color:#ffd700;border:1px solid #ffd70044">
                        +{level['xp']} XP
                    </span>
                </div>
            </div>
        </div>
        <div style="font-size:13px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">
            🎙️ SCENARIO
        </div>
        <div style="font-size:14px;font-weight:600;line-height:1.7;color:#c8dde8;
                    background:#0b141a;border-radius:12px;padding:14px;border:1px solid #203038">
            {level['scenario']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Rubric preview
    with st.expander("📋 What you'll be evaluated on"):
        for item in level["evaluation_rubric"]:
            st.markdown(f"• {item}")

    st.markdown("""
    <div style="font-size:13px;font-weight:800;color:#4a6572;text-transform:uppercase;
                letter-spacing:1.5px;margin:20px 0 10px">🎤 Your Response</div>
    """, unsafe_allow_html=True)

    # Audio input (if available) or text
    st.markdown("""
    <div class="g-card" style="padding:14px">
        <div style="font-size:13px;font-weight:700;color:#4a6572;margin-bottom:10px">
            🎙️ Record your pitch (or type below)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Streamlit's audio input (v1.29+)
    try:
        audio_data = st.audio_input("Record your response")
        if audio_data:
            st.audio(audio_data)
            st.markdown("""
            <div class="g-card" style="border-color:#ff9600;padding:12px;text-align:center">
                <span style="font-size:13px;font-weight:700;color:#ff9600">
                    🎙️ Audio recorded! Gemini transcription coming soon — type your pitch below for instant AI feedback.
                </span>
            </div>
            """, unsafe_allow_html=True)
    except Exception:
        st.markdown("""
        <div class="g-card" style="padding:12px;text-align:center">
            <span style="font-size:13px;font-weight:700;color:#4a6572">
                🎙️ Audio input available in Streamlit v1.29+
            </span>
        </div>
        """, unsafe_allow_html=True)

    user_response = st.text_area(
        "Type or paste your response here...",
        height=160,
        placeholder="Start speaking or typing your response...",
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Get AI Feedback", use_container_width=True):
        if user_response.strip():
            with st.spinner("🐴 Gallopi is reviewing your pitch..."):
                scores = evaluate_with_gemini(user_response, level["prompt"])
            st.session_state.last_score = scores
            st.session_state.show_results = True
            # Deduct energy
            if st.session_state.energy > 0:
                st.session_state.energy -= 1
            st.rerun()
        else:
            st.warning("Share your response first before submitting! 🐴")

    if st.button("← Back to Path", use_container_width=True):
        st.switch_page("Home.py")

st.markdown('</div>', unsafe_allow_html=True)