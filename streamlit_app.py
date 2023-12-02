import streamlit as st
from google.cloud import firestore

st.header('Hello 🌎!')
if st.button('Balloons?'):
    st.balloons()

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("spending-monitor-aded2-firebase-adminsdk-p52z8-3e21e9992f.json")

# Create a reference to the Google post.
doc_ref = db.collection("users").document("sCWJrAbRa3dUJgIwyZc8")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())