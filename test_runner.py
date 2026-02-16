from app.agents.parser import parse_instruction
from app.agents.playwright_code_generator import map_actions
from app.agents.demonstrating import execute_test

def run_test(title, instruction, expected):
    print("\n" + "=" * 50)
    print(title)
    print("Instruction:", instruction)
    print("=" * 50)

    actions = parse_instruction(instruction)
    steps = map_actions(actions)
    status, logs = execute_test(steps, expected)

    for log in logs:
        print("✔", log) if "SUCCESS" in log else print("✖", log)

    print("\nRESULT:", "PASS" if status else "FAIL")


# -------- TEST CASE 1 --------
run_test(
    "TEST CASE 1 : GOOGLE SEARCH",
    "Open Google and search for Amazon",
    "success"
)

# -------- TEST CASE 2 --------
run_test(
    "TEST CASE 2 : VALID LOGIN",
    "Login using username and password",
    "success"
)

# -------- TEST CASE 3 --------
run_test(
    "TEST CASE 3 : INVALID LOGIN",
    "Login using invalid username and password",
    "fail"
)

print("\n" + "=" * 50)
print("ALL TESTS COMPLETED")
print("=" * 50)
