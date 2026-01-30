from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
            { "role":"user","content":[
                {"type":"text", "text":"Generate a caption for this image in about 59 words "},
                {"type":"image_url", "image_url":{"url":" dsdsdddsdjdskfds " }},


            ]
            }
        ],
)
print(response.choices[0].message.content)


'''
get image from internet
 generate a caption for image
'''