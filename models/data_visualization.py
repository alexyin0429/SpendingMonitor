import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def pie_chart(input_df):
    if input_df is not None and not input_df.empty:
        fig, ax = plt.subplots(figsize=(2,2))
        input_df['category'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax, textprops={'fontsize': 5})
        ax.set_aspect('equal')
        ax.set_ylabel('', fontsize=1)
        ax.set_title("This Month's Spending by Category", fontsize=5)
        st.pyplot(fig)
    else:
        st.warning("No data available for the current month.")

def stacked_barplot(curr_month_df, last_month_df):
    if curr_month_df is not None and last_month_df is not None:
        this_month_agg = curr_month_df.groupby('category')['amount'].sum()
        last_month_agg = last_month_df.groupby('category')['amount'].sum()

        df_combined = pd.DataFrame({
            'This Month': this_month_agg,
            'Last Month': last_month_agg
        }).fillna(0)

        fig, ax = plt.subplots(figsize=(8, 6))
        df_combined.plot(kind='bar', stacked=True, ax=ax, colormap='Set3')

        ax.set_title('This Month vs. Last Month by Category')
        ax.set_xlabel('Category')
        ax.set_ylabel('Total Amount')
        ax.legend(title='Time Period', bbox_to_anchor=(1, 1))

        st.pyplot(fig)
    else:
        st.warning("No data available for the current/past month.")