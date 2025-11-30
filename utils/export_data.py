import pandas as pd
from utils.storage import load_collection

# List of collections you want to export
collections = [
    "users",
    "sessions",
    "clicks",
    "events",
    "interactions",
    "learning_outcomes",
    "survey_responses",
    "ai_training_feedback"
]

for name in collections:
    df = load_collection(name)
    if not df.empty:
        filename = f"artifacts/{name}_{pd.Timestamp.today().date()}.csv"
        df.to_csv(filename, index=False)
        print(f"Exported {name} → {filename}")
    else:
        print(f"No data for {name}")