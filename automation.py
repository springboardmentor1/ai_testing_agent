from playwright.sync_api import sync_playwright
import time
import os

def run_test(test_type, search_text=None):
    start_time = time.time()

    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    screenshot_path = f"screenshots/{test_type.replace(' ', '_')}.png"

    status = "FAIL"
    details = ""

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            if test_type == "Google":
                page.goto("https://www.google.com")

                if search_text:
                    page.fill("input[name='q']", search_text)
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(3000)

            elif test_type == "YouTube":
                page.goto("https://www.youtube.com")

                if search_text:
                    page.fill("input#search", search_text)
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(4000)

            elif test_type == "Amazon":
                page.goto("https://www.amazon.in")

                if search_text:
                    page.fill("input#twotabsearchtextbox", search_text)
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(3000)

            elif test_type == "GitHub":
                page.goto("https://www.github.com")

            page.screenshot(path=screenshot_path)

            status = "PASS"
            details = f"{test_type} automation executed successfully."
            browser.close()

    except Exception as e:
        details = str(e)

    execution_time = round(time.time() - start_time, 2)

    return status, details, execution_time, screenshot_path
