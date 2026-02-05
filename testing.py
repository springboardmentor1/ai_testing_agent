import os
from app.agents.baseline_agent import agent_app

print("==================================================")
print(" 🤖 AI TESTING AGENT - VISUAL DEMO")
print("==================================================\n")

test_cases = [
    {
        "name": "Test 1: Navigate to Google",
        "input": "Navigate to https://www.google.com and verify the title is 'Google'"
    },
    {
        "name": "Test 2: Search for AI (Wikipedia)",
        "input": "Open https://www.wikipedia.org, type 'Artificial Intelligence' into the search bar, hit Enter, and verify the title is 'Artificial intelligence - Wikipedia'"
    },
    {
        "name": "Test 3: Secure Login Simulation",
        "input": "Open https://practicetestautomation.com/practice-test-login/, type 'student' into the username field, type 'Password123' into the password field, click the Submit button, and verify the text 'Logged In Successfully' exists"
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n🔹 RUNNING: {test['name']}")
    print(f"   Instruction: \"{test['input']}\"") 
    print("-" * 50)

    try:
        print("   ⏳ Launching Browser...")
        # Run the Agent
        result = agent_app.invoke({"input": test['input']})
        
        # Print Execution Logs
        print("   📝 Execution Log:")
        for log in result['execution_logs']:
            if "SUCCESS" in log:
                print(f"      ✅ {log}")
            elif "ERROR" in log:
                print(f"      ❌ {log}")
            else:
                print(f"      ℹ️ {log}")

    except Exception as e:
        print(f"      🚨 CRITICAL FAILURE: {e}")
    
    print("-" * 50)
    print("   [End of Test Case]\n")

print("==================================================")
print("  DEMO COMPLETED")
print("==================================================")