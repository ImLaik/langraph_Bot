
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
import re

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
 
MOG_DATA_DICTIONARY = """
# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** public

---
 
## Tables Overview
 
This database contains 9 tables for analytics on insurance market data, agent performance, geographic information, and sales opportunities.
 
---
 
## Table: il_mi_master_geo
 
Geographic reference table containing zipcode and location information.
 
**Columns:**
- zipcode (VARCHAR): Zipcode as text
- zip_code (INT): Zipcode as integer
- locale_name (VARCHAR): Locality name
- physical_delivery_address (VARCHAR): Physical delivery address
- physical_city (VARCHAR): City name
- physical_state (VARCHAR): State abbreviation
- physical_zip (NUMERIC): Physical zipcode
- physical_zip_4 (NUMERIC): Zipcode +4 extension
- zcta (NUMERIC): ZIP Code Tabulation Area
- po_name (VARCHAR): Post office name
- zip_type (VARCHAR): Type of zipcode
- zip_join_type (VARCHAR): Join type classification
- county_fips (NUMERIC): County FIPS code
- primary_state (VARCHAR): Primary state
- state_id (NUMERIC): State identifier
- county_id (NUMERIC): County identifier
- county_name (VARCHAR): Full county name
- county_name_short (VARCHAR): Short county name
- county_state (VARCHAR): County and state combined
- county_state_name (VARCHAR): County and state full name
- msa_id (VARCHAR): Metropolitan Statistical Area ID
- msa_name (VARCHAR): MSA full name
- msa_name_short (VARCHAR): MSA short name
- msa_name_type (VARCHAR): MSA type classification
- latitude (NUMERIC): Latitude coordinate
- longitude (NUMERIC): Longitude coordinate
- population_2021 (NUMERIC): Population as of 2021
- household (NUMERIC): Number of households
- household_income (NUMERIC): Median household income
- market_agents (NUMERIC): Number of market agents
- zipcode_state (VARCHAR) **[PRIMARY KEY]**: Combined zipcode and state key
 
---
 
## Table: il_mi_market
 
Historical insurance data by year, state, zipcode, and product , for entire market(USA)
 
**Columns:**
- year (INT): Year of data
- state (VARCHAR): State abbreviation
- zipcode (INT): Zipcode
- product (VARCHAR): Insurance product type
- premium (NUMERIC): Premium amount (Market)
- policies (NUMERIC): Number of policies (Market)
- face_amount (NUMERIC): Face amount of policies (Market)
- metric (VARCHAR): Metric type
- zipcode_state (VARCHAR) **[FOREIGN KEY → master_geo.zipcode_state]**: Combined zipcode and state key
 
---
## Table: il_mi_client_dummy
 
Historical data for client by year, state, zipcode, and product.
 
**Columns:**
- year (INT): Year of data
- state (VARCHAR): State abbreviation
- zipcode (INT): Zipcode
- product (VARCHAR): Insurance product type
- premium (NUMERIC): Premium amount
- policies (NUMERIC): Number of policies
- face_amount (NUMERIC): Face amount of policies
- metric (VARCHAR): Metric type
- zipcode_state (VARCHAR) **[FOREIGN KEY → master_geo.zipcode_state]**: Combined zipcode and state key
 
---
 
 
 
## Table: il_mi_sales_opty
 
Sales opportunity analysis by territory and market.
 
**Columns:**
- year (INT): Year of data
- state (VARCHAR): State abbreviation
- territory (INT): Territory code
- msa (VARCHAR): Metropolitan Statistical Area
- product (VARCHAR): Insurance product type
- market_size (NUMERIC): Total market size
- historical_sales (INT): Historical sales count
- market_share (NUMERIC): Current market share percentage
- sales_premium_opportunity (NUMERIC): Total sales opportunity
- incremental_sales_premium_opportunity (NUMERIC): Additional opportunity
- agent_recruiting_opty (NUMERIC): Agent recruiting opportunity
 
---
 
## Table: il_mi_agent_performance
 
Agent performance metrics by territory and MSA.
 
**Columns:**
- state (VARCHAR): State abbreviation
- year (NUMERIC): Year of data
- territory (NUMERIC): Territory code
- msa (VARCHAR): Metropolitan Statistical Area
- life_appointed_agents (NUMERIC): Number of appointed life agents
- life_agents (NUMERIC): Total life agents
- company_agents (NUMERIC): Company agents count
- active_company_agents (NUMERIC): Active company agents
- active_agent_apps (NUMERIC): Applications by active agents
- active_agents_premium (NUMERIC): Premium from active agents
- incremental_sales_opty (NUMERIC): Incremental sales opportunity
- active_ratio (NUMERIC): Ratio of active agents
- premium_per_agent (VARCHAR): Premium per agent
- productivity_target (NUMERIC): Productivity target
- market_premium (NUMERIC): Total market premium
- premium_share (NUMERIC): Premium share percentage
- premium_share_norm (NUMERIC): Normalized premium share
- agent_share (NUMERIC): Agent share percentage
- agent_share_norm (NUMERIC): Normalized agent share
- sales_effectivess_per_agent (NUMERIC): Sales effectiveness metric
- sales_effectivess_per_agent_norm (NUMERIC): Normalized effectiveness
- marketing_spend (NUMERIC): Marketing spend amount
- marketing_spend_norm (NUMERIC): Normalized marketing spend
- premium_earned_per_usd_of_spend (NUMERIC): ROI metric
- premium_earned_per_usd_of_spend_norm (NUMERIC): Normalized ROI
- members (NUMERIC): Number of members
- members_norm (NUMERIC): Normalized members count
- population (NUMERIC): Population count
- population_norm (NUMERIC): Normalized population
- members_share (NUMERIC): Members share percentage
- members_share_norm (NUMERIC): Normalized members share
- members_score (NUMERIC): Members score
- members_score_norm (NUMERIC): Normalized members score
- number_of_policies (NUMERIC): Total policies
- number_of_policies_norm (NUMERIC): Normalized policies count
- number_of_policies_per_member (NUMERIC): Policies per member ratio
- number_of_policies_per_member_norm (NUMERIC): Normalized ratio
- apps_per_agent (NUMERIC): Applications per agent
 
---
 
## Table: il_mi_life_agents_by_zipcode
 
Life insurance agents distribution by zipcode.
 
**Columns:**
- year (INT): Year of data
- state (TEXT): State abbreviation
- zipcode (INT): Zipcode
- agent_count (INT): Total number of agents
- client_agents (INT): Total number of client agents
- zipcode_int (INT): Zipcode as integer
- zipcode_state (VARCHAR) **[FOREIGN KEY → master_geo.zipcode_state]**: Combined zipcode and state key
 
---
 
## Table: il_mi_income
 
Income statistics by zipcode.
 
**Columns:**
- year (INT): Year of data
- state (VARCHAR): State abbreviation
- zipcode (VARCHAR): Zipcode
- total_income (NUMERIC): Total income amount
- total_household (NUMERIC): Total households
- zipcode_state (VARCHAR) **[FOREIGN KEY → master_geo.zipcode_state]**: Combined zipcode and state key
 
---
 
## Table: il_mi_population
 
Population demographics by zipcode.
 
**Columns:**
- zipcode (INT): Zipcode
- total_population (INT): Total population
- hispanic_population (INT): Hispanic population count
- county (VARCHAR): County name
- state (VARCHAR): State abbreviation
- county_state (VARCHAR): County and state combined
- zipcode_state (VARCHAR) **[FOREIGN KEY → master_geo.zipcode_state]**: Combined zipcode and state key
 
---
 
## Table: il_mi_map_data
 
Geographic visualization data for mapping applications.
 
**Columns:**
- year (VARCHAR): Year of data
- state (VARCHAR): State abbreviation
- product (VARCHAR): Insurance product type
- msa (VARCHAR): Metropolitan Statistical Area
- metric (VARCHAR): Metric type
- value (INT): Metric value
- legend (VARCHAR): Legend classification
- color (INT): Color code
- year_state_product_msa (VARCHAR): Composite key
- color_adj (INT): Adjusted color code
- product_msa (VARCHAR): Product and MSA combination
 
---
 
## Key Relationships
 
- **all_mog_data.zipcode_state** → master_geo.zipcode_state
- **life_agents_by_zipcode.zipcode_state** → master_geo.zipcode_state
- **income_data.zipcode_state** → master_geo.zipcode_state
- **population.zipcode_state** → master_geo.zipcode_state
 
Use the `zipcode_state` column to JOIN MOG Product related tables together.
 
---
 
## Important Notes
 
1. **Date Range**: Data typically ranges from 2020-2023
2. **Geographic Scope**: Primarily US data with state and zipcode granularity
3. **Product Types**: Life insurance products (exact types in the product column)
4. **Metric Types**: Various business metrics (premium, policies, face_amount, etc.)
5. **NULL Handling**: Some columns may contain NULL values - handle appropriately
6. **Join Key**: Always use `zipcode_state` for joining geographic tables
"""
 
 
 
