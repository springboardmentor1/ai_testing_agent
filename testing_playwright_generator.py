from app.agents.playwright_generator import generate_playwright_script

actions = [
    {"action": "open", "target": "https://www.google.com", "value": ""},
    {"action": "type", "target": "textarea[name='q']", "value": "mobiles"}
]

script = generate_playwright_script(actions)
print(script)
