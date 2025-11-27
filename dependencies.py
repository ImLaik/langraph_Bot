from fastapi import FastAPI
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Dict, Any
from loguru import logger
from langserve import add_routes
from parent_graph.graph import parent_graph
from utils.states import OutputState


class InputState(BaseModel):
    question: str = Field(..., description="User's question.")
    page_url: str = Field(..., description="Origin page URL.")
    frontend_origin: str = Field(..., description="Frontend origin identifier.")

    # Optional additional inputs
    contracts: Optional[List[Dict[str, Any]]] = None
    metrics: Optional[List[str]] = None


def setup_app_state(app: FastAPI) -> None:
    """
    Configure LangServe routes and register parent graph endpoint.

    Raises:
        RuntimeError: If route registration fails.
    """

    logger.info("Initializing LangServe routes for parent graph.")

    # ----------------------------------------------------------------------
    # Validate graph type bindings early — fail fast
    # ----------------------------------------------------------------------
    try:
        _ = InputState.model_json_schema()
        _ = OutputState.model_json_schema()
    except ValidationError as exc:
        logger.critical(f"Input/Output model validation failed: {exc}")
        raise RuntimeError("Invalid input/output schema configuration.") from exc

    # ----------------------------------------------------------------------
    # Register LangServe routes
    # ----------------------------------------------------------------------
    try:
        add_routes(
            app,
            parent_graph.with_types(
                input_type=InputState,
                output_type=OutputState,
            ),
            path="/adaptive_rag",
            playground_type="default",
            include_callback_events=False,
            enabled_endpoints=["invoke"],   # restrict for security
        )
    except Exception as exc:
        logger.critical(f"Failed to register LangServe routes: {exc}")
        raise RuntimeError("Route registration failed.") from exc

    logger.info("LangServe routes registered successfully under /adaptive_rag.")
