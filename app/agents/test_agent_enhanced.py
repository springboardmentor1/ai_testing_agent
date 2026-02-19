"""
Enhanced Test Agent with Error Handling & Adaptive DOM Mapping
Milestone 4 Complete Implementation
"""


from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from app.config.llm import call_llm
import json


class TestState(TypedDict):
    """Complete state with error handling"""
    # Input
    user_instruction: str
    
    # Parsing state
    parsed_steps: list
    parsing_status: str
    parsing_errors: str
    
    # Browser state
    browser_open: bool
    current_url: str
    logged_in: bool
    
    # Code generation state
    generated_code: str
    code_file_path: str
    
    # Execution state
    execution_status: str
    execution_output: str
    execution_errors: str
    retry_count: int
    
    # Final result
    test_passed: bool


# Adaptive selector mapping for common elements
ADAPTIVE_SELECTORS = {
    "search_box": [
        'textarea[name="q"]',
        'input[name="q"]',
        'input[type="search"]',
        'textarea[title*="Search"]',
        'input[title*="Search"]',
        '[data-testid*="search"]',
        '#search',
        '.search-input'
    ],
    "login_button": [
        'button:has-text("Log in")',
        'button:has-text("Sign in")',
        'a:has-text("Log in")',
        '[data-testid*="login"]',
        '#login-button',
        '.login-btn'
    ],
    "logout_indicator": [
        'a[href*="logout"]',
        'button:has-text("Sign Out")',
        'button:has-text("Log Out")',
        '[data-testid*="user"]',
        '[data-testid*="profile"]',
        '.user-menu'
    ]
}


ENHANCED_PARSER_PROMPT = """
Convert user instruction into STRICT JSON test steps with ERROR HANDLING.

Available actions:
- OPEN_BROWSER (url: string)
- SEARCH (query: string) 
- CLICK (selector: string, description: string)
- TYPE (selector: string, value: string, description: string)
- CHECK_LOGIN (expected: bool)
- WAIT (duration: number)
- SCREENSHOT (filename: string)
- ASSERT_TEXT (selector: string, text: string)
- RETRY (action: object, max_attempts: number)

Output ONLY valid JSON: {{"steps": [...]}}

Examples:

Input: "open browser search for python tutorial"
Output:
{{
  "steps": [
    {{"action": "OPEN_BROWSER", "url": "google.com"}},
    {{"action": "SEARCH", "query": "python tutorial"}}
  ]
}}

Input: "go to github check if logged in take screenshot"
Output:
{{
  "steps": [
    {{"action": "OPEN_BROWSER", "url": "github.com"}},
    {{"action": "CHECK_LOGIN", "expected": false}},
    {{"action": "SCREENSHOT", "filename": "github.png"}}
  ]
}}

User instruction: {instruction}
Output (JSON only):
"""


def parse_with_error_handling(state: TestState) -> TestState:
    """Parse with retry logic"""
    print("\n [Node 1] Parsing with error handling...")
    
    prompt = ENHANCED_PARSER_PROMPT.format(instruction=state["user_instruction"])
    
    for attempt in range(3):
        try:
            raw = call_llm(prompt)
            raw = raw.strip()
            
            # Clean markdown
            if raw.startswith("```"):
                lines = raw.split('\n')
                raw = '\n'.join(lines[1:-1])
                if raw.startswith('json'):
                    raw = raw[4:].strip()
            
            parsed = json.loads(raw)
            
            if "steps" in parsed and isinstance(parsed["steps"], list):
                print(f"✅ Parsed {len(parsed['steps'])} steps (attempt {attempt + 1})")
                
                return {
                    **state,
                    "parsed_steps": parsed["steps"],
                    "parsing_status": "success",
                    "parsing_errors": "",
                    "browser_open": False,
                    "current_url": "",
                    "logged_in": False,
                    "retry_count": 0
                }
        except json.JSONDecodeError as e:
            print(f"  Parsing attempt {attempt + 1} failed: {e}")
            continue
    
    print("❌ Parsing failed after 3 attempts")
    return {
        **state,
        "parsed_steps": [],
        "parsing_status": "failed",
        "parsing_errors": "Could not parse instruction after 3 attempts"
    }


