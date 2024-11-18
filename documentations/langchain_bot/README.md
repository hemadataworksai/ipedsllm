# Python ChatBot Application


## 1. langchain_bot
This directory contains a Python-based backend service using `FastAPI` and `Uvicorn`. It provides endpoints for:

  - Storing chat history in `Redis`
  - Utilizing user-specific chat history for real-time agent interactions
  - Retrieving `PostgreSQL` table details from a `Chroma DB` collection
  - Generating SQL queries based on user requests

The service integrates these components to efficiently fetch and process data in response to end-user queries.

