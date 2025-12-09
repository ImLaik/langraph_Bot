from typing import Optional, Union, Dict, Any, List, Tuple
from langchain_core.documents import Document
from langgraph.graph import MessagesState
from pydantic import BaseModel

class WorkingState(MessagesState):
    """
    Internal state used by the graph and all nodes.
    This MUST NOT be returned directly to the client.
    """
    # Required input fields (copied from Input)
    question: str
    page_url: str
    frontend_origin: str

    # Optional inputs
    contracts: Optional[List[Dict[str, Any]]] = None
    metrics: Optional[List[str]] = None

    # Runtime / transient fields (tool-specific)
    tool_info: Optional[Dict[str, Any]] = None
    selected_tool: Optional[str] = None
    allowed_tables: Optional[Tuple[str, ...]] = None

    sql_query: Optional[str] = None
    assumptions: Optional[str] = None

    df_json: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    error: Optional[str] = None
    context: Optional[List[Document]] = None
    messages: Optional[List[Dict[str, Any]]] = None
    # The final human-facing generation content (populated by finalizer)
    generation: Optional[Union[str, Dict[str, Any]]] = None

    # routing helper (internal)
    next: Optional[str] = None


class OutputState(BaseModel):
    """
    Clean output exposed to external clients.
    Contains only 'generation' (and optionally metadata you permit).
    """
    generation: Union[str, Dict[str, Any]]
