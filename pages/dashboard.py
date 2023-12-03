from config.page_config import config_page
from modules.files import file_uploader
from models.data_preprocessing import data_cleaning
from streamlit_extras.dataframe_explorer import dataframe_explorer 
import streamlit as st
import pandas as pd

def dashboard():
    config_page()
    st.title("Your Dashboard")
    try:
        uploaded_df, bank, card = file_uploader(["csv"])
        df_clean = data_cleaning(uploaded_df, bank, card)
        filtered_df = dataframe_explorer(df_clean, case=False)
        st.dataframe(filtered_df, use_container_width=True)
    except TypeError as err:
        st.warning("No file has been uploaded.", icon="⚠️")
    




if __name__ == "__main__":
    dashboard()
