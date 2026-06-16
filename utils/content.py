"""
utils/content.py — Static level definitions, question banks, and scenarios
"""

ANIMAL_AVATARS = [
    ("🦊", "The Fox",     "Clever & Strategic"),
    ("🐺", "The Wolf",    "Bold & Direct"),
    ("🦁", "The Lion",    "Commanding Leader"),
    ("🐬", "The Dolphin", "Empathetic & Smart"),
    ("🦅", "The Eagle",   "Visionary & Sharp"),
    ("🐼", "The Panda",   "Calm & Thoughtful"),
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
        "scenario": "You've just walked into a networking event. Introduce yourself to a stranger in a way that makes them want to continue the conversation.",
        "questions": [
            {
                "q": "Introduce yourself to a new colleague at a networking event. Make it memorable!",
                "hint": "Include your name, role, and one interesting hook about what you do.",
                "rubric": "Clear introduction · Memorable hook · Friendly tone · Shows curiosity about others",
            },
            {
                "q": "Someone asks: 'So, what do you do?' — give your best 30-second answer.",
                "hint": "Avoid job-title-only answers. Tell a mini-story about impact.",
                "rubric": "Avoids jargon · Shows passion · Relatable impact · Invites follow-up",
            },
            {
                "q": "A senior executive just sat next to you. Start a conversation that isn't small talk.",
                "hint": "Lead with curiosity, not self-promotion.",
                "rubric": "Confident opener · Genuine curiosity · Not sycophantic · Comfortable tone",
            },
        ],
        "evaluation_prompt": (
            "You are an expert communication coach. Evaluate this networking introduction response.\n"
            "Score each dimension 0-100:\n"
            "- clarity: How clear and structured is the introduction?\n"
            "- warmth: How warm, confident, and engaging is the delivery?\n"
            "- content: Does it include a hook, role, and invitation to converse?\n"
            "- conciseness: Is it appropriately brief?\n\n"
            "Also check which rubric flags were met (true/false):\n"
            "0: Clear and confident self-introduction\n"
            "1: Memorable hook or unique angle\n"
            "2: Showed genuine interest in the other person\n"
            "3: Maintained upbeat, friendly tone\n"
            "4: Natural, not rehearsed-sounding\n\n"
            "Respond ONLY in JSON (no markdown, no backticks):\n"
            '{"clarity":75,"warmth":80,"content":70,"conciseness":85,"rubric_passed":[0,3],'
            '"overall_tip":"One specific actionable tip in 1-2 sentences."}\n\n'
            "User response:\n"
        ),
        "rubric_items": [
            "Clear and confident self-introduction",
            "Memorable hook or unique angle",
            "Showed genuine interest in the other person",
            "Maintained upbeat, friendly tone",
            "Natural, not rehearsed-sounding",
        ],
    },
    {
        "id": 2,
        "title": "Active Listening",
        "icon": "👂",
        "difficulty": "Beginner",
        "xp": 75,
        "color": "#58cc02",
        "shadow": "#46a302",
        "scenario": "Your team member comes to you frustrated about a project. Your job: listen deeply and respond with empathy.",
        "questions": [
            {
                "q": "A colleague says: 'I feel like my ideas are never taken seriously in meetings.' Respond with empathy.",
                "hint": "Acknowledge their feeling before offering solutions.",
                "rubric": "Validates feelings · Paraphrases what they heard · Asks clarifying question · No immediate advice",
            },
            {
                "q": "After listening to a long complaint, summarize back what you heard to confirm understanding.",
                "hint": "Use 'What I'm hearing is...' or 'It sounds like...' framing.",
                "rubric": "Accurate summary · Empathetic tone · Invites correction · No judgment",
            },
            {
                "q": "Someone just shared exciting news about their promotion. How do you respond as an active listener?",
                "hint": "Match their energy. Ask questions that show you care about details.",
                "rubric": "Matches emotional tone · Asks follow-up · Shows genuine interest · Celebrates appropriately",
            },
        ],
        "evaluation_prompt": (
            "You are an expert communication coach evaluating active listening skills.\n"
            "Score 0-100: clarity, warmth, content (empathy/listening quality), conciseness.\n"
            "Check rubric (true/false for indices 0-4):\n"
            "0: Validated the speaker's feelings\n"
            "1: Accurately paraphrased or summarized\n"
            "2: Asked a thoughtful clarifying question\n"
            "3: Avoided jumping to solutions prematurely\n"
            "4: Warm and non-judgmental tone throughout\n\n"
            "Respond ONLY in JSON:\n"
            '{"clarity":75,"warmth":80,"content":70,"conciseness":85,"rubric_passed":[0,3],'
            '"overall_tip":"Tip here."}\n\nUser response:\n'
        ),
        "rubric_items": [
            "Validated the speaker's feelings first",
            "Accurately paraphrased or summarized",
            "Asked a thoughtful clarifying question",
            "Avoided jumping to solutions prematurely",
            "Warm and non-judgmental tone throughout",
        ],
    },
    {
        "id": 3,
        "title": "Storytelling",
        "icon": "📖",
        "difficulty": "Beginner",
        "xp": 100,
        "color": "#58cc02",
        "shadow": "#46a302",
        "scenario": "Great communicators tell stories, not facts. Practice structuring your experiences as compelling narratives.",
        "questions": [
            {
                "q": "Tell the story of a challenge you overcame at work using the STAR format (Situation, Task, Action, Result).",
                "hint": "Keep it under 90 seconds. End with the quantified result.",
                "rubric": "Clear situation · Specific task · Concrete action · Measurable result",
            },
            {
                "q": "Describe a time you had to convince someone who disagreed with you. What happened?",
                "hint": "Focus on HOW you persuaded, not just that you did.",
                "rubric": "Shows empathy · Specific persuasion technique · Resolution clear · Learnings shared",
            },
            {
                "q": "Tell a 60-second story that illustrates your biggest professional strength.",
                "hint": "Show, don't tell. A story is always more powerful than a claim.",
                "rubric": "Concrete example · Clear strength demonstrated · Emotional resonance · Appropriate length",
            },
        ],
        "evaluation_prompt": (
            "You are an expert communication coach evaluating business storytelling.\n"
            "Score 0-100: clarity (structure), warmth (engagement), content (STAR completeness), conciseness.\n"
            "Check rubric (indices 0-4):\n"
            "0: Clear situation/context established\n"
            "1: Specific actions described (not vague)\n"
            "2: Quantified or concrete result mentioned\n"
            "3: Emotional engagement or narrative tension\n"
            "4: Appropriate pacing and length\n\n"
            "Respond ONLY in JSON:\n"
            '{"clarity":75,"warmth":80,"content":70,"conciseness":85,"rubric_passed":[0,2],'
            '"overall_tip":"Tip here."}\n\nUser response:\n'
        ),
        "rubric_items": [
            "Clear situation/context established",
            "Specific actions described (not vague)",
            "Quantified or concrete result mentioned",
            "Emotional engagement or narrative tension",
            "Appropriate pacing and length",
        ],
    },
    {
        "id": 4,
        "title": "Elevator Pitch",
        "icon": "🚀",
        "difficulty": "Intermediate",
        "xp": 125,
        "color": "#1cb0f6",
        "shadow": "#1899d6",
        "scenario": "You're in an elevator with a key decision-maker. You have 60 seconds. Make it count.",
        "questions": [
            {
                "q": "Pitch your current project (or dream project) to a skeptical CEO in 60 seconds.",
                "hint": "Problem → Solution → Impact → Ask. No jargon.",
                "rubric": "Problem clear · Solution specific · Impact quantified · Clear ask",
            },
            {
                "q": "An investor asks: 'Why should I fund you over 10 other candidates?' Respond.",
                "hint": "Lead with your unique differentiator, then evidence.",
                "rubric": "Unique differentiator stated · Evidence provided · Confident tone · Concise",
            },
            {
                "q": "You have 30 seconds to pitch yourself for a role you really want. Go.",
                "hint": "Three things: who you are, what you do best, why them.",
                "rubric": "Identity clear · Core strength named · Company-specific fit · Energy and confidence",
            },
        ],
        "evaluation_prompt": (
            "You are an expert communication coach evaluating an elevator pitch.\n"
            "Score 0-100: clarity, warmth (confidence/energy), content (pitch completeness), conciseness.\n"
            "Check rubric (indices 0-4):\n"
            "0: Clear problem statement in opening\n"
            "1: Specific, jargon-free solution\n"
            "2: Quantified or concrete business impact\n"
            "3: Confident and energetic tone\n"
            "4: Strong call-to-action at end\n\n"
            "Respond ONLY in JSON:\n"
            '{"clarity":75,"warmth":80,"content":70,"conciseness":85,"rubric_passed":[0,3],'
            '"overall_tip":"Tip here."}\n\nUser response:\n'
        ),
        "rubric_items": [
            "Clear problem statement in opening",
            "Specific, jargon-free solution",
            "Quantified or concrete business impact",
            "Confident and energetic tone",
            "Strong call-to-action at end",
        ],
    },
    {
        "id": 5,
        "title": "Conflict Resolution",
        "icon": "🤝",
        "difficulty": "Intermediate",
        "xp": 150,
        "color": "#1cb0f6",
        "shadow": "#1899d6",
        "scenario": "Workplace conflicts are inevitable. Practice navigating them with grace and assertiveness.",
        "questions": [
            {
                "q": "A colleague publicly dismissed your idea in a meeting. How do you address it with them afterwards?",
                "hint": "Stay factual, not emotional. Use 'I' statements.",
                "rubric": "Uses I-statements · Factual not emotional · Seeks understanding · Proposes resolution",
            },
            {
                "q": "Two of your team members are in conflict. As the team lead, how do you mediate?",
                "hint": "Listen to both sides. Focus on shared goals.",
                "rubric": "Neutral stance · Acknowledges both parties · Redirects to shared goal · Clear next steps",
            },
            {
                "q": "A client is angry about a missed deadline. Walk them through your response.",
                "hint": "Acknowledge → Apologize → Action plan. No excuses first.",
                "rubric": "Acknowledges impact · Genuine apology · Concrete action plan · Maintains relationship",
            },
        ],
        "evaluation_prompt": (
            "You are an expert communication coach evaluating conflict resolution skills.\n"
            "Score 0-100: clarity, warmth (empathy/tone), content (resolution quality), conciseness.\n"
            "Check rubric (indices 0-4):\n"
            "0: Used I-statements (not blame language)\n"
            "1: Acknowledged the other person's perspective\n"
            "2: Stayed calm and professional in tone\n"
            "3: Offered a concrete resolution or next step\n"
            "4: Preserved the relationship\n\n"
            "Respond ONLY in JSON:\n"
            '{"clarity":75,"warmth":80,"content":70,"conciseness":85,"rubric_passed":[0,2],'
            '"overall_tip":"Tip here."}\n\nUser response:\n'
        ),
        "rubric_items": [
            "Used I-statements (not blame language)",
            "Acknowledged the other person's perspective",
            "Stayed calm and professional in tone",
            "Offered a concrete resolution or next step",
            "Preserved the relationship",
        ],
    },
    {
        "id": 6,
        "title": "Leadership Voice",
        "icon": "🎙️",
        "difficulty": "Advanced",
        "xp": 175,
        "color": "#a346ff",
        "shadow": "#8238cc",
        "scenario": "Leaders inspire action through their words. Practice speaking with authority, clarity, and authenticity.",
        "questions": [
            {
                "q": "Your team just hit a major setback. Rally them with a 60-second motivational message.",
                "hint": "Acknowledge the difficulty. Paint a clear path forward. Show you believe in them.",
                "rubric": "Acknowledges difficulty · Gives clear direction · Expresses belief in team · Ends on action",
            },
            {
                "q": "Deliver critical feedback to a high-performing employee who is becoming arrogant.",
                "hint": "Lead with appreciation, then address the behavior, not the person.",
                "rubric": "Leads with positive · Specific behavior (not character) · Clear expectation · Supportive tone",
            },
            {
                "q": "You need to announce an unpopular decision to your team. How do you communicate it?",
                "hint": "Explain the why. Acknowledge the impact. Open for questions.",
                "rubric": "Explains reasoning · Acknowledges impact · Shows empathy · Invites dialogue",
            },
        ],
        "evaluation_prompt": (
            "You are evaluating leadership communication.\n"
            "Score 0-100: clarity, warmth (authority + empathy balance), content (leadership quality), conciseness.\n"
            "Check rubric (indices 0-4):\n"
            "0: Spoke with authority and confidence\n"
            "1: Showed genuine empathy for their audience\n"
            "2: Gave a clear direction or decision\n"
            "3: Inspired rather than just informed\n"
            "4: Invited dialogue or questions\n\n"
            "Respond ONLY in JSON:\n"
            '{"clarity":75,"warmth":80,"content":70,"conciseness":85,"rubric_passed":[0,2],'
            '"overall_tip":"Tip here."}\n\nUser response:\n'
        ),
        "rubric_items": [
            "Spoke with authority and confidence",
            "Showed genuine empathy for their audience",
            "Gave a clear direction or decision",
            "Inspired rather than just informed",
            "Invited dialogue or questions",
        ],
    },
    {
        "id": 7,
        "title": "Data Storytelling",
        "icon": "📊",
        "difficulty": "Advanced",
        "xp": 200,
        "color": "#a346ff",
        "shadow": "#8238cc",
        "scenario": "Numbers don't speak for themselves. Turn data into a compelling narrative that drives decisions.",
        "questions": [
            {
                "q": "You have this data: 'Customer churn increased 18% last quarter.' Present this finding to the board in a way that drives action.",
                "hint": "Context → Insight → Implication → Recommendation.",
                "rubric": "Provides context · Names the insight · States business implication · Clear recommendation",
            },
            {
                "q": "Explain a complex technical process to a non-technical executive in under 60 seconds.",
                "hint": "Use an analogy. Avoid acronyms. Focus on business value.",
                "rubric": "Uses analogy or metaphor · No jargon · Business value clear · Audience-appropriate language",
            },
            {
                "q": "Your team's results are mixed — some wins, some misses. How do you present this honestly without sounding defensive?",
                "hint": "Lead with honesty. Own the misses. Double down on learnings.",
                "rubric": "Balanced and honest · Owns failures · Highlights learnings · Forward-looking",
            },
        ],
        "evaluation_prompt": (
            "You are evaluating data storytelling and presentation skills.\n"
            "Score 0-100: clarity, warmth (confidence/engagement), content (insight quality), conciseness.\n"
            "Check rubric (indices 0-4):\n"
            "0: Led with the key insight, not raw data\n"
            "1: Connected data to business impact\n"
            "2: Used plain language (no jargon)\n"
            "3: Gave a clear recommendation\n"
            "4: Structured logically (context → insight → action)\n\n"
            "Respond ONLY in JSON:\n"
            '{"clarity":75,"warmth":80,"content":70,"conciseness":85,"rubric_passed":[0,3],'
            '"overall_tip":"Tip here."}\n\nUser response:\n'
        ),
        "rubric_items": [
            "Led with the key insight, not raw data",
            "Connected data to business impact",
            "Used plain language (no jargon)",
            "Gave a clear recommendation",
            "Structured logically (context → insight → action)",
        ],
    },
    {
        "id": 8,
        "title": "Boardroom Master",
        "icon": "👑",
        "difficulty": "Expert",
        "xp": 250,
        "color": "#ffd700",
        "shadow": "#e8b400",
        "scenario": "The ultimate test. You're in the boardroom. Combine everything you've learned.",
        "questions": [
            {
                "q": "Present a full business proposal in 90 seconds to a board of directors. Include problem, solution, investment required, and projected ROI.",
                "hint": "Structure: Hook → Problem → Solution → Numbers → Ask.",
                "rubric": "Compelling hook · Problem quantified · Solution clear · ROI stated · Confident delivery",
            },
            {
                "q": "A board member challenges your proposal with: 'This is too risky. Why should we bet on this?' Handle the objection.",
                "hint": "Acknowledge the concern. Reframe risk. Provide evidence.",
                "rubric": "Acknowledges concern · No defensiveness · Provides evidence · Reframes confidently",
            },
            {
                "q": "Close the meeting by summarizing decisions made and next steps. Make everyone feel aligned.",
                "hint": "Recap key decisions. Assign clear owners. Set a timeline. Thank contributors.",
                "rubric": "Decisions clearly recapped · Owners named · Timeline set · Positive close",
            },
        ],
        "evaluation_prompt": (
            "You are evaluating boardroom-level executive communication.\n"
            "Score 0-100: clarity, warmth (executive presence), content (boardroom quality), conciseness.\n"
            "Check rubric (indices 0-4):\n"
            "0: Opened with a compelling hook\n"
            "1: All key business components covered\n"
            "2: Handled pressure or complexity with grace\n"
            "3: Used numbers or evidence effectively\n"
            "4: Closed with clear next steps and alignment\n\n"
            "Respond ONLY in JSON:\n"
            '{"clarity":75,"warmth":80,"content":70,"conciseness":85,"rubric_passed":[0,2,4],'
            '"overall_tip":"Tip here."}\n\nUser response:\n'
        ),
        "rubric_items": [
            "Opened with a compelling hook",
            "All key business components covered",
            "Handled pressure or complexity with grace",
            "Used numbers or evidence effectively",
            "Closed with clear next steps and alignment",
        ],
    },
]

LEVELS_BY_ID = {lvl["id"]: lvl for lvl in LEVELS}