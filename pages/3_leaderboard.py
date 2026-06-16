import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from utils.state import init_state
from utils.helpers import inject_css, topbar

st.set_page_config(page_title="Leaderboard · Gallopi", page_icon="🏆",
                   layout="centered", initial_sidebar_state="collapsed")
init_state()
inject_css()
topbar(back_href="/")

nick   = st.session_state.nickname or "You"
avatar = st.session_state.avatar or "🦄"
user_xp= st.session_state.xp
streak = st.session_state.streak

ALL_PLAYERS = [
    {"name":"PitchKing","avatar":"🦁","xp":3450,"streak":21,"level":8},
    {"name":"SarahS","avatar":"🦊","xp":2180,"streak":14,"level":7},
    {"name":"AlexT","avatar":"🐼","xp":1920,"streak":9,"level":6},
    {"name":nick,"avatar":avatar,"xp":user_xp,"streak":streak,"level":4},
    {"name":"DominicV","avatar":"🐨","xp":980,"streak":5,"level":4},
    {"name":"MiaK","avatar":"🦥","xp":740,"streak":3,"level":3},
    {"name":"JorgeM","avatar":"🦊","xp":620,"streak":2,"level":3},
    {"name":"PriyaR","avatar":"🦄","xp":440,"streak":1,"level":2},
]
ALL_PLAYERS.sort(key=lambda p: p["xp"], reverse=True)
p1,p2,p3 = ALL_PLAYERS[0],ALL_PLAYERS[1],ALL_PLAYERS[2]

