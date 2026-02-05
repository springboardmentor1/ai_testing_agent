import re
from typing import List
from app.agents.instruction_state import InstructionState

def instruction_parser_node(state: InstructionState) -> InstructionState:
    text = state["input"].lower()
    actions: List[dict] = []

    intent = "unknown"

    if "open google" in text:
        actions.append({
            "action": "navigate",
            "target": "https://www.google.com",
            "value": None
        })
        intent = "open_google"

    search_match = re.search(r"search for (.+)", text)
    if search_match:
        term = search_match.group(1)
        actions.append({
            "action": "type",
            "target": "search_box",
            "value": term
        })
        actions.append({
            "action": "press",
            "target": "enter",
            "value": None
        })
        intent = "search"

    confidence = 0.8 if actions else 0.2

    return {
        **state,
        "intent": intent,
        "confidence": confidence,
        "parsed_actions": actions
    }
