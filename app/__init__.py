def generate_playwright_script(actions):
    """
    Converts structured actions into a runnable Playwright Python script
    """

    lines = []

    # Script Header
    lines.append("from playwright.sync_api import sync_playwright")
    lines.append("")
    lines.append("def run_test():")
    lines.append("    with sync_playwright() as p:")
    lines.append("        browser = p.chromium.launch(headless=True)")
    lines.append("        page = browser.new_page()")

    # Convert each action
    for step in actions:
        action = step["action"]
        target = step["target"]
        value = step["value"]

        if action == "open":
            lines.append(f"        page.goto('{target}')")

        elif action == "click":
            lines.append(f"        page.click('{target}')")

        elif action == "type":
            lines.append(f"        page.fill('{target}', '{value}')")

        elif action == "assert_text":
            lines.append(
                f"        assert '{value}' in page.inner_text('{target}')"
            )

    lines.append("        browser.close()")
    lines.append("")
    lines.append("if __name__ == '__main__':")
    lines.append("    run_test()")

    return "\n".join(lines)
