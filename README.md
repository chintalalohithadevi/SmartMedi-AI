# SmartMedi-AI
SmartMedi AI is a Python-based web application built with Streamlit that helps users organize medication reminders in one place. It uses SQLite to store reminder details locally, so saved entries remain available when the application is restarted.
## 📸 Dashboard Preview
![SmartMedi AI Dashboard](screenshots/SmartMedi%20AI%20Dashboard.png)
✨ Features

- Add Reminders: Save a medication name, reminder time, and optional notes.
- View Dashboard: See the total number of reminders and different medicine names.
- Search Reminders: Find entries by medication name.
- Edit Reminders: Update saved reminder details.
- Delete Reminders: Remove entries that are no longer needed.
- Persistent Storage: Store reminder data in a local SQLite database.
- Interactive Interface: Use a simple, user-friendly Streamlit dashboard.

🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Git and GitHub

📁 Project Structure

SmartMedi-AI/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md

The "smartmedi.db" database file is created locally when the application runs. The ".venv" virtual environment is also stored locally and is not required in the GitHub repository.

⚙️ Installation and Setup

Prerequisites

Install Python and Git on your computer.

1. Clone the repository

git clone https://github.com/chintalalohithadevi/SmartMedi-AI.git

2. Open the project folder

cd SmartMedi-AI

3. Create a virtual environment

python -m venv .venv

4. Activate the virtual environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

5. Install the required packages

python -m pip install -r requirements.txt

6. Run the application

python -m streamlit run app.py

Open the local URL displayed in your terminal to access the dashboard.

🗄️ Database

SmartMedi AI uses SQLite for local data storage.

- Reminder details are saved in the "smartmedi.db" file.
- Saved entries persist across application restarts when the same database file is used.
- The database is created locally and should not be committed to GitHub.

🎯 Project Objectives

- Simplify the organization of medication reminders.
- Practice Python application development.
- Understand database operations using SQLite.
- Build an interactive dashboard using Streamlit.
- Apply software development and GitHub version-control skills.

🚀 Future Enhancements

- Optional notification integration.
- Calendar-based reminder views.
- Improved dashboard analytics.
- Export and backup functionality.
- AI-assisted features, if added and tested in a future version.

👩‍💻 Author

Chintala Lohitha Devi

GitHub: "@chintalalohithadevi" (https://github.com/chintalalohithadevi)

⚠️ Important Note

This project is a learning and demonstration application for organizing reminder information. It does not currently send notifications, provide medical advice, or determine medication dosages. Follow instructions from a qualified healthcare professional for medication use.

---

⭐ If you find this project useful, feel free to explore the code and share feedback.