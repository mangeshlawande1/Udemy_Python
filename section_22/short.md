# The Problem with Synchronous RAG Code

## Current State
✅ Indexing code works
✅ Chat code works
✅ Everything functions correctly

**But there's a fundamental problem...**

---

## The Problem: Synchronous Blocking

### What Happens Now
```
Run index.py → System BLOCKED → Wait 10-20 seconds → Done
                    ↓
        Can't do anything else!
```

### Real-World Scenario
| Files | Pages Each | Estimated Time |
|-------|------------|----------------|
| 1 PDF | 104 pages | ~20 seconds |
| 100 PDFs | 100+ pages | ~30+ minutes |
| 1000 PDFs | 100+ pages | **Hours!** |

**While processing: System is completely blocked** 🔒

---

## Why This is Bad for Production

```python
# Current approach (BLOCKING)
def index_documents():
    # User waits...
    # System frozen...
    # No other requests can be handled...
    process_1000_files()  # Takes hours!
```

**Problems:**
- ❌ Users must wait
- ❌ System unresponsive
- ❌ Can't handle multiple requests
- ❌ Poor user experience
- ❌ Not scalable

---

## The Solution: Asynchronous Processing

```
User uploads file → Returns immediately → Processing happens in background
         ↓                                            ↓
   User continues working              Files being indexed silently
```

**Benefits:**
- ✅ Immediate response to user
- ✅ Background processing
- ✅ Handle multiple requests
- ✅ Better user experience
- ✅ Production-ready

---

## What's Coming Next

| Topic | Purpose |
|-------|---------|
| **FastAPI** | Build async APIs |
| **Background Tasks** | Process without blocking |
| **Async/Await** | Non-blocking code patterns |
| **Production Patterns** | Real-world best practices |

---

## Key Takeaway

> **"If it works, don't touch it"** - Developer Rule
>
> **"If it works but doesn't scale, fix it"** - Production Rule

**Next Section: Asynchronous Programming with Python** 🚀


### 

# System Design: Queues for Asynchronous Processing

## Why System Design Matters for AI
Even in Agentic AI, you need to understand how production systems work!

---

## What is a Queue?

**Queue** = Data structure following **FIFO** (First In, First Out)

```
[Task 1] → [Task 2] → [Task 3] → [Task 4]
   ↑                                 ↑
 First In                        Last In
 First Out                       Last Out
```

---

## The Problem: Synchronous Server

```
User 1: "Explain Node.js" → Server BUSY processing...
                                    ↓
User 2: "Help with Python" → ⏳ Waiting...
User 3: "What is RAG?"     → ⏳ Waiting...
User 4: "Debug my code"    → ⏳ Waiting...
```

**Result:** One user blocks everyone! ❌

---

## The Solution: Queue-Based Architecture

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Users          FastAPI Server         Queue           │
│                                                         │
│   User 1 ──→ ┌──────────────┐                          │
│   User 2 ──→ │   HTTP       │ ──→ [Task1][Task2][Task3]│
│   User 3 ──→ │   Server     │                          │
│              │              │      "Got it, please     │
│              │  (Never      │       wait!"             │
│              │   Busy!)     │                          │
│              └──────────────┘           │              │
│                     ↑                   ↓              │
│                     │         ┌──────────────┐         │
│               Read Result     │  Consumer/   │         │
│                     │         │  Processor   │         │
│                     │         │              │         │
│              ┌──────────────┐ │ (Picks one   │         │
│              │   Database   │←│  at a time)  │         │
│              │   (Results)  │ └──────────────┘         │
│              └──────────────┘                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## How It Works

| Step | Action |
|------|--------|
| 1 | User sends request to server |
| 2 | Server pushes task to queue |
| 3 | Server immediately responds: "Got it, please wait!" |
| 4 | Consumer picks tasks one by one |
| 5 | Consumer processes and stores result in DB |
| 6 | User asks: "What's the status?" |
| 7 | Server reads result from DB and returns |

---

## Benefits

