import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# --- Data Models ---
class AutomationCommand(BaseModel):
    action: str = Field(description="Action: 'goto', 'click', 'fill', 'press', or 'assert'")
    params: Dict[str, Any] = Field(description="Parameters (url, selector, value, key)")
    description: str = Field(description="Readable description of step")

class AutomationPlan(BaseModel):
    steps: List[AutomationCommand] = Field(description="List of automation steps")

# --- AI Setup ---
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY")
)

parser = JsonOutputParser(pydantic_object=AutomationPlan)

def parse_instruction(instruction: str):
    # --- SMART SYSTEM PROMPT ---
    system_prompt = """
    You are an expert QA Automation Engineer. Convert instructions into structured steps.
    
    ### SITE-SPECIFIC RULES (CRITICAL):
    
    1. **IF AMAZON:**
       - Search Input: "#twotabsearchtextbox"
       - Search Button: "#nav-search-submit-button"
       
    2. **IF YOUTUBE:**
       - Search Input: "input[name='search_query']"
       - First Video: "ytd-video-renderer:nth-of-type(1) #video-title"
       
    3. **IF GOOGLE:**
       - Search Input: "[name='q']"
       - First Result: "div.g:nth-of-type(1) a h3"
       
    4. **IF WIKIPEDIA:**
       - Search Input: "input#searchInput"
       - Search Button: "button.pure-button"
    
    ### GENERAL ACTIONS:
    - **Navigation:** "Open [URL]" -> action: "goto".
    - **Typing:** "Type [text]" -> action: "fill".
    - **Clicking:** "Click [element]" -> action: "click".
    - **Keys:** "Hit Enter" -> action: "press", params: {{"key": "Enter"}}.
    
    ### EXAMPLE (Amazon):
    Input: "Navigate to amazon.in and search for iphone"
    Output:
    [
      {{
        "action": "goto", 
        "params": {{ "url": "https://www.amazon.in" }}
      }},
      {{
        "action": "fill", 
        "params": {{ "selector": "#twotabsearchtextbox", "value": "iphone" }}, 
        "description": "Type 'iphone' into Amazon search"
      }},
      {{
        "action": "click", 
        "params": {{ "selector": "#nav-search-submit-button" }}, 
        "description": "Click Search"
      }}
    ]
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{query}\n\n{format_instructions}")
    ])

    print(f"🧠 AI: Analyzing Instruction: '{instruction}'...")

    try:
        response = (prompt | llm | parser).invoke({
            "query": instruction,
            "format_instructions": parser.get_format_instructions()
        })
        return response.get("steps", [])
    except Exception as e:
        print(f"❌ Parser Error: {e}")
        return []