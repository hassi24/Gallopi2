import streamlit as st
from utils.state import init_state
from utils.helpers import inject_css, topbar, grade_response
from utils.content import LEVELS_BY_ID

st.set_page_config(page_title="Arena · Gallopi", page_icon="🎙️", layout="centered", initial_sidebar_state="collapsed")
init_state()
inject_css()
topbar()

if not st.session_state.active_scenario:
    st.warning("No level context currently active.")
    if st.button("Return Map Home"): st.switch_page("Home.py")
    st.stop()

lvl = LEVELS_BY_ID.get(st.session_state.active_scenario)
q_index = st.session_state.arena_q_index
current_q = lvl["questions"][q_index]

st.markdown(f"## 🗣️ Challenge: {lvl['title']}")
st.info(f"👉 **Prompt Context:** {current_q['q']}\n\n💡 *Hint:* {current_q['hint']}")

rec_clicked = st.button("🔴 Click to Record Voice Input")
if rec_clicked:
    st.markdown("<p style='color:#ff9600;font-weight:bold;'>🟢 Streaming Microphones Captures Active...</p>", unsafe_allow_html=True)

user_text = st.text_area(
    "Live Transcript Edit Sync Box:",
    value="I am super excited to join the new development team and collaborate closely to hit our metrics growth target!" if rec_clicked else "",
    placeholder="Speak or type your full presentation details..."
)

if st.button("Submit Speech Challenge 🚀", type="primary"):
    if user_text.strip():
        scores = grade_response(user_text, current_q["keywords"], current_q["forbidden"])
        st.session_state.arena_scores = scores
        st.session_state.arena_show_results = True
        
        st.session_state.xp += 25
        st.session_state.gems += 15
        st.session_state.session_history.append({
            "level": lvl["title"], "icon": lvl["icon"], "score": scores["overall"], "xp": 25, "date": "Today"
        })
        st.balloons()
    else:
        st.error("Please provide transcripts before evaluating answers.")

if st.session_state.arena_show_results and st.session_state.arena_scores:
    res = st.session_state.arena_scores
    st.markdown(f"### 📊 Performance Evaluation Matrix Score: `{res['overall']} / 100`")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Confidence Meter", f"{res['confidence']}%")
    c2.metric("Vocabulary Range", f"{res['vocabulary']}%")
    c3.metric("Speech Clarity", f"{res['clarity']}%")
    
    st.markdown("#### 🌟 Detected Strengths:")
    for s in res["strengths"]: st.success(s)
    
    st.markdown("#### ⚠️ Focus areas for Improvement:")
    for imp in res["improvements"]: st.warning(imp)
    
    st.info(f"💡 **Unicorn Coaching Guidance:** {res['tip']}")
    
    if st.button("Finish & Return to Course Map 🧭"):
        st.session_state.active_scenario = None
        st.session_state.arena_show_results = False
        st.switch_page("Home.py")