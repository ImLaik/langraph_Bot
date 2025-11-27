from typing import Optional
from pydantic import BaseModel, Field

class StructuredResponse(BaseModel):
    """
    Represents the routing assistant decision output.
    """
    response: Optional[str] = Field(
        None,
        description="response"
    )

    