
from langchain_core.output_parsers import JsonOutputParser
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from navigater.state import State
from utils import llm
import os
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain.agents import create_agent
# from langgraph.prebuilt import create_react_agent, AgentExecutor
import json
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
import re
import pandas as pd
from product_prompts.MOG_IL_PROMPT import MOG_IL_PROMPT
import logging
from datetime import datetime


load_dotenv()

user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
host = os.getenv("PG_HOST", "localhost")
port = os.getenv("PG_PORT", "5432")
dbname = os.getenv("PG_DATABASE")




REACT_SQL_PROMPT = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "chat_history", "product_prompt", "tools", "tool_names"],
    template="""You are an expert SQL generator with read-only access to a PostgreSQL database. 
    Using the provided data dictionary (tables/columns), translate the user's request into a correct, executable SQL query. 
    Use exact names and types from the dictionary. Return only the SQL (no explanations).

    You have access to the following tools:
    {tools}

    TOOLS AVAILABLE:
    (Must be one of: {tool_names})
    You MUST strictly follow this ReAct format every step:
    Thought: <what you are thinking next>
    Action: <one of the tool names above>
    Action Input: <exact string input to the tool and Always provide the SQL query as a plain string without backticks or code formatting, and pass only the executable query in Action Input.>
    Observation: <result of the action>
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: <JSON object as specified below>
    ---

    ## PLEASE FOLLOW THE GIVEN INSTRUCTIONS IN EACH STEPS: 
    INSTRUCTIONS: {product_prompt}

    - **OUTPUT FORMAT:**     
        - If not, Produces a JSON object *only*, with this structure:
        {{{{
            "sql_query": <your SQL query here>,
            "assumptions": <any assumptions you made to generate this query, or empty string if none>
        }}}}
  

    - **Examples:**
        - For string columns filtered by substrings or ambiguous values, ALWAYS use fuzzy.
        - For non-numeric columns, numeric queries must use substring fuzzy (`ILIKE`). NEVER cast unless subset of data confirms numeric format.
    - **IMPORTANT:**
        - Never deviate from the JSON structure for your final response.
        - Document any mappings and data handling or type reasoning in "assumptions" for clarity and traceability.
        - If no SQL is possible, respond with -- NO_SQL_POSSIBLE; in the "sql_query" only.
        - When making assumptions, **do not reference specific table names**. State assumptions only in terms of business dimensions (e.g., year, state, MSA, product) and the logic applied (filters, joins, aggregations, calculations). 
   
   

    Previous conversation:
    {chat_history}

    User question:
    {input}

    Begin step-by-step reasoning now.
    {agent_scratchpad}
    """
)
 

"""
Spinnaker Analytics Data Dictionary
Auto-generated from Excel file
"""

 

CONTRACT_SUMMARY_DATA_DICTIONARY = """
# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** public
 
---
 
## Tables Overview
 
This database contains 1 tables for analytics on contract summary.
 
## Table: contract_summary
 
Historical data for contracts of various Carriers.
 
**Please Follow the Below Table Structure**
<column-name> (datatype) : <description> : <importance-level> : <importance-identification>  

**Columns:**
  - contract_id (VARCHAR) : Contract ID : High : Unique Count of Contract ID is no.of Unique Contracts i.e. 1 Unique Contract ID signifies 1 Contract
  - carrier (VARCHAR) : Carrier Name : Low : Should be returned in order to tie-up the details
  - ingestion_date (Date) : Contract Ingestion Date: Low : ""
  - year (INT) : Year : Low : ""
  - program_name (VARCHAR) : Program Name : Low : Should be returned in order to tie-up the details
  - bonus_type (VARCHAR): Bonus Type : Medium : Should be returned in order to tie-up the details
  - threshold_applied_to (VARCHAR): Threshold applied to : Medium : Should be returned in order to tie-up the details
  - threshold   (VARCHAR): Threshold Value / Range : High : Best Combination of EWP and Loss Ratio where EWP is not ridiculiosly high and Loss Ratio is not ridiculiosly low
  - bonus   (NUMERIC) : Bonus percentage : Very high : Higher the better
  - effective_date (Date) : Contract Effective Date : Low : Should be returned in order to tie-up the details
  - expiration_date (Date) : Contract Expiration Date : Low : Should be returned in order to tie-up the details
  - source_document (VARCHAR) : Source Document Name : Very Low : ""
  - notes (VARCHAR) : Additional Notes : Low : ""

---
 
"""
 
