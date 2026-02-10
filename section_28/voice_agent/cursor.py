from dotenv import load_dotenv
from openai import OpenAI
import requests 
from pydantic import BaseModel, Field
from typing import Optional
import json
import os

import asyncio
import speech_recognition as sr 
from openai.helpers import LocalAudioPlayer
from openai import AsyncOpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def run_command(cmd:str):
    result = os.system(cmd)
    return result

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The Weather in {city} is {response.text}"
    
    return "Something went wrong !!"



async def tts(speech:str):
   async with async_client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="coral",
        instructions="Always speak in cheerfull manner with full of delight and happy. ",
        input=speech,
        response_format="pcm",
    ) as response:
       await  LocalAudioPlayer().play(response)


class MyOutputFormat(BaseModel):
    step: str = Field( ..., description= "The ID of the step. Example : PLAN, OUTPUT, TOOL. etc., " )
    content: Optional[str] = Field(None, description="The Optional string content for the step.")
    tool: Optional[str] = Field(None, description= "The id of the tool to call. " )
    input:Optional[str] = Field(None, description= "the input patameter for tools. ")


SYSTEM_PROMPT = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - "get_weather(city:str)": Takes a city name as an input and returns the current weather for the city
    - "run_command(cmd:str)": Takes linux command as a string and executes the command and returns the output after executing it.

    Example:
    START: What is the weather of new york?
    PLAN: {{ "step": "PLAN", "content": "The user is interseted in weather data of new york" }}
    PLAN: {{ "step": "PLAN", "content": "From the available tools I should call get_weather" }}
    PLAN: {{ "step": "TOOL", "tool": "get_weather", "input": "new york" }}
    PLAN: {{ "step": "OBSERVE", "OUTPUT": "12 Degree Cel" }}
    OUTPUT: {{ "step": "OUTPUT", "content": "The weather for new york seems to be 12 degrees." }}

"""


message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

r = sr.Recognizer() # speech to text 
with sr.Microphone() as source: 
    r.adjust_for_ambient_noise(source)
    r.pause_threshold = 2 


while True:
    # print("Speak something.... ")
    # audio = r.listen(source)

    # print("Processing Audio ...(STT)")

    user_query = input(">>")
    # user_query = r.recognize_google(audio)

    message_history.append({"role":"user", "content": user_query })

    while True:
        response = client.chat.completions.parse(
            model='gemini-3-flash-preview',
            response_format=MyOutputFormat,
            messages=message_history,
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role":"assistant", "content":raw_result })

        parsed_result = response.choices[0].message.parsed

        if parsed_result.step == "START":
            print("start--> ", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print("🛠️: Calling TooL: ", tool_to_call,"++", tool_input )
            continue

        if parsed_result.step == "PLAN":
            print("🧠--> ", parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("🤖--> ", parsed_result.content)
            asyncio.run(tts(speech=response.choices[0].message.content))
            break;


    
'''
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
import requests 
from pydantic import BaseModel, Field
from typing import Optional
import os
import asyncio
import speech_recognition as sr 

load_dotenv()

# Gemini client for chat
gemini_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# OpenAI client for TTS
openai_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The Weather in {city} is {response.text}"
    
    return "Something went wrong !!"

async def tts(speech: str):
    """Text-to-speech using OpenAI's API"""
    try:
        async with openai_client.audio.speech.with_streaming_response.create(
            model="tts-1",  # ✅ OpenAI TTS model
            voice="nova",   # Options: alloy, echo, fable, onyx, nova, shimmer
            input=speech,
            response_format="mp3"
        ) as response:
            # Save to file and play
            output_file = "speech.mp3"
            await response.stream_to_file(output_file)
            
            # Play the audio (Windows)
            os.system(f'start {output_file}')
            # For Linux: os.system(f'mpg123 {output_file}')
            # For Mac: os.system(f'afplay {output_file}')
            
    except Exception as e:
        print(f"⚠️ TTS failed: {e}")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc.")
    content: Optional[str] = Field(None, description="The optional string content for the step.")
    tool: Optional[str] = Field(None, description="The id of the tool to call.")
    input: Optional[str] = Field(None, description="The input parameter for tools.")

SYSTEM_PROMPT = """
You are a helpful AI Assistant specialized in resolving user queries.
You work in start, plan, action, observe mode.

For the given user query and available tools, plan step-by-step execution, 
select relevant tools, and perform actions based on your planning.

Wait for observations and resolve the query based on tool results.

Rules:
- Follow the Output JSON Format
- Always perform one step at a time and wait for next input
- Carefully analyze the user query

Output JSON Format:
{
    "step": "string",
    "content": "string",
    "tool": "The name of function if the step is TOOL",
    "input": "The input parameter for the function"
}

Available Tools:
- "get_weather(city:str)": Takes a city name and returns current weather
- "run_command(cmd:str)": Takes a Linux command and executes it

Example:
START: What is the weather of new york?
PLAN: { "step": "PLAN", "content": "User wants weather data for New York" }
PLAN: { "step": "PLAN", "content": "I should call get_weather" }
TOOL: { "step": "TOOL", "tool": "get_weather", "input": "new york" }
OBSERVE: { "step": "OBSERVE", "content": "12 Degree Cel" }
OUTPUT: { "step": "OUTPUT", "content": "The weather for New York is 12 degrees." }
"""

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

r = sr.Recognizer()
with sr.Microphone() as source: 
    r.adjust_for_ambient_noise(source)
    r.pause_threshold = 2 

while True:
    user_query = input("\n💬 >> ").strip()
    
    if user_query.lower() in ['quit', 'exit', 'q']:
        print("👋 Goodbye!")
        break
    
    if not user_query:
        continue
    
    message_history.append({"role": "user", "content": user_query})
    
    while True:
        response = gemini_client.chat.completions.parse(
            model='gemini-2.0-flash-exp',  # ✅ Fixed model name
            response_format=MyOutputFormat,
            messages=message_history,
        )
        
        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})
        
        parsed_result = response.choices[0].message.parsed
        
        if parsed_result.step == "START":
            print("🚀 START:", parsed_result.content)
            continue
        
        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"🛠️  Calling Tool: {tool_to_call}({tool_input})")
            
            # Actually call the tool
            if tool_to_call == "get_weather":
                result = get_weather(tool_input)
            elif tool_to_call == "run_command":
                result = run_command(tool_input)
            else:
                result = "Unknown tool"
            
            # Add observation to history
            message_history.append({
                "role": "user", 
                "content": f"OBSERVE: Tool '{tool_to_call}' returned: {result}"
            })
            continue
        
        if parsed_result.step == "PLAN":
            print("🧠 PLAN:", parsed_result.content)
            continue
        
        if parsed_result.step == "OUTPUT":
            print("🤖 AI:", parsed_result.content)
            
            # Run TTS asynchronously
            asyncio.run(tts(speech=parsed_result.content))
            break
'''