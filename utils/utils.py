import os
import re
import logging

from typing import Optional, Any
from typing import Any, Dict, Callable, List
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_core.documents import Document
from parent_graph.state import ParentState
from tools.sql_agent.state import SQLAgentState
import importlib

logger = logging.getLogger(__name__)

load_dotenv()

def create_llm(
    azure_deployment: Optional[str] = None,
    azure_endpoint: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    openai_api_version: Optional[str] = None,
    temperature: Optional[float] = None,
    temperature_required: Optional[bool] = None,
    **extra_params: Any,
) -> AzureChatOpenAI:
    """Creates an AzureChatOpenAI instance with environment-based fallbacks."""
    
    azure_deployment = azure_deployment or os.getenv("AZURE_OPENAI_GPT_4o_MODEL")
    azure_endpoint = azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    openai_api_key = openai_api_key or os.getenv("AZURE_OPENAI_API_KEY")
    openai_api_version = openai_api_version or os.getenv("AZURE_OPENAI_API_VERSION")
    
    missing_configs = {
        "AZURE_OPENAI_GPT_4o_MODEL": azure_deployment,
        "AZURE_OPENAI_ENDPOINT": azure_endpoint,
        "AZURE_OPENAI_API_KEY": openai_api_key,
        "AZURE_OPENAI_API_VERSION": openai_api_version,
    }
    
    missing = [key for key, value in missing_configs.items() if not value]
    if missing:
        raise ValueError(f"Missing required configurations: {', '.join(missing)}")
    
    if temperature_required and temperature is None:
        raise ValueError("Temperature is required but not provided.")
    if temperature_required is False and temperature is not None:
        logger.warning("Temperature provided but ignored.")
    
    return AzureChatOpenAI(
        azure_deployment=azure_deployment,
        azure_endpoint=azure_endpoint,
        openai_api_key=openai_api_key,
        openai_api_version=openai_api_version,
        temperature=temperature if temperature_required is not False else None,
        **extra_params
    )

def invoke_with_logging(
    service_func: Callable[[Dict[str, Any]], Any],
    payload: Dict[str, Any],
    service_name: str
) -> Any:
    """
    Helper function to invoke an external service with logging and error handling.
    """
    try:
        logger.debug(f"Invoking {service_name} with payload: {payload}")
        result = service_func(payload)
        logger.debug(f"{service_name} result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error invoking {service_name}: {e}")
        raise

def log_function(func: Callable) -> Callable:
    """
    Decorator to log function entry and exit with function name.
    """
    def wrapper(*args, **kwargs):
        logger.info(f"Entering function: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Exiting function: {func.__name__}")
        return result
    return wrapper

def get_relevant_catalog_context(
    question: str,
    page_url: str,
    *,
    k: int = 3,
    collection_name: str = "routing_prompts",
    persist_directory: str = "./chroma_db",
    embeddings: Optional[AzureOpenAIEmbeddings] = None,
    vectorstore: Optional[Chroma] = None
) -> str:
    """
    Retrieve relevant context from Chroma based on the question and page URL.

    Parameters
    ----------
    question : str
        User question or query.
    page_url : str
        Current page URL to add contextual relevance.
    k : int, optional
        Number of top results to retrieve. Default is 3.
    collection_name : str, optional
        Chroma collection name.
    persist_directory : str, optional
        Directory where Chroma DB is persisted.
    embeddings : AzureOpenAIEmbeddings, optional
        Pre-initialized embedding model.
    vectorstore : Chroma, optional
        Pre-initialized vector store.

    Returns
    -------
    str
        Concatenated relevant context.
    """

    # ------------------------------------------------------------
    # Validate inputs
    # ------------------------------------------------------------
    if not question or not question.strip():
        raise ValueError("Parameter 'question' must be a non-empty string.")

    if not page_url or not page_url.strip():
        raise ValueError("Parameter 'page_url' must be a non-empty string.")

    # ------------------------------------------------------------
    # Initialize embeddings if not provided
    # ------------------------------------------------------------
    if embeddings is None:
        azure_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")
        openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")

        missing_vars = [
            var for var, val in {
                "AZURE_OPENAI_EMBEDDING_MODEL": azure_deployment,
                "AZURE_OPENAI_API_KEY": openai_api_key,
                "AZURE_OPENAI_ENDPOINT": azure_endpoint,
                "AZURE_OPENAI_API_VERSION": openai_api_version,
            }.items() 
            if not val
        ]

        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        logger.debug("Initializing Azure OpenAI Embeddings...")
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=azure_deployment,
            openai_api_key=openai_api_key,
            azure_endpoint=azure_endpoint,
            openai_api_version=openai_api_version
        )

    # ------------------------------------------------------------
    # Initialize vectorstore if not provided
    # ------------------------------------------------------------
    if vectorstore is None:
        logger.debug("Loading Chroma vectorstore...")
        vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=persist_directory,
            embedding_function=embeddings
        )

    # ------------------------------------------------------------
    # Query vectorstore
    # ------------------------------------------------------------
    query_string = f"{question.strip()} {page_url.strip()}"

    logger.info(f"Performing similarity search for query: {query_string}")

    try:
        results: List[Document] = vectorstore.similarity_search(query_string, k=k)
    except Exception as e:
        logger.error(f"Vectorstore query failed: {e}")
        raise RuntimeError("Failed to query vectorstore.") from e

    if not results:
        logger.warning("No relevant documents found in the vectorstore.")
        return ""

    # ------------------------------------------------------------
    # Construct context
    # ------------------------------------------------------------
    context = "\n\n".join(doc.page_content for doc in results)
    logger.debug(f"Retrieved {len(results)} documents.")

    return context

