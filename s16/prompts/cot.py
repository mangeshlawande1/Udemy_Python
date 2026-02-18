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
            - Strictly follow the given JSON OUTPUT format 
            - only run one step at a time .
            - The sequence of steps START (where  user gives an input), PLAN (That can be multiple times) and finally 
            - OUTPUT (Which is going to be displayed to the user). 

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

user_query = """
    Hey, can you write a code to add n numbers in javascript. 
"""

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {"role": "user", "content": user_query},
        # Manually Keep adding messages to history
        {
            "role": "assistant",
            "content": json.dumps(
                {"step": "PLAN", "content": "You want to a JS code to add n numbers."}
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "PLAN",
                    "content": "I will create a function that takes a variable number of arguments or an array and uses the reduce method to calculate the sum.",
                },
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "OUTPUT",
                    "content": "function addNumbers(...numbers) {\n  return numbers.reduce((sum, current) => sum + current, 0);\n}\n\n// Example usage:\nconsole.log(addNumbers(1, 2, 3, 4, 5)); // Output: 15",
                }
            ),
        },
    ],
)


print(response.choices[0].message.content)
