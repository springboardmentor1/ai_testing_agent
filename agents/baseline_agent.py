import asyncio
import os
import json
import re
from pathlib import Path
from typing import TypedDict, List
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

    report_history: List[dict] 
    iteration_count: int


PARSER_SYSTEM_PROMPT = """
You are a web testing assistant. Convert the user's natural language instruction 
into a JSON object with these exact keys:
- "action": (must be 'navigate', 'click', 'type', or 'verify')
- "target": (the button name, input field, or URL)
- "value": (the text to type, if any; otherwise null)

IMPORTANT: Output ONLY the raw JSON object.
"""

def llm_parser(state: AgentState) -> AgentState:

    count = state.get("iteration_count", 0) + 1
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", PARSER_SYSTEM_PROMPT),
        ("human", "{user_input}") 
    ])
    chain = prompt | llm
    ai_response = chain.invoke({"user_input": state["input"]})
    
    content = ai_response.content
    try:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        parsed_json = json.loads(json_match.group(0)) if json_match else {"action": "error"}
    except Exception:
        parsed_json = {"action": "error", "target": "parsing"}
    
    return {**state, "parsed_command": parsed_json, "iteration_count": count}

def real_code_generator(state: AgentState) -> AgentState:
    return state


async def browser_executor(state: AgentState) -> AgentState:
    cmd = state["parsed_command"]
    raw_input = state["input"].lower()
    history = state.get("report_history", [])

    if cmd["action"] == "error": 
        return {**state, "output": f"Error: {cmd.get('target')}"}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        try:
            target = cmd["target"]
            static_uri = Path("static/index.html").absolute().as_uri()
            if not Path("static/index.html").exists():
                static_uri = Path("index.html").absolute().as_uri()


            if cmd["action"] == "navigate":
                target_url = static_uri if "index.html" in target.lower() else (
                    target if target.startswith("http") else f"https://{target}"
                )
                await page.goto(target_url, wait_until="load")
                report = f"Navigated to {target_url}"
            
            elif cmd["action"] == "click":
                if page.url == "about:blank": await page.goto(static_uri)
                clean_target = re.sub(r'button|link', '', target, flags=re.I).strip()
        
                await page.get_by_text(clean_target, exact=False).or_(
                    page.get_by_role("button", name=clean_target, exact=False)
                ).first.click(timeout=5000)
                report = f"Clicked '{clean_target}'"
                
            elif cmd["action"] == "type":
                if page.url == "about:blank":
                    url = "https://www.google.com" if any(x in raw_input for x in ["search", "google"]) else static_uri
                    await page.goto(url)
                
                field = page.get_by_role("combobox").or_(page.get_by_role("textarea")).or_(
                    page.get_by_placeholder("Username", exact=False)
                ).first
                await field.fill(cmd["value"])
                if "search" in raw_input: await page.keyboard.press("Enter")
                report = f"Typed '{cmd['value']}'"

            elif cmd["action"] == "verify":
                if page.url == "about:blank": await page.goto(static_uri)
                await expect(page.get_by_text(target).first).to_be_visible(timeout=5000)
                report = f"Verified visibility of '{target}'"

          
            history.append({"action": cmd["action"], "status": " SUCCESS", "details": report})

        except Exception as e:
            report = f"Execution Failed: {str(e)}"
    
            history.append({"action": cmd["action"], "status": " FAILED", "details": report})
        finally:
            await asyncio.sleep(1)
            await browser.close()
            
    return {**state, "output": report, "report_history": history}


def should_continue(state: AgentState):
    """
    Implements advanced error handling logic.
    If execution fails, it allows for a limited number of retries (Self-Healing).
    """
    if "Execution Failed" in state["output"] and state["iteration_count"] < 3:
        print(f" Action Failed. Self-Healing Attempt {state['iteration_count']}...")
        return "retry"
    return "end"


workflow = StateGraph(AgentState)

workflow.add_node("parser", llm_parser)
workflow.add_node("generator", real_code_generator)
workflow.add_node("executor", browser_executor)

workflow.set_entry_point("parser")
workflow.add_edge("parser", "generator")
workflow.add_edge("generator", "executor")

workflow.add_conditional_edges(
    "executor",
    should_continue,
    {
        "retry": "parser",
        "end": END
    }
)

agent = workflow.compile()