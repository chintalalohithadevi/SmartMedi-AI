import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SmartMedi AI",
    page_icon="💊",
    layout="wide"
)

st.title("💊 SmartMedi AI")
st.subheader("Your Smart Medication Reminder Dashboard")

st.info(
    "This app helps you organize reminders based "
    "on your prescribed schedule."
)

st.header("➕ Add a Medication Reminder")

with st.form("medication_form"):
    medicine_name = st.text_input("Medication name")
    reminder_time = st.time_input("Reminder time")
    notes = st.text_input("Notes (optional)")

    submitted = st.form_submit_button("Save Reminder")

if "medications" not in st.session_state:
    st.session_state.medications = []

if submitted:
    if medicine_name.strip():
        st.session_state.medications.append({
            "Medication": medicine_name.strip(),
            "Reminder Time": reminder_time.strftime("%I:%M %p"),
            "Notes": notes.strip()
        })
        st.success("Reminder added successfully!")
    else:
        st.warning("Please enter a medication name.")

st.header("📋 Your Reminder List")

if st.session_state.medications:
    df = pd.DataFrame(st.session_state.medications)
    st.dataframe(df, use_container_width=True)
else:
    st.write("No reminders added yet. Add one above.")

st.caption(
    "Demo project: follow your healthcare professional's "
    "instructions. This app does not provide medical advice."
)