# DevDocs

A multi-agent documentation assistant. Ask about any library, get answers grounded in real docs — not hallucinated APIs.

Built with LangGraph, Groq, Context7 MCP, and Streamlit.

## How it works

```
User message
     │
     ▼
┌─────────┐   route="search"   ┌────────┐   ┌────────┐
│ Router  │ ─────────────────► │ Search │──►│ Writer │──► Structured report
└─────────┘                    └────────┘   └────────┘
     │
     │ route="answer" (doc_context already sufficient)
     └────────────────────────────────────────┘
```

- **Router** — extracts library/version from the message, decides whether existing `doc_context` in state already answers the question (`route="answer"`) or fresh docs are needed (`route="search"`).
- **Search** — only runs when routed. Uses [Context7](https://github.com/upstash/context7) MCP tools to resolve the library ID and fetch relevant doc chunks, saves them to state.
- **Writer** — reads `doc_context` and `library` from state, produces a structured report:
  - `## Problem` — restates the question
  - `## Docs reference` — the relevant doc excerpt, cited
  - `## Solution` — a working code snippet + short explanation

State (library, version, route, doc_context, errors_seen, messages) is passed between agents via LangGraph's shared `SessionState` and persisted per-thread with `InMemorySaver`.

## Project structure

```
.
├── app.py              # Streamlit UI
├── pipeline.py          # Orchestrates router → search → writer
├── state.py             # Shared SessionState schema
└── agents/
    ├── router.py         # Extracts library/version, decides routing
    ├── search.py         # Context7 MCP doc retrieval
    └── writer.py         # Produces the structured report
```

## Setup

1. Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include: `streamlit`, `nest_asyncio`, `python-dotenv`, `langgraph`, `langchain`, `langchain-groq`, `langchain-mcp-adapters`.

2. Node.js is required for the Context7 MCP server (launched via `npx`).

3. Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key
```

## Run

```bash
streamlit run app.py
```

Open the local URL Streamlit prints, and start asking about a library — e.g. *"How do I add a middleware in FastAPI 0.115?"*

## Notes

- Each browser session gets its own `thread_id`, so conversation/state is isolated per session.
- Click **Clear session** in the sidebar to reset state, chat history, and topics.
- If `doc_context` is empty when the writer runs, the report will say so and ask you to rephrase rather than guessing at APIs.

## License

MIT
