import streamlit as st
import pandas as pd
import plotly.express as px
from utils.storage import load_survey_responses

st.title("📋Survey Responses")

df_responses = load_survey_responses()
if df_responses.empty:
    st.warning("No data available or quota exceeded.")


if not df_responses.empty:
    st.dataframe(df_responses)


