import os
import re
import logging
import importlib
from typing import Optional, Any, Dict, Callable, List, Union, Tuple

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from utils.states import WorkingState, OutputState

logger = logging.getLogger(__name__)
load_dotenv()

# ---------------------------------------------------------------------------
# ENVIRONMENT CONFIG LOADING
# ---------------------------------------------------------------------------

def _require_env(var: str) -> str:
    value = os.getenv(var)
    if not value:
        raise EnvironmentError(f"Missing required environment variable: {var}")
    return value

AZURE_ENDPOINT = _require_env("AZURE_OPENAI_ENDPOINT")
AZURE_API_KEY = _require_env("AZURE_OPENAI_API_KEY")
AZURE_API_VERSION = _require_env("AZURE_OPENAI_API_VERSION")

DEFAULT_GPT_MODEL = _require_env("AZURE_OPENAI_GPT_4o_MODEL")
DEFAULT_EMBED_MODEL = _require_env("AZURE_OPENAI_EMBEDDING_MODEL")


# ---------------------------------------------------------------------------
# LLM CREATION
# ---------------------------------------------------------------------------
def create_llm(
    *,
    azure_deployment: Optional[str] = None,
    azure_endpoint: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    openai_api_version: Optional[str] = None,
    temperature: Optional[float] = None,
    temperature_required: Optional[bool] = None,
    **params: Any,
) -> AzureChatOpenAI:
    """
    Creates an AzureChatOpenAI instance with strict validation.
    Safely handles temperature logic and guarantees required config exists.
    """

    azure_deployment = azure_deployment or DEFAULT_GPT_MODEL
    azure_endpoint = azure_endpoint or AZURE_ENDPOINT
    openai_api_key = openai_api_key or AZURE_API_KEY
    openai_api_version = openai_api_version or AZURE_API_VERSION

    missing = [
        name
        for name, value in {
            "azure_deployment": azure_deployment,
            "azure_endpoint": azure_endpoint,
            "openai_api_key": openai_api_key,
            "openai_api_version": openai_api_version,
        }.items()
        if not value
    ]
    if missing:
        raise ValueError(f"Missing required configuration values: {', '.join(missing)}")

    if temperature_required and temperature is None:
        raise ValueError("Temperature is required but not provided.")

    # No temperature expected, warn and ignore if provided
    if temperature_required is False:
        if temperature is not None:
            logger.warning("Temperature provided but ignored (temperature_required=False)")
        temperature = None

    return AzureChatOpenAI(
        azure_deployment=azure_deployment,
        azure_endpoint=azure_endpoint,
        openai_api_key=openai_api_key,
        openai_api_version=openai_api_version,
        temperature=temperature,
        **params,
    )


# ---------------------------------------------------------------------------
# SERVICE INVOCATION WRAPPER
# ---------------------------------------------------------------------------
def invoke_with_logging(
    service_func: Callable[[Dict[str, Any]], Any],
    payload: Dict[str, Any],
    service_name: str,
) -> Any:
    """
    Wrap any call with structured logging and error propagation.
    """
    try:
        logger.debug(f"{service_name}: request payload={payload}")
        result = service_func(payload)
        logger.debug(f"{service_name}: response={result}")
        return result
    except Exception as exc:
        logger.error(f"{service_name} failed: {exc}")
        raise


# ---------------------------------------------------------------------------
# LOGGING DECORATOR
# ---------------------------------------------------------------------------
def log_function(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        logger.info(f"Entering: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Exiting: {func.__name__}")
            return result
        except Exception:
            logger.exception(f"Error in function: {func.__name__}")
            raise
    return wrapper


# ---------------------------------------------------------------------------
# VECTOR CONTEXT RETRIEVAL
# ---------------------------------------------------------------------------
def get_relevant_catalog_context(
    question: str,
    page_url: str,
    *,
    k: int = 3,
    collection_name: str = "routing_prompts",
    persist_directory: str = "./chroma_db",
    embeddings: Optional[AzureOpenAIEmbeddings] = None,
    vectorstore: Optional[Chroma] = None,
) -> str:
    """
    Perform semantic search with strict input validation and safety.
    """

    if not question or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    if not page_url or not page_url.strip():
        raise ValueError("Page URL must be a non-empty string.")

    if embeddings is None:
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=DEFAULT_EMBED_MODEL,
            openai_api_key=AZURE_API_KEY,
            azure_endpoint=AZURE_ENDPOINT,
            openai_api_version=AZURE_API_VERSION,
        )

    if vectorstore is None:
        vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=persist_directory,
            embedding_function=embeddings,
        )

    query = question.strip()
    logger.info(f"Vector search: query='{query}'")

    try:
        results: List[Document] = vectorstore.similarity_search(query, k=k)
    except Exception as exc:
        logger.error(f"Vectorstore similarity_search failed: {exc}")
        raise RuntimeError("Failed to query vectorstore.") from exc

    if not results:
        logger.warning("Vectorstore returned no relevant documents.")
        return ""

    return "\n\n".join(doc.page_content for doc in results)


