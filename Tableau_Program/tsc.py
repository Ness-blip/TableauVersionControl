# TSC.py
import tableauserverclient as TSC

# ----------------- Config -----------------
SERVER_URL = "" # Enter Server URL here
SITE_ID = ""   # Empty string if you're using the Default site
TOKEN_NAME = "" # Enter token name here
TOKEN_SECRET = "" # Insert Token here
# ------------------------------------------

def authenticate():
    tableau_auth = TSC.PersonalAccessTokenAuth(TOKEN_NAME, TOKEN_SECRET, SITE_ID)
    server = TSC.Server(SERVER_URL, use_server_version=True)
    return server, tableau_auth

def get_available_projects():
    server, tableau_auth = authenticate()
    with server.auth.sign_in(tableau_auth):
        all_projects, _ = server.projects.get()
        return [p.name for p in all_projects]

def publish_to_tableau(file_path, project_name="Default"):
    """Publishes a workbook to Tableau Server."""
    server, tableau_auth = authenticate()
    try:
        with server.auth.sign_in(tableau_auth):
            print("Signed into Tableau")

            # Get project by name
            all_projects, _ = server.projects.get()
            project = next((p for p in all_projects if p.name == project_name), None)

            if not project:
                print(f"Project '{project_name}' not found.")
                return

            # Publish workbook
            new_workbook = TSC.WorkbookItem(project_id=project.id)
            new_workbook = server.workbooks.publish(new_workbook, file_path, mode=TSC.Server.PublishMode.Overwrite)

            print(f"Workbook '{new_workbook.name}' successfully published to project '{project_name}'.")

    except Exception as e:
        print(f"Publish failed: {e}")
