from typing import Optional, Literal
from pydantic import BaseModel, Field

class StructuredAgentResponse(BaseModel):
    """
    Represents the agent's decision and output.
    Depending on 'next', `response` can either be:
      - Markdown answer to user (finalize_output)
      - Rewritten question to pass to route_question tool
    """
    response: Optional[str] = Field(
        None,
        description=(
            "If 'next' is 'finalize_output': Markdown formatted answer to the user's question.\n"
            "If 'next' is 'route_question': rewritten question based on chat history."
        )
    )
    next: Optional[Literal["finalize_output", "route_question"]] = Field(
        None,
        description=(
            "'finalize_output' means direct answer; 'route_question' means send rewritten question to routing tool."
        )
    )