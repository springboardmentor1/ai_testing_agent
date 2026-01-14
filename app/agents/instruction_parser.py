from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

class ParserState(TypedDict):
    input: str
    actions: List[Dict[str, str]]

def parse_instruction(state: ParserState) -> ParserState:
    text = state["input"].lower()
    actions = []

    if "open" in text and "google" in text:
        actions.append({"action": "open", "target": "google"})

    if "search for" in text:
        query = text.split("search for")[-1].strip()
        actions.append({"action": "search", "target": query})

    return {
        "input": state["input"],
        "actions": actions
    }

graph = StateGraph(ParserState)
graph.add_node("parser", parse_instruction)
graph.set_entry_point("parser")
graph.add_edge("parser", END)

parser_agent = graph.compile()
