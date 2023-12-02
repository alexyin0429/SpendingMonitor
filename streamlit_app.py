import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

st.header('Hello 🌎!')
if st.button('Balloons?'):
    st.balloons()

# Authenticate to Firestore with the JSON account key.
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="spending-monitor")
# Create a reference to the Google post.
doc_ref = db.collection("users").document("sCWJrAbRa3dUJgIwyZc8")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())