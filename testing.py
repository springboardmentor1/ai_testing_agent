from app.agents.baseline_agent import agent

if __name__ == "__main__":
    result = agent.invoke({"input": "Hello, Agent!"})
    print(result)