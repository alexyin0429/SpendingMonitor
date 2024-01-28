from config.page_config import config_page
from modules.files import file_uploader
from models.data_preprocessing import data_cleaning
import streamlit as st

config_page()
def dashboard():
    uploaded_file = file_uploader(['csv'])
    if uploaded_file is not None:
        data = uploaded_file[0]
        bank = uploaded_file[1]
        card = uploaded_file[2]
        data_clean = data_cleaning(data, bank, card)
        if not (data_clean.empty):
            st.download_button(
                label="Download data as CSV",
                data=data_clean.to_csv().encode('utf-8'),
                file_name=f'{bank}_{card}_transactions.csv',
                mime='text/csv',)

if __name__ == "__main__":
    dashboard()
