from typing import Optional, Union, Dict, Any, List
from langgraph.graph import MessagesState


class ParentState(MessagesState):
    """
    State container for the parent routing graph.
    """
    question: str
    page_url: str
    frontend_origin: str
    tool_info: Optional[Dict[str, Any]] = None
    selected_tool: Optional[str] = None

    contracts: Optional[List[Dict[str, Any]]] = None
    metrics: Optional[List[str]] = None
    # Graph output fields
    generation: Optional[Union[str, Dict[str, Any]]] = None
    next: Optional[str] = None
    
