"""
utils/helpers.py — Shared UI components, CSS injection, and local grading fallback
"""
import streamlit as st
import json
import re


# ─────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
[data-testid="stMain"],
.main, .block-container {
    background: #0b141a !important;
    font-family: 'Nunito', sans-serif !important;
    color: #e8f4f8 !important;
}

/* Hide all default Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
.stDeployButton,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* Padding for fixed top/bottom bars */
[data-testid="stAppViewContainer"] > section[data-testid="stMain"] > div {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Cards ── */
.g-card {
    background: #131f24;
    border: 2px solid #203038;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 14px;
}

/* ── Section headers ── */
.section-header {
    font-size: 12px;
    font-weight: 800;
    color: #4a6572;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    margin: 20px 0 12px;
}

/* ── Streamlit widget resets ── */
.stTextInput input, .stTextArea textarea {
    background: #131f24 !important;
    border: 2px solid #203038 !important;
    color: #e8f4f8 !important;
    border-radius: 14px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #1cb0f6 !important;
    box-shadow: none !important;
}
label[data-testid="stWidgetLabel"],
.stSelectbox label {
    color: #8a9baa !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
}
.stSelectbox > div > div {
    background: #131f24 !important;
    border: 2px solid #203038 !important;
    color: #e8f4f8 !important;
    border-radius: 14px !important;
}

/* ── Base button (green 3D) ── */
div[data-testid="stButton"] > button {
    background: #58cc02 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 16px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    padding: 14px 28px !important;
    box-shadow: 0 4px 0 #46a302 !important;
    width: 100% !important;
    transition: transform 0.08s, box-shadow 0.08s !important;
    letter-spacing: 0.3px !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(3px) !important;
    box-shadow: 0 1px 0 #46a302 !important;
}
div[data-testid="stButton"] > button:hover {
    background: #65d900 !important;
    border: none !important;
}

/* ── Radio overrides ── */
div[data-testid="stRadio"] > div {
    background: transparent !important;
    gap: 6px !important;
}
div[data-testid="stRadio"] label {
    background: #131f24 !important;
    border: 2px solid #203038 !important;
    border-radius: 12px !important;
    padding: 10px 16px !important;
    color: #e8f4f8 !important;
    font-weight: 700 !important;
    cursor: pointer !important;
}

/* ── Expander ── */
details[data-testid="stExpander"] {
    background: #131f24 !important;
    border: 2px solid #203038 !important;
    border-radius: 16px !important;
}
details[data-testid="stExpander"] summary {
    font-weight: 700 !important;
    color: #8a9baa !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0b141a; }
::-webkit-scrollbar-thumb { background: #203038; border-radius: 4px; }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #1cb0f6 !important; }
</style>
"""

TOP_BAR_STYLE = """
<style>
.top-bar {
    position: fixed; top: 0; left: 0; right: 0;
    background: #0b141a;
    border-bottom: 2px solid #203038;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    z-index: 9999;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    height: 56px;
}
.tb-metric {
    display: flex; align-items: center; gap: 5px;
    font-size: 15px; font-weight: 800;
}
.tb-flag   { font-size: 22px; }
.tb-streak { color: #ff9600; }
.tb-xp     { color: #1cb0f6; }
.tb-energy { color: #a346ff; }
.tb-back   { font-size: 22px; text-decoration: none; color: #e8f4f8; }

/* Push page content below fixed top bar */
.page-wrap {
    max-width: 500px;
    margin: 0 auto;
    padding: 66px 16px 100px;
}
</style>
"""

NAV_STYLE = """
<style>
.bottom-nav-fixed {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: #0b141a;
    border-top: 2px solid #203038;
    display: flex;
    z-index: 9998;
    height: 68px;
    font-family: 'Nunito', sans-serif;
}
.bnav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    cursor: pointer;
    font-size: 10px;
    font-weight: 800;
    color: #3c5566;
    text-decoration: none;
    transition: color 0.15s;
    padding-bottom: 4px;
    border: none;
    background: transparent;
}
.bnav-item .ni { font-size: 24px; line-height: 1.1; }
.bnav-item.active { color: #58cc02; }
.bnav-item:hover { color: #58cc0299; }

/* Override st.columns spacer inside nav container */
.nav-col div[data-testid="stButton"] > button {
    background: transparent !important;
    box-shadow: none !important;
    border-radius: 12px !important;
    color: #3c5566 !important;
    font-size: 10px !important;
    padding: 6px 2px !important;
    line-height: 1.4;
    min-height: 54px;
    border: none !important;
    white-space: pre-line;
}
.nav-col div[data-testid="stButton"] > button:hover {
    background: #131f2488 !important;
    color: #58cc02 !important;
}
.nav-col div[data-testid="stButton"] > button:active {
    transform: none !important;
    box-shadow: none !important;
}
</style>
"""

PATH_NODE_CSS = """
<style>
.path-node-btn {
    width: 78px; height: 78px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    font-weight: 900;
    cursor: pointer;
    border: none;
    transition: transform 0.08s, box-shadow 0.08s;
    text-decoration: none;
    margin: 0 auto;
}
.pn-done   { background: #58cc02; box-shadow: 0 5px 0 #46a302; color: #fff; }
.pn-active { background: #1cb0f6; box-shadow: 0 5px 0 #1899d6; color: #fff;
             animation: pulse-node 1.8s infinite; }
.pn-locked { background: #3c4d55; box-shadow: 0 5px 0 #2c393f; color: #4a6572;
             cursor: not-allowed; }
.pn-future { background: #1e3040; box-shadow: 0 5px 0 #152330; color: #3c5566;
             cursor: not-allowed; }
@keyframes pulse-node {
    0%,100% { box-shadow: 0 5px 0 #1899d6, 0 0 0 0 rgba(28,176,246,0.4); }
    50%      { box-shadow: 0 5px 0 #1899d6, 0 0 0 14px rgba(28,176,246,0); }
}
.path-node-btn:active { transform: translateY(4px); }
.node-label {
    font-size: 11px; font-weight: 700;
    color: #4a6572; text-align: center;
    margin-top: 6px; line-height: 1.3;
}
.node-xp { font-size: 11px; font-weight: 800; color: #ff9600; margin-top: 2px; }
.node-tap { font-size: 10px; font-weight: 800; color: #1cb0f6; margin-top: 2px; }
.path-connector {
    display: flex; justify-content: center; margin: 0;
    height: 30px;
}
.path-line {
    width: 3px;
    background: repeating-linear-gradient(
        180deg,
        #203038 0, #203038 6px,
        transparent 6px, transparent 12px
    );
    border-radius: 2px;
}
.treasure-row {
    display: flex; flex-direction: column;
    align-items: center; margin: 6px 0 16px;
}
.treasure-icon {
    font-size: 52px;
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 0 16px #ff960088);
}
@keyframes float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}
</style>
"""


def inject_global_css():
    st.markdown(GLOBAL_CSS + TOP_BAR_STYLE + NAV_STYLE + PATH_NODE_CSS,
                unsafe_allow_html=True)


def render_top_bar(back_href: str = None):
    """Renders the fixed top metric bar."""
    flag = "🇺🇸"
    streak = st.session_state.get("streak", 0)
    xp = st.session_state.get("xp", 0)
    energy = st.session_state.get("energy", 0)

    left = f'<a href="{back_href}" class="tb-back">←</a>' if back_href else f'<span class="tb-flag">{flag}</span>'

    st.markdown(f"""
    <div class="top-bar">
        {left}
        <div class="tb-metric tb-streak">🔥 {streak}</div>
        <div class="tb-metric tb-xp">💎 {xp:,}</div>
        <div class="tb-metric tb-energy">⚡ {energy}/5</div>
    </div>
    """, unsafe_allow_html=True)


def render_bottom_nav():
    """Renders the sticky bottom nav using Streamlit columns inside a fixed div."""
    p = st.session_state.get("current_page", "path")

    # Spacer div placeholder for fixed nav
    st.markdown('<div class="bottom-nav-fixed" id="bnav-placeholder"></div>', unsafe_allow_html=True)

    # Actual clickable nav in a fixed container rendered via columns
    nav_items = [
        ("path",        "🏠", "Path"),
        ("quests",      "🏅", "Quests"),
        ("leaderboard", "🏆", "Rank"),
        ("profile",     "👤", "Profile"),
    ]
    st.markdown('<div class="nav-col" style="position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#0b141a;border-top:2px solid #203038;height:68px;display:flex">', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (pid, icon, label) in enumerate(nav_items):
        active_style = "color:#58cc02!important" if p == pid else ""
        with cols[i]:
            if st.button(f"{icon}\n{label}", key=f"nav_{pid}", use_container_width=True):
                st.session_state.current_page = pid
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def parse_gemini_json(raw: str) -> dict:
    """Safely extract a JSON object from a Gemini response string."""
    raw = raw.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    # Try direct parse first
    try:
        return json.loads(raw)
    except Exception:
        pass
    # Try to find first { ... } block
    match = re.search(r"\{.*?\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return {}


def fallback_scores() -> dict:
    """Return demo scores when no Gemini key is available."""
    return {
        "clarity": 78,
        "warmth": 82,
        "content": 74,
        "conciseness": 85,
        "rubric_passed": [0, 2, 4],
        "overall_tip": "Great start! Try opening with a stronger hook — lead with the core problem before diving into your solution to grab attention immediately.",
    }


def evaluate_with_gemini(user_text: str, prompt_prefix: str) -> dict:
    """Call Gemini to evaluate user response. Falls back to mock on error."""
    import os
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return fallback_scores()
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt_prefix + user_text)
        result = parse_gemini_json(response.text)
        if "clarity" not in result:
            return fallback_scores()
        return result
    except Exception as e:
        fb = fallback_scores()
        fb["overall_tip"] = f"[API Error: {str(e)[:80]}] " + fb["overall_tip"]
        return fb