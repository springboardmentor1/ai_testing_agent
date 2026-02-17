

AI Agent for Automatic Website Testing using Natural Language

## Objective
Establish the foundational environment and application structure required for building an AI-based web testing agent. This milestone focuses on setting up the development stack, initializing a basic Flask application, and implementing a baseline LangGraph agent configuration.

---

## Tasks and Deliverables

### 1. Python Environment Setup
- Install **Python 3.10+**
- Create and activate a virtual environment
- Install required dependencies:
  - Flask
  - LangGraph
  - Playwright
- Install Playwright browser binaries

---

### 2. Project Structure Definition
- Define a clean and minimal project folder structure
- Separate concerns for:
  - Backend application
  - HTML templates
  - Static assets
- Ensure the structure is scalable for future milestones

---

### 3. Flask Server Initialization
- Initialize a basic Flask application
- Configure Flask to:
  - Serve a static HTML test page
  - Expose a simple API endpoint for receiving user input
- Verify server functionality via browser and API testing

---

### 4. Baseline LangGraph Agent Configuration
- Define an initial LangGraph workflow
- Create a basic agent state to handle user inputs
- Connect Flask input to the LangGraph agent pipeline
- Validate that user instructions can be received and processed by the agent (no automation logic yet)

---

## Outcome
By the end of Milestone 1:
- The development environment is fully set up
- A working Flask application serves a static HTML page
- A baseline LangGraph agent is integrated and able to accept user input
- The system is ready for instruction parsing and automation logic in Milestone 2

---


# ai_testing_agent
## How to Run

```bash
source venv/bin/activate
python -m app.server
