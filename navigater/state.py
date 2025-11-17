from pydantic import BaseModel
from typing import Optional, List
from typing import Union, Dict, Any


# from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages

from typing_extensions import TypedDict


class State(TypedDict, total=False):
    question: str
    messages: str
    page_url: str
    frontend_origin: str
    generation: Union[str, Dict[str, Any]]
    route_to: Optional[str]
    selected_tool: Optional[str]
    db: Optional[object]
    contracts: Optional[List[str]]
    metrics: Optional[List[str]]
    product: Optional[str]
    data_dict: Optional[str]
    tool_prompt: Optional[str]
    relevant_tables: Optional[List[str]]
    fallback_state: Optional[str]
