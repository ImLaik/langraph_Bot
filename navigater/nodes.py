from navigater.state import ParentState
from utils import initialize_llm
from navigater.prompt import master_router_prompt
from langchain_core.messages import HumanMessage, AIMessage
from typing import Literal, Dict, Any
from langgraph.prebuilt import create_react_agent
# from langchain.agents import AgentExecutor
from langchain_core.output_parsers import JsonOutputParser
from agent.prompts import agent_prompt
# from agent.tools import tools
from agent.graph import agent_graph
import json

def route_user_query(state: ParentState) -> Dict[str, Any]:
    """
    Node 1: Route the user query using the master router prompt
    """
    print("🔍 Routing user query...")
    
    llm = initialize_llm(temperature=0.0, temperature_required=True)
    

    # JsonOutputParser() already returns a dict, so you don't need json.loads()
    routing_chain = master_router_prompt | llm | JsonOutputParser()
    routing_data = routing_chain.invoke({
        "user_query": state.user_query,
        "page_url": state.page_url,
        "frontend_origin": state.frontend_origin,
        "chat_history": state["messages"]  
    })
    
    # P;arse JSON response
    try:
        print(f"✅ Routing complete: is_correct_location = {routing_data.get('is_correct_location', True)}")
        
        # Return dict to update state
        return {
            "routing_response": routing_data,
            "is_correct_location": routing_data.get("is_correct_location", True),
            "is_incorrect_location_msg": routing_data.get("is_incorrect_location_msg")
        }
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing routing response: {e}")
        # Default to correct location on error
        return {
            "is_correct_location": True,
            "is_incorrect_location_msg": None,
            "routing_response": {
                "is_correct_location": True,
                "is_incorrect_location_msg": None
            }
        }


def handle_incorrect_location(state: ParentState) -> Dict[str, Any]:
    """
    Node 2: Handle incorrect location by returning redirect message
    """
    print("⚠️ User is in incorrect location. Sending redirect message...")
    
    # Return dict to update state
    return {
        "final_response": state.is_incorrect_location_msg or "Please navigate to the correct page."
    }

def call_your_agent(state: ParentState) -> Dict[str, Any]:
    """Node 3: Call agent and store in temp field"""
    print("🤖 Calling graph agent directly...")

    # llm = initialize_llm(temperature=0.0, temperature_required=True)

    # Format chat history
    chat_history_str = "\n".join([
        f"User: {msg.content}" if isinstance(msg, HumanMessage)
        else f"Assistant: {msg.content}"
        for msg in state["messages"]
    ])

    # Build and invoke your graph
    graph = agent_graph()
    graph_result = graph.invoke({
        "input": state["user_query"],
        "page_url": state["page_url"],
        "chat_history": chat_history_str
    })

    return {
        "agent_output": graph_result,
        "messages": [
            HumanMessage(content=state.user_query),
            AIMessage(content=graph_result)
        ]
    }

def router_decision(state: ParentState) -> Literal["call_agent", "redirect"]:
    """
    Conditional edge: Decide whether to call agent or redirect
    """
    # Use direct attribute access
    if state.is_correct_location:
        return "call_agent"
    else:
        return "redirect"