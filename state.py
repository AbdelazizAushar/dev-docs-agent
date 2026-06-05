from langchain.agents import AgentState


class SessionState(AgentState):
    library: str
    version: str | None
    errors_seen: list[str]
    doc_context: str
    route: str
