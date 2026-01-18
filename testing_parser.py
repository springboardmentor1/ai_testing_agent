from app.agents.instruction_parser import parser_agent

if __name__ == "__main__":
    result = parser_agent.invoke({
        "input": "open Google and search for amazon"
    })
    print(result)