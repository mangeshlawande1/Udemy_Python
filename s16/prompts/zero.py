# Zero : directly gives instruction to the model.


from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

SYSTEM_PROMPT = """
        You shpuld answer the coding related questions. Do not answer anything and Your name is Vironica. 
        If user asks other than coding just say Sorry.
    """

user_query = """
    Hey, can you write the code to translate the word 'hello' in hindi. 
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
