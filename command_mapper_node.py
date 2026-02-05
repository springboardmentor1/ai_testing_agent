from app.agents.instruction_state import InstructionState

def command_mapper_node(state: InstructionState) -> InstructionState:
    return {
        **state,
        "commands": state.get("parsed_actions", [])
    }
