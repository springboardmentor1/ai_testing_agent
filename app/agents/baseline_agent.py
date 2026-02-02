import asyncio
import os
import json
import re
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
You are a web testing assistant. Convert the user's natural language instruction 
into a JSON object with these exact keys:
- "action": (must be 'navigate', 'click', 'type', or 'verify')
- "target": (the button name, input field, or URL)
- "value": (the text to type, if any; otherwise null)

IMPORTANT: Output ONLY the raw JSON object. Do not include any conversational text.
"""

def llm_parser(state: AgentState) -> AgentState:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", PARSER_SYSTEM_PROMPT),
        ("human", "{user_input}") 
    ])
    
    chain = prompt | llm
    ai_response = chain.invoke({"user_input": state["input"]})
    content = ai_response.content
    try:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            clean_json = json_match.group(0)
            parsed_json = json.loads(clean_json)
        else:
            raise ValueError("No JSON found in response")
    except Exception as e:
        parsed_json = {"action": "error", "target": "parsing", "value": str(e)}
    
    return {**state, "parsed_command": parsed_json}

def real_code_generator(state: AgentState) -> AgentState:
    cmd = state["parsed_command"]
    action = cmd.get("action")
    target = cmd.get("target")
    value = cmd.get("value")

    if action == "navigate":
        code = f"page.goto('{target}')"
    elif action == "click":
        code = f"page.get_by_text('{target}', exact=False).first.click()"
    elif action == "type":
        code = f"page.get_by_role('combobox').first.fill('{value}')"
    elif action == "verify":
        code = f"expect(page.get_by_text('{target}')).to_be_visible()"
    else:
        code = "print('Unsupported action')"

    return {**state, "output": code}


async def browser_executor(state: AgentState) -> AgentState:
    cmd = state["parsed_command"]
    if cmd["action"] == "error": return {**state, "output": f" Error: {cmd['target']}"}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        try:
            target_url = cmd["target"]
            
            if cmd["action"] == "navigate":
                if not target_url.startswith("http"): target_url = f"https://{target_url}"
                await page.goto(target_url, wait_until="load", timeout=15000)
                report = f" Navigated to {target_url}"
            
            else:
                await page.goto("https://www.youtube.com", wait_until="load")
                try:
                    consent_btn = page.get_by_role("button", name=re.compile("Accept|Agree", re.I))
                    if await consent_btn.is_visible(timeout=2000):
                        await consent_btn.click()
                except:
                    pass

                if cmd["action"] == "click":
                    await page.get_by_text(cmd["target"], exact=False).first.click(timeout=10000)
                    report = f" Clicked '{cmd['target']}'"
                
                elif cmd["action"] == "type":
                    search_box = page.get_by_role("combobox").or_(page.get_by_role("textarea")).first
                    await search_box.fill(cmd["value"])
                    await search_box.press("Enter")
                    report = f" Typed '{cmd['value']}' and searched."
                
                elif cmd["action"] == "verify":
                    await expect(page.get_by_text(cmd["target"]).first).to_be_visible(timeout=10000)
                    report = f" Verified: '{cmd['target']}' is visible."

        except Exception as e:
            report = f" Execution Failed: {str(e)}"
        finally:
            await asyncio.sleep(2)
            await browser.close()
            
    return {**state, "output": report}

graph = StateGraph(AgentState)
graph.add_node("parser", llm_parser)
graph.add_node("generator", real_code_generator)
graph.add_node("executor", browser_executor)

graph.set_entry_point("parser")
graph.add_edge("parser", "generator")
graph.add_edge("generator", "executor")
graph.add_edge("executor", END)

agent = graph.compile()