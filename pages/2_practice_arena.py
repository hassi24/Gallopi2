import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import streamlit.components.v1 as components
from utils.state import init_state
from utils.helpers import inject_css, topbar, grade_response
from utils.content import LEVELS_BY_ID

st.set_page_config(
    page_title="Practice Arena · Gallopi",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

init_state()
inject_css()
topbar(back_href="/")

if not st.session_state.active_scenario:
    st.markdown("""
<div style="text-align:center;padding:40px 20px;">
    <div style="font-size:48px;margin-bottom:16px;">🦄</div>
    <div style="font-size:18px;font-weight:800;margin-bottom:12px;">No level selected!</div>
    <div style="font-size:14px;color:#4a6572;font-weight:600;">Head back to the path and tap a level to begin.</div>
</div>
""", unsafe_allow_html=True)
    if st.button("← Back to Path", use_container_width=True):
        st.switch_page("Home.py")
    st.stop()

level = LEVELS_BY_ID.get(st.session_state.active_scenario)
if not level:
    st.error("Level not found.")
    st.stop()

questions = level["questions"]
q_index   = st.session_state.arena_q_index
total_q   = len(questions)


# ═══════════════════════════════════════════════════════════
# RESULTS SCREEN
# ═══════════════════════════════════════════════════════════
def show_results():
    scores = st.session_state.arena_scores
    if not scores:
        return

    avg_clarity     = int(sum(s["clarity"]     for s in scores) / len(scores))
    avg_confidence  = int(sum(s["confidence"]  for s in scores) / len(scores))
    avg_vocabulary  = int(sum(s["vocabulary"]  for s in scores) / len(scores))
    avg_conciseness = int(sum(s["conciseness"] for s in scores) / len(scores))
    overall         = int(sum(s["overall"]      for s in scores) / len(scores))
    xp_earned       = int(level["xp"] * (overall / 100))

    all_passed = set()
    for s in scores:
        all_passed.update(s.get("rubric_passed", []))
    all_passed_list = sorted(all_passed)

    all_strengths, all_improvements = [], []
    for s in scores:
        all_strengths.extend(s.get("strengths", []))
        all_improvements.extend(s.get("improvements", []))

    seen_s, seen_i = set(), set()
    uniq_strengths, uniq_improvements = [], []
    for x in all_strengths:
        if x not in seen_s:
            seen_s.add(x); uniq_strengths.append(x)
    for x in all_improvements:
        if x not in seen_i:
            seen_i.add(x); uniq_improvements.append(x)

    uniq_strengths    = uniq_strengths[:3]
    uniq_improvements = uniq_improvements[:3]
    tip               = scores[-1].get("tip", "Keep practicing!")

    score_color = "#58cc02" if overall >= 80 else ("#ff9600" if overall >= 60 else "#ff4b4b")
    grade_label = "Excellent! 🌟" if overall >= 80 else ("Good Work! 💪" if overall >= 60 else "Keep Going! 🔄")

    if overall >= 80:
        st.markdown("""
<style>
@keyframes confetti-drop {
    0% { transform: translateY(-30px) rotate(0deg); opacity: 1; }
    100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
}
.confetti-emoji {
    position: fixed; top: -20px; font-size: 24px;
    animation: confetti-drop 3.5s ease-in forwards;
    pointer-events: none; z-index: 99999;
}
</style>
<div class="confetti-emoji" style="left:5%;animation-delay:0s;">🎉</div>
<div class="confetti-emoji" style="left:15%;animation-delay:0.3s;">⭐</div>
<div class="confetti-emoji" style="left:25%;animation-delay:0.6s;">🌟</div>
<div class="confetti-emoji" style="left:40%;animation-delay:0.2s;">✨</div>
<div class="confetti-emoji" style="left:55%;animation-delay:0.5s;">🎊</div>
<div class="confetti-emoji" style="left:65%;animation-delay:0.1s;">💎</div>
<div class="confetti-emoji" style="left:75%;animation-delay:0.8s;">🦄</div>
<div class="confetti-emoji" style="left:88%;animation-delay:0.4s;">🏆</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:linear-gradient(135deg,#131f24,#0f1e14);
            border:2px solid {score_color};border-radius:24px;
            padding:24px 20px;margin:0 16px 16px;text-align:center;">
    <div class="unicorn-mascot">🦄</div>
    <div style="font-size:72px;font-weight:900;color:{score_color};
                line-height:1;text-shadow:0 0 30px {score_color}88;">{overall}</div>
    <div style="font-size:12px;color:#4a6572;font-weight:700;margin:-4px 0 8px;">OVERALL SCORE</div>
    <div style="font-size:20px;font-weight:900;">{grade_label}</div>
    <div style="margin-top:12px;padding:8px 20px;background:#ffd70022;
                border:1px solid #ffd70044;border-radius:50px;display:inline-block;">
        <span style="font-size:14px;font-weight:800;color:#ffd700;">🏆 +{xp_earned} XP earned!</span>
    </div>
</div>
""", unsafe_allow_html=True)

    metrics = [
        ("🎯 Clarity",      avg_clarity,     "#1cb0f6"),
        ("💪 Confidence",   avg_confidence,  "#ff9600"),
        ("📚 Vocabulary",   avg_vocabulary,  "#a346ff"),
        ("✂️ Conciseness",  avg_conciseness, "#58cc02"),
    ]
    cols = st.columns(2)
    for i, (label, val, color) in enumerate(metrics):
        with cols[i % 2]:
            st.markdown(f"""
<div style="background:#131f24;border:2px solid #203038;border-radius:16px;
            padding:14px 12px;margin-bottom:10px;">
    <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-size:12px;font-weight:700;">{label}</span>
        <span style="font-size:14px;font-weight:900;color:{color};">{val}</span>
    </div>
    <div style="background:#203038;border-radius:50px;height:10px;overflow:hidden;">
        <div style="background:{color};width:{val}%;height:100%;border-radius:50px;
                    box-shadow:0 0 8px {color}66;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 10px;margin-top:4px;">📊 Detailed Feedback</div>', unsafe_allow_html=True)
    col_s, col_i = st.columns(2)
    with col_s:
        st.markdown("""
<div style="background:#0f2a0f;border:2px solid #58cc0244;border-radius:16px;padding:14px;margin-bottom:10px;">
    <div style="font-size:12px;font-weight:800;color:#58cc02;margin-bottom:8px;">✅ STRENGTHS</div>
""", unsafe_allow_html=True)
        for s in uniq_strengths:
            st.markdown(f'<div style="font-size:12px;font-weight:600;color:#e8f4f8;margin-bottom:6px;line-height:1.4;">• {s}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_i:
        st.markdown("""
<div style="background:#2a1010;border:2px solid #ff4b4b44;border-radius:16px;padding:14px;margin-bottom:10px;">
    <div style="font-size:12px;font-weight:800;color:#ff7b7b;margin-bottom:8px;">🔧 IMPROVE</div>
""", unsafe_allow_html=True)
        for imp in uniq_improvements:
            st.markdown(f'<div style="font-size:12px;font-weight:600;color:#e8f4f8;margin-bottom:6px;line-height:1.4;">• {imp}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 10px;">📋 Communication Checklist</div>', unsafe_allow_html=True)
    for idx, item in enumerate(level["rubric_items"]):
        passed = idx in all_passed_list
        icon   = "✅" if passed else "❌"
        color  = "#e8f4f8" if passed else "#ff7b7b"
        border = "#58cc0244" if passed else "#ff4b4b44"
        bg     = "#0f2a0f" if passed else "#2a1010"
        st.markdown(f"""
<div style="background:{bg};border:1.5px solid {border};border-radius:12px;
            padding:10px 14px;margin:0 16px 8px;
            display:flex;align-items:center;gap:10px;">
    <span style="font-size:16px;">{icon}</span>
    <span style="font-size:13px;font-weight:600;color:{color};">{item}</span>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:#0d1e26;border:2px solid #1cb0f6;border-radius:20px;
            padding:18px;margin:16px 16px 16px;">
    <div style="font-size:13px;font-weight:800;color:#1cb0f6;margin-bottom:8px;">💡 Gallopi's Coaching Tip</div>
    <div style="font-size:14px;font-weight:600;line-height:1.6;">{tip}</div>
</div>
""", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.arena_q_index = 0
            st.session_state.arena_answers = []
            st.session_state.arena_show_results = False
            st.session_state.arena_scores = None
            st.rerun()
    with col_b:
        if st.button("🏠 Back to Path", use_container_width=True):
            if overall >= 60:
                lid = st.session_state.active_scenario
                if lid not in st.session_state.completed_levels:
                    st.session_state.completed_levels.append(lid)
                    if lid == st.session_state.current_level:
                        st.session_state.current_level = lid + 1
                st.session_state.xp += xp_earned
                if st.session_state.energy > 0:
                    st.session_state.energy -= 1
            st.session_state.active_scenario = None
            st.switch_page("Home.py")


# ═══════════════════════════════════════════════════════════
# ROUTER — results or question
# ═══════════════════════════════════════════════════════════
if st.session_state.arena_show_results and st.session_state.arena_scores:
    show_results()
    st.stop()

if q_index >= total_q:
    all_scores = []
    for idx, ans in enumerate(st.session_state.arena_answers):
        q_data = questions[idx]
        score  = grade_response(ans, q_data["keywords"], q_data["forbidden"])
        all_scores.append(score)
    st.session_state.arena_scores       = all_scores
    st.session_state.arena_show_results = True
    st.rerun()


# ═══════════════════════════════════════════════════════════
# QUESTION SCREEN
# ═══════════════════════════════════════════════════════════
current_q   = questions[q_index]
diff_colors = {"Beginner":"#58cc02","Intermediate":"#ff9600","Advanced":"#a346ff","Expert":"#ffd700"}
diff_color  = diff_colors.get(level["difficulty"], "#4a6572")

progress_pct = int((q_index / total_q) * 100)
st.markdown(f"""
<div style="padding:0 16px 16px;">
    <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-size:12px;font-weight:700;color:#4a6572;">
            Question {q_index + 1} of {total_q}
        </span>
        <span style="font-size:12px;font-weight:800;color:#58cc02;">{progress_pct}%</span>
    </div>
    <div style="background:#203038;border-radius:50px;height:10px;overflow:hidden;">
        <div style="background:linear-gradient(90deg,#1cb0f6,#58cc02);
                    width:{progress_pct}%;height:100%;border-radius:50px;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:#131f24;border:2px solid #1cb0f6;border-radius:20px;
            padding:18px;margin:0 16px 16px;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <div style="font-size:40px;">{level['icon']}</div>
        <div>
            <div style="font-size:20px;font-weight:900;">{level['title']}</div>
            <div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap;">
                <span style="background:{diff_color}22;color:{diff_color};border:1px solid {diff_color}44;
                             padding:3px 10px;border-radius:50px;font-size:11px;font-weight:800;">
                    {level['difficulty']}
                </span>
                <span style="background:#ffd70022;color:#ffd700;border:1px solid #ffd70044;
                             padding:3px 10px;border-radius:50px;font-size:11px;font-weight:800;">
                    +{level['xp']} XP
                </span>
            </div>
        </div>
    </div>
    <div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;
                letter-spacing:1.2px;margin-bottom:6px;">🎭 SCENARIO</div>
    <div style="font-size:13px;font-weight:600;line-height:1.6;color:#c8dde8;
                background:#0b141a;border-radius:12px;padding:12px;border:1px solid #203038;">
        {level['scenario']}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:#1a2f3a;border:2px solid #1cb0f6;border-radius:20px;
            padding:18px;margin:0 16px 16px;">
    <div style="font-size:12px;font-weight:800;color:#1cb0f6;text-transform:uppercase;
                letter-spacing:1.2px;margin-bottom:10px;">🎙️ CHALLENGE {q_index+1}</div>
    <div style="font-size:16px;font-weight:800;line-height:1.5;margin-bottom:10px;">
        {current_q['q']}
    </div>
    <div style="background:#0b141a;border-radius:10px;padding:10px 12px;
                border-left:3px solid #ff9600;">
        <span style="font-size:11px;font-weight:700;color:#ff9600;">💡 HINT: </span>
        <span style="font-size:12px;font-weight:600;color:#8a9baa;">{current_q['hint']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# VOICE RECORDER — real browser MediaRecorder + Web Speech API
# ═══════════════════════════════════════════════════════════
voice_html = f"""
<style>
  * {{ box-sizing: border-box; }}
  body {{ background: transparent; margin: 0; font-family: 'Nunito', sans-serif; }}

  #recorder-card {{
    background: #131f24;
    border: 2px solid #203038;
    border-radius: 18px;
    padding: 18px 16px 14px;
    margin: 0 0 12px;
    text-align: center;
  }}
  #rec-title {{
    font-size: 13px; font-weight: 800; color: #8a9baa;
    text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 14px;
  }}
  #mic-btn {{
    width: 80px; height: 80px; border-radius: 50%;
    background: #58cc02; border: none;
    box-shadow: 0 5px 0 #46a302;
    font-size: 36px; cursor: pointer;
    transition: transform 0.1s, box-shadow 0.1s;
    display: inline-flex; align-items: center; justify-content: center;
    margin-bottom: 12px;
  }}
  #mic-btn.recording {{
    background: #ff4b4b !important;
    box-shadow: 0 5px 0 #cc3333 !important;
    animation: pulse-mic 1s ease-in-out infinite;
  }}
  #mic-btn:active {{ transform: translateY(3px); box-shadow: 0 2px 0 #46a302; }}
  @keyframes pulse-mic {{
    0%,100% {{ box-shadow: 0 5px 0 #cc3333, 0 0 0 0 rgba(255,75,75,0.4); }}
    50%      {{ box-shadow: 0 5px 0 #cc3333, 0 0 0 16px rgba(255,75,75,0); }}
  }}
  #status-txt {{
    font-size: 13px; font-weight: 700; color: #4a6572; margin-bottom: 6px;
  }}
  #timer {{
    font-size: 28px; font-weight: 900; color: #1cb0f6;
    font-variant-numeric: tabular-nums; min-height: 36px;
  }}
  #waveform {{
    display: flex; align-items: center; justify-content: center; gap: 4px;
    height: 40px; margin: 10px 0 6px; visibility: hidden;
  }}
  .bar {{
    width: 5px; border-radius: 3px; background: #1cb0f6;
    animation: wave 0.8s ease-in-out infinite;
  }}
  @keyframes wave {{
    0%,100% {{ height: 6px; opacity: 0.4; }}
    50%      {{ height: 32px; opacity: 1; }}
  }}
  #transcript-box {{
    background: #0b141a; border: 2px solid #1cb0f6;
    border-radius: 14px; padding: 12px 14px;
    font-size: 14px; font-weight: 600; color: #e8f4f8;
    min-height: 60px; text-align: left; line-height: 1.6;
    margin-top: 12px; display: none; white-space: pre-wrap; word-break: break-word;
  }}
  #copy-area {{ display: none; }}
  #submit-row {{ margin-top: 14px; }}
  #use-btn {{
    background: #58cc02; color: #fff; border: none;
    border-radius: 14px; font-size: 15px; font-weight: 800;
    padding: 12px 24px; width: 100%;
    box-shadow: 0 4px 0 #46a302; cursor: pointer;
    transition: transform 0.1s, box-shadow 0.1s;
  }}
  #use-btn:active {{ transform: translateY(3px); box-shadow: 0 1px 0 #46a302; }}
  #use-btn:disabled {{ background: #2c4a2c; box-shadow: 0 4px 0 #1e331e; color: #4a7a4a; cursor: not-allowed; }}
  #fallback-note {{
    font-size: 11px; color: #3c5566; margin-top: 10px; font-weight: 600;
    text-align: center;
  }}
  #no-mic-msg {{
    font-size: 12px; color: #ff9600; font-weight: 700;
    padding: 8px 12px; background: #2a1a00; border-radius: 10px;
    margin-top: 10px; display: none;
  }}
</style>

<div id="recorder-card">
  <div id="rec-title">🎙️ Voice Response</div>

  <button id="mic-btn" onclick="toggleRecord()" title="Tap to record">🎙️</button>
  <div id="status-txt">Tap the mic to start recording</div>
  <div id="timer"></div>

  <div id="waveform">
    {''.join(f'<div class="bar" style="animation-delay:{i*0.12:.2f}s"></div>' for i in range(9))}
  </div>

  <div id="no-mic-msg">⚠️ Microphone access denied or unavailable in this browser.</div>

  <div id="transcript-box"></div>

  <div id="submit-row">
    <button id="use-btn" disabled onclick="useTranscript()">🎙️ Record first to submit</button>
  </div>
  <div id="fallback-note">Tip: Use Chrome or Edge for best speech recognition support</div>
</div>

<!-- Hidden textarea that Streamlit reads via query param trick -->
<textarea id="copy-area"></textarea>

<script>
let mediaRecorder = null;
let recognition   = null;
let isRecording   = false;
let timerInterval = null;
let seconds       = 0;
let transcript    = "";

const micBtn     = document.getElementById("mic-btn");
const statusTxt  = document.getElementById("status-txt");
const timerEl    = document.getElementById("timer");
const waveform   = document.getElementById("waveform");
const tBox       = document.getElementById("transcript-box");
const useBtn     = document.getElementById("use-btn");
const noMicMsg   = document.getElementById("no-mic-msg");

function fmtTime(s) {{
  const m = Math.floor(s/60).toString().padStart(2,"0");
  const ss= (s%60).toString().padStart(2,"0");
  return m+":"+ss;
}}

function startTimer() {{
  seconds = 0;
  timerEl.textContent = fmtTime(0);
  timerInterval = setInterval(()=>{{ seconds++; timerEl.textContent = fmtTime(seconds); }}, 1000);
}}
function stopTimer() {{ clearInterval(timerInterval); }}

function toggleRecord() {{
  if (!isRecording) startRecording(); else stopRecording();
}}

async function startRecording() {{
  transcript = "";
  isRecording = true;
  micBtn.classList.add("recording");
  micBtn.textContent = "⏹️";
  statusTxt.textContent = "Recording… speak clearly!";
  waveform.style.visibility = "visible";
  tBox.style.display = "none";
  tBox.textContent = "";
  useBtn.disabled = true;
  useBtn.textContent = "🎙️ Record first to submit";
  startTimer();

  // Web Speech API (live transcript)
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {{
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";
    let finalTranscript = "";
    recognition.onresult = (e) => {{
      let interim = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {{
        if (e.results[i].isFinal) finalTranscript += e.results[i][0].transcript + " ";
        else interim += e.results[i][0].transcript;
      }}
      transcript = (finalTranscript + interim).trim();
      if (transcript) {{
        tBox.textContent = transcript;
        tBox.style.display = "block";
      }}
    }};
    recognition.onerror = (e) => {{
      if (e.error === "not-allowed" || e.error === "service-not-allowed") {{
        noMicMsg.style.display = "block";
        stopRecording();
      }}
    }};
    recognition.start();
  }} else {{
    // Fallback: just use MediaRecorder without live transcript
    try {{
      const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();
      statusTxt.textContent = "Recording… (transcript unavailable in this browser, type below)";
    }} catch(err) {{
      noMicMsg.style.display = "block";
      isRecording = false;
      micBtn.classList.remove("recording");
      micBtn.textContent = "🎙️";
      statusTxt.textContent = "Microphone unavailable — type your response below.";
      waveform.style.visibility = "hidden";
      stopTimer();
    }}
  }}
}}

function stopRecording() {{
  isRecording = false;
  micBtn.classList.remove("recording");
  micBtn.textContent = "🎙️";
  waveform.style.visibility = "hidden";
  stopTimer();

  if (recognition) {{ recognition.stop(); recognition = null; }}
  if (mediaRecorder && mediaRecorder.state !== "inactive") {{
    mediaRecorder.stop();
    mediaRecorder.stream.getTracks().forEach(t => t.stop());
  }}

  const dur = fmtTime(seconds);
  if (transcript && transcript.trim().length > 2) {{
    statusTxt.textContent = `✅ Recorded ${{dur}} · Tap mic to re-record`;
    tBox.textContent = transcript.trim();
    tBox.style.display = "block";
    useBtn.disabled = false;
    useBtn.textContent = "✅ Use This Response →";
  }} else {{
    statusTxt.textContent = `Recording stopped (${{dur}}) · No speech detected — try again or type below`;
    useBtn.disabled = true;
  }}
}}

function useTranscript() {{
  if (!transcript || transcript.trim().length < 3) return;
  // Send to Streamlit via URL search param + page reload approach
  // We use sessionStorage so the parent Streamlit page can read it
  const key = "gallopi_voice_{q_index}";
  try {{
    window.parent.postMessage({{
      type: "streamlit:setComponentValue",
      value: transcript.trim()
    }}, "*");
  }} catch(e) {{}}
  // Fallback: fill hidden textarea and fire input event for Streamlit component
  const ta = document.getElementById("copy-area");
  ta.value = transcript.trim();
  // Store in parent's sessionStorage via postMessage
  window.parent.postMessage({{ gallopi_voice: transcript.trim(), q_index: {q_index} }}, "*");
  useBtn.textContent = "✅ Submitted! Scroll down →";
  useBtn.style.background = "#1cb0f6";
  useBtn.style.boxShadow = "0 4px 0 #1899d6";
  statusTxt.textContent = "Voice response captured — now submit below ↓";
}}
</script>
"""

components.html(voice_html, height=420, scrolling=False)

# Voice transcript capture via session state key
# The iframe posts a message; we catch it with a JS listener injected into the main page
st.markdown(f"""
<script>
(function() {{
  window.addEventListener("message", function(e) {{
    if (e.data && e.data.gallopi_voice !== undefined && e.data.q_index === {q_index}) {{
      // Write to a hidden input that triggers Streamlit rerun
      const inputs = window.parent.document.querySelectorAll('textarea[data-testid="stTextArea"]');
      inputs.forEach(inp => {{
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        nativeInputValueSetter.call(inp, e.data.gallopi_voice);
        inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
      }});
    }}
  }});
}})();
</script>
""", unsafe_allow_html=True)

st.markdown('<div style="padding:0 16px 8px;"><div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;">📝 Your Response (edit or type here)</div></div>', unsafe_allow_html=True)

user_response = st.text_area(
    "Your spoken response",
    height=130,
    placeholder="Your voice transcript will appear here automatically after recording…\nor type your response directly.",
    label_visibility="collapsed",
    key=f"response_{q_index}",
)

with st.expander("🔍 Power words for this question"):
    kw_pills = "".join(
        f'<span style="background:#1cb0f633;color:#1cb0f6;padding:4px 10px;'
        f'border-radius:50px;font-size:12px;font-weight:700;margin:3px;display:inline-block;">{kw}</span>'
        for kw in current_q["keywords"][:8]
    )
    st.markdown(f'<div style="padding:6px 0;display:flex;flex-wrap:wrap;gap:4px;">{kw_pills}</div>', unsafe_allow_html=True)

st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

col_sub, col_skip = st.columns([3, 1])
with col_sub:
    btn_label = "✅ Submit & Finish" if q_index == total_q - 1 else f"Submit → Q{q_index + 2}"
    if st.button(btn_label, use_container_width=True):
        if user_response.strip():
            st.session_state.arena_answers.append(user_response.strip())
            st.session_state.arena_q_index += 1
            st.rerun()
        else:
            st.warning("Record your voice or type a response before submitting!")

with col_skip:
    if st.button("Skip", use_container_width=True):
        st.session_state.arena_answers.append("[Skipped]")
        st.session_state.arena_q_index += 1
        st.rerun()

if st.session_state.arena_answers:
    st.markdown(f'<div style="font-size:11px;color:#4a6572;font-weight:700;text-align:center;margin-top:8px;">✅ {len(st.session_state.arena_answers)} of {total_q} answered</div>', unsafe_allow_html=True)

st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)
