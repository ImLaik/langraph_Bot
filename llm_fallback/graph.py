from typing import List, Dict, Any, Optional

from loguru import logger
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END, START, StateGraph

from utils.utils import load_vector_retriever, create_llm
from llm_fallback.prompt import prompt
from llm_fallback.model import StructuredResponse
from utils.states import WorkingState


# -----------------------------------------
# Node: Retrieve Documents
# -----------------------------------------
def get_docs(state: WorkingState) -> WorkingState:
    """
    Retrieve relevant documents for a given question using the configured vector store.
    """
    logger.info("Executing: LLM Fallback...")

    question = state.get("question")
    if not question:
        raise ValueError("Missing 'question' in state. Cannot retrieve documents.")

    vector_store, retriever = load_vector_retriever()
    if retriever is None:
        raise RuntimeError("Vector retriever not initialized properly.")

    try:
        docs: List[Document] = retriever._get_relevant_documents(question, run_manager=None)
        logger.debug(f"Retrieved {len(docs)} documents for question.")
    except Exception as exc:
        logger.exception("Error while retrieving documents.")
        raise RuntimeError(f"Document retrieval failed: {exc}") from exc

    return {"context": docs}


# -----------------------------------------
# Node: Generate Response
# -----------------------------------------
def generate_response(state: WorkingState) -> WorkingState:
    """
    Generate the LLM response based on the question, chat history, and retrieved context.
    """

    question: Optional[str] = state.get("question")
    messages: Optional[List[Dict[str, Any]]] = state.get("messages")
    context: Optional[List[Document]] = state.get("context")

    if not question:
        raise ValueError("Missing 'question' in state.")

    if context is None:
        logger.warning("No context provided to generate_response. Proceeding without context.")

    llm = create_llm()
    
    if llm is None:
        raise RuntimeError("create_llm() returned None. Cannot proceed.")

    try:
        router_llm = llm.with_structured_output(
            StructuredResponse,
            method="function_calling"
        )
        chain = prompt | router_llm

        model_output = chain.invoke(
            {
                "question": question,
                "messages": messages,
                "context": context,
            }
        )

    except Exception as exc:
        logger.exception("LLM generation error.")
        raise RuntimeError(f"LLM generation failed: {exc}") from exc

    response_dict = model_output.model_dump()
    response_text = response_dict.get("response")

    if not response_text:
        raise ValueError("StructuredResponse did not return 'response'.")

    state["generation"] = response_text
    logger.info("Executed: LLM fallback executed successfully")
    return state


# -----------------------------------------
# Graph Assembly
# -----------------------------------------
llm_fallback_graph = StateGraph(WorkingState)

llm_fallback_graph.add_node("get_docs", get_docs)
llm_fallback_graph.add_node("generate_response", generate_response)

llm_fallback_graph.add_edge(START, "get_docs")
llm_fallback_graph.add_edge("get_docs", "generate_response")
llm_fallback_graph.add_edge("generate_response", END)

llm_fallback_graph = llm_fallback_graph.compile()
