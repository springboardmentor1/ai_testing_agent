from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com")

        # Wait for search box
        page.wait_for_selector("textarea[name='q']", timeout=15000)

        page.fill("textarea[name='q']", "mobiles")
        page.keyboard.press("Enter")

        print("🔐 If CAPTCHA appears, solve it manually.")
        print("⏳ Press ENTER in terminal after results load...")

        input()  # 👈 IMPORTANT: waits for human

        browser.close()

if __name__ == "__main__":
    run_test()
