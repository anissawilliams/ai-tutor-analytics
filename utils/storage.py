import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# ---------------------------------------------------------
# 1. Initialize Firebase Admin once, using st.secrets
# ---------------------------------------------------------
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate({
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        })
        firebase_admin.initialize_app(cred)
    return firestore.client()

# ---------------------------------------------------------
# 2. Generic loader with caching
# ---------------------------------------------------------
@st.cache_data(ttl=300)
def load_collection(name: str, rename_map: dict = None):
    db = init_firebase()
    docs = db.collection(name).stream()
    df = pd.DataFrame([doc.to_dict() for doc in docs])

    if rename_map:
        df.rename(columns=rename_map, inplace=True)

    return df

# ---------------------------------------------------------
# 3. Specific loaders
# ---------------------------------------------------------
def load_clicks():
    return load_collection("clicks", {
        "timeStamp": "timestamp",
        "elementName": "element_name",
        "elementType": "element_type",
        "userId": "user_id"
    })

def load_events():
    return load_collection("events", {
        "timeStamp": "timestamp",
        "eventType": "event_type",
        "userId": "user_id"
    })

def load_sessions():
    return load_collection("sessions", {
        "startTime": "start_time",
        "userId": "user_id"
    })

def load_interactions():
    return load_collection("interactions", {
        "timeStamp": "timestamp",
        "userId": "user_id",
        "persona": "persona",
        "question": "question",
        "responseLength": "response_length"
    })

def load_users():
    return load_collection("users")

def load_learning_outcomes():
    return load_collection("learning_outcomes")

def load_survey_responses():
    return load_collection("survey_responses")

def load_training_feedback():
    return load_collection("ai_training_feedback")