st.markdown("""
<div style="padding:16px 16px 8px;">
    <div style="font-size:24px;font-weight:900;margin-bottom:4px;">🏆 Leaderboard</div>
    <div style="font-size:13px;color:#4a6572;font-weight:600;">Top communicators this week</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:linear-gradient(135deg,#0f1e14,#0b141a);
            border:2px solid #ffd70044;border-radius:24px;
            margin:0 16px 20px;padding:24px 16px 0;">
    <div style="text-align:center;margin-bottom:16px;">
        <div style="font-size:11px;font-weight:800;color:#ffd700;letter-spacing:2.5px;">
            ✦ THIS WEEK'S CHAMPIONS ✦
        </div>
    </div>
    <div style="display:flex;align-items:flex-end;justify-content:center;gap:6px;">

        <div style="display:flex;flex-direction:column;align-items:center;gap:3px;flex:1;">
            <div style="font-size:28px;">{p2['avatar']}</div>
            <div style="font-weight:800;font-size:12px;text-align:center;">{p2['name']}</div>
            <div style="font-size:10px;color:#ff9600;font-weight:700;">🔥{p2['streak']}</div>
            <div style="background:linear-gradient(180deg,#6a7f8a,#4a5f6a);
                        width:100%;min-height:88px;border-radius:14px 14px 0 0;
                        display:flex;flex-direction:column;align-items:center;
                        justify-content:flex-end;padding:10px;
                        box-shadow:0 0 20px rgba(106,127,138,0.4);">
                <div style="font-size:22px;">🥈</div>
                <div style="font-weight:900;font-size:20px;color:#fff;">#2</div>
                <div style="font-size:11px;font-weight:700;color:#ffffffaa;">{p2['xp']:,} XP</div>
            </div>
        </div>

        <div style="display:flex;flex-direction:column;align-items:center;gap:3px;flex:1.2;">
            <div style="font-size:14px;line-height:1;">👑</div>
            <div style="font-size:34px;">{p1['avatar']}</div>
            <div style="font-weight:900;font-size:13px;text-align:center;color:#ffd700;">{p1['name']}</div>
            <div style="font-size:10px;color:#ff9600;font-weight:700;">🔥{p1['streak']}</div>
            <div style="background:linear-gradient(180deg,#ffd700,#d4a000);
                        width:100%;min-height:118px;border-radius:14px 14px 0 0;
                        display:flex;flex-direction:column;align-items:center;
                        justify-content:flex-end;padding:10px;
                        box-shadow:0 0 30px rgba(255,215,0,0.45);">
                <div style="font-size:26px;">🥇</div>
                <div style="font-weight:900;font-size:24px;color:#0b141a;">#1</div>
                <div style="font-size:11px;font-weight:800;color:#0b141a99;">{p1['xp']:,} XP</div>
            </div>
        </div>

        <div style="display:flex;flex-direction:column;align-items:center;gap:3px;flex:1;">
            <div style="font-size:28px;">{p3['avatar']}</div>
            <div style="font-weight:800;font-size:12px;text-align:center;">{p3['name']}</div>
            <div style="font-size:10px;color:#ff9600;font-weight:700;">🔥{p3['streak']}</div>
            <div style="background:linear-gradient(180deg,#cd7f32,#9a5f22);
                        width:100%;min-height:70px;border-radius:14px 14px 0 0;
                        display:flex;flex-direction:column;align-items:center;
                        justify-content:flex-end;padding:10px;
                        box-shadow:0 0 20px rgba(205,127,50,0.4);">
                <div style="font-size:20px;">🥉</div>
                <div style="font-weight:900;font-size:18px;color:#fff;">#3</div>
                <div style="font-size:11px;font-weight:700;color:#ffffffaa;">{p3['xp']:,} XP</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 12px;">📋 Full Rankings</div>', unsafe_allow_html=True)

for rank, player in enumerate(ALL_PLAYERS, 1):
    is_you = player["name"] == nick
    bg = "#1a2f3a" if is_you else "#131f24"
    border = "#1cb0f6" if is_you else "#203038"
    r_icons = {1:"🥇",2:"🥈",3:"🥉"}
    r_colors = {1:"#ffd700",2:"#8a9baa",3:"#cd7f32"}
    rd = r_icons.get(rank, f"#{rank}")
    rc = r_colors.get(rank, "#4a6572")
    you_badge = '<span style="font-size:10px;background:#1cb0f6;color:#fff;padding:2px 8px;border-radius:50px;margin-left:6px;">YOU</span>' if is_you else ""
    st.markdown(f"""
<div style="background:{bg};border:2px solid {border};border-radius:16px;
            padding:12px 16px;margin:0 16px 8px;
            display:flex;align-items:center;gap:12px;">
    <div style="font-size:{'18px' if rank<=3 else '14px'};font-weight:900;
                color:{rc};min-width:30px;text-align:center;">{rd}</div>
    <div style="font-size:26px;">{player['avatar']}</div>
    <div style="flex:1;">
        <div style="font-weight:800;font-size:14px;">{player['name']}{you_badge}</div>
        <div style="font-size:11px;color:#4a6572;font-weight:600;">
            Lv.{player['level']} · 🔥{player['streak']} streak
        </div>
    </div>
    <div style="text-align:right;">
        <div style="font-weight:900;color:#1cb0f6;font-size:14px;">💎 {player['xp']:,}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(135deg,#131f24,#1a1030);
            border:2px solid #a346ff44;border-radius:20px;
            padding:18px;margin:16px 16px 32px;text-align:center;">
    <div style="font-size:32px;margin-bottom:8px;">🚀</div>
    <div style="font-weight:900;font-size:16px;margin-bottom:6px;">Keep Climbing!</div>
    <div style="font-size:13px;color:#4a6572;font-weight:600;">
        Complete daily practice sessions to earn XP and rise to #1
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("🎙️ Practice Now", use_container_width=True):
    st.session_state.active_scenario = st.session_state.current_level
    st.session_state.arena_q_index = 0
    st.session_state.arena_answers = []
    st.session_state.arena_show_results = False
    st.session_state.arena_scores = None
    st.switch_page("pages/2_Practice_Arena.py")

if st.button("← Back to Path", use_container_width=True):
    st.switch_page("Home.py")

st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)
