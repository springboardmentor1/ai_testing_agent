def generate_script(actions):
    code = [
        "from playwright.sync_api import sync_playwright",
        "",
        "def test():",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=True)",
        "        page = browser.new_page()"
    ]

    for a in actions:
        if a["action"] == "goto":
            code.append(f"        page.goto('{a['value']}')")
        elif a["action"] == "assert":
            code.append(
                f"        assert page.inner_text('{a['selector']}') == '{a['value']}'"
            )

    code.append("        browser.close()")
    code.append("")
    code.append("test()")

    return "\n".join(code)