# ---------------------------------------------------------------------------
# PARSERS
# ---------------------------------------------------------------------------
def parse_relevant_tables(value: Union[str, list, None]) -> Union[List[str], None]:
    if not value:
        return value

    if isinstance(value, str):
        cleaned = re.sub(r"[\[\]]", "", value)
        return [v.strip() for v in cleaned.split(",") if v.strip()]

    return value


def parse_array_str(value: Union[str, list, None]) -> Union[List[str], None]:
    if not value:
        return value

    if isinstance(value, str):
        cleaned = re.sub(r"[\[\]]", "", value)
        return [
            v.strip().strip('"').strip("'")
            for v in cleaned.split(",")
            if v.strip()
        ]

    return value


# ---------------------------------------------------------------------------
# DYNAMIC PROMPT LOADER
# ---------------------------------------------------------------------------
def load_product_prompt(prompt_name: str) -> str:
    """
    Loads prompts dynamically from product_prompts/<prompt_name>.py
    """

    module_path = f"product_prompts.{prompt_name}"

    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {module_path}")

    try:
        return getattr(module, prompt_name)
    except AttributeError:
        raise ValueError(f"Prompt variable '{prompt_name}' missing in module '{module_path}'")


# ---------------------------------------------------------------------------
# STATE TRANSFORMERS
# ---------------------------------------------------------------------------
def to_working_from_input(input_obj: Any) -> WorkingState:
    data = (
        input_obj.model_dump()
        if hasattr(input_obj, "model_dump")
        else dict(input_obj)
    )

    return WorkingState(
        question=data.get("question"),
        page_url=data.get("page_url"),
        frontend_origin=data.get("frontend_origin"),
        contracts=data.get("contracts"),
        metrics=data.get("metrics"),
        messages=[],  # Always initialize empty
    )


def finalize_to_output(state: WorkingState) -> OutputState:
    if state.get("error"):
        return OutputState(generation=f"Error: {state['error']}")

    generation = state.get("generation") or "No output generated."
    return OutputState(generation=generation)


# ---------------------------------------------------------------------------
# CONTRACT FILTERING
# ---------------------------------------------------------------------------
def filter_contracts(
    contract_list: List[Dict[str, Any]],
    metrics: List[str],
    contracts: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Filter contracts deterministically and attach 'isPrimary'.
    """

    if not contract_list:
        return []

    if not metrics:
        metrics = []

    keys = ["primary_carrier_name", "carrier_name", "plan_name"]
    filtered_keys = keys + metrics

    hash_map = {c["hash_key"]: c.get("isPrimary") for c in contracts}

    output = []
    for contract in contract_list:
        filtered = {}
        for key in filtered_keys:
            if key in contract:
                filtered[key] = contract[key]
        filtered["isPrimary"] = hash_map.get(contract.get("hash_key"))
        output.append(filtered)

    return output


# ---------------------------------------------------------------------------
# VECTOR STORE LOADER
# ---------------------------------------------------------------------------
def load_vector_retriever() -> Tuple[Chroma, Any]:
    parent_dir = os.path.normpath(__file__).rsplit(os.sep, maxsplit=2)[0]
    vector_db_dir = f"{parent_dir}/llm_fallback/VectorStore/spinnaker_chatbot_data"

    embeddings = AzureOpenAIEmbeddings(
        openai_api_key=AZURE_API_KEY,
        azure_endpoint=AZURE_ENDPOINT,
        azure_deployment=DEFAULT_EMBED_MODEL,
        openai_api_version=AZURE_API_VERSION,
    )

    vector_store = Chroma(
        collection_name="vector_store",
        persist_directory=vector_db_dir,
        embedding_function=embeddings,
    )

    return vector_store, vector_store.as_retriever()
