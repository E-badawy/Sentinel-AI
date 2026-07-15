from typing import TypedDict


class AgentState(TypedDict):
    session_id: str
    message: str
    response: str
    tool: str
    history: list
    file: str