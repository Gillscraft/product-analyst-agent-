# product-analyst-agent-
Building a product analyst agent using python + LLMs

 title: "Agentic Workflow — Google Sheets Connector"
 title: "Agentic Workflow — Google Sheets Connector"

  summary: >
    This repo shows how to connect to Google Sheets using Python.
    It’s a foundational step toward building a Product Analyst Agent.
    Copy the files below, plug in your own Google Sheet + credentials, and run locally.

  files_and_what_they_do:
    sheets_connector.py: >
      The main code you run.
      It authenticates, pulls data from your Google Sheet, and prints a preview.

    requirements.txt: >
      The dependency list.
      Install these packages once so the Python script can run.

    .env.example: >
      A safe template (meant to be copied).
      Users copy this file to create their own .env and paste their Sheet ID there.
      This keeps configuration out of the code.

    .gitignore: >
      Safety file.
      Prevents local/private files (like .env and credentials.json) from being uploaded to GitHub.

  what_users_need_to_create_locally:
    - file: ".env"
      how: "Copy .env.example → rename to .env → set GOOGLE_SHEET_ID"
      example: "GOOGLE_SHEET_ID=your_sheet_id_here"
    - file: "credentials.json"
      how: "Add your own Google service account credentials file (never upload this)"

  setup_steps:
    - description: "Create and activate a clean Python environment"
      command: "python3 -m venv venv && source venv/bin/activate"

    - description: "Install required packages"
      command: "pip install -r requirements.txt"

  run:
    command: "python3 sheets_connector.py"
    result: >
      The script authenticates with Google Sheets, fetches your worksheet data,
      and prints a preview.

  note_on_sheet_id: >
    Your Sheet ID comes from the URL:
    https://docs.google.com/spreadsheets/d/[THIS_IS_THE_ID]/edit

  next_steps:
    - Add analysis and charts
    - Add insight summaries
    - Build toward an agentic workflow