| Synchronous | Asynchronous (Queue) |
|-------------|---------------------|
| Server blocked | Server always free |
| Users wait | Immediate response |
| One at a time | Handle many requests |
| Poor UX | Great UX |
| Not scalable | Highly scalable |

---

## Key Components

1. **FastAPI Server** - Receives requests, pushes to queue
2. **Queue** - Holds tasks in order (FIFO)
3. **Consumer/Processor** - Picks and processes tasks
4. **Database** - Stores results

---

## Coming Up Next
We'll code all of this:
- FastAPI server
- Queue implementation
- Background processors
- Result storage

**Production-ready async RAG system!** 🚀

#### 


# Setting Up Valkey (Redis Alternative) for Job Queues

## What We Need

**RQ (Redis Queue)** - Simple job queue library for Python
- Requires Redis (or Redis-compatible) backend
- We'll use **Valkey** - a drop-in Redis replacement

---

## Why Valkey Instead of Redis?

| Redis | Valkey |
|-------|--------|
| License changed (not fully open source) | Fully open source |
| Works with RQ | Works with RQ |
| Same commands | Same commands |

**Valkey = Drop-in replacement for Redis**
- Code written for Redis works with Valkey
- No changes needed!

---

## Project Structure

```
rag_q/
├── docker-compose.yml
```

---

## Docker Compose Setup

```yaml
services:
  valkey:
    image: valkey/valkey
    ports:
      - "6379:6379"
```

---

## Start Valkey

```bash
# Navigate to rag_q folder
cd rag_q

# Start in detached mode
docker compose up -d
```

---

## Verify Setup

Check Docker Desktop or run:
```bash
docker ps
```

**Running Services:**
| Service | Port | Purpose |
|---------|------|---------|
| Qdrant (Vector DB) | 6333 | Store embeddings |
| Valkey (Queue Backend) | 6379 | Job queue storage |

---

## What's Coming Next

1. **Python RQ** - Job queue library
2. **FastAPI** - HTTP server
3. **Workers** - Background processors
4. **Integration** - Complete async RAG system

---

## Key Takeaway

**Infrastructure ready:**
- ✅ Vector Database (Qdrant) - Port 6333
- ✅ Queue Backend (Valkey) - Port 6379

**Next: Connect FastAPI + RQ for async processing!** 🚀



#######


# Setting Up Python RQ (Redis Queue)

## Installation

```bash
pip install rq
pip freeze > requirements.txt
```

---

## Project Structure

```
rag_q/
├── docker-compose.yml
├── client/
│   └── rq_client.py      # Queue connection
└── queues/
    └── (workers go here)
```

---

## Queue Connection Setup

### `client/rq_client.py`

```python
from redis import Redis
from rq import Queue

# Create Redis connection (works with Valkey too!)
redis_connection = Redis(
    host="localhost",
    port=6379
)

# Create queue instance
queue = Queue(connection=redis_connection)
```

---

## Understanding Producer vs Consumer

```
┌──────────────┐         ┌─────────┐         ┌──────────────┐
│   Producer   │ ──────→ │  Queue  │ ──────→ │   Consumer   │
│  (FastAPI)   │ enqueue │ (Redis) │  pick   │   (Worker)   │
└──────────────┘         └─────────┘         └──────────────┘
```

| Component | Role | Code Location |
|-----------|------|---------------|
| **Producer** | Pushes jobs to queue | `client/rq_client.py` |
| **Consumer** | Picks and processes jobs | `queues/` folder |

---

## Queue Methods Available

```python
queue.enqueue(function, args)     # Add job to queue
queue.enqueue_call(...)           # Add with options
queue.enqueue_in(timedelta, ...)  # Delayed execution
```

---

## What We Have Now

✅ **Valkey** running on port 6379
✅ **Queue connection** configured
✅ **Ready to enqueue** jobs

---

## Next Steps

1. Create **worker functions** in `queues/` folder
2. Set up **FastAPI** to enqueue jobs
3. Start **RQ workers** to process jobs

