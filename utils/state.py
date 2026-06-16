"""
utils/state.py — Safe session_state initializations for Gallopi
"""
import streamlit as st


DEFAULTS = {
    # Onboarding
    "onboarded": False,
    "onboard_step": 1,
    "nickname": "",
    "avatar": "",
    "focus_areas": [],
    # Navigation
    "current_page": "path",
    # Stats
    "streak": 7,
    "xp": 1240,
    "gems": 85,
    "energy": 4,
    # Progress
    "completed_levels": [1, 2, 3],
    "current_level": 4,
    "target_level": 4,
    # Practice Arena state
    "arena_question_index": 0,
    "arena_answers": [],
    "arena_show_results": False,
    "arena_scores": None,
    "arena_level_id": None,
}


def init_state():
    """Initialize all session state keys with defaults if not already set."""
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value