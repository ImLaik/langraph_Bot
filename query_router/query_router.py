from utils.utils import create_llm
from langchain_core.output_parsers import StrOutputParser

from query_router.prompt import routing_prompt
from parent_graph.models import RouteQuery

# LLM Instantiation - One for all
llm = create_llm()

# Router
router_structured_llm = llm.with_structured_output(RouteQuery, method="function_calling")
question_router = routing_prompt | router_structured_llm
