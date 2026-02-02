'''from playwright.sync_api import sync_playwright
from codegen import generate_action
import time

def execute_test(test_json, headless=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=800)
        page = browser.new_page()

        for step in test_json["steps"]:
            code = generate_action(step)
            print("[EXECUTING]", code)
            exec(code)
            time.sleep(0.5)

        print("TEST EXECUTED SUCCESSFULLY")
        time.sleep(3)
        browser.close()'''


from playwright.sync_api import sync_playwright
from codegen import generate_action
import time

def handle_google_consent(page):
    try:
        page.click("button:has-text('Accept all')", timeout=3000)
        time.sleep(1)
    except:
        pass  


def execute_test(test_json, headless=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=800)
        page = browser.new_page()

        for step in test_json["steps"]:
            code = generate_action(step)
            print("[EXECUTING]", code)

            
            if "google.com" in page.url:
                handle_google_consent(page)

            exec(code)
            time.sleep(0.5)

        print("TEST EXECUTED SUCCESSFULLY")
        time.sleep(3)
        browser.close()
