import streamlit as st

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")

st.title("📊 AI Java Tutor Analytics")

st.write("""
Welcome to the Analytics Dashboard.  

Use the sidebar to navigate between pages:
- **Users** → Engagement & Retention
- **Learning Outcomes** → Performance metrics
- **Training Feedback** → AI tutor critique loop
- **Interactions** → Lesson transcripts and response trends
- **Clicks** → UI engagement patterns
- **Events** → System actions (persona selections, mode changes)
- **Sessions** → Session summaries and drill‑downs
""")