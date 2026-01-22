from langgraph.graph import StateGraph
from graph.state import ParserState
from rule_parser import rule_based_parser

def instruction_parser_node(state: ParserState):
    actions = rule_based_parser(state["user_input"])
    return {"actions": actions}

builder = StateGraph(ParserState)

builder.add_node("instruction_parser", instruction_parser_node)
builder.set_entry_point("instruction_parser")

parser_graph = builder.compile()
