import json
import re
from typing import Dict, Any

import pandas as pd
from loguru import logger
from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import END, START, StateGraph

from db.sql_db import initialize_db_cached
from tools.sql_agent.prompt import REACT_SQL_PROMPT, EXPLAIN_PROMPT
from utils.utils import (
    parse_relevant_tables,
    create_llm,
    load_product_prompt,
)
from utils.states import WorkingState


# ---------------------------------------------------------------------------
# STEP 1 – Build SQL Query using LLM Agent
# ---------------------------------------------------------------------------
def prepare_sql_query(state: WorkingState) -> WorkingState:
    logger.info("STEP 1: Preparing SQL query...")

    question: str = state.get("question", "")
    tool_info: Dict[str, Any] = state.get("tool_info", {})

    try:
        # Extract metadata
        relevant_tables = parse_relevant_tables(tool_info.get("relevant_tables", ""))
        product_prompt_name = tool_info.get("product_prompt")

        # Prepare DB (cached)
        allowed_tuple = tuple(sorted(relevant_tables)) if relevant_tables else None
        db = initialize_db_cached(allowed_tuple)

        llm = create_llm()
        product_prompt_text = load_product_prompt(product_prompt_name) or ""

        # Build the system prompt
        system_prompt = REACT_SQL_PROMPT.format(
            input=question,
            agent_scratchpad="",
            chat_history="",
            product_prompt=product_prompt_text,
            tools="",
            tool_names="",
        )

        # Create SQL agent
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        tools = toolkit.get_tools()

        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=system_prompt,
        )

        agent_response = agent.invoke(
            {
                "input": question,
                "product_prompt": product_prompt_text,
            }
        )

        # Get last AIMessage
        final_message = next(
            (
                msg
                for msg in reversed(agent_response.get("messages", []))
                if isinstance(msg, AIMessage)
                and msg.content
                and msg.content.strip()
            ),
            None,
        )

        if not final_message:
            raise ValueError("No AIMessage content returned from SQL agent.")

        content = final_message.content.strip()

        # Strip "Final Answer:"
        if content.lower().startswith("final answer"):
            content = content.split(":", 1)[1].strip()

        # Extract JSON block
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object detected in LLM output.")

        parsed = json.loads(json_match.group(0))
        sql_query = parsed.get("sql_query", "")
        assumptions = parsed.get("assumptions", "")

        if not sql_query:
            raise ValueError("SQL query missing in LLM output JSON.")

        # Store results
        state["sql_query"] = sql_query
        state["assumptions"] = assumptions
        state["allowed_tables"] = allowed_tuple  # Store key for DB reuse

        return state

    except Exception as e:
        logger.exception("prepare_sql_query failed")
        state["error"] = f"SQL query preparation failed: {e}"
        return state


# ---------------------------------------------------------------------------
# STEP 2 – Execute SQL Query
# ---------------------------------------------------------------------------
def execute_sql(state: WorkingState) -> WorkingState:
    logger.info("STEP 2: Executing SQL query...")

    if state.get("error"):
        logger.warning("Skipping execute_sql due to earlier error.")
        return state

    sql_query = state.get("sql_query", "")
    allowed_tables = state.get("allowed_tables")

    try:
        if not sql_query:
            raise ValueError("State missing sql_query.")

        # Fetch cached DB again (safe)
        db = initialize_db_cached(allowed_tables)

        with db._engine.connect() as conn:
            df = pd.read_sql(sql_query, conn)

        state["df_json"] = df.to_dict(orient="records")
        logger.debug(f"SQL returned {len(state['df_json'])} rows.")

        return state

    except Exception as e:
        logger.exception("execute_sql failed")
        state["error"] = f"SQL execution failed: {e}"
        return state


# ---------------------------------------------------------------------------
# STEP 3 – Natural Language Summary of Results
# ---------------------------------------------------------------------------
def summarize_results(state: WorkingState) -> WorkingState:
    logger.info("STEP 3: Summarizing SQL results...")

    if state.get("error"):
        logger.warning("Skipping summarize_results due to earlier error.")
        return state

    try:
        question = state.get("question", "")
        sql_query = state.get("sql_query", "")
        assumptions = state.get("assumptions", "")
        df_json = state.get("df_json", [])

        llm = create_llm()

        df = pd.DataFrame(df_json)
        sql_result_preview = (
            df.head(10).to_string(index=False) if not df.empty else "No rows returned"
        )

        summary = (
            RunnablePassthrough()
            | EXPLAIN_PROMPT
            | llm
            | StrOutputParser()
        ).invoke(
            {
                "question": question,
                "query": sql_query,
                "sql_response": sql_result_preview,
                "assumptions": assumptions,
            }
        )

        state["generation"] = summary
        logger.debug("Summary generated successfully.")
        return state

    except Exception as e:
        logger.exception("summarize_results failed")
        state["error"] = f"Summary generation failed: {e}"
        return state


# ---------------------------------------------------------------------------
# BUILD GRAPH
# ---------------------------------------------------------------------------
sql_agent_graph_builder = StateGraph(WorkingState)

sql_agent_graph_builder.add_node("prepare_sql_query", prepare_sql_query)
sql_agent_graph_builder.add_node("execute_sql", execute_sql)
sql_agent_graph_builder.add_node("summarize_results", summarize_results)

sql_agent_graph_builder.add_edge(START, "prepare_sql_query")
sql_agent_graph_builder.add_edge("prepare_sql_query", "execute_sql")
sql_agent_graph_builder.add_edge("execute_sql", "summarize_results")
sql_agent_graph_builder.add_edge("summarize_results", END)

sql_agent_graph = sql_agent_graph_builder.compile()
