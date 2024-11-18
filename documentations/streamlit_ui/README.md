# Python ChatBot Application


## 1. streamlit_ui
This directory contains Streamlit-based frontend services that:

  - Create endpoints using `user_id` and `conversation_id`
  - Establish user sessions
  - Integrate with the Redis DB Chat History service
  - Utilize `Langserve` technology to invoke HTTP POST methods
  - Connect to the FastAPI backend modules

The frontend services manage user interactions and seamlessly communicate with the backend to provide a cohesive chat experience.