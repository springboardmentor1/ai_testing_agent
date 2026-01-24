from app.agents.baseline_agent import agent

if __name__ == "__main__":
    result = agent.invoke({
        "input": "Open google and search for amazon mobiles"
    })
    print(result)
