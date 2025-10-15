import os
import os
import re
import logging

from typing import Optional, Any
from typing import Any, Dict, Callable, List
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

def initialize_llm(
    azure_deployment: Optional[str] = None,
    azure_endpoint: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    openai_api_version: Optional[str] = None,
    temperature: Optional[float] = None,
    temperature_required: Optional[bool] = None,
    **extra_params: Any,
) -> AzureChatOpenAI:
    """Creates an AzureChatOpenAI instance with environment-based fallbacks."""
    
    azure_deployment = azure_deployment or os.getenv("CHAT_MODEL")
    azure_endpoint = azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    openai_api_key = openai_api_key or os.getenv("AZURE_OPENAI_API_KEY")
    openai_api_version = openai_api_version or os.getenv("OPENAI_API_VERSION")
    
    missing_configs = {
        "CHAT_MODEL": azure_deployment,
        "AZURE_OPENAI_ENDPOINT": azure_endpoint,
        "AZURE_OPENAI_API_KEY": openai_api_key,
        "OPENAI_API_VERSION": openai_api_version,
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
