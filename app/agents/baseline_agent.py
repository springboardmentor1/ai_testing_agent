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
from app.agents.reporter import TestReporter

load_dotenv()

class AgentState(TypedDict, total=False):
    input: str
    parsed_command: List[dict]
    step_results: List[dict]
    output: str
    report_path: str
    status: str


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
        parsed_json = json.loads(json_match.group(0)) if json_match else []
    except Exception as e:
        parsed_json = []

    # --- Generic fallback ---
    if not parsed_json:
        user_input = state["input"].lower()
        steps = []

        # Always start with a navigate step
        steps.append({
            "action": "navigate",
            "target": user_input,   # keep it generic, executor will resolve
            "value": None
        })

        # If instruction contains "search for X"
        match = re.search(r"search for (.+)", user_input)
        if match:
            query = match.group(1).strip()
            steps.append({"action": "type", "target": "search box", "value": query})
            steps.append({"action": "click", "target": "search", "value": None})

        parsed_json = steps

    return {**state, "parsed_command": parsed_json}



def real_code_generator(state: AgentState) -> AgentState:
    return state

async def browser_executor(state: AgentState) -> AgentState:
    commands = state["parsed_command"]
    raw_input = state["input"].lower()
    report_lines = []
    step_results = []

    reporter = TestReporter()
    screenshots = []
    errors = []

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
                    step_results.append({"step": f"Parsing error: {target}", "status": "fail"})
                    continue

                if action == "navigate":
                    target_url = static_uri if "index.html" in target.lower() else (
                        target if target.startswith("http") else f"https://{target}"
                    )
                    try:
                        response = await page.goto(target_url, wait_until="load", timeout=10000)

                        if not response:
                            msg = f"❌ Navigation failed: No response from {target_url}"
                            errors.append(msg)
                            report_lines.append(msg)
                            step_results.append({"step": f"Navigate to {target_url}", "status": "fail", "error": msg})
                            continue

                        if not response.ok:
                            msg = f"❌ Navigation failed: HTTP {response.status} from {target_url}"
                            errors.append(msg)
                            report_lines.append(msg)
                            step_results.append({"step": f"Navigate to {target_url}", "status": "fail", "error": msg})
                            continue

                        report_lines.append(f"✅ Navigated to {page.url} (HTTP {response.status})")
                        step_results.append({"step": f"Navigate to {target_url}", "status": "pass"})

                    except Exception as e:
                        msg = f"❌ Navigation error: {str(e)}"
                        errors.append(str(e))
                        report_lines.append(msg)
                        step_results.append({"step": f"Navigate to {target_url}", "status": "fail", "error": str(e)})
                        continue

                elif action == "click":
                    clean_target = re.sub(r'button|link', '', target, flags=re.I).strip()
                    locator = (
                        page.get_by_role("button", name=clean_target).or_(
                            page.get_by_text(clean_target, exact=False)
                        ).first
                    )
                    try:
                        if await locator.count() > 0:
                            await locator.click(timeout=5000)
                            report_lines.append(f"✅ Clicked on '{clean_target}'")
                            step_results.append({"step": f"Click {clean_target}", "status": "pass"})
                        else:
                            msg = f"⚠️ No clickable element found for '{clean_target}'"
                            report_lines.append(msg)
                            step_results.append({"step": f"Click {clean_target}", "status": "fail", "error": msg})
                    except Exception as e:
                        msg = f"❌ Click failed: {str(e)}"
                        errors.append(str(e))
                        report_lines.append(msg)
                        step_results.append({"step": f"Click {clean_target}", "status": "fail", "error": str(e)})

                elif action == "type":
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

                    try:
                        if await field.count() > 0:
                            await field.fill(value)
                            if "search" in raw_input:
                                await page.keyboard.press("Enter")
                            report_lines.append(f"✅ Typed '{value}' into '{target}'")
                            step_results.append({"step": f"Type into {target}", "status": "pass"})
                        else:
                            msg = f"⚠️ No input field found for '{target}'"
                            report_lines.append(msg)
                            step_results.append({"step": f"Type into {target}", "status": "fail", "error": msg})
                    except Exception as e:
                        msg = f"❌ Typing failed: {str(e)}"
                        errors.append(str(e))
                        report_lines.append(msg)
                        step_results.append({"step": f"Type into {target}", "status": "fail", "error": str(e)})

                elif action == "verify":
                    try:
                        await expect(page.get_by_text(target, exact=False).first).to_be_visible(timeout=5000)
                        report_lines.append(f"✅ Verified visibility of '{target}'")
                        step_results.append({"step": f"Verify {target}", "status": "pass"})
                    except Exception as e:
                        msg = f"⚠️ Could not verify '{target}': {str(e)}"
                        errors.append(str(e))
                        report_lines.append(msg)
                        step_results.append({"step": f"Verify {target}", "status": "fail", "error": str(e)})

                else:
                    msg = f"❌ Unknown action: {action}"
                    report_lines.append(msg)
                    step_results.append({"step": f"Unknown action {action}", "status": "fail", "error": msg})

               # ✅ Screenshot after every step 
                try: 
                    screenshot_bytes = await page.screenshot(full_page=True) 
                    screenshots.append(reporter.save_screenshot(screenshot_bytes, f"step_{len(step_results)}")) 
                except Exception as e: 
                    report_lines.append(f"⚠️ Screenshot capture failed: {str(e)}")
 
        except Exception as e:
            errors.append(str(e))
            try:
                screenshot_bytes = await page.screenshot()
                path = reporter.save_screenshot(screenshot_bytes)
                screenshots.append(path)
            except:
                pass
            report_lines.append(f"❌ Execution Failed: {str(e)}")
            step_results.append({"step": "Execution", "status": "fail", "error": str(e)})

        finally:
            await asyncio.sleep(2)
            await browser.close()
    
    # Determine final status
    final_status = (
        "passed"
        if step_results and all(s.get("status") == "pass" for s in step_results)
        else "failed"
    )

    # Generate HTML report
    report_path = reporter.generate_html_report(
        "Milestone_4_Test",
        [str(c) for c in commands],
        "\n".join(report_lines),
        errors,
        screenshots,
        final_status=final_status
    )

    final_output = "\n".join(report_lines) + f"\n📄 HTML Report Generated: {report_path}"
    final_status = (
        "passed"
        if step_results and all(s.get("status") == "pass" for s in step_results)
        else "failed"
    )

    return {
    **state,   # keep original state first
    "parsed_command": commands,
    "step_results": step_results,
    "output": final_output,
    "report_path": report_path,
    "status": final_status
  }



graph = StateGraph(AgentState)
graph.add_node("parser", llm_parser)
graph.add_node("generator", real_code_generator)
graph.add_node("executor", browser_executor)

graph.set_entry_point("parser")
graph.add_edge("parser", "generator")
graph.add_edge("generator", "executor")
graph.add_edge("executor", END)
agent = graph.compile()
