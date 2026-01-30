def generate_action(step):
    action = step["action"]

    if action == "goto":
        return f'page.goto("{step["url"]}")'

    elif action == "fill":
        return f'page.fill("{step["selector"]}", "{step["value"]}")'

    elif action == "click":
        return f'page.click("{step["selector"]}")'

    elif action == "assert_text":
        return f'assert page.text_content("{step["selector"]}") == "{step["value"]}"'

    elif action == "assert_visible":
        return f'assert page.is_visible("{step["selector"]}")'

    elif action == "assert_url":
        return f'assert page.url == "{step["value"]}"'

    else:
        raise ValueError(f"Unsupported action: {action}")
