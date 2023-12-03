import streamlit as st
import pandas as pd

def file_uploader(expected_file_type: list):
    st.write("Upload a bank statement file")
    bank_options = ["BMO", "CIBC"]
    card_options = ["Credit Card", "Debit Card"]
    uploaded_file = st.file_uploader("Choose a file", type=expected_file_type)
    bank_selected = st.selectbox("For Which Bank?", bank_options)
    card_selected = st.selectbox("For Which Card?", card_options)
    submit_button = st.button("Submit")
    if bank_selected not in bank_options or card_selected not in card_options:
        st.error("Bank and/or card not valid!", icon="⛔️")
    else:
        if uploaded_file is not None and submit_button:
            st.success("File Upload Successfully!", icon="✅")
            if bank_selected == "CIBC":
                df = pd.read_csv(uploaded_file, header=None)
            else:
                df = pd.read_csv(uploaded_file)
            return df, bank_selected, card_selected
        elif uploaded_file is None and submit_button:
            st.error("File Not Found!", icon="⛔️")