import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from utils.state import init_state
from utils.helpers import inject_css, topbar

st.set_page_config(page_title="Profile · Gallopi", page_icon="👤",
                   layout="centered", initial_sidebar_state="collapsed")
init_state()
inject_css()
topbar(back_href="/")

nick         = st.session_state.nickname or "Learner"
avatar       = st.session_state.avatar or "🦄"
avatar_label = st.session_state.avatar_label or "Unicorn"
focus        = st.session_state.focus_areas
xp           = st.session_state.xp
streak       = st.session_state.streak
done         = st.session_state.completed_levels
energy       = st.session_state.energy
history      = st.session_state.session_history
friends      = st.session_state.friends

RANKS = [
    (0,"Nervous Newcomer 😰"),(200,"Confident Talker 💬"),
    (500,"Rising Star 🌟"),(1000,"Communication Pro 💼"),
    (2000,"Pitch Master 🎯"),(3500,"Boardroom Legend 👑"),
]
current_rank = RANKS[0][1]
next_rank_xp = RANKS[1][0]
for t, rname in RANKS:
    if xp >= t:
        current_rank = rname
for t, _ in RANKS:
    if xp < t:
        next_rank_xp = t
        break
else:
    next_rank_xp = RANKS[-1][0]

prev_t = max(t for t, _ in RANKS if t <= xp)
rank_pct = min(100, int((xp - prev_t) / max(1, next_rank_xp - prev_t) * 100))

focus_pills = "".join(
    f'<span style="background:#a346ff22;border:1px solid #a346ff44;color:#a346ff;'
    f'padding:4px 12px;border-radius:50px;font-size:11px;font-weight:700;margin:3px;'
    f'display:inline-block;">{f}</span>' for f in focus
)

