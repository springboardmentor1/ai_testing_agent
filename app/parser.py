import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the Strict Data Model for AI Output
class AutomationCommand(BaseModel):
    action: str = Field(description="The action: 'goto', 'click', 'fill', 'press', or 'assert'")
    params: Dict[str, Any] = Field(description="Parameters for the action (e.g., url, selector, value, key)")
    description: str = Field(description="Human-readable description of what this step does")

class AutomationPlan(BaseModel):
    steps: List[AutomationCommand] = Field(description="List of sequential automation steps")

# Initialize the LLM (Llama 3.3)
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY")
)

# Initialize the Parser
parser = JsonOutputParser(pydantic_object=AutomationPlan)

def parse_instruction(instruction: str):
    """
    Converts natural language into a list of structured Playwright commands.
    """
    
    # SYSTEM PROMPT 
    system_prompt = """
    You are an expert QA Automation Engineer.
    Your job is to convert natural language test instructions into a list of structured steps.
    
    ### RULES:
    1. **Navigation:** If user says "Open [URL]", output action: "goto".
    2. **Typing:** If user says "Type [text] into [field]", output action: "fill".
       - **Selector Strategy:** Use your knowledge of standard web elements.
       - Common Search IDs: "#searchInput", "#search", "[name='q']", "[name='search']".
       - Common Login IDs: "#username", "#email", "#password".
    3. **Clicking:** If user says "Click [element]", output action: "click".
       - **Selector Strategy:** ALWAYS prioritize IDs first.
       - Example: "Click Submit" -> selector: "#submit" (Preferred) or "button[type='submit']"
       - Example: "Click Login" -> selector: "#login-btn" or "#login"
    4. **Keys:** If user says "Hit Enter", output action: "press".
    5. **Assertions:** If user says "Verify title is [text]" or "Check if text exists", output action: "assert".
       - For titles: params = {{"type": "title", "value": "Expected Title"}}
       - For text: params = {{"type": "text", "selector": "body", "value": "Expected Text"}}
    
    ### OUTPUT FORMAT:
    Return ONLY a JSON object with a "steps" key containing the list.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{query}\n\n{format_instructions}")
    ])

    chain = prompt | llm | parser

    try:
        response = chain.invoke({
            "query": instruction,
            "format_instructions": parser.get_format_instructions()
        })
        return response.get("steps", [])
    except Exception as e:
        print(f"Error in Parser: {e}")
        return []