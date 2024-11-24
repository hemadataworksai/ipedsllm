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

    # Retrieves the column names and data types for a given table in the database.
    def get_table_columns(self, table_name):
       # SQL query to get column information for the specified table
        query_columns = f"PRAGMA table_info({table_name});"
        #Execute the query and fetch all results
        columns_info = self.db.execute(query_columns).fetchall()
        # Return a list containing the column name and data type
        return [(col[1], col[2]) for col in columns_info]

    # Retrieves a sample of rows from a specified table, limited by the given number.
    def get_sample_rows(self, table_name, limit=3):
        # SQL query to select a sample of rows from the table with a limit
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        # Execute the query and fetch the sample rows
        sample_rows = self.db.execute(query).fetchall()
         # Join the rows into a string, each row on a new line
        return "\n".join([str(row) for row in sample_rows])

