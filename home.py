import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from utils.state import init_state
from utils.helpers import inject_css, topbar, bottom_nav
from utils.content import ANIMAL_AVATARS, FOCUS_OPTIONS, LEVELS, LEVELS_BY_ID

st.set_page_config(
    page_title="Gallopi 🦄",
    page_icon="🦄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

init_state()
inject_css()

# ═══════════════════════════════════════════════════════════
# ONBOARDING
# ═══════════════════════════════════════════════════════════
def onboarding():
    step = st.session_state.onboard_step

    # Progress dots
    dots_html = '<div class="step-dots">'
    for i in range(1, 5):
        cls = "dot done" if i < step else ("dot active" if i == step else "dot")
        dots_html += f'<div class="{cls}"></div>'
    dots_html += '</div>'

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown(dots_html, unsafe_allow_html=True)

    # ── Step 1: Hook ─────────────────────────────────────
    if step == 1:
        st.markdown("""
<div style="text-align:center;padding:10px 16px 0;">
    <div class="unicorn-mascot">🦄</div>
    <div style="background:#1cb0f6;border-radius:20px;padding:16px 20px;
                color:#fff;font-weight:700;font-size:17px;line-height:1.5;
                margin:16px 0 10px;box-shadow:0 4px 0 #1899d6;">
        Neigh! 🦄 I'm Gallopi — your personal<br>
        communication coach!<br>
        <span style="font-size:13px;opacity:0.9;">
          Let's get you boardroom-ready. It'll be fun!
        </span>
    </div>
    <div style="font-size:13px;color:#4a6572;font-weight:600;margin-top:8px;">
        Join 50,000+ professionals levelling up their skills
    </div>
</div>
""", unsafe_allow_html=True)
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        if st.button("🚀 Let's GO!", use_container_width=True):
            st.session_state.onboard_step = 2
            st.rerun()

    # ── Step 2: Nickname ──────────────────────────────────
    elif step == 2:
        st.markdown("""
<div style="text-align:center;padding:8px 0 16px;">
    <div style="font-size:48px;margin-bottom:8px;">✏️</div>
    <div style="font-size:22px;font-weight:900;margin-bottom:6px;">What should I call you?</div>
    <div style="font-size:13px;color:#4a6572;font-weight:600;">
        Pick a name that'll look great on the leaderboard!
    </div>
</div>
""", unsafe_allow_html=True)
        nick = st.text_input("Your nickname", placeholder="e.g. SpeechWizard99",
                             label_visibility="collapsed")
        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        if st.button("Continue →", use_container_width=True):
            if nick.strip():
                st.session_state.nickname = nick.strip()
                st.session_state.onboard_step = 3
                st.rerun()
            else:
                st.warning("Give yourself a name first! 😄")

    # ── Step 3: Animal Avatar ─────────────────────────────
    elif step == 3:
        st.markdown("""
<div style="text-align:center;padding:8px 0 16px;">
    <div style="font-size:22px;font-weight:900;margin-bottom:6px;">Pick your animal companion!</div>
    <div style="font-size:13px;color:#4a6572;font-weight:600;">
        Your spirit guide for the journey 🌟
    </div>
</div>
""", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, (emoji, label, tagline) in enumerate(ANIMAL_AVATARS):
            with cols[i % 3]:
                is_sel = st.session_state.avatar == emoji
                border_col = "#58cc02" if is_sel else "#203038"
                bg_col = "#0f2a0f" if is_sel else "#131f24"
                shadow = "box-shadow:0 4px 0 #46a302;" if is_sel else ""
                checkmark = '<div style="position:absolute;top:4px;right:4px;background:#58cc02;color:#fff;border-radius:50%;width:18px;height:18px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:900;">✓</div>' if is_sel else ""
                st.markdown(f"""
<div style="background:{bg_col};border:2.5px solid {border_col};border-radius:18px;
            padding:14px 8px;text-align:center;margin-bottom:8px;position:relative;{shadow}">
    {checkmark}
    <div style="font-size:40px;margin-bottom:6px;">{emoji}</div>
    <div style="font-size:12px;font-weight:800;color:#e8f4f8;">{label}</div>
    <div style="font-size:10px;color:#4a6572;margin-top:2px;">{tagline}</div>
</div>
""", unsafe_allow_html=True)
                if st.button(f"Pick {emoji}", key=f"av_{i}", use_container_width=True):
                    st.session_state.avatar = emoji
                    st.session_state.avatar_label = label
                    st.rerun()

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        if st.session_state.avatar:
            if st.button("Continue →", use_container_width=True):
                st.session_state.onboard_step = 4
                st.rerun()
        else:
            st.markdown('<p style="text-align:center;color:#4a6572;font-size:13px;font-weight:600;">Choose a companion above ↑</p>', unsafe_allow_html=True)

    # ── Step 4: Focus Areas ───────────────────────────────
    elif step == 4:
        st.markdown("""
<div style="text-align:center;padding:8px 0 16px;">
    <div style="font-size:22px;font-weight:900;margin-bottom:6px;">What do you want to master?</div>
    <div style="font-size:13px;color:#4a6572;font-weight:600;">Choose all that apply</div>
</div>
""", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, (opt, icon) in enumerate(FOCUS_OPTIONS):
            full_opt = f"{opt} {icon}"
            with cols[i % 2]:
                is_sel = full_opt in st.session_state.focus_areas
                bg = "#0f2a0f" if is_sel else "#131f24"
                border = "#58cc02" if is_sel else "#203038"
                check = "✓ " if is_sel else ""
                st.markdown(f"""
<div style="background:{bg};border:2.5px solid {border};border-radius:16px;
            padding:14px 12px;text-align:center;margin-bottom:8px;">
    <span style="font-size:22px;">{icon}</span>
    <div style="font-size:13px;font-weight:800;margin-top:6px;">{check}{opt}</div>
</div>
""", unsafe_allow_html=True)
                if st.button(f"{icon} {opt}", key=f"focus_{i}", use_container_width=True):
                    if full_opt in st.session_state.focus_areas:
                        st.session_state.focus_areas.remove(full_opt)
                    else:
                        st.session_state.focus_areas.append(full_opt)
                    st.rerun()

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        if st.session_state.focus_areas:
            if st.button("Start Training 🦄 →", use_container_width=True):
                st.session_state.onboarded = True
                st.session_state.current_page = "path"
                st.rerun()
        else:
            st.markdown('<p style="text-align:center;color:#4a6572;font-size:13px;font-weight:600;">Select at least one focus area ↑</p>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PATH VIEW
# ═══════════════════════════════════════════════════════════
PATH_POSITIONS = ["center","right","center","left","center","right","center","left"]

def render_path():
    nick = st.session_state.nickname or "Learner"
    avatar = st.session_state.avatar or "🦄"
    completed = st.session_state.completed_levels
    current = st.session_state.current_level
    xp = st.session_state.xp

    # Welcome header
    st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:16px 16px 8px;margin-top:4px;">
    <div>
        <div style="font-size:12px;color:#4a6572;font-weight:700;">Welcome back,</div>
        <div style="font-size:22px;font-weight:900;">{avatar} {nick}</div>
    </div>
    <div style="background:#131f24;border:2px solid #203038;border-radius:16px;
                padding:10px 16px;text-align:center;">
        <div style="font-size:20px;">⚡</div>
        <div style="font-size:13px;font-weight:800;color:#a346ff;">{st.session_state.energy}/5</div>
    </div>
</div>
""", unsafe_allow_html=True)

    # Daily XP bar
    xp_pct = min(100, int((xp % 100)))
    st.markdown(f"""
<div style="background:#131f24;border:2px solid #203038;border-radius:20px;
            padding:16px;margin:0 16px 16px;">
    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
        <span style="font-weight:700;font-size:13px;">Daily XP Goal</span>
        <span style="color:#58cc02;font-weight:800;font-size:13px;">85 / 100 XP</span>
    </div>
    <div style="background:#203038;border-radius:50px;height:12px;overflow:hidden;">
        <div style="background:linear-gradient(90deg,#58cc02,#7be800);width:85%;
                    height:100%;border-radius:50px;
                    box-shadow:0 0 10px #58cc0255;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 12px;">🗺️ Your Learning Path</div>', unsafe_allow_html=True)

    # Render each level node
    for i, level in enumerate(LEVELS):
        pos = PATH_POSITIONS[i]
        lid = level["id"]

        if lid in completed:
            node_class = "done"
            icon_display = "✓"
            node_bg = "#58cc02"
            node_shadow = "#46a302"
            cursor = "pointer"
        elif lid == current:
            node_class = "active"
            icon_display = level["icon"]
            node_bg = "#1cb0f6"
            node_shadow = "#1899d6"
            cursor = "pointer"
        else:
            node_class = "locked"
            icon_display = "🔒"
            node_bg = "#3c4d55"
            node_shadow = "#2c393f"
            cursor = "not-allowed"

        # Stagger: left col=0, center col=1, right col=2
        c1, c2, c3 = st.columns([1, 1, 1])
        target_col = c1 if pos == "left" else (c3 if pos == "right" else c2)

        # Treasure chest at midpoint
        if i == 3:
            st.markdown("""
<div style="display:flex;flex-direction:column;align-items:center;margin:8px 0 16px;">
    <div style="font-size:52px;animation:float 3s ease-in-out infinite;
                filter:drop-shadow(0 0 16px #ff960088);">🎁</div>
    <div style="font-size:11px;font-weight:800;color:#ff9600;margin-top:6px;">
        ⭐⭐⭐ Checkpoint Reward!
    </div>
    <div style="font-size:10px;color:#4a6572;font-weight:600;margin-top:2px;">
        +200 XP Bonus Chest
    </div>
</div>
<style>
@keyframes float {
    0%,100% { transform:translateY(0); }
    50% { transform:translateY(-10px); }
}
</style>
""", unsafe_allow_html=True)

        with target_col:
            # Clickable completed or active levels
            if lid in completed or lid == current:
                # Show the visual node
                pulse_anim = "animation:pulse-node 1.8s infinite;" if lid == current else ""
                st.markdown(f"""
<style>
@keyframes pulse-node {{
    0%,100% {{ box-shadow:0 5px 0 {node_shadow},0 0 0 0 rgba(28,176,246,0.4); }}
    50% {{ box-shadow:0 5px 0 {node_shadow},0 0 0 14px rgba(28,176,246,0); }}
}}
</style>
<div style="display:flex;flex-direction:column;align-items:center;
            padding:8px 0 2px;gap:4px;">
    <div style="width:78px;height:78px;border-radius:50%;
                background:{node_bg};box-shadow:0 5px 0 {node_shadow};
                display:flex;align-items:center;justify-content:center;
                font-size:28px;font-weight:900;color:#fff;
                cursor:{cursor};{pulse_anim}">
        {icon_display}
    </div>
    <div style="font-size:11px;font-weight:700;color:#4a6572;text-align:center;
                max-width:90px;line-height:1.3;">
        {level['title']}
    </div>
    <div style="font-size:11px;font-weight:800;color:#ff9600;">+{level['xp']} XP</div>
    {"<div style='font-size:10px;font-weight:800;color:#1cb0f6;'>TAP BELOW ↓</div>" if lid == current else ""}
</div>
""", unsafe_allow_html=True)
                # The actual Streamlit button that WORKS
                if lid == current:
                    if st.button(f"▶ Start {level['title']}", key=f"lvl_{lid}", use_container_width=True):
                        st.session_state.active_scenario = lid
                        st.session_state.arena_q_index = 0
                        st.session_state.arena_answers = []
                        st.session_state.arena_show_results = False
                        st.session_state.arena_scores = None
                        st.switch_page("pages/2_Practice_Arena.py")
                elif lid in completed:
                    if st.button(f"↺ Redo {level['title']}", key=f"lvl_{lid}", use_container_width=True):
                        st.session_state.active_scenario = lid
                        st.session_state.arena_q_index = 0
                        st.session_state.arena_answers = []
                        st.session_state.arena_show_results = False
                        st.session_state.arena_scores = None
                        st.switch_page("pages/2_Practice_Arena.py")
            else:
                # Locked — just visual, no button
                st.markdown(f"""
<div style="display:flex;flex-direction:column;align-items:center;
            padding:8px 0 2px;gap:4px;">
    <div style="width:78px;height:78px;border-radius:50%;
                background:{node_bg};box-shadow:0 5px 0 {node_shadow};
                display:flex;align-items:center;justify-content:center;
                font-size:28px;cursor:not-allowed;opacity:0.7;">
        {icon_display}
    </div>
    <div style="font-size:11px;font-weight:700;color:#4a6572;text-align:center;
                max-width:90px;line-height:1.3;">
        {level['title']}
    </div>
    <div style="font-size:11px;font-weight:800;color:#4a6572;">+{level['xp']} XP</div>
</div>
""", unsafe_allow_html=True)

        # Connector line between nodes
        if i < len(LEVELS) - 1:
            st.markdown("""
<div style="display:flex;justify-content:center;margin:0;">
    <div style="width:3px;height:28px;
                background:repeating-linear-gradient(
                    180deg,#203038 0,#203038 6px,transparent 6px,transparent 12px
                );border-radius:2px;"></div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# QUESTS VIEW
# ═══════════════════════════════════════════════════════════
def render_quests():
    st.markdown("""
<div style="padding:16px 16px 8px;">
    <div style="font-size:22px;font-weight:900;margin-bottom:4px;">🏅 Daily Quests</div>
    <div style="font-size:13px;color:#4a6572;font-weight:600;">Resets in 14h 32m</div>
</div>
""", unsafe_allow_html=True)

    quests = [
        {"title":"Warm-Up Speaker","desc":"Complete 1 practice session today",
         "reward":20,"progress":1,"total":1,"done":True},
        {"title":"Pitch Perfect","desc":"Score 80%+ on any level",
         "reward":35,"progress":0,"total":1,"done":False},
        {"title":"Streak Keeper","desc":"Maintain your 7-day streak",
         "reward":50,"progress":7,"total":7,"done":True},
        {"title":"Word Wizard","desc":"Use 5 power phrases in responses",
         "reward":25,"progress":3,"total":5,"done":False},
    ]

    for q in quests:
        pct = min(100, int(q["progress"] / q["total"] * 100))
        done_border = "border-color:#58cc02;" if q["done"] else ""
        bar_color = "#58cc02" if q["done"] else "#a346ff"
        icon = "✅" if q["done"] else "💎"
        badge_text = "✅ Done" if q["done"] else f"{q['progress']}/{q['total']}"
        st.markdown(f"""
<div style="background:#131f24;border:2px solid #203038;{done_border}border-radius:20px;
            padding:16px;margin:0 16px 10px;">
    <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px;">
        <div style="flex:1;">
            <div style="font-weight:800;font-size:15px;">{q['title']}</div>
            <div style="font-size:12px;color:#4a6572;font-weight:600;margin-top:2px;">{q['desc']}</div>
        </div>
        <div style="text-align:center;min-width:56px;">
            <div style="font-size:20px;">{icon}</div>
            <div style="font-size:12px;font-weight:800;color:#1cb0f6;">+{q['reward']} XP</div>
        </div>
    </div>
    <div style="background:#203038;border-radius:50px;height:10px;overflow:hidden;margin-bottom:4px;">
        <div style="background:{bar_color};width:{pct}%;height:100%;border-radius:50px;"></div>
    </div>
    <div style="font-size:11px;color:#4a6572;font-weight:700;">{badge_text}</div>
</div>
""", unsafe_allow_html=True)

    # Weekly challenge
    st.markdown("""
<div style="padding:0 16px;">
    <div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;
                letter-spacing:1.8px;margin:20px 0 12px;">🔥 Weekly Challenge</div>
    <div style="background:linear-gradient(135deg,#131f24,#1a1030);
                border:2px solid #a346ff;border-radius:20px;padding:18px;">
        <div style="display:flex;gap:14px;align-items:center;">
            <div style="font-size:48px;">🏆</div>
            <div>
                <div style="font-weight:900;font-size:16px;">Master Communicator</div>
                <div style="font-size:13px;color:#4a6572;font-weight:600;">
                    Complete 5 sessions this week
                </div>
                <div style="font-size:13px;color:#a346ff;font-weight:800;margin-top:4px;">
                    3/5 done · +200 XP reward
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# LEADERBOARD VIEW
# ═══════════════════════════════════════════════════════════
def render_leaderboard():
    nick = st.session_state.nickname or "You"
    avatar = st.session_state.avatar or "🦄"
    user_xp = st.session_state.xp
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

    st.markdown(f"""
<div style="padding:16px 16px 8px;">
    <div style="font-size:22px;font-weight:900;margin-bottom:4px;">🏆 Leaderboard</div>
    <div style="font-size:13px;color:#4a6572;font-weight:600;">Top communicators this week</div>
</div>

<div style="background:linear-gradient(135deg,#0f1e14,#0b141a);
            border:2px solid #ffd70044;border-radius:20px;
            margin:0 16px 20px;padding:20px 16px;">
    <div style="text-align:center;margin-bottom:16px;">
        <div style="font-size:12px;font-weight:800;color:#ffd700;letter-spacing:2px;">
            THIS WEEK'S CHAMPIONS
        </div>
    </div>
    <div style="display:flex;align-items:flex-end;justify-content:center;gap:8px;">

        <!-- 2nd Place -->
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;">
            <div style="font-size:30px;">{p2['avatar']}</div>
            <div style="font-weight:800;font-size:12px;text-align:center;">{p2['name']}</div>
            <div style="font-size:10px;color:#ff9600;font-weight:700;">🔥{p2['streak']}</div>
            <div style="background:linear-gradient(180deg,#7a8f9a,#5a6f7a);
                        width:100%;min-height:90px;border-radius:14px 14px 0 0;
                        display:flex;flex-direction:column;align-items:center;
                        justify-content:flex-end;padding:10px;
                        box-shadow:0 0 20px rgba(138,159,170,0.3);">
                <div style="font-size:24px;">🥈</div>
                <div style="font-weight:900;font-size:22px;color:#fff;">#2</div>
                <div style="font-size:11px;font-weight:700;color:#ffffffaa;">{p2['xp']:,} XP</div>
            </div>
        </div>

        <!-- 1st Place -->
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1.1;">
            <div style="font-size:13px;line-height:1;">👑</div>
            <div style="font-size:36px;">{p1['avatar']}</div>
            <div style="font-weight:900;font-size:13px;text-align:center;color:#ffd700;">{p1['name']}</div>
            <div style="font-size:10px;color:#ff9600;font-weight:700;">🔥{p1['streak']}</div>
            <div style="background:linear-gradient(180deg,#ffd700,#e8a000);
                        width:100%;min-height:120px;border-radius:14px 14px 0 0;
                        display:flex;flex-direction:column;align-items:center;
                        justify-content:flex-end;padding:10px;
                        box-shadow:0 0 30px rgba(255,215,0,0.4);">
                <div style="font-size:28px;">🥇</div>
                <div style="font-weight:900;font-size:24px;color:#0b141a;">#1</div>
                <div style="font-size:11px;font-weight:800;color:#0b141a99;">{p1['xp']:,} XP</div>
            </div>
        </div>

        <!-- 3rd Place -->
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;">
            <div style="font-size:30px;">{p3['avatar']}</div>
            <div style="font-weight:800;font-size:12px;text-align:center;">{p3['name']}</div>
            <div style="font-size:10px;color:#ff9600;font-weight:700;">🔥{p3['streak']}</div>
            <div style="background:linear-gradient(180deg,#cd7f32,#a06020);
                        width:100%;min-height:72px;border-radius:14px 14px 0 0;
                        display:flex;flex-direction:column;align-items:center;
                        justify-content:flex-end;padding:10px;
                        box-shadow:0 0 20px rgba(205,127,50,0.3);">
                <div style="font-size:20px;">🥉</div>
                <div style="font-weight:900;font-size:20px;color:#fff;">#3</div>
                <div style="font-size:11px;font-weight:700;color:#ffffffaa;">{p3['xp']:,} XP</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 10px;">📋 Full Rankings</div>', unsafe_allow_html=True)

    for rank, player in enumerate(ALL_PLAYERS, 1):
        is_you = player["name"] == nick
        bg = "#1a2f3a" if is_you else "#131f24"
        border = "#1cb0f6" if is_you else "#203038"
        rank_icons = {1:"🥇",2:"🥈",3:"🥉"}
        rank_colors = {1:"#ffd700",2:"#8a9baa",3:"#cd7f32"}
        rank_d = rank_icons.get(rank, f"#{rank}")
        rank_c = rank_colors.get(rank, "#4a6572")
        you_badge = '<span style="font-size:10px;background:#1cb0f6;color:#fff;padding:2px 8px;border-radius:50px;margin-left:6px;">YOU</span>' if is_you else ""
        st.markdown(f"""
<div style="background:{bg};border:2px solid {border};border-radius:16px;
            padding:14px 16px;margin:0 16px 8px;
            display:flex;align-items:center;gap:12px;">
    <div style="font-size:{'20px' if rank<=3 else '14px'};font-weight:900;
                color:{rank_c};min-width:32px;text-align:center;">{rank_d}</div>
    <div style="font-size:28px;">{player['avatar']}</div>
    <div style="flex:1;">
        <div style="font-weight:800;font-size:14px;">{player['name']}{you_badge}</div>
        <div style="font-size:11px;color:#4a6572;font-weight:600;">
            Level {player['level']} · 🔥{player['streak']}
        </div>
    </div>
    <div style="font-weight:900;color:#1cb0f6;font-size:14px;">💎 {player['xp']:,}</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PROFILE VIEW
# ═══════════════════════════════════════════════════════════
def render_profile():
    nick = st.session_state.nickname or "Learner"
    avatar = st.session_state.avatar or "🦄"
    avatar_label = st.session_state.avatar_label or "Unicorn"
    focus = st.session_state.focus_areas
    xp = st.session_state.xp
    streak = st.session_state.streak
    done = st.session_state.completed_levels
    energy = st.session_state.energy

    RANKS = [
        (0,"Nervous Newcomer 😰"),(200,"Confident Talker 💬"),
        (500,"Rising Star 🌟"),(1000,"Communication Pro 💼"),
        (2000,"Pitch Master 🎯"),(3500,"Boardroom Legend 👑"),
    ]
    current_rank = RANKS[0][1]
    next_rank_xp = RANKS[1][0]
    for threshold, rname in RANKS:
        if xp >= threshold:
            current_rank = rname
    for t, _ in RANKS:
        if xp < t:
            next_rank_xp = t
            break
    else:
        next_rank_xp = RANKS[-1][0]

    prev_t = max(t for t,_ in RANKS if t <= xp)
    rank_pct = min(100, int((xp - prev_t) / max(1, next_rank_xp - prev_t) * 100))

    focus_pills = "".join(
        f'<span style="background:#a346ff22;border:1px solid #a346ff44;'
        f'color:#a346ff;padding:4px 12px;border-radius:50px;'
        f'font-size:11px;font-weight:700;margin:2px;">{f}</span>'
        for f in focus
    )

    st.markdown(f"""
<div style="background:linear-gradient(160deg,#131f24,#0d1e1a);
            border:2px solid #203038;border-radius:20px;
            margin:16px 16px 14px;padding:24px 20px;text-align:center;">
    <div class="unicorn-small">{avatar}</div>
    <div style="font-size:26px;font-weight:900;margin-top:4px;">{nick}</div>
    <div style="font-size:13px;color:#a346ff;font-weight:700;margin-top:2px;">{avatar_label}</div>
    <div style="font-size:13px;color:#58cc02;font-weight:700;margin-top:2px;">{current_rank}</div>
    <div style="margin:12px 0 6px;display:flex;flex-wrap:wrap;justify-content:center;gap:4px;">
        {focus_pills}
    </div>
    <div style="margin-top:14px;">
        <div style="display:flex;justify-content:space-between;
                    font-size:11px;font-weight:700;color:#4a6572;margin-bottom:6px;">
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

    # Reset button
    st.markdown('<div style="padding:0 16px;margin-top:8px;">', unsafe_allow_html=True)
    if st.button("🗑️ Reset & Restart Onboarding", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════
if not st.session_state.onboarded:
    topbar()
    onboarding()
else:
    topbar()
    page = st.session_state.current_page
    if page == "path":
        render_path()
    elif page == "quests":
        render_quests()
    elif page == "leaderboard":
        render_leaderboard()
    elif page == "profile":
        render_profile()
    bottom_nav()
