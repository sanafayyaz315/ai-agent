import re
import json
import os
from dotenv import load_dotenv
from llm import LLM
from tools import add, subtract
from utils import load_template

stop_words = ("PAUSE",)
load_dotenv()
template_dir = os.getenv("TEMPLATE_DIR")
max_iterations = 10
tools = {
"add": add,
"subtract": subtract,
}

# generate 
def generate(llm, prompt, stop_words=("PAUSE",), stop=False):
    response = ""
    stop_word_ind = None

    for chunk in llm.stream(prompt):
        response += chunk
        for word in stop_words:
            if word in response[-20:]: # check for stop words in the last 20 characters (not words or subwords, characters). Doing this because PAUSE is represented as two tokwns [PA, USE] so cannot do token by token compaison with stop words. Instead checking if stop words exist in the last 20 characters of the response or not.
                stop = True
                # stop_word = word
                stop_word_ind = response.find(word) # index of the first character of stop word
                break
        if stop:
            break
    print(f"\nstop word found at {stop_word_ind}")
    return response[:stop_word_ind] # omit stop word from response

def parse_action(response):
    # Match ```json { ... } ```
    pattern = r'```json\s*(\{.*?\})\s*```'
    match = re.search(pattern, response, re.DOTALL)
    # print(match)
    if not match:
        raise ValueError("No valid JSON block found after 'Action:'")

    json_str = match.group(1)
    try:
        data = json.loads(json_str)
        if "action" not in data or "input" not in data:
            raise ValueError("JSON missing required 'action' or 'input' fields")

    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parsing error: {e}")

    action = data["action"]
    action_input = data["input"]

    return action, action_input

def execute_tool(tool, input):
    if not tool or not input:
        raise ValueError("action or action_input are None")
    func = tools[tool]
    return func(input)

def run(llm, message):
    messages = []
    template_path = os.path.join(template_dir, "add_subtract.txt")
    print(template_path)
    with open(template_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    messages.append({"role": "system", "content": system_prompt})
    state = []
    next_prompt = message

    for step in range(max_iterations):
        messages.append({"role": "user", "content": next_prompt})
        response = generate(llm, messages)
        messages.append({"role": "assistant", "content": response})
        # state.append(response)
        state.append({"user":  next_prompt})
        state.append({"assistant":  response})

        if "Action" in response:
            try: # try-except to check if Action block is correctly generated ans is parseable
                action, action_input = parse_action(response)

                if action not in tools:
                    observation = f"Action '{action}' not available in the set of tools."
                    next_prompt =  f"{observation}"
                    # state.append(next_prompt)
                    continue

                observation = execute_tool(action, action_input)
                next_prompt =  f"{observation}"
                # state.append(next_prompt)
            except Exception as e:
                    observation = (
                        "Error: Failed to parse action from response."
                        "Carefully review the `Thought`, `Action`, `Action Input` format. "
                        f"Details: {str(e)}"
                    )
                    next_prompt = f"{observation}\n"

        elif "Final Answer" in response:
            break
        else:
            observation = "Missing `Action` or `Final Answer` in response."
            next_prompt =  f"{observation}"
            # state.append(next_prompt)


    return response, state, messages
 

if __name__ == "__main__":
    api_key = "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"
    llm = LLM(api_key=api_key)
    message = "what is the sum and difference of 5000 and 699?"
    response, state, messages= run(llm, message)

    # print(f"----------------------MESSAGES-----------: \n {messages}")
    print("----------------------STATE--------------: \n")
    for step in state:
        for user, content in step.items():
            print(f"{user}: ", content)
            break
    print(f"\n----------------------FINAL RESPONSE-----: \n {response}")
    
    



 

    
    # action, action_input = parse_action(response)
    # observation = execute_tool(action, action_input, tools)
    # print(observation)

    






    