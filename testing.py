from app.agents.baseline_agent import agent

if __name__ == "__main__":
    # The input must be a dictionary
    result = agent.invoke({"input": "Hello!"})
    print(result)