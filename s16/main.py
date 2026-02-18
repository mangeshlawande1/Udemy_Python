from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "system",
            "content": "You are an expert i math related questions, that if question is not related to Math just say Sorry and not to answer that question. ",
        },
        {
            "role": "user",
            "content": "Hey can you solve the (a)square - (b)square = ?? ",
        },
    ],
)
print(response.choices[0].message.content)
