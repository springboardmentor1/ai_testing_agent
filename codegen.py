def generate_action(step):
    action = step["action"]

    if action == "goto":
        return f'page.goto("{step["url"]}")'

    elif action == "fill":
        return f'page.fill("{step["selector"]}", "{step["value"]}")'

    elif action == "click":
        return f'page.click("{step["selector"]}")'

    elif action == "assert_visible":
        return (
            f'page.wait_for_selector("{step["selector"]}", '
            f'state="visible", timeout=5000)'
        )

    else:
        raise ValueError(f"Unsupported action: {action}")


