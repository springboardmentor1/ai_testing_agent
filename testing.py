

<<<<<<< HEAD
#testing.py-to run in terminal

from agent import run_agent

if __name__ == "__main__":
    user_input = input("Enter input: ")
    output = run_agent(user_input)
    print("Agent output:", output)
=======
from ai_testing_agent.agent import agent

if __name__ == "__main__":
    result = agent.invoke({"inpu"})
    print(result)
>>>>>>> e86365c4232a5c9468af5a1ef5cd343c6c71190d
