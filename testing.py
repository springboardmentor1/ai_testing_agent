from app.agents.parser import convert_instruction
from app.agents.generator import generate_script
from app.agents.executor import run_test
from app.agents.reporter import generate_report

instruction = "Open the page and verify hello message"

steps = convert_instruction(instruction)
script = generate_script(steps)

with open("generated_test.py", "w") as f:
    f.write(script)

status = run_test()
generate_report(status)

print("Test Status:", status)
import asyncio
from app.agents.baseline_agent import agent

async def run_test_case(instruction):
    print("\n" + "=" * 60)
    print(f"TEST: {instruction}")
    print("=" * 60)

    result = await agent.ainvoke({"input": instruction})

    cmd = result.get("parsed_command", {})
    print("\nLLM PARSED:")
    print(cmd)

    print("\nEXECUTION RESULT:")
    print(result.get("output"))

async def main():
    await run_test_case("Navigate to index.html")
    await run_test_case("Click Login")
    await run_test_case("Type 'Intern_2026' into Enter Username field")
    await run_test_case("Navigate to google.com")
    await run_test_case("Search for Playwright automation")

if __name__ == "__main__":
    asyncio.run(main())

print("Test Status:", status)
