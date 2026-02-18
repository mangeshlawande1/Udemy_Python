# COT  Prompt :


from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

SYSTEM_PROMPT = """
        You are an expert of AI Assistant in resolving user queries using chain of thought.
        You work on START, PLAN OUTPUT steps. 
        You need to PLAN what needs to be done. The plan can be multiple steps. 
        Once you think enough PLANE  has been done , finally you can give an OUTPUT.

        Rules :
            - Strictly follow the given JSON OUTPUT format. 
            - only run one step at a time .
            - The sequence of steps START (where  user gives an input), PLAN (That can be multiple times) and finally output (Which is going to be displayed to the user). 
            - Return ONLY ONE JSON object per turn. Do NOT wrap it in a list.

        OUTPUT JSON Format :
            { "step": "START" | "PLAN" | "OUTPUT" , "content":"str" }

        Example 1 :
        START : "Hey can you write a code to solve 2 + 3 * 5 /10"
        PLAN : {"step":"PLAN", "content": "Seems like user is interested in math problems."} 
        PLAN : {"step":"PLAN", "content": "Looking at the problems, we should solve this using BODMAS method  ."} 
        PLAN : {"step":"PLAN", "content": "Yes BOSMAS is correct thing to be done here."} 
        PLAN : {"step":"PLAN", "content": "First we multiply 3*5 which is 15 ."} 
        PLAN : {"step":"PLAN", "content": "Now the new equation becomes 2 + 15 / 10"} 
        PLAN : {"step":"PLAN", "content": "Must perfoem divide  15 / 10 = 1.5 ."} 
        PLAN : {"step":"PLAN", "content": "Now the new equation is 2 +  1.5 = 3.5 "} 
        PLAN : {"step":"PLAN", "content": "Great we have solve and finally left with  3.5"} 
        OUTPUT: {"step":"OUTPUT", "content": "3.5"}  

    """

message_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
]

print("\n\n\n")

user_query = input("==> ")
message_history.append({"role": "user", "content": user_query})


while True:
    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        response_format={"type": "json_object"},
        messages=message_history,
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result = json.loads(raw_result)

    if isinstance(parsed_result, list):
        parsed_result = parsed_result[0]

    step = parsed_result.get("step")
    content = parsed_result.get("content")

    if step == "START":
        print("\n start LLM Loop: ", content)
        continue

    if step == "PLAN":
        print("\nPlanning 🧠:: ", content)
        continue

    if step == "OUTPUT":
        print("\nLLM 🤖: ", content)
        break

# print(response.choices[0].message.content)
