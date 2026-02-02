from instruction_parser import agent
from executor import execute_test

test_case = input("Enter test case: ")
parser_result = agent.invoke({"input": test_case})
playwright_json = parser_result["output"]

print("\nGenerated Playwright JSON:")
print(playwright_json)

execute_test(playwright_json, headless=False)



