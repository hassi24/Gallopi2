ANIMAL_AVATARS = [
    ("🦁", "Lion Leader",   "Bold & Commanding"),
    ("🦊", "Clever Fox",    "Sharp & Strategic"),
    ("🐼", "Calm Panda",    "Cool Under Pressure"),
    ("🐨", "Team Koala",    "Collaborative & Kind"),
    ("🦥", "Steady Sloth",  "Thoughtful & Deep"),
    ("🦄", "Unicorn",       "Creative & Inspiring"),
]

FOCUS_OPTIONS = [
    ("Interview Prep", "🎤"),
    ("Public Speaking", "🎙️"),
    ("Leadership Pitching", "💼"),
    ("Active Listening", "👂"),
]

LEVELS = [
    {
        "id": 1,
        "title": "First Impressions",
        "icon": "👋",
        "difficulty": "Beginner",
        "xp": 50,
        "color": "#58cc02",
        "shadow": "#46a302",
        "scenario": "Introduce yourself memorably in a professional setting.",
        "questions": [
            {
                "q": "Introduce yourself to a new colleague at a networking event!",
                "hint": "Include your name, role, and one interesting target passion hook.",
                "keywords": ["name", "excited", "passionate", "collaborate", "team", "growth"],
                "forbidden": ["um", "uh", "like", "basically", "maybe"],
            }
        ],
        "rubric_items": [
            "Clear articulation of professional focus",
            "Strong opening engagement hook",
            "Absence of distracting vocal filler phrases"
        ]
    }
]

LEVELS_BY_ID = {l["id"]: l for l in LEVELS}