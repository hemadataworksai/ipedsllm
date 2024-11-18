from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
collection_name = os.getenv('COLLECTION_NAME')
CHROMADB_HOST = os.getenv('CHROMADB_HOST')
CHROMADB_PORT = os.getenv('CHROMADB_PORT')

settings = Settings(anonymized_telemetry=False, allow_reset=True,chroma_server_host=CHROMADB_HOST,chroma_server_http_port=CHROMADB_PORT,chroma_server_api_default_path= "/api/v1" )

client = chromadb.Client(settings=settings)

embedding_function = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY, model=os.getenv('TEXT_EMBEDDING')
)

vectorstore = Chroma(client=client, collection_name=collection_name,
                     embedding_function=embedding_function)

retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}
Search for the table descriptions in the context and accordingly search for column names and associated column description. Include only relevant tables and columns which can be used by the downstream Text-to-SQL Agent to create SQL Queries for generating answer.
Search for any information performing the following tasks:
1. Table Names
2. Table Descriptions
3. Column Names
4. Column Descriptions
5. Encoded Values
Finally, only return table names, column names and Encoded Values only (if available).

Question: {question}
"""
retriever_prompt = ChatPromptTemplate.from_template(template)