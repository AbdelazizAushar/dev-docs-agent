import asyncio
import nest_asyncio
import streamlit as st
from datetime import datetime

nest_asyncio.apply()

st.set_page_config(
    page_title="DevDocs",
    page_icon="⌥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    background-color: #ffffff !important;
    color: #18181b !important;
}

[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }
.block-container {
    padding: 2rem max(2rem, 5vw) !important;
    max-width: 850px !important;
}

[data-testid="stSidebar"] {
    background-color: #fafafa !important;
    border-right: 1px solid #e4e4e7 !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    font-size: 13px;
    color: #52525b;
}

.sidebar-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #a1a1aa;
    margin-bottom: 8px;
    margin-top: 24px;
}

.session-pill {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
    border: 1px solid #e4e4e7;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    font-family: 'JetBrains Mono', monospace;
    color: #71717a;
    margin-bottom: 8px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.session-pill span {
    color: #18181b;
    font-weight: 600;
}
.session-pill span.active {
    color: #16a34a;
}

.msg-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 32px;
    animation: fadeIn 0.25s ease-out;
}
.msg-row.user { flex-direction: row-reverse; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to   { opacity: 1; transform: translateY(0); }
}

.avatar {
    width: 34px;
    height: 34px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
    flex-shrink: 0;
}
.avatar.bot {
    background: #ffffff;
    border: 1px solid #e4e4e7;
    color: #18181b;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
}
.avatar.user-av {
    background: #f4f4f5;
    border: 1px solid #e4e4e7;
    color: #52525b;
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 0.05em;
}

.bubble {
    max-width: 80%;
    padding: 14px 18px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.6;
}
.bubble.bot {
    background: #ffffff;
    border: 1px solid #e4e4e7;
    color: #18181b;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.bubble.user {
    background: #f4f4f5;
    border: 1px solid #e4e4e7;
    color: #18181b;
}

.report-section { margin-top: 14px; margin-bottom: 14px; }
.report-section:first-child { margin-top: 0; }
.report-section:last-child  { margin-bottom: 0; }

