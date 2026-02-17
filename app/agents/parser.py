
def convert_instruction(text):
    return [
        {"action": "goto", "value": "http://127.0.0.1:5000"},
        {"action": "assert", "selector": "h1", "value": "Hello Flask"}
    ]