from typing import Dict, Any, Callable, Optional, Mapping, List
from loguru import logger
from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver

from utils.utils import (
    invoke_with_logging,
    get_relevant_catalog_context,
    call_subgraph_preserving_state,
    append_model_message,
    append_user_message,
    handle_redirect,
    finalize_node,   
)
from query_router.query_router import question_router
from tool_calling_graph.graph import tool_calling_agent_graph
from tools.sql_agent.graph import sql_agent_graph
from tools.contract_comparator.graph import contract_comparator_graph
from llm_fallback.graph import llm_fallback_graph
from tools.image_tool.graph import image_tool_graph
from utils.states import WorkingState
from Agent.graph import agent_graph

# Node name constants
NODE_UPDATE_USER_MESSAGES = "append_user_message"
NODE_AGENT = "agent_graph"
NODE_HANDLE_REDIRECT = "handle_redirect"
NODE_ROUTE_QUESTION = "route_question"
NODE_TOOL_CALLING_AGENT = "tool_calling_agent_graph"
NODE_SQL_AGENT = "sql_agent_graph"
NODE_CONTRACT_COMPARATOR = "contract_comparator_graph"
NODE_IMAGE_TOOL = "image_tool_graph"
NODE_LLM_FALLBACK = "llm_fallback_graph"
NODE_APPEND_MODEL_MESSAGE = "append_model_message"
NODE_FINALIZE = "finalize_output"


# ---------------------------------------------------------------------------
# Router node
# ---------------------------------------------------------------------------
def route_question(state: WorkingState) -> Dict[str, Any]:
    """
    Route the question to redirect, tool-calling agent, or fallback LLM.

    Returns a dictionary that must contain at least the key 'next' with one of:
      - NODE_HANDLE_REDIRECT
      - NODE_TOOL_CALLING_AGENT
      - NODE_LLM_FALLBACK

    Optionally may include 'generation' (when redirecting) and other fields.
    """
    logger.info("Starting route_question")

    question = state.get("question")
    page_url = state.get("page_url")
    frontend_origin = state.get("frontend_origin")
    messages = state.get("messages", [])
    
    if not question:
        logger.error("route_question: missing 'question' in state")
        raise ValueError("Missing 'question' in state.")

    # Retrieve context from product/catalog
    try:
        catalog_context = get_relevant_catalog_context(question, page_url)
        print(f"\n\nCatalog Context: {catalog_context}\n\n")
        logger.debug("Catalog context retrieved.")
    except Exception as exc:
        logger.exception("Failed retrieving catalog context.")
        raise RuntimeError("Catalog context retrieval failed.") from exc

    # Invoke the router with logging wrapper
    try:
        router_response = invoke_with_logging(
            question_router.invoke,
            {
                "question": question,
                "page_url": page_url,
                "frontend_origin": frontend_origin,
                "messages": messages,
                "catalog_context": catalog_context,
            },
            "question_router",
        )
    except Exception as exc:
        logger.exception("Router invocation failed.")
        raise RuntimeError("Router invocation failed.") from exc

    # Normalize router response to dict
    try:
        response_dict: Mapping[str, Any]
        if hasattr(router_response, "model_dump"):
            response_dict = router_response.model_dump()
        elif isinstance(router_response, dict):
            response_dict = router_response
        else:
            # Fallback: attempt to transform to dict
            response_dict = dict(router_response)  # may raise
    except Exception as exc:
        logger.exception("Failed to normalize router response to dict.")
        raise RuntimeError("Invalid router response format.") from exc

    logger.debug("Router response (normalized): {}", response_dict)

    is_correct_location = response_dict.get("is_correct_location")
    route_to = response_dict.get("route_to")

    # Validate route target
    if not route_to:
        logger.warning("Router did not return 'route_to'; using fallback LLM.")
        return {"next": NODE_LLM_FALLBACK}

    # Redirect branch (explicit incorrect location)
    if (is_correct_location is False) and (route_to == "handle_redirect"):
        incorrect_msg = (
            response_dict.get("is_incorrect_location_msg")
            or "You are viewing the wrong location."
        )
        logger.info("Routing to redirect flow with message.")
        # ensure the redirect message is set as the generation so append_model_message will persist it
        return {
            "tool_info": state.get("tool_info"),
            "selected_tool": state.get("selected_tool"),
            "generation": incorrect_msg,
            "next": NODE_HANDLE_REDIRECT,
        }

    # Tool-calling agent path
    if route_to == "tool_calling_agent":
        logger.info("Routing to tool_calling_agent_graph.")
        return {"next": NODE_TOOL_CALLING_AGENT}

    # Default fallback path
    logger.info("Routing to LLM fallback graph.")
    return {"next": NODE_LLM_FALLBACK}



