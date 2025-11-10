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

llm=AzureChatOpenAI(
azure_deployment =  os.getenv("CHAT_MODEL"),
azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT"),
openai_api_key = os.getenv("AZURE_OPENAI_API_KEY"),
openai_api_version =  os.getenv("OPENAI_API_VERSION"),
seed=102,
temperature=0
)