from langgraph.graph import StateGraph, START, END

from app.agents.state import AgentState
from app.tools.llm_tool import llm_tool
from app.tools.search_tool import search_tool
from app.tools.router_tool import router_tool
from app.tools.email_tool import email_tool
from app.tools.analytics_tool import analytics_tool
from app.tools.document_tool import document_tool


def router_node(state: AgentState):

    message = state["message"]

    # Never route large text blocks back into search
    if (
        len(message) > 400
        or "Title:" in message
        or "URL:" in message
        or "Content:" in message
    ):
        tool = "llm"
    else:
        tool = router_tool.execute(message)

    return {
        **state,
        "tool": tool
    }

def llm_node(state: AgentState):

    response = llm_tool.execute(
        message=state["message"],
        history=state["history"]
    )

    return {
        **state,
        "response": response
    }


def search_node(state: AgentState):

    search_results = search_tool.execute(state["message"])

    prompt = f"""
    Use the following search results to answer the user's question.

    Search Results

    {search_results}

    Question

    {state['message']}
    """

    response = llm_tool.execute(prompt)

    return {
        **state,
        "response": response
    }

def email_node(state: AgentState):

    response = email_tool.execute(
        message=state["message"],
        session_id=state["session_id"]
    )

    return {
        **state,
        "response": response
    }
    
def analytics_node(state: AgentState):

    response = analytics_tool.execute(
        state["message"]
    )

    return {
        **state,
        "response": response
    }    

def document_node(state: AgentState):

    result = document_tool.execute(
        state["message"]
    )

    return {
        **state,
        "response": result["message"],
        "file": result["file"]
    }
    
builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("llm", llm_node)
builder.add_node("search", search_node)
builder.add_node("email", email_node)
builder.add_node("analytics", analytics_node)
builder.add_node("document", document_node)
builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    lambda state: state["tool"],
    {
        "llm": "llm",
        "search": "search",
        "email": "email",
         "analytics": "analytics",
         "document": "document",
    }
)

builder.add_edge("llm", END)
builder.add_edge("search", END)
builder.add_edge("email", END)
builder.add_edge("analytics", END)
builder.add_edge("document", END)

graph = builder.compile()