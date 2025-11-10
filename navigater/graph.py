from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from navigater.state import State
from navigater.prompt import route_user_query
from navigater.nodes import handle_redirect,llm_fallback,call_your_agent,sql_qa_tool,contract_comparator_tool,spinnaker_qa_tool,route_condition,tool_router

from langgraph.graph import StateGraph, END

# Build the workflow
workflow_route = StateGraph(State)

# Add nodes
workflow_route.add_node("route_query", route_user_query)
workflow_route.add_node("handle_redirect", handle_redirect)
workflow_route.add_node("llm_fallback", llm_fallback)
workflow_route.add_node("call_agent", call_your_agent)

# Add tool nodes
workflow_route.add_node("sql_qa_tool", sql_qa_tool)
workflow_route.add_node("contract_comparator_tool", contract_comparator_tool)
workflow_route.add_node("spinnaker_qa_tool", spinnaker_qa_tool)

# Set entry point
workflow_route.set_entry_point("route_query")

# Add conditional edges from route_query
workflow_route.add_conditional_edges(
    "route_query",
    route_condition,
    {
        "call_agent": "call_agent",
        "handle_redirect": "handle_redirect",
        "llm_fallback": "llm_fallback"
    }
)

# Add conditional edges from call_agent to tools
workflow_route.add_conditional_edges(
    "call_agent",
    tool_router,  # This function decides which tool based on state["selected_tool"]
    {
        "sql_qa_tool": "sql_qa_tool",
        "contract_comparator_tool": "contract_comparator_tool",
        "spinnaker_qa_tool": "spinnaker_qa_tool"
    }
)

# All endpoints go to END
workflow_route.add_edge("handle_redirect", END)
workflow_route.add_edge("llm_fallback", END)
workflow_route.add_edge("sql_qa_tool", END)
workflow_route.add_edge("contract_comparator_tool", END)
workflow_route.add_edge("spinnaker_qa_tool", END)

# Compile the graph
app_route = workflow_route.compile()
