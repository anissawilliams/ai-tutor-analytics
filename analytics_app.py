import streamlit as st
from utils.storage import load_collection

st.set_page_config(page_title="AI Java Tutor Analytics", page_icon="📊", layout="wide")

st.title("📊 AI Java Tutor Analytics")

# Try loading data
df_users = load_collection("users")
df_sessions = load_collection("sessions")
df_clicks = load_collection("clicks")

# Metrics row with safety checks
col1, col2, col3 = st.columns(3)

if df_users.empty:
    col1.warning("No user data")
else:
    col1.metric("Users", len(df_users))

if df_sessions.empty:
    col2.warning("No session data")
else:
    col2.metric("Sessions", len(df_sessions))

if df_clicks.empty:
    col3.warning("No click data")
else:
    col3.metric("Clicks", len(df_clicks))

# Navigation grid
st.markdown("## Navigation")

colA, colB, colC = st.columns(3)

with colA:
    st.caption("Student feedback and training insights.")
    st.page_link("pages/08_Survey_Responses.py", label="Survey Responses")
    st.page_link("pages/01_Learning_Outcomes.py", label="Learning Outcomes")
    st.page_link("pages/03_Training_Feedback.py", label="Training Feedback")

with colB:
    st.caption("User activity and engagement.")
    st.page_link("pages/04_Interactions.py", label="Interactions")
    st.page_link("pages/05_Clicks.py", label="Clicks")
    st.page_link("pages/06_Events.py", label="Events")

with colC:
    st.caption("User profiles and session analytics.")
    st.page_link("pages/07_Sessions.py", label="Sessions")
    st.page_link("pages/01_Users.py", label="Users")
