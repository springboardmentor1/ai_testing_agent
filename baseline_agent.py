from typing import TypedDict
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    input: str
    output: str

def respond(state: AgentState) -> AgentState:
    return {
        "input": state["input"],
        "output": f"Echo: {state['input']}"
    }

graph = StateGraph(AgentState)
graph.add_node("respond", respond)
graph.set_entry_point("respond")
graph.add_edge("respond", END)

agent = graph.compile()
