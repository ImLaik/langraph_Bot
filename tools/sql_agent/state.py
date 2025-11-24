# sql_agent/state.py
from typing import Any, List, Dict, Optional
from typing_extensions import TypedDict

class SQLAgentState(TypedDict):
    question: str
    tool_info: Dict[str, Any]
    sql_query: Optional[str]
    assumptions: Optional[str]
    db: Any  # Could type more strictly if needed
    df_json: Optional[List[Dict[str, Any]]]
    summary: Optional[str]
    error: Optional[str]
    