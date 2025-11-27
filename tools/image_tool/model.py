from typing import Optional
from pydantic import BaseModel, Field

class ImageTool(BaseModel):
    """
    Represents the routing assistant decision output.
    """
    response: Optional[str] = Field(
        None,
        description="Markdown-formatted response."
    )
