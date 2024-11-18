from main import get_chat_session
import streamlit_authenticator as stauth
import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from register import sign_up
import os
import ast
from dotenv import load_dotenv
import uuid
load_dotenv()

st.set_page_config(page_title="Login", page_icon="👋", layout="centered")

db_url = os.getenv("POSTGRES_DB_URL")
#==========================================================DB connection=================================================================
db = SQLDatabase.from_uri(db_url)

query = f"Select email, username, password from {os.getenv('POSTGRES_USR_TBL')}"
input = db.run_no_throw(query)
credentials = {'usernames': {}}

emails = []
usernames = []
password = []

if input != '':
    for eid, un, pwd in ast.literal_eval(input):
        emails.append(eid)
        usernames.append(un)
        password.append(pwd)

    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {
            'name': emails[index], 'password': password[index]}

authenticator = stauth.Authenticate(credentials=credentials, cookie_name='user_id',
                                    cookie_key='abcdef', cookie_expiry_days=7, pre_authorized=False)
name, authentication_status, username = authenticator.login()

info, info1 = st.columns(2)

if username:
    if username in usernames:
        if authentication_status:
            authenticator.logout('Logout', 'main')
            
            user_id = username
            conversation_id = str(uuid.uuid4())
            st.write(f'Welcome *{username}*')
            
            st.session_state['user_id'] = user_id
            if 'conversation_id' not in st.session_state:
                st.session_state['conversation_id'] = None
                
            if st.session_state['conversation_id'] is None:
                st.session_state['conversation_id'] = conversation_id
            
            get_chat_session(str(st.session_state['user_id']),str(st.session_state['conversation_id']))
            
        elif not authentication_status:
            with info:
                st.error('Invalid username or password')
        else:
            with info:
                st.warning('Please fill in the credentials')
    else:
        with info:
            st.warning("Username doesn't exists. Please sign up")

if not authentication_status:
    sign_up()
    
