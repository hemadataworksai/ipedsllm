import os
from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import load_dotenv


class DatabaseInformationRetrieval:
    def __init__(self, db_url:str):
        self.db = SQLDatabase.from_uri(db_url)

    # Retrieves the column names and data types for a given table in the database.
    def get_table_columns(self, table_name:str):
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


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    db_url = os.getenv("DB_URL")

    SQL_generator= DatabaseInformationRetrieval(db_url=db_url)