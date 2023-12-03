import pandas as pd

def data_cleaning(df, bank, card):
    if bank == "BMO":
        if card == "Credit":
            return _data_cleaning_for_bmo_credit(df)
        else:
            return _data_cleaning_for_bmo_debit(df)
    else:
        return _data_cleaning_for_cibc_credit(df)

def _data_cleaning_for_bmo_debit(df):
    df = df.rename(columns={'Transaction Type': 'Transaction_Type', 
                            'Date Posted': 'Date', 
                            'Transaction Amount': 'Amount', 
                            'Description': 'Description'})
    # Convert 'Date' from integer to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    # Creating 'Spending' and 'Income' columns based on 'Transaction_Type'
    df['Spending'] = df['Transaction_Type'].apply(lambda x: 1 if x == 'DEBIT' else 0)
    df['Income'] = df['Transaction_Type'].apply(lambda x: 1 if x == 'CREDIT' else 0)
    # Reordering columns to match the requested format
    df = df[['Date', 'Description', 'Amount', 'Spending', 'Income']]
    return df

def _data_cleaning_for_bmo_credit(df):
    # Rename and select relevant columns
    df = df.rename(columns={'Transaction Date': 'Date', 
                            'Transaction Amount': 'Amount'})
    # Convert 'Date' from integer to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    # Creating 'Spending' and 'Income' columns based on 'Amount'
    df['Spending'] = df['Amount'].apply(lambda x: 1 if x > 0 else 0)
    df['Income'] = df['Amount'].apply(lambda x: 1 if x < 0 else 0)
    # Reordering columns to match the requested format
    df = df[['Date', 'Description', 'Amount', 'Spending', 'Income']]
    return df

def _data_cleaning_for_cibc_credit(df):
    df.columns = ['Date', 'Description', 'Spending', 'Income', 'Card']
    # Drop the 'Card' column
    df = df.drop(columns=['Card'])
    # Create a new 'Amount' column which takes the non-NaN value from either 'Spending' or 'Income'
    # If 'Spending' is not NaN, take its value; otherwise, take the negative of 'Income' value
    df['Amount'] = df['Spending'].fillna(0) - df['Income'].fillna(0)

    # Set 'Spending' to 1 if 'Amount' is positive, and 'Income' to 1 if 'Amount' is negative
    df['Spending'] = (df['Amount'] > 0).astype(int)
    df['Income'] = (df['Amount'] < 0).astype(int)

    # Select only the required columns
    df = df[['Date', 'Description', 'Amount', 'Spending', 'Income']]
    df['Amount'] = df['Amount'].apply(lambda x: abs(x))
    return df