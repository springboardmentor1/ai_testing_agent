from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import json

# =========================
# State Definition
# =========================
class AgentState(TypedDict):
    input: str
    actions: List[Dict[str, str]]

# =========================
# Rule-based Parser
# =========================
def rule_parser(state: AgentState) -> AgentState:
    text = state["input"].lower()
    actions = []

    if "open" in text and "google" in text:
        actions.append({
            "action": "open",
            "target": "https://www.google.com",
            "value": ""
        })

    if "search for" in text:
        query = text.split("search for")[-1].strip()
        actions.append({
            "action": "type",
            "target": "input[name='q']",
            "value": query
        })
        actions.append({
            "action": "click",
            "target": "input[name='btnK']",
            "value": ""
        })

    return {
        "input": state["input"],
        "actions": actions
    }

# =========================
# LLM-based Parser (LLaMA 3.3)
# =========================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

prompt = PromptTemplate(
    input_variables=["instruction"],
    template="""
You are an AI test instruction parser.

Convert the user instruction into structured browser actions.

Allowed actions:
- open (url)
- click (selector)
- type (selector, value)
- assert_text (selector, text)

Instruction:
{instruction}

Return ONLY valid JSON:
[
  {{ "action": "...", "target": "...", "value": "..." }}
]
"""
)

def llm_parser(state: AgentState) -> AgentState:
    response = llm.invoke(
        prompt.format(instruction=state["input"])
    )

    actions = json.loads(response.content)

    return {
        "input": state["input"],
        "actions": actions
    }

# =========================
# Router (Rule vs LLM)
# =========================
def router(state: AgentState) -> AgentState:
    # Simple heuristic
    if len(state["input"].split()) > 3:
        return llm_parser(state)
    return rule_parser(state)

# =========================
# LangGraph Workflow
# =========================
graph = StateGraph(AgentState)
graph.add_node("router", router)
graph.set_entry_point("router")
graph.add_edge("router", END)

agent = graph.compile()
