from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import json

# ---------- State ----------
class LLMParserState(TypedDict):
    input: str
    actions: List[Dict[str, str]]

# ---------- LLaMA 3.3 via Groq ----------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

prompt = PromptTemplate(
    input_variables=["instruction"],
    template="""
You are an AI test instruction parser.

Convert the following user instruction into structured browser actions.

Allowed actions:
- open (url)
- click (selector)
- type (selector, value)
- assert_text (selector, text)

User instruction:
{instruction}

Return ONLY valid JSON (no explanation):

[
  {{ "action": "...", "target": "...", "value": "..." }}
]
"""
)

def llm_parse(state: LLMParserState) -> LLMParserState:
    response = llm.invoke(
        prompt.format(instruction=state["input"])
    )

    actions = json.loads(response.content)

    return {
        "input": state["input"],
        "actions": actions
    }

# ---------- LangGraph ----------
graph = StateGraph(LLMParserState)
graph.add_node("llm_parser", llm_parse)
graph.set_entry_point("llm_parser")
graph.add_edge("llm_parser", END)

llm_parser_agent = graph.compile()
