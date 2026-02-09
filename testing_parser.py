from app.agents.baseline_agent import agent

if __name__ == "__main__":
    result = agent.invoke({
        "input": "Open test page and enter name and click submit and verify success"
    })
    print(result)
