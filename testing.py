import asyncio
from app.agents.baseline_agent import agent

async def run_test_case(instruction):
    print(f"\n{'='*60}")  
    print(f" STARTING TEST: '{instruction}'")
    print(f"\n{'='*60}")  
    
    try:
        result = await agent.ainvoke({"input": instruction})
        commands = result.get("parsed_command", [])

        print(f"\n1.  LLM INTERPRETATION:")
        for i, cmd in enumerate(commands, 1):
         print(f" Step {i}:")  
         print(f"   - Action: {cmd.get('action')}")
         print(f"   - Target: {cmd.get('target')}")
         print(f"   - Value:  {cmd.get('value')}")
        
        print(f"\n2.  EXECUTION REPORT:")
        print(f"   {result.get('output')}")
        
    except Exception as e:
        print(f"\n SCRIPT ERROR: {e}")

async def main():
    """
    Milestone 3 Test Suite

    This suite performs:
    - Phase 1: Validation of local static HTML interactions
    - Phase 2: Automation on live web domains (e.g., YouTube)

    Designed to test dynamic environment switching and selector robustness.
    """

    print("📂 Starting Milestone 3: Unified Test Execution Begins")

    print("🧱 Phase 1: Validating Local Static HTML")
    
    await run_test_case("Navigate to index.html, type 'psingh01' into the username field,"
          "type 'psingh123' into the password field, and click on the login button")


    print("▶️ Phase 2: External Web Automation – YouTube Scenario")

    await run_test_case("Navigate to youtube.com, Search for 'n8n automation' in the search bar")

    print(f"\n{'='*60}") 
    print("✅ All Milestone 3 Tests Completed Successfully.")
    print(f"\n{'='*60}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest suite interrupted by user.")