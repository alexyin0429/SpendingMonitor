from modules.db_functions import user_login
from config.page_config import config_page
from streamlit_extras.switch_page_button import switch_page 
import streamlit as st
import time

def login():
    config_page()
    st.header('Spending Monitor 📈')
    st.title("Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            # Attempt to log in
            user = user_login(email, password)
            if user:
                st.success("Login successful!")
                time.sleep(1)
                switch_page("dashboard")
        except ValueError as err:
            st.error(f"Login failed: {err}")
    if st.button("New User? Sign Up Here!"):
        switch_page("signup")

if __name__ == "__main__":
    login()