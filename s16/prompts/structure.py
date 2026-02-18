# few Shot Prompting  : This technique is widely used and it is way good than zero shot prompting.
#


from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

## Give direct instructions with few examples.
# Give at least 50-60 examples.
# Increase the accuracy of model .
# You can bind the output quality as well : In which format you want to bind ths output like json

SYSTEM_PROMPT = """
        You should answer the coding related questions. Do not answer anything and Your name is Vironica. 
        If user asks other than coding just say Sorry.

        Rule:
            - Strictly follow theoutput in JSON format 
        
        Output Format:  
        {{
        "code":"string" or None,
        "isCodingQuestion":boolean
        }}

        Examples:
        Q: Can you explain a + b whole square ? 
        A : {{ "code":None,   "isCodingQuestion":False }}

        Q: write a code in pytho for adding two numbers.
        A :{{"code" : "def add(a, b):
            return a+b", "isCodingQuestion": True }}

    """
#     Hey, can you can you explain a+b whole square.

user_query = """
    Hey, can you write a code to add n numbers in javascript. 

"""

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {"role": "user", "content": user_query},
    ],
)
print(response.choices[0].message.content)
