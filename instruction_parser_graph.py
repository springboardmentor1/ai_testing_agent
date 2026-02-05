from langgraph.graph import StateGraph, END
from app.agents.instruction_state import InstructionState
from app.agents.parser_node import instruction_parser_node
from app.agents.hf_llm_parser_node import hf_llm_parser_node
from app.agents.command_mapper_node import command_mapper_node


def route_parser(state: InstructionState):
    if state.get("confidence", 0) < 0.7:
        return "hf_llm_parser"
    return "map_commands"


graph = StateGraph(InstructionState)

graph.add_node("rule_parser", instruction_parser_node)
graph.add_node("hf_llm_parser", hf_llm_parser_node)
graph.add_node("map_commands", command_mapper_node)

graph.set_entry_point("rule_parser")

graph.add_conditional_edges(
    "rule_parser",
    route_parser,
    {
        "hf_llm_parser": "hf_llm_parser",
        "map_commands": "map_commands"
    }
)

graph.add_edge("hf_llm_parser", "map_commands")
graph.add_edge("map_commands", END)

instruction_parser_agent = graph.compile()
