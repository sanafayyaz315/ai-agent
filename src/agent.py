import re
import json
import os
import inspect
import asyncio
from dotenv import load_dotenv
from llm import LLM
from tools import *
from utils import load_template, get_tool_descriptions
from tool_registry import TOOLS
from config import SYSTEM_PROMPT_TEMPLATE_SQL, SYSTEM_PROMPT_TEMPLATE_CALCULATOR, MAX_ITERATIONS, DB_SCHEMA
stop_words = ("PAUSE",)
load_dotenv()
# template_dir = os.getenv("TEMPLATE_DIR")
max_iterations = MAX_ITERATIONS

tool_description = get_tool_descriptions(TOOLS)
                                         
# generate 
def generate(llm, prompt, stop_words=("PAUSE",), stop=False):
    response = ""
    stop_word_ind = None

    for chunk in llm.stream(prompt):
        response += chunk
        yield chunk
        for word in stop_words:
            if word in response[-20:]: # check for stop words in the last 20 characters (not words or subwords, characters). Doing this because PAUSE is represented as two tokwns [PA, USE] so cannot do token by token compaison with stop words. Instead checking if stop words exist in the last 20 characters of the response or not.
                stop = True
                # stop_word = word
                # stop_word_ind = response.find(word) # index of the first character of stop word
                break
        if stop:
            break
    print(f"\nstop word found at {stop_word_ind}")
    # return response[:stop_word_ind] # omit stop word from response

def parse_action(response):
    # Match ```json { ... } ```
    pattern = r'```json\s*(\{.*?\})\s*```'
    match = re.search(pattern, response, re.DOTALL)
    # print(match)
    if not match:
        raise ValueError("No valid JSON block found after 'Action:'")

    json_str = match.group(1)
    # Remove backslash followed by spaces and newline (line continuation backslashes)
    # This removes backslash + spaces + newline sequences from the JSON string, 
    # which breaks the SQL string into multiple lines without the backslash.
    json_str = re.sub(r'\\\s*\n\s*', ' ', json_str)
    try:
        data = json.loads(json_str)
        if "action" not in data or "action_input" not in data:
            raise ValueError("JSON missing required 'action' or 'input' fields")

    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parsing error: {e}")

    action = data["action"]
    action_input = data["action_input"]

    return action, action_input

async def execute_tool(tool, input):
    if not tool:
        raise ValueError("action or action_input are None")
    if tool == "execute_sql":
        observation = await execute_sql(input)
    else:
        func = TOOLS[tool]
        observation = func(input)

    return observation


async def run(llm, message, agent="text-to-sql"):
    messages = []
    # template_path = os.path.join(template_dir, "multipurpose.txt")
    # print(template_path)s
    # with open(template_path, 'r', encoding='utf-8') as f:
    #     system_prompt = f.read()  
    if agent == "text-to-sql":
        system_prompt = SYSTEM_PROMPT_TEMPLATE_SQL.format(schema=DB_SCHEMA)
    elif agent == "calculator":
        system_prompt = SYSTEM_PROMPT_TEMPLATE_CALCULATOR.format(tool_description=tool_description)

    messages.append({"role": "system", "content": system_prompt})
    state = []
    next_prompt = message

    for _ in range(max_iterations):
        # append the user question, observation as next_prompt
        messages.append({"role": "user", "content": next_prompt})
        # collect streaming reponse from the llm
        response = ""
        for chunk in generate(llm, messages):
            # print(chunk, end="", flush=True)
            yield ("response", chunk)
            response += chunk     
        # append response to messages
        messages.append({"role": "assistant", "content": response})

        state.append({"user":  next_prompt})
        state.append({"assistant":  response})

        if "Action" in response:
            try: # try-except to check if Action block is correctly generated ans is parseable
                action, action_input = parse_action(response)
            except Exception as e:
                observation = (
                    "Error: Failed to parse action from response.\n"
                    "Carefully review the `Thought`, `Action`, `Action Input` format.\n" 
                    "Make sure Actions are called in the right order\n"
                    f"Details: {str(e)}"
                )
                next_prompt = f"{observation}\n"
                yield ("observation", next_prompt)
                continue

            if action not in TOOLS:
                observation = f"Action '{action}' not available in the set of tools."
            else:
                try:
                    observation =  await execute_tool(action, action_input)
                except Exception as e:
                    observation = f"Error: Failed to execute tool: `{action}`. Details: {str(e)}"
            next_prompt = f"\nObservation: {observation}\n"
            yield ("observation", next_prompt)
            

        elif "Final Answer" in response:
            break
        else:
            observation = "Missing `Action` or `Final Answer` in response."
            next_prompt =  f"{observation}"

    return 

if __name__ == "__main__":
    from config import (
        API_KEY,
        MODEL
        )
    llm = LLM(api_key=API_KEY, model=MODEL)
    message = "what is the sum and difference and product of 5000 and 99?"
    message = "what is the email for Alice Smith?"
    message = "what is the total number of orders?"
    message = "provide me the latest order details. provide the details of the customers and products purchased."
    message = "How many Monitors have been sold?"
    message = "Give me purchase details for ALice Smith"
    async def main(message):
        llm = LLM(api_key=API_KEY, model=MODEL)        
        response = ""
        async for kind, chunk in run(llm, message, agent="text-to-sql"):
            if kind == "response":
                response += chunk
                print(chunk, end="", flush=True)
            elif kind == "observation":
                print("\n", chunk, flush=True)

        print("\n----------------------FINAL RESPONSE-----:")
        print(response[response.find("Final Answer"):])

    asyncio.run(main(message))

    # print(f"----------------------MESSAGES-----------: \n {messages}")
    # print("----------------------STATE--------------: \n")
    # for step in state:
    #     for user, content in step.items():
    #         print(f"{user}: ", content)
    #         break
    # print(f"\n----------------------FINAL RESPONSE-----: \n {response[response.find('Final Answer'):]}")
    
    



 
    






    