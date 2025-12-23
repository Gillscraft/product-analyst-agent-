# product-analyst-agent-
Building a product analyst agent using python + LLMs

title: Agentic Workflow — Google Sheets Connector

summary: >
  This repo shows how to connect all the tools (Google sheets,openAI, Python Charts) are getting called 
  It’s a second last step toward building an Product Analyst Agent.
  You can copy the code, plug in your own Google Sheet and OpenAI API key, and run it locally.

files:

  intelligent_agent.py: >
    The main Python file.
    This is the file you run.
    It connects to Google Sheets, pulls data, connects to OpenAI, sends data and then calls chart builder file to build the charts recommended by the LLM and generates a graph

    
 sheets_connector.py: >
 file that connects to google sheets and pulls back data into python

Chart_builder.py:> 
contains all the logic and packages to build charts 

Openai_connector.py:> 
Logic that establishes a connection between OpenAI servers 




  requirements.txt: >
    A short list of Python packages required to run the code.
    Install these once before running the script.

  .env.example: >
    A template configuration file.
    Copy this file, rename it to .env, and paste in your own Google Sheet ID.
    This keeps configuration out of the code.


local_files_you_create:
  - .env:
      purpose: Stores your Google Sheet ID locally
      example OPEN_AI_KEY: add your open AI key ensure there's no space after = sign
      example: GOOGLE_SHEET_ID=your_sheet_id_here

setup:
  - Create a virtual environment:
      command: python3 -m venv venv && source venv/bin/activate

  - Install dependencies:
      command: pip install -r requirements.txt

run:
  command: python3 sheets_connector.py
  result: >
    Authenticates with Google Sheets,
    fetches the data,
    and prints a preview.

sheet id note: >
  Your Sheet ID comes from the Google Sheets URL:
  https://docs.google.com/spreadsheets/d/[THIS_IS_THE_ID]/edit


