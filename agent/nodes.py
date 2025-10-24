from utils import initialize_llm
from navigater.state import ParentState
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from navigater.state import ParentState
from typing import Literal, Dict, Any
# from agent.prompts import agent_prompt
# from agent.tools import tools


# def route_agent(state: ParentState) -> Dict[str, Any]:
#     """Node: Main routing agent that decides which tool to use based on prompt"""
#     print("🧭 Routing agent running...")

#     # Initialize the LLM
#     llm= initialize_llm(temperature=0.0, temperature_required=True)

#     # Prepare the chat history
#     chat_history_str = "\n".join([
#         f"User: {msg.content}" if isinstance(msg, HumanMessage)
#         else f"Assistant: {msg.content}"
#         for msg in state.messages
#     ])

#     # Format the prompt
#     formatted_prompt = agent_prompt.format(
#         tools="\n".join([t.name for t in tools]),  # all available tools
#         tool_names=", ".join([t.name for t in tools]),
#         page_url=state.page_url,
#         chat_history=chat_history_str,
#         input=state.user_query,
#         agent_scratchpad=""
#     )

#     # Invoke the LLM
#     raw_response = llm.invoke(formatted_prompt)
#     agent_output = StrOutputParser().parse(raw_response)

#     print("📤 Agent output:", agent_output[:200])  # truncate for logging

#     # Return new messages (LangGraph auto-adds them)
#     return {
#         "agent_output": agent_output,
#         "messages": [
#             HumanMessage(content=state.user_query),
#             AIMessage(content=agent_output)
#         ]
#     }
def route_agent(state: ParentState) -> ParentState:
    agent_output = "to tool B"
    state.messages.append(HumanMessage(content=state.user_query))
    state.messages.append(AIMessage(content=agent_output))
    state.agent_output = agent_output
    return state

