from playwright.sync_api import sync_playwright

# ================= FORM TEST (MANUAL UI INPUT) =================
def run_form_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("\n--- FORM TEST STARTED ---")

        pass_count = 0
        fail_count = 0

        try:
            # Open local HTML form
            page.goto(
                "file:///C:/Users/batch_utw5sck/OneDrive/Desktop/AI_AGENT/playwright_automation/form.html"
            )
            print("Form opened")
            print("Human must type name manually in the UI")
            input("After typing, press ENTER here...")

            # READ WHAT HUMAN TYPED
            typed_name = page.locator("#username").input_value()
            print(f"Name entered in form: {typed_name}")

            # CLICK LOGIN (automation)
            page.locator("#login").click()

            # ASSERT RESULT
            result = page.locator("#result")
            result.wait_for(timeout=5000)

            if result.is_visible():
                print("ASSERT PASS: Login message displayed")
                pass_count += 1
            else:
                print("ASSERT FAIL: Login message not displayed")
                fail_count += 1

        except Exception as e:
            print("ERROR:", e)
            fail_count += 1

        print("\n--- FORM TEST SUMMARY ---")
        print(f"Passed Assertions: {pass_count}")
        print(f"Failed Assertions: {fail_count}")

        input("\nPress ENTER to close browser...")
        browser.close()


# ================= GOOGLE TEST (FULL AUTOMATION) =================
def run_google_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("\n--- GOOGLE TEST STARTED ---")

        pass_count = 0
        fail_count = 0

        try:
            # OPEN GOOGLE
            page.goto("https://www.google.com", timeout=20000)
            print("Google opened")

            # PLAYWRIGHT TYPES (NO HUMAN)
            page.fill("textarea[name='q']", "amazon")
            print("Playwright typed: amazon")

            page.keyboard.press("Enter")
            page.wait_for_load_state("networkidle")

            current_url = page.url.lower()

            # ASSERTION 1 (REAL ASSERTION)
            if "amazon" in current_url:
                print("ASSERT PASS: Amazon related page opened")
                pass_count += 1
            else:
                print("ASSERT FAIL: Amazon page not opened")
                fail_count += 1

        except Exception as e:
            print("ERROR:", e)
            fail_count += 1

        print("\n--- GOOGLE TEST SUMMARY ---")
        print(f"Passed Assertions: {pass_count}")
        print(f"Failed Assertions: {fail_count}")

        input("\nPress ENTER to close browser...")
        browser.close()
