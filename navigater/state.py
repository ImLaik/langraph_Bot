from pydantic import BaseModel
from typing import Optional, List
# from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages

from typing_extensions import TypedDict
class State(TypedDict, total=False):
    question: str
    messages: str
    page_url: str
    frontend_origin: str
    generation: str
    route_to: Optional[str]
    selected_tool: Optional[str]
    db: Optional[object]
    contracts: Optional[List[str]]
    metrics: Optional[List[str]]
    product: Optional[str]

