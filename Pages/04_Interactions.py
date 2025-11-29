import streamlit as st
import pandas as pd
import plotly.express as px
from utils.storage import load_interactions

st.title("💬 Lesson Interactions")
df_interactions = load_interactions()
#df_interactions = pd.DataFrame([doc.to_dict() for doc in db.collection("interactions").stream()])

if not df_interactions.empty:
    df_interactions['timestamp'] = pd.to_datetime(df_interactions['timestamp'])

    # Filters
    min_date, max_date = df_interactions['timestamp'].min(), df_interactions['timestamp'].max()
    start_date, end_date = st.date_input("Select Date Range", [min_date, max_date])
    df_interactions = df_interactions[(df_interactions['timestamp'].dt.date >= start_date) &
                                      (df_interactions['timestamp'].dt.date <= end_date)]

    persona_options = df_interactions['persona'].dropna().unique().tolist()
    selected_persona = st.multiselect("Filter by Persona", persona_options, default=persona_options)
    df_interactions = df_interactions[df_interactions['persona'].isin(selected_persona)]

    # Show filtered table
    st.dataframe(df_interactions[['timestamp','session_id','persona','question','response_length']].sort_values('timestamp', ascending=False))

    # Insights
    st.subheader("Interactions per Persona")
    persona_counts = df_interactions['persona'].value_counts().reset_index()
    persona_counts.columns = ['Persona','Interactions']
    fig_persona = px.bar(persona_counts, x='Persona', y='Interactions', title="Interactions by Persona")
    st.plotly_chart(fig_persona, use_container_width=True)

    st.subheader("Response Length Trends")
    length_trend = df_interactions.groupby(df_interactions['timestamp'].dt.date)['response_length'].mean().reset_index()
    fig_len = px.line(length_trend, x='timestamp', y='response_length', title="Avg Response Length per Day")
    st.plotly_chart(fig_len, use_container_width=True)

    st.subheader("Session Activity")
    session_counts = df_interactions['session_id'].value_counts().reset_index()
    session_counts.columns = ['Session ID','Interactions']
    fig_sess = px.bar(session_counts.head(20), x='Session ID', y='Interactions', title="Top 20 Sessions by Interaction Count")
    st.plotly_chart(fig_sess, use_container_width=True)
else:
    st.info("No interactions recorded yet.")