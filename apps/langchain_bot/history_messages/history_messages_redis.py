import json
import logging
from typing import List, Optional

import redis
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import (
    BaseMessage,
    message_to_dict,
    messages_from_dict,
)
logger = logging.getLogger(__name__)


class RedisChatMessageHistory(BaseChatMessageHistory):
    """Chat message history stored in an Redis database."""

    def __init__(
            self,
            session_id: str,
            url: str = "",
            token: str = "",
            key_prefix: str = "message_store:",
            ttl: Optional[int] = None,
    ):

        if url == "" or token == "":
            raise ValueError(
                "REDIS_URL and REDIS_TOKEN are needed."
            )

        try:
            self.redis_client = redis.Redis.from_url(url=url)
        except Exception:
            logger.error("Redis instance could not be initiated.")

        self.session_id = session_id
        self.key_prefix = key_prefix
        self.ttl = ttl

    @property
    def key(self) -> str:
        """Construct the record key to use"""
        return self.key_prefix + self.session_id

    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        """Retrieve the messages from Redis"""
        _items = self.redis_client.lrange(self.key, 0, -1)
        items = [json.loads(m) for m in _items[::-1]]
        messages = messages_from_dict(items)
        return messages

    def add_message(self, message: BaseMessage) -> None:
        """Append the message to the record in Redis"""
        self.redis_client.lpush(self.key, json.dumps(message_to_dict(message)))
        if self.ttl:
            self.redis_client.expire(self.key, self.ttl)

    def clear(self) -> None:
        """Clear session memory from Redis"""
        self.redis_client.delete(self.key)
