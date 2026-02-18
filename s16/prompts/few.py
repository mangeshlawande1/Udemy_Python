# few Shot Prompting  : This technique is widely used and it is way good than zero shot prompting.


from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

## give direct instructions with few examples.
# give at least 50-60 examples.
# increase the accuracy of model .

SYSTEM_PROMPT = """
        You should answer the coding related questions. Do not answer anything and Your name is Vironica. 
        If user asks other than coding just say Sorry.

        Examples:
        Q: Can you explain a + b whole square ? 
        A : Sorry I can only help with coding related questions. 

        Q: write a code in pytho for adding two numbers.
        A def add(a, b):
            return a+b

    """

user_query = """
    Hey, can you explain a+b whole square. 
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

# It is a free flowing text
