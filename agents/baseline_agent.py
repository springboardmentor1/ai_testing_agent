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
    parsed_command: List[dict]
    output: str
    report_history: List[dict] 
    iteration_count: int       



PARSER_SYSTEM_PROMPT = """
You are a professional Web Automation Engineer. Convert natural language into a 
JSON LIST of actionable steps. 

Each object must follow this schema:
{{
  "action": "navigate" | "click" | "type" | "verify",
  "target": "URL or element description",
  "value": "text to type or null"
}}

Example: "Go to google.com and search for AI"
[
  {{"action": "navigate", "target": "google.com", "value": null}},
  {{"action": "type", "target": "search bar", "value": "AI"}}
]

IMPORTANT: Return ONLY the raw JSON list. No preamble or conversational filler.
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
      
        json_match = re.search(r"\[.*\]", content, re.DOTALL)
        parsed_json = json.loads(json_match.group(0)) if json_match else []
    except Exception as e:
        parsed_json = [{"action": "error", "target": "parsing", "value": str(e)}]
    
    return {**state, "parsed_command": parsed_json, "iteration_count": count}

async def browser_executor(state: AgentState) -> AgentState:
    commands = state.get("parsed_command", [])
    history = state.get("report_history", [])
    report_details = ""

    if not commands or commands[0].get("action") == "error":
        return {**state, "output": "Execution Failed: Invalid Command Format"}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        try:
            for cmd in commands:
                action = cmd["action"]
                target = cmd["target"]
                val = cmd.get("value")

            
                if action == "navigate":
                    target_url = target if target.startswith("http") else f"https://{target}"
                    await page.goto(target_url, wait_until="load", timeout=15000)
                    step_report = f"Successfully navigated to {target_url}"
                
               
                elif action == "click":
                   
                    await page.get_by_role("button", name=target, exact=False).or_(
                        page.get_by_text(target, exact=False)
                    ).first.click(timeout=8000)
                    step_report = f"Clicked element: '{target}'"
                
               
                elif action == "type":
                    
                    field_selectors = [
                        "textarea:visible", 
                        "input[name='q']:visible", 
                        "input[type='text']:visible", 
                        "[role='combobox']:visible"
                    ]
                    
                    found_field = None
                    for selector in field_selectors:
                        try:
                            locator = page.locator(selector).first
                            if await locator.is_visible(timeout=2000):
                                found_field = locator
                                break
                        except: continue
                    
                    if found_field:
                        await found_field.fill(val)
                        await page.keyboard.press("Enter")
                        step_report = f"Typed '{val}' into visible input field."
                    else:
                        raise Exception("Could not find a visible or editable input field.")
                
              
                elif action == "verify":
                    await expect(page.get_by_text(target).first).to_be_visible(timeout=8000)
                    step_report = f"Verified visibility of '{target}'"

              
                history.append({"action": action, "status": " SUCCESS", "details": step_report})
                report_details = step_report

        except Exception as e:
            error_msg = f"Execution Failed at step '{action}': {str(e)}"
            
            history.append({"action": action, "status": " FAILED", "details": error_msg})
            report_details = error_msg
        finally:
            await asyncio.sleep(2)
            await browser.close()
            
    return {**state, "report_history": history, "output": report_details}


def should_continue(state: AgentState):
    """
    Implements advanced error handling (Milestone 4).
    Loops back to parser for adaptive re-evaluation up to 3 times. 
    """
    if "Failed" in state.get("output", "") and state.get("iteration_count", 0) < 3:
        print(f" Self-Healing triggered: Attempt {state['iteration_count']}...")
        return "retry"
    return "end"


workflow = StateGraph(AgentState)

workflow.add_node("parser", llm_parser)
workflow.add_node("executor", browser_executor)

workflow.set_entry_point("parser")
workflow.add_edge("parser", "executor")


workflow.add_conditional_edges(
    "executor",
    should_continue,
    {
        "retry": "parser",
        "end": END
    }
)

agent = workflow.compile()