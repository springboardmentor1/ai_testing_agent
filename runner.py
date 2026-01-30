from playwright.sync_api import sync_playwright
from codegen import generate_action
from steps import steps

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1200)

        page = browser.new_page()

        for step in steps:
            code = generate_action(step)
            exec(code)

        browser.close()
        print("TEST EXECUTED SUCCESSFULLY")

if __name__ == "__main__":
    run_test()