MOG_PROMPT = f"""You are an expert SQL query generator. Your task is to create a SQL Query from the user input for the given tables. The database and table (data dictionary) are provided below

---
     
### Data Dictionary:  
{MOG_DATA_DICTIONARY}

---
 
### CRITICAL: Use EXACT Table and Column Names from Data Dictionary
- **ALWAYS** refer to the data dictionary above for correct table names, column names, data type and its structure. 
- Use the column description for more context to generate more accurate responses 
- Select the appropriate tables to generate relevant SQL queries based on the user's request

 
## IMPORTANT: Default Values and Aggregation Rules

When user doesn't specify any dimensions, follow these default dimensions:
 
### For queries that involve tables il_mi_market, il_mi_client_dummy, il_mi_income, il_mi_population and il_mi_life_agents_by_zipcode that belongs to Market Overview / Intelligence product

**Use defaults as defined below:**
- year: 2023
- metric: 'Sales'

**Note:** If user specifies these above two dimensions then use the user input


**Rules To Follow:**
- Add additional [dimension] (e.g., state, product) to GROUP BY clause if user asks "by [dimension]" or "for [dimension]" or "where [dimension]"
- For EVERY dimension in GROUP BY, use HAVING to filter for requested values (e.g., HAVING state = 'AK')
- Do NOT use WHERE for filtering these dimensions.
- Only use WHERE for columns not included in the GROUP BY (rare for your use case).

**Examples:**
- "What's the total premium?" 
  -> GROUP BY year, metric HAVING year = 2023 AND metric = 'Sales'
- "Premium by state (for Alaska)" 
  -> GROUP BY year, state, metric HAVING year = 2023 AND metric = 'Sales' AND state = 'AK'
- "Premium by product" 
  -> GROUP BY year, product, metric HAVING year = 2023 AND metric = 'Sales' 

 
### For sales_opty:
**Defaults:**
- year: 2023 (if not specified)
 
**Add additional [dimension] to GROUP BY if user asks "by [dimension]" or "for [dimension]" or where [dimension]**
 
### For agent_performance:
**Defaults:**
- year: group by year = '2023' (if not specified)
 
**Add additional [dimension] to GROUP BY if user asks "by [dimension]" or "for [dimension]" or where [dimension]**

 
## Critical GROUP BY Rules:
 
1. **Add GROUP BY if user explicitly says:**
   - "by state"
   - "by product"
   - "by year"
   - "for each [dimension]"
   - "breakdown by [dimension]"
 
2. **If user wants a single total**
   - "What's the total premium?" → SUM() with GROUP BY **Defaults.**
   - "Show me sales opportunity" → SUM() with GROUP BY **Defaults.**
   
3. When the user asks for wallet share(s), compute it for premium, policies, and agents as client_value / market_value. 
    - Pull market metrics from il_mi_market and client metrics from il_mi_client_dummy. 
    - **Apply identical filters/dimensions to both Market and Client Numbers**. 
    - Use safe division (avoid divide-by-zero)
 
 
# Critical Rules to Follow while generating SQL query: 
- Classify query: Overall Totals vs Breakdown.
- Use the data dictionary for exact tables/columns and types.
- For Breakdown queries, add GROUP BY for requested dimensions.
- With aggregates (SUM, AVG, MIN, MAX), only use GROUP BY when a breakdown is requested; otherwise none.
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
    
    question=State["question"]
    messages=State["messages"]
    time= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    llm_fallback_chain= prompt|llm
    
    try:
        response = llm_fallback_chain.invoke({
            "question": question,
            "messages": messages,
            "time": time
        })
        
        # Extract content from response,it always returns an object
        if hasattr(response, 'content'):
            generation = response.content
        else:
            generation = str(response)
            
        State["generation"] = generation
        
    except Exception as e:
        logging.error(f"Error in llm_fallback: {e}")
        State["generation"] = "I'm having trouble processing your request. Please try again or contact info@spinnakeranalytics.com for assistance."
    
    return State

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


def call_your_agent(state: State) -> State:
    """Agent decides which tool to use"""
    print("Agent routing to tool")
    
    prompt = ChatPromptTemplate.from_template("""You are a helpful assistant responsible for routing user queries to the appropriate tool.

