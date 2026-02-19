
AI Agent to Test Websites Automatically Using Natural Language

This project is an AI-powered web testing platform that allows users to execute website tests using simple natural language instructions.

Instead of writing automation scripts manually, the system converts instructions into automated browser actions using AI agents and Playwright.

This project was developed as part of the Infosys Springboard Internship 6.0.

Project Overview

The system understands instructions such as:

Open google and search for laptops

The platform automatically:

Parses the instruction using an AI agent

Converts it into structured test actions

Generates a Playwright automation script

Executes the test in a real browser

Displays results, logs, and analytics in a dashboard

Features

Natural Language Test Execution
Rule-Based + LLM-Based Instruction Parser
LangGraph Workflow Integration
Automatic Playwright Script Generation
Real Browser Automation
Local Login Test Validation
Execution Logs and Debug Center
Test Reports Dashboard
Analytics Visualization
Failure Analysis System
Interactive Streamlit UI

Project Architecture

User Instruction
↓
AI Agent (LangGraph Router)
↓
Structured Actions
↓
Playwright Script Generator
↓
Automation Execution
↓
Logs, Reports, and Analytics

Project Structure
app
 ├── agents
 │   ├── baseline_agent.py
 │   ├── playwright_generator.py
 │   ├── playwright_executor.py
 │   └── report_generator.py
 │
 ├── server.py
 |──static
 │   └── test.html
 |──streamlit_app.py
 |──history.csv


Technologies Used
Python 3.x
Flask – Web server
LangGraph – Agent workflow orchestration
Playwright – Installed for future automation



Technologies Used
Python 3.x
Flask – Web server
LangGraph – Agent workflow orchestration
Playwright – Installed for future automation
Groq LLaMA Model
Streamlit
Pandas
Plotly

Installation:

Install dependencies
pip install -r requirements.txt


Install Playwright browsers
playwright install

Running the Application:
Run the Streamlit Dashboard
streamlit run streamlit_app.py


(Optional) Run the Flask API
python app/server.py


Example Test Instructions:

Open google and search for laptops

Open amazon and search for shoes

Open flipkart and search for mobiles

Open test page and verify login success

Local Test Page

A local login page is included to validate automation testing.

Dashboard Modules

Test Execution
Runs automation tests using natural language

Test Reports
Stores and displays test history

Analytics Dashboard
Shows test statistics and results

Execution Logs
Displays detailed execution logs and debugging information

Future Improvements:
Parallel Test Execution
AI-generated Test Cases
Screenshot Validation
Cloud-Based Test Execution
Advanced Failure Detection

Author
Sibani Sri Perni
