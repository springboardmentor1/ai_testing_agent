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

'''
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
        browser.close()'''
from playwright.sync_api import sync_playwright
from codegen import generate_action
import time
from datetime import datetime


#Handle Google consent popup
def handle_google_consent(page):
    try:
        for frame in page.frames:
            try:
                frame.click("button:has-text('Accept all')", timeout=2000)
                time.sleep(1)
                return
            except:
                pass
    except:
        pass


#Reporting function
def create_report(test_case, steps, status, error, start_time):
    end_time = time.time()

    return {
        "test_case": test_case,
        "status": status,
        "steps_executed": len(steps),
        "error": str(error) if error else None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "execution_time_sec": round(end_time - start_time, 2)
    }


#Main executor
def execute_test(test_json, test_case="", headless=False):
    start_time = time.time()
    status = "PASS"
    error = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=800)
        page = browser.new_page()

        try:
            for step in test_json["steps"]:
                code = generate_action(step)
                print("[EXECUTING]", code)

                try:
                    exec(code)
                except Exception as step_error:
                    #Screenshot on failure
                    page.screenshot(path="error_screenshot.png")
                    raise step_error

                # Handle Google consent after navigation
                if step["action"] == "goto" and "google.com" in step.get("url", ""):
                    handle_google_consent(page)

                time.sleep(0.5)

            print("TEST EXECUTED SUCCESSFULLY")

        except Exception as e:
            status = "FAIL"
            error = e
            print("TEST FAILED:", e)

        finally:
            browser.close()

    #Generate report
    report = create_report(
        test_case,
        test_json["steps"],
        status,
        error,
        start_time
    )

    return report
