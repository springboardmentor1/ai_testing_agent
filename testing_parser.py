from app.agents.llm_instruction_parser import llm_parser_agent

if __name__ == "__main__":
    result = llm_parser_agent.invoke({
        "input": "Open google and search for amazon mobiles"
    })
    print(result)
