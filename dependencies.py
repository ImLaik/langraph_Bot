from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from loguru import logger
from langserve import add_routes
from parent_graph.state import ParentState
from parent_graph.graph import parent_graph


class Input(BaseModel):
    question: str = Field(..., description="User's question.")
    page_url: str = Field(..., description="Origin page URL.")
    frontend_origin: str = Field(..., description="Frontend origin identifier.")
    contracts: Optional[List[Dict[str, Any]]] = None
    metrics: Optional[List[str]] = None


def setup_app_state(app: FastAPI) -> None:
    """
    Register LangServe routes for the parent graph.
    """
    logger.info("Initializing LangServe routes for parent graph.")

    add_routes(
        app,
        parent_graph.with_types(
            input_type=Input,
            output_type=ParentState
        ),
        path="/adaptive_rag",
        playground_type="default",
        include_callback_events=False,
        enabled_endpoints=["invoke"]
    )

    logger.info("Routes registered successfully under /adaptive_rag.")
