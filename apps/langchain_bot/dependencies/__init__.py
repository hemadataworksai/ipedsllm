import os

from apps.langchain_bot.env import db_url

from apps.langchain_bot.context.vectors_store_sentence_transformer import DocumentRetriever
from apps.langchain_bot.db_information.database_information_retrieval import DatabaseInformationRetrieval
from apps.langchain_bot.llm_provider.llm_provider import LLMProvider
from apps.langchain_bot.table_formatter.table_formatter import TableFormatter

table_formatter = TableFormatter()
database_information_retrieval = DatabaseInformationRetrieval(db_url=db_url)
document_retriever = DocumentRetriever()
llm = LLMProvider(provider=os.getenv("LLM_PROVIDER",None))