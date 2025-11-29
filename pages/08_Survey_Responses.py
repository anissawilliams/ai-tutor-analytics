import streamlit as st
import pandas as pd
import plotly.express as px
from utils.storage import load_survey_responses

st.title(" Survey Responses")

df_responses = load_survey_responses()
st.dataframe(df_responses)

