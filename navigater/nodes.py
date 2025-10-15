from navigater.state import ParentState
from utils import initialize_llm
from navigater.prompt import master_router_prompt
from langchain_core.messages import HumanMessage, AIMessage
from typing import Literal, Dict, Any
from langchain_core.output_parsers import JsonOutputParser
# from agent.tools import tools
# from langchain.agents import AgentExecutor, create_react_agent
# from agent.prompts import agent_prompt
import json

def route_user_query(state: ParentState) -> Dict[str, Any]:
    """
    Node 1: Route the user query using the master router prompt
    """
    print("🔍 Routing user query...")
    
    llm = initialize_llm(temperature=0.0, temperature_required=True)
    
    # Format chat history - use direct attribute access
    formatted_history = []
    for msg in state.chat_history:
        if isinstance(msg, dict):
            if msg.get("role") == "user":
                formatted_history.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                formatted_history.append(AIMessage(content=msg.get("content", "")))

    # JsonOutputParser() already returns a dict, so you don't need json.loads()
    routing_chain = master_router_prompt | llm | JsonOutputParser()
    routing_data = routing_chain.invoke({
        "user_query": state.user_query,
        "page_url": state.page_url,
        "frontend_origin": state.frontend_origin,
        "chat_history": formatted_history
    })
    
    # Parse JSON response
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
    """
    Node 3: Call your main agent when user is in correct location
    """
    print("🤖 User is in correct location. Calling main agent...")
    

    #  actual agent
    
    agent_response = f"""
    Processing your query: "{state.user_query}"
    
    Current location: {state.page_url}
    
    [Your agent's actual response would go here]
    """
    
    # Return dict to update state
    return {
        "final_response": agent_response.strip()
    }
# def call_your_agent(state: ParentState) -> Dict[str, Any]:
#     """Node 3: Call your main agent when user is in correct location"""
#     print("🤖 User is in correct location. Calling main agent...")
    
#     llm = initialize_llm(temperature=0.0, temperature_required=True)
    
#     # Create ReAct agent
#     agent = create_react_agent(
#         llm=llm,
#         tools=tools,
#         prompt=agent_prompt
#     )
    
#     # Create agent executor
#     agent_executor = AgentExecutor(
#         agent=agent,
#         tools=tools,
#         verbose=True,
#         handle_parsing_errors=True,
#         max_iterations=5
#     )
    
#     # Format chat history
#     chat_history_str = ""
#     for msg in state.chat_history:
#         if isinstance(msg, dict):
#             role = msg.get("role", "")
#             content = msg.get("content", "")
#             chat_history_str += f"{role}: {content}\n"
    
#     # Prepare agent input
#     agent_input = {
#         "input": state.user_query,
#         "page_url": state.page_url,
#         "chat_history": chat_history_str,
#         "tools": "\n".join([f"- {tool.name}: {tool.description}" for tool in tools]),
#         "tool_names": ", ".join([tool.name for tool in tools])
#     }
    
#     try:
#         result = agent_executor.invoke(agent_input)
#         final_response = result.get("output", "I couldn't process your request.")
        
#         print(f"✅ Agent completed successfully")
        
#         return {
#             "final_response": final_response
#         }
        
#     except Exception as e:
#         print(f"❌ Error in agent execution: {e}")
#         return {
#             "final_response": f"I encountered an error: {str(e)}"
#         }


def router_decision(state: ParentState) -> Literal["call_agent", "redirect"]:
    """
    Conditional edge: Decide whether to call agent or redirect
    """
    # Use direct attribute access
    if state.is_correct_location:
        return "call_agent"
    else:
        return "redirect"