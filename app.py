import streamlit as st
from ai_processor import generate_debrief
from database import create_table, save_report

create_table()

st.set_page_config(
    page_title="Field Visit Debrief Tool",
    layout="wide"
)

st.title("🌾 Field Visit Debrief Tool")
st.markdown("AI-powered field intelligence platform for program teams")

# Form Inputs
location = st.text_input("Location")

visit_date = st.date_input("Visit Date")

program_area = st.selectbox(
    "Program Area",
    [
        "Agriculture",
        "Women Empowerment",
        "Youth Skilling",
        "Livelihood"
    ]
)

stakeholders = st.text_input("Stakeholders Met")

notes = st.text_area(
    "Field Notes",
    height=200
)

# Generate Debrief
if st.button("Generate Debrief"):

    if not notes.strip():
        st.warning("Please enter field notes.")

    else:

        with st.spinner("Generating AI Debrief..."):

            st.session_state["debrief"] = generate_debrief(
                location,
                program_area,
                stakeholders,
                notes
            )

# Display Debrief
if "debrief" in st.session_state:

    st.subheader("📋 AI Debrief")
    st.markdown(st.session_state["debrief"])

    if st.button("💾 Save Report"):

        save_report(
            visit_date,
            location,
            program_area,
            stakeholders,
            notes,
            st.session_state["debrief"]
        )

        st.success("✅ Report Saved Successfully!")