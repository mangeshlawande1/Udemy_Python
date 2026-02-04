# Scalable Rag with Async Queues &distributed workers 

154--162

### 154 
as we see before is a synchronous code 
the console is getting blocked , i dont do nothing now 

- it wait until the process is complete,
- we can run the things in background let user do whatever he want 

*Introduction to Queues*
- python fastapi server --> 
to resolve user query   
here , the server is busy to resolve the current user query, while other user is blocking mode .

- rather than everything here push the request in queue(got req, please wait), 
- the separate processor function known as consumer/processor 
    - it pick up task at a time , it goinig to do processing store thed result some kinf of db  ,
    whenever user ask jobs, its read ready response and give it back .

hence server is never busy in doing the retrieval.

156. Simple job Queues for python 
Simple job queue for  python.
- RQ (Redis Queue) is a simple Python library for queuing jobs and processing them in the background with workers. It uses the Redis in-memory data store as a message broker and is designed for a low barrier to entry and easy integration into Python applications. 


### Redis/ Valkey
- you can easily setup redis locally .
:: redis open source licence was revoked.

- valkey is dropin replacement for redis, setup the valkey.

> docker compose up -d 

How can we use RQ 
how we can setup the RQ 

1. need to setup the queues 
2. create a folder known as client.

how to setup workers in python rq  

158. 

# workerirchestration with Python RQ

Fastapi server  
POST /chat {message } [enqueue a msg into the queue ]

- processor fun take the uery and process it and store the data in redis 

/ result -- roe fetching the result 

#### Setup Fastapi


Setup endpoint for ingestion    

- fetch current status of job 

- how to run process function in background .


cmd to run terminal 
 rq-worker 



 ----------------------------------
 Great, you’re now touching **real backend architecture** — this is exactly how production RAG / AI systems are built.
Let’s go **slow, layered, and precise**, because queues are a *mental shift*, not just code.

---

# 1. The Core Problem (Why synchronous code breaks)

### What you have now (synchronous)

```
User → FastAPI → RAG pipeline → LLM → Response
```

### What goes wrong

* Request **blocks** the server
* CPU / network / LLM latency
* Other users wait
* Server looks “busy” even though work is just *waiting*

Example:

* User A uploads 100 PDFs
* Indexing takes 30 seconds
* User B calls `/chat`
  ❌ User B is blocked

---

# 2. The Core Idea: Queues

Instead of *doing the work immediately*:

> **Accept request → enqueue job → respond instantly**

Then:

* Background workers do the heavy work
* Server stays responsive
* Users can poll for results

---

## Mental Model (VERY IMPORTANT)

```
FastAPI (producer)
   |
   | enqueue job
   ↓
Queue (Redis / Valkey)
   ↓
Worker (consumer)
   |
   | process job
   ↓
Result store (Redis / DB)
```

### Key principle

👉 **Web servers should not do heavy work**

---

# 3. Producer–Consumer Architecture

| Component | Role                          |
| --------- | ----------------------------- |
| FastAPI   | Producer (enqueue jobs)       |
| Queue     | Buffer                        |
| Worker    | Consumer (process jobs)       |
| Redis     | Message broker + result store |

---

# 4. Why RQ (Redis Queue)?

### What is RQ?

RQ is:

* Simple job queue
* Python-native
* Redis-backed
* No complex config (unlike Celery)

### Why RQ is perfect here

* Low learning curve
* Perfect for AI workloads
* Easy FastAPI integration

---

# 5. Redis vs Valkey

### Redis issue

* License changed
* Not fully open anymore

### Valkey

* Open source
* Drop-in replacement
* Same protocol
* Same client libraries

👉 **RQ works with Valkey without changes**

---

# 6. Setup Valkey with Docker Compose

### `docker-compose.yml`

```yaml
version: "3.8"

services:
  valkey:
    image: valkey/valkey
    container_name: valkey
    ports:
      - "6379:6379"
```

### Start it

```bash
docker compose up -d
```

Test:

```bash
redis-cli ping
# PONG
```

