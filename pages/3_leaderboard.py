import streamlit as st
from utils.state import init_state
from utils.helpers import inject_css, topbar
from utils.content import ANIMAL_AVATARS

st.set_page_config(page_title="Leaderboard", layout="centered")
init_state()
inject_css()
topbar()

st.title("🏆 Arena Rankings")
all_players = [
    {"name": "PitchKing", "avatar": "🦁", "xp": 450},
    {"name": f"{st.session_state.nickname or 'You'} (You)", "avatar": st.session_state.avatar, "xp": st.session_state.xp},
    {"name": "SarahS", "avatar": "🦊", "xp": 120},
    {"name": "AlexT", "avatar": "Panda", "xp": 90}
]
sorted_players = sorted(all_players, key=lambda x: x["xp"], reverse=True)

for idx, p in enumerate(sorted_players, 1):
    st.markdown(f"""
    <div style='display:flex; justify-content:space-between; background:#131f24; padding:12px; margin:6px 0; border:1px solid #203038; border-radius:12px;'>
        <span><b>#{idx}</b> {p['avatar']} {p['name']}</span>
        <span style='color:#1cb0f6; font-weight:bold;'>{p['xp']} XP</span>
    </div>
    """, unsafe_allow_html=True)

if st.button("Return Main Menu 🗺️"): st.switch_page("Home.py")