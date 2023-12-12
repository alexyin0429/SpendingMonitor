from google.cloud import firestore
from google.oauth2 import service_account
from firebase_admin import auth, credentials
from modules.apis import categorize_transactions
from datetime import datetime, timedelta
import requests
import streamlit as st
import pandas as pd
import firebase_admin
import json
import calendar

def auth_to_firestore():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="spending-monitor-aded2")
    return db

def initialize_firebase_admin():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firestore-key.json")
        firebase_admin.initialize_app(cred)

def user_signup(email, password):
    initialize_firebase_admin()
    db = auth_to_firestore()
    try:
        # Create a new user with email and password
        user = auth.create_user(email=email, password=password)
        uid = user.uid
        user_email = user.email
        user_ref = db.collection('users').document(uid)
        user_ref.set({
            'email': user_email
        })
        return user, None
    except auth.EmailAlreadyExistsError as e:
        return None, e
    
def sign_in_with_email_and_password(email, password, return_secure_token=True):
    payload = json.dumps({"email":email, "password":password, "return_secure_token":return_secure_token})
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    r = requests.post(rest_api_url,
                    params={"key": st.secrets["FIREBASE_WEB_API_KEY"]},
                    data=payload)
    return r.json()

def user_login(email, password):
    user = sign_in_with_email_and_password(email, password)
    if 'error' in user:
        raise ValueError(user['error']['message'])
    return user

def save_transactions(input_df, bank, card):
    if 'user_id' not in st.session_state:
        raise PermissionError(f"Cannot Save Data")
    else:
        db = auth_to_firestore()
        user_id = st.session_state.user_id
        user_ref = db.collection('users').document(user_id)
        transaction_ref = user_ref.collection('transactions')
        for i, row in input_df.iterrows():
            date_timestamp = datetime.strptime(row['Date'], '%Y-%m-%d')
            transaction_ref = user_ref.collection('transactions')
            transaction_data = {
                'date': date_timestamp,
                'description': row['Description'],
                'amount': row['Amount'],
                'category': row['Category'],
                'bank': bank,
                'card_type': card
            }
            transaction_ref.add(transaction_data)
        
    return None

def get_all_transactions():
    try:
        user_id = st.session_state.user_id
        db = auth_to_firestore()
        user_ref = db.collection("users").document(user_id)
        transactions = user_ref.collection("transactions").get()
        transactions_data = [transaction.to_dict() for transaction in transactions]
        return transactions_data
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")

def get_current_month_transactions():
    user_id = st.session_state.user_id
    db = auth_to_firestore()
    try:
        # Get the first and last day of the current month
        today = datetime.now()
        first_day = today.replace(day=1)
        fs_first_day = datetime.combine(first_day, datetime.min.time())
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        fs_last_day = datetime.combine(last_day, datetime.min.time())
        
        # Build a reference to the user's document in the users collection
        user_doc_ref = db.collection('users').document(user_id)

        # Query transactions in the current month
        transactions_ref = user_doc_ref.collection('transactions')
        query = transactions_ref.where('date', '>=', fs_first_day).where('date', '<=', fs_last_day).get()

        # Convert query results to a DataFrame
        transactions_data = [{'date': doc.get('date'), 'category': doc.get('category'), 'amount': doc.get('amount')} for doc in query]
        df = pd.DataFrame(transactions_data)

        return df
    except Exception as e:
        st.error(f"Error fetching data from the database: {e}")
        return None
    
def get_last_month_transactions():
    user_id = st.session_state.user_id
    db = auth_to_firestore()
    try:
        # Get the first and last day of the current month
        today = datetime.now()
        last_month_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_month_end = today.replace(day=1) - timedelta(days=1)
        fs_first_day_last_month = datetime.combine(last_month_start, datetime.min.time())
        fs_last_day_last_month = datetime.combine(last_month_end, datetime.min.time())
        
        # Build a reference to the user's document in the users collection
        user_doc_ref = db.collection('users').document(user_id)

        # Query transactions in the current month
        transactions_ref = user_doc_ref.collection('transactions')
        query = transactions_ref.where('date', '>=', fs_first_day_last_month).where('date', '<=', fs_last_day_last_month).get()

        # Convert query results to a DataFrame
        transactions_data = [{'date': doc.get('date'), 'category': doc.get('category'), 'amount': doc.get('amount')} for doc in query]
        df = pd.DataFrame(transactions_data)

        return df
    except Exception as e:
        st.error(f"Error fetching data from the database: {e}")
        return None