def parse_relevant_tables(value):
    """Convert '[a, b, c]' → ['a', 'b', 'c']"""
    if isinstance(value, str):
        cleaned = re.sub(r"[\[\]]", "", value)
        tables = [t.strip() for t in cleaned.split(",") if t.strip()]
        return tables
    return value

def load_product_prompt(prompt_name: str) -> str:
    """
    Dynamically load a product prompt constant from a file in product_prompts folder.

    prompt_name: The constant name, which should also match the file name.
                 Example: MOG_IL_PROMPT → product_prompts/MOG_IL_PROMPT.py
    """
    PROMPT_FOLDER = "product_prompts"
    try:
        # Build module path - e.g. product_prompts.MOG_IL_PROMPT
        module_path = f"{PROMPT_FOLDER}.{prompt_name}"
        
        # Import the module dynamically
        module = importlib.import_module(module_path)
        
        # Get the constant inside the module that matches the name
        return getattr(module, prompt_name)
    
    except ModuleNotFoundError:
        raise FileNotFoundError(f"Prompt file for '{prompt_name}' not found in {PROMPT_FOLDER}")
    except AttributeError:
        raise ValueError(f"Prompt variable '{prompt_name}' not found inside {module_path}")
    
def parent_to_sql_agent(state: ParentState) -> SQLAgentState:
    return {
        "question": state["question"],
        "tool_info": state["tool_info"],
        "sql_query": None,
        "assumptions": None,
        "db": None,
        "df_json": None,
        "summary": None,
        "error": None,
    }

def sql_agent_to_parent(sql_state: SQLAgentState) -> ParentState:
    """
    Merges SQL outputs back into parent state.
    Puts final SQL summary into 'generation' so that parent graph output is consistent
    regardless of downstream node.
    """
    parent_state: ParentState = {
        **sql_state,                # brings sql_query, assumptions, df_json, summary, etc.
        "messages": [],             # preserve/initialize messages here
        "next": None,
    }

    # Populate generation from summary or error
    if sql_state.get("error"):
        parent_state["generation"] = f"SQL Agent Error: {sql_state['error']}"
    else:
        parent_state["generation"] = sql_state.get("summary", "No summary generated.")

    return parent_state

def filter_contracts(contract_list, metrics, contracts):
    print(f"\nContract list: {contract_list}")
    print(f"\nMetrics: {metrics}")
    print(f"\nContracts: {contracts}")
    keys = [
        "primary_carrier_name",
        "carrier_name",
        "plan_name",
    ]
    filtered_keys = keys + metrics

    # Build a mapping from hash_key to isPrimary
    contracts_map = {c['hash_key']: c['isPrimary'] for c in contracts}

    filtered_contracts = []
    for contract in contract_list:
        c = {}
        for key in filtered_keys:
            c[key] = contract[key]
        c['isPrimary'] = contracts_map.get(contract['hash_key'])
        filtered_contracts.append(c)

    return filtered_contracts