## CORE RULES
- Analyze the user query and page URL to determine which tool to use
- Do NOT generate SQL queries or rewrite the user query
- Return a JSON response indicating which tool should handle this query

---

## TOOL SELECTION LOGIC

### Priority One: URL-Based Tool Selection (CHECK THIS FIRST)
**Current Page URL:** {page_url}

**Match URL to Product and Tool:**

1. If page_url contains `/sales-prophet/individual-life/` → Use `SQL_QA_Tool` (MOG product)
   - Matches: `/sales-prophet/individual-life/market-overview`, `/sales-prophet/individual-life/wallet-share-assessment`, etc.

2. If page_url equals `/commission-intelligence/property-and-casualty/contract-summary` → Use `SQL_QA_Tool`

3. If page_url equals `/commission-intelligence/property-and-casualty/contract-comparison` → Use `Contract_Comparator_Tool`

4. If page_url contains `/commission-intelligence` (but not contract-comparison) → Use `SQL_QA_Tool`
   - Matches: `/commission-intelligence`, `/commission-intelligence/property-and-casualty/contract-ingestion`, etc.

5. Otherwise → Go to Priority Two (Query-Based Selection)

**IMPORTANT: If the URL matches any pattern above, you MUST use that tool.**

---

### Priority Two: Query-Based Tool Selection
If the URL does NOT match any product, analyze the user's query and match it to the Product Catalog below.

