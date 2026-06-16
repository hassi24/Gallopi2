import streamlit as st
from utils.state import init_state
from utils.helpers import inject_css, topbar

st.set_page_config(page_title="Profile", layout="centered")
init_state()
inject_css()
topbar()

st.title("👤 User Profile Management Hub")
st.markdown(f"<h3>{st.session_state.avatar} Handle: {st.session_state.nickname or 'Learner'}</h3>", unsafe_allow_html=True)

st.markdown("### 📈 Recent Activity Session Records")
if not st.session_state.session_history:
    st.info("No timeline metrics captured yet. Finish your initial challenge module on the learning map!")
else:
    for item in st.session_state.session_history:
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; background:#131f24; padding:12px; margin:4px 0; border-radius:8px; border:1px solid #203038;'>
            <span>{item['icon']} <b>{item['level']}</b></span>
            <span style='color:#ff9600; font-weight:bold;'>Score: {item['score']}/100 (+{item['xp']} XP)</span>
        </div>
        """, unsafe_allow_html=True)

if st.button("Return Main Menu 🗺️"): st.switch_page("Home.py")