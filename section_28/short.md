# Conversational Voice Agents - Introduction

## What are Voice Agents?

**Voice Agents** = AI that can listen to you speak and respond with voice

Instead of:
```
Text Input → LLM → Text Output
```

We want:
```
Voice Input → AI → Voice Output
```

---

## Why Voice Agents?

| Scenario | Text Agents | Voice Agents |
|----------|-------------|--------------|
| Driving | ❌ Dangerous | ✅ Hands-free |
| Multitasking | ❌ Need to type | ✅ Just talk |
| Accessibility | Limited | ✅ Natural interaction |
| Customer Support | Chatbots | ✅ Phone calls |
| Sales | Manual | ✅ Automated calls |

**Voice Agents = Next Big Thing!** 🚀

---

## Use Cases

- 📞 Customer support
- 💼 Sales executives
- 🏥 Healthcare assistants
- 📅 Appointment scheduling
- 🎓 Education & tutoring
- 🤖 Personal assistants

---

## The Technical Challenge

### Why Can't We Just Feed Voice to LLMs?

**LLMs (Transformers) work with:**
- Input: Text tokens (numbers)
- Output: Probability of next tokens

**Voice is:**
- Sound waves (spectrum)
- Different accents
- Different pitches
- Different speeds
- Continuous (not discrete tokens)

**Problem:** You can't directly convert voice waves into token probabilities!

---

## Two Architectures for Voice Agents

### 1. Speech-to-Speech (S2S)
```
Voice In → Model → Voice Out
```

### 2. Chained Architecture
```
Voice → STT → Text → LLM → Text → TTS → Voice
```

---

## Speech-to-Speech (S2S) Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   User Audio ───→ [ S2S Model ] ───→ Audio Output          │
│                        ↓                                    │
│               (Tool calls, search, etc.)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Pros & Cons

| ✅ Pros | ❌ Cons |
|---------|---------|
| Low latency | Very expensive |
| Real-time | Limited scope |
| Natural conversation | Specific use cases only |
| Native audio handling | Less flexible |

### Best For
- Real-time customer support calls
- Sales calls
- Simple, focused voice interactions

---

## Key Insight

> **Even S2S internally uses a chain-like architecture!**

Understanding the **Chained Architecture** is fundamental to understanding all voice AI systems.

---

## What's Coming

1. ⏳ **Chained Architecture** - The foundation (next video)
2. ⏳ Build voice agent with chained approach
3. ⏳ Explore S2S implementation
4. ⏳ Real-time voice applications

**Next: Understanding Chained Architecture!** 🎙️



# Chained Architecture & Speech-to-Text (STT)

## Chained Architecture Explained

```
┌─────────────────────────────────────────────────────────────┐
│                   CHAINED ARCHITECTURE                      │
│                                                             │
│  User Voice ──→ [STT] ──→ Text ──→ [LLM] ──→ Text ──→ [TTS] ──→ Audio
│                  │                  │                  │     │
│            Speech-to-Text    Any Model      Text-to-Speech  │
│                              (GPT, Claude,                  │
│                               Gemini, etc.)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Chained vs S2S Comparison

| Aspect | Chained | S2S |
|--------|---------|-----|
| Flexibility | ✅ Any LLM | ❌ Specific models only |
| Cost | ✅ Lower | ❌ Expensive |
| Latency | ❌ Higher | ✅ Lower |
| Tool calling | ✅ Full support | Limited |
| LangGraph/LangChain | ✅ Yes | Limited |
| Model choice | ✅ GPT, Claude, Gemini, etc. | ❌ Only S2S models (4o-realtime) |

---

## Step 1: Speech-to-Text (STT)

### Installation

```bash
pip install SpeechRecognition
pip freeze > requirements.txt
```

### MacOS Additional Setup
```bash
brew install portaudio
pip install pyaudio
```

---

## Code: `voice_agent/main.py`

```python
import speech_recognition as sr

