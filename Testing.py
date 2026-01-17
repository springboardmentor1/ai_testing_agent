from Agent.parser import convert_instruction
from Agent.generator import generate_script
from Agent.executor import run_test
from Agent.reporter import generate_report

instruction = "Open the page and verify hello message"

steps = convert_instruction(instruction)
script = generate_script(steps)

with open("generated_test.py", "w") as f:
    f.write(script)

status = run_test()
generate_report(status)

print("Test Status:", status)
