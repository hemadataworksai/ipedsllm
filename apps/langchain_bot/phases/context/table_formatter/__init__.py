from typing import List, Any


class TableFormatter:

    #function to  Formats the provided table context into a  string
    def docs2str(self, tables_context:List[Any]) -> str:
        str_context = ""
        for ix, table_info in enumerate(tables_context):
            table_name = table_info.get("Table_Name")
            table_description = table_info.get("Table_Description")
            # Format the information about the table, including its index, description, columns, and sample rows
            str_context += f"{ix + 1}. Table: {table_name}\n"
            str_context += f"   Description: {table_description}\n"
        return str_context