# ---------------------------------------------------------------------------
# Graph builder (returns compiled graph)
# ---------------------------------------------------------------------------
def build_parent_graph() -> StateGraph:
    """
    Build and compile the parent graph. This function is safe to call multiple times
    (compiles a new graph instance each call).
    """
    parent_graph_builder = StateGraph(WorkingState)

    # Register nodes
    parent_graph_builder.add_node(NODE_UPDATE_USER_MESSAGES, append_user_message)
    parent_graph_builder.add_node(NODE_HANDLE_REDIRECT, handle_redirect)
    parent_graph_builder.add_node(NODE_ROUTE_QUESTION, route_question)

    parent_graph_builder.add_node(
        NODE_AGENT,
        lambda state: call_subgraph_preserving_state(agent_graph, state, "agent_graph"),
    )
    parent_graph_builder.add_node(
        NODE_TOOL_CALLING_AGENT,
        lambda state: call_subgraph_preserving_state(
            tool_calling_agent_graph, state, "tool_calling_agent_graph"
        ),
    )
    parent_graph_builder.add_node(
        NODE_SQL_AGENT,
        lambda state: call_subgraph_preserving_state(sql_agent_graph, state, "sql_agent_graph"),
    )
    parent_graph_builder.add_node(
        NODE_LLM_FALLBACK,
        lambda state: call_subgraph_preserving_state(llm_fallback_graph, state, "llm_fallback_graph"),
    )
    parent_graph_builder.add_node(
        NODE_CONTRACT_COMPARATOR,
        lambda state: call_subgraph_preserving_state(
            contract_comparator_graph, state, "contract_comparator_graph"
        ),
    )
    parent_graph_builder.add_node(
        NODE_IMAGE_TOOL,
        lambda state: call_subgraph_preserving_state(image_tool_graph, state, "image_tool_graph"),
    )

    parent_graph_builder.add_node(NODE_APPEND_MODEL_MESSAGE, append_model_message)
    parent_graph_builder.add_node(NODE_FINALIZE, finalize_node)
    
    parent_graph_builder.add_conditional_edges(
        NODE_AGENT,
        lambda state: state["next"],
        {
            "route_question": NODE_ROUTE_QUESTION,
            "finalize_output": NODE_FINALIZE
        },
    )

    # Conditional routing from the router node
    parent_graph_builder.add_conditional_edges(
        NODE_ROUTE_QUESTION,
        lambda state: state["next"],
        {
            "handle_redirect": NODE_HANDLE_REDIRECT,
            "tool_calling_agent_graph": NODE_TOOL_CALLING_AGENT,
            "llm_fallback_graph": NODE_LLM_FALLBACK,
        },
    )

    # Conditional routing for tool_calling_agent_graph -> choose specific tool chains
    parent_graph_builder.add_conditional_edges(
        NODE_TOOL_CALLING_AGENT,
        lambda state: state["next"],
        {
            "sql_tool": NODE_SQL_AGENT,
            "contract_comparator": NODE_CONTRACT_COMPARATOR,
            "image_tool": NODE_IMAGE_TOOL,
            "llm_fallback_graph": NODE_LLM_FALLBACK,
        },
    )

    # Graph topology
    # Ensure user message is appended immediately after START
    parent_graph_builder.add_edge(START, NODE_UPDATE_USER_MESSAGES)
    parent_graph_builder.add_edge(NODE_UPDATE_USER_MESSAGES, NODE_AGENT)

    # After routing/handling/tool chains, flow should go to append_model_message -> finalize -> END
    parent_graph_builder.add_edge(NODE_HANDLE_REDIRECT, NODE_APPEND_MODEL_MESSAGE)
    parent_graph_builder.add_edge(NODE_SQL_AGENT, NODE_APPEND_MODEL_MESSAGE)
    parent_graph_builder.add_edge(NODE_CONTRACT_COMPARATOR, NODE_APPEND_MODEL_MESSAGE)
    parent_graph_builder.add_edge(NODE_LLM_FALLBACK, NODE_APPEND_MODEL_MESSAGE)
    parent_graph_builder.add_edge(NODE_IMAGE_TOOL, NODE_APPEND_MODEL_MESSAGE)

    parent_graph_builder.add_edge(NODE_APPEND_MODEL_MESSAGE, NODE_FINALIZE)
    parent_graph_builder.add_edge(NODE_FINALIZE, END)

    # Memory saver hookup (stores state snapshots keyed by thread_id from config)
    memory = MemorySaver()
    compiled = parent_graph_builder.compile(checkpointer=memory)

    logger.info("Parent graph built and compiled.")
    return compiled


# Build graph at module import time
parent_graph = build_parent_graph()



# # Generate the PNG data from your graph
# png_data = parent_graph.get_graph(xray=1).draw_mermaid_png()

# # Save the PNG data to a file in binary mode
# with open("parent_graph/parent_graph.png", "wb") as file:
#     file.write(png_data)

# print("Graph saved as parent_graph.png")