CONTRACT_SUMMARY_PROMPT = f"""
You are an expert SQL generator specialized in analyzing **Contingent Commission Contracts**.
Your task is to generate an accurate SQL query based on the user's question using the provided data dictionary.

---

### Database Context

**Database:** mog_spinnaker_analytics  
**Schema:** public  
**Primary Table:** contract_summary  

This table contains historical data of contingent commission contracts extracted from contract PDFs.  
Each contract PDF may contain multiple rows, but **contract_id** represents a single unique contract (even if repeated).

---

### Data Dictionary
{CONTRACT_SUMMARY_DATA_DICTIONARY}

---

### SQL Generation Rules

#### General Rules
1. Always use **exact table and column names** from the data dictionary.
2. Always query from **public.contract_summary** unless explicitly instructed otherwise.
3. The goal is to **analyze contract performance, bonuses, carriers, and contract durations**.
4. Never hallucinate columns or tables that don’t exist.
5. Prefer **aggregate metrics (COUNT, MAX, AVG, etc.)** when the user asks "how many", "average", "total", or "top".
6. Always use **snake_case** for SQL syntax consistency.

---

### Column Interpretation & Semantic Rules

- **contract_id** → Represents one unique contract, but may appear in multiple rows.  
  → Use `COUNT(DISTINCT contract_id)` when counting unique contracts.
  
- **carrier** → Identifies the insurance carrier. Always include it when comparing or grouping across carriers.

- **bonus** → Numeric bonus percentage.  
  → When user asks for "highest bonus", "best contract", or "top contracts", use `MAX(bonus)`.

- **effective_date** / **expiration_date** → Represent the contract’s active duration.  
  → A contract is **active in a given year (e.g., 2025)** if that year falls **between** its effective and expiration dates:
    ```sql
    WHERE EXTRACT(YEAR FROM effective_date) <= 2025
      AND EXTRACT(YEAR FROM expiration_date) >= 2025
    ```
  → Avoid using current date or null checks unless user specifies “current” or “ongoing”.

- **year** → Use only when explicitly mentioned by user (e.g., “for year 2023”), not as a date filter for activity.

- **threshold**, **threshold_applied_to**, **bonus_type**, **program_name** → Use in filtering, grouping, or descriptive output if user refers to them.

---

### Common Query Patterns

**Counting contracts**
- Always use:
  ```sql
  SELECT COUNT(DISTINCT contract_id) AS total_contracts
  FROM contract_summary
  
**Active contracts by year**

- Example: "How many contracts are active in 2025?"
  SELECT COUNT(DISTINCT contract_id) AS active_contracts_2025
  FROM contract_summary
  WHERE EXTRACT(YEAR FROM effective_date) <= 2025
    AND EXTRACT(YEAR FROM expiration_date) >= 2025
    
** Active Contracts by Year**

- Example: "How many contracts are active in 2025?"
  SELECT COUNT(DISTINCT contract_id)
  FROM contract_summary
  WHERE year = 2025

    
**Top bonus by carrier**

- Example: "Show me the top bonus by each carrier"
  SELECT carrier, MAX(bonus) AS top_bonus
  FROM contract_summary
  GROUP BY carrier
  ORDER BY top_bonus DESC
  
**Best-performing contract**

- Example: "Which is the best contract?"
  SELECT DISTINCT contract_id, carrier, program_name, bonus
  FROM contract_summary
  WHERE bonus = (SELECT MAX(bonus) FROM contract_summary);
  

**Behavioral Rules**

- For grouping or comparison:

 - When user says “by” or “for each”, add a GROUP BY clause with that dimension.

 - Example: “Show bonus by carrier” → GROUP BY carrier.

- For filtering:

 - When user specifies a value or condition, add a WHERE clause.

 - Example: “contracts for carrier ABC” → WHERE carrier ILIKE '%ABC%'.

- For summarization:

 - When user says “summary” or “overview”, return aggregated metrics (count, average bonus, etc.).

- For top-N results:

 - When user says “top 5”, “highest”, or “best”, use ORDER BY ... DESC LIMIT N.

- Always prefer DISTINCT for contract_id

 - Never double-count repeated contract_id rows.

- Avoid NULL rows unless explicitly required

 - Exclude NULL values from aggregations unless user requests them.

**Output Format**

 - Output must be a single executable SQL query (no explanations, no markdown formatting).

 - The query should be valid PostgreSQL syntax.

Now, generate the most accurate and optimized SQL query based on the user’s question.
"""


