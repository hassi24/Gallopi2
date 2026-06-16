import re
import streamlit as st

# ═══════════════════════════════════════════════════════════
# DETERMINISTIC LOCAL GRADING ENGINE
# ═══════════════════════════════════════════════════════════

FILLER_WORDS = ["um", "uh", "like", "basically", "literally", "you know",
                "i guess", "sort of", "kind of", "anyway", "whatever", "right like"]

def grade_response(text: str, keywords: list, forbidden: list) -> dict:
    """
    100% local deterministic grader. No AI needed.
    Returns scores, strengths, improvements, and tip.
    """
    if not text or not text.strip():
        return {
            "clarity": 0, "confidence": 0, "vocabulary": 0, "conciseness": 0,
            "overall": 0, "rubric_passed": [],
            "strengths": ["No response recorded"],
            "improvements": ["Please provide a response to evaluate"],
            "tip": "Speak clearly and respond to the question prompt.",
            "word_count": 0, "filler_count": 0, "keyword_hits": 0,
        }

    words = text.lower().split()
    word_count = len(words)
    text_lower = text.lower()

    # — Filler word penalty —
    filler_hits = []
    for fw in FILLER_WORDS:
        count = text_lower.count(fw)
        if count > 0:
            filler_hits.append((fw, count))
    total_fillers = sum(c for _, c in filler_hits)
    filler_penalty = min(40, total_fillers * 8)

    # — Keyword alignment score —
    kw_hits = []
    all_kw = keywords or []
    for kw in all_kw:
        if kw.lower() in text_lower:
            kw_hits.append(kw)
    keyword_ratio = len(kw_hits) / max(len(all_kw), 1)
    vocabulary_score = int(min(100, 40 + keyword_ratio * 60))

    # — Forbidden word check (from level) —
    forbidden_hits = []
    for fw in (forbidden or []):
        if fw.lower() in text_lower:
            forbidden_hits.append(fw)
    forbidden_penalty = min(30, len(forbidden_hits) * 8)

    # — Word count scoring (ideal: 40-150 words) —
    if word_count < 10:
        length_score = 20
    elif word_count < 25:
        length_score = 45
    elif word_count < 40:
        length_score = 65
    elif word_count <= 150:
        length_score = 90
    elif word_count <= 220:
        length_score = 75
    else:
        length_score = 55

    # — Sentence structure check —
    sentences = re.split(r'[.!?]+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    has_opener = len(sentences) > 0 and len(sentences[0].split()) >= 4
    has_closer = len(sentences) > 1 and len(sentences[-1].split()) >= 3
    structure_bonus = 10 if has_opener else 0
    structure_bonus += 8 if has_closer else 0

    # — Confidence markers (positive language) —
    confidence_markers = ["will", "can", "achieve", "confident", "ensure",
                          "committed", "deliver", "lead", "drive", "believe",
                          "passionate", "excited", "proud", "strong"]
    conf_hits = sum(1 for m in confidence_markers if m in text_lower)
    confidence_score = min(100, 40 + conf_hits * 10)
    confidence_score -= filler_penalty
    confidence_score = max(10, confidence_score)

    # — Clarity score —
    clarity_score = min(100, length_score + structure_bonus)
    clarity_score -= forbidden_penalty
    clarity_score = max(10, clarity_score)

    # — Conciseness —
    if word_count < 10:
        conciseness_score = 20
    elif word_count <= 80:
        conciseness_score = 95
    elif word_count <= 130:
        conciseness_score = 80
    elif word_count <= 180:
        conciseness_score = 65
    else:
        conciseness_score = 45

    # — Overall score —
    overall = int(
        clarity_score * 0.25 +
        confidence_score * 0.25 +
        vocabulary_score * 0.30 +
        conciseness_score * 0.20
    )
    overall = max(10, min(99, overall))

    # — Rubric pass/fail (5 items) —
    rubric_passed = []
    if keyword_ratio >= 0.3:
        rubric_passed.append(0)
    if total_fillers == 0:
        rubric_passed.append(1)
    if word_count >= 30:
        rubric_passed.append(2)
    if confidence_score >= 55:
        rubric_passed.append(3)
    if clarity_score >= 55:
        rubric_passed.append(4)

    # — Strengths —
    strengths = []
    if keyword_ratio >= 0.4:
        strengths.append(f"Strong vocabulary — used {len(kw_hits)} key power phrases")
    if total_fillers == 0:
        strengths.append("Zero filler words — clean, confident delivery!")
    elif total_fillers <= 1:
        strengths.append("Minimal filler words — almost filler-free!")
    if word_count >= 40:
        strengths.append(f"Good depth — {word_count} words shows thorough thinking")
    if confidence_score >= 65:
        strengths.append("Confident, assertive language detected")
    if has_opener:
        strengths.append("Strong opening sentence structure")
    if not strengths:
        strengths.append("You submitted a response — that's the first step!")

    # — Improvements —
    improvements = []
    if total_fillers > 2:
        worst = sorted(filler_hits, key=lambda x: -x[1])[:2]
        worst_str = ", ".join([f'"{w}" ({c}x)' for w, c in worst])
        improvements.append(f"Eliminate filler words: {worst_str}")
    if keyword_ratio < 0.3:
        missed = [k for k in all_kw[:4] if k not in kw_hits]
        if missed:
            improvements.append(f"Try incorporating: {', '.join(missed[:3])}")
    if word_count < 25:
        improvements.append("Expand your answer — aim for at least 40 words")
    if word_count > 180:
        improvements.append("Be more concise — trim to under 150 words")
    if forbidden_hits:
        improvements.append(f"Avoid these words in this context: {', '.join(forbidden_hits[:3])}")
    if confidence_score < 50:
        improvements.append("Use stronger, more assertive language (will, ensure, commit)")
    if not improvements:
        improvements.append("Keep pushing for even more specific examples and data")

    # — Coaching tip —
    if overall >= 85:
        tip = "Excellent! You're boardroom-ready. Next time, add one specific data point to make it unforgettable."
    elif overall >= 70:
        tip = "Solid response! Focus on eliminating filler words and adding more power vocabulary to break into the top tier."
    elif overall >= 55:
        tip = "Good foundation. Practice speaking with more assertive language — replace 'I think' with 'I know' and 'maybe' with 'will'."
    else:
        tip = "Keep practicing! Start with a strong opener, include 2-3 key power words, and finish with a clear call to action."

    return {
        "clarity": clarity_score,
        "confidence": confidence_score,
        "vocabulary": vocabulary_score,
        "conciseness": conciseness_score,
        "overall": overall,
        "rubric_passed": rubric_passed,
        "strengths": strengths[:3],
        "improvements": improvements[:3],
        "tip": tip,
        "word_count": word_count,
        "filler_count": total_fillers,
        "keyword_hits": len(kw_hits),
    }


# ═══════════════════════════════════════════════════════════
# GLOBAL CSS — injected once at top of every page
# ═══════════════════════════════════════════════════════════

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, .block-container {
    background-color: #0b141a !important;
    font-family: 'Nunito', sans-serif !important;
    color: #e8f4f8 !important;
}

#MainMenu, footer, header,
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stDeployButton { display: none !important; }

.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 520px !important;
    margin: 0 auto !important;
}

