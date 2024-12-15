from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from apps.langchain_bot.dependencies import document_retriever, table_formatter, llm

#get top k tables based on user's query and format to string 
def get_context(inputs : dict) -> str:
    context = document_retriever.find_top_k_similar(inputs["question"],k=3)
    return table_formatter.doc2str(context)


def create_final_prompt(question, context) -> str:
    return f"Question : {question} \n Context : {context}"


def generate_sql_llm(final_prompt:str):
    return llm.invoke(final_prompt)
# TODO: complete those functions for SQL generation and rephrasing

def get_query_results(sql_query:str):
    print(sql_query)
    return "25 students"


def rephrase_query_results(query_results:str ):
    print(query_results)
    return "friendly answer"


# Wrap functions with RunnableLambda
get_context_runnable = RunnableLambda(get_context)
create_final_prompt_runnable = RunnableLambda(lambda inputs: create_final_prompt(**inputs))
generate_sql_llm_runnable = RunnableLambda(generate_sql_llm)
get_query_results_runnable = RunnableLambda(get_query_results)
rephrase_query_results_runnable = RunnableLambda(rephrase_query_results)

# Compose the chain using the pipe operator
chain = (
        RunnableParallel({
            "context": get_context_runnable,
            "question": RunnablePassthrough(),
        })
        | create_final_prompt_runnable
        | generate_sql_llm_runnable
        | get_query_results_runnable
        | rephrase_query_results_runnable
)

if __name__ == '__main__':
    load_dotenv()
    print(chain.invoke({"question" : 'how many students at Boston?',"messages" : [] } ))

