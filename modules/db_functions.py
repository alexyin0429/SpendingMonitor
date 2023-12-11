from google.cloud import firestore
from google.oauth2 import service_account
from firebase_admin import auth, credentials
import requests
import streamlit as st
import firebase_admin
import json

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
    try:
        # Create a new user with email and password
        user = auth.create_user(email=email, password=password)
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
    # Sign in the user with email and password
    user = sign_in_with_email_and_password(email, password)
    if 'error' in user:
        raise ValueError(user['error']['message'])
    return user

def save_transactions():
    return None

def get_all_transactions(user_id):
    try:
        db = auth_to_firestore()
        user_ref = db.collection("users").document(user_id)
        transactions = user_ref.collection("transactions").get()
        # convert the data snapshot to dict
        transactions_data = [transaction.to_dict() for transaction in transactions]
        return transactions_data
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")