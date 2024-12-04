from dotenv import load_dotenv

from apps.langchain_bot.dependencies import document_retriever, table_formatter, llm


def get_context(question:str) -> str:
    context = document_retriever.find_top_k_similar(question,k=3)
    return table_formatter.doc2str(context)


def create_final_prompt(question, context) -> str:
    return f"Question : {question} \n Context : {context}"


def generate_sql_llm(final_prompt:str):
    return llm.invoke(final_prompt)


def get_query_results(sql_query:str):
    pass


def rephrase_query_results(query_results):
    pass



def get_chain(question:str):
    context:str =  get_context(question)
    final_prompt:str = create_final_prompt(question,context)
    sql_query:str  = generate_sql_llm(final_prompt)
    # query_results = get_query_results(sql_query)
    # friendly_answer:str = rephrase_query_results(query_results)

    return sql_query

if __name__ == '__main__':
    load_dotenv()
    chain = get_chain('Hello World')
    print(chain)

#
# db = SQLDatabase.from_uri(db_url)
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# # Create a context chain for processing input and generating the query using retriever and  llm
# context_chain = (
#         {"context": itemgetter("question") | retriever,
#          "question": itemgetter("question")}
#         | retriever_prompt
#         | llm
#         | StrOutputParser()
# )
# # Create a chain for generating the SQL query based on the LLM and final prompt
# generate_query = create_sql_query_chain(llm, db, final_prompt)
# # Create a tool to execute the query on the SQL database
# execute_query = QuerySQLDataBaseTool(db=db)
# rephrase_answer = answer_prompt | llm | StrOutputParser()
# # Build a final chain that assigns context, generates SQL queries, executes the query, and rephrases the answer
# chain = (
#         RunnablePassthrough.assign(context=context_chain, table_names_to_use=select_table) |
#         RunnablePassthrough.assign(query=generate_query).assign(
#             result=itemgetter("query") | execute_query
#         )
#         | rephrase_answer
# )
