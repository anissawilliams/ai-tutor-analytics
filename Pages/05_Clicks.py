import streamlit as st
import pandas as pd
import plotly.express as px
from utils.storage import load_clicks

st.title("🖱️ Clicks & UI Engagement")

df_clicks = load_clicks()
#df_clicks = pd.DataFrame([doc.to_dict() for doc in db.collection("clicks").stream()])

if not df_clicks.empty:
    # Normalize field names if Firestore uses camelCase
    df_clicks.rename(columns={
        'timeStamp': 'timestamp',
        'elementName': 'element_name',
        'elementType': 'element_type',
        'userId': 'user_id'
    }, inplace=True)

    # Parse timestamp if present
    if 'timestamp' in df_clicks.columns:
        df_clicks['timestamp'] = pd.to_datetime(df_clicks['timestamp'], errors='coerce')
        df_clicks = df_clicks.sort_values('timestamp')

    # Only select columns that exist
    cols_to_show = [c for c in ['timestamp','element_name','element_type','user_id','session_id'] if c in df_clicks.columns]

    st.dataframe(df_clicks[cols_to_show])

    # --- Ensure timestamp is parsed if present ---
    if 'timestamp' in df_clicks.columns:
        df_clicks['timestamp'] = pd.to_datetime(df_clicks['timestamp'], errors='coerce')
        df_clicks = df_clicks.sort_values('timestamp')

    # --- Only show available columns ---
    cols_to_show = [c for c in ['timestamp','element_name','element_type','user_id','session_id'] if c in df_clicks.columns]
    st.dataframe(df_clicks[cols_to_show])

    # --- Insights ---
    st.subheader("Clicks per Element")
    if 'element_name' in df_clicks.columns:
        element_counts = df_clicks['element_name'].value_counts().reset_index()
        element_counts.columns = ['Element','Clicks']
        fig_elem = px.bar(element_counts, x='Element', y='Clicks', title="Most Clicked Elements")
        st.plotly_chart(fig_elem, use_container_width=True)

    st.subheader("Clicks per Element Type")
    if 'element_type' in df_clicks.columns:
        type_counts = df_clicks['element_type'].value_counts().reset_index()
        type_counts.columns = ['Type','Clicks']
        fig_type = px.pie(type_counts, values='Clicks', names='Type', hole=0.4, title="Clicks by Element Type")
        st.plotly_chart(fig_type, use_container_width=True)

    st.subheader("Clicks Over Time")
    if 'timestamp' in df_clicks.columns:
        clicks_trend = df_clicks.groupby(df_clicks['timestamp'].dt.date).size().reset_index(name='Clicks')
        fig_trend = px.line(clicks_trend, x='timestamp', y='Clicks', title="Clicks per Day")
        st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Top Users by Clicks")
    if 'user_id' in df_clicks.columns:
        user_counts = df_clicks['user_id'].value_counts().reset_index()
        user_counts.columns = ['User ID','Clicks']
        fig_users = px.bar(user_counts.head(20), x='User ID', y='Clicks', title="Top 20 Users by Clicks")
        st.plotly_chart(fig_users, use_container_width=True)
else:
    st.info("No clicks recorded yet.")