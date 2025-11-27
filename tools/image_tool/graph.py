import json
from typing import Dict, Any, List, Optional

from loguru import logger
from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph

from utils.utils import (
    create_llm,
    invoke_with_logging,
    parse_array_str,
)
from tools.image_tool.prompt import build_prompt
from tools.image_tool.model import ImageTool
from utils.states import WorkingState


# ---------------------------------------------------------------------------
# NODE: Image Tool Response Generator
# ---------------------------------------------------------------------------
def generate_response(state: WorkingState) -> WorkingState:
    logger.info("Image tool invoked")

    try:
        tool_info: Dict[str, Any] | None = state.get("tool_info")
        if not tool_info:
            raise ValueError("Missing `tool_info` in state")

        question: Optional[str] = state.get("question")
        if not question:
            raise ValueError("Missing `question` in state")

        messages: List[Dict[str, Any]] | None = state.get("messages", [])
        if messages is None:
            messages = []

        # Parse image URLs input
        raw_urls = tool_info.get("image_urls")
        image_urls = parse_array_str(raw_urls)

        if not image_urls:
            logger.warning("Image tool received empty or invalid image URL list")

        # Construct prompt
        prompt = build_prompt(image_urls, question, messages)

        # Create LLM once for this node execution
        llm = create_llm()
        structured_llm = llm.with_structured_output(
            ImageTool,
            method="function_calling",
        )

        chain = prompt | structured_llm

        response = invoke_with_logging(
            chain.invoke,
            {
                "question": question,
                "image_urls": image_urls,
                "chat_history": messages,
            },
            "ImageTool",
        )

        response_dict = response.model_dump()

        final_output = response_dict.get("response")
        if not final_output:
            raise RuntimeError("LLM returned no `response` field in structured output")

        state["generation"] = final_output
        logger.info("Image tool completed successfully")

        return state

    except Exception as exc:
        logger.exception("Image tool failed")
        state["error"] = f"Image tool failed: {exc}"
        return state


# ---------------------------------------------------------------------------
# GRAPH DEFINITION
# ---------------------------------------------------------------------------
graph_builder = StateGraph(WorkingState)

graph_builder.add_node("generate_response", generate_response)

graph_builder.add_edge(START, "generate_response")
graph_builder.add_edge("generate_response", END)

image_tool_graph = graph_builder.compile()
