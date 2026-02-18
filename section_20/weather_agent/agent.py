from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional

import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


class MyOutputFormat(BaseModel):
    step: str = Field(..., description="Id of the step: PLAN, OUTPUT, TOOL, etc.,")
    content: Optional[str] = Field(None, description="Optional string content ")
    function: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool ")


def run_command(cmd: str):
    result = os.system(cmd)
    return result


def get_weather(city: str):
    url = f"http://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."

    return "Something went wrong"


available_tools = {"get_weather": get_weather, "run_command": run_command}

SYSTEM_PROMPT = """
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - "get_weather": Takes a city name as an input and returns the current weather for the city
    - "run_command": Takes linux command as a string and executes the command and returns the output after executing it.

    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

while True:
    query = input("==> ")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.parse(
            # model="gemini-3-flash-preview",
            model="gemini-3-pro-preview",
            response_format=MyOutputFormat,
            messages=messages,
        )
        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        # parsed_response = json.loads(response.choices[0].message.content)
        parsed_result = response.choices[0].message.parsed
        ## provide type safety

        if parsed_result.step == "plan":
            print(f"🧠: {parsed_result.content}")
            continue

        if parsed_result.step == "action":
            tool_name = parsed_result.function
            tool_input = parsed_result.input
            print(f"🛠️: Calling Tool:{tool_name}({tool_input})")

            tool_response = available_tools[tool_name](tool_input)
            print(f"🛠️: {tool_name}({tool_input}) = {tool_response}")
            messages.append(
                {
                    "role": "user",
                    "content": json.dumps({"step": "observe", "output": tool_response}),
                }
            )
            continue

        if parsed_result.step == "output":
            print(f"🤖: {parsed_result.content}")
            break
