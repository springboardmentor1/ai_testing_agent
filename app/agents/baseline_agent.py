import asyncio
import json
import re
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from playwright.async_api import async_playwright, expect

load_dotenv()

class AgentState(TypedDict):
    input: str
    parsed_command: dict
    output: str


PARSER_SYSTEM_PROMPT = """
Convert user instruction to JSON:
{
  "action": "navigate | click | type | verify",
  "target": "string",
  "value": "string | null"
}
ONLY output JSON.
"""

def llm_parser(state: AgentState) -> AgentState:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", PARSER_SYSTEM_PROMPT),
        ("human", "{input}")
    ])

    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})

    try:
        parsed = json.loads(re.search(r"\{.*\}", response.content, re.S).group())
    except Exception as e:
        parsed = {"action": "error", "target": "parse", "value": str(e)}

    return {**state, "parsed_command": parsed}


async def browser_executor(state: AgentState) -> AgentState:
    cmd = state["parsed_command"]

    if cmd["action"] == "error":
        return {**state, "output": "Parsing failed"}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            if cmd["action"] == "navigate":
                url = cmd["target"]
                if "index.html" in url:
                    path = Path("app/static/index.html").absolute().as_uri()
                    await page.goto(path)
                else:
                    await page.goto(f"https://{url}")

            elif cmd["action"] == "click":
                await page.get_by_text(cmd["target"], exact=False).click()

            elif cmd["action"] == "type":
                await page.get_by_placeholder("Enter Username").fill(cmd["value"])

            elif cmd["action"] == "verify":
                await expect(page.get_by_text(cmd["target"])).to_be_visible()

            await asyncio.sleep(2)
            await browser.close()
            return {**state, "output": "✅ Success"}

        except Exception as e:
            await browser.close()
            return {**state, "output": f"❌ Failed: {e}"}


graph = StateGraph(AgentState)
graph.add_node("parser", llm_parser)
graph.add_node("executor", browser_executor)
graph.set_entry_point("parser")
graph.add_edge("parser", "executor")
graph.add_edge("executor", END)

agent = graph.compile()
