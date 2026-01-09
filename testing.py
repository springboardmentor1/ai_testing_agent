from agents.baseline_agent import agent

if __name__ == "__main__":
    result = agent.invoke({"input":"Hi there!"})
    print(result)