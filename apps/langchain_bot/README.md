# Python ChatBot Application

## 1. langchain_bot
This directory contains a Python-based backend service using `FastAPI` and `Uvicorn`. It provides endpoints for:

  - Storing chat history in `Redis`
  - Utilizing user-specific chat history for real-time agent interactions
  - Retrieving table details from ```/data/data_for_embedding/tableinfo.json``` 
  - Generating SQL queries based on user requests
  - Connect to `Postgres` Database and perform query and getting results
  - Rephrasing the SQL results into a friendly answer.

The service integrates these components to efficiently fetch and process data in response to end-user queries.

