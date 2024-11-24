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
# Function to retrieve table details from a CSV file and return formatted descriptions
def get_table_details():
    table_description = pd.read_csv(os.getenv('DATA_DICT_PATH'))
    
    table_details = ""
    # Iterate through each row in the table description CSV file
    for _, row in table_description.iterrows():
        # Concatenate the table name and description to the table_details string
        table_details = table_details + "Table Name:" + \
            row['Table'] + "\n" + "Table Description:" + \
            row['Description'] + "\n\n"

    return table_details

# Define a Pydantic model for representing a table in an SQL database
class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")

# Function to extract a list of table names from a list of Table objects
def get_tables(tables: List[Table]) -> List[str]:
    tables = [table.name for table in tables]
    return tables
# Retrieve the formatted table details (name and description) from the CSV
table_details = get_table_details()
table_details_prompt = f"""Refer the Above Context and Return the names of SQL Tables mentioned in the above context\n\n 
The tables are:

{table_details}
 """

# Chain definition for extracting table names using the provided LLM and prompt template
table_chain = {"input": itemgetter("question")} | create_extraction_chain_pydantic(
    Table, llm, system_message=table_details_prompt) | get_tables
