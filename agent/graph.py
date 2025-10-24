# graph.py
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from navigater.state import ParentState
from agent.nodes import route_agent

def build_graph():
    """Build and compile the LangGraph routing agent"""
    graph = StateGraph(ParentState)
    
    # Add node
    graph.add_node("route_agent", route_agent)
    
    # Define entry & end
    graph.set_entry_point("route_agent")
    graph.add_edge("route_agent", END)
    
    # Compile
    return graph.compile()
agent_graph =build_graph()


