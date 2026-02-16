from typing import List, Dict

def generate_playwright_code(steps: List[Dict]) -> str:
    """
    Generates robust Playwright code with Debugging capabilities.
    """
    
    code_lines = [
        "from playwright.sync_api import sync_playwright, expect",
        "import time",
        "import os",
        "",
        "def run_automation():",
        "    results = []",
        "",
        "    with sync_playwright() as p:",
        "        print('   [Browser] Launching...')",
        "        # Launch with arguments to bypass bot detection",
        "        browser = p.chromium.launch(",
        "            headless=False, ",
        "            slow_mo=3000, ",
        "            args=['--disable-blink-features=AutomationControlled', '--start-maximized']",
        "        )",
        "        context = browser.new_context(no_viewport=True)",
        "        page = context.new_page()",
        "        try:",
    ]

    for step in steps:
        action = step.get("action")
        params = step.get("params", {})
        desc = step.get("description", "Unknown Step")

        code_lines.append(f"            # Step: {desc}")

        if action == "goto":
            url = params.get("url")
            code_lines.append(f'            print("   -> Navigating to {url}...")')
            code_lines.append(f'            page.goto(r"""{url}""", timeout=60000, wait_until="domcontentloaded")')
            
            code_lines.append(f'            print(f"   [Debug] Page Loaded: {{page.title()}}")') 
            code_lines.append(f'            results.append({{"status": "success", "message": "Opened {url}"}})')

        elif action == "fill":
            sel = params.get("selector")
            val = params.get("value")
            code_lines.append(f'            page.locator("""{sel}""").highlight()')
            code_lines.append(f'            time.sleep(0.5)')
            code_lines.append(f'            page.locator("""{sel}""").fill("""{val}""")')
            code_lines.append(f'            results.append({{"status": "success", "message": "Typed \'{val}\' into {sel}"}})')

        elif action == "click":
            sel = params.get("selector")
            
            
            if sel == "#video-title":
                sel = "ytd-video-renderer:nth-of-type(1) #video-title"
                print("   [Fix] Applied YouTube Selector Fix")

            code_lines.append(f'            page.locator("""{sel}""").highlight()')
            code_lines.append(f'            time.sleep(0.5)')
            code_lines.append(f'            page.locator("""{sel}""").click()')
            code_lines.append(f'            results.append({{"status": "success", "message": "Clicked {sel}"}})')

        elif action == "press":
            key = params.get("key")
            code_lines.append(f'            page.keyboard.press("""{key}""")')
            code_lines.append(f'            results.append({{"status": "success", "message": "Pressed \'{key}\'"}})')

        elif action == "assert":
            check_type = params.get("type")
            value = params.get("value")
            if check_type == "title":
                code_lines.append(f'            expect(page).to_have_title("""{value}""", timeout=5000)')
                code_lines.append(f'            results.append({{"status": "success", "message": "Verified title: \'{value}\'"}})')

    code_lines.append("            print('   [Browser] Closing...')")
    code_lines.append("            browser.close()")
    code_lines.append("            return results")
    
    
    code_lines.append("        except Exception as e:")
    code_lines.append("            print(f'   [CRITICAL FAIL] Error: {e}')")
    code_lines.append("            try:")
    code_lines.append("                print(f'   [Debug Info] Current URL: {page.url}')")
    code_lines.append("                print(f'   [Debug Info] Page Title: {page.title()}')")
    code_lines.append("            except: pass")
    code_lines.append("            browser.close()")
    code_lines.append("            return [{'status': 'error', 'message': str(e)}]")

    return "\n".join(code_lines)