def main():
    # Create recognizer
    r = sr.Recognizer()
    
    # Access microphone
    with sr.Microphone() as source:
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        
        print("Speak something...")
        
        # Listen (stops after 2 seconds of silence)
        audio = r.listen(source)
        
        print("Processing audio...")
        
        # Convert speech to text using Google
        stt = r.recognize_google(audio)
        
        print(f"User said: {stt}")

if __name__ == "__main__":
    main()
```

---

## How It Works

```
1. sr.Recognizer() → Create speech recognizer
2. sr.Microphone() → Access user's mic
3. adjust_for_ambient_noise() → Background noise cancellation
4. r.listen(source) → Capture audio
5. r.recognize_google(audio) → Convert to text
```

---

## Run the Code

```bash
cd voice_agent
python main.py
```

**Output:**
```
Speak something...
(You speak: "Hey there agent, how are you doing?")
Processing audio...
User said: hey there agent how are you doing
```

---

## STT Providers Available

```python
r.recognize_google(audio)      # Google (free, default)
r.recognize_whisper(audio)     # OpenAI Whisper
r.recognize_sphinx(audio)      # CMU Sphinx (offline)
r.recognize_bing(audio)        # Microsoft Bing
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `Could not find PyAudio` | MacOS: `brew install portaudio` + `pip install pyaudio` |
| `No microphone found` | Check system permissions |
| `Recognition failed` | Check internet connection (for Google) |

---

## Progress

```
Chained Architecture Steps:
[✅] STT - Speech to Text ← Done!
[ ] LLM - Language Model Processing
[ ] TTS - Text to Speech
```

**Next: Connecting to LLM (GPT-4, etc.)!** 🎙️


# Complete Voice Agent with LLM & TTS

## Architecture Complete

```
User Voice → [STT] → Text → [LLM] → Text → [TTS] → Audio
              ✅           ✅            ✅
```

---

## Installation

```bash
pip install openai-voice-helpers
pip freeze > requirements.txt
```

---

## Complete Code: `voice_agent/main.py`

```python
import asyncio
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer

# Load environment
load_dotenv()

# Create clients
client = OpenAI()
async_client = AsyncOpenAI()

# System prompt for voice agent
system_prompt = """You are an expert voice agent. 
You are given the transcript of what user has said using voice. 
You need to output as if you are a voice agent and whatever you speak 
will be converted back to audio using AI and played back to user."""

# Message history for conversation
messages = [
    {"role": "system", "content": system_prompt}
]

async def tts(speech: str):
    """Text to Speech - Convert text to audio and play"""
    async with async_client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="coral",
        instructions="Always speak in cheerful manner with full of delight and happiness",
        input=speech,
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)

def main():
    global messages
    
    # Create recognizer
    r = sr.Recognizer()
    
    while True:
        # Access microphone
        with sr.Microphone() as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source)
            
            print("Speak something...")
            
            # Listen for audio
            audio = r.listen(source)
            
            print("Processing audio...")
            
            # STT: Convert speech to text
            try:
                stt = r.recognize_google(audio)
                print(f"User said: {stt}")
            except sr.UnknownValueError:
                print("Could not understand audio")
                continue
            
            # Add user message to history
            messages.append({"role": "user", "content": stt})
            
            # LLM: Get AI response
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )
            
            ai_response = response.choices[0].message.content
            print(f"AI response: {ai_response}")
            
            # Add AI response to history
            messages.append({"role": "assistant", "content": ai_response})
            
            # TTS: Convert text to speech and play
            asyncio.run(tts(ai_response))

if __name__ == "__main__":
    main()
```

---

## Voice Options

| Voice | Style |
|-------|-------|
| `alloy` | Neutral |
| `coral` | Friendly |
| `echo` | Male |
| `fable` | British |
| `nova` | Female |
| `onyx` | Deep male |
| `shimmer` | Soft female |

Try them at: https://openai.fm

---

## Example Conversation

