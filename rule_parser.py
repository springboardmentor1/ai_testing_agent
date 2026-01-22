def rule_based_parser(text: str):
    text = text.lower()
    actions = []

    # Rule 1: Open Google
    if "open google" in text:
        actions.append({
            "action": "open_browser",
            "target": "https://www.google.com"
        })

    # Rule 2: Search for something
    if "search for" in text:
        query = text.split("search for")[-1].strip()
        actions.append({
            "action": "search",
            "engine": "google",
            "query": query
        })

    return actions
