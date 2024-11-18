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
from langchain.chat_models import ChatOpenAIfrom 

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
db_url = os.getenv("DB_URL")
db = SQLDatabase.from_uri(db_url)

class SQLGenerator:
    def __init__(self, db):
        self.db = db_connection

    def get_table_columns(self, table_name):
        query_columns = f"PRAGMA table_info({table_name});"
        columns_info = self.db.execute(query_columns).fetchall()
        return [(col[1], col[2]) for col in columns_info]

    def get_sample_rows(self, table_name, limit=3):
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        sample_rows = self.db.execute(query).fetchall()
        return "\n".join([str(row) for row in sample_rows])

