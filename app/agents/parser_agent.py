from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.config.llm import call_llm
import json


# ---------- State Definition ----------
class AgentState(TypedDict):
    input: str
    output: dict


# ---------- Prompt Template ----------
PARSER_PROMPT = """
You are a command parser.

Convert the user instruction into STRICT JSON.

Allowed actions:
- OPEN_BROWSER (target: url)
- SEARCH (query: string)

Rules:
- Output ONLY valid JSON
- No text outside JSON
- Always return an object with a "steps" array

Example:
{{
  "steps": [
    {{ "action": "OPEN_BROWSER", "target": "https://www.google.com" }},
    {{ "action": "SEARCH", "query": "amazon" }}
  ]
}}

User instruction:
{instruction}
"""


# ---------- Parser Node (PURE LLM) ----------
def respond(state: AgentState) -> AgentState:
    prompt = PARSER_PROMPT.format(instruction=state["input"])

    # Retry loop is NOT rule-based parsing
    # It is only validation (allowed)
    for _ in range(3):
        raw = call_llm(prompt)
        parsed = json.loads(raw)   # will raise if invalid
        return {
            "input": state["input"],
            "output": parsed
        }

    # If LLM violates contract after retries
    raise ValueError("LLM failed to produce valid JSON")


# ---------- LangGraph Wiring ----------
def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("parse", respond)
    graph.set_entry_point("parse")
    graph.add_edge("parse", END)

    return graph.compile()


# ---------- Agent Instance ----------
agent = build_agent()
