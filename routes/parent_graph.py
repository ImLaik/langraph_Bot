from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from loguru import logger

from parent_graph.graph import parent_graph
from utils.states import OutputState
from utils.utils import finalize_to_output
from db.redis import redis_client
import copy
import json
import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
DEV_URI = os.getenv("DEV_URI", "http://localhost:3000")
PROD_URI = os.getenv("PROD_URI")


# ---------------------------------------------------------------------------
# Request Model
# ---------------------------------------------------------------------------
class InputState(BaseModel):
    question: str = Field(..., description="User question")
    page_url: str = Field(..., description="Originating page URL")
    session_id: str = Field(..., description="Unique user session identifier")

    frontend_origin: Optional[str] = None
    product: Optional[str] = None
    contracts: Optional[List[Dict[str, Any]]] = []
    metrics: Optional[List[str]] = []
    messages: Optional[List[Dict[str, Any]]] = None


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
router = APIRouter(prefix="/master_bot", tags=["Master Bot"])

REDIS_TTL_SECONDS = 86400  # 24 hours


@router.post(
    "/queries",
    response_model=OutputState,
    summary="Execute Master Bot LangGraph Pipeline",
)
async def master_bot_query(payload: InputState):
    logger.info(f"Master bot request received for session_id={payload.session_id}")

    try:
        data = payload.model_dump()

        # Configure frontend origin
        data["frontend_origin"] = (
            DEV_URI
            if ENVIRONMENT == "development"
            else PROD_URI
        )

        # ------------------------------------------------------
        # LOAD CHAT HISTORY FROM REDIS
        # ------------------------------------------------------
        raw_history = redis_client.get(payload.session_id)

        if raw_history:
            try:
                existing_history = json.loads(raw_history)
                if not isinstance(existing_history, list):
                    logger.error(f"Chat history corrupted for {payload.session_id}")
                    existing_history = []
            except json.JSONDecodeError:
                logger.error(f"Chat history JSON invalid for {payload.session_id}")
                existing_history = []
        else:
            existing_history = []
        copied_list = copy.deepcopy(existing_history)
        data["messages"] = copied_list

        # ------------------------------------------------------
        # EXECUTE GRAPH
        # ------------------------------------------------------
        typed_graph = parent_graph.with_types(
            input_type=InputState,
            output_type=OutputState,
        )

        raw_state = typed_graph.invoke(
            data,
            config={"configurable": {"thread_id": payload.session_id}},
        )

        # Normalize output
        if isinstance(raw_state, dict):
            output = finalize_to_output(raw_state)
        elif isinstance(raw_state, OutputState):
            output = raw_state
        else:
            logger.error(f"Invalid graph output type: {type(raw_state)}")
            raise TypeError("Graph returned an unexpected output type")

        # ------------------------------------------------------
        # UPDATE CHAT HISTORY IN REDIS
        # ------------------------------------------------------
        updated_history = list(existing_history)

        updated_history.append({
            "role": "user",
            "content": payload.question,
        })

        updated_history.append({
            "role": "bot",
            "content": output.generation,
        })

        # output_messages = raw_state["messages"]
        redis_client.setex(
            payload.session_id,
            REDIS_TTL_SECONDS,
            json.dumps(updated_history)
        )

        logger.info(f"Master bot completed successfully for session_id={payload.session_id}")
        return output

    except Exception as exc:
        logger.exception(f"Master bot execution failed for session={payload.session_id}: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Internal error during graph execution",
        )
