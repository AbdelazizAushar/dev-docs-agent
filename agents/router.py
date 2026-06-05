import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from state import SessionState

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError(
        "Missing GROQ_API_KEY inside your environment settings or .env file.")

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)


@tool
def update_library(library: str, version: str | None, runtime: ToolRuntime) -> Command:
    """Update the library name and version in state once extracted from the user message."""
    return Command(update={
        "library": library,
        "version": version,
        "messages": [ToolMessage("Library context updated.", tool_call_id=runtime.tool_call_id)]
    })


@tool
def decide_route(route: str, runtime: ToolRuntime) -> Command:
    """Set the routing decision in state. Use 'search' if docs are needed, 'answer' if doc_context is sufficient."""
    return Command(update={
        "route": route,
        "messages": [ToolMessage(f"Route set to: {route}", tool_call_id=runtime.tool_call_id)]
    })


system_prompt = """
You are a router agent. Given the user's message and current session state:
1. Extract the library name and version if mentioned. Call update_library to save them.
2. Check if doc_context in state already covers the user's question.
   - If yes: call decide_route with route='answer'.
   - If no or doc_context is empty: call decide_route with route='search'.
"""

router_agent = create_agent(
    model=llm,
    tools=[update_library, decide_route],
    system_prompt=system_prompt,
    state_schema=SessionState,
)
