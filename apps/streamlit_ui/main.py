import os
import streamlit as st
from langserve import RemoteRunnable
from dotenv import load_dotenv
load_dotenv()

def get_chat_session(user_id: str, conversation_id: str):
    chat = RemoteRunnable(os.getenv('FAST_API_URL'),
                          cookies={"user_id": user_id})
    
    st.title("University Explorer AI Chatbot")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        with st.chat_message("assistant"):
            st.markdown(message["response"])
    
    # Accept user input
    if prompt := st.chat_input("Ask About Institutional Demographics, Graduation and Other Resources"):        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.spinner("Generating response..."):
            with st.chat_message("assistant"):
                response = chat.invoke({"question": prompt}, {'configurable': {
                                       'conversation_id': conversation_id}})
                st.markdown(response)
                st.session_state.messages.append({"role": "user", "content": prompt, "response": response})