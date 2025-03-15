import pandas as pd

def data_cleaning(df, bank, card):
    if bank == "BMO":
        if card == "Credit Card":
            return _data_cleaning_for_bmo_credit(df)
        else:
            return _data_cleaning_for_bmo_debit(df)
    else:
        if card == "Credit Card":
            return _data_cleaning_for_cibc_credit(df)
        else:
            return _data_cleaning_for_cibc_debit(df)

def _data_cleaning_for_bmo_debit(df):
    transaction_amount_column = ' Transaction Amount'
    df['Spending'] = 0.0
    df['Income'] = 0.0
    df.loc[df['Transaction Type'] == 'DEBIT', 'Spending'] = -df[transaction_amount_column]
    df.loc[df['Transaction Type'] == 'CREDIT', 'Income'] = df[transaction_amount_column]
    df = df.rename(columns={'Transaction Type': 'Transaction_Type', 
                            'Date Posted': 'Date', 
                            ' Transaction Amount': 'Amount', 
                            'Description': 'Description'})
    # Convert 'Date' from integer to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    # Reordering columns to match the requested format
    df = df[['Date', 'Description', 'Spending', 'Income']]
    return df

def _data_cleaning_for_bmo_credit(df):
    # Rename and select relevant columns
    df = df.rename(columns={'Transaction Date': 'Date', 
                            'Transaction Amount': 'Amount'})
    # Convert 'Date' from integer to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    # Creating 'Spending' and 'Income' columns based on 'Amount'
    df['Spending'] = df['Amount'].apply(lambda x: x if x > 0 else 0)
    df['Income'] = df['Amount'].apply(lambda x: -x if x < 0 else 0)
    # Reordering columns to match the requested format
    df = df[['Date', 'Description', 'Spending', 'Income']]
    return df

def _data_cleaning_for_cibc_credit(df):
    df.columns = ['Date', 'Description', 'Spending', 'Income', 'Card']
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    # Drop the 'Card' column
    df = df.drop(columns=['Card'])

    # Select only the required columns
    df = df[['Date', 'Description', 'Spending', 'Income']]
    return df

def _data_cleaning_for_cibc_debit(df):
    df.columns = ['Date', 'Description', 'Spending', 'Income']
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    return df