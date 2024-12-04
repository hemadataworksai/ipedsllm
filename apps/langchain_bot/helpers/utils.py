import re
from typing import  Callable, Dict, Any

from fastapi import HTTPException
from flask import Request
from langchain_community.chat_message_histories import UpstashRedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from apps.langchain_bot.env import redis_url, redis_token


def _is_valid_identifier(value: str) -> bool:
    """Check if the value is a valid identifier."""
    valid_characters = re.compile(r"^[a-zA-Z0-9-_]+$")
    return bool(valid_characters.match(value))



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

# function to modify the config for each request
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