**Coming up: Setting up RQ Workers!** 🚀


###

# Creating the RQ Worker Function

## What We're Building

```
┌─────────────┐      ┌─────────┐      ┌──────────────────┐      ┌─────────┐
│   FastAPI   │ ──→  │  Queue  │ ──→  │  process_query   │ ──→  │  Redis  │
│  /chat POST │      │         │      │    (Worker)      │      │ (Result)│
└─────────────┘      └─────────┘      └──────────────────┘      └─────────┘
                                              ↓
                                      ┌──────────────────┐
                                      │  /result GET     │ ←── User fetches
                                      └──────────────────┘
```

---

## Project Structure

```
rag_q/
├── docker-compose.yml
├── client/
│   ├── __init__.py       # Make it a module
│   └── rq_client.py
└── queues/
    └── worker.py         # Worker function
```

---

## Worker Code: `queues/worker.py`

```python
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

# Load environment variables
load_dotenv()

# Setup OpenAI client
openai_client = OpenAI()

# Setup embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# Connect to vector database
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model
)

def process_query(query: str):
    """Worker function that processes RAG queries"""
    
    # 1. Search for relevant chunks
    print("Searching chunks...")
    search_results = vector_db.similarity_search(query=query)
    
    # 2. Prepare context
    print("Preparing context...")
    context = "\n\n".join([
        f"Page Content: {result.page_content}\n"
        f"Page Number: {result.metadata.get('page', 'N/A')}\n"
        f"Source: {result.metadata.get('source', 'N/A')}"
        for result in search_results
    ])
    
    # 3. Create system prompt
    system_prompt = f"""You are a helpful AI assistant who answers user queries 
    based on the available context retrieved from a PDF file.
    
    Context:
    {context}
    """
    
    # 4. Call OpenAI
    print("Calling LLM...")
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )
    
    # 5. Return result
    result = response.choices[0].message.content
    print("Done!")
    return result
```

---

## How to Enqueue Jobs

```python
from client.rq_client import queue
from queues.worker import process_query

# This is how FastAPI will enqueue jobs
job = queue.enqueue(process_query, "What is Node.js?")
```

---

## Architecture Overview

| Component | Purpose | File |
|-----------|---------|------|
| **Queue Client** | Connection to Redis/Valkey | `client/rq_client.py` |
| **Worker Function** | Process RAG queries | `queues/worker.py` |
| **FastAPI** | HTTP endpoints | (Next video) |

---

## API Routes We'll Create

| Route | Method | Purpose |
|-------|--------|---------|
| `/chat` | POST | Enqueue user query |
| `/result` | GET | Fetch processing result |

---

## Key Concept

**Worker function runs separately from the API server!**

```
API Server: Receives request → Enqueues → Returns immediately
Worker:     Picks job → Processes → Stores result
API Server: User asks for result → Returns from storage
```

**Next: Setting up FastAPI and tying everything together!** 🚀


###

# Setting Up FastAPI Server

## Installation

```bash
pip install fastapi[standard]
pip freeze > requirements.txt
```

---

## Project Structure

```
rag_q/
├── docker-compose.yml
├── .env                  # API keys
├── main.py               # Entry point
├── server.py             # FastAPI app
├── client/
│   ├── __init__.py
│   └── rq_client.py
└── queues/
    └── worker.py
```

---

## Server Setup: `server.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return "Server is up and running"
```

---

## Entry Point: `main.py`

```python
from dotenv import load_dotenv
import uvicorn
from server import app

# Load environment variables
load_dotenv()

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
```

---

## Environment File: `.env`

```
OPENAI_API_KEY=your_api_key_here
```

---

## Run the Server

```bash
python -m rag_q.main
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Verify Setup

| URL | Purpose |
|-----|---------|
| `http://localhost:8000` | Root endpoint |
| `http://localhost:8000/docs` | Swagger documentation |

---

## Current Architecture

