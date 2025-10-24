from pydantic import BaseModel
from typing import Optional, List, Dict, Any,Annotated,Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages

class ParentState(BaseModel):
    user_query: str
    page_url: str
    agent_output: Optional[str] = None
    chat_history: List[Dict[str, str]] = []
    frontend_origin: str = "https://app.spinnaker.com",
    messages: Annotated[Sequence[BaseMessage], add_messages]=[]
    is_correct_location: bool = True
    is_incorrect_location_msg: Optional[str] = None
    routing_response: Dict[str, Any] = {}
    # agent_output: str 
    final_response: str = ""