**Steps:**
1. Read the user's query carefully
2. Compare the query content against the **Keywords** in the Product Catalog
3. Identify which product the query is most likely asking about
4. Select the tool associated with that product

**CRITICAL:**
- Base your decision on the Product Catalog definitions and keywords
- If uncertain which tool to use → use `Spinnaker_Solutions_QA_Tool`

---

## PRODUCT CATALOG

1. **MOG** (Market Opportunity Generator / Market Intelligence):
   - **URL:** `/sales-prophet/individual-life/market-overview`
   - **Sub URLs:** `/sales-prophet/individual-life/wallet-share-assessment`, `/sales-prophet/individual-life/sales-opportunity`, `/sales-prophet/individual-life/agent-performance`
   - **Tool:** `SQL_QA_Tool`
   - **Keywords:** market premiums, client premiums, policies, agents, MSAs, states, counties, population, sales opportunity, carrier policies, effectiveness, premium share

2. **Commission Intelligence** (Contingent Commission):
   - **URL:** `/commission-intelligence`
   - **Sub URLs:** `/commission-intelligence/property-and-casualty/contract-ingestion`, `/commission-intelligence/property-and-casualty/contract-summary`
   - **Tool:** `SQL_QA_Tool`
   - **Keywords:** contingent commission, carrier contracts, loss ratio, eligible written premium (EWP), growth rate, thresholds

3. **Contract Comparator** (Contingent Commission Contract Comparator):
   - **URL:** `/commission-intelligence/property-and-casualty/contract-comparison`
   - **Tool:** `Contract_Comparator_Tool`
   - **Keywords:** compare contracts, side-by-side analysis, contract differences, which contract is better, carrier comparisons, bonus structure comparison

4. **Contract Summary** (Contingent Commission Contract Summary):
   - **URL:** `/commission-intelligence/property-and-casualty/contract-summary`
   - **Tool:** `SQL_QA_Tool`
   - **Keywords:** contracts summary, contract information, contract details, contract synopsis, contract abstract

