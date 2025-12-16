from typing import Optional
from pydantic import BaseModel, Field

class SQLToolResult(BaseModel):
    """
    Output schema for the SQL generation tool.

    This model represents the final decision of the SQL agent:
    either a valid, executable SQL query or a clear justification
    for why a query cannot be generated.
    """

    sql_query: Optional[str] = Field(
        default=None,
        description=(
            "A single, read-only, executable SQL query. "
            "Must be null if a valid SQL query cannot be generated."
        ),
    )

    assumptions: Optional[str] = Field(
        default=None,
        description=(
            "Explicit assumptions made while constructing the SQL query. "
            "If sql_query is null, this field must explain precisely why "
            "query generation is not possible (e.g., missing tables, "
            "ambiguous metrics, insufficient filters)."
        ),
    )
