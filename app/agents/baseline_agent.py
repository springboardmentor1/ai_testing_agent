from typing import TypedDict, List
from langgraph.graph import StateGraph, END

# Import our custom modules
from app.parser import parse_instruction
from app.code_generator import generate_playwright_code
from app.executor import execute_generated_code

# Define Agent State
class AgentState(TypedDict):
    input: str                  # User's raw instruction
    parsed_steps: List[dict]    # JSON steps from Parser
    generated_code: str         # Python code from Generator
    execution_logs: List[str]   # Result logs from Executor
    output: str                 # Final response to user

# 1. Parsing Node
def parse_node(state: AgentState):
    print(f"DEBUG: Parsing '{state['input']}'...")
    steps = parse_instruction(state['input'])
    return {"parsed_steps": steps}

# 2. Code Generation Node
def generate_node(state: AgentState):
    print("DEBUG: Generating Python Code...")
    code = generate_playwright_code(state['parsed_steps'])
    return {"generated_code": code}

# 3. Execution Node
def execute_node(state: AgentState):
    print("DEBUG: Executing Code in Headless Browser...")
    logs = execute_generated_code(state['generated_code'])
    return {
        "execution_logs": logs,
        "output": "\n".join(logs)
    }

# Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("parser", parse_node)
workflow.add_node("generator", generate_node)
workflow.add_node("executor", execute_node)

# Connect the edges (Linear Flow)
workflow.set_entry_point("parser")
workflow.add_edge("parser", "generator")
workflow.add_edge("generator", "executor")
workflow.add_edge("executor", END)

# Compile
agent_app = workflow.compile()