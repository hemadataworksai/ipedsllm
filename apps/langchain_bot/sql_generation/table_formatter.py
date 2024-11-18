from langchain_community.utilities.sql_database import SQLDatabase
import streamlit as st
from prompts import final_prompt, answer_prompt
from table_details import table_chain as select_table
from vector_store import retriever, retriever_prompt, model
from vectors_store_sentence_transformer import DocumentRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain.memory import ChatMessageHistory
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from sql_generator import SQLGenerator
# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
db_url = os.getenv("DB_URL")


SQL_generator= SQLGenerator()

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
