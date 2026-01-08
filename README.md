## About Finch Care

**[Finch Care](https://finchcare.com/)** (also known simply as *Finch: Self‑Care Pet*) is a self‑care and mental wellness app that blends mood tracking, habit building, journaling, and guided self‑care activities with a fun virtual pet companion. Every small self‑care task you log (like mood check‑ins, journaling, breathing exercises, or simple goals) helps take care of your Finch pet and rewards you with progress and insights. The app uses gamification to make daily self‑reflection and positive routines feel more engaging and less like chores, so people can build healthy habits over time. Finch is meant to support general wellbeing, not replace professional mental health care. 

# Finch Mood Tag Analyzer

Visualize your Finch Care mood data with tag‑based highlights. This Streamlit app allows you to upload your `Mood.json` from Finch, select a date range, and highlight specific mood tags to track trends over time.

## Features

- Upload Finch Care exported `Mood.json` file
- Select date range to analyze
- Highlight one or multiple tags
- Interactive plot showing daily average mood and tag‑specific points
- Clean, one‑line UI layout for file upload, date range, and tags

## How to Use

1. Export your mood data from Finch Care: Settings → Your Data → Advanced Management → Export Data (only `Mood.json` is needed)
2. Clone this repository or download the `finch_dashboard.py` file.
3. Install dependencies:

```bash
pip install streamlit pandas matplotlib
