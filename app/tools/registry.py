from app.tools.llm_tool import llm_tool
from app.tools.search_tool import search_tool
from app.tools.email_tool import email_tool


TOOLS = {
    "llm": llm_tool,
    "search": search_tool,
    "email": email_tool,
}


def get_tool(name: str):
    """
    Returns a registered tool.
    Defaults to the LLM tool.
    """
    return TOOLS.get(name, llm_tool)