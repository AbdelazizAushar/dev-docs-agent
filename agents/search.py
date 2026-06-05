import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from state import SessionState

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("Missing GROQ_API_KEY inside your environment settings or .env file.")

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

@tool
def save_doc_context(doc_chunks: str, runtime: ToolRuntime) -> Command:
    """Save fetched documentation chunks into state after retrieving them."""
    return Command(update={
        "doc_context": doc_chunks,
        "messages": [ToolMessage("Documentation saved.", tool_call_id=runtime.tool_call_id)]
    })

system_prompt = """
You are a documentation search agent.
1. Read library and version from state.
2. Use Context7 tools to resolve the library ID, then fetch relevant docs for the user's question.
3. Call save_doc_context with the raw documentation chunks you retrieved.
Do not summarize or answer — only fetch and save.
"""

async def create_search_agent():
    client = MultiServerMCPClient({
        "context7": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@upstash/context7-mcp"]
        }
    })
    tools = await client.get_tools()
    return create_agent(
        model=llm,
        tools=[*tools, save_doc_context], 
        system_prompt=system_prompt,
        state_schema=SessionState,
    )