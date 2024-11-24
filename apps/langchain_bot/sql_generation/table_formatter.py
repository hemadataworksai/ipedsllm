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
