import asyncio
from agents.baseline_agent import agent

async def run_test_case(instruction):
    """
    Triggers the LangGraph agent for a specific natural language instruction.
    Validates Interpretation (Milestone 2) and Browser Execution (Milestone 3).
    """
    print(f"\n{'='*60}")
    print(f" STARTING TEST: '{instruction}'")
    print(f"{'='*60}")
    
    try:
        
        result = await agent.ainvoke({"input": instruction})
        
       
        cmd = result.get("parsed_command", {})
        print(f"\n1.  LLM INTERPRETATION:")
        print(f"   - Action: {cmd.get('action')}")
        print(f"   - Target: {cmd.get('target')}")
        print(f"   - Value:  {cmd.get('value')}")
        
     
        print(f"\n2.  EXECUTION REPORT:")
        print(f"   {result.get('output')}")
        
    except Exception as e:
        print(f"\n SCRIPT ERROR: {e}")

async def main():
    """
    Milestone 3 Unified Test Suite
    Demonstrates dynamic environment switching between local and live web.
    """
    print("  Initializing Milestone 3 Unified Test Suite...")


    print("\n--- Phase 1: Local Static HTML Validation ---")
    

    await run_test_case("Navigate to index.html")

    await run_test_case("Click on the Login")


    await run_test_case("Type 'Intern_2026' into the Enter Username field")

    print("\n--- Phase 2: Live Web Domain Validation ---")

    await run_test_case("Navigate to google.com")

    await run_test_case("Search for 'Python Playwright automation' in the search bar")

    print(f"\n{'='*60}")
    print("🏁 ALL MILESTONE 3 TESTS COMPLETED")
    print(f"{'='*60}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest suite interrupted by user.")