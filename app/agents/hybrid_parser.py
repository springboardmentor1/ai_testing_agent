from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from app.agents.instruction_parser import parser_agent
from app.agents.llm_instruction_parser import llm_parser_agent

class HybridState(TypedDict):
    input: str
    actions: List[Dict[str, str]]

def route_parser(state: HybridState):
    # Simple heuristic
    if len(state["input"].split()) > 3:
        return llm_parser_agent.invoke(state)
    return parser_agent.invoke(state)

graph = StateGraph(HybridState)
graph.add_node("router", route_parser)
graph.set_entry_point("router")
graph.add_edge("router", END)

hybrid_parser_agent = graph.compile()
