import openai
import streamlit as st
import time

def categorize_transactions(df_transaction):
    CATEGORY_OPTIONS = ["Shopping", "Restaurant", "Food Delivery", "Grocery", "Utilities", "Income/Refund", "Undefined"]
    openai.api_key = st.secrets["OPEN_AI_API_KEY"]
    df_transaction['Category'] = ''
    for index, row in df_transaction.iterrows():
        success = False
        while not success:
            try:
                prompt = (f"Based on the transaction details: Description: '{row['Description']}', "
                          f"Amount: {row['Amount']}, Income Indicator: {row['Income']}, what is the most likely category? Answer in only one word. "
                          f"Options: {CATEGORY_OPTIONS}.")

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "You are a helpful assistant."},
                              {"role": "user", "content": prompt}],
                    max_tokens=100
                )

                category = response['choices'][0]['message']['content'].strip()
                df_transaction.at[index, 'Category'] = category
                success = True  # Mark as success to exit the loop
                time.sleep(5)

            except Exception as e:
                print(f"Error processing row {index}: {e}. Retrying in 20 seconds...")
                time.sleep(20)

    return df_transaction
