# Tableau_Program
 
## Objective: 
Create a version-controlled workflow with change logging for Tableau Workbooks.
## Scope of Work: 
Develop an internal application that serves as a repository and a “middleman” between Tableau Desktop and Tableau Server. The application will allow team members to log and document changes to Tableau workbooks and publish the workbook to the server using Tableau’s General Admin log-in. The tool is intended to formalize change logging, improve version control, provide a historical audit of workbook modifications, and future-proof issues caused by team departures breaking extract and workbook processes. 
## How this could work at a high level: 
1. Workbook Saved in Tableau Desktop
2. Custom Upload Tool
- Analyst launches program and selects the workbook. 
- The program uploads the workbook to a repository (file server, git repo, cloud storage). 
- Prompts the user to log/document changes. 
- Program saves metadata: username, date/time, version, changes. 
3. Workbook Published to Tableau Server
- Once documentation is complete, the program automatically publishes the workbook to Tableau Server using the Tableau REST API. 
4. Change Log maintained
- All logs are stored in a centralized database or file. (JSON, CSV, SQL DBs) for auditability.
## Phase 1: Planning the Core Workflow
**Select Tableau workbook file (.twb or .twbx).**
**Save a copy in a versioned repository (local folder or Git to start).**
**Prompt for change documentation (simple form or input prompt).**
**Log changes to a JSON or CSV file for now.**
**Publish to Tableau Server using Tableau's REST API.**
**Confirm success or handle errors.**