/* Page content pushed below top bar */
section[data-testid="stMain"] > div:first-child {
    padding-top: 0 !important;
}

/* Text inputs */
.stTextInput input, .stTextArea textarea {
    background: #131f24 !important;
    border: 2px solid #203038 !important;
    border-radius: 14px !important;
    color: #e8f4f8 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 14px 18px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #1cb0f6 !important;
    box-shadow: none !important;
    outline: none !important;
}
label, [data-testid="stWidgetLabel"] p {
    color: #8a9baa !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}

/* ALL buttons → 3D green by default */
div[data-testid="stButton"] > button {
    background: #58cc02 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 16px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    padding: 13px 24px !important;
    box-shadow: 0 4px 0 #46a302 !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: transform 0.08s ease, box-shadow 0.08s ease !important;
    cursor: pointer !important;
}
div[data-testid="stButton"] > button:hover {
    background: #6ada10 !important;
    border: none !important;
    box-shadow: 0 5px 0 #46a302 !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(3px) !important;
    box-shadow: 0 1px 0 #46a302 !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #131f24 !important;
    border: 2px solid #203038 !important;
    color: #e8f4f8 !important;
    border-radius: 14px !important;
}

/* Expander */
details[data-testid="stExpander"] {
    background: #131f24 !important;
    border: 2px solid #203038 !important;
    border-radius: 16px !important;
}
details summary {
    font-weight: 700 !important;
    color: #8a9baa !important;
    padding: 12px 16px !important;
}

/* Step dots */
.step-dots { display:flex; gap:8px; justify-content:center; margin-bottom:20px; }
.dot { width:10px; height:10px; border-radius:50%; background:#203038; }
.dot.active { background:#1cb0f6; }
.dot.done { background:#58cc02; }

/* Unicorn animations */
@keyframes unicorn-float {
    0%,100% { transform: translateY(0px) rotate(-2deg); }
    50%      { transform: translateY(-14px) rotate(2deg); }
}
@keyframes unicorn-pulse {
    0%,100% { filter: drop-shadow(0 0 8px #a346ff88); }
    50%      { filter: drop-shadow(0 0 22px #a346ffcc); }
}
.unicorn-mascot {
    font-size: 80px;
    display: block;
    text-align: center;
    animation: unicorn-float 3s ease-in-out infinite, unicorn-pulse 2.5s ease-in-out infinite;
    cursor: default;
    user-select: none;
    margin: 0 auto 8px;
}
.unicorn-small {
    font-size: 36px;
    display: inline-block;
    animation: unicorn-float 3s ease-in-out infinite;
}

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0b141a; }
::-webkit-scrollbar-thumb { background: #203038; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


def topbar(back_href: str = None):
    streak = st.session_state.get("streak", 0)
    xp     = st.session_state.get("xp", 0)
    energy = st.session_state.get("energy", 0)
    left_html = (
        f'<a href="{back_href}" style="font-size:22px;text-decoration:none;color:#e8f4f8;">&#8592;</a>'
        if back_href else '<span style="font-size:18px;font-weight:900;color:#e8f4f8;">US</span>'
    )
    st.markdown(f"""
<div style="position:fixed;top:0;left:0;right:0;z-index:9999;
            background:#0b141a;border-bottom:2px solid #203038;
            height:52px;display:flex;align-items:center;justify-content:space-around;
            font-family:'Nunito',sans-serif;font-weight:800;padding:0 12px;">
    {left_html}
    <span style="color:#ff9600;font-size:15px;">&#128293; {streak}</span>
    <span style="color:#1cb0f6;font-size:15px;">&#128142; {xp:,}</span>
    <span style="color:#a346ff;font-size:15px;">&#9889; {energy}/5</span>
</div>
<div style="height:60px;"></div>
""", unsafe_allow_html=True)


def bottom_nav():
    p = st.session_state.get("current_page", "path")
    nav_items = [("path","🏠","Path"),("quests","🏅","Quests"),("leaderboard","🏆","Rank"),("profile","👤","Me")]
    st.markdown('<div style="height:80px;"></div>', unsafe_allow_html=True)
    st.markdown("""
<style>
.bnav-wrap {
    position:fixed;bottom:0;left:0;right:0;z-index:9998;
    background:#0b141a;border-top:2px solid #203038;height:68px;
    display:flex;font-family:'Nunito',sans-serif;
}
.bnav-btn {
    flex:1;display:flex;flex-direction:column;align-items:center;
    justify-content:center;gap:2px;font-size:10px;font-weight:800;
    color:#3c5566;text-decoration:none;border:none;background:transparent;
    cursor:pointer;padding-bottom:4px;
}
.bnav-btn .ni { font-size:24px;line-height:1.1; }
.bnav-btn.active { color:#58cc02; }
</style>
""", unsafe_allow_html=True)

    # Streamlit columns inside fixed div
    st.markdown('<div class="bnav-wrap">', unsafe_allow_html=True)
    cols = st.columns(4)
    for i,(pid,icon,label) in enumerate(nav_items):
        with cols[i]:
            active_color = "#58cc02" if p == pid else "#3c5566"
            # Each column gets a button that updates page
            if st.button(f"{icon}\n{label}", key=f"bnav_{pid}", use_container_width=True):
                st.session_state.current_page = pid
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Override button styling inside nav only
    st.markdown("""
<style>
/* Nav bar button style override */
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
    background: transparent !important;
    box-shadow: none !important;
    border-radius: 10px !important;
    color: #3c5566 !important;
    font-size: 10px !important;
    padding: 6px 2px !important;
    min-height: 54px !important;
    border: none !important;
    white-space: pre-line !important;
    line-height: 1.5 !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:hover {
    background: #131f2488 !important;
    color: #58cc02 !important;
    box-shadow: none !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:active {
    transform: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)
