from agents import Agent, Runner
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# Define the client with your API key
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'base_url': "https://generativelanguage.googleapis.com/v1beta/openai/"}
)

# Define the agent using the client object
agent = Agent(
    client=client,
    model="gemini-3-flash-preview",  # Specify a model name
    name="Hello, world Agent",
    instructions="You are an agent which greets the user and helps them using emojis and in a funny way."
)

# Run the agent
result = Runner.run_sync(agent, "Hey There, my name is Alice!")

print(result.final_output)