.report-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #71717a;
    margin-bottom: 6px;
}
.report-problem {
    color: #9f1239;
    font-size: 14px;
    padding: 10px 14px;
    border-left: 3px solid #f43f5e;
    background: #fff1f2;
    border-radius: 0 8px 8px 0;
}
.report-ref {
    color: #065f46;
    font-size: 13px;
    padding: 12px;
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    white-space: pre-wrap;
}
.report-solution { color: #18181b; font-size: 14px; }

.bubble pre {
    font-family: 'JetBrains Mono', monospace !important;
    background: #18181b !important;
    color: #f4f4f5 !important;
    padding: 14px !important;
    border-radius: 8px !important;
    margin: 10px 0 !important;
    border: none !important;
}
.bubble code {
    font-family: 'JetBrains Mono', monospace !important;
    background: #f4f4f5 !important;
    border: 1px solid #e4e4e7 !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    color: #e11d48 !important;
}
.bubble pre code {
    color: #a7f3d0 !important;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
}

.typing {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 14px 18px;
    background: #ffffff;
    border: 1px solid #e4e4e7;
    border-radius: 12px;
    width: fit-content;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.typing span {
    width: 6px; height: 6px;
    background: #a1a1aa;
    border-radius: 50%;
    animation: pulse 1.2s infinite both;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes pulse {
    0%, 100% { opacity: 0.3; transform: scale(0.8); }
    50%       { opacity: 1;   transform: scale(1.1); }
}

[data-testid="stChatInput"] {
    background-color: #ffffff !important;
    border: 1px solid #e4e4e7 !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06) !important;
}
[data-testid="stChatInput"] textarea { color: #18181b !important; }

.stButton button {
    background: #ffffff;
    border: 1px solid #e4e4e7;
    color: #52525b;
    font-size: 13px;
    font-weight: 500;
    border-radius: 6px;
    padding: 6px 14px;
    width: 100%;
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.stButton button:hover {
    border-color: #d4d4d8;
    color: #18181b;
    background: #f4f4f5;
}

.topic-chip {
    background: #ffffff;
    border: 1px solid #e4e4e7;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
    color: #52525b;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.top-bar {
    display: flex;
    align-items: center;
    gap: 14px;
    padding-bottom: 20px;
    border-bottom: 1px solid #e4e4e7;
    margin-bottom: 28px;
}
.top-bar-icon {
    font-size: 18px;
    background: #ffffff;
    border: 1px solid #e4e4e7;
    border-radius: 8px;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #18181b;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
}
.top-bar-title { font-size: 16px; font-weight: 600; color: #18181b; line-height: 1.2; }
.top-bar-sub   { font-size: 13px; color: #71717a; margin-top: 2px; }

[data-testid="stAppViewContainer"] > div:first-child { padding-bottom: 100px; }
</style>
""", unsafe_allow_html=True)


# ── session state ──────────────────────────────────────────────────────────────
def init_session():
    if "agent_state" not in st.session_state:
        st.session_state.agent_state = {
            "messages": [],
            "library": "",
            "version": None,
            "errors_seen": [],
            "doc_context": "",
            "route": "",
        }
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "topics" not in st.session_state:
        st.session_state.topics = []
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"session-{datetime.now().strftime('%H%M%S')}"
    if "initialized" not in st.session_state:
        st.session_state.initialized = False


init_session()


# ── pipeline ───────────────────────────────────────────────────────────────────
@st.cache_resource
def load_pipeline():
    try:
        from pipeline import run
        return run
    except Exception:
        return None


pipeline_run = load_pipeline()


# ── helpers ────────────────────────────────────────────────────────────────────
def parse_report(text: str) -> dict:
    sections = {"problem": "", "docs": "", "solution": "", "raw": text}
    lines = text.split("\n")
    current = "raw"
    buf = []
    for line in lines:
        l = line.strip()
        if l.startswith("## Problem"):
            if buf and current != "raw":
                sections[current] = "\n".join(buf).strip()
            current, buf = "problem", []
        elif l.startswith("## Docs"):
            if buf:
                sections[current] = "\n".join(buf).strip()
            current, buf = "docs", []
        elif l.startswith("## Solution"):
            if buf:
                sections[current] = "\n".join(buf).strip()
            current, buf = "solution", []
        else:
            buf.append(line)
    if buf:
        sections[current] = "\n".join(buf).strip()
    return sections


def render_message(msg: dict):
    role = msg["role"]
    content = msg["content"]

    if role == "user":
        st.markdown(f"""
        <div class="msg-row user">
            <div class="avatar user-av">You</div>
            <div class="bubble user">{content}</div>
        </div>
        """, unsafe_allow_html=True)
        return

    parsed = parse_report(content)
    has_sections = parsed["problem"] or parsed["docs"] or parsed["solution"]

    if has_sections:
        problem_html = (
            f'<div class="report-section"><div class="report-label">Problem</div>'
            f'<div class="report-problem">{parsed["problem"]}</div></div>'
        ) if parsed["problem"] else ""
        docs_html = (
            f'<div class="report-section"><div class="report-label">Docs reference</div>'
            f'<div class="report-ref">{parsed["docs"]}</div></div>'
        ) if parsed["docs"] else ""

        st.markdown(f"""
        <div class="msg-row">
            <div class="avatar bot">⌥</div>
            <div class="bubble bot">
                {problem_html}
                {docs_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if parsed["solution"]:
            st.markdown("""
            <div class="msg-row" style="margin-top:-20px;">
                <div style="width:34px;flex-shrink:0;"></div>
                <div class="bubble bot">
                    <div class="report-section">
                        <div class="report-label">Solution</div>
                        <div class="report-solution">
            """, unsafe_allow_html=True)
            st.markdown(parsed["solution"])
            st.markdown("</div></div></div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-row">
            <div class="avatar bot">⌥</div>
            <div class="bubble bot">{content}</div>
        </div>
        """, unsafe_allow_html=True)


# ── sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-label">Session</div>',
                unsafe_allow_html=True)

    lib = st.session_state.agent_state.get("library", "") or "—"
    ver = st.session_state.agent_state.get("version") or "latest"
    lib_class = "active" if lib != "—" else ""

    st.markdown(f"""
        <div class="session-pill">library <span class="{lib_class}">{lib}</span></div>
        <div class="session-pill">version <span>{ver}</span></div>
        <div class="session-pill">thread  <span>{st.session_state.thread_id}</span></div>
    """, unsafe_allow_html=True)

    if st.session_state.topics:
        st.markdown('<div class="sidebar-label">Topics</div>',
                    unsafe_allow_html=True)
        chips = "".join(
            [f'<span class="topic-chip">{t}</span>' for t in st.session_state.topics[-8:]])
        st.markdown(
            f'<div style="display:flex;flex-wrap:wrap;gap:8px;">{chips}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Actions</div>',
                unsafe_allow_html=True)
    if st.button("Clear session"):
        for key in ["agent_state", "chat_history", "topics", "thread_id", "initialized"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# ── main ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
    <div class="top-bar-icon">⌥</div>
    <div>
        <div class="top-bar-title">DevDocs</div>
        <div class="top-bar-sub">Ask about any library. Get answers from actual docs.</div>
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.initialized:
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "What are you building? Tell me the library and what's blocking you."
    })
    st.session_state.initialized = True

for msg in st.session_state.chat_history:
    render_message(msg)

user_input = st.chat_input("Ask about any library...")

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input})
    render_message({"role": "user", "content": user_input})

    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="msg-row">
        <div class="avatar bot">⌥</div>
        <div class="typing"><span></span><span></span><span></span></div>
    </div>
    """, unsafe_allow_html=True)

    if pipeline_run:
        try:
            # ── FIX: pipeline now returns (response, updated_state) ──
            response, updated_state = asyncio.run(
                pipeline_run(
                    user_input,
                    st.session_state.agent_state,
                    thread_id=st.session_state.thread_id
                )
            )
            # write updated state back so sidebar reflects library/version changes
            st.session_state.agent_state.update(updated_state)
        except Exception as e:
            response = f"Something went wrong: `{str(e)}`"
    else:
        response = "Pipeline not loaded. Check that `pipeline.py` is in the same directory."

    # update topics from the now-refreshed agent state
    lib = st.session_state.agent_state.get("library", "")
    if lib and lib not in st.session_state.topics:
        st.session_state.topics.append(lib)

    typing_placeholder.empty()
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})
    render_message({"role": "assistant", "content": response})

    st.rerun()
