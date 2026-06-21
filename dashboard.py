import streamlit as st
import pandas as pd
import sqlite3
from ai_processor import generate_action_items

st.set_page_config(
    page_title="Field Intelligence Dashboard",
    layout="wide"
)

st.title("📊 Field Intelligence Dashboard")
st.caption("AI-powered insights for program managers")

# Load Data
conn = sqlite3.connect("reports.db")

df = pd.read_sql(
    "SELECT * FROM reports",
    conn
)

conn.close()

if len(df) == 0:
    st.warning("No reports found.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")

selected_location = st.sidebar.selectbox(
    "Location",
    ["All"] + sorted(df["location"].unique())
)

selected_program = st.sidebar.selectbox(
    "Program",
    ["All"] + sorted(df["program_area"].unique())
)

search_term = st.sidebar.text_input(
    "Search Reports"
)

filtered_df = df.copy()

if selected_location != "All":
    filtered_df = filtered_df[
        filtered_df["location"] == selected_location
    ]

if selected_program != "All":
    filtered_df = filtered_df[
        filtered_df["program_area"] == selected_program
    ]

if search_term:
    filtered_df = filtered_df[
        filtered_df["debrief"].str.contains(
            search_term,
            case=False,
            na=False
        )
    ]

if len(filtered_df) == 0:
    st.warning("No reports match the selected filters.")
    st.stop()

# Metrics
most_active_location = (
    filtered_df["location"]
    .value_counts()
    .idxmax()
)

most_common_program = (
    filtered_df["program_area"]
    .value_counts()
    .idxmax()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Visits",
    len(filtered_df)
)

col2.metric(
    "Locations Covered",
    filtered_df["location"].nunique()
)

col3.metric(
    "Most Active Location",
    most_active_location
)

col4.metric(
    "Top Program",
    most_common_program
)

st.divider()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Program Distribution")

    st.bar_chart(
        filtered_df["program_area"].value_counts()
    )

with right:
    st.subheader("Location Coverage")

    st.bar_chart(
        filtered_df["location"].value_counts()
    )

st.divider()

# AI Recommendations
st.subheader("🎯 Recommended Actions")

if st.button("Generate Action Items"):

    all_reports = "\n\n".join(
        filtered_df["debrief"].tolist()
    )

    actions = generate_action_items(
        all_reports
    )

    st.success("Recommendations Generated")
    st.write(actions)

st.divider()

# Report Explorer
st.subheader("📁 Field Reports")

for _, row in filtered_df.iterrows():

    with st.expander(
        f"{row['location']} | {row['program_area']} | {row['date']}"
    ):

        st.markdown(
            f"**Stakeholders:** {row['stakeholders']}"
        )

        st.markdown("### AI Debrief")

        st.write(
            row["debrief"]
        )