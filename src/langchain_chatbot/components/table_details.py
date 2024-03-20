from typing import List
import pandas as pd
import streamlit as st
from operator import itemgetter
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)


@st.cache_data
def get_table_details():
    # Read the CSV file into a DataFrame
    table_description = pd.read_csv("Data/table_descriptions.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + \
            row['Table'] + "\n" + "Table Description:" + \
            row['Description'] + "\n\n"

    return table_details


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")


def get_tables(tables: List[Table]) -> List[str]:
    tables = [table.name for table in tables]
    return tables


# table_names = "\n".join(db.get_usable_table_names())
table_details = get_table_details()
table_details_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question.\n\n Return the names of all the columns from relevant tables that MIGHT be relevant tot eh user question \
The tables are:

{table_details}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

table_chain = {"input": itemgetter("question")} | create_extraction_chain_pydantic(
    Table, llm, system_message=table_details_prompt) | get_tables
