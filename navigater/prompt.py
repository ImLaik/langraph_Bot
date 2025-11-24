
from langchain_core.prompts import ChatPromptTemplate
from navigater.state import State
from utils.utils import create_llm
import logging
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma

load_dotenv()

llm = create_llm()

def get_relevant_catalog_context(question, page_url):
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION")

    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=azure_deployment,
        openai_api_key=openai_api_key,
        azure_endpoint=azure_endpoint,
        openai_api_version=openai_api_version
    )

    vectorstore = Chroma(
        collection_name="routing_prompts",
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    
    query = f"{question} {page_url}"
    results = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in results])
    return context

    

# def route_user_query(State)->State:
#     print("routing user query")
#     prompt=ChatPromptTemplate.from_template("""You are a **smart routing assistant** for Spinnaker Analytics' LLM Agent Application.  
# Your job is to determine if the user's provided `page_url` correctly matches one of the Spinnaker product catalog URLs and return a JSON object following the schema below.

# ---

# ### Output Schema
# {{
#     "is_correct_location": true or false,
#     "is_incorrect_location_msg": "string or null",
#     "route_to": "agent" or "llm_fallback" or "redirect"
# }}

# ---
                                                        
# ## Rules to Follow
# - If page_url matches a product catalog URL Or matches the Sub URL (If available) →
#     "is_correct_location": true
#     "is_incorrect_location_msg": null
#     "route_to": "agent"

# - If it does NOT match →
#     "is_correct_location": false
#     "is_incorrect_location_msg": "Format: To [briefly explain what they can do], please visit [Product Name] at {{frontend_origin}}/<product url>"
#     "route_to": "redirect"

# - General Queries and Greetings  →
#     "is_correct_location": true
#     "is_incorrect_location_msg": null
#     "route_to": "llm_fallback"
 
# --- 
   
# ### PRODUCT CATALOG:
# {catalog_context}
# ---

# ### Routing Logic

# 1. **First, check for greetings or general questions:**
#    - If user query is a greeting (hello, hi, how are you) or general question → Return `is_correct_location: true`, `is_incorrect_location_msg: null`, and `route_to: "llm_fallback"`

# 2. **Check if URL matches exactly:**
#    - Compare the provided page_url with the URLs in the catalog
#    - If the URL matches (also check if it's in Sub URL) → Return `is_correct_location: true`, `is_incorrect_location_msg: null`, and `route_to: "agent"`

# 3. **Special Commission Intelligence Rule:**
#    - **CRITICAL:** If the page_url contains `/commission-intelligence` (anywhere in the path):
#      - Read and understand the user query
#      - Check if query keywords match Commission Intelligence, Contract Comparator, or Contract Summary keywords
#      - If YES → Return `is_correct_location: true`, `is_incorrect_location_msg: null`, and `route_to: "agent"`
#      - If NO (query is about a different product like MOG) → Go to step 4

# 4. **Infer product from user query:**
#    - If no match yet, analyze the user query keywords against the product catalog
#    - Match query to the most appropriate product based on keywords and description
   
#    **IF the query clearly matches a product:**
#    - Compare inferred product URL with current page_url
#    - If they DON'T match:
#      - Generate a contextual, friendly redirection message:
#        - Acknowledge what the user is asking about
#        - Briefly explain why they should visit the specific product page (1 sentence max)
#        - Provide the redirect link using ONLY the exact URL from the product catalog
#      - Format: "To [briefly explain what they can do], please visit [Product Name] at {{frontend_origin}}/<exact-product-url-from-catalog>"
#      - Return `is_correct_location: false`, the message, and `route_to: "redirect"`
   
#    **IF the query does NOT match any product in the catalog:**
#    - Respond politely without providing any URL
#    - Return `is_correct_location: true`, `is_incorrect_location_msg: null`, and `route_to: "llm_fallback"`
   
#    **IF uncertain or confused:**
#    - Return `is_correct_location: true`, `is_incorrect_location_msg: null`, and `route_to: "llm_fallback"`

# 5. **CRITICAL RULES:**
#    - Only provide URLs that exist in the product catalog
#    - If unsure which product matches, do NOT guess a URL
#    - When in doubt, return `is_correct_location: true` and `route_to: "llm_fallback"`
#    - Always return only valid JSON following the schema above
#    - `is_incorrect_location_msg` should be proper Markdown text

# ---

# ## Please Find Below User Provided Input
# User Question: {question}
# Page URL: {page_url}
# Frontend Origin: {frontend_origin}
# Product Catalog:{catalog_context}

# Previous Conversation: 
# {messages}

# Return ONLY valid JSON with no additional text.
# """
#     )
    
#     question=State["question"]
#     messages=State["messages"]
#     page_url = State["page_url"]
#     frontend_origin=State["frontend_origin"]
#     catalog_context = get_relevant_catalog_context(question, page_url)
    
#     json_parser = JsonOutputParser()
#     question_router_chain = prompt | llm | json_parser
    
    
#     try:
#         response = question_router_chain.invoke({
#             "question": question,
#             "page_url": page_url,
#             "messages": messages,
#             "frontend_origin": frontend_origin,
#             "catalog_context":catalog_context
#         })
#         print(f"Response: {response}")
#         route_to = response.get("route_to", "llm_fallback")
#         State["route_to"] = route_to
        
#         generation = response.get("is_incorrect_location_msg", "")
#         State["generation"] = generation
        
#     except Exception as e:
#         logging.error(f"Error in route_user_query: {e}")
#         State["route_to"] = "llm_fallback"
#         State["generation"] = ""
    
#     return State



