from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from navigater.state import State
from navigater.prompt import route_user_query
from navigater.nodes import (
    handle_redirect,
    llm_fallback,
    call_your_agent,
    sql_qa_tool,
    contract_comparator_tool,
    spinnaker_qa_tool,
    route_condition,
    tool_router,
    fallback_condition,
    spinnaker_questions,
    general_questions,
    execute_sql,
    generate_response,
)

from langgraph.graph import StateGraph, END

# Build the workflow
workflow_route = StateGraph(State)

# Add nodes
workflow_route.add_node("route_query", route_user_query)
workflow_route.add_node("handle_redirect", handle_redirect)
workflow_route.add_node("llm_fallback", llm_fallback)
workflow_route.add_node("call_agent", call_your_agent)
workflow_route.add_node("fallback_condition", fallback_condition)
workflow_route.add_node("spinnaker_questions", spinnaker_questions)
workflow_route.add_node("general_questions", general_questions)
workflow_route.add_node("generate_response", generate_response)


# Add tool nodes
workflow_route.add_node("sql_qa_tool", sql_qa_tool)
workflow_route.add_node("contract_comparator_tool", contract_comparator_tool)
workflow_route.add_node("spinnaker_qa_tool", spinnaker_qa_tool)
workflow_route.add_node("execute_sql", execute_sql)

# Set entry point
workflow_route.set_entry_point("route_query")

# Add conditional edges from route_query
workflow_route.add_conditional_edges(
    "route_query",
    route_condition,
    {
        "call_agent": "call_agent",
        "handle_redirect": "handle_redirect",
        "llm_fallback": "llm_fallback",
    },
)

workflow_route.add_conditional_edges(
    "llm_fallback",
    fallback_condition,
    {
        "spinnaker_questions": "spinnaker_questions",
        "general_questions": "general_questions",
    },
)

# Add conditional edges from call_agent to tools
workflow_route.add_conditional_edges(
    "call_agent",
    tool_router,  # This function decides which tool based on state["selected_tool"]
    {
        "sql_qa_tool": "sql_qa_tool",
        "contract_comparator_tool": "contract_comparator_tool",
        "spinnaker_qa_tool": "spinnaker_qa_tool",
    },
)

# All endpoints go to END
workflow_route.add_edge("sql_qa_tool", "execute_sql")
workflow_route.add_edge("execute_sql", "generate_response")
workflow_route.add_edge("execute_sql", END)
workflow_route.add_edge("generate_response", END)
workflow_route.add_edge("handle_redirect", END)
workflow_route.add_edge("llm_fallback", END)
workflow_route.add_edge("sql_qa_tool", END)
workflow_route.add_edge("contract_comparator_tool", END)
workflow_route.add_edge("spinnaker_questions", END)
workflow_route.add_edge("general_questions", END)

# Compile the graph
app_route = workflow_route.compile()
