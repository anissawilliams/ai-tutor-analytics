import streamlit as st
import pandas as pd
import plotly.express as px
from utils.storage import load_training_feedback
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("📝 AI Training Feedback")

df_feedback = load_training_feedback()
if not df_feedback.empty:
    df_feedback['timestamp'] = pd.to_datetime(df_feedback['timestamp'])

    # Filters
    min_date, max_date = df_feedback['timestamp'].min(), df_feedback['timestamp'].max()
    start_date, end_date = st.date_input("Select Feedback Date Range", [min_date, max_date])
    df_feedback = df_feedback[(df_feedback['timestamp'].dt.date >= start_date) &
                              (df_feedback['timestamp'].dt.date <= end_date)]

    persona_options = df_feedback['persona'].dropna().unique().tolist()
    selected_persona = st.multiselect("Filter by Persona", persona_options, default=persona_options)
    df_feedback = df_feedback[df_feedback['persona'].isin(selected_persona)]

    st.dataframe(df_feedback[['timestamp', 'persona', 'bad_response', 'critique']].sort_values('timestamp', ascending=False))

    # Insights
    critique_counts = df_feedback.groupby('persona')['critique'].count().reset_index()
    fig_c = px.bar(critique_counts, x='persona', y='critique', title="Number of Critiques by Persona")
    st.plotly_chart(fig_c, use_container_width=True)

    df_feedback['bad_length'] = df_feedback['bad_response'].apply(lambda x: len(x) if isinstance(x, str) else 0)
    length_trend = df_feedback.groupby(df_feedback['timestamp'].dt.date)['bad_length'].mean().reset_index()
    fig_l = px.line(length_trend, x='timestamp', y='bad_length', title="Avg Bad Response Length per Day")
    st.plotly_chart(fig_l, use_container_width=True)

    # Word Cloud
    st.subheader("Critique Themes Word Cloud")
    text = " ".join(df_feedback['critique'].dropna().tolist())
    if text.strip():
        wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate(text)
        fig_wc, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig_wc)
    else:
        st.info("No critiques available for word cloud.")
else:
    st.info("No training feedback recorded yet.")