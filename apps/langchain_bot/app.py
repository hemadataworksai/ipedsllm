from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory
from langserve import add_routes

from apps.langchain_bot.chain import chain
from apps.langchain_bot.helpers.utils import  create_session_factory, _per_request_config_modifier
from apps.langchain_bot.interfaces.chat import InputChat

# FastAPI application setup with metadata
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A Chatbot for University Search",
)
# Add middleware to allow Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create a chain with history by including chat message history management
chain_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=create_session_factory(),
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
