import os
from typing import Dict, Any, Optional
import pandas as pd
from loguru import logger
from langgraph.graph import END, START, StateGraph
from utils.states import WorkingState

# Node constants
NODE_EXTRACT_TOOL = "extract_tool_name"

# CSV configuration
TOOL_MAPPING_CSV = "tool_mapping.csv"
REQUIRED_COLUMNS = {"product_catalog_module_url", "agent_tool"}

# Base URL your CSV expects
PRODUCT_BASE_URL = "https://www.spinnakerhub.com"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _load_mapping_csv(path: str) -> pd.DataFrame:
    """
    Load the tool mapping CSV with strict validation.
    Throws ValueError for any structural errors.
    """
    if not os.path.exists(path):
        msg = f"Tool mapping CSV not found: {path}"
        logger.critical(msg)
        raise ValueError(msg)

    try:
        df = pd.read_csv(path, dtype=str)  # Treat everything as string to avoid dtype surprises.
    except Exception as exc:
        msg = f"Failed to read tool mapping CSV: {exc}"
        logger.critical(msg)
        raise ValueError(msg)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        msg = f"Tool mapping CSV missing required columns: {missing}"
        logger.critical(msg)
        raise ValueError(msg)

    # Normalize columns to avoid trailing spaces or URL formatting issues
    df["product_catalog_module_url"] = df["product_catalog_module_url"].astype(str).str.strip()
    df["agent_tool"] = df["agent_tool"].astype(str).str.strip()

    return df


def _resolve_tool_for_page(df: pd.DataFrame, full_url: str) -> Optional[Dict[str, Any]]:
    """
    Given a loaded DataFrame and full URL, return the matching CSV row as a dict.
    Returns None when unmatched.
    """
    match = df[df["product_catalog_module_url"] == full_url]
    if match.empty:
        return None
    return match.iloc[0].to_dict()


# ---------------------------------------------------------------------------
# Node logic
# ---------------------------------------------------------------------------
def extract_tool_name(state: WorkingState) -> WorkingState:
    """
    Resolve the correct tool based on the page URL using a CSV mapping table.

    Mutates and returns the WorkingState with keys:
        - selected_tool: resolved tool name or None
        - tool_info: metadata dict from the CSV (when matched)
        - generation: any fallback message
        - next: target node
    """
    logger.info("tool_calling_agent_graph: extract_tool_name triggered.")

    # ----------------------------------------------------------------------
    # Validate required state
    # ----------------------------------------------------------------------
    page_url = state.get("page_url")
    if not page_url:
        logger.error("Missing 'page_url' in state; cannot resolve tool.")
        state["generation"] = "No page URL provided; cannot resolve tool."
        state["selected_tool"] = None
        state["next"] = "llm_fallback_graph"
        return state

    # Normalize incoming page_url to avoid trailing slash issues
    page_url = str(page_url).strip()

    # ----------------------------------------------------------------------
    # Load CSV
    # ----------------------------------------------------------------------
    try:
        mapping_df = _load_mapping_csv(TOOL_MAPPING_CSV)
    except ValueError as exc:
        logger.error(f"Tool mapping load failed: {exc}")
        state["generation"] = "Tool mapping unavailable. Reverting to default handling."
        state["selected_tool"] = None
        state["next"] = "llm_fallback_graph"
        return state

    # ----------------------------------------------------------------------
    # Construct fully qualified URL used in mapping table
    # ----------------------------------------------------------------------
    full_url = f"{PRODUCT_BASE_URL}{page_url}"
    logger.debug(f"Resolving tool for full URL: {full_url}")

    # ----------------------------------------------------------------------
    # Lookup tool in CSV
    # ----------------------------------------------------------------------
    row_dict = _resolve_tool_for_page(mapping_df, full_url)

    if row_dict is None:
        logger.warning(f"No tool match found for URL: {full_url}")
        state["generation"] = "No matching tool found. Switching to default handling."
        state["selected_tool"] = None
        state["next"] = "llm_fallback_graph"
        return state

    tool_name = row_dict.get("agent_tool")

    if not tool_name or not isinstance(tool_name, str) or not tool_name.strip():
        logger.warning(f"Invalid or empty tool name in CSV row: {row_dict}")
        state["generation"] = "Invalid tool mapping; cannot proceed."
        state["selected_tool"] = None
        state["next"] = "llm_fallback_graph"
        return state

    # ----------------------------------------------------------------------
    # Success
    # ----------------------------------------------------------------------
    logger.info(f"Resolved tool: {tool_name}")
    # logger.debug(f"Tool metadata: {row_dict}")

    state["tool_info"] = row_dict
    state["selected_tool"] = tool_name
    state["next"] = tool_name

    return state


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------
def build_tool_calling_agent_graph() -> StateGraph:
    graph = StateGraph(WorkingState)

    graph.add_node(NODE_EXTRACT_TOOL, extract_tool_name)

    graph.add_edge(START, NODE_EXTRACT_TOOL)
    graph.add_edge(NODE_EXTRACT_TOOL, END)

    compiled = graph.compile()
    logger.info("tool_calling_agent_graph compiled.")
    return compiled


# Build graph on import (matching your existing pattern)
tool_calling_agent_graph = build_tool_calling_agent_graph()
