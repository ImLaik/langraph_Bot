# from controllers.Web_Bot.chains import rag_chain
# from controllers.SQL_Bot.chains import sql_chain
# from controllers.Helper.state import state
# from controllers.Comparator.chains import comparator
# from langchain.agents import Tool
# import asyncio

# def spinnaker_solutions_qa_tool_sync(input_data) -> str:
#     # Wrap input as dict if it is just a string
#     if isinstance(input_data, str):
#         input_dict = {"question": input_data}
#     else:
#         input_dict = input_data

#     return asyncio.run(spinnaker_solutions_qa_tool_async(input_dict))


# async def spinnaker_solutions_qa_tool_async(input_data) -> str:
#     if isinstance(input_data, str):
#         input_dict = {"question": input_data}
#     else:
#         input_dict = input_data

#     question = input_dict["question"]
#     chat_history = input_dict.get("chat_history") or state.global_chat_history
#     response = await rag_chain.ainvoke(
#         {"question": question, "chat_history": chat_history}
#     )
#     return response


# def sql_qa_tool_wrapper_sync(input_data: dict) -> str:
#     return asyncio.run(sql_qa_tool_wrapper_async(input_data))


# async def sql_qa_tool_wrapper_async(input_data: dict) -> str:
#     if isinstance(input_data, str):
#         input_dict = {"user_query": input_data, "chat_history": []}
#     else:
#         input_dict = input_data

#     response = await sql_chain.ainvoke(input_dict)
#     return response


# def comparator_sync(input_data) -> str:
#     # Wrap input as dict if it is just a string
#     if isinstance(input_data, str):
#         input_dict = {"question": input_data}
#     else:
#         input_dict = input_data

#     return asyncio.run(comparator_async(input_dict))


# async def comparator_async(input_data) -> str:
#     if isinstance(input_data, str):
#         input_dict = {"question": input_data}
#     else:
#         input_dict = input_data

#     question = input_dict["question"]
#     chat_history = input_dict.get("chat_history") or state.global_chat_history
#     response = await comparator.ainvoke(
#         {"question": question, "chat_history": chat_history}
#     )
#     return response


# # Define tools
# spinnaker_vector_db_tool = Tool(
#     name="Spinnaker_Solutions_QA_Tool",
#     func=spinnaker_solutions_qa_tool_sync,
#     coroutine=spinnaker_solutions_qa_tool_async,
#     description="""Use this tool to answer questions specifically related to Spinnaker Analytics, including its solutions, products, industries, functions, use cases, and modules.
#     This tool provides concise, user-engaging summaries with links to official product pages (if available), and suggests requesting a demo whenever the topic is about solutions, products, functions, or modules. 
#     If the context does not provide an answer, it will direct the user to Spinnaker's official contact channels.

#     When to use this tool:
#     - The user asks about Spinnaker Analytics’ solutions, products, capabilities, industries served, or application areas.
#     - The user asks about how to request a demo or purchase a Spinnaker Analytics solution.
#     - The question requires value proposition, product suite info, or industry/function/module coverage from Spinnaker Analytics.

#     When NOT to use:
#     - The query asks for Spinnaker Analytics’ employee, executive, or client names, pricing, financials, or confidential/internal company information.
#     - The question is about career/job opportunities or unrelated to Spinnaker Analytics.
#     """
# )

# sql_db_tool = Tool(
#     name="SQL_QA_Tool",
#     func=sql_qa_tool_wrapper_sync,
#     coroutine=sql_qa_tool_wrapper_async,
#     description= """Use this tool to generate expert-level, read-only SQL queries for a PostgreSQL database, following a strict ReAct reasoning format (Thought/Action/Observation). 
#     This tool constructs correct SELECT/EXPLAIN/SHOW queries based on user questions about data extraction or analysis. 
#     The agent will only use SELECT, WITH, EXPLAIN, or SHOW statements by default, and always prefers explicit columns over SELECT *, adding LIMIT 100 unless otherwise specified.

#     When to use this tool:
#     - The user asks for data, insights, or analysis that requires constructing a SQL query.
#     - The user question can be answered by querying a PostgreSQL database.
#     - The task is to write, debug, modify, or explain a SQL statement.

#     When NOT to use:
#     - The user requests operations outside read-only actions, unless explicitly asked for data modification.
#     - The request cannot be represented as a SQL query ("-- NO_SQL_POSSIBLE;" will be returned).
#     - The input is not related to database querying or analysis.

#     Output from this tool is just the SQL query, strictly following the required step-by-step output format.
#     """
# )

# contract_comparator_tool = Tool(
#         name="Contract_Comparator_Tool",
#         func=comparator_sync,
#         coroutine=comparator_async,
#         description="""Analyze and compare insurance agent contracts from multiple carriers and plans using key metrics such as program bonus type, eligibility criteria, bonus ranges, payment timing, jurisdiction, and more.
#     This tool evaluates contract features, strengths, and weaknesses according to user-defined priorities and questions.
#     It delivers side-by-side comparisons, highlights tradeoffs, and recommends the best contract based on performance across selected metrics.
#     Use this tool to assist agents in making informed contract decisions.
#     """
#     )


# # Define tools
# tools = [
#     spinnaker_vector_db_tool,
#     sql_db_tool,
#     contract_comparator_tool
# ]
