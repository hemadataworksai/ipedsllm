import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
import streamlit as st
from prompts import final_prompt, answer_prompt
from table_details import table_chain as select_table
from vectors_store_sentence_transformer import DocumentRetriever
from vector_store import retriever_prompt, retriever, model
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain.memory import ChatMessageHistory
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains import create_sql_query_chain
from langchain.chat_models import ChatOpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
db_url = os.getenv("DB_URL")

class SQLGenerator:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_table_columns(self, table_name):
        query_columns = f"PRAGMA table_info({table_name});"
        columns_info = self.db.execute(query_columns).fetchall()
        return [(col[1], col[2]) for col in columns_info]

    def get_sample_rows(self, table_name, limit=3):
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        sample_rows = self.db.execute(query).fetchall()
        return "\n".join([str(row) for row in sample_rows])


class TableFormatter:
    def __init__(self, sql_generator):
        self.sql_generator = sql_generator

    def format_to_string(self, table_context):
        str_context = ""
        for ix, table_info in enumerate(table_context):
            table_name = table_info.get("Table_Name")
            table_description = table_info.get("Table_Description")
            columns = self.sql_generator.get_table_columns(table_name)
            columns_details = "\n".join([f"{col_name} ({col_type})" for col_name, col_type in columns])
            sample_rows = self.sql_generator.get_sample_rows(table_name)
            str_context += f"{ix + 1}. Table: {table_name}\n"
            str_context += f"   Description: {table_description}\n"
            str_context += f"   Columns:\n   {columns_details}\n"
            str_context += f"   Sample Rows:\n{sample_rows}\n\n"
        return str_context


class Orchestrator:
    def __init__(self, db_connection):
        self.sql_generator = SQLGenerator(db_connection)
        self.table_formatter = TableFormatter(self.sql_generator)
        self.db_url = db_url
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    @st.cache_resource
    def get_chain(self):
        print("Creating chain")
        db = SQLDatabase.from_uri(self.db_url)
        document_retriever = DocumentRetriever()
        
        question = itemgetter("question")
        table_context = document_retriever.find_top_k_similar(question=question, k=4)

        final_prompt_for_sql_generate = self.compose_final_prompt(
            instructions="instructions_placeholder", question=question, table_context=table_context
        )

        sql_query_to_execute = create_sql_query_chain(self.llm, db, final_prompt_for_sql_generate)

        with db.connect() as connection:
            sql_results = connection.execute(sql_query_to_execute).fetchall()

        my_rephrase_prompt = f""" 
        Given the following user question, corresponding SQL query, and SQL result, answer the user question.

        Question: {question}
        SQL Query: {sql_query_to_execute}
        SQL Result: {sql_results}
        Answer: 
        """
        final_answer_rephrase = self.llm.invoke(my_rephrase_prompt)

        return final_answer_rephrase

    def generate_final_output(self, table_context):
        formatted_context = self.table_formatter.format_to_string(table_context)
        return formatted_context

    def compose_final_prompt(self, instructions, question, table_context):
        return f"{instructions}\nQuestion: {question}\nContext: {table_context}"

    def invoke_chain(self, question, messages):
        try:
            chain = self.get_chain()
            history = create_history(messages)
            response = chain.invoke({"question": question, "top_k": 3, "messages": history.messages})
            
            history.add_user_message(question)
            history.add_ai_message(response)
            
            if not response or response.strip() == "" or "error" in response:
                return "Sorry, I couldn't find any specific information related to your query. Please try asking something else or provide more details!"
            
            return response 
        
        except Exception as e:
            print(f"Error invoking chain: {e}")
            return "Sorry, an error occurred while processing your request."


def create_history(messages):
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history



