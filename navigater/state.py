from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ParentState(BaseModel):
    user_query: str
    page_url: str
    chat_history: List[Dict[str, str]] = []
    frontend_origin: str = "https://app.spinnaker.com"
    is_correct_location: bool = True
    is_incorrect_location_msg: Optional[str] = None
    routing_response: Dict[str, Any] = {}
    final_response: str = ""
