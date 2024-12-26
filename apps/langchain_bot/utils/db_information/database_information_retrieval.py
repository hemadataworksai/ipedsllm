import os
from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import load_dotenv

class DatabaseInformationRetrieval:
    """
    A utility class for interacting with a database to retrieve metadata and sample data from tables.

    Attributes:
        db (SQLDatabase): An instance of SQLDatabase used to execute queries.
    """

    def __init__(self, db_url: str):
        """
        Initializes the DatabaseInformationRetrieval class with a database connection.

        Args:
            db_url (str): The URL of the database to connect to.
        """
        self.db = SQLDatabase.from_uri(db_url)

    def get_table_columns(self, table_name: str):
        """
        Retrieves the column names and data types for a specified table in the database.

        Args:
            table_name (str): The name of the table to retrieve column information for.

        Returns:
            list: A list of tuples where each tuple contains the column name and data type.

        Example:
            [('id', 'INTEGER'), ('name', 'TEXT'), ('age', 'INTEGER')]
        """
        # SQL query to get column information for the specified table
        query_columns = f"PRAGMA table_info({table_name});"

        # Execute the query and fetch all results
        columns_info = self.db.execute(query_columns).fetchall()

        # Return a list containing the column name and data type
        return [(col[1], col[2]) for col in columns_info]

    def get_sample_rows(self, table_name: str, limit: int = 3):
        """
        Retrieves a sample of rows from a specified table, limited by the given number.

        Args:
            table_name (str): The name of the table to retrieve sample rows from.
            limit (int): The maximum number of rows to retrieve. Default is 3.

        Returns:
            str: A string representation of the sample rows, with each row on a new line.

        Example:
            """
        (1, 'Alice', 25)
        (2, 'Bob', 30)
        (3, 'Charlie', 35)
        """
    """
        # SQL query to select a sample of rows from the table with a limit
        query = f"SELECT * FROM {table_name} LIMIT {limit};"

        # Execute the query and fetch the sample rows
        sample_rows = self.db.execute(query).fetchall()

        # Join the rows into a string, each row on a new line
        return "\n".join([str(row) for row in sample_rows])

if __name__ == "__main__":
    """
    Entry point of the script. Loads environment variables, initializes the class, and performs example operations.
    """
    # Load environment variables from a .env file
    load_dotenv()

    # Retrieve the database URL from the environment variables
    db_url = os.getenv("DB_URL")

    # Instantiate the DatabaseInformationRetrieval class
    SQL_generator = DatabaseInformationRetrieval(db_url=db_url)

    # Example usage:
    # Uncomment and replace 'table_name' with your actual table name for testing.
    # print(SQL_generator.get_table_columns("table_name"))
    # print(SQL_generator.get_sample_rows("table_name"))
