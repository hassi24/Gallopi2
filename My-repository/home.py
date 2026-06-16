import streamlit as st
from utils.state import init_state
from utils.helpers import inject_css, topbar
from utils.content import ANIMAL_AVATARS, FOCUS_OPTIONS, LEVELS

st.set_page_config(page_title="Gallopi 🦄", page_icon="🦄", layout="centered", initial_sidebar_state="collapsed")
init_state()
inject_css()

if not st.session_state.onboarded:
    st.markdown('<div class="unicorn-float">🦄</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Welcome to Gallopi!</h2>", unsafe_allow_html=True)
    
    with st.form("onboard_form"):
        nick = st.text_input("What is your username?", value=st.session_state.nickname)
        
        avatar_idx = st.selectbox(
            "Choose Your Cute Animal Companion Profile Avatar:",
            range(len(ANIMAL_AVATARS)),
            format_func=lambda x: f"{ANIMAL_AVATARS[x][0]} {ANIMAL_AVATARS[x][1]} ({ANIMAL_AVATARS[x][2]})"
        )
        
        focus = st.multiselect("Select Your Primary Skill Vectors:", [f[0] for f in FOCUS_OPTIONS])
        
        if st.form_submit_button("Launch Journey Path 🚀"):
            if nick.strip():
                st.session_state.nickname = nick
                st.session_state.avatar = ANIMAL_AVATARS[avatar_idx][0]
                st.session_state.avatar_label = ANIMAL_AVATARS[avatar_idx][1]
                st.session_state.focus_areas = focus
                st.session_state.onboarded = True
                st.balloons()
                st.rerun()
            else:
                st.warning("Please specify an active account username profile option.")
else:
    topbar()
    
    xp_val = st.session_state.xp
    progress_html = f"""
    <div class="g-card">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px">
            <span style="font-weight:700;font-size:13px;color:#f7f9fc;">Daily XP Goal</span>
            <span style="color:#58cc02;font-weight:800;font-size:13px">{xp_val} / 150 XP</span>
        </div>
        <div style="background:#203038;border-radius:50px;height:12px;overflow:hidden">
            <div style="background:linear-gradient(90deg,#58cc02,#7be800);width:{min(100, int((xp_val/150)*100))}.0%;height:100%;border-radius:50px;"></div>
        </div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align:center; color:#1cb0f6;'>🗺️ Learning Map</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        for lvl in LEVELS:
            btn_id = f"lvl_btn_{lvl['id']}"
            if st.button(f"{lvl['icon']} {lvl['title']} (Start)", key=btn_id, use_container_width=True):
                st.session_state.active_scenario = lvl["id"]
                st.session_state.arena_q_index = 0
                st.session_state.arena_answers = []
                st.session_state.arena_show_results = False
                st.session_state.arena_scores = None
                st.switch_page("pages/2_Practice_Arena.py")