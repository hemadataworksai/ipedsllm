from typing import TypedDict


# Define the input structure for the chat endpoint
class InputChat(TypedDict):
    """Input for the chat endpoint."""
    question: str
    """Human input"""