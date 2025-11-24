import os
import pandas as pd
from loguru import logger
from typing import Dict, Any
from fastapi import HTTPException
from parent_graph.state import ParentState

def tool_calling_agent_graph(state: ParentState) -> Dict[str, Any]:
    """
    Resolve the correct tool/agent for the current page based on a CSV mapping table.

    Returns:
        dict with keys:
        - generation: tool name or fallback message
        - tool_info: optional metadata from CSV row
        - selected_tool: name of the resolved tool
        - next: node to route to
    """

    logger.info("Tool-calling agent graph triggered.")

    # -------------------------------------------------------------------------
    # Validate required state fields
    # -------------------------------------------------------------------------
    page_url = state["page_url"]

    if not page_url:
        logger.error("State is missing 'page_url'.")
        return {
            "generation": "No page URL provided; cannot resolve tool.",
            "next": "llm_fallback_graph"
        }

    # -------------------------------------------------------------------------
    # Validate CSV availability
    # -------------------------------------------------------------------------
    mapping_path = "tool_mapping.csv"
    if not os.path.exists(mapping_path):
        msg = f"CSV mapping file not found: {mapping_path}"
        logger.critical(msg)
        raise HTTPException(status_code=500, detail=msg)

    # -------------------------------------------------------------------------
    # Read mapping CSV safely
    # -------------------------------------------------------------------------
    try:
        csv_data = pd.read_csv(mapping_path)
    except Exception as e:
        logger.critical(f"Failed reading tool mapping CSV: {e}")
        raise HTTPException(status_code=500, detail="Invalid tool mapping CSV file.")

    required_columns = {"product_catalog_module_url", "agent_tool"}
    missing = required_columns - set(csv_data.columns)

    if missing:
        msg = f"Tool mapping CSV missing required columns: {missing}"
        logger.critical(msg)
        raise HTTPException(status_code=500, detail=msg)

    # -------------------------------------------------------------------------
    # Construct lookup URL
    # -------------------------------------------------------------------------
    full_url = f"https://www.spinnakerhub.com{page_url}"

    # -------------------------------------------------------------------------
    # Lookup matching tool
    # -------------------------------------------------------------------------
    matching_rows = csv_data[csv_data["product_catalog_module_url"] == full_url]

    if matching_rows.empty:
        logger.warning(f"No matching tool found for page_url='{page_url}', full_url='{full_url}'")
        return {
            "generation": "No matching tool found; falling back to default handling.",
            "selected_tool": None,
            "next": "llm_fallback_graph"
        }

    row = matching_rows.iloc[0]
    tool_name = row["agent_tool"]

    if not isinstance(tool_name, str) or not tool_name.strip():
        logger.warning(f"Tool name missing or invalid for CSV row: {row.to_dict()}")
        return {
            "generation": "Invalid tool mapping; cannot proceed.",
            "selected_tool": None,
            "next": "llm_fallback_graph"
        }

    row_dict = row.to_dict()

    logger.info(f"Matched tool: {tool_name}")
    logger.debug(f"Resolved tool metadata: {row_dict}")

    # -------------------------------------------------------------------------
    # Validate next-node routing target
    # -------------------------------------------------------------------------
    # NOTE: If your graph has only fixed nodes, ensure this tool_name is valid.
    # allowed_nodes = {"handle_redirect", "tool_calling_agent_graph", "llm_fallback_graph"}

    # if tool_name not in allowed_nodes:
    #     logger.warning(
    #         f"Resolved tool '{tool_name}', but no graph node exists with this name. "
    #         "Falling back to llm_fallback_graph."
    #     )
    #     return {
    #         "generation": tool_name,
    #         "tool_info": row_dict,
    #         "selected_tool": tool_name,
    #         "next": "llm_fallback_graph"
    #     }

    # -------------------------------------------------------------------------
    # Success → Route to appropriate tool node
    # -------------------------------------------------------------------------
    return {
        "generation": tool_name,
        "tool_info": row_dict,
        "selected_tool": tool_name,
        "next": tool_name
    }
