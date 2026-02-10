# Running LLMs Locally with Docker + Ollama

## Why Run Models Locally?

### Closed-Source Models (Can't run locally):
- ❌ GPT-4, GPT-4o (OpenAI)
- ❌ Gemini (Google)
- Need API access, costs money, data sent to third party

### Open-Source Models (Can run locally):
- ✅ DeepSeek
- ✅ Qwen
- ✅ Llama 3 (Meta)
- ✅ Gemma 2 (Google)

**Benefits:** Privacy, no API costs, data stays on your machine

**Drawback:** Needs good CPU/GPU hardware

---

## Setup Guide

### Step 1: Install Docker

1. Download **Docker Desktop** from `docker.com`
2. Install and launch
3. Verify installation:
```bash
docker --version
docker pull busybox  # Test pull
docker run busybox ls  # Test run
```

---

### Step 2: Install Ollama (via Docker)

```bash
# Pull Ollama image (~2GB)
docker pull ollama/ollama

# Run Ollama container
docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

**What this does:**
- `-d` = Run in background (detached)
- `-v` = Mount volume for model storage
- `-p 11434:11434` = Expose port 11434
- `--name ollama` = Name the container

✅ Ollama engine now running at `localhost:11434`

---

### Step 3: Install Open WebUI (Chat Interface)

```bash
# Pull Open WebUI image (~1GB)
docker pull ghcr.io/open-webui/open-webui:main

# Run Open WebUI container
docker run -d \
  -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

✅ Open WebUI now at `localhost:3000`

---

### Step 4: Setup & Download a Model

1. **Open browser:** `http://localhost:3000`
2. **Create account:** Sign up (local only, not cloud)
3. **Go to:** Settings → Admin Panel → Models
4. **Choose model from** `ollama.com/library`:
   - Gemma 2B (2GB) - Small, fast
   - Llama 3 8B (4.7GB) - Medium
   - DeepSeek (larger) - Advanced

5. **Download model:**
```
Model name: gemma:2b
Click "Download"
```

Wait for download (~2GB for Gemma)

---

### Step 5: Chat with Your Local Model

1. Click "New Chat"
2. Select model: **Gemma:2b**
3. Ask: "Hey there, who are you?"

**Response:** "I'm a large language model trained by Google"

---

## How It Works (Architecture):

```
┌─────────────────────┐
│   Browser (You)     │
│  localhost:3000     │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Open WebUI        │  (Chat Interface)
│   Port 3000         │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Ollama Engine     │  (Model Runner)
│   Port 11434        │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Local Model       │  (Gemma, Llama, etc.)
│   Stored on disk    │
└─────────────────────┘
```

---

## CPU Usage Monitoring

Check Docker Desktop → Container Stats:

| Status | CPU Usage |
|--------|-----------|
| Idle | 0% |
| Answering query | 140-295% (multi-core) |
| Done responding | Drops back to 0% |

---

## Available Models on Ollama:

| Model | Size | Best For |
|-------|------|----------|
| **Gemma 2B** | 2GB | Fast, simple tasks |
| **Llama 3 8B** | 4.7GB | Balanced performance |
| **Qwen 7B** | 4.4GB | Multilingual |
| **DeepSeek** | 8GB+ | Advanced reasoning |
| **Mistral 7B** | 4.1GB | Code generation |

Browse all: `ollama.com/library`

---

## Commands Summary:

```bash
# Check running containers
docker ps

# Stop Ollama
docker stop ollama

# Start Ollama
docker start ollama

# View logs
docker logs ollama

# Remove container
docker rm ollama

# Pull new model (from inside Ollama container)
docker exec -it ollama ollama pull llama3
```

---

## Key Benefits:

✅ **100% Private** - Data never leaves your machine  
✅ **Free** - No API costs  
✅ **Offline** - Works without internet (after download)  
✅ **Customizable** - Run any open-source model  
✅ **Docker** - Easy setup, platform-agnostic  

## Requirements:

⚠️ **Hardware needs:**
- 8GB+ RAM minimum
- 16GB+ recommended
- SSD storage for models
- Multi-core CPU (GPU optional but helps)

---

## Next Steps:

Now you can use Ollama models in Python code (covered in next videos)!


=====================================================


# Using Ollama with FastAPI

