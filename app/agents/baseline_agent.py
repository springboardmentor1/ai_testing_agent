import asyncio
import os
import json
import re
from pathlib import Path
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from playwright.async_api import async_playwright, expect
from typing import List

load_dotenv()

class AgentState(TypedDict):
    input: str
    parsed_command: List[dict]
    output: str

PARSER_SYSTEM_PROMPT = """
You are a web testing assistant. Convert the user's natural language instruction 
into a JSON array of steps. Each step must be a JSON object with these exact keys:
- "action": (must be 'navigate', 'click', 'type', or 'verify')
- "target": (the button name, input field, or URL)
- "value": (the text to type, if any; otherwise null)

IMPORTANT: Output ONLY the raw JSON array, no explanation or extra text.
"""


def llm_parser(state: AgentState) -> AgentState:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", PARSER_SYSTEM_PROMPT),
        ("human", "{user_input}") 
    ])
    chain = prompt | llm
    ai_response = chain.invoke({"user_input": state["input"]})
    
    content = ai_response.content
    try:
        json_match = re.search(r"\[.*\]", content, re.DOTALL)
        parsed_json = json.loads(json_match.group(0)) if json_match else [{"action": "error"}]
    except Exception as e:
        parsed_json = [{"action": "error", "target": "parsing", "value": str(e)}]
    
    return {**state, "parsed_command": parsed_json}

def real_code_generator(state: AgentState) -> AgentState:
    return state

async def browser_executor(state: AgentState) -> AgentState:
    commands = state["parsed_command"]
    raw_input = state["input"].lower()
    report_lines = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()

        try:
            static_uri = Path("static/index.html").absolute().as_uri()
            if not Path("static/index.html").exists():
                static_uri = Path("index.html").absolute().as_uri()

            for cmd in commands:
                action = cmd.get("action")
                target = cmd.get("target")
                value = cmd.get("value")

                if action == "error":
                    report_lines.append(f"❌ Parsing error: {target}")
                    continue

                if action == "navigate":
                    target_url = static_uri if "index.html" in target.lower() else (
                        target if target.startswith("http") else f"https://{target}"
                    )
                    await page.goto(target_url, wait_until="load")
                    report_lines.append(f"✅ Navigated to {target_url}")

                elif action == "click":
                    if page.url == "about:blank":
                        await page.goto(static_uri)

                    clean_target = re.sub(r'button|link', '', target, flags=re.I).strip()
                    button = page.locator(f"button:has-text('{clean_target}')").first
                    await button.click(timeout=5000)
                    report_lines.append(f"✅ Clicked on '{clean_target}'")

                elif action == "type":
                    if page.url == "about:blank":
                        if "search" in raw_input or "youtube" in raw_input:
                            await page.goto("https://www.youtube.com")
                        else:
                            await page.goto(static_uri)

                    normalized_target = (
                        target.lower()
                        .replace("enter ", "")
                        .replace("field", "")
                        .replace("the", "")
                        .strip()
                    )

                    if "username" in normalized_target:
                        field = page.locator("input#username")
                    elif "password" in normalized_target:
                        field = page.locator("input#password")
                    else:
                        field = (
                            page.get_by_placeholder(normalized_target, exact=False)
                            .or_(page.locator(f"input[placeholder*='{normalized_target}' i]"))
                            .or_(page.locator(f"input[id*='{normalized_target}' i]"))
                            .or_(page.get_by_role("textbox"))
                            .or_(page.get_by_role("combobox"))
                            .first
                        )

                    await field.fill(value)
                    if "search" in raw_input:
                        await page.keyboard.press("Enter")

                    report_lines.append(f"✅ Typed '{value}' into '{target}'")

                elif action == "verify":
                    if page.url == "about:blank":
                        await page.goto(static_uri)

                    await expect(page.get_by_text(target, exact=False).first).to_be_visible(timeout=5000)
                    report_lines.append(f"✅ Verified visibility of '{target}'")

                else:
                    report_lines.append(f"❌ Unknown action: {action}")

        except Exception as e:
            try:
                await page.screenshot(path="error_screenshot.png")
                report_lines.append(f"❌ Execution Failed: {str(e)} (screenshot saved)")
            except:
                report_lines.append(f"❌ Execution Failed: {str(e)}")
        finally:
            await asyncio.sleep(2)
            await browser.close()

    return {**state, "output": "\n".join(report_lines)}


   

graph = StateGraph(AgentState)
graph.add_node("parser", llm_parser)
graph.add_node("generator", real_code_generator)
graph.add_node("executor", browser_executor)

graph.set_entry_point("parser")
graph.add_edge("parser", "generator")
graph.add_edge("generator", "executor")
graph.add_edge("executor", END)
agent = graph.compile()
