import streamlit_authenticator as stauth
import streamlit as st
import datetime
import re
from langchain_community.utilities.sql_database import SQLDatabase
from db_connection import db_insert
import os
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv("POSTGRES_DB_URL")

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,3}$'
    
    if re.match(email_regex, email):
        return True
    else:
        return False


def sign_up():
    db = SQLDatabase.from_uri(db_url)
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder="Enter Your Email")
        username = st.text_input(
            ':blue[Username]', placeholder="Enter your Username")
        password1 = st.text_input(
            ':blue[Password]', placeholder="Enter your Password", type='password')
        password2 = st.text_input(
            ':blue[Confirm Password]', placeholder="Confirm your Password", type='password')
        query = f"Select * from public.user_details where username = '{username}' or email = '{email}'"
        if email:
            if validate_email(email):
                if re.fullmatch(password1, password2) != None:
                    hashed_password = stauth.utilities.hasher.Hasher(
                        [password1]).generate()
                    date_joined = str(datetime.datetime.now())
                    if '' == db.run_no_throw(query):
                        data_to_insert = (
                            email, username, hashed_password[0], date_joined)
                        db_insert(data_to_insert)
                        st.write('Successfully registered')
                    else:
                        st.write('Username/Email already exists')
                else:
                    st.write('Password is not matching')
            else:
                st.write('Inavlid Email format')
        bt1, bt2, bt3, bt4, bt5 = st.columns(5)
        with bt3:
            st.form_submit_button(label=':red[Sign Up]')