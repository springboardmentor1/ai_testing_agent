
import subprocess
import sys
import time
from typing import Dict, List


def generate_adaptive_python_test(
    steps: List[Dict],
    adaptive_selectors: Dict = None
) -> str:

    """
    Generate Python test with:
    - Visible browser (headless=False) for demos
    - Adaptive selectors with fallbacks
    - Multi-site search support (Google, YouTube, Amazon)
    - Cookie consent handling
    - Slow motion for visibility
    """
    
    lines = []
    lines.append('"""\n')
    lines.append('Auto-generated Playwright test with adaptive selectors\n')
    lines.append('Browser: VISIBLE MODE for demonstration\n')
    lines.append('"""\n\n')
    
    lines.append('from playwright.sync_api import sync_playwright, expect, TimeoutError as PWTimeoutError\n')
    lines.append('import sys\n')
    lines.append('import time\n\n\n')
    
    # Add helper function for adaptive selector finding
    lines.append('def find_element_adaptive(page, selectors, element_name="element"):\n')
    lines.append('    """Try multiple selectors until one works"""\n')
    lines.append('    for selector in selectors:\n')
    lines.append('        try:\n')
    lines.append('            elem = page.locator(selector).first\n')
    lines.append('            elem.wait_for(state="visible", timeout=5000)\n')
    lines.append('            print(f"   Found {element_name} using: {selector}")\n')
    lines.append('            return elem\n')
    lines.append('        except:\n')
    lines.append('            continue\n')
    lines.append('    raise Exception(f"Could not find {element_name} with any selector")\n\n\n')
    
    lines.append('def handle_cookie_consent(page):\n')
    lines.append('    """Handle common cookie consent popups"""\n')
    lines.append('    consent_selectors = [\n')
    lines.append('        "button:has-text(\\"Accept all\\")",\n')
    lines.append('        "button:has-text(\\"Accept\\")",\n')
    lines.append('        "button:has-text(\\"I agree\\")",\n')
    lines.append('        "[id*=\\"accept\\"]",\n')
    lines.append('        "[class*=\\"accept\\"]"\n')
    lines.append('    ]\n')
    lines.append('    for selector in consent_selectors:\n')
    lines.append('        try:\n')
    lines.append('            page.locator(selector).click(timeout=3000)\n')
    lines.append('            print("   Accepted cookies")\n')
    lines.append('            return True\n')
    lines.append('        except:\n')
    lines.append('            continue\n')
    lines.append('    return False\n\n\n')
    
    lines.append('def run_test():\n')
    lines.append('    """Execute the test with error handling"""\n')
    lines.append('    print(" Starting test execution in VISIBLE MODE...")\n')
    lines.append('    \n')
    lines.append('    with sync_playwright() as p:\n')
    lines.append('        # Launch VISIBLE browser with slow motion\n')
    lines.append('        browser = p.chromium.launch(\n')
    lines.append('            headless=False,  # Visible for demo\n')
    lines.append('            slow_mo=900       # Slow motion effect\n')
    lines.append('        )\n')
    lines.append('        context = browser.new_context(\n')
    lines.append('            viewport={"width": 1280, "height": 720},\n')
    lines.append('            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\n')
    lines.append('        )\n')
    lines.append('        page = context.new_page()\n')
    lines.append('        \n')
    lines.append('        try:\n')
    
    # Generate steps with error handling
    for i, step in enumerate(steps, 1):
        action = step.get("action", "")
        
        lines.append(f'            print("\\n  Step {i}: {action}")\n')
        lines.append('            try:\n')
        
        if action == "OPEN_BROWSER":
            url = step.get("url", "")
            if not url.startswith(("http://", "https://")):
                url = f"https://{url}"
            
            lines.append(f'                print("   Opening {url}...")\n')
            lines.append(f'                page.goto("{url}", wait_until="domcontentloaded", timeout=30000)\n')
            lines.append('                page.wait_for_load_state("domcontentloaded")\n')
            lines.append('                time.sleep(2)  # Let page stabilize\n')
            lines.append('                \n')
            lines.append('                # Handle cookie consent\n')
            lines.append('                handle_cookie_consent(page)\n')
            lines.append('                \n')
            lines.append('                print("   Page loaded")\n')
        
        elif action == "SEARCH":
            query = step.get("query", "")
            query = query.replace('"', '\\"')
            
            lines.append(f'                print("   Searching for: {query}")\n')
            lines.append('                \n')
            lines.append('                # Click somewhere to activate page\n')
            lines.append('                page.mouse.click(300, 300)\n')
            lines.append('                time.sleep(1)\n')
            lines.append('                \n')
            lines.append('                # Detect site and use appropriate search\n')
            lines.append('                current_url = page.url.lower()\n')
            lines.append('                \n')
            
            # GOOGLE
            lines.append('                if "google." in current_url:\n')
            lines.append('                    print("   Google search detected")\n')
            lines.append('                    search_selectors = [\n')
            lines.append('                        "textarea[name=\\"q\\"]",\n')
            lines.append('                        "input[name=\\"q\\"]",\n')
            lines.append('                        "input[type=\\"search\\"]"\n')
            lines.append('                    ]\n')
            lines.append('                    search_box = find_element_adaptive(page, search_selectors, "Google search box")\n')
            lines.append(f'                    search_box.fill("{query}")\n')
            lines.append('                    page.keyboard.press("Enter")\n')
            lines.append('                \n')
            
            # YOUTUBE
            lines.append('                elif "youtube.com" in current_url:\n')
            lines.append('                    print("   YouTube search detected")\n')
            lines.append('                    page.wait_for_selector("input[name=\\"search_query\\"]", timeout=30000)\n')
            lines.append('                    page.click("input[name=\\"search_query\\"]")\n')
            lines.append(f'                    page.fill("input[name=\\"search_query\\"]", "{query}")\n')
            lines.append('                    page.keyboard.press("Enter")\n')
            lines.append('                \n')
            
            # AMAZON
            lines.append('                elif "amazon." in current_url:\n')
            lines.append('                    print("   Amazon search detected")\n')
            lines.append('                    amazon_selectors = [\n')
            lines.append('                        "#twotabsearchtextbox",\n')
            lines.append('                        "input[type=\\"text\\"][name=\\"field-keywords\\"]"\n')
            lines.append('                    ]\n')
            lines.append('                    search_box = find_element_adaptive(page, amazon_selectors, "Amazon search")\n')
            lines.append(f'                    search_box.fill("{query}")\n')
            lines.append('                    page.keyboard.press("Enter")\n')
            lines.append('                \n')
            
            # FALLBACK
            lines.append('                else:\n')
            lines.append('                    print("    Generic search - trying common selectors")\n')
            lines.append('                    generic_selectors = [\n')
            lines.append('                        "input[type=\\"search\\"]",\n')
            lines.append('                        "input[name*=\\"search\\"]",\n')
            lines.append('                        "input[placeholder*=\\"Search\\"]",\n')
            lines.append('                        "[data-testid*=\\"search\\"]"\n')
            lines.append('                    ]\n')
            lines.append('                    search_box = find_element_adaptive(page, generic_selectors, "search box")\n')
            lines.append(f'                    search_box.fill("{query}")\n')
            lines.append('                    page.keyboard.press("Enter")\n')
            lines.append('                \n')
            lines.append('                page.wait_for_load_state("networkidle", timeout=15000)\n')
            lines.append('                time.sleep(3)  # Let results load\n')
            lines.append('                print("   Search completed")\n')
        
        elif action == "CLICK":
            selector = step.get("selector", "")
            description = step.get("description", "element")
            
            lines.append(f'                print("   Clicking: {description}")\n')
            lines.append(f'                page.locator("{selector}").wait_for(state="visible", timeout=10000)\n')
            lines.append(f'                page.locator("{selector}").click()\n')
            lines.append('                time.sleep(2)\n')
            lines.append('                print("   Clicked")\n')
        
        elif action == "TYPE":
            selector = step.get("selector", "")
            value = step.get("value", "")
            value = value.replace('"', '\\"')
            
            lines.append(f'                print("  ⌨  Typing...")\n')
            lines.append(f'                page.locator("{selector}").wait_for(state="visible", timeout=10000)\n')
            lines.append(f'                page.locator("{selector}").click()\n')
            lines.append(f'                page.locator("{selector}").fill("{value}")\n')
            lines.append('                time.sleep(1)\n')
            lines.append('                print("   Typed")\n')
        
        elif action == "CHECK_LOGIN":
            expected = step.get("expected", False)
            
            lines.append(f'                print("   Checking login status (expected: {expected})")\n')
            lines.append('                logout_selectors = [\n')
            lines.append('                    "a[href*=\\"logout\\"]",\n')
            lines.append('                    "button:has-text(\\"Sign Out\\")",\n')
            lines.append('                    "button:has-text(\\"Log Out\\")",\n')
            lines.append('                    "[data-testid*=\\"user\\"]",\n')
            lines.append('                    ".user-menu"\n')
            lines.append('                ]\n')
            lines.append('                is_logged_in = False\n')
            lines.append('                for selector in logout_selectors:\n')
            lines.append('                    try:\n')
            lines.append('                        page.locator(selector).wait_for(state="visible", timeout=3000)\n')
            lines.append('                        is_logged_in = True\n')
            lines.append('                        print(f"   Login detected via: {selector}")\n')
            lines.append('                        break\n')
            lines.append('                    except:\n')
            lines.append('                        continue\n')
            
            if expected:
                lines.append('                assert is_logged_in, "Expected to be logged in"\n')
            else:
                lines.append('                assert not is_logged_in, "Expected to be logged out"\n')
            
            lines.append('                print("   Login check passed")\n')
        
        elif action == "WAIT":
            duration = step.get("duration", 3000)
            lines.append(f'                print("    Waiting {duration}ms")\n')
            lines.append(f'                page.wait_for_timeout({duration})\n')
        
        elif action == "SCREENSHOT":
            filename = step.get("filename", "screenshot.png")
            lines.append(f'                print("   Taking screenshot: {filename}")\n')
            lines.append(f'                page.screenshot(path="screenshots/{filename}")\n')
            lines.append('                print("   Screenshot saved")\n')
        
        # Close try block for step
        lines.append('            except Exception as step_error:\n')
        lines.append(f'                print(f"    Step {i} error: {{step_error}}")\n')
        lines.append('                page.screenshot(path="screenshots/error_step_{i}.png")\n')
        lines.append('                raise\n')
        lines.append('            \n')
    
    # Success case
    lines.append('            print("\\n All steps PASSED!")\n')
    lines.append('            print(" Browser stays open for 20 seconds for inspection")\n')
    lines.append('            time.sleep(20)\n')
    lines.append('            browser.close()\n')
    lines.append('            return 0\n')
    lines.append('            \n')
    
    # Error handling
    lines.append('        except AssertionError as e:\n')
    lines.append('            print(f"\\n Assertion failed: {e}")\n')
    lines.append('            page.screenshot(path="screenshots/assertion_failed.png")\n')
    lines.append('            time.sleep(20)\n')
    lines.append('            browser.close()\n')
    lines.append('            return 1\n')
    lines.append('            \n')
    lines.append('        except PWTimeoutError as e:\n')
    lines.append('            print(f"\\n  Timeout: {e}")\n')
    lines.append('            page.screenshot(path="screenshots/timeout_error.png")\n')
    lines.append('            time.sleep(20)\n')
    lines.append('            browser.close()\n')
    lines.append('            return 1\n')
    lines.append('            \n')
    lines.append('        except Exception as e:\n')
    lines.append('            print(f"\\n Test FAILED: {e}")\n')
    lines.append('            page.screenshot(path="screenshots/test_error.png")\n')
    lines.append('            time.sleep(20)\n')
    lines.append('            browser.close()\n')
    lines.append('            return 1\n')
    lines.append('\n\n')
    lines.append('if __name__ == "__main__":\n')
    lines.append('    exit_code = run_test()\n')
    lines.append('    sys.exit(exit_code)\n')
    
    return "".join(lines)


def execute_python_test(test_file_path: str, timeout: int = 180) -> Dict:
    """
    Execute Python test with longer timeout for visible mode
    
    Args:
        test_file_path: Path to .py test file
        timeout: Maximum execution time (180s for visible mode)
        
    Returns:
        Execution results dictionary
    """
    
    print(f"\n🎭 Executing: {test_file_path}")
    print("👁️  Running in VISIBLE MODE - Browser will appear")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file_path],
            stdout=sys.stdout,  # Live output to terminal
            stderr=sys.stderr,  # Live errors to terminal
            timeout=timeout
        )
        
        return {
            "status": "passed" if result.returncode == 0 else "failed",
            "output": "Live output shown in terminal (visible mode)",
            "errors": "",
            "return_code": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "output": "",
            "errors": f"Test timed out after {timeout} seconds",
            "return_code": -1
        }
    
    except Exception as e:
        return {
            "status": "error",
            "output": "",
            "errors": str(e),
            "return_code": -1
        }