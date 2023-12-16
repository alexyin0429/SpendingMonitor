from config.page_config import config_page
from modules.files import file_uploader
from modules.apis import categorize_transactions
from modules.db_functions import save_transactions, get_current_month_transactions, get_last_month_transactions
from modules.calculation import calculate_total_spending_amount
from models.data_preprocessing import data_cleaning
from models.data_visualization import pie_chart, stacked_barplot
from streamlit_extras.dataframe_explorer import dataframe_explorer 
import streamlit as st
import pandas as pd

def dashboard():
    config_page()
    st.title("Your Dashboard")
    
    # display current month spending
    curr_month_transactions = get_current_month_transactions()
    curr_month_net_spending = calculate_total_spending_amount(curr_month_transactions)
    str_curr_month_net_spending = str(curr_month_net_spending)
    last_month_transactions = get_last_month_transactions()
    last_month_net_spending = calculate_total_spending_amount(last_month_transactions)
    delta_in_transaction = 100 * (curr_month_net_spending - last_month_net_spending) / last_month_net_spending
    str_delta_in_transaction = str(round(delta_in_transaction, 2))
    st.metric(label="Current Month Net Spending Amount 💸", 
            value="＄" + str_curr_month_net_spending,
            delta=str_delta_in_transaction + ' % lower compared to last month',
            delta_color='inverse')

    col1, col2 = st.columns(2)

    with col1:
        current_month_pie_chart()

    with col2:
        past_month_stack_barplot()
        
    with st.spinner("Categorizing transactions..."):
        try:
            uploaded_df, bank, card = file_uploader(["csv"])
            df_clean = data_cleaning(uploaded_df, bank, card)
            df_categorized = categorize_transactions(df_clean.head(3))
            save_transactions(df_categorized, bank, card)
        except TypeError as err:
            st.warning("No file has been uploaded.", icon="⚠️")
        except PermissionError as err:
            st.stop("🚨Cannot save data")
        finally:
            st.spinner(text="Categorization complete.")

def current_month_pie_chart():
    curr_month_transactions = get_current_month_transactions()
    pie_chart(curr_month_transactions)

def past_month_stack_barplot():
    curr_month_transactions = get_current_month_transactions()
    past_month_transactions = get_last_month_transactions()
    stacked_barplot(curr_month_transactions, past_month_transactions)




if __name__ == "__main__":
    dashboard()
