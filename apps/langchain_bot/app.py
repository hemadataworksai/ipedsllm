import re
from langchain_core.chat_history import BaseChatMessageHistory
from prompts import final_prompt, answer_prompt
from table_details import table_chain as select_table
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec
from typing_extensions import TypedDict
from langchain_community.chat_message_histories import (
    UpstashRedisChatMessageHistory,
)
from chroma_retriever import retriever, retriever_prompt
from typing import Any, Callable, Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
db_url = os.getenv("POSTGRES_DB_URL")
redis_url = os.getenv("UPSTASH_URL")
redis_token = os.getenv("UPSTASH_TOKEN")

db = SQLDatabase.from_uri(db_url)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
context_chain = (
    {"context": itemgetter("question") | retriever,
     "question": itemgetter("question")}
    | retriever_prompt
    | llm
    | StrOutputParser()
)
generate_query = create_sql_query_chain(llm, db, final_prompt)
execute_query = QuerySQLDataBaseTool(db=db)
rephrase_answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(context=context_chain, table_names_to_use=select_table) |
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
)

def _is_valid_identifier(value: str) -> bool:
    """Check if the value is a valid identifier."""
    valid_characters = re.compile(r"^[a-zA-Z0-9-_]+$")
    return bool(valid_characters.match(value))

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A Chatbot for University Search",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_session_factory() -> Callable[[str, str], BaseChatMessageHistory]:
    """Create a factory that can retrieve chat histories.

    The chat histories are keyed by user ID and conversation ID.

    Returns:
        A factory that can retrieve chat histories keyed by user ID and conversation ID.
    """
    def get_chat_history(user_id: str, conversation_id: str) -> UpstashRedisChatMessageHistory:
        """Get a chat history from a user id and conversation id."""
        if not _is_valid_identifier(user_id):
            raise ValueError(
                f"User ID {user_id} is not in a valid format. "
                "User ID must only contain alphanumeric characters, "
                "hyphens, and underscores."
                "Please include a valid cookie in the request headers called 'user-id'."
            )
        if not _is_valid_identifier(conversation_id):
            raise ValueError(
                f"Conversation ID {conversation_id} is not in a valid format. "
                "Conversation ID must only contain alphanumeric characters, "
                "hyphens, and underscores. Please provide a valid conversation id "
                "via config. For example, "
                "chain.invoke(.., {'configurable': {'conversation_id': '123'}})"
            )

        return UpstashRedisChatMessageHistory(
            url=redis_url,
            token=redis_token,
            ttl=604800,
            session_id=f"{user_id}-{conversation_id}",
        )

    return get_chat_history

def _per_request_config_modifier(
    config: Dict[str, Any], request: Request
) -> Dict[str, Any]:
    """Update the config"""
    config = config.copy()
    configurable = config.get("configurable", {})
    user_id = request.cookies.get("user_id", None)
    
    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="No user id found. Please set a cookie named 'user_id'.",
        )

    configurable["user_id"] = user_id
    config["configurable"] = configurable
    return config

class InputChat(TypedDict):
    """Input for the chat endpoint."""
    question: str
    """Human input"""

chain_with_history = RunnableWithMessageHistory(
    chain,
    create_session_factory(),
    input_messages_key="question",
    history_messages_key="messages",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
).with_types(input_type=InputChat)

add_routes(
    app,
    chain_with_history,
    per_req_config_modifier=_per_request_config_modifier
)