PRODUCT_ALLOWED_TABLES = {
    "market-overview": ["il_mi_population", "il_mi_life_agents_by_zipcode", "mi_master_geo", "il_mi_market", "il_mi_mog","il_mi_client_dummy", "il_mi_income"],
    "il_mi_sales_opty": [],
    "il_mi_agent_performance": [],
    "contract-summary": ["contract_summary"],
}


def build_postgres_uri():
    print(f"user: {user}_{password}_{host}_{port}_{dbname}")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

def initialize_db(allowed_tables: list[str] | None = None):
    """
    - Connect to Postgres
    - Discover available tables
    - Re-init LangChain SQLDatabase with filtered include_tables
    Returns: SQLDatabase instance (filtered)
    """
    print(f"initialize db: {allowed_tables} and {type(allowed_tables)}")
  
    if not (user and password and dbname):
        raise ValueError("Missing Postgres credentials in environment")

    uri = build_postgres_uri()
    if allowed_tables:
        temp_db = SQLDatabase.from_uri(uri, include_tables=allowed_tables)
        db = temp_db  # Reuse the same connection!
    else:
        db = SQLDatabase.from_uri(uri)
    
    return db


def llm_fallback(State)->State:
    print("went to llm fallback")
    prompt=ChatPromptTemplate.from_template("""You are an advanced routing assistant. Your job is to decide the correct route for a user query.

You MUST strictly output only one of the following:
- "spinnaker_questions"
- "general_questions"

### Inputs:
- Current Question: {question}
- Conversation History: {messages}

### Routing Criteria:
1. Route to **spinnaker_questions** if the question or conversation history
   mentions Spinnaker Analytics (the company), its products, offerings, services,
   tools, architecture, implementations, internal processes, or any content
   specifically related to Spinnaker Analytics.

2. Route to **general_questions** if the question:
   - is not related to Spinnaker Analytics
   - is a casual/general query
   - is general AI usage
   - is programming help
   - is small talk or unrelated content

### CRITICAL RULE:
You MUST output ONLY the word:
"spinnaker_questions"
OR
"general_questions"

NO explanation, NO sentences, NO extra text.

Now produce the route:
"""
    )
    
    question=State["question"]
    messages=State["messages"]
    # time= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    llm_fallback_chain= prompt|llm
    
    try:
        response = llm_fallback_chain.invoke({
            "question": question,
            "messages": messages,
            # "time": time
        })
        
        # Extract content from response,it always returns an object
        if hasattr(response, 'content'):
            generation = response.content
        else:
            generation = str(response)
            
        State["fallback_state"] = generation
        
    except Exception as e:
        logging.error(f"Error in llm_fallback: {e}")
        State["generation"] = "I'm having trouble processing your request. Please try again or contact info@spinnakeranalytics.com for assistance."
    
    return State

def fallback_condition(state: State) -> str:
    """Determines which node to route to based on route_to value."""
    fallback_state = state.get("fallback_state", "general_questions")
    
    if fallback_state == "general_questions":
        return "general_questions"
    else:  # llm_fallback or any other value
        return "spinnaker_questions"

