from dotenv import load_dotenv
import speech_recognition as  sr 
from openai import OpenAI
import os 
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async def tts(speech:str):
   async with async_client.audio.speech.with_streaming_response.create(
        model="gemini-2.5-flash-tts",
        voice="coral",
        instructions="Always speak in cheerfull manner with full of delightand happy. ",
        input=speech,
        response_format="pcm",
    ) as response:
       await  LocalAudioPlayer().play(response)





def main():
    r = sr.Recognizer() # Speech to Text 
    
    with sr.Microphone() as source: # mic access 
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2 

        print("Speak Something.... ")
        audio = r.listen(source)

        print("Procesing Audio... (STT)")
        stt = r.recognize_google(audio) 
       
        print("You Said ...", stt)

        SYSTM_PROMPT = f"""
            You're an ai expert voice agent, You are given the teranscript of what user has said using voice .
            You need to output as if you are an voice agent and whatever you speak 
            will be converted back to audio using AI and play back to user.
        """

        response = client.chat.completions.create(
        model='gemini-3-flash-preview',
        # model="llama-3.3-70b-versatile",

        messages=[
            {"role":"system", "content":SYSTM_PROMPT },
            {"role":"user", "content":stt }
        ]
    )
        
    ai_response = response.choices[0].message.content

    print("AI:", ai_response)
    asyncio.run(tts(speech = ai_response))
        

"""


"""



main()