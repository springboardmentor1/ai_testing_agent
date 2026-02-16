def parse_instruction(text):
    text = text.lower()
    actions = []

    # ---------- GOOGLE SEARCH ----------
    if "google" in text:
        actions.append({
            "action": "navigate",
            "target": "https://www.google.com"
        })

    if "search" in text and "amazon" in text:
        actions.append({
            "action": "fill",
            "target": "textarea[name='q'], input[name='q']",
            "value": "amazon"
        })
        actions.append({
            "action": "press",
            "key": "Enter"
        })

    # ---------- LOGIN ----------
    if "login" in text:
        actions.append({
            "action": "navigate",
            "target": "http://127.0.0.1:5000/login"
        })

        if "invalid" in text:
            actions.append({"action": "fill", "target": "#username", "value": "wrong"})
            actions.append({"action": "fill", "target": "#password", "value": "wrong"})
        else:
            actions.append({"action": "fill", "target": "#username", "value": "admin"})
            actions.append({"action": "fill", "target": "#password", "value": "1234"})

        actions.append({"action": "click", "target": "#loginBtn"})

    return actions