# Profile hero card with animated unicorn
st.markdown(f"""
<div style="background:linear-gradient(160deg,#131f24,#0d1e1a);
            border:2px solid #203038;border-radius:24px;
            margin:0 16px 16px;padding:24px 20px;text-align:center;">
    <div class="unicorn-mascot">{avatar}</div>
    <div style="font-size:26px;font-weight:900;margin-top:4px;">{nick}</div>
    <div style="font-size:13px;color:#a346ff;font-weight:700;margin-top:2px;">{avatar_label}</div>
    <div style="font-size:13px;color:#58cc02;font-weight:700;margin-top:2px;">{current_rank}</div>
    <div style="margin:12px 0;display:flex;flex-wrap:wrap;justify-content:center;">
        {focus_pills if focus_pills else '<span style="color:#4a6572;font-size:13px;">No focus areas set</span>'}
    </div>
    <div style="margin-top:12px;">
        <div style="display:flex;justify-content:space-between;font-size:11px;
                    font-weight:700;color:#4a6572;margin-bottom:6px;">
            <span>{xp:,} XP</span>
            <span>{max(0,next_rank_xp-xp):,} to next rank</span>
        </div>
        <div style="background:#203038;border-radius:50px;height:12px;overflow:hidden;">
            <div style="background:linear-gradient(90deg,#58cc02,#7be800);
                        width:{rank_pct}%;height:100%;border-radius:50px;
                        box-shadow:0 0 10px #58cc0244;"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats grid
st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 10px;">📊 Your Stats</div>', unsafe_allow_html=True)
stats = [
    ("🔥", str(streak), "Day Streak", "#ff9600"),
    ("💎", f"{xp:,}", "Total XP", "#1cb0f6"),
    ("✅", str(len(done)), "Levels Done", "#58cc02"),
    ("⚡", f"{energy}/5", "Energy", "#a346ff"),
]
cols = st.columns(2)
for i, (icon, val, label, color) in enumerate(stats):
    with cols[i % 2]:
        st.markdown(f"""
<div style="background:#131f24;border:2px solid #203038;border-radius:18px;
            padding:16px 10px;text-align:center;margin-bottom:10px;">
    <div style="font-size:24px;margin-bottom:4px;">{icon}</div>
    <div style="font-size:26px;font-weight:900;color:{color};">{val}</div>
    <div style="font-size:11px;color:#4a6572;font-weight:700;">{label}</div>
</div>
""", unsafe_allow_html=True)

# Weekly activity heatmap
st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 10px;">📈 This Week\'s Activity</div>', unsafe_allow_html=True)
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
activity = [3, 1, 2, 3, 3, 0, 1]
heat_colors = ["#1c2e38","#1a4a20","#2d7a28","#58cc02"]
heights = [18, 30, 46, 62]
heat_html = '<div style="display:flex;gap:6px;align-items:flex-end;justify-content:center;margin-bottom:8px;padding:0 8px;">'
for day, act in zip(days, activity):
    c = heat_colors[act]
    h = heights[act]
    glow = f"box-shadow:0 0 10px {c}88;" if act == 3 else ""
    heat_html += f"""
<div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;">
    <div style="width:100%;height:{h}px;background:{c};border-radius:6px;{glow}"></div>
    <div style="font-size:9px;color:#4a6572;font-weight:700;">{day}</div>
</div>"""
heat_html += '</div>'
st.markdown(f"""
<div style="background:#131f24;border:2px solid #203038;border-radius:18px;
            padding:16px;margin:0 16px 16px;">
    {heat_html}
    <div style="text-align:center;font-size:11px;color:#4a6572;font-weight:600;">
        Sessions per day this week
    </div>
</div>
""", unsafe_allow_html=True)

# Session history
st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 10px;">📅 Recent Sessions</div>', unsafe_allow_html=True)
for session in history:
    score_color = "#58cc02" if session["score"] >= 80 else "#ff9600"
    st.markdown(f"""
<div style="background:#131f24;border:2px solid #203038;border-radius:16px;
            padding:14px 16px;margin:0 16px 8px;
            display:flex;align-items:center;gap:12px;">
    <div style="font-size:30px;">{session['icon']}</div>
    <div style="flex:1;">
        <div style="font-weight:800;font-size:14px;">{session['level']}</div>
        <div style="font-size:11px;color:#4a6572;font-weight:600;margin-top:2px;">{session['date']}</div>
    </div>
    <div style="text-align:right;">
        <div style="font-weight:900;color:{score_color};font-size:16px;">{session['score']}%</div>
        <div style="font-size:11px;color:#1cb0f6;font-weight:700;">+{session['xp']} XP</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Friends
st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 10px;margin-top:8px;">👥 Friends</div>', unsafe_allow_html=True)
for f in friends:
    st.markdown(f"""
<div style="background:#131f24;border:2px solid #203038;border-radius:14px;
            padding:12px 16px;margin:0 16px 8px;
            display:flex;align-items:center;justify-content:space-between;">
    <div style="font-weight:700;font-size:14px;">{f}</div>
    <div style="font-size:11px;color:#58cc02;font-weight:700;">✓ Friend</div>
</div>
""", unsafe_allow_html=True)

# Add friend
st.markdown('<div style="padding:0 16px;margin-top:4px;">', unsafe_allow_html=True)
new_friend = st.text_input("Add friend by nickname", placeholder="Enter their Gallopi username...",
                           label_visibility="collapsed")
if st.button("➕ Add Friend", use_container_width=True):
    if new_friend.strip():
        if new_friend.strip() not in st.session_state.friends:
            st.session_state.friends.append(new_friend.strip())
        st.success(f"Friend request sent to {new_friend.strip()}! 🎉")
    else:
        st.warning("Enter a username to add a friend!")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("🏅 View Badges", use_container_width=True):
        st.switch_page("pages/4_Badges.py")
with col2:
    if st.button("🎙️ Practice", use_container_width=True):
        st.session_state.active_scenario = st.session_state.current_level
        st.session_state.arena_q_index = 0
        st.session_state.arena_answers = []
        st.session_state.arena_show_results = False
        st.session_state.arena_scores = None
        st.switch_page("pages/2_Practice_Arena.py")

with st.expander("⚠️ Danger Zone — Reset Progress"):
    st.markdown('<p style="color:#ff7b7b;font-size:13px;font-weight:600;padding:0 4px;">This resets all progress and restarts onboarding.</p>', unsafe_allow_html=True)
    if st.button("🗑️ Reset Everything", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.switch_page("Home.py")

if st.button("← Back to Path", use_container_width=True):
    st.switch_page("Home.py")

st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)
