import streamlit as st

DEFAULTS = {
    "onboarded": False,
    "onboard_step": 1,
    "nickname": "",
    "avatar": "🦄",
    "avatar_label": "Unicorn",
    "focus_areas": [],
    "current_page": "path",
    "streak": 7,
    "xp": 1240,
    "gems": 85,
    "energy": 4,
    "completed_levels": [1, 2, 3],
    "current_level": 4,
    "active_scenario": None,
    "arena_q_index": 0,
    "arena_answers": [],
    "arena_show_results": False,
    "arena_scores": None,
    "session_history": [
        {"level": "Storytelling", "icon": "📖", "score": 88, "xp": 110, "date": "Today"},
        {"level": "Active Listening", "icon": "👂", "score": 92, "xp": 75, "date": "Yesterday"},
        {"level": "First Impressions", "icon": "👋", "score": 76, "xp": 50, "date": "Jun 13"},
    ],
    "friends": ["PitchKing 🐴", "SarahS 👩🏼‍💻", "AlexT 🦙"],
}

def init_state():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v
