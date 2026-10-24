import sqlite3
from datetime import datetime
import pandas as pd
import streamlit as st

DB_NAME = "smartmedi.db"

st.set_page_config(
    page_title="SmartMedi AI",
    page_icon="💊",
    layout="wide"
)
# CLEAN DARK BLUE AND TEAL THEME
st.markdown("""
<style>
    .stApp {
        background-color: #101827;
        color: #e5edf7;
    }

    h1, h2, h3 {
        color: #5eead4 !important;
        font-weight: 700;
    }

    p, label, [data-testid="stMarkdownContainer"] {
        color: #d6e1ef;
    }

    [data-testid="stMetric"] {
        background-color: #182438;
        border: 1px solid #2b3b52;
        padding: 16px;
        border-radius: 12px;
        box-shadow: none;
    }

    [data-testid="stMetricLabel"] {
        color: #9fb1c8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #5eead4 !important;
        font-weight: 700;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background-color: #0f766e;
        color: #ffffff;
        border: 1px solid #2dd4bf;
        border-radius: 8px;
        font-weight: 600;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background-color: #115e59;
        color: #ffffff;
        border: 1px solid #5eead4;
    }

    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {
        background-color: #182438;
        color: #f1f5f9;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #2b3b52;
        border-radius: 10px;
    }

    hr {
        border-color: #2b3b52;
    }
</style>
""", unsafe_allow_html=True)


# DATABASE SETUP
def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medication TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                notes TEXT DEFAULT ''
            )
        """)


def get_medications():
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT id, medication, reminder_time, notes
            FROM medications
            ORDER BY id
        """).fetchall()
        return [dict(row) for row in rows]


def add_medication(name, reminder_time, notes):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO medications
                (medication, reminder_time, notes)
            VALUES (?, ?, ?)
        """, (name, reminder_time, notes))


def update_medication(medication_id, name, reminder_time, notes):
    with get_connection() as conn:
        conn.execute("""
            UPDATE medications
            SET medication = ?, reminder_time = ?, notes = ?
            WHERE id = ?
        """, (name, reminder_time, notes, medication_id))


def delete_medication(medication_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM medications WHERE id = ?",
            (medication_id,)
        )


initialize_database()

st.title("💊 SmartMedi AI")
st.subheader("Your Smart Medication Reminder Dashboard")

st.info(
    "Organize reminders according to your "
    "healthcare professional's instructions."
)

# ADD REMINDER
st.header("➕ Add a Medication Reminder")

with st.form("add_form", clear_on_submit=True):
    name = st.text_input("Medication name")
    reminder_time = st.time_input("Reminder time")
    notes = st.text_input("Notes (optional)")

    submitted = st.form_submit_button("Save Reminder")

if submitted:
    if name.strip():
        add_medication(
            name.strip(),
            reminder_time.strftime("%I:%M %p"),
            notes.strip()
        )
        st.success("Reminder saved to database!")
        st.rerun()
    else:
        st.warning("Please enter a medication name.")

# LOAD SAVED DATA
medications = get_medications()

# DASHBOARD
st.header("📊 Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Reminders", len(medications))

with col2:
    unique_count = len({
        item["medication"].casefold()
        for item in medications
    })
    st.metric("Different Medicines", unique_count)

# SEARCH
st.header("🔎 Search Your Reminders")
search_text = st.text_input("Search by medication name")

filtered = [
    item for item in medications
    if search_text.strip().casefold()
    in item["medication"].casefold()
]

st.header("📋 Your Reminder List")

if filtered:
    display_data = [{
        "Medication": item["medication"],
        "Reminder Time": item["reminder_time"],
        "Notes": item["notes"]
    } for item in filtered]

    st.dataframe(
        pd.DataFrame(display_data),
        width="stretch"
    )
else:
    st.write("No matching reminders found.")

# EDIT AND DELETE
st.header("✏️ Edit or Delete a Reminder")

if medications:
    selected_id = st.selectbox(
        "Choose a reminder",
        options=[item["id"] for item in medications],
        format_func=lambda item_id: next(
            f"{item['medication']} — {item['reminder_time']}"
            for item in medications
            if item["id"] == item_id
        ),
        key="selected_reminder"
    )

    selected = next(
        item for item in medications
        if item["id"] == selected_id
    )

    edit_key = f"edit_name_{selected_id}"
    time_key = f"edit_time_{selected_id}"
    notes_key = f"edit_notes_{selected_id}"

    # Load current values when this reminder is selected
    if st.session_state.get("loaded_reminder_id") != selected_id:
        st.session_state[edit_key] = selected["medication"]
        st.session_state[time_key] = datetime.strptime(
            selected["reminder_time"], "%I:%M %p"
        ).time()
        st.session_state[notes_key] = selected["notes"]
        st.session_state["loaded_reminder_id"] = selected_id

    with st.form("edit_form"):
        edit_name = st.text_input(
            "Medication name", key=edit_key
        )
        edit_time = st.time_input(
            "Reminder time", key=time_key
        )
        edit_notes = st.text_input(
            "Notes", key=notes_key
        )

        save_changes = st.form_submit_button("Save Changes")

    if save_changes:
        if edit_name.strip():
            update_medication(
                selected_id,
                edit_name.strip(),
                edit_time.strftime("%I:%M %p"),
                edit_notes.strip()
            )
            st.success("Reminder updated!")
            st.rerun()
        else:
            st.warning("Medication name is required.")

    if st.button("🗑️ Delete Selected Reminder"):
        delete_medication(selected_id)
        st.session_state.pop("selected_reminder", None)
        st.session_state.pop("loaded_reminder_id", None)
        st.rerun()

else:
    st.write("Add a reminder to enable editing and deleting.")

st.caption(
    "Demo project only. SQLite stores reminder details locally. "
    "This app does not send notifications or provide medical advice."
)