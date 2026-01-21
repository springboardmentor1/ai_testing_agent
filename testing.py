

#testing.py-to run in terminal

from agent import run_agent

if __name__ == "__main__":
    user_input = input("Enter input: ")
    output = run_agent(user_input)
    print("Agent output:", output)
