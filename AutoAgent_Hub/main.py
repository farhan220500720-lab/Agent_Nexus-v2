from agentic_agent import run_agent
import os
from dotenv import load_dotenv

# Load the key from the .env file we just created
load_dotenv()

def main():
    print("--- AutoAgent_Hub Initialized ---")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        # 1. Get input from the user
        try:
            user_input = input("You: ")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

        # 2. Check if user wants to quit
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # 3. Run the Agent with the user's input
        # The error happened because this part was missing 'user_input' inside the ()
        print("Agent is thinking...")
        try:
            response = run_agent(user_input)
            print(f"AutoAgent: {response}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()