(Valkey responds as Redis)

---

# 7. Install Dependencies

```bash
pip install fastapi uvicorn rq redis
```

---

# 8. Project Structure (Clean & Scalable)

```plaintext
project/
├── app/
│   ├── main.py          # FastAPI server
│   ├── queue.py         # Queue setup
│   ├── tasks.py         # Background jobs
│   └── worker.py        # Worker entry
├── client/
│   └── submit_job.py
├── docker-compose.yml
```

---

# 9. Setup the Queue (`queue.py`)

```python
from redis import Redis
from rq import Queue

redis_conn = Redis(host="localhost", port=6379)
task_queue = Queue("rag-tasks", connection=redis_conn)
```

This queue:

* Stores jobs
* Persists state
* Handles retries

---

# 10. Background Processor (Consumer)

### `tasks.py`

```python
import time

def process_query(job_id: str, message: str):
    # Simulate heavy RAG work
    time.sleep(10)

    result = f"Processed message: {message}"

    return result
```

👉 This function **never runs inside FastAPI**

---

# 11. FastAPI as Producer

### `main.py`

```python
from fastapi import FastAPI
from app.queue import task_queue
from app.tasks import process_query

app = FastAPI()

@app.post("/chat")
def chat(message: str):
    job = task_queue.enqueue(process_query, message)
    return {
        "job_id": job.id,
        "status": "queued"
    }
```

### What happens

* Request accepted immediately
* Job pushed to queue
* User is NOT blocked

---

# 12. Job Status & Result Endpoint

```python
from rq.job import Job
from app.queue import redis_conn

@app.get("/result/{job_id}")
def get_result(job_id: str):
    job = Job.fetch(job_id, connection=redis_conn)

    if job.is_finished:
        return {"status": "done", "result": job.result}

    if job.is_failed:
        return {"status": "failed"}

    return {"status": job.get_status()}
```

---

# 13. Worker Setup (MOST IMPORTANT PART)

Workers are **separate processes**

### `worker.py`

```python
from redis import Redis
from rq import Worker, Queue

redis_conn = Redis(host="localhost", port=6379)
queue = Queue("rag-tasks", connection=redis_conn)

worker = Worker([queue], connection=redis_conn)
worker.work()
```

---

## Run the worker (terminal)

```bash
rq worker rag-tasks
```

Or explicitly:

```bash
rq-worker rag-tasks
```

👉 This process:

* Blocks
* Waits for jobs
* Processes one job at a time

---

# 14. End-to-End Flow (RAG example)

```
POST /chat
 → enqueue(query)
 → return job_id

Worker
 → retrieve docs
 → vector search
 → LLM call
 → store result

GET /result/{job_id}
 → return answer
```

---

# 15. Why This Fixes Blocking

| Without Queue | With Queue         |
| ------------- | ------------------ |
| Server blocks | Server always free |
| Users wait    | Users async        |
| Poor scale    | Horizontal scale   |
| Hard retries  | Built-in retries   |

---

# 16. Scaling the System

### Add more workers

```bash
rq worker rag-tasks
rq worker rag-tasks
rq worker rag-tasks
```

Each worker:

* Processes one job
* Parallelism achieved

---

# 17. Where RAG Fits in This

Your **RAG pipeline goes inside `process_query()`**

```python
def process_query(message):
    chunks = retrieve_chunks(message)
    answer = llm_answer(chunks, message)
    return answer
```

FastAPI **never touches embeddings or LLMs directly**.

---

# 18. Production Notes (Important)

* Store results in Redis / DB
* Add job TTL
* Add retry logic
* Add rate limiting
* Add auth
* Add job priority queues

---

# 19. One-Line Summary

> **Queues decouple user requests from heavy processing, keeping your server responsive and scalable.**

---

If you want next, I can:

* Integrate **RQ + RAG pipeline**
* Show **progress updates**
* Add **job cancellation**
* Compare **RQ vs Celery**
* Dockerize **FastAPI + Worker + Valkey**
* Build **async UI polling**

