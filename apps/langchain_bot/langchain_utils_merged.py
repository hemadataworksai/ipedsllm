#
# from langchain_community.utilities.sql_database import SQLDatabase
# import streamlit as st
# from langchain.memory import ChatMessageHistory
# import os
# from dotenv import load_dotenv
#
# from vectors_store_sentence_transformer import DocumentRetriever
# from CustomLLM import CustomLLM
# from SQL_generator import SQLGenerator
# from table_formatter import TableFormatter
#
# # Load environment variables
# load_dotenv()
#
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
# LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
#
# db_url = os.getenv("DB_URL")
# db = SQLDatabase.from_uri(db_url)
#
#
# SQL_generator= SQLGenerator()
# table_formatter= TableFormatter()
# document_retriever = DocumentRetriever()
# custom_llm=CustomLLM()
#
#
# class Orchestrator:
#     def __init__(self, db, llm_provider="openai"):
#         self.sql_generator = SQLGenerator(db)
#         self.table_formatter = TableFormatter(self.sql_generator)
#         self.document_retriever = DocumentRetriever()
#         self.llm = CustomLLM(provider=llm_provider)
#         self.db_url = db_url
#         #self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
#
#
#     def generate_final_output(self, table_context):
#         # Format the table context to a string for inclusion in the prompt
#         formatted_context = self.table_formatter.doc2str(table_context)
#         return formatted_context
#
#     def compose_final_prompt(self, instructions, question, table_context):
#       # Compose the final prompt that will be used to generate the SQL query
#         return f"{instructions}\nQuestion: {question}\nContext: {table_context}"
#
#
#
#     @st.cache_resource
#     def get_chain(self, question):
#         print("Creating chain")
#         #question = itemgetter("question")
#         # Retrieve top K similar documents based on the question
#         table_context = self.document_retriever.find_top_k_similar(question=question, k=4)
#
#         # Format the context for SQL generation
#         formatted_context = self.generate_final_output(table_context)
#
#         # Create the final SQL prompt
#         final_prompt_for_sql_generate = self.compose_final_prompt(
#             instructions="Provide an SQL query for the following context:",
#             question=question,
#             table_context=formatted_context
#         )
#
#         # Generate the SQL query
#         sql_query = self.create_sql_query_chain(final_prompt_for_sql_generate)
#
#         # Execute SQL and rephrase the answer
#         with self.sql_generator.db.connect() as connection:
#             sql_results = connection.execute(sql_query).fetchall()
#
#         # Rephrase the final answer
#         final_answer = self.my_rephrase_prompt(question, sql_query, sql_results)
#         return final_answer
#
#
#     def my_rephrase_prompt(self, question, sql_query, sql_results):
#         my_prompt=f""" Given the following user question, corresponding SQL query, and SQL result, answer the user question.
#
#         Question: {question}
#         SQL Query: {sql_query}
#         SQL Result: {sql_results}
#         Answer:
#         """
#         # Invoke the LLM to rephrase the answer
#         final_answer_rephrase = self.llm.invoke(my_prompt)
#
#         return final_answer_rephrase
#
#
#     def invoke_chain(self, question, messages):
#         try:
#             chain = self.get_chain()
#             history = create_history(messages)
#             # Invoke the chain to process the question and retrieve the response
#             response = chain.invoke({"question": question, "top_k": 3, "messages": history.messages})
#             # Add the question and the AI response to the  history
#             history.add_user_message(question)
#             history.add_ai_message(response)
#             # If the response is empty or contains an error, return an error message
#             if not response or response.strip() == "" or "error" in response:
#                 return "Sorry, I couldn't find any specific information related to your query. Please try asking something else or provide more details!"
#
#             return response
#
#         except Exception as e:
#             print(f"Error invoking chain: {e}")
#             return "Sorry, an error occurred while processing your request."
#
#    # Create a history object from the provided list of messages
#     def create_history(messages):
#         history = ChatMessageHistory()
#         for message in messages:
#             if message["role"] == "user":
#                 history.add_user_message(message["content"])
#             else:
#                 history.add_ai_message(message["content"])
#         return history
#
#
# #Testing
# if __name__=="__main__":
#    orchestrator = Orchestrator(db, llm_provider="openai")
#    question= "how many institutions are there in Boston?"
#    response= Orchestrator.invoke_chain(question, [])
#    print(response)
#
# #if __name__ == "__main__":
#     #response = Orchestrator.invoke_chain("how many institutions are in boston?", "")
#     #print(response)
#
#
#
#