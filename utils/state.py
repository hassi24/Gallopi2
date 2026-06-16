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
    "xp": 85,
    "gems": 1240,
    "energy": 4,
    "completed_levels": [],
    "current_level": 1,
    "active_scenario": None,
    "arena_q_index": 0,
    "arena_answers": [],
    "arena_show_results": False,
    "arena_scores": None,
    "session_history": [],
    "friends": ["PitchKing 🦁", "SarahS 🦊", "AlexT 🐼"],
}

def init_state():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v