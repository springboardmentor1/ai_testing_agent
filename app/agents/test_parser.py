from app.agents.parser_agent import agent

print("Invoking parser...\n")

result = agent.invoke({
    "input": "open Google and search for insta"
})

print("FINAL OUTPUT:\n")
print(result["output"])