```
Speak something...
User: "Hi agent, how are you?"
Processing audio...
AI response: "Hello! I'm doing great. Thank you for asking. How can I assist you today?"
🔊 (Audio plays)

Speak something...
User: "My name is Piyush"
Processing audio...
AI response: "Hello Piyush! Nice to meet you. How can I help you today?"
🔊 (Audio plays)

Speak something...
User: "What is my name?"
Processing audio...
AI response: "Your name is Piyush!"
🔊 (Audio plays)
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    CONVERSATION LOOP                        │
│                                                             │
│  1. 🎤 Listen for user voice                               │
│         ↓                                                   │
│  2. 📝 STT: Convert to text (Google)                       │
│         ↓                                                   │
│  3. 💬 Append to message history                           │
│         ↓                                                   │
│  4. 🧠 LLM: Get AI response (GPT-4.1-mini)                 │
│         ↓                                                   │
│  5. 💬 Append AI response to history                       │
│         ↓                                                   │
│  6. 🔊 TTS: Convert to audio & play                        │
│         ↓                                                   │
│  7. 🔄 Loop back to step 1                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Components

| Step | Component | Library |
|------|-----------|---------|
| STT | `speech_recognition` | Google Speech API |
| LLM | `OpenAI` | GPT-4.1-mini |
| TTS | `AsyncOpenAI` | OpenAI TTS API |
| Audio | `LocalAudioPlayer` | openai-voice-helpers |

---

## Files Needed

```
voice_agent/
├── main.py
├── .env (OPENAI_API_KEY=...)
└── requirements.txt
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| PyAudio error | `brew install portaudio && pip install pyaudio` |
| No audio output | Check system audio settings |
| STT not working | Check microphone permissions |
| API key error | Verify `.env` file |

---

## Summary

**You built a complete voice agent using chained architecture!**

- ✅ STT: Speech Recognition (Google)
- ✅ LLM: OpenAI GPT-4.1-mini
- ✅ TTS: OpenAI Text-to-Speech
- ✅ Conversation history maintained
- ✅ Continuous conversation loop

**This is the foundation for building:**
- Customer support bots
- Sales assistants
- Personal voice assistants
- Interactive voice applications

🎉 **Congratulations!**

==========================================

# Building a Voice-Controlled Cursor Agent

## What We're Building

Converting the text-based cursor agent (from earlier) into a **voice-controlled coding assistant**.

```
Voice Command: "Create a todo app with dark theme"
         ↓
   [STT] → [LLM + Tools] → [TTS]
         ↓
Agent creates files and speaks back to you!
```

---

## Complete Code: `voice_agent/cursor.py`