def general_questions(state: State) -> str:
     
    question=state["question"]
    messages=state["messages"]
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prompt=ChatPromptTemplate.from_template("""# Sage Chatbot — Persona & Experience

Below are core details about Sage’s persona, background, and capabilities.

---

## 1. What is your name?

**Q:** What should I call you?  
**A:** I’m **Sage**, the AI assistant for Spinnaker Analytics.

---

## 2. Who are you?
**A:** I’m **Sage**, the AI assistant for Spinnaker Analytics.

**Q:** Who is Sage?  
**A:** I’m the conversational interface for Spinnaker Analytics, here to help with questions and guidance.

---

## 3. What is your knowledge cutoff?

**Q:** How current is your information?  
**A:** My training data goes up to **June 2024**. For events or developments after that, I may need you to provide context.

---

## 4. How many years of experience do you have?

**Q:** How long has your team been practicing?  
**A:** The Spinnaker Analytics team averages **15+ years** of domain expertise, and the firm has **20+ years** of cumulative industry experience.

---

## 5. Are you available around the clock?

**Q:** Can I ask you questions at any time?  
**A:** Yes—Sage is available **24/7** to respond to your queries.

---

## 6. What is your response style?

**Q:** How will you answer my questions?  
**A:** I provide **clear, detailed, and actionable** responses—especially step‑by‑step guidance or code examples you can replicate directly.

</context>
When answer to user:
1. Answer the question as truthfully as possible from the context given to you. Do not try to make up any answer if you are not sure about it. If you’re uncertain about a topic, you should reply, "’ I’m not sure about that question, please reach out to info@spinnakeranalytics.com for more information".
2. Do not disclose any information of the spinnaker employees, client names,  CEOs, Team or Leadership or any personal information(except email address: info@spinnakeranalytics.com and phone number: +1 617-303-1937.), price of products or solutions.
3. Do not answer any question related to career or job openings or finance figures, sales figures etc. or any such information that is not available in the context and do not ask for any personal information from the user.
4. If question is asked regarding the demo or buying the product/solutions redirect them towards spinnaker analytics contact-us page (https://www.spinnakeranalytics.com/contact) or request-demo (https://www.spinnakeranalytics.com/?requestDemo=true).
5. Your final answer should be visually appealing for that you can use markdown/bullets/highlight the important information as you see fit.


\n\nCurrent time: {time}
\n\nPrevious messages: {messages}
\n\nQuestion: {question}
"""
    )
    general_questions_chain= prompt|llm
    
    response= general_questions_chain.invoke({
            "question": question,
            "messages": messages,
            "time": current_time
        })
    
    state["generation"]=response.content

    return state


def spinnaker_questions(state: State) -> str:
    
    response="hi iam in spinnaker question"
    state["generation"]=response

    return state

def route_condition(state: State) -> str:
    """Determines which node to route to based on route_to value."""
    route_to = state.get("route_to", "llm_fallback")
    
    if route_to == "agent":
        return "call_agent"
    elif route_to == "redirect":
        return "handle_redirect"
    else:  # llm_fallback or any other value
        return "llm_fallback"
    

def handle_redirect(state: State) -> State:
    """Handles redirection messages when user is on wrong page."""
    print("handling redirect")
    # The generation already contains the redirect message from route_user_query
    return state

def parse_relevant_tables(value):
    """Convert '[a, b, c]' → ['a', 'b', 'c']"""
    if isinstance(value, str):
        cleaned = re.sub(r'[\[\]]', '', value)
        tables = [t.strip() for t in cleaned.split(',') if t.strip()]
        return tables
    return value

