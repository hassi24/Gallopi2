import streamlit as st
from utils.state import init_state
from utils.helpers import inject_css, topbar

st.set_page_config(page_title="Badges", layout="centered")
init_state()
inject_css()
topbar()

st.title("🏅 Earned Milestones")
has_done = len(st.session_state.session_history) > 0

badges = [
    {"name": "First Word", "icon": "🌱", "earned": has_done, "desc": "Completed your first speech assignment."},
    {"name": "Streak Master", "icon": "🔥", "earned": True, "desc": "Kept account activity alive past 5 days."}
]

for b in badges:
    opacity = "1.0" if b["earned"] else "0.3; filter: grayscale(100%);"
    lbl = "✅ UNLOCKED" if b["earned"] else "🔒 LOCKED"
    st.markdown(f"""
    <div class="g-card" style="opacity: {opacity}; display:flex; gap:20px; align-items:center;">
        <span style="font-size:40px;">{b['icon']}</span>
        <div>
            <h4 style="margin:0; color:#1cb0f6;">{b['name']}</h4>
            <p style="margin:2px 0; font-size:12px; color:#4a6572;">{b['desc']}</p>
            <b style="font-size:11px; color:#58cc02;">{lbl}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

if st.button("Return Main Menu 🗺️"): st.switch_page("Home.py")