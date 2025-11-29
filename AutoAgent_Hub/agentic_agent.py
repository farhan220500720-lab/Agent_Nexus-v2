import json
import datetime
from utils import call_gpt_model

# --- 1. Define the "Real World" Tools ---
def get_current_time():
    """Returns the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- 2. Describe Tools to the AI ---
available_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current real-world date and time.",
            "parameters": {
                "type": "object",
                "properties": {}, # No arguments needed for this tool
                "required": [],
            },
        },
    }
]

# Map tool names to actual Python functions
tool_functions = {
    "get_current_time": get_current_time,
}

# --- 3. Agent Memory & Logic ---
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant. If asked about time, use your tools."}
]

def run_agent(user_input: str) -> str:
    global conversation_history
    
    # Add user message
    conversation_history.append({"role": "user", "content": user_input})

    # First Call: See if the AI wants to talk or run a tool
    response_message = call_gpt_model(conversation_history, tools=available_tools)

    if not response_message:
        return "Error: No response from model."

    # Add the AI's initial response (which might be a tool call) to history
    conversation_history.append(response_message)

    # --- CHECK: Did the AI ask to run a tool? ---
    if response_message.tool_calls:
        print(f" > Agent is using a tool...") # Debug print
        
        # Loop through all requested tools
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = tool_functions.get(function_name)
            
            if function_to_call:
                # Run the actual Python function
                function_response = function_to_call()
                
                # Give the result back to the AI
                conversation_history.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })

        # Second Call: Ask AI to generate the final answer using the tool result
        final_response = call_gpt_model(conversation_history, tools=available_tools)
        
        if final_response and final_response.content:
            conversation_history.append(final_response)
            return final_response.content
            
    # If no tool was needed, just return the text
    return response_message.content