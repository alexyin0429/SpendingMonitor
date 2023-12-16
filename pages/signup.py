from config.page_config import config_page
from modules.db_functions import user_signup, store_user_id_in_session
from streamlit_extras.switch_page_button import switch_page 
import streamlit as st

def signup():
    config_page()
    st.title("Sign Up Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if password != confirm_password:
        st.error("The two password entries do not match! Please double check entries.")
    else:
        if st.button("Sign up"):
            # Attempt to sign up
            user, error = user_signup(email, password)
            if user:
                st.success("Signed up successfully!")
                store_user_id_in_session(user['localId'])
                if st.button("📊 Dashboard"):
                    switch_page("dashboard")
            else:
                st.error(f"Sign up failed: {error}")

if __name__ == "__main__":
    signup()