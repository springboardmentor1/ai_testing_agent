from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from app.parser import parse_instruction

# 1. Define the State (Memory)
class AgentState(TypedDict):
    input: str
    parsed_commands: List[dict]  #  stores the JSON list here
    output: str

# 2. Define the Node (The Work)
def parse_node(state: AgentState):
    user_input = state['input']
    
    # Calls Groq Parser
    commands = parse_instruction(user_input)
    
    if not commands:
        return {"output": "Failed to parse instruction."}

    return {
        "parsed_commands": commands, 
        "output": f"Successfully generated {len(commands)} steps."
    }

# 3. Build the Workflow Graph
workflow = StateGraph(AgentState)

workflow.add_node("parser", parse_node)
workflow.set_entry_point("parser")
workflow.add_edge("parser", END)

agent_app = workflow.compile()