5. **Generic Questions**:
   - **Tool:** `Spinnaker_Solutions_QA_Tool`
   - **Keywords:** Spinnaker Analytics, product features, demos, purchasing, who are you, how can I contact you/spinnaker, questions related to spinnaker analytics and its solutions

---

## AVAILABLE TOOLS

1. **SQL_QA_Tool**
   - Use for queries requiring data retrieval or analysis from the PostgreSQL database
   - Used by: MOG, Commission Intelligence, Contract Summary

2. **Contract_Comparator_Tool**
   - Use for side-by-side contract comparisons
   - Compares multiple contracts across commission structures, bonuses, eligibility, thresholds
   - Used by: Contract Comparator

3. **Spinnaker_Solutions_QA_Tool**
   - Use for questions about Spinnaker Analytics solutions, modules, functions, industries, product demos, and purchasing
   - Used by: General Spinnaker information queries

---

## OUTPUT FORMAT

Return a JSON object with the following structure:
{{
    "selected_tool": "SQL_QA_Tool" or "Contract_Comparator_Tool" or "Spinnaker_Solutions_QA_Tool",
    "reasoning": "Brief explanation of why this tool was selected"
}}

---

## SPECIAL CASES

### Greetings & General Capability Questions
- For greetings ("hi", "hello", "how are you") → Use `Spinnaker_Solutions_QA_Tool`
- For general capability questions → Use `Spinnaker_Solutions_QA_Tool`

### Inappropriate Queries
- For queries that are racial, sexist, or NSFW → Use `Spinnaker_Solutions_QA_Tool`
  (The tool will handle the rejection message)

---

## INPUT

Previous conversation history:
{messages}

User Query: {question}

Page URL: {page_url}

---

Return ONLY valid JSON with no additional text.

""")
    
    chain = prompt | llm | JsonOutputParser()
 
    response = chain.invoke({
        "question": state["question"],
        "page_url": state["page_url"],
        "messages": state["messages"]
    })
    # Store which tool to use
    state["selected_tool"] = response.get("selected_tool", "Spinnaker_Solutions_QA_Tool")
    
    return state


def sql_qa_tool(state: State) -> State:
    """Tool node for SQL queries"""
    print("Executing SQL_QA_Tool")

    question=state["question"]


    page_url = state.get("page_url",None)
    if page_url:
        request_url_product = page_url.split("/")[-1] if len(page_url.split("/")) > 1 else None
        print("****************",request_url_product)
        
        current_product = state.get('product')  # Returns None if 'product' key is missing


        print("****************",current_product)
        if current_product:
          if request_url_product == current_product:
              print(f"product: {request_url_product}")
              pass
          else:
              print("New product detected")
              state['product'] = request_url_product
              allowed_tables = PRODUCT_ALLOWED_TABLES.get(request_url_product, [])
              print(f"Allowed Tables: {allowed_tables}")
              state["db"] = initialize_db(allowed_tables)
        else:
            print("no product found ,product is empty in state")
            state['product'] = request_url_product
            allowed_tables = PRODUCT_ALLOWED_TABLES.get(request_url_product, [])
            print(f"Allowed Tables: {allowed_tables}")
            state["db"] = initialize_db(allowed_tables)

    else:
        print("no page url found in request ")

    contracts = state.get("contracts", [])
    metrics = state.get("metrics", [])
    
    if contracts and metrics:
        state["contracts"] = contracts
        state["metrics"] = metrics
        print(f"Using {len(contracts)} contracts and {len(metrics)} metrics")
    else:
        print("no contracts and metrics for this request")  
   
    
    print("hi iam inside create react agent")
    db= state["db"]
    print("************",db)
    if not db:
        return {"error": "No database connection."}
    
    product=state["product"]
    print("this is the product now which iam going to pass to the product prompt",product)
    product_prompt = None
    if product=="market-overview":
        product_prompt = MOG_PROMPT
    elif product=="contract-summary":
        product_prompt = CONTRACT_SUMMARY_PROMPT

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    
    agent = create_agent(model=llm,
    tools=tools,
    system_prompt=REACT_SQL_PROMPT.template)
    
    try:
      print("iam in the try")
      print(">>> DEBUG: question =", repr(question))

      agent_response = agent.invoke({"input": question, "product_prompt": product_prompt})
      content = agent_response["messages"][0].content

      print(content)

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