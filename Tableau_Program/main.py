# main.py
import os
import shutil
import tkinter as tk
import getpass
import json
##import tsc
from tkinter import filedialog, ttk
from datetime import datetime
from ui_components import load_change_log_form, refresh_log_history

CONFIG_FILE = "config.json"

# Load or Set Up Directory
if os.path.exists(CONFIG_FILE): 
    with open(CONFIG_FILE,'r') as f: 
        config = json.load(f)
    BASE_DIR = config.get("base_directory","")
    if not os.path.isdir(BASE_DIR):
        BASE_DIR = filedialog.askdirectory(title="Select Repository Folder")
else:
    BASE_DIR = filedialog.askdirectory(title= "Select Repository Folder")
    config = {"base_directory": BASE_DIR}
    with open(CONFIG_FILE,"w") as f: 
        json.dump(config,f, indent=4)

repo_folder = os.path.join(BASE_DIR, "tableau_repository")
db_path = os.path.join(BASE_DIR, "change_log.db")

# --- Setup window ---
root = tk.Tk()
root.title("Tableau Workbook Logger")
root.geometry("900x500")


repo_folder = "tableau_repository"
os.makedirs(repo_folder, exist_ok=True)

# ---- RIGHT PANEL WITH SCROLLING ----
right_panel_outer = tk.Frame(root, bg="#f9f9f9", bd=1, relief="sunken")
right_panel_outer.grid(row=0, column=1, sticky="nsew")

history_canvas = tk.Canvas(right_panel_outer, bg="#f9f9f9", highlightthickness=0)
history_canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(right_panel_outer, orient="vertical", command=history_canvas.yview)
scrollbar.pack(side="right", fill="y")

history_canvas.configure(yscrollcommand=scrollbar.set)

right_panel = tk.Frame(history_canvas, bg="#f9f9f9")
history_canvas.create_window((0, 0), window=right_panel, anchor="nw")

# Auto-adjust canvas scroll region
def on_frame_configure(event):
    history_canvas.configure(scrollregion=history_canvas.bbox("all"))
right_panel.bind("<Configure>", on_frame_configure)

# filter_frame = tk.Frame(right_panel_outer, bg="#f9f9f9")
# filter_frame.pack(anchor="nw", padx=5, pady=(5,10))

# tk.Label(filter_frame, text="Author:", bg="#f9f9f9").grid(row=0, column=2, sticky="e")
# author_filter = tk.Entry(filter_frame)
# author_filter.grid(row=0, column=3, padx=5)

# tk.Label(filter_frame, text="Workbook:", bg="#f9f9f9").grid(row=1, column=2, sticky="e")
# workbook_filter = tk.Entry(filter_frame)
# workbook_filter.grid(row=0, column=3, padx=5)

# def apply_filters():
#     refresh_log_history(
#         right_panel,
#         author_filter.get().strip(),
#         workbook_filter.get().strip()
#     )

# tk.Button(filter_frame, text="Filter",command=apply_filters).grid(row=2, column=0, columnspan=2, padx=5)

# ---- LEFT PANEL ----
left_panel = tk.Frame(root, padx=20, pady=20)
left_panel.grid(row=0, column=0, sticky="nsew")

# Upload button logic
def handle_upload():
    file_path = filedialog.askopenfilename(
        title="Select Tableau Workbook",
        filetypes=[("Tableau Files", "*.twb *.twbx")]
    )

    if not file_path:
        return

    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_file_name = f"{name}_{timestamp}{ext}"
    new_file_path = os.path.join(repo_folder, new_file_name)

    shutil.copy2(file_path, new_file_path)
    print(f"Copied {new_file_name} to {new_file_path}")

    # Load the form into left panel
    load_change_log_form(left_panel, new_file_name, timestamp, lambda: refresh_log_history(
        right_panel,
        ))

    print("Logged in as:", getpass.getuser() )
# Upload button
upload_btn = tk.Button(left_panel, text="Upload Workbook", width=25, height=2, command=handle_upload)
upload_btn.grid(row=0, column=0, pady=(0, 20))

# Form section label
form_label = tk.Label(left_panel, text="Change Log Form", font=("Helvetica", 12, "bold"))
form_label.grid(row=1, column=0, sticky="w")

# Placeholder
form_placeholder = tk.Label(left_panel, text="[Form will go here]", fg="gray")
form_placeholder.grid(row=2, column=0, sticky="w")

# Resizing behavior
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.rowconfigure(0, weight=1)

# Load history on startup
refresh_log_history(right_panel)

# Run the app
root.mainloop()
