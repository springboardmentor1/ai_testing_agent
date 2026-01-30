steps = [
    {"action": "goto", "url": "http://localhost:5000"},
    {"action": "fill", "selector": "#username", "value": "user"},
    {"action": "fill", "selector": "#password", "value": "wrong"},
    {"action": "click", "selector": "#loginBtn"},
    {"action": "assert_visible", "selector": "#error"}
]
