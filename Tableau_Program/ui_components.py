# ui_components.py
import getpass
import os
import json
import tkinter as tk
import sqlite3
from tkinter import ttk
from datetime import datetime

# Global repo folder (optional to pass in)
REPO_FOLDER = "tableau_repository"
author = getpass.getuser()

# ---- REFRESH LOG HISTORY ----
def refresh_log_history(right_panel, author_filter=None, workbook_filter=None):
    for widget in right_panel.winfo_children():
        widget.destroy()

    tk.Label(right_panel, text="\U0001F4DC Change Log History", font=("Helvetica", 12, "bold"), bg="#f9f9f9").pack(anchor="nw")

    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "change_log.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs ORDER BY id DESC")
    logs = cursor.fetchall()
    conn.close()

    if not logs:
        tk.Label(right_panel, text="No logs yet.", fg="gray", bg="#f9f9f9").pack(anchor="nw", pady=10)
        return

    for entry in logs:
        # Unpack columns
        _, file_name, timestamp, author, ticket, department, impact, summary, datasource = entry

        text = f"""
Author: {author}
Workbook: {file_name}
Change Summary: {summary}
Datasource Changes: {datasource}
Ticket #: {ticket}
Department: {department}
Impact: {impact}
Timestamp: {timestamp}
-------------------------------------
"""
        label = tk.Label(right_panel, text=text, justify="left", anchor="w", bg="#f9f9f9", font=("Courier", 9))
        label.pack(anchor="nw", padx=5, pady=2)
# def refresh_log_history(right_panel, author_filter=None, workbook_filter=None):
#     for widget in right_panel.winfo_children():
#         widget.destroy()

#     tk.Label(right_panel, text="\U0001F4DC Change Log History", font=("Helvetica", 12, "bold"), bg="#f9f9f9").pack(anchor="nw")

#     log_path = os.path.join(REPO_FOLDER, "change_log.json")

#     # Apply filters
#     if author_filter:
#         logs = [log for log in logs if author_filter.lower() in log.get("author", "").lower()]

#     if workbook_filter:
#         logs = [log for log in logs if workbook_filter.lower() in log.get("file_name", "").lower()]


#     if not os.path.exists(log_path):
#         tk.Label(right_panel, text="No logs yet.", fg="gray", bg="#f9f9f9").pack(anchor="nw", pady=10)
#         return

#     try:
#         with open(log_path, "r") as f:
#             logs = json.load(f)
#     except json.JSONDecodeError:
#         tk.Label(right_panel, text="Error reading log file.", fg="red", bg="#f9f9f9").pack(anchor="nw", pady=10)
#         return

#     for entry in reversed(logs):
#         text = f"""
# Analyst: {entry.get('author', '[N/A]')}
# Workbook: {entry.get('file_name', '[N/A]')}
# Ticket: {entry.get('ticket_number','[N/A]')}
# Department Requesting Change: {entry.get('department','[N/A]')}
# Change Summary: {entry.get('change_summary', '[N/A]')}
# Timestamp: {entry.get('timestamp', '[N/A]')}
# -------------------------------------
# """
#         label = tk.Label(right_panel, text=text, justify="left", anchor="w", bg="#f9f9f9", font=("Courier", 9))
#         label.pack(anchor="nw", padx=5, pady=2)


# ---- LOAD CHANGE LOG FORM ----
def load_change_log_form(container, file_name, timestamp, refresh_callback):
    form = tk.Frame(container)
    form.grid(row=3, column=0, sticky="w", pady=(10, 0))

    # tk.Label(form, text="Author:").grid(row=0, column=0, sticky="e")
    # author_entry = tk.Entry(form)
    # author_entry.grid(row=0, column=1)

    tk.Label(form, text="Ticket #:").grid(row=0, column=0, sticky="e")
    ticket_entry = tk.Entry(form)
    ticket_entry.grid(row=0, column=1)

    # Team Selection, commented out due to only Analytics team having access to this program.
    # tk.Label(form, text="Team:").grid(row=1, column=0, sticky="e")
    # team_var = tk.StringVar()
    # team_entry = ttk.Combobox(form, textvariable=team_var)
    # team_entry['values'] = ["Analytics"]
    # team_entry.grid(row=2, column=1)

    tk.Label(form, text="Impact Level:").grid(row=1, column=0, sticky="e")
    impact_var = tk.StringVar()
    impact_dropdown = ttk.Combobox(form, textvariable=impact_var)
    impact_dropdown['values'] = ["Low", "Medium", "High"]
    impact_dropdown.grid(row=1, column=1)

    tk.Label(form, text="Department:").grid(row=3, column=0, sticky="e")
    department_var = tk.StringVar()
    department_dropdown = ttk.Combobox(form, textvariable=department_var)
    department_dropdown['values'] = ["Performance","Marketing","Client Services","Operations","Accounting","Salesforce","Software Support","Transitions","Investments","Experience","Other"]
    department_dropdown.grid(row=3, column=1)

    if department_dropdown == "Other":
        tk.Label(form, text="Department Name").grid(row=5,column=1, sticky="e")
        department_entry = tk.Entry(form)
        department_entry.grid(row=5, column=0)


    tk.Label(form, text="Change Summary:").grid(row=7, column=0, sticky="e")
    change_summary = tk.Text(form, height=5, width=30)
    change_summary.grid(row=7, column=1)

    # Datasource Changes Field
    tk.Label(form, text="Datasource Changes (Optional):").grid(row=8, column=0, sticky="e")
    datasource_changes = tk.Text(form, height=5, width=30)
    datasource_changes.grid(row=8, column=1)

    # def submit_form():
    #     log_entry = {
    #         "file_name": file_name,
    #         "timestamp": timestamp,
    #         "author": getpass.getuser().title(),
    #         "ticket_number": ticket_entry.get(),
    #         #"team": team_entry.get(),
    #         "department": department_dropdown.get(),
    #         "impact": impact_var.get(),
    #         "change_summary": change_summary.get("1.0", "end").strip()
    #     }

    #     log_path = os.path.join(REPO_FOLDER, "change_log.json")
    #     if os.path.exists(log_path):
    #         with open(log_path, "r") as f:
    #             try:
    #                 logs = json.load(f)
    #             except json.JSONDecodeError:
    #                 logs = []
    #     else:
    #         logs = []

    #     logs.append(log_entry)
    #     with open(log_path, "w") as f:
    #         json.dump(logs, f, indent=4)

    #     print("Log saved for", file_name)
    #     form.destroy()
    #     refresh_callback()

    def submit_form():
    # Prepare the log entry
        log_entry = (
            file_name,
            timestamp,
            getpass.getuser().title(),
            ticket_entry.get(),
            department_dropdown.get(),
            impact_var.get(),
            change_summary.get("1.0", "end").strip(),
            datasource_changes.get("1.0", "end").strip()  # new field!
        )

        # Connect to SQLite and insert the record
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "change_log.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO logs
            (file_name, timestamp, author, ticket_number, department, impact, change_summary, datasource_changes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', log_entry)

        conn.commit()
        conn.close()

        print("Log saved for", file_name)
        form.destroy()
        refresh_callback()

    submit_button = tk.Button(form, text="Submit", command=submit_form)
    submit_button.grid(row=9, column=1, pady=10)
