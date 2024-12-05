from typing import List, Any

from langchain_core.messages import HumanMessage
from typing_extensions import TypedDict


# Define the input structure for the chat endpoint
class InputChat(TypedDict):
    """Input for the chat endpoint."""
    """Human input"""
    question: str
    messages :List[HumanMessage]