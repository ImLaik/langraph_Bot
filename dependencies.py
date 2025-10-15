from langserve import add_routes
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from navigater.graph import master_graph
from navigater.state import ParentState



# class QueryRequest(BaseModel):
#     user_query: str
#     product: str
#     page_url: str
#     session_id: str
#     chat_history: Optional[list] = [] 
#     contracts: Optional[list] = []
#     metrics: Optional[list] = []

def setup_app_state(app):
    """
    Initialize LangServe routes for both graphs
    """
    
    # Master Graph Route - validates routing
    add_routes(
        app,
        master_graph.with_types(
            input_type=ParentState,
            output_type=ParentState
        ),
        path="/adaptive_rag",
        playground_type="default",
        # config_schema={"configurable": {"thread_id": str}}, 
        include_callback_events=False,
        enabled_endpoints=["invoke"] 
    )
