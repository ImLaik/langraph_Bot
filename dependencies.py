from langserve import add_routes
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from navigater.graph import app_route
from navigater.state import State


def setup_app_state(app):
    """
    Initialize LangServe routes for both graphs
    """
    
    # Master Graph Route - validates routing
    add_routes(
        app,
        app_route.with_types(
            input_type=State,
            output_type=State
        ),
        path="/adaptive_rag",
        playground_type="default",
        # config_schema={"configurable": {"thread_id": str}}, 
        include_callback_events=False,
        enabled_endpoints=["invoke"] 
    )
