# LangGraph - The Persistence Problem

## The Problem

### Current Behavior
```python
# Run 1: Tell AI your name
state = {"messages": ["My name is Piyush"]}
# AI: "Hello Piyush! How can I assist you?"
# State exists in memory ✓

# --- Application ends, state deleted ---

# Run 2: Ask AI your name
state = {"messages": ["What is my name?"]}  # Fresh state!
# AI: "I don't know your name based on current conversation"
# Previous state is GONE ✗
```

---

## Visual Explanation

### Run 1
```
┌─────────────────────────────────────┐
│           In-Memory State           │
│  messages: ["My name is Piyush",    │
│             "Hello Piyush!"]        │
└─────────────────────────────────────┘
                   ↓
            App terminates
                   ↓
              State DELETED
```

### Run 2 (New Session)
```
┌─────────────────────────────────────┐
│       Fresh In-Memory State         │
│  messages: ["What is my name?"]     │
│                                     │
│  (No history from Run 1!)           │
└─────────────────────────────────────┘
```

---

## Why This Happens

| Aspect | Current Behavior |
|--------|-----------------|
| State storage | RAM (memory) only |
| Persistence | ❌ None |
| After app restart | State is lost |
| Conversation history | Not maintained |

---

## Real-World Impact

**Without persistence:**
- ❌ Users can't continue conversations
- ❌ Context lost between sessions
- ❌ No memory of previous interactions
- ❌ Every run starts fresh

**With persistence:**
- ✅ Conversations continue across sessions
- ✅ AI remembers user context
- ✅ State saved to database
- ✅ Production-ready chatbots

---

## The Solution: Checkpointing

**Checkpointing** = Saving state to persistent storage

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Run 1      │ ──→ │  Checkpoint  │ ──→ │   Run 2      │
│ "My name is  │     │   (Save)     │     │ "What is my  │
│  Piyush"     │     │   Database   │     │  name?"      │
└──────────────┘     └──────────────┘     └──────────────┘
                           ↓
                     State Restored!
                     AI knows: "Piyush"
```

---

## Coming Up

1. **What is Checkpointing?**
2. **Types of Checkpointers**
   - Memory (temporary)
   - SQLite (file-based)
   - PostgreSQL (production)
3. **Implementing Checkpoints in LangGraph**

---

## Key Takeaway

> **In-memory state = Lost when app stops**
> **Checkpointed state = Persisted forever**

**Next: Implementing checkpointing for persistent conversations!** 🚀


# Setting Up MongoDB for LangGraph Checkpointing

## Why MongoDB?

**Checkpointing** requires persistent storage. MongoDB will store:
- Conversation state
- Message history
- Graph execution snapshots

---

## Docker Compose Setup

### File: `langgraph_learning/docker-compose.yml`

```yaml
services:
  mongodb:
    image: mongo
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=admin
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

---

## Configuration Explained

| Setting | Value | Purpose |
|---------|-------|---------|
| `image` | `mongo` | Official MongoDB image |
| `ports` | `27017:27017` | MongoDB default port |
| `MONGO_INITDB_ROOT_USERNAME` | `admin` | Database username |
| `MONGO_INITDB_ROOT_PASSWORD` | `admin` | Database password |
| `volumes` | `mongodb_data` | Persist data across restarts |

---

## Start MongoDB

### Prerequisites
- Docker Desktop running
- Docker engine started

### Commands
```bash
# Navigate to project folder
cd langgraph_learning

# Start MongoDB
docker compose up -d
```

---

## Verify Setup

### Option 1: Docker Desktop
- Open Docker Desktop
- Check Containers
- `langgraph_learning` → `mongodb` should be running

### Option 2: Terminal
```bash
docker ps
```

**Output:**
```
CONTAINER ID   IMAGE   COMMAND                  PORTS
abc123...      mongo   "docker-entrypoint..."   0.0.0.0:27017->27017/tcp
```

---

## Connection Details

| Property | Value |
|----------|-------|
| Host | `localhost` |
| Port | `27017` |
| Username | `admin` |
| Password | `admin` |
| Connection String | `mongodb://admin:admin@localhost:27017` |

