import json
import re
from transformers import pipeline
from app.agents.instruction_state import InstructionState

llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    device=-1
)

def hf_llm_parser_node(state: InstructionState) -> InstructionState:
    instruction = state["input"]

    prompt = f"""
You are a JSON generator.

Instruction:
{instruction}

Return ONLY a valid JSON array.
No explanation.
No text.
No markdown.

Example:
[
  {{"action":"navigate","target":"https://www.google.com","value":null}},
  {{"action":"type","target":"search_box","value":"amazon"}},
  {{"action":"press","target":"enter","value":null}}
]
"""

    result = llm(prompt, max_new_tokens=256)[0]["generated_text"]

    try:
        json_text = re.search(r"\[.*\]", result, re.DOTALL).group(0)
        parsed_actions = json.loads(json_text)
        confidence = 0.9
    except Exception:
        parsed_actions = []
        confidence = 0.3

    return {
        **state,
        "intent": "llm_parsed",
        "confidence": confidence,
        "parsed_actions": parsed_actions
    }
