from typing import List, Dict

def generate_playwright_code(steps: List[Dict]) -> str:
    """
    Converts a list of JSON steps into a full executable Python script string.
    """
    
    # 1. Start the Code Template
    code_lines = [
        "from playwright.sync_api import sync_playwright, expect",
        "import time",
        "",
        "def run_automation():",
        "    results = []",
        "    with sync_playwright() as p:",
        "        # FIX: Explicit window size (1280x720) prevents blank rendering issues",
        "        # FIX: slow_mo=2000 makes every move take 2 seconds (Very visible)",
        "        browser = p.chromium.launch(headless=False, slow_mo=2000)",
        "        context = browser.new_context(viewport={'width': 1280, 'height': 720})",
        "        page = context.new_page()",
        "        try:",
    ]

    # 2. Loop through steps and translate to Code
    for step in steps:
        action = step.get("action")
        params = step.get("params", {})
        desc = step.get("description", "Unknown Step")

        code_lines.append(f"            # Step: {desc}")

        if action == "goto":
            url = params.get("url")
            code_lines.append(f'            print("   -> Loading {url}...")')
            code_lines.append(f'            page.goto(r"""{url}""")')
        
            code_lines.append(f'            print("   -> Waiting for page graphics...")')
            code_lines.append(f'            time.sleep(4)')
            code_lines.append(f'            results.append("SUCCESS: Opened {url}")')

        elif action == "fill":
            sel = params.get("selector")
            val = params.get("value")
            code_lines.append(f'            page.locator("""{sel}""").wait_for(state="visible", timeout=10000)')
            code_lines.append(f'            page.locator("""{sel}""").fill("""{val}""")')
            code_lines.append(f'            results.append("SUCCESS: Typed \'{val}\' into {sel}")')

        elif action == "press":
            sel = params.get("selector", "body")
            key = params.get("key")
            code_lines.append(f'            page.locator("""{sel}""").press("""{key}""")')
            code_lines.append(f'            results.append("SUCCESS: Pressed key \'{key}\'")')

        elif action == "click":
            sel = params.get("selector")
            code_lines.append(f'            page.locator("""{sel}""").wait_for(state="visible", timeout=10000)')
            
            code_lines.append(f'            time.sleep(1)') 
            code_lines.append(f'            page.locator("""{sel}""").click()')
            code_lines.append(f'            results.append("SUCCESS: Clicked {sel}")')

        elif action == "assert":
            check_type = params.get("type")
            value = params.get("value")
            
            if check_type == "title":
                code_lines.append(f'            expect(page).to_have_title("""{value}""", timeout=10000)')
                code_lines.append(f'            results.append("SUCCESS: Verified title is \'{value}\'")')
            elif check_type == "text":
                sel = params.get("selector", "body")
                code_lines.append(f'            expect(page.locator("""{sel}""")).to_contain_text("""{value}""", timeout=10000)')
                code_lines.append(f'            results.append("SUCCESS: Found text \'{value}\'")')

    # 3. Close the Block
    code_lines.append("            # Final pause to admire the result")
    code_lines.append("            time.sleep(3)") 
    code_lines.append("            browser.close()")
    code_lines.append("            return results")
    code_lines.append("        except Exception as e:")
    code_lines.append("            browser.close()")
    code_lines.append("            return [f'ERROR: {str(e)}']")
    
    return "\n".join(code_lines)