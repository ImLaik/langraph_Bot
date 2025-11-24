from typing import Dict, Any
from loguru import logger
from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver

from utils.utils import invoke_with_logging, log_function, get_relevant_catalog_context, sql_agent_to_parent, parent_to_sql_agent
from parent_graph.state import ParentState
from query_router.query_router import question_router
from tool_calling_graph.graph import tool_calling_agent_graph
from tools.sql_agent.graph import sql_agent_graph
from tools.contract_comparator.graph import contract_comparator_graph

def handle_redirect(state: ParentState) -> ParentState:
    logger.info("Redirect node triggered.")
    return state


def llm_fallback_graph(state: ParentState) -> ParentState:
    logger.info("LLM fallback node triggered.")
    return state


@log_function
def route_question(state: ParentState) -> Dict[str, Any]:
    """
    Route the question to redirect, tool-calling agent, or fallback LLM.

    Returns:
        dict with keys:
        - next: name of downstream graph node
        - generation: only when redirecting
    """
    logger.info("Starting route_question...")

    question = state.get("question")
    page_url = state.get("page_url")
    frontend_origin = state.get("frontend_origin")
    messages = state.get("messages", [])

    # Retrieve context from catalog
    try:
        catalog_context = get_relevant_catalog_context(question, page_url)
    except Exception as e:
        logger.error(f"Failed retrieving catalog context: {e}")
        raise RuntimeError("Catalog context retrieval failed.") from e

    # Invoke router chain
    try:
        response = invoke_with_logging(
            question_router.invoke,
            {
                "question": question,
                "page_url": page_url,
                "frontend_origin": frontend_origin,
                "messages": messages,
                "catalog_context": catalog_context,
            },
            "question_router"
        )
    except Exception as e:
        logger.error(f"Router invocation failed: {e}")
        raise RuntimeError("Router invocation failed.") from e

    response_dict = response.model_dump()
    is_correct_location = response_dict.get("is_correct_location")

    logger.debug(f"Router response: {response_dict}")

    # Redirect branch
    if not is_correct_location:
        incorrect_msg = response_dict.get("is_incorrect_location_msg")
        if not incorrect_msg:
            logger.warning("Router returned incorrect_location but no message. Using fallback.")
            incorrect_msg = "You are viewing the wrong location."

        logger.info("Routing user to redirect flow.")
        return {
            "generation": incorrect_msg,
            "next": "handle_redirect"
        }

    # Correct location → Tool calling agent
    logger.info("Routing to tool_calling_agent_graph.")
    return {"next": "tool_calling_agent_graph"}

parent_graph_builder = StateGraph(ParentState)

# Register nodes
parent_graph_builder.add_node("handle_redirect", handle_redirect)
parent_graph_builder.add_node("tool_calling_agent_graph", tool_calling_agent_graph)
parent_graph_builder.add_node("llm_fallback_graph", llm_fallback_graph)
parent_graph_builder.add_node("route_question", route_question)
# parent_graph_builder.add_node("sql_agent_graph", sql_agent_graph)
parent_graph_builder.add_node(
    "sql_agent_graph",
    lambda parent_state: sql_agent_to_parent(sql_agent_graph.invoke(parent_to_sql_agent(parent_state)))
)
parent_graph_builder.add_node("contract_comparator_graph", contract_comparator_graph)


# Conditional Routing
parent_graph_builder.add_conditional_edges(
    "route_question",
    lambda state: state["next"],
    {
        "handle_redirect": "handle_redirect",
        "tool_calling_agent_graph": "tool_calling_agent_graph",
        "llm_fallback_graph": "llm_fallback_graph"
    },
)

parent_graph_builder.add_conditional_edges(
    "tool_calling_agent_graph",
    lambda state: state["next"],
    {
        "sql_tool": "sql_agent_graph",
        "contract_comparator": "contract_comparator_graph",
        "llm_fallback_graph": "llm_fallback_graph"
    },
)

# Graph entry/exit
parent_graph_builder.add_edge(START, "route_question")
parent_graph_builder.add_edge("handle_redirect", END)
parent_graph_builder.add_edge("sql_agent_graph", END)
parent_graph_builder.add_edge("contract_comparator_graph", END)
parent_graph_builder.add_edge("llm_fallback_graph", END)

memory = MemorySaver()
parent_graph = parent_graph_builder.compile()

# # Generate the PNG data from your graph
# png_data = parent_graph.get_graph(xray=1).draw_mermaid_png()

# # Save the PNG data to a file in binary mode
# with open("parent_graph/parent_graph.png", "wb") as file:
#     file.write(png_data)

# print("Graph saved as parent_graph.png")