```python
import os
import json
import asyncio
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

# Clients
client = OpenAI()
async_client = AsyncOpenAI()

# Tools
def run_command(command: str):
    """Execute system command"""
    result = os.system(command)
    return result

def get_weather(city: str):
    """Get weather for a city"""
    import requests
    url = f"https://wttr.in/{city.lower()}?format=3"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"

available_tools = {
    "run_command": run_command,
    "get_weather": get_weather
}

# Output format
class MyOutputFormat(BaseModel):
    step: str = Field(description="Step type: plan, output, tool")
    content: Optional[str] = Field(default=None)
    tool: Optional[str] = Field(default=None)
    input: Optional[str] = Field(default=None)

# System prompt
system_prompt = """You are a voice-controlled AI coding assistant.
You can create files, run commands, and help with coding tasks.

Available tools:
- run_command: Takes a Linux command as string and executes it
- get_weather: Takes city name and returns weather

Steps: plan → tool (if needed) → output

Always respond concisely as your response will be spoken aloud.
"""

# TTS function
async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="coral",
        instructions="Speak clearly and concisely",
        input=speech,
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)

# Main function
def main():
    r = sr.Recognizer()
    message_history = [{"role": "system", "content": system_prompt}]
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2
        
        while True:
            print("\nSpeak something...")
            audio = r.listen(source)
            print("Processing audio...")
            
            try:
                user_query = r.recognize_google(audio)
                print(f"User said: {user_query}")
            except sr.UnknownValueError:
                print("Could not understand audio")
                continue
            
            message_history.append({"role": "user", "content": user_query})
            
            # Agent loop
            while True:
                response = client.beta.chat.completions.parse(
                    model="gpt-4.1",
                    messages=message_history,
                    response_format=MyOutputFormat
                )
                
                parsed_result = response.choices[0].message.parsed
                
                if parsed_result.step == "plan":
                    print(f"🧠 Plan: {parsed_result.content}")
                    message_history.append({
                        "role": "assistant", 
                        "content": json.dumps(parsed_result.dict())
                    })
                    continue
                
                if parsed_result.step == "tool":
                    tool_name = parsed_result.tool
                    tool_input = parsed_result.input
                    print(f"🔧 Tool: {tool_name}({tool_input})")
                    
                    tool_result = available_tools[tool_name](tool_input)
                    
                    message_history.append({
                        "role": "developer",
                        "content": json.dumps({
                            "step": "observe",
                            "tool": tool_name,
                            "output": str(tool_result)
                        })
                    })
                    continue
                
                if parsed_result.step == "output":
                    output = parsed_result.content
                    print(f"✅ Output: {output}")
                    
                    # Speak the output!
                    asyncio.run(tts(output))
                    
                    message_history.append({
                        "role": "assistant",
                        "content": output
                    })
                    break

if __name__ == "__main__":
    main()
```

---

## Example Conversation

```
Speak something...
User: "Create a dark themed todo app using HTML, CSS and JavaScript"

🧠 Plan: I'll create a todo application with dark theme...
🔧 Tool: run_command(mkdir todo_app)
🔧 Tool: run_command(touch todo_app/index.html)
🔧 Tool: run_command(echo '...' > todo_app/index.html)
🔧 Tool: run_command(touch todo_app/style.css)
🔧 Tool: run_command(echo '...' > todo_app/style.css)
🔧 Tool: run_command(touch todo_app/script.js)
🔧 Tool: run_command(echo '...' > todo_app/script.js)

✅ Output: "Your dark themed todo application is ready..."
🔊 (Speaks the output)
```

---

## What Changed from Text to Voice

| Text Version | Voice Version |
|--------------|---------------|
| `input("Query: ")` | `r.recognize_google(audio)` |
| `print(output)` | `asyncio.run(tts(output))` |
| Keyboard input | Microphone input |
| Screen output | Speaker output |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                VOICE CURSOR AGENT                           │
│                                                             │
│  🎤 "Create a todo app" (Voice)                            │
│         ↓                                                   │
│  [STT] Convert to text                                     │
│         ↓                                                   │
│  [Agent Loop]                                              │
│     ├── Plan                                               │
│     ├── Tool calls (run_command, etc.)                     │
│     └── Output                                             │
│         ↓                                                   │
│  [TTS] Convert response to speech                          │
│         ↓                                                   │
│  🔊 "Your app is ready..." (Voice)                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Files Created by Agent

```
todo_app/
├── index.html   (Dark themed HTML)
├── style.css    (Dark theme styles)
└── script.js    (Todo functionality)
```

---

## Key Takeaway

**Any text-based agent can become a voice agent by:**
1. Replacing `input()` with STT (Speech-to-Text)
2. Replacing final `print()` with TTS (Text-to-Speech)

```python
# Before (Text)
user_query = input("Query: ")
print(output)

# After (Voice)
user_query = r.recognize_google(audio)
asyncio.run(tts(output))
```

---

## Summary

You've built a **voice-controlled AI coding assistant** that can:
- ✅ Listen to voice commands
- ✅ Create files and folders
- ✅ Write code
- ✅ Execute system commands
- ✅ Speak back results

**This is real voice-to-voice AI automation!** 🎉

