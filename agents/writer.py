import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from state import SessionState

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError(
        "Missing GROQ_API_KEY inside your environment settings or .env file.")

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)


@tool
def read_doc_context(runtime: ToolRuntime) -> str:
    """Read the current documentation context from state."""
    return runtime.state.get("doc_context", "") or "No documentation found in state."


@tool
def read_library(runtime: ToolRuntime) -> str:
    """Read the current library name from state."""
    return runtime.state.get("library", "unknown library")


system_prompt = """
You are a documentation writer agent.
1. Call read_doc_context to get the fetched documentation.
2. Call read_library to get the library name for citation.
3. Produce a structured report in this exact format:

## Problem
Restate what the user is asking in one clear sentence.

## Docs reference
The most relevant excerpt from the documentation. Cite the library name and version.

## Solution
A working code snippet that directly answers the question, followed by a short explanation.

Rules:
- Base your answer strictly on doc_context, do not hallucinate APIs.
- If doc_context is empty, say so and ask the user to rephrase.
- Keep the solution focused — one clear example, not multiple alternatives.
"""

writer_agent = create_agent(
    model=llm,
    tools=[read_doc_context, read_library],
    system_prompt=system_prompt,
    state_schema=SessionState,
)
