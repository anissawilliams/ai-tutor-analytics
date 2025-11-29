import streamlit as st
import pandas as pd
import plotly.express as px
from utils.storage import load_users

st.title("🔥 Engagement & Retention")
df_users = load_users()
#df_users = pd.DataFrame([doc.to_dict() for doc in db.collection("users").stream()])

if not df_users.empty:
    # Persona filter
    if 'persona' in df_users.columns:
        persona_options = df_users['persona'].dropna().unique().tolist()
        selected_persona = st.selectbox("Filter by Persona", ["All"] + persona_options)
        if selected_persona != "All":
            df_users = df_users[df_users['persona'] == selected_persona]

    st.dataframe(df_users)

    # Insights
    total_students = len(df_users)
    returning_students = df_users[df_users['streak'] > 1].shape[0]
    retention_rate = (returning_students / total_students) * 100 if total_students > 0 else 0
    st.metric("Retention Rate", f"{retention_rate:.1f}%")

    if 'proficiency' in df_users.columns:
        df_users['proficiency'] = df_users['proficiency'].fillna('Beginner')
        prof_counts = df_users['proficiency'].value_counts().reset_index()
        prof_counts.columns = ['Level', 'Count']
        fig_prof = px.pie(prof_counts, values='Count', names='Level', hole=0.4)
        st.plotly_chart(fig_prof, use_container_width=True)
else:
    st.info("No user data yet.")