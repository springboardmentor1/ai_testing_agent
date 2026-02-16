from typing import TypedDict
import json
import re
import os

from dotenv import load_dotenv
from google import genai
from langgraph.graph import StateGraph, END

#Load API key from .env
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

MODEL_NAME = "models/gemini-flash-latest"


class ParserState(TypedDict):
    input: str
    output: dict


SYSTEM_PROMPT = """
You are an AI test automation engine.

Convert a natural language test case into EXECUTABLE Playwright JSON.

IMPORTANT RULES:
- Output ONLY valid JSON
- Do NOT include explanations, markdown, or extra text
- Follow the schema strictly
- Use ONLY the allowed actions

ALLOWED ACTIONS:
- goto
- fill
- click
- assert_visible

STRICTLY FORBIDDEN:
- assert_url
- assert_text
- expect
- any other assertion type

OUTPUT SCHEMA:
{
  "steps": [
    {
      "action": "goto | fill | click | assert_visible",
      "url": "string (required only for goto)",
      "selector": "string (required for fill, click, assert_visible)",
      "value": "string (required only for fill)"
    }
  ]
}

GENERAL GUIDELINES:
- Break the test case into ordered UI steps
- Use 'goto' to open web pages
- Use 'fill' to enter text into inputs
- Use 'click' to press buttons or links
- Use 'assert_visible' to verify UI results

KNOWN APPLICATION CONTEXTS:

1) LOGIN PAGE
- URL: http://localhost:5000
- Username input: #username
- Password input: #password
- Login button: #loginBtn
- Dashboard: #dashboard
- Error message: #error
- Valid credentials:
  - username: admin
  - password: admin123

2) GOOGLE
- URL: https://www.google.com
- Search input: input[name='q']

3) AMAZON
- URL: https://www.amazon.in
- Search input: input[name='field-keywords']
- Logo selector: #nav-logo-sprites

ASSERTION RULES:
- Successful login → assert_visible #dashboard
- Failed login → assert_visible #error
- Google page → navigation only (no assertions)
- Amazon page → assert_visible #nav-logo-sprites
"""


def parse_instruction(state: ParserState) -> ParserState:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"{SYSTEM_PROMPT}\n\nTest case:\n{state['input']}",
        config={"temperature": 0}
    )

    text = response.text.strip()

    #Remove markdown formatting if LLM adds it
    text = re.sub(r"^```(json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    # Extract JSON safely
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"Invalid JSON generated: {text}")

    parsed = json.loads(match.group())

    return {
        "input": state["input"],
        "output": parsed
    }


#Build LangGraph workflow
graph = StateGraph(ParserState)
graph.add_node("parse_instruction", parse_instruction)
graph.set_entry_point("parse_instruction")
graph.add_edge("parse_instruction", END)

agent = graph.compile()

