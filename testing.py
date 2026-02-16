
from ai_testing_agent.agent import agent

if __name__ == "__main__":
    result = agent.invoke({"input": "Hello, world!"})
    print(result)
