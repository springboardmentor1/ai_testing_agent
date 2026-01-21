import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Any

# 1. Load Environment Variables
load_dotenv()

# 2. Defines the JSON Structure 
class AutomationCommand(BaseModel):
    action: str = Field(description="The action: 'goto', 'click', 'fill', 'press'")
    params: Dict[str, Any] = Field(description="Parameters like {'url': '...'} or {'selector': '...', 'value': '...'}")
    description: str = Field(description="Short explanation of the step")

class CommandList(BaseModel):
    commands: List[AutomationCommand]

# 3. Main Parsing Logic
def parse_instruction(instruction: str):
    try:
        # Initialize Groq (Llama 3)
        llm = ChatGroq(
            temperature=0,
            model_name="llama-3.3-70b-versatile",
            api_key=os.environ.get("GROQ_API_KEY")
        )

        parser = JsonOutputParser(pydantic_object=CommandList)

        # The System Prompt: Teaches the AI how to write Playwright steps
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert QA Automation Agent. Convert user instructions into a sequence of Playwright commands. \n"
                       "Supported Actions: \n"
                       "- 'goto' (params: url) \n"
                       "- 'click' (params: selector) \n"
                       "- 'fill' (params: selector, value) \n"
                       "- 'press' (params: selector, key) \n\n"
                       "Rules: \n"
                       "1. If the user says 'search for X', generate TWO commands: 'fill' then 'press' Enter. \n"
                       "2. Return ONLY valid JSON matching the format instructions. \n"
                       "{format_instructions}"),
            ("human", "{query}")
        ])

        # Create the Chain
        chain = prompt | llm | parser

        print(f"DEBUG: Sending to Groq... '{instruction}'")
        
        # Execute
        response = chain.invoke({
            "query": instruction,
            "format_instructions": parser.get_format_instructions()
        })

        return response['commands']

    except Exception as e:
        print(f"Error in Parser: {e}")
        return []