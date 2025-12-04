from typing import List, Dict, Any, Optional

from loguru import logger
from langchain_core.documents import Document
from langgraph.graph import END, START, StateGraph

from utils.utils import create_llm
from Agent.prompt import agent_prompt
from Agent.model import StructuredAgentResponse
from utils.states import WorkingState

# -----------------------------------------
# Node: Generate Response
# -----------------------------------------
def agent(state: WorkingState) -> WorkingState:
    """
    Generate the LLM response based on the question, chat history, and retrieved context.
    """
    logger.info("Executing: Agent...")

    question: Optional[str] = state.get("question")
    page_url: Optional[str] = state.get("page_url")
    frontend_origin: Optional[str] = state.get("frontend_origin")
    full_url = f"{frontend_origin}/{page_url}"
    messages: Optional[List[Dict[str, Any]]] = state.get("messages")
    
    if not question:
        raise ValueError("Missing 'question' in state.")

    llm = create_llm()
    
    if llm is None:
        raise RuntimeError("create_llm() returned None. Cannot proceed.")

    try:
        agent_llm = llm.with_structured_output(
            StructuredAgentResponse,
            method="function_calling"
        )
        chain = agent_prompt | agent_llm

        model_output = chain.invoke(
            {
                "question": question,
                "messages": messages,
                "page_url": full_url
            }
        )

    except Exception as exc:
        logger.exception("LLM generation error.")
        raise RuntimeError(f"LLM generation failed: {exc}") from exc

    response_dict = model_output.model_dump()
        
    response_text = response_dict.get("response")
    route_to = response_dict.get("next")

    if not response_text:
        raise ValueError("StructuredResponse did not return 'response'.")

    if route_to == "finalize_output":
        state["generation"] = response_text
    else:
        state["question"] = response_text
        
    state["next"] = route_to
    
    return state


# -----------------------------------------
# Graph Assembly
# -----------------------------------------
agent_graph = StateGraph(WorkingState)

agent_graph.add_node("agent", agent)

agent_graph.add_edge(START, "agent")
agent_graph.add_edge("agent", END)

agent_graph = agent_graph.compile()
