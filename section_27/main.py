from openai import OpenAI

# Point to LMSYS, not OpenAI
client = OpenAI(base_url="https://api.lmsys.org/v1/", api_key="lm-sys") 

response = client.chat.completions.create(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)