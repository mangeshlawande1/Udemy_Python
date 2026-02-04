from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import requests

# Load environment variables
load_dotenv()

# Configure OpenAI client to use Google's Gemini API
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Download and encode the image to base64
image_url = "https://images.pexels.com/photos/34719406/pexels-photo-34719406.jpeg"
response = requests.get(image_url)
image_base64 = base64.b64encode(response.content).decode('utf-8')

SYSTEM_PROMPT =  """You are a creative caption writer. Analyze the provided image and generate a compelling, 
descriptive caption that captures the essence, mood, and key elements of the image.

Your caption should:
- Be concise yet descriptive (around 30-50 words)
- Highlight the main subject and atmosphere
- Use vivid and engaging language
- Be suitable for social media or professional use"""
# Create the completion request
response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "system",
            "content":SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate a caption for this image."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ]
)

# Print the result
print("Generated Caption:")
print("-" * 50)
print(response.choices[0].message.content)



''''
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
import requests
from io import BytesIO

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Download the image
image_url = "https://images.pexels.com/photos/34719406/pexels-photo-34719406.jpeg"
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))

# Use Gemini
model = genai.GenerativeModel('gemini-3-flash-preview')
response = model.generate_content([
    "Generate a caption for this image.",
    img
])

print(response.text)

'''