# # from geopy.geocoders import Nominatim
# from openai import OpenAI
# from dotenv import load_dotenv
# import requests
# import os
# import json

# load_dotenv()


# client = OpenAI(
#     api_key=os.getenv("GEMINI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )


# def get_weather(city: str):
#     url = f"http://wttr.in{city}?format=%C+%t"
#     response = requests.get(url)
#     return (
#         f"The weather in {city} is {response.text}."
#         if response.status_code == 200
#         else "Error"
#     )


# available_tools = {
#     "get_weather":get_weather,

# }

# SYSTEM_PROMPT = """
#         You are an expert of AI Assistant in resolving user queries using chain of thought.
#         You work on START, PLAN OUTPUT steps.
#         You need to PLAN what needs to be done. The plan can be multiple steps.
#         Once you think enough PLANE  has been done , finally you can give an OUTPUT.
#         You can also call a tool required from the list of available tools.
#         For every tool call wait for observe step which is output from the called tool.

#         Rules :
#             - Strictly follow the given JSON OUTPUT format
#             - only run one step at a time .
#             - The sequence of steps START (where  user gives an input), PLAN (That can be multiple times) and finally OUTPUT (Which is going to be displayed to the user).

#         OUTPUT JSON Format :
#             { "step": "START" | "PLAN" | "OUTPUT" | "TOOL" , "content":"string", "tool":"string","input":"string" }

#         Available Tools :
#             - get_weather(city:str): takes city name is input and return the weather information about the city.

#         Example 1 :
#         START : "Hey can you write a code to solve 2 + 3 * 5 /10"
#         PLAN : {"step":"PLAN", "content": "Seems like user is interested in math problems."}
#         PLAN : {"step":"PLAN", "content": "Looking at the problems, we should solve this using BODMAS method  ."}
#         PLAN : {"step":"PLAN", "content": "Yes BOSMAS is correct thing to be done here."}
#         PLAN : {"step":"PLAN", "content": "First we multiply 3*5 which is 15 ."}
#         PLAN : {"step":"PLAN", "content": "Now the new equation becomes 2 + 15 / 10"}
#         PLAN : {"step":"PLAN", "content": "Must perfoem divide  15 / 10 = 1.5 ."}
#         PLAN : {"step":"PLAN", "content": "Now the new equation is 2 +  1.5 = 3.5 "}
#         PLAN : {"step":"PLAN", "content": "Great we have solve and finally left with  3.5"}
#         OUTPUT: {"step":"OUTPUT", "content": "3.5"}

#         Example 2 :
#         START : "What is the weather of Delhi?"
#         PLAN : {"step":"PLAN", "content": "Seems like user is interested getting weather of delhi in india."}
#         PLAN : {"step":"PLAN", "content": "Looking at the available tools from the list of available tools."}
#         PLAN : {"step":"PLAN", "content": "Yes we have get_weather tool available for this query."}
#         PLAN : {"step":"PLAN", "content": "I need to call get_weather  tool for delhi as input for city."}
#         PLAN : {"step":"TOOL", "tool":"get_weather","content": "delhi"}
#         PLAN : {"step":"OBSERVE", "tool": "get_weather", "content":"the temp of delhi is cloudy with 20 C." }
#         PLAN : {"step":"PLAN", "content": "Great, I got the weather info about Delhi."}
#         OUTPUT: {"step":"OUTPUT", "content": "The Current weather in Delhi is 20 C with some Cloudy Sky."}
#     """

# message_history = [ { "role": "system", "content": SYSTEM_PROMPT, } ]
# print("\n")

# while True:

#     # Start the conversation with the user query
#     user_input = input("==> ")
#     message_history.append({"role": "user", "content": user_input})

#     while True:
#         response = client.chat.completions.create(
#             model="gemini-3-flash-preview",
#             response_format={"type": "json_object"},
#             messages=message_history,
#         )


#         raw_result = response.choices[0].message.content
#         message_history.append({"role": "assistant", "content": raw_result})
#         parsed_result = json.loads(raw_result)

#         if isinstance(parsed_result, list):
#             parsed_result = parsed_result[0]

#         step = parsed_result.get("step")
#         content = parsed_result.get("content")

#         if step == "START":
#             print("\n start LLM Loop: ", content)
#             continue

#         if step == "TOOL":
#             tool_to_call = parsed_result.get("tool")
#             tool_input = parsed_result.get("input")
#             print(f" {tool_to_call} ({tool_input})")

#             tool_response = available_tools[tool_to_call](tool_input)
#             message_history.append(
#                 {"role":"developer","content": json.dumps(
#                     { "step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
#                 )}
#             )

