from app.agents.baseline_agent import agent_app
import json

#  test case 
test_input = {"input": "Open Wikipedia.org, find the search bar, type 'AI Agents', and hit Enter."}

print(f"User Input: {test_input['input']}")
print("-" * 50)

try:
    # Run the Agent
    result = agent_app.invoke(test_input)
    
    # Shows the Result
    commands = result.get('parsed_commands', [])
    print(f"\nSUCCESS! AI Generated {len(commands)} Steps:\n")
    print(json.dumps(commands, indent=2))

except Exception as e:
    print(f"Test Failed: {e}")