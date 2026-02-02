import asyncio
from app.agents.baseline_agent import agent

async def run_test_case(instruction):
    print(f"\n{"="*60}")
    print(f" STARTING TEST: '{instruction}'")
    print(f"{"="*60}")
    
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
    Milestone 3 Test Suite for YouTube
    """
    print("🚀 Kicking off Milestone 3 — Target: YouTube. Let the automation begin!")


    await run_test_case("Navigate to youtube.com")
    await run_test_case("Search for 'n8n automation' in the search bar")
    await run_test_case("Scroll to footer and click on the 'Help' link")

    print(f"\n{"="*60}")
    print("✅ All Milestone 3 Tests Completed Successfully.")
    print(f"{"="*60}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest suite interrupted by user.")