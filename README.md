# Milestone 3 – Visible AI Web Test Agent (Python)

## Project Title
**AI Web Test Agent – Natural Language Driven Visible Browser Automation**
---
## Overview
This project implements an **AI-powered web test automation system** that converts
**natural language instructions** into **visible Playwright browser actions** using **Python only**.
Users can visually observe browser actions such as:
- Opening websites
- Typing into inputs
- Clicking buttons
- Searching on Google, YouTube, Amazon
- Logging into local HTML pages
---
## Milestone 3 Objective
The goal of **Milestone 3** was to achieve:
- Fully **visible browser automation**
- End-to-end flow:
  **Instruction → Parsing → Code Generation → Execution**
- Robust handling of real websites
- Clear execution feedback for users
---
## Key Features
### Natural Language Test Instructions
Users can write instructions like:
-open browser go to amazon and search for wireless mouse
-etc

The system automatically converts them into Playwright test steps.
---
### Stateful AI Test Agent
- Built using **LangGraph**
- Tracks:
  - Browser open/close state
  - Current URL
  - Execution status
- Controls full test lifecycle
---
### Python-Only Playwright Execution
- No Node.js required
- Uses **Playwright Python**
- Chromium runs in:
  - `headless=False`
  - `slow_mo` enabled for visibility
---
### Fully Visible Browser Actions
- Typing, clicking, and searching are clearly visible
- Browser remains open until user confirmation
- Designed for learning, debugging, and demos
---
### Supported Websites
The agent supports site-specific logic for:

- **Google Search**
- **YouTube Search & Play**
- **Amazon Product Search**
- **Local HTML Login Pages**
Each site uses safe selectors and fallbacks.
---
### Local Login Automation
- Automates login using:
  - Username input
  - Password input
  - Login button click
- Redirects to home page after successful login
---
### Live Execution Logs
- Execution logs stream live to terminal
- No silent execution
- Clear success/failure messages
---
### Minimal Dark UI
- Clean dark-themed interface
- Input box for instructions
- Example test commands
- Shows generated Python code and status
---
## Tech Stack
- Python 3
- Playwright (Python)
- Flask
- LangGraph
- LLM (Groq / Ollama)
- HTML, CSS, JavaScript
---