```
┌─────────────────────────────────────────┐
│              FastAPI Server             │
│                                         │
│  GET /  →  "Server is up and running"   │
│                                         │
│  (More endpoints coming...)             │
└─────────────────────────────────────────┘
```

---

## What's Next

| Endpoint | Purpose |
|----------|---------|
| `POST /ingest` | Upload and index documents |
| `POST /chat` | Submit queries to queue |
| `GET /result/{job_id}` | Fetch processing results |

**Next: Creating the ingestion endpoint!** 🚀

###


# Creating the Chat Route with Queue Integration

## What We're Building

```
User sends query → Enqueue job → Return job ID immediately
                       ↓
              Job waits in queue for processing
```

---

## Updated Project Structure

```
rag_q/
├── __init__.py           # NEW: Package imports
├── server.py             # Chat route
├── main.py
├── .env
├── client/
│   ├── __init__.py
│   └── rq_client.py
└── queues/
    └── worker.py
```

---

## Package Imports: `rag_q/__init__.py`

```python
from .client.rq_client import queue
from .queues.worker import process_query
```

---

## Chat Route: `server.py`

```python
from dotenv import load_dotenv
load_dotenv()  # Load BEFORE other imports!

from fastapi import FastAPI, Query

# Import queue and worker
from . import queue, process_query

app = FastAPI()

@app.get("/")
def root():
    return "Server is up and running"

@app.post("/chat")
def chat(query: str = Query(..., description="The chat message of user")):
    # Enqueue the job (doesn't wait for completion!)
    job = queue.enqueue(process_query, query)
    
    # Return job ID immediately
    return {
        "status": "queued",
        "job_id": job.id
    }
```

---

## Important: Load Order

```python
# ✅ CORRECT - Load env first
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
# ... other imports

# ❌ WRONG - Imports before env loaded
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()  # Too late!
```

---

## Testing the Route

**Request:**
```
POST /chat?query=explain arrow functions in JavaScript
```

**Response:**
```json
{
    "status": "queued",
    "job_id": "abc123-def456-..."
}
```

---

## What Happens

| Step | Action | Blocking? |
|------|--------|-----------|
| 1 | User sends query | No |
| 2 | Job enqueued | No |
| 3 | Return job ID | No |
| 4 | Processing | Happens later! |

**Key Point:** The response is **immediate**! Processing happens separately.

---

## Current State

```
┌─────────┐     ┌─────────┐     ┌─────────────┐
│  User   │ ──→ │ FastAPI │ ──→ │    Queue    │
│         │ ←── │  /chat  │     │ (Job waits) │
└─────────┘     └─────────┘     └─────────────┘
     ↑                               
     │ Returns job ID                
     │ (Job NOT processed yet!)      
```

**Problem:** Job is in queue, but no worker is processing it!

---

## Next Steps

1. Create `/result/{job_id}` endpoint to check job status
2. Start RQ worker to actually process jobs

**Next: Fetching job status and results!** 🚀

###


# Creating the Job Status Route

## What We're Building

```
User has job_id → Check job status → Get result (if ready)
```

---

## Updated `server.py`

```python
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query

from . import queue, process_query

app = FastAPI()

@app.get("/")
def root():
    return "Server is up and running"

@app.post("/chat")
def chat(query: str = Query(..., description="The chat message of user")):
    job = queue.enqueue(process_query, query)
    return {
        "status": "queued",
        "job_id": job.id
    }

@app.get("/job_status")
def get_result(job_id: str = Query(..., description="The job ID")):
    # Fetch job from queue
    job = queue.fetch_job(job_id)
    
    # Get return value (None if not completed)
    result = job.return_value
    
    return {
        "result": result
    }
```

---

## Testing the Flow

### Step 1: Submit a Query
```
POST /chat?query=explain arrow functions in JavaScript
```
**Response:**
```json
{
    "status": "queued", 
    "job_id": "abc123..."
}
```

### Step 2: Check Job Status
```
GET /job_status?job_id=abc123...
```
**Response:**
```json
{
    "result": null
}
```