---

## Project Structure

```
langgraph_learning/
├── docker-compose.yml    # MongoDB setup
├── chat.py               # Basic LangGraph
├── chat_2.py             # Conditional edges
└── .env                  # API keys
```

---

## What's Next?

1. ✅ MongoDB running
2. ⏳ Install LangGraph MongoDB checkpointer
3. ⏳ Configure checkpointing in graph
4. ⏳ Test persistent conversations

**Next: Implementing checkpointing with MongoDB!** 🚀


# LangGraph Checkpointing with MongoDB

## Overview
Store conversation state persistently in MongoDB so users can continue conversations across sessions.

---

## Installation

```bash
pip install pymongo langgraph-checkpoint-mongodb
pip freeze > requirements.txt
```

---

## Complete Code: `chat_checkpoint.py`

```python
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

# Initialize LLM
llm = init_chat_model(model="gpt-4.1-mini", model_provider="openai")

# Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Create Graph Builder
graph_builder = StateGraph(State)

# Chatbot Node
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Register node
graph_builder.add_node("chatbot", chatbot)

# Add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile function with checkpointer
def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

# MongoDB connection string
DB_URI = "mongodb://admin:admin@localhost:27017"

# Configuration with thread_id (user scope)
config = {"configurable": {"thread_id": "piyush"}}

# Run with checkpointing
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph = compile_graph_with_checkpointer(checkpointer)
    
    # Stream the response
    for chunk in graph.stream(
        {"messages": ["What is my name?"]},
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
```

---

## Key Concepts

### Thread ID (Scope)
```python
# Each user gets their own conversation history
config = {"configurable": {"thread_id": "piyush"}}  # Piyush's history
config = {"configurable": {"thread_id": "john"}}    # John's history
```

### Connection String Format
```
mongodb://username:password@host:port
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                         MongoDB                              │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │  Thread: piyush │    │  Thread: john   │                │
│  │  ─────────────  │    │  ─────────────  │                │
│  │  "My name is    │    │  "My name is    │                │
│  │   Piyush"       │    │   John"         │                │
│  │  "Hello Piyush" │    │  "Hello John"   │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## Testing Persistence

### Session 1: Set Name
```python
# thread_id = "piyush"
{"messages": ["My name is Piyush"]}
# AI: "Hello Piyush!"
```

### Session 2: Ask Name (Later/New Run)
```python
# thread_id = "piyush"
{"messages": ["What is my name?"]}
# AI: "Your name is Piyush!"  ← Remembered!
```

### Different User
```python
# thread_id = "john"
{"messages": ["What is my name?"]}
# AI: "I don't have that information"  ← Separate scope!
```

---

## Streaming vs Invoke

### Invoke (Get final result)
```python
result = graph.invoke({"messages": [...]}, config)
```

### Stream (Real-time chunks)
```python
for chunk in graph.stream({"messages": [...]}, config, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
```

---

## Common Issues

### Authentication Failed
```python
# Wrong
"mongodb://localhost:27017"

# Correct (with credentials)
"mongodb://admin:admin@localhost:27017"
```

### Connection Closed Early
```python
# Wrong - connection closes before use
def compile():
    with MongoDBSaver... as cp:
        return graph  # Connection closed!

# Correct - use within context
with MongoDBSaver... as checkpointer:
    graph = compile(checkpointer)
    graph.invoke(...)  # Inside context
```

---

## Summary

| Feature | Without Checkpointing | With Checkpointing |
|---------|----------------------|-------------------|
| State persistence | ❌ Lost on restart | ✅ Saved to MongoDB |
| Conversation memory | ❌ None | ✅ Full history |
| Multi-user support | ❌ N/A | ✅ Via thread_id |
| Production ready | ❌ No | ✅ Yes |

---

## Key Takeaways

1. **`thread_id`** = User/conversation scope
2. **MongoDB** = Persistent storage for state
3. **Checkpointer** = Passed during `compile()`
4. **Context manager** = Keep connection open during use

**Now your LangGraph has persistent memory!** 🧠💾
