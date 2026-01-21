# from agents.baseline_agent import agent

# if __name__ == "__main__":
#     result = agent.invoke({"input":"Hi there!"})
#     print(result)

# from agents.baseline_agent import agent

# if __name__ == "__main__":
#     # Test case 1: Navigation
#     result1 = agent.invoke({"input": "Navigate to google.com"})
#     print(f"Test 1 Results: {result1['parsed_command']}")

#     # Test case 2: Clicking
#     result2 = agent.invoke({"input": "Click the Submit button"})
#     print(f"Test 2 Results: {result2['parsed_command']}")


from app.agents.baseline_agent import agent
import json

def test_agent(instruction):
    print(f"\n--- Testing Instruction: '{instruction}' ---")
    try:
        
        result = agent.invoke({"input": instruction})
        
        
        print(f"1. Parsed Command: {result.get('parsed_command')}")
        
        
        print(f"2. Agent Output: {result.get('output')}")
        
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    # Test Case 1: Complex Navigation
    test_agent("Please go to the bing.com website immediately")

    # Test Case 2: Natural Language Action
    test_agent("Press the big blue login button at the top")

    # Test Case 3: Data Entry (Typing)
    test_agent("Type Testing123 into the password field")

    # Test Case 4: Verification (Milestone 2 Requirement)
    test_agent("Check if the message 'Welcome' is visible on the dashboard")