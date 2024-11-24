from langchain_community.utilities.sql_database import SQLDatabase

class SQLGenerator:
    def __init__(self, db:SQLDatabase):
        self.db = db

    def get_table_columns(self, table_name):
        query_columns = f"PRAGMA table_info({table_name});"
        columns_info = self.db.execute(query_columns).fetchall()
        return [(col[1], col[2]) for col in columns_info]

    def get_sample_rows(self, table_name, limit=3):
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        sample_rows = self.db.execute(query).fetchall()
        return "\n".join([str(row) for row in sample_rows])

