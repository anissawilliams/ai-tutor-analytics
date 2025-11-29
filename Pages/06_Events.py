import streamlit as st
import pandas as pd
import plotly.express as px
from utils.storage import load_events

st.title("📌 Events & System Actions")

df_events = load_events()
#df_events = pd.DataFrame([doc.to_dict() for doc in db.collection("events").stream()])
if df_events.empty:
    st.warning("No data available or quota exceeded.")
else:
    st.dataframe(df_events.head())
if not df_events.empty:
    df_events['timestamp'] = pd.to_datetime(df_events['timestamp'])

    # Filters
    min_date, max_date = df_events['timestamp'].min(), df_events['timestamp'].max()
    start_date, end_date = st.date_input("Select Date Range", [min_date, max_date])
    df_events = df_events[(df_events['timestamp'].dt.date >= start_date) &
                          (df_events['timestamp'].dt.date <= end_date)]

    event_types = df_events['event_type'].dropna().unique().tolist()
    selected_types = st.multiselect("Filter by Event Type", event_types, default=event_types)
    df_events = df_events[df_events['event_type'].isin(selected_types)]

    # Show filtered table
    st.dataframe(df_events[['timestamp','user_id','session_id','event_type','persona']].sort_values('timestamp', ascending=False))

    # Insights
    st.subheader("Events by Type")
    type_counts = df_events['event_type'].value_counts().reset_index()
    type_counts.columns = ['Event Type','Count']
    fig_type = px.bar(type_counts, x='Event Type', y='Count', title="Event Frequency by Type")
    st.plotly_chart(fig_type, use_container_width=True)

    if 'persona' in df_events.columns:
        st.subheader("Persona Selections")
        persona_counts = df_events['persona'].value_counts().reset_index()
        persona_counts.columns = ['Persona','Selections']
        fig_persona = px.bar(persona_counts, x='Persona', y='Selections', title="Persona Selection Counts")
        st.plotly_chart(fig_persona, use_container_width=True)

    st.subheader("Events Over Time")
    trend = df_events.groupby(df_events['timestamp'].dt.date).size().reset_index(name='Events')
    fig_trend = px.line(trend, x='timestamp', y='Events', title="Events per Day")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Top Users by Events")
    user_counts = df_events['user_id'].value_counts().reset_index()
    user_counts.columns = ['User ID','Events']
    fig_users = px.bar(user_counts.head(20), x='User ID', y='Events', title="Top 20 Users by Events")
    st.plotly_chart(fig_users, use_container_width=True)
else:
    st.info("No events recorded yet.")