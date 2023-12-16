import pandas as pd


def calculate_total_spending_amount(transaction_df):
    income_amount = transaction_df.loc[transaction_df['category'] == 'Income/Refund', 'amount'].sum()
    spending_amount = transaction_df.loc[transaction_df['category'] != 'Income/Refund', 'amount'].sum()
    net_amount = round(spending_amount - income_amount, 2)
    return net_amount