from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from navigater.state import ParentState
from navigater.nodes import route_user_query,handle_incorrect_location,call_your_agent,router_decision

def create_routing_graph():
    """Create and compile the routing graph"""
    
    # Initialize graph
    workflow = StateGraph(ParentState)
    
    # Add nodes
    workflow.add_node("route_query", route_user_query)
    workflow.add_node("handle_redirect", handle_incorrect_location)
    workflow.add_node("call_agent", call_your_agent)
    
    # Set entry point
    workflow.set_entry_point("route_query")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "route_query",
        router_decision,
        {
            "call_agent": "call_agent",
            "redirect": "handle_redirect"
        }
    )
    
    # Add edges to END
    workflow.add_edge("call_agent", END)
    workflow.add_edge("handle_redirect", END)
    
    # Compile graph
    return workflow.compile()
master_graph = create_routing_graph()
