from typing import Optional
from pydantic import BaseModel, Field

class RouteQuery(BaseModel):
    """
    Represents the routing assistant decision output.
    """
    is_correct_location: bool = Field(
        ...,
        description="True if the provided page_url is correct for the user's query; False if redirection is needed."
    )
    is_incorrect_location_msg: Optional[str] = Field(
        None,
        description="Markdown-formatted friendly message guiding the user to the correct product page if location is incorrect, otherwise null."
    )
    route_to: Optional[str] = Field(
        ...,
        description="Tell where to route"
    )
    