def track_browser_state(state: TestState) -> TestState:
    """Track browser state predictions"""
    print("\n🔍 [Node 2] Tracking browser state...")
    
    browser_open = False
    current_url = ""
    logged_in = False
    
    for step in state["parsed_steps"]:
        action = step.get("action")
        
        if action == "OPEN_BROWSER":
            browser_open = True
            url = step.get("url", "")
            if not url.startswith("http"):
                url = f"https://{url}"
            current_url = url
        
        elif action == "CHECK_LOGIN":
            expected = step.get("expected", False)
            logged_in = expected
    
    return {
        **state,
        "browser_open": browser_open,
        "current_url": current_url,
        "logged_in": logged_in
    }


def generate_adaptive_code(state: TestState) -> TestState:
    """Generate code with adaptive selectors"""
    print("\n [Node 3] Generating code with adaptive DOM mapping...")
    
    from app.executor.python_executor_enhanced import generate_adaptive_python_test
    
    code = generate_adaptive_python_test(state["parsed_steps"], ADAPTIVE_SELECTORS)
    
    print(f"✅ Generated {len(code.split(chr(10)))} lines with error handling")
    
    return {
        **state,
        "generated_code": code
    }


def save_code(state: TestState) -> TestState:
    """Save code to file"""
    print("\n [Node 4] Saving test file...")
    
    import os
    from datetime import datetime
    
    test_dir = "app/generated_tests"
    os.makedirs(test_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_{timestamp}.py"
    filepath = os.path.join(test_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(state["generated_code"])
    
    print(f"✅ Saved to: {filepath}")
    
    return {
        **state,
        "code_file_path": filepath
    }


def execute_with_retry(state: TestState) -> TestState:
    """Execute test with retry logic"""
    print("\n [Node 5] Executing test with retry...")
    
    from app.executor.python_executor_enhanced import execute_python_test
    
    max_retries = 2
    
    for attempt in range(max_retries):
        print(f"  Attempt {attempt + 1}/{max_retries}")
        
        result = execute_python_test(state["code_file_path"])
        
        if result["return_code"] == 0:
            print("✅ Test passed!")
            return {
                **state,
                "execution_status": "passed",
                "execution_output": result.get("output", ""),
                "execution_errors": "",
                "retry_count": attempt,
                "test_passed": True
            }
        
        print(f" Attempt {attempt + 1} failed")
    
    # All retries failed
    return {
        **state,
        "execution_status": "failed",
        "execution_output": result.get("output", ""),
        "execution_errors": result.get("errors", ""),
        "retry_count": max_retries,
        "test_passed": False
    }


def should_execute(state: TestState) -> Literal["execute", "skip"]:
    """Conditional edge"""
    if state["parsing_status"] == "success" and state["parsed_steps"]:
        return "execute"
    return "skip"


def build_enhanced_agent():
    """Build enhanced agent with error handling"""
    workflow = StateGraph(TestState)
    
    # Add nodes with error handling
    workflow.add_node("parse", parse_with_error_handling)
    workflow.add_node("track_state", track_browser_state)
    workflow.add_node("generate", generate_adaptive_code)
    workflow.add_node("save", save_code)
    workflow.add_node("execute", execute_with_retry)
    
    # Set flow
    workflow.set_entry_point("parse")
    workflow.add_edge("parse", "track_state")
    workflow.add_edge("track_state", "generate")
    workflow.add_edge("generate", "save")
    
    workflow.add_conditional_edges(
        "save",
        should_execute,
        {
            "execute": "execute",
            "skip": END
        }
    )
    
    workflow.add_edge("execute", END)
    
    return workflow.compile()


# Create enhanced agent
agent = build_enhanced_agent()