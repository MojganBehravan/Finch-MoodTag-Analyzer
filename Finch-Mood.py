# finch_dashboard.py
import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Finch Mood Tag Analyzer", layout="wide")
st.title("Finch Mood Tag Analyzer")
st.caption("Visualize mood trends and tagged days from your Finch export")

col1, col2, col3 = st.columns([2, 2, 2])

uploaded_file = col1.file_uploader("Upload Mood.json ", type="json")

if uploaded_file:
    # Load JSON safely
    try:
        raw = json.load(uploaded_file)
    except json.JSONDecodeError:
        col1.error("Could not read the file. Please upload a valid Mood.json file.")
        uploaded_file = None

    # Validate JSON structure
    if uploaded_file and "data" not in raw:
        col1.error("Invalid file. Please upload the Mood.json file from Finch.")
        uploaded_file = None

    # Convert to DataFrame and check required columns
    if uploaded_file:
        df = pd.DataFrame(raw["data"])
        required_cols = ["dt", "value", "mood_type", "mood_tag_ids"]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            col1.error("Please upload the Mood.json file. The required fields: " + ", ".join(missing)+" are missing")
            uploaded_file = None

    # Process data if valid
    if uploaded_file:
        df["dt"] = pd.to_datetime(df["dt"], errors="coerce")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df[df["mood_type"] == "feeling"]

        # Date range selection
        min_date, max_date = df["dt"].min().date(), df["dt"].max().date()
        date_range = col2.date_input("Date range", value=[min_date, max_date],
                                     min_value=min_date, max_value=max_date)
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        df = df[(df["dt"] >= start_date) & (df["dt"] <= end_date)]

        # Tags selection
        all_tags = sorted({tag for tags in df["mood_tag_ids"].dropna() if isinstance(tags, list) for tag in tags})
        selected_tags = col3.multiselect("Tags", options=all_tags)

        # Prepare plot
        df["date"] = df["dt"].dt.date
        daily_avg = df.groupby("date", as_index=False)["value"].mean()
        highlight_dates = df[df["mood_tag_ids"].apply(
            lambda x: isinstance(x, list) and any(tag in x for tag in selected_tags)
        )]["date"].unique()

        # Plot
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(daily_avg["date"], daily_avg["value"], marker="o", label="Baseline")
        ax.scatter(
            daily_avg.loc[daily_avg["date"].isin(highlight_dates), "date"],
            daily_avg.loc[daily_avg["date"].isin(highlight_dates), "value"],
            color="red", s=100, label="Selected tags"
        )
        ax.set_xlabel("Date")
        ax.set_ylabel("Average Feeling")
        ax.set_title("Daily Feeling Baseline")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

else:
    col1.info("Please upload a Finch JSON file to get started.")