## Goal:
Build REST API endpoints so users can interact with your **locally-running Ollama models** via HTTP requests.

---

## Step 1: Install FastAPI

```bash
# Install FastAPI with all features
pip install "fastapi[standard]"

# Save to requirements
pip freeze > requirements.txt
```

---

## Step 2: Basic FastAPI Setup

**File: `server.py`**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/contact-us")
def contact():
    return {"email": "piyushgarg.dev@gmail.com"}
```

**Run server:**
```bash
fastapi dev server.py
```

**Access:**
- Main: `http://localhost:8000`
- Contact: `http://localhost:8000/contact-us`
- **Auto Docs**: `http://localhost:8000/docs` 📄

---

## Step 3: Install Ollama Python SDK

```bash
pip install ollama
pip freeze > requirements.txt
```

---

## Step 4: Connect FastAPI to Ollama

**Make sure Ollama container is running:**
```bash
docker ps  # Should show ollama container on port 11434
```

**Updated `server.py`:**

```python
from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()

# Connect to Ollama running in Docker
client = Client(host="http://localhost:11434")

@app.post("/chat")
def chat(
    message: str = Body(..., description="The message to send")
):
    # Call Ollama with user message
    response = client.chat(
        model="gemma:2b",  # Model you downloaded earlier
        messages=[
            {"role": "user", "content": message}
        ]
    )
    
    # Return the response
    return {"response": response.message.content}
```

---

## Step 5: Test the API

### Option A: Use Auto-Generated Docs

1. Go to `http://localhost:8000/docs`
2. Click on `/chat` endpoint
3. Click "Try it out"
4. Enter message: `"Why is the sky blue?"`
5. Click "Execute"

**Response:**
```json
{
  "response": "The sky appears blue due to Rayleigh light scattering..."
}
```

### Option B: Use cURL

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Who are you?"}'
```

**Response:**
```json
{
  "response": "I am a chatbot designed to assist..."
}
```

### Option C: Use Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What is 2+2?"}
)

print(response.json())
# Output: {"response": "2 + 2 equals 4"}
```

---

## Architecture Overview

```
┌──────────────┐
│   User/App   │
└──────┬───────┘
       │ HTTP POST /chat
       ↓
┌──────────────────┐
│   FastAPI Server │  (Port 8000)
│   server.py      │
└──────┬───────────┘
       │ Ollama Python SDK
       ↓
┌──────────────────┐
│  Ollama Engine   │  (Port 11434)
│  Docker Container│
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│  Gemma 2B Model  │  (Local storage)
└──────────────────┘
```

---

## Complete Code Example

```python
from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()

# Initialize Ollama client
client = Client(host="http://localhost:11434")

@app.get("/")
def root():
    return {"message": "Ollama FastAPI Server"}

@app.post("/chat")
def chat(message: str = Body(..., embed=True)):
    """
    Chat with locally running Ollama model
    
    - **message**: Your question/prompt
    """
    response = client.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    
    return {
        "response": response.message.content,
        "model": "gemma:2b"
    }

@app.get("/models")
def list_models():
    """List available models"""
    models = client.list()
    return {"models": [m.model for m in models.models]}
```

---

## Run the Server

```bash
# Navigate to project folder
cd ollama-fastapi

# Run FastAPI development server
fastapi dev server.py
```

**Output:**
```
INFO:     Uvicorn running on http://localhost:8000
INFO:     Application startup complete.
```

---

## Test with Multiple Questions

**Request 1:**
```json
POST /chat
{
  "message": "Why is the sky blue?"
}
```
**Response:** Explains Rayleigh scattering

**Request 2:**
```json
POST /chat
{
  "message": "Who are you?"
}
```
**Response:** "I am a chatbot designed to assist..."

---

## Key Benefits

✅ **Free API** - No OpenAI/Gemini costs  
✅ **Privacy** - Data stays on your machine  
✅ **Offline** - Works without internet  
✅ **Custom models** - Use any Ollama model  
✅ **Auto docs** - FastAPI generates `/docs`  
✅ **Scalable** - Can add authentication, rate limiting, etc.

---

## Next Steps

You can now:
- Add more endpoints (summarize, translate, etc.)
- Add authentication
- Deploy to production
- Use throughout the course instead of paid APIs!

**Important:** Make sure Ollama Docker container is running before starting FastAPI server.