def call_your_agent(state: State) -> State:
    """Agent decides which tool to use"""
    print("Agent routing to tool")
     
    question= state["question"]
    page_url= state["page_url"]
    messages= state["messages"]
    csv_data = pd.read_csv('Spinnaker Bot Mapping.csv')
    print(page_url)
    matching_row = csv_data[csv_data['Product Catalog Module url'] == page_url].iloc[0]
    print("📋 Available columns:", csv_data.columns.tolist())

    tool = matching_row['Agent / Tool ']  
    # db_selected=matching_row['Data Source']  
    data_dict = matching_row['Data Dictionary ']  
    tool_prompt = matching_row['Tool_Prompt']  
    relevant_tables=matching_row['Relevant Tables']
    print(tool)
    # print(db_selected)
    print(data_dict)
    print(tool_prompt)
    print(relevant_tables)
  
    # Store which tool to use
    state["selected_tool"] = tool if tool else "Spinnaker_Solutions_QA_Tool"
    # state['db']= db_selected
    state['data_dict']= data_dict
    state['tool_prompt']= tool_prompt
    state['relevant_tables'] = parse_relevant_tables(relevant_tables)

    return state
    


def sql_qa_tool(state: State) -> State:
    """Tool node for SQL queries"""
    print("Executing SQL_QA_Tool")

    question=state["question"]
    tool_prompt=state["tool_prompt"]
    relevant_tables=state["relevant_tables"]
    print(f"Tool prompt name: {tool_prompt} ")
    print(f"Relevant tables: {relevant_tables} and type: {type(relevant_tables)}")
    db= initialize_db(relevant_tables)
    # db= state["db"]  
    print("hello world")
    print(db)
    print("✅ Connected tables:", db.get_usable_table_names())
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    

    
    try:
      print("iam in the try")
      print(">>> DEBUG: question =", repr(question))

      if tool_prompt=="MOG_IL_PROMPT":
          tool_prompt=MOG_IL_PROMPT
      
      formatted_system_prompt = REACT_SQL_PROMPT.format(
        input=question,
        agent_scratchpad="",
        chat_history="",
        product_prompt=tool_prompt,
        tools="", 
        tool_names=""
    )
      agent = create_agent(model=llm,
        tools=tools,
        system_prompt=formatted_system_prompt)
    #   print(f"the tool prompt is:{tool_prompt}") 
      agent_response = agent.invoke({"input": question, "product_prompt": tool_prompt})
      print(f"*********** agent_response:{agent_response}")
      content = agent_response.get("output")
      print("============================")
      print(f"hi i am content:{content}")
      print('-------------------------------')
      print(f"Final response: {agent_response.get("Final Answer")}")
      messages = agent_response["messages"]
      print('000000000000000000')
      print(f"MEssages: {messages}")
      last_msg = messages[-1]   # the final AIMessage
      print("111111111111111")
      print(f"last msg: {last_msg}")
      content = last_msg.content
      print("FINAL RAW CONTENT:", content)


# Find the JSON part after "Final Answer:"
      match = re.search(r"Final Answer:\s*(\{.*\})", content, re.DOTALL)

      if match:
            data = json.loads(match.group(1))
            print("SQL Query:", data["sql_query"])
            print("Assumptions:", data["assumptions"])
      else:
            print("Final Answer not found.")

      state["generation"] = data["sql_query"]
    except Exception as e:
        error_message = f"sql_agent Could not parse SQL: {e}"
        print(error_message)

        # Store the error in the generation field for traceability
        state["generation"] = error_message

        # Option 1: return the whole state, including the error
    return state    
       

def contract_comparator_tool(state: State) -> State:
    """Tool node for contract comparison"""
    print("Executing Contract_Comparator_Tool")
    
    question = state["question"]
    # Your comparison logic here
    result = "iam in contract comparator tool"
    
    state["generation"] = result
    return state


def spinnaker_qa_tool(state: State) -> State:
    """Tool node for Spinnaker info"""
    print("Executing Spinnaker_Solutions_QA_Tool")
    
    question = state["question"]
    # Your QA logic here
    result = "iam in spinnaker qa tool"
    
    state["generation"] = result
    return state


def tool_router(state: State) -> str:
    """Route to appropriate tool based on agent decision"""
    selected_tool = state.get("selected_tool", "spinnaker_qa_tool")
    
    if selected_tool == "SQL_QA_Tool":
        return "sql_qa_tool"
    elif selected_tool == "Contract_Comparator_Tool":
        return "contract_comparator_tool"
    else:
        return "spinnaker_qa_tool"