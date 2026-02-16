from langchain_core.runnables import RunnableLambda
from app.parser import parse_instruction
from app.code_generator import generate_playwright_code
from app.executor import execute_python_code

def run_agent_pipeline(input_data: dict):
    instruction = input_data.get("input")
    steps = parse_instruction(instruction)
    code = generate_playwright_code(steps)
    logs = execute_python_code(code)
    
    return {
        "input": instruction,
        "execution_logs": logs
    }

agent_app = RunnableLambda(run_agent_pipeline)