# ai_testing_agent
Milestone 1: Project Initialization and Baseline Agent Setup

This project implements the foundation for an AI-based system that will automatically test websites using natural language instructions.
Milestone 1 focuses on environment setup, project structure, and a baseline LangGraph agent.

Features (Milestone 1)
•	Set up Python environment and install dependencies (LangGraph, Playwright, Flask). 
•	Define project structure and initialize Flask server for static HTML test page. 
•	Implement baseline LangGraph agent configuration for handling user inputs. 

Technologies Used
Python 3.x
Flask – Web server
LangGraph – Agent workflow orchestration
Playwright – Installed for future automation

Installation
pip install flask
pip install langgraph
pip install playwright
playwright install

Project Structure
AI-Agent-Testing/
│
├── app/
│   ├── agents/
│   │   └── baseline_agent.py
│   ├── server.py
│
├── static/
│   └── index.html
│
├── run.py
├── testing.py

How to Run
Start Flask Server
python run.py
Open: http://127.0.0.1:5000

Test LangGraph Agent
python testing.py

Current Status:
✔ Flask server running
✔ Baseline agent working
✔ Project ready for next milestones
