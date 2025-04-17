# sqlite_setup.py
import sqlite3
import os

# Path to the database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "change_log.db")

# Connect to SQLite (creates file if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the logs table (if it doesn't already exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    author TEXT NOT NULL,
    ticket_number TEXT,
    department TEXT,
    impact TEXT,
    change_summary TEXT,
    datasource_changes TEXT
)
''')

conn.commit()
conn.close()

print("SQLite Database and logs table are ready!")
