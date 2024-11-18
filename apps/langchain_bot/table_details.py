from typing import List
import pandas as pd
from operator import itemgetter
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

def get_table_details():
    table_description = pd.read_csv(os.getenv('DATA_DICT_PATH'))
    
    table_details = ""
    for _, row in table_description.iterrows():
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

table_details = get_table_details()
table_details_prompt = f"""Refer the Above Context and Return the names of SQL Tables mentioned in the above context\n\n 
The tables are:

{table_details}
 """

table_chain = {"input": itemgetter("question")} | create_extraction_chain_pydantic(
    Table, llm, system_message=table_details_prompt) | get_tables
