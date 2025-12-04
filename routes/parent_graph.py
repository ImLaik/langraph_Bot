from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from loguru import logger

from parent_graph.graph import parent_graph
from utils.states import OutputState
from utils.utils import finalize_to_output
import os

ENVIRONMENT = os.getenv("ENVIRONMENT")

# ---------------------------------------------------------------------------
# Request Model
# ---------------------------------------------------------------------------
class InputState(BaseModel):
    question: str = Field(..., description="User question")
    page_url: str = Field(..., description="Page URL")
    frontend_origin: Optional[str] = None

    contracts: Optional[List[Dict[str, Any]]] = []
    metrics: Optional[List[str]] = []

    session_id: str = Field(..., description="User's question.")

    product: Optional[str] = None


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
router = APIRouter()


@router.post("/master_bot/queries", response_model=OutputState, summary="Execute Master Bot Graph")
async def master_bot_query(request:Request, payload: InputState):
    """
    Executes the parent LangGraph workflow with the provided input state.
    Ensures consistent conversion of the graph's WorkingState to OutputState.
    """
    logger.info("Received master bot request")

    try:
        payload = payload.model_dump()
        
        session_id = payload.get("session_id")
        frontend_origin = "https://www.spinnakerhub.com"
        

        if ENVIRONMENT == "development":
            frontend_origin = "http://localhost:3000"
            
        payload["frontend_origin"] = frontend_origin
        # Bind input/output types to graph
        typed_graph = parent_graph.with_types(
            input_type=InputState,
            output_type=OutputState,
        )

        # Execute graph
        raw_state = typed_graph.invoke(payload, config={"configurable": {"thread_id": session_id}})

        # Normalize output
        if isinstance(raw_state, dict):
            output = finalize_to_output(raw_state)
        elif isinstance(raw_state, OutputState):
            output = raw_state
        else:
            logger.error(f"Unexpected graph output type: {type(raw_state)}")
            raise TypeError("Graph returned an invalid output type")

        logger.info("Master bot query executed successfully")
        return output

    except Exception as exc:
        logger.exception(f"Master bot request failed: {exc}")
        raise HTTPException(status_code=500, detail="Internal error during graph execution")
