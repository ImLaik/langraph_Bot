from __future__ import annotations

from typing import Any, Dict, List

from loguru import logger
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.output_parsers import StrOutputParser

from db.cosmo_db import CosmoDBConnection
from parent_graph.state import ParentState
from utils.utils import filter_contracts, create_llm, invoke_with_logging
from query_router.prompt import routing_prompt
from tools.contract_comparator.model import ContractComparator
from tools.contract_comparator.prompt import contract_comparator_prompt

# ---------------------------------------------------------------------------
# LLM INITIALIZATION (shared instance)
# ---------------------------------------------------------------------------
llm = create_llm()


# ---------------------------------------------------------------------------
# NODE: Prepare Contracts
# ---------------------------------------------------------------------------
def prepare_contracts(state: ParentState) -> ParentState:
    logger.info("Preparing contracts for comparison...")

    try:
        page_url: str | None = state.get("page_url")
        if not page_url:
            raise ValueError("Missing `page_url` in state")

        selected_metrics: list[str] | None = state.get("metrics")
        selected_contracts: list[Dict[str, Any]] | None = state.get("contracts")

        if not selected_contracts:
            raise ValueError("No contracts provided to prepare")

        # Determine container
        container_name = (
            "world_insurance_contract_comparator_db"
            if "property-and-casualty" in page_url
            else "alliant_contract_comparator_db"
        )
        logger.debug(f"Using CosmosDB container: {container_name}")

        client, database, container = CosmoDBConnection(container_name=container_name)

        contract_records: List[Dict[str, Any]] = []

        # Fetch each contract’s data
        for contract_data in selected_contracts:
            carrier_name = contract_data.get("contractName")
            plan_name = contract_data.get("planName")
            hash_key = contract_data.get("hash_key")

            if not (carrier_name and plan_name and hash_key):
                logger.warning(
                    f"Skipping contract due to missing attributes: {contract_data}"
                )
                continue

            query = """
                SELECT *
                FROM c
                WHERE c.plan_name = @plan_name
                AND c.hash_key = @hash_key
            """

            parameters = [
                {"name": "@plan_name", "value": plan_name},
                {"name": "@hash_key", "value": hash_key},
            ]

            results = list(
                container.query_items(
                    query=query,
                    parameters=parameters,
                    partition_key=carrier_name,
                )
            )

            if not results:
                logger.warning(
                    f"No CosmosDB records found for {carrier_name} - {plan_name}"
                )

            contract_records.extend(results)

        if not contract_records:
            raise RuntimeError("No matching contract records found in CosmosDB")

        # Filter the contract information
        filtered_data = filter_contracts(
            contract_records, selected_metrics, selected_contracts
        )

        state["contracts"] = filtered_data
        logger.info("Contract preparation completed.")
        return state

    except Exception as exc:
        logger.exception("prepare_contracts failed")
        state["error"] = f"Contract preparation failed: {exc}"
        return state


# ---------------------------------------------------------------------------
# NODE: Contract Comparator
# ---------------------------------------------------------------------------
def contract_comparator(state: ParentState) -> ParentState:
    logger.info("Running contract comparator...")

    try:
        question: str | None = state.get("question")
        metrics = state.get("metrics")
        context = state.get("contracts")

        if not question:
            raise ValueError("Missing question for comparator")

        if not context:
            raise ValueError("Missing contract data in state")

        # Structured LLM wrapper
        structured_llm = llm.with_structured_output(
            ContractComparator, 
            method="function_calling"
        )

        comparison_chain = contract_comparator_prompt | structured_llm

        response = invoke_with_logging(
            comparison_chain.invoke,
            {
                "question": question,
                "metrics": metrics,
                "context": context,
                "chat_history": [],
            },
            "contract_comparator",
        )

        response_dict = response.model_dump()

        final_response = response_dict.get("response")
        if not final_response:
            raise RuntimeError("LLM did not produce a valid comparator response")

        state["generation"] = final_response
        logger.info("Contract comparison completed successfully.")

        return state

    except Exception as exc:
        logger.exception("contract_comparator failed")
        state["error"] = f"Contract comparator failed: {exc}"
        return state


# ---------------------------------------------------------------------------
# GRAPH DEFINITION
# ---------------------------------------------------------------------------
contract_comparator_graph_builder = StateGraph(ParentState)

contract_comparator_graph_builder.add_node("prepare_contracts", prepare_contracts)
contract_comparator_graph_builder.add_node("contract_comparator", contract_comparator)

contract_comparator_graph_builder.add_edge(START, "prepare_contracts")
contract_comparator_graph_builder.add_edge("prepare_contracts", "contract_comparator")
contract_comparator_graph_builder.add_edge("contract_comparator", END)

# Enable optional checkpointing if desired
# memory = MemorySaver()
# contract_comparator_graph = contract_comparator_graph_builder.compile(checkpointer=memory)

contract_comparator_graph = contract_comparator_graph_builder.compile()

