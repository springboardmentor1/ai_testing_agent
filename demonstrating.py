from playwright.sync_api import sync_playwright

def execute_test(steps, expected):
    logs = []

    with sync_playwright() as p:
        print(" Launching headless browser")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            for step in steps:
                action = step["action"]

                if action == "navigate":
                    print(f" Navigating to {step['target']}")
                    page.goto(step["target"])
                    page.wait_for_load_state("load")
                    logs.append("SUCCESS: Navigation completed")

                elif action == "fill":
                    print(f" Filling {step['target']}")
                    page.wait_for_selector(step["target"])
                    page.fill(step["target"], step["value"])
                    logs.append(f"SUCCESS: Filled {step['target']}")

                elif action == "press":
                    print(" Pressing ENTER")
                    page.keyboard.press(step["key"])
                    page.wait_for_load_state("networkidle")
                    logs.append("SUCCESS: Search executed")

                elif action == "click":
                    print("🖱 Clicking login button")
                    page.click(step["target"])
                    page.wait_for_selector("#msg")
                    msg = page.inner_text("#msg")

                    if expected == "success":
                        assert "Login Successful" in msg
                        logs.append("SUCCESS: Valid login confirmed")
                    else:
                        assert "Invalid Credentials" in msg
                        logs.append("SUCCESS: Invalid login detected")

            browser.close()
            return True, logs

        except Exception as e:
            browser.close()
            logs.append(f"ERROR: {e}")
            return False, logs
