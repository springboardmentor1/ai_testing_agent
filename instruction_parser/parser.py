import json
import requests

from instruction_parser.prompt import SYSTEM_PROMPT
from schemas.instruction_schema import ParsedInstruction


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.3"


def parse_instruction(user_input: str):
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{SYSTEM_PROMPT}\nUser instruction: {user_input}",
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()

    print("\n======= FULL OLLAMA RESPONSE =======")
    print(data)
    print("===================================\n")

    llm_output = data["response"].strip()

    print("\n======= RAW MODEL OUTPUT =======")
    print(llm_output)
    print("================================\n")

    parsed_json = json.loads(llm_output)
    return ParsedInstruction(**parsed_json)
