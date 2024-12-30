import os

from apps.langchain_bot.env import db_url

from apps.langchain_bot.phases.context.vectors_store_sentence_transformer import DocumentRetriever
from apps.langchain_bot.utils.db_information.database_information_retrieval import DatabaseInformationRetrieval
from apps.langchain_bot.utils.llm_provider.llm_provider import LLMProvider
#TODO: Add comments- such as these are Helper functions to do x, y, x
database_information_retrieval = DatabaseInformationRetrieval(db_url=db_url)
document_retriever = DocumentRetriever()
llm = LLMProvider(provider=os.getenv("LLM_PROVIDER",None))
