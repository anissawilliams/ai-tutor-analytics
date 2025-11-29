import streamlit as st
import pandas as pd
import plotly.express as px
from utils.storage import load_learning_outcomes

st.title("🧠 Learning Performance")

df_outcomes = load_learning_outcomes()
if df_outcomes.empty:
    st.warning("No data available or quota exceeded.")

#df_outcomes = pd.DataFrame([doc.to_dict() for doc in db.collection("learning_outcomes").stream()])

if not df_outcomes.empty:
    df_outcomes['timestamp'] = pd.to_datetime(df_outcomes['timestamp'])

    # Filters
    min_date, max_date = df_outcomes['timestamp'].min(), df_outcomes['timestamp'].max()
    start_date, end_date = st.date_input("Select Date Range", [min_date, max_date])
    df_outcomes = df_outcomes[(df_outcomes['timestamp'].dt.date >= start_date) &
                              (df_outcomes['timestamp'].dt.date <= end_date)]

    persona_options = df_outcomes['persona'].dropna().unique().tolist()
    selected_persona = st.multiselect("Filter by Persona", persona_options, default=persona_options)
    df_outcomes = df_outcomes[df_outcomes['persona'].isin(selected_persona)]

    st.dataframe(df_outcomes)

    # Insights
    success_rate = df_outcomes['is_correct'].mean() * 100
    st.metric("Global Success Rate", f"{success_rate:.1f}%")

    persona_perf = df_outcomes.groupby('persona')['is_correct'].mean().reset_index()
    persona_perf['is_correct'] *= 100
    fig_p = px.bar(persona_perf, x='persona', y='is_correct', range_y=[0, 100])
    st.plotly_chart(fig_p, use_container_width=True)
else:
    st.info("No learning outcomes recorded yet.")