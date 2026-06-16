import streamlit as st

def grade_response(text: str, keywords: list, forbidden: list) -> dict:
    if not text or not text.strip():
        return {
            "clarity": 0, "confidence": 0, "vocabulary": 0, "overall": 0,
            "strengths": ["No speech received"], "improvements": ["Provide a response"],
            "tip": "Speak clearly into your recording browser tool.", "filler_count": 0
        }

    words = text.lower().split()
    word_count = len(words)
    text_lower = text.lower()

    filler_count = sum(text_lower.count(fw) for fw in forbidden)
    confidence_score = max(10, 100 - (filler_count * 20))

    keyword_hits = sum(1 for kw in keywords if kw in text_lower)
    relevance_score = min(100, int((keyword_hits / max(1, len(keywords))) * 150))

    vocab_score = min(100, int((len(set(words)) / max(1, word_count)) * 120))
    overall = int((confidence_score + relevance_score + vocab_score) / 3)

    strengths = []
    improvements = []
    if confidence_score > 80: strengths.append("Excellent execution directly free of passive fillers.")
    else: improvements.append("Minimize pacing metrics including vocal hedges.")

    if relevance_score > 60: strengths.append("Strong content context inclusion alignment matches.")
    else: improvements.append("Incorporate more context milestone industry anchors.")

    return {
        "clarity": 85, "confidence": confidence_score, "vocabulary": vocab_score, "overall": overall,
        "strengths": strengths, "improvements": improvements, "tip": "Elevate delivery via crisp metric action keywords.",
        "filler_count": filler_count
    }

def inject_css():
    st.markdown("""
<style>
    .stApp { background-color: #0b141a; color: #f7f9fc; }
    .unicorn-float { font-size: 70px; animation: float 3s ease-in-out infinite; display: inline-block; text-align: center; width: 100%; }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
    .g-card { background: #131f24; border: 2px solid #203038; border-radius: 16px; padding: 16px; margin-bottom: 12px; }
    div[data-testid="stForm"] { background: #131f24 !important; border: 2px solid #203038 !important; border-radius: 16px !important; }
</style>
""", unsafe_allow_html=True)

def topbar(back_href="/"):
    st.markdown(f"""
<div style="display:flex; justify-content: space-around; background: #131f24; padding: 12px; border-radius:16px; border:2px solid #203038; margin-bottom:20px;">
    <span style="color:#ff9600; font-weight:bold;">🔥 {st.session_state.get('streak', 7)} Days</span>
    <span style="color:#1cb0f6; font-weight:bold;">💎 {st.session_state.get('gems', 1240)} Gems</span>
</div>
""", unsafe_allow_html=True)

def bottom_nav(p="path"):
    pass