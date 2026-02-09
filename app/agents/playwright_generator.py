def generate_playwright_script(actions):
    lines = []

    lines.append("from playwright.sync_api import sync_playwright")
    lines.append("")
    lines.append("def run_test():")
    lines.append("    with sync_playwright() as p:")
    lines.append("        browser = p.chromium.launch(headless=False)")
    lines.append("        page = browser.new_page()")
    lines.append("")

    lines.append("        GENERIC_SEARCH_SELECTORS = [")
    lines.append("            \"textarea[name='q']\",")
    lines.append("            \"input[name='q']\",")
    lines.append("            \"input[type='search']\",")
    lines.append("            \"input\"")
    lines.append("        ]")
    lines.append("")

    current_site = ""

    for step in actions:
        action = step["action"]

        # ---------- OPEN ----------
        if action == "open":
            target = step["target"]

            if target == "google":
                url = "https://www.google.com"
                current_site = "google"
            elif target == "amazon":
                url = "https://www.amazon.in"
                current_site = "amazon"
            elif target == "flipkart":
                url = "https://www.flipkart.com"
                current_site = "flipkart"
            elif target == "test":
                url = "http://127.0.0.1:5000/test.html"
                current_site = "test"
            else:
                url = target
                current_site = "generic"

            lines.append(f"        page.goto('{url}', timeout=60000)")
            lines.append("        page.wait_for_load_state('domcontentloaded')")
            lines.append("")

        # ---------- SEARCH ----------
        elif action == "search":
            query = step["value"]

            if current_site == "amazon":
                lines.append("        search_box = 'input#twotabsearchtextbox'")
            elif current_site == "flipkart":
                lines.append("        search_box = 'input[name=\"q\"]'")
            elif current_site == "google":
                lines.append("        search_box = 'textarea[name=\"q\"]'")
            else:
                lines.append("        search_box = None")

            lines.append("        if search_box:")
            lines.append(f"            page.fill(search_box, '{query}')")
            lines.append("        else:")
            lines.append("            for sel in GENERIC_SEARCH_SELECTORS:")
            lines.append("                try:")
            lines.append("                    page.wait_for_selector(sel, timeout=3000)")
            lines.append(f"                    page.fill(sel, '{query}')")
            lines.append("                    break")
            lines.append("                except:")
            lines.append("                    pass")

            lines.append("        page.keyboard.press('Enter')")

            # GUARANTEED HUMAN-VISIBLE PAUSE
            if current_site == "google":
                lines.append("        print('Waiting for Google results...')")
                lines.append("        page.wait_for_selector('#search', timeout=30000)")
                lines.append("        page.wait_for_timeout(8000)")
            else:
                lines.append("        page.wait_for_timeout(6000)")

            lines.append("        print('PAGE TITLE:', page.title())")
            lines.append("")

        # ---------- VERIFY (MANUAL LOCAL LOGIN) ----------
        elif action == "verify":
            lines.append("        print('Please enter username/password manually and click Login')")
            lines.append("        page.wait_for_selector('#result', timeout=60000)")
            lines.append("        result_text = page.text_content('#result')")
            lines.append("        print('VERIFY RESULT:', result_text)")
            lines.append("        if 'Success' not in result_text:")
            lines.append("            raise Exception('Verification failed')")
            lines.append("        page.wait_for_timeout(3000)")
            lines.append("")

    lines.append("        print('TEST FINISHED')")
    lines.append("        browser.close()")
    lines.append("")
    lines.append("if __name__ == '__main__':")
    lines.append("    run_test()")

    return '\n'.join(lines)
