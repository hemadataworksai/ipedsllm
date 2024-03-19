from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate, PromptTemplate

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=get_example_selector(),
    input_variables=["input", "top_k"],
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a PostgreSQL expert. Given an input question, create a syntactically correct PostgreSQL query to run.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.\n\nDO NOT MAKE ANY DML QUERIES SUCH AS INSERT, UPDATE, DELETE, OR ANY OTHER DDL QUERIES SUCH AS CREATE, ALTER, DROP"),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)