#         if step == "PLAN":
#             print("\nPlanning 🧠:: ", content)
#             continue

#         if step == "OUTPUT":
#             print("\nLLM 🤖: ", content)
#             break





import os
import json
import time
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. Setup Client
# Ensure your .env has GEMINI_API_KEY
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


def get_weather(city: str):
    """Fetches weather using wttr.in (No API key needed)"""
    # Clean the input (remove quotes or extra spaces)
    city = city.strip().replace('"', "").replace("'", "")
    url = f"http://wttr.in/{city}?format=%C+%t"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return f"The weather in {city} is {response.text}."
        return f"Error: Could not find weather for {city}."
    except Exception as e:
        return f"Tool Error: {str(e)}"


available_tools = {
    "get_weather": get_weather,
}

# 2. Optimized System Prompt
# Added a strict rule to call tools immediately if available.
SYSTEM_PROMPT = """
You are an expert AI Assistant that uses a ReAct (Reasoning and Acting) loop.
Your goal is to solve the user query using the available tools.

JSON OUTPUT FORMAT:
{ "step": "PLAN" | "TOOL" | "OUTPUT", "content": "string", "tool": "string", "input": "string" }

RULES:
- ONLY output the JSON object. Do not add any other text.
- Step "PLAN": Explain what you are doing.
- Step "TOOL": Use this to call a tool. Example: {"step": "TOOL", "tool": "get_weather", "input": "Mumbai"}
- Step "OUTPUT": Use this for the final answer once you have information.
- If you need information from a tool, you MUST call the TOOL immediately after a PLAN.

 Example 1 :
         START : "What is the weather of Delhi?"
         PLAN : {"step":"PLAN", "content": "Seems like user is interested getting weather of delhi in india."}
         PLAN : {"step":"PLAN", "content": "Looking at the available tools from the list of available tools."}
         PLAN : {"step":"PLAN", "content": "Yes we have get_weather tool available for this query."}
         PLAN : {"step":"PLAN", "content": "I need to call get_weather  tool for delhi as input for city."}
         PLAN : {"step":"TOOL", "tool":"get_weather","content": "delhi"}
         PLAN : {"step":"OBSERVE", "tool": "get_weather", "content":"the temp of delhi is cloudy with 20 C." }
         PLAN : {"step":"PLAN", "content": "Great, I got the weather info about Delhi."}
         OUTPUT: {"step":"OUTPUT", "content": "The Current weather in Delhi is 20 C with some Cloudy Sky."}
"""


# 3. Main Logic
def run_agent():
    # Outer loop for new user questions
    while True:
        user_input = input("\n==> User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Reset history for a new question, but keep the system prompt
        message_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        message_history.append({"role": "user", "content": user_input})

        # Inner loop for the ReAct chain (Thinking -> Acting -> Observing)
        max_iterations = 10
        for i in range(max_iterations):
            # 🛑 Rate Limit Delay: Gemini Free tier allows ~15 requests/min.
            # 4 seconds between turns is a safe middle ground.
            time.sleep(4)

            try:
                response = client.chat.completions.create(
                    model="gemini-3-flash-preview", 
                    response_format={"type": "json_object"},
                    messages=message_history,
                )

                raw_result = response.choices[0].message.content
                parsed_result = json.loads(raw_result)

                # Record the assistant's thought/action in history
                message_history.append({"role": "assistant", "content": raw_result})
                if isinstance(parsed_result, list):
                    parsed_result = parsed_result[0]  # Grab the first dict if it's a list
                # ------------------------------

                step = parsed_result.get("step")
                content = parsed_result.get("content", "")

                if step == "PLAN":
                    print(f"🧠 Planning: {content}")
                    continue

                if step == "TOOL":
                    tool_name = parsed_result.get("tool")
                    tool_input = parsed_result.get("input")
                    print(f"🛠️  Calling Tool: {tool_name}({tool_input})")

                    # Execute the actual Python function
                    observation = available_tools[tool_name](tool_input)
                    print(f"👀 Observation: {observation}")

                    # Feed the result back as a USER message so the LLM can "see" it
                    message_history.append(
                        {"role": "user", "content": f"OBSERVE: {observation}"}
                    )
                    continue

                if step == "OUTPUT":
                    print(f"🤖 LLM Answer: {content}")
                    break

            except Exception as e:
                print(f"❌ Error during loop: {e}")
                break
        else:
            print("⚠️ Max iterations reached without an answer.")


if __name__ == "__main__":
    run_agent()
