from instruction_parser import agent
from executor import execute_test

#Take test case input
test_case = input("Enter test case: ")

#Generate Playwright steps using AI
parser_result = agent.invoke({"input": test_case})
playwright_json = parser_result["output"]

print("\nGenerated Playwright JSON:")
print(playwright_json)

#Execute test and capture report
report = execute_test(playwright_json, test_case, headless=False)

#Display final report
print("\nFINAL TEST REPORT")
print("-------------------------")
print(f"Test Case: {report['test_case']}")
print(f"Status: {report['status']}")
print(f"Steps Executed: {report['steps_executed']}")
print(f"Execution Time: {report['execution_time_sec']} seconds")
print(f"Timestamp: {report['timestamp']}")

if report["error"]:
    print(f"Error: {report['error']}")
