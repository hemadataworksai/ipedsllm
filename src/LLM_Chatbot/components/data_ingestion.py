import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

# Access environment variables


def db_connect():
    """
    This function connects to the database and returns the connection object.
    """
    # DB connection string
    db_url = os.getenv("DB_URL")
    # Create a database connection
    engine = create_engine(db_url)

    # Creating a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Connecting and creating a cursor
    connection = engine.connect()

    return engine, connection, session


def execute_sql_query(query, connection):
    """
    This function executes the SQL query and returns the result.
    """
    result = connection.execute(text(query))
    rows = result.fetchall()

    # Printing the rows
    for row in rows:
        print(row)

    # Closing the connection
    connection.close()

    return rows


# # Example usage
# if __name__ == "__main__":
#     engine, connection, session = db_connect()
#     query = "SELECT * FROM \"ADM2022\" LIMIT 5"
#     execute_sql_query(query, connection)