**Result is `null`** because no worker is processing jobs!

---

## Current Problem

```
┌─────────┐     ┌─────────┐     ┌─────────────┐
│  User   │ ──→ │ FastAPI │ ──→ │    Queue    │
│         │     │         │     │             │
└─────────┘     └─────────┘     │ Job 1 ⏳    │
                                │ Job 2 ⏳    │
                                │ (waiting...)│
                                └─────────────┘
                                       ↓
                                   No Worker!
                                   Jobs stuck!
```

---

## Queue Methods Used

| Method | Purpose |
|--------|---------|
| `queue.enqueue(func, args)` | Add job to queue |
| `queue.fetch_job(job_id)` | Get job by ID |
| `job.return_value` | Get result (None if not done) |

---

## What's Missing

❌ **No worker running** to process queued jobs
- Jobs are sitting in queue
- `return_value` is always `None`
- Need to start RQ worker process

---

## Available Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Health check |
| `/chat` | POST | Submit query to queue |
| `/job_status` | GET | Check job result |

---

## Next Step

**Start the RQ Worker** to actually process jobs in the background!

**Next: Running the background processor!** 🚀


### 

# Running RQ Workers for Background Processing

## The Problem
Jobs are queued but no worker is processing them!

---

## Starting RQ Worker

### Basic Command
```bash
cd rag_q
rq worker
```

### Mac OS Fix (Important!)
If on Mac OS, you need to set this environment variable first:

```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
rq worker
```

---

## Worker Setup: Update `worker.py`

```python
from dotenv import load_dotenv
load_dotenv()  # Load env in worker process too!

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

# ... rest of the code
```

**Important:** Worker runs in a separate process, needs its own env loading!

---

## Running the System

### Terminal 1: FastAPI Server
```bash
python -m rag_q.main
```

### Terminal 2: RQ Worker
```bash
cd rag_q
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES  # Mac only
rq worker
```

---

## Testing the Flow

### 1. Submit Jobs (while worker is stopped)
```
POST /chat?query=explain debugging in JavaScript
POST /chat?query=explain arrow functions
```

### 2. Check Status (returns null - not processed)
```
GET /job_status?job_id=xxx
→ {"result": null}
```

### 3. Start Worker
```bash
rq worker
```
**Worker output:**
```
Searching chunks...
Preparing context...
Calling LLM...
Done!
```

### 4. Check Status Again (returns result!)
```
GET /job_status?job_id=xxx
→ {"result": "Arrow functions are..."}
```

---

## Scaling with Multiple Workers

```bash
# Terminal 2
rq worker

# Terminal 3
rq worker

# Terminal 4
rq worker
```

**3 workers = 3 parallel job processing!**

```
┌─────────┐     ┌─────────────┐     ┌──────────┐
│  Queue  │ ──→ │  Worker 1   │ ──→ │ Process  │
│         │ ──→ │  Worker 2   │ ──→ │ Parallel │
│ Job 1   │ ──→ │  Worker 3   │ ──→ │ Jobs!    │
│ Job 2   │     └─────────────┘     └──────────┘
│ Job 3   │
└─────────┘
```

---

## Complete Architecture

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  User ──→ FastAPI ──→ Queue (Valkey) ──→ Workers ──→ Result│
│              │              │               │              │
│         /chat POST     Stores Jobs     Processes        Redis
│         /job_status    (FIFO)          in parallel     Storage
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Key Commands Summary

| Command | Purpose |
|---------|---------|
| `python -m rag_q.main` | Start FastAPI server |
| `rq worker` | Start one worker |
| `export OBJC_DISABLE...` | Mac OS fix |

---

## Benefits Achieved

| Before (Sync) | After (Async + Queue) |
|---------------|----------------------|
| Server blocked | Server always free |
| One request at a time | Many parallel requests |
| User waits | Instant response |
| Not scalable | Add more workers = more throughput |

**Congratulations! You've built a production-ready async RAG system!** 🎉


