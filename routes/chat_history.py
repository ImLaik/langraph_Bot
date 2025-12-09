from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel
from db.redis import redis_client
from typing import List, Dict, Any
import json

router = APIRouter(prefix="/master_bot", tags=["Chat History"])


# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------
class ChatHistoryResponse(BaseModel):
    success: bool
    chat_history: List[Dict[str, Any]]


class DeleteHistoryResponse(BaseModel):
    success: bool
    message: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get(
    "/chat_history/{session_id}",
    response_model=ChatHistoryResponse,
    summary="Retrieve chat history for a session",
)
async def get_chat_history(session_id: str):
    logger.info(f"Fetching chat history for session_id={session_id}")

    try:
        raw = redis_client.get(session_id)

        if not raw:
            return ChatHistoryResponse(success=True, chat_history=[])

        try:
            history = json.loads(raw)
        except json.JSONDecodeError:
            logger.error(f"Corrupt Redis JSON for session_id={session_id}")
            history = []

        return ChatHistoryResponse(success=True, chat_history=history)

    except Exception as exc:
        logger.exception(f"Failed to fetch chat history for {session_id}: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve chat history"
        )


@router.post(
    "/chat_history/{session_id}",
    response_model=DeleteHistoryResponse,
    summary="Delete chat history for a session",
)
async def delete_chat_history(session_id: str):
    logger.info(f"Deleting chat history for session_id={session_id}")

    try:
        redis_client.delete(session_id)
        return DeleteHistoryResponse(
            success=True,
            message=f"Chat history for session {session_id} deleted."
        )
    except Exception as exc:
        logger.exception(f"Failed to delete chat history for {session_id}: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete chat history"
        )
