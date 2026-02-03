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

IMPORTANT: Output ONLY the raw JSON object.
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
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        parsed_json = json.loads(json_match.group(0)) if json_match else {"action": "error"}
    except Exception as e:
        parsed_json = {"action": "error", "target": "parsing", "value": str(e)}
    
    return {**state, "parsed_command": parsed_json}

def real_code_generator(state: AgentState) -> AgentState:
    return state


async def browser_executor(state: AgentState) -> AgentState:
    cmd = state["parsed_command"]
    raw_input = state["input"].lower()
    if cmd["action"] == "error": return {**state, "output": f"Error: {cmd.get('target')}"}

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
                report = f" Success: Navigated to {target_url}"
            
         
            elif cmd["action"] == "click":
          
                if page.url == "about:blank":
                    await page.goto(static_uri)
                
                clean_target = re.sub(r'button|link', '', target, flags=re.I).strip()
                await page.get_by_text(clean_target, exact=False).first.click(timeout=5000)
                report = f" Success: Clicked '{clean_target}'"
                
           
            elif cmd["action"] == "type":
                if page.url == "about:blank":
                  
                    if "search" in raw_input or "google" in raw_input:
                        await page.goto("https://www.google.com")
                    else:
                        await page.goto(static_uri)
                
                field = page.get_by_role("combobox").or_(page.get_by_role("textarea")).or_(
                    page.get_by_placeholder("Username", exact=False)
                ).first
                
                await field.fill(cmd["value"])
                
        
                if "search" in raw_input:
                    await page.keyboard.press("Enter")
                    
                report = f" Success: Typed '{cmd['value']}'"

      
            elif cmd["action"] == "verify":
                if page.url == "about:blank": await page.goto(static_uri)
                await expect(page.get_by_text(target).first).to_be_visible(timeout=5000)
                report = f" Success: Verified visibility of '{target}'"

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