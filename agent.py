<<<<<<< HEAD
#agent program

def run_agent(user_input: str) -> str:
    return f"Echo from agent: {user_input}"
=======
from typing import TypedDict
from langgraph.graph import StateGraph, END
class AgentState(TypedDict):
    input: str
    output: str
def respond(state: AgentState) -> AgentState:
    user_input = state["input"]

    return {
        "input": user_input,
        "output": f"Echo from LangGraph agent: {user_input}"
    }
graph = StateGraph(AgentState)

graph.add_node("respond", respond)      
graph.set_entry_point("respond")        
graph.add_edge("respond", END)          

agent = graph.compile()

>>>>>>> e86365c4232a5c9468af5a1ef5cd343c6c71190d
