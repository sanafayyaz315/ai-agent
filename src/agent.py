from llm import LLM
from tools import add, subtract
from utils import load_template

import re
import json


stop_words = ("PAUSE",)

# format prompt
def format_prompt(template, message):
    prompt = template.format(input=message)
    return prompt

# generate 
def generate(llm, prompt, stop_words=("PAUSE",), stop=False):
    response = ""
    stop_word_ind = None

    for chunk in llm.stream(prompt):
        response += chunk
        for word in stop_words:
            if word in response[-20:]: # check for stop words in the last 20 characters (not words or subwords, characters). Doing this because PAUSE is represented as two tokwns [PA, USE] so cannot do token by token compaison with stop words. Instead checking if stop words exist in the last 20 characters of the response or not.
                stop = True
                stop_word_ind = response.find(word) # index of the first character of stop word
                break
        if stop:
            break
    print(f"\nstop word dound at {stop_word_ind}")
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




if __name__ == "__main__":
    api_key = "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"
    llm = LLM(api_key=api_key)
    tools = {
    "add": add,
    "subtract": subtract,
    }

    message = "what is the difference of 700 and 59?"
    template_path = "../templates/add_subtract.txt"

    template = load_template(template_path)
    prompt = format_prompt(template, message) 
    response = generate(llm, prompt)
    print(response)
    action, action_input = parse_action(response)
    observation = execute_tool(action, action_input, tools)
    print(observation)




    