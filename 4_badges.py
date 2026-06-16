import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from utils.state import init_state
from utils.helpers import inject_css, topbar

st.set_page_config(page_title="Badges · Gallopi", page_icon="🏅",
                   layout="centered", initial_sidebar_state="collapsed")
init_state()
inject_css()
topbar(back_href="/")

completed = st.session_state.completed_levels
xp        = st.session_state.xp
streak    = st.session_state.streak

BADGES = [
    {"icon":"🗣️","name":"First Words",     "desc":"Complete your first practice",         "color":"#58cc02","shadow":"#46a302","earned": len(completed) >= 1, "category":"Milestone"},
    {"icon":"🔥","name":"On Fire",          "desc":"Maintain a 7-day streak",              "color":"#ff9600","shadow":"#e58500","earned": streak >= 7,          "category":"Streak"},
    {"icon":"👂","name":"Deep Listener",    "desc":"Score 80%+ on Active Listening",       "color":"#1cb0f6","shadow":"#1899d6","earned": len(completed) >= 2,  "category":"Skill"},
    {"icon":"📖","name":"Storyteller",      "desc":"Complete the Storytelling level",      "color":"#1cb0f6","shadow":"#1899d6","earned": len(completed) >= 3,  "category":"Track"},
    {"icon":"🚀","name":"Pitch Perfect",    "desc":"Score 90%+ on Elevator Pitch",        "color":"#ff9600","shadow":"#e58500","earned": False,                 "category":"Skill"},
    {"icon":"🏆","name":"Podium Star",      "desc":"Reach Top 3 on the leaderboard",      "color":"#ffd700","shadow":"#e8b400","earned": False,                 "category":"Social"},
    {"icon":"🎙️","name":"Stage Ready",      "desc":"Complete the Public Speaking track",   "color":"#a346ff","shadow":"#8238cc","earned": False,                 "category":"Track"},
    {"icon":"⚡","name":"Speed Talker",      "desc":"Complete a level in under 2 minutes", "color":"#ff9600","shadow":"#e58500","earned": False,                 "category":"Skill"},
    {"icon":"💎","name":"Gem Collector",    "desc":"Earn 5,000 total XP",                 "color":"#1cb0f6","shadow":"#1899d6","earned": xp >= 5000,            "category":"Milestone"},
    {"icon":"👑","name":"Boardroom Master", "desc":"Complete all 8 levels",               "color":"#ffd700","shadow":"#e8b400","earned": len(completed) >= 8,  "category":"Milestone"},
    {"icon":"🌟","name":"Perfect Score",    "desc":"Get 95%+ on any level",               "color":"#58cc02","shadow":"#46a302","earned": False,                 "category":"Skill"},
    {"icon":"🤝","name":"Team Player",      "desc":"Invite 3 friends to Gallopi",         "color":"#a346ff","shadow":"#8238cc","earned": False,                 "category":"Social"},
]

earned_count = sum(1 for b in BADGES if b["earned"])

st.markdown(f"""
<div style="padding:16px 16px 8px;">
    <div style="font-size:24px;font-weight:900;margin-bottom:4px;">🏅 Badge Collection</div>
    <div style="font-size:13px;color:#4a6572;font-weight:600;">{earned_count} of {len(BADGES)} badges earned</div>
</div>

<div style="background:#131f24;border:2px solid #a346ff;border-radius:20px;
            padding:16px;margin:0 16px 20px;text-align:center;">
    <div style="font-size:40px;font-weight:900;color:#a346ff;">{earned_count}</div>
    <div style="font-size:12px;color:#4a6572;font-weight:700;margin-bottom:10px;">
        OF {len(BADGES)} BADGES EARNED
    </div>
    <div style="background:#203038;border-radius:50px;height:12px;overflow:hidden;">
        <div style="background:linear-gradient(90deg,#a346ff,#c87aff);
                    width:{int(earned_count/len(BADGES)*100)}%;
                    height:100%;border-radius:50px;
                    box-shadow:0 0 12px #a346ff55;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Earned badges
earned_list = [b for b in BADGES if b["earned"]]
locked_list = [b for b in BADGES if not b["earned"]]

if earned_list:
    st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 12px;">✅ Earned Badges</div>', unsafe_allow_html=True)
    for row_start in range(0, len(earned_list), 3):
        row = earned_list[row_start:row_start+3]
        cols = st.columns(3)
        for ci, badge in enumerate(row):
            with cols[ci]:
                st.markdown(f"""
<div style="display:flex;flex-direction:column;align-items:center;gap:6px;
            padding:12px 4px;text-align:center;">
    <div style="width:68px;height:68px;border-radius:50%;
                background:radial-gradient(circle at 35% 35%,{badge['color']}dd,{badge['shadow']});
                display:flex;align-items:center;justify-content:center;font-size:28px;
                box-shadow:0 4px 0 {badge['shadow']},0 0 20px {badge['color']}55;
                border:3px solid {badge['color']};">
        {badge['icon']}
    </div>
    <div style="font-size:11px;font-weight:800;color:#e8f4f8;line-height:1.3;">{badge['name']}</div>
    <div style="font-size:9px;color:#4a6572;font-weight:600;">{badge['category']}</div>
</div>
""", unsafe_allow_html=True)

if locked_list:
    st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 12px;margin-top:12px;">🔒 Locked Badges</div>', unsafe_allow_html=True)
    for row_start in range(0, len(locked_list), 3):
        row = locked_list[row_start:row_start+3]
        cols = st.columns(3)
        for ci, badge in enumerate(row):
            with cols[ci]:
                st.markdown(f"""
<div style="display:flex;flex-direction:column;align-items:center;gap:6px;
            padding:12px 4px;text-align:center;">
    <div style="width:68px;height:68px;border-radius:50%;
                background:{badge['color']}22;
                display:flex;align-items:center;justify-content:center;font-size:28px;
                border:3px solid #203038;filter:grayscale(100%);opacity:0.38;">
        {badge['icon']}
    </div>
    <div style="font-size:11px;font-weight:800;color:#3c5566;line-height:1.3;">{badge['name']}</div>
    <div style="font-size:9px;color:#2c3e45;font-weight:600;line-height:1.3;max-width:72px;">{badge['desc']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
if st.button("🎙️ Earn More Badges — Practice Now!", use_container_width=True):
    st.session_state.active_scenario = st.session_state.current_level
    st.session_state.arena_q_index = 0
    st.session_state.arena_answers = []
    st.session_state.arena_show_results = False
    st.session_state.arena_scores = None
    st.switch_page("pages/2_Practice_Arena.py")

if st.button("← Back to Path", use_container_width=True):
    st.switch_page("Home.py")

st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)