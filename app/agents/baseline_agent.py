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

    # ---- Local Test Page ----
    if "test page" in text:
        actions.append({"action": "open", "target": "test", "value": ""})
        actions.append({"action": "verify", "target": "login", "value": ""})
        return {"input": state["input"], "actions": actions}

    # ---- Known Websites ----
    for site in ["google", "amazon", "flipkart"]:
        if site in text:
            actions.append({"action": "open", "target": site, "value": ""})
            break

    # ---- Search Intent ----
    if "search for" in text:
        query = text.split("search for")[-1].strip()
        actions.append({"action": "search", "target": "", "value": query})

    return {"input": state["input"], "actions": actions}

# =========================
# LLM-based Parser
# =========================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

prompt = PromptTemplate(
    input_variables=["instruction"],
    template="""
You are an AI test instruction parser.

Convert the instruction into structured browser actions.

Allowed actions:
- open (site or url)
- search (query)
- click
- type
- verify

Return ONLY valid JSON array.
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
    text = state["input"].lower()

    # Known simple patterns → rule-based
    known_keywords = ["google", "amazon", "flipkart", "test page", "search for"]

    if any(k in text for k in known_keywords) and len(text.split()) <= 10:
        return rule_parser(state)

    # Complex / flexible instructions → LLM
    return llm_parser(state)

# =========================
# LangGraph Workflow
# =========================
graph = StateGraph(AgentState)
graph.add_node("router", router)
graph.set_entry_point("router")
graph.add_edge("router", END)

agent = graph.compile()
