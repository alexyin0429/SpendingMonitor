import streamlit as st

def config_page():
    st.set_page_config(
        page_title="Spending Monitor App",
        page_icon="💰",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    return None