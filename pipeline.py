from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

from state import SessionState
from agents.router import router_agent
from agents.writer import writer_agent
from agents.search import create_search_agent

load_dotenv()

checkpointer = InMemorySaver()


async def run(user_message: str, state: SessionState, thread_id: str = "default") -> str:

    # Add user message to state
    state["messages"] = state.get(
        "messages", []) + [HumanMessage(content=user_message)]

    config = {"configurable": {"thread_id": thread_id}}

    # Router runs — updates library, version, and route in state via tools
    router_result = await router_agent.ainvoke(state, config=config)

    # Read route decision directly from state (set by decide_route tool)
    route = router_result.get("route", "search")

    # Search only if needed — saves doc_context to state via tool
    if route == "search":
        search_agent = await create_search_agent()
        router_result = await search_agent.ainvoke(router_result, config=config)

    # Writer reads doc_context from state via tool, returns structured report
    writer_result = await writer_agent.ainvoke(router_result, config=config)

    return writer_result["messages"][-1].content, router_result
