from typing import TypedDict
from langgraph.graph import StateGraph,END
from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
import json
from dotenv import load_dotenv
import os

load_dotenv()

class AgentState(TypedDict):
    input:str
    parsed_command:dict
    output:str

def respond(state:AgentState)->AgentState:
    return {
        "input":state["input"],
        "output":f"Echo: {state['input']}"
    }

def rule_based_parser(state: AgentState) -> AgentState:
    text = state["input"].lower()
    command = {"action": "unknown", "target": None, "value": None}

    if "goto" in text or "navigate" in text:
        command["action"] = "navigate"
        # Extract URL 
        command["target"] = text.split("to")[-1].strip()
    
    elif "click" in text:
        command["action"] = "click"
        command["target"] = text.replace("click", "").strip()
        
    elif "type" in text or "enter" in text:
        command["action"] = "type"
        # Example: "Type hello into search"
        parts = text.split("into")
        command["value"] = parts[0].replace("type", "").strip()
        command["target"] = parts[1].strip() if len(parts) > 1 else None

    return {**state, "parsed_command": command}


import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


PARSER_SYSTEM_PROMPT = """
You are a web testing assistant. Convert the user's natural language instruction 
into a JSON object with these exact keys:
- "action": (must be 'navigate', 'click', 'type', or 'verify')
- "target": (the button name, input field, or URL)
- "value": (the text to type, if any; otherwise null)

Example Output:
{{"action": "navigate", "target": "google.com", "value": null}}
"""

def llm_parser(state: AgentState) -> AgentState:
    
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", PARSER_SYSTEM_PROMPT),
        ("human", "{user_input}") 
    ])
    
    chain = prompt | llm
    
    # Process the user input through the Instruction Parser Module
    ai_response = chain.invoke({"user_input": state["input"]})
    
    # Parse the response into a structured command
    parsed_json = json.loads(ai_response.content)
    
    return {**state, "parsed_command": parsed_json}
def mock_code_generator(state: AgentState) -> AgentState:
    command = state["parsed_command"]
    action = command["action"]
    target = command["target"]
    
    # In Milestone 3, this will be actual Playwright code
    generated_code = f"# Playwright Script\nawait page.{action}('{target}')"
    
    return {**state, "output": f"CODE GENERATED:\n{generated_code}"}

# # 1. Initialize Graph
# graph = StateGraph(AgentState)

# # 2. Add Nodes
# graph.add_node("parser", rule_based_parser)
# graph.add_node("respond", respond)

# # 3. Define the Flow (Edges)
# graph.set_entry_point("parser") # Start at the parser station
# graph.add_edge("parser", "respond") # Then go to respond
# graph.add_edge("respond", END) # Then finish

# agent = graph.compile()


graph = StateGraph(AgentState)

graph.add_node("parser", llm_parser)
graph.add_node("generator", mock_code_generator)
graph.set_entry_point("parser")
graph.add_edge("parser", "generator")
graph.add_edge("generator", END)

agent = graph.compile()