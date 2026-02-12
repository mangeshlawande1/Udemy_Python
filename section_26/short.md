# Memory in AI Agents - Introduction

## The Problem: Context Window Limitations

### What is Context Window?
Every LLM has a **fixed context window** (e.g., 1 million tokens max).

### The Issue
```
┌─────────────────────────────────────────────────────────────┐
│                    Conversation Flow                        │
│                                                             │
│  User: "Hi"                                                 │
│  AI: "Hello!"                                               │
│  User: "My name is Piyush"    ← Important info!            │
│  AI: "Hi Piyush!"                                           │
│  User: "X"                                                  │
│  AI: "Y"                                                    │
│  ... (many more messages) ...                               │
│  User: "What is my name?"     ← Context window here         │
│  AI: "I don't know"           ← Name info scrolled out!    │
└─────────────────────────────────────────────────────────────┘
```

### Visual: Context Window Sliding
```
Early conversation:
[Hi, Hello, My name is Piyush, Hi Piyush, X, Y, Z...]
 └────────── Context Window ──────────┘

Later conversation:
[...A, B, C, D, E, F, G, What is my name?]
         └────── Context Window ──────┘
         
Name info is OUT of window!
```

---

## The Solution: Memory Layer

```
┌─────────────────────────────────────────────────────────────┐
│                      Memory Store                           │
│                                                             │
│  • Name: Piyush                                             │
│  • Preferences: Likes Python                                │
│  • Age: 25                                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
              ↓ Always available to agent
┌─────────────────────────────────────────────────────────────┐
│                    LLM Conversation                         │
│  (Uses memory even when info is out of context window)      │
└─────────────────────────────────────────────────────────────┘
```

---

## Types of Memory

### 1. Short-Term Memory (STM)
- **Duration**: Session only
- **Purpose**: Hold temporary info during task
- **Deleted**: When task/session ends
- **Example**: Creating a project (forgets after completion)

### 2. Long-Term Memory (LTM)
- **Duration**: Forever (persisted)
- **Purpose**: Remember user permanently
- **Stored**: Database
- **Example**: User's name, preferences

---

## Long-Term Memory Subtypes

```
Long-Term Memory (LTM)
├── Factual Memory
│   └── Facts about the user
│   └── Example: Name, age, location
│
├── Episodic Memory
│   └── Past interactions & behaviors
│   └── Example: How user talks, preferences
│
└── Semantic Memory
    └── General world knowledge
    └── Example: "Delhi is capital of India"
```

---

## Memory Summary Table

| Type | Duration | Purpose | Example |
|------|----------|---------|---------|
| **Short-Term** | Session | Temporary task info | Current project context |
| **Factual** | Forever | User facts | Name, age, preferences |
| **Episodic** | Forever | Interaction history | User's communication style |
| **Semantic** | Forever | World knowledge | General facts |

---

## Why Memory Matters

| Without Memory | With Memory |
|----------------|-------------|
| Forgets after context window | Remembers forever |
| "What's your name?" repeated | Knows you from day 1 |
| No personalization | Personalized responses |
| Frustrating UX | Natural conversation |

---

## Coming Up

1. **Short-Term Memory** - Implementation
2. **Long-Term Memory** - Implementation
3. **Factual Memory** - User facts extraction
4. **Episodic Memory** - Interaction patterns
5. **Semantic Memory** - Knowledge graphs
6. **Vector Embeddings** for memory retrieval

**Next: Deep dive into each memory type!** 🧠


# Short-Term Memory (STM) in AI Agents

## What is Short-Term Memory?

**Short-Term Memory** = Temporary information held during an active session/task.

- **Also called**: Working Memory
- **Duration**: Session only
- **Deleted**: When session/task ends

---

## Real-World Analogy: Restaurant Order

```
┌─────────────────────────────────────────────────────────────┐
│                    Restaurant Scenario                      │
│                                                             │
│  1. You order a burger → Get Order #132                    │
│  2. You remember #132 while waiting                        │
│  3. Order arrives → Transaction complete                   │
│  4. You FORGET #132 immediately                            │
│                                                             │
│  Q: What was your last order number?                       │
│  A: "I don't remember" → Short-term memory deleted!        │
└─────────────────────────────────────────────────────────────┘
```

---

## AI Agent Example: Food Ordering Bot

### Good UX (With Short-Term Memory)
```
Agent: "How can I help?"
User:  "Where is my order #132?"
Agent: "It's getting prepared."
User:  "What's the status?"
Agent: "Order #132 is still being prepared."  ← Remembers!
```

### Bad UX (Without Short-Term Memory)
```
Agent: "How can I help?"
User:  "Where is my order #132?"
Agent: "It's getting prepared."
User:  "What's the status?"
Agent: "What is your order number?"  ← Forgot! Frustrating!
```

---

## Short-Term Memory = Conversation History

```python
# This is short-term memory!
message_history = [
    {"role": "user", "content": "Where is order #132?"},
    {"role": "assistant", "content": "It's getting prepared."},
    {"role": "user", "content": "What's the status?"},
]

# Send full history with each request
response = client.chat.completions.create(
    model="gpt-4o",
    messages=message_history  # ← Short-term memory
)
```

---

## Lifecycle of Short-Term Memory

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Session     │ →  │ Task in     │ →  │ Session     │
│ Starts      │    │ Progress    │    │ Ends        │
└─────────────┘    └─────────────┘    └─────────────┘
       ↓                  ↓                  ↓
   Memory              Memory             Memory
   Created            Updated            DELETED
```

---

## Key Characteristics

| Aspect | Short-Term Memory |
|--------|-------------------|
| **Duration** | Current session only |
| **Storage** | In-memory (RAM) |
| **Persistence** | Not stored in database |
| **Purpose** | Maintain conversation context |
| **Deleted** | When task completes |

---

## What You've Already Been Doing

```python
# From your previous code - this IS short-term memory!

# Example 1: Message history array
message_history = []
message_history.append({"role": "user", "content": query})
message_history.append({"role": "assistant", "content": response})

# Example 2: LangGraph state
class State(TypedDict):
    messages: Annotated[list, add_messages]  # ← Short-term memory!
```

---

## When to Use Short-Term Memory

✅ **Use for:**
- Current conversation context
- Ongoing task information
- Session-specific data
- Temporary calculations

❌ **Don't use for:**
- User preferences (use Long-Term)
- User name/age (use Factual Memory)
- Past interaction patterns (use Episodic Memory)

---

## Summary

> **Short-Term Memory = Conversation history within a session**

You've already been implementing this! Every time you:
- Maintain `message_history` array
- Send full conversation to LLM
- Track ongoing task state

**That's short-term memory in action!** 🧠

**Next: Long-Term Memory - Remembering forever!**


# Long-Term Memory (LTM) in AI Agents

## What is Long-Term Memory?

**Long-Term Memory** = Permanent information stored in a database, persists forever across sessions.

- **Scope**: User-level (not session-level)
- **Storage**: Database (MongoDB, Vector Store, Graph DB)
- **Duration**: Forever
- **Purpose**: Remember user permanently

---

## Real-World Analogy: Restaurant Customer

```
┌─────────────────────────────────────────────────────────────┐
│                    First Visit                              │
│  Agent: "Welcome! What's your name?"                       │
│  User:  "My name is Piyush"                                │
│  Agent: "Order #132 coming up, Piyush!"                    │
│                                                             │
│  → Store in LTM: Name = Piyush                             │
│  → Short-term: Order #132 (deleted after order)            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Second Visit (Next Day)                  │
│  Agent: "Hey Piyush! What's your order today?"             │
│         ↑ Remembered from LTM!                              │
│                                                             │
│  (Doesn't ask "What's your name?" again!)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Short-Term vs Long-Term Memory

| Aspect | Short-Term | Long-Term |
|--------|------------|-----------|
| **Scope** | Session | User |
| **Duration** | Until task ends | Forever |
| **Storage** | RAM | Database |
| **Example** | Order #132 | Name: Piyush |
| **Deleted** | After session | Never |

---

## How Long-Term Memory Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │     │   Agent     │     │  Database   │
│   Chats     │ →   │  Extracts   │ →   │   Stores    │
│             │     │   Facts     │     │   Forever   │
└─────────────┘     └─────────────┘     └─────────────┘

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   New       │     │   Fetch     │     │   Inject    │
│   Session   │ →   │   Memory    │ →   │   Context   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Injection (Similar to RAG)
```python
# Fetch user memories from database
memories = fetch_memories(user_id="piyush")
# ["Name: Piyush", "Age: 25", "Prefers: Vegetarian"]

# Inject as system context
system_prompt = f"""You are a helpful assistant.
User information:
{memories}
"""
```

---

## The Problem: Memory Overload

```
User has 4000+ memories stored over time
            ↓
Can you inject ALL into context?
            ↓
         NO! 
            ↓
Context window limit hit again!
```

---

## Solution: Categorize Long-Term Memory

```
Long-Term Memory (LTM)
├── Factual Memory
│   └── Always retrieve (critical facts)
│   └── Name, age, preferences
│
├── Episodic Memory
│   └── Sometimes retrieve (on demand)
│   └── Past interactions, behaviors
│
└── Semantic Memory
    └── Occasionally retrieve
    └── General knowledge
```

---

## When to Retrieve What?

| Memory Type | Retrieval Frequency | Example |
|-------------|---------------------|---------|
| **Factual** | Always | "User's name is Piyush" |
| **Episodic** | On demand | "User prefers concise answers" |
| **Semantic** | Occasionally | "Delhi is capital of India" |

---

## Storage Options

```
┌─────────────────────────────────────────────────────────────┐
│                    Storage Options                          │
│                                                             │
│  • MongoDB         - Document storage                      │
│  • Qdrant          - Vector embeddings                     │
│  • Neo4j           - Graph relationships                   │
│  • PostgreSQL      - Relational data                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Summary

| Question | Answer |
|----------|--------|
| What is LTM? | Permanent user memory |
| Where stored? | Database |
| How long? | Forever |
| When retrieved? | Every new session |
| Problem? | Can grow too large for context |
| Solution? | Categorize (Factual, Episodic, Semantic) |

---

## Coming Up

1. **Factual Memory** - Always retrieve
2. **Episodic Memory** - On-demand retrieval
3. **Semantic Memory** - General knowledge
4. **MEM0** - Memory framework implementation
5. **Vector + Graph DB** - Smart memory storage

**Next: Factual Memory - The most important facts!** 🧠


# Factual Memory - Core User Facts

## What is Factual Memory?

**Factual Memory** = Essential facts about the user that never change (or rarely change).

- **Type**: Long-Term Memory
- **Retrieval**: **Always** included in context
- **Size**: Small (5-15 data points)
- **Examples**: Name, age, location, preferences

---

## Examples of Factual Memory

```
┌─────────────────────────────────────────────────────────────┐
│                    User: Piyush                             │
│                                                             │
│  • Name: Piyush Garg                                       │
│  • Age: 25                                                  │
│  • Location: Delhi, India                                  │
│  • Email: piyush@example.com                               │
│  • Preferred Language: English                             │
│  • Communication Style: Concise answers                    │
│  • Output Preference: Markdown format                      │
│  • Expertise Level: Intermediate developer                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Real-World Analogy: Your Friend

```
What you remember about a close friend:
✅ Their name
✅ Where they live
✅ What they like
✅ Their personality

What you DON'T remember:
❌ Every conversation you've had
❌ What they said on March 15, 2023
❌ Exact words from last meeting

→ The basics = Factual Memory
```

---

## Key Characteristics

| Aspect | Factual Memory |
|--------|----------------|
| **Size** | Small (5-15 items) |
| **Frequency** | Always in context |
| **Changes** | Rarely |
| **Importance** | Critical |
| **Context cost** | Low |

---

## Why Always Include?

```
Factual Memory Size:
┌────────────────────┐
│ ~10 facts          │ ← Tiny!
│ ~100-200 tokens    │ ← Fits easily
└────────────────────┘

Context Window:
┌────────────────────────────────────────────────────────────┐
│                     1,000,000 tokens                       │
└────────────────────────────────────────────────────────────┘

Factual memory is so small, ALWAYS include it!
```

---

## How to Use Factual Memory

```python
# Fetch factual memory for user
factual_memory = {
    "name": "Piyush",
    "age": 25,
    "location": "Delhi",
    "preference": "short answers in markdown"
}

# Always inject into system prompt
system_prompt = f"""You are a helpful assistant.

User Facts:
- Name: {factual_memory['name']}
- Age: {factual_memory['age']}
- Location: {factual_memory['location']}
- Preference: {factual_memory['preference']}

Use this information to personalize responses.
"""
```

---

## What Counts as Factual Memory?

| ✅ Include | ❌ Don't Include |
|-----------|-----------------|
| Name | Conversation logs |
| Age | Temporary tasks |
| Location | Session-specific data |
| Email | Every interaction |
| Preferences | Order numbers |
| Communication style | One-time requests |
| Expertise level | |

---

## Summary

```
Factual Memory = User's Core Identity

┌─────────────────────────────────────┐
│  • Small dataset (5-15 facts)       │
│  • Always retrieved                 │
│  • Always in context                │
│  • Personalizes every response      │
└─────────────────────────────────────┘
```

---

## In the Memory Hierarchy

```
Long-Term Memory
├── Factual Memory ← ALWAYS RETRIEVE (You are here!)
│   └── Name, age, preferences
│
├── Episodic Memory (Next!)
│   └── Past interactions
│
└── Semantic Memory
    └── World knowledge
```

**Next: Episodic Memory - Remembering past interactions!** 🧠


# Episodic Memory - Past Interactions

## What is Episodic Memory?

**Episodic Memory** = Information about past interactions, events, and conversations.

- **Type**: Long-Term Memory
- **Retrieval**: **On-demand** (when relevant)
- **Size**: Can be large (many past interactions)
- **Examples**: Past conversations, events, outcomes

---

## Factual vs Episodic Memory

| Aspect | Factual Memory | Episodic Memory |
|--------|----------------|-----------------|
| **What** | Core identity facts | Past events/interactions |
| **Size** | Small (5-15 facts) | Large (many interactions) |
| **Retrieval** | Always | On-demand |
| **Example** | "Name: Piyush" | "Visited Paris in 2023" |
| **Context** | Always included | Only when relevant |

---

## Examples of Episodic Memory

```
┌─────────────────────────────────────────────────────────────┐
│                    User: Piyush                             │
│                    Past Interactions                        │
│                                                             │
│  • Visited Paris in June 2023                              │
│  • Doesn't like discussing politics                        │
│  • Had issues with model latency last deployment          │
│  • Asked about Python decorators 3 times                   │
│  • Prefers examples over theory (learned over time)        │
│  • Conversation about React on March 15                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## When to Retrieve Episodic Memory

### User Query Analysis
```
User: "Do you remember when I visited Paris?"
              ↓
      Trigger: Episodic memory needed!
              ↓
      Fetch from vector DB/database
              ↓
      "Yes, you visited Paris in June 2023"
```

### Without Episodic Trigger
```
User: "What's the weather today?"
              ↓
      No episodic memory needed
              ↓
      Just answer the question
```

---

## How It Works (RAG-like)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  User: "Remember when I visited Paris?"                    │
│         ↓                                                   │
│  Agent analyzes: Episodic memory query detected            │
│         ↓                                                   │
│  Tool call → Search vector DB for "Paris visit"            │
│         ↓                                                   │
│  Retrieved: "User visited Paris in June 2023"              │
│         ↓                                                   │
│  Inject into context + Generate response                   │
│         ↓                                                   │
│  "Yes! You visited Paris in June 2023."                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Pattern

```python
# User query
user_query = "Do you remember when I visited Paris?"

# Step 1: Check if episodic memory needed
if is_episodic_query(user_query):
    # Step 2: Retrieve relevant memories
    memories = vector_db.similarity_search(user_query)
    # Returns: ["Visited Paris in June 2023"]
    
    # Step 3: Inject into context
    context = f"""
    User Facts: {factual_memory}
    
    Relevant Past Interactions:
    {memories}
    
    User Query: {user_query}
    """
else:
    # Just use factual memory
    context = f"""
    User Facts: {factual_memory}
    User Query: {user_query}
    """
```

---

## Storage & Retrieval

### Storage
```
Every conversation → Vector embeddings → Vector DB
                                              ↓
                              Indexed for similarity search
```

### Retrieval
```
User query → Vector embedding → Similarity search → Top K results
```

---

## Real-World Example

```
┌─────────────────────────────────────────────────────────────┐
│  Conversation History (Episodic Memory Storage)             │
│                                                             │
│  [2024-01-15] User: "I love Python decorators"             │
│  [2024-01-20] User: "Going to Paris next month!"           │
│  [2024-02-15] User: "Back from Paris, it was amazing"      │
│  [2024-03-10] User: "The deployment had latency issues"    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Current Query: "What did I say about Paris?"
                        ↓
        Retrieve: Conversations from Jan 20 & Feb 15
                        ↓
        Response: "You mentioned you were going to Paris 
                   and later said it was amazing!"
```

---

## Summary

```
Episodic Memory = Past Events & Interactions

┌─────────────────────────────────────────┐
│  • Large dataset (many conversations)   │
│  • Retrieved on-demand                  │
│  • Similarity search (RAG-like)         │
│  • Only when relevant to query          │
└─────────────────────────────────────────┘
```

---

## Memory Hierarchy Updated

```
Long-Term Memory
├── Factual Memory ✅
│   └── Always retrieve
│
├── Episodic Memory ✅ (You are here!)
│   └── On-demand retrieval
│   └── Past interactions
│
└── Semantic Memory (Next!)
    └── General knowledge
```

**Next: Semantic Memory - General world knowledge!** 🧠


# Semantic Memory - General World Knowledge

## What is Semantic Memory?

**Semantic Memory** = General knowledge about the world, unrelated to the user or specific events.

- **Type**: Long-Term Memory
- **Retrieval**: Occasionally (when needed)
- **Size**: Can be very large
- **Examples**: Facts, definitions, templates, procedures

---

## Examples of Semantic Memory

```
┌─────────────────────────────────────────────────────────────┐
│                    General Knowledge                        │
│                                                             │
│  • Paris is the capital of France                          │
│  • Delhi is the capital of India                           │
│  • JSON parsing involves key-value pairs                   │
│  • Python uses indentation for code blocks                 │
│  • REST APIs use HTTP methods                              │
│  • Docker uses containers for isolation                    │
│                                                             │
│  (Nothing about a specific user!)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Semantic vs Other Memories

| Memory Type | About | Example |
|-------------|-------|---------|
| **Factual** | User identity | "User's name is Piyush" |
| **Episodic** | User's past | "User visited Paris in 2023" |
| **Semantic** | World facts | "Paris is capital of France" |

---

## When to Use Semantic Memory

### Example 1: General Question
```
User: "What's the capital of France?"
        ↓
Retrieve: Semantic memory → "Paris"
        ↓
Response: "The capital of France is Paris."
```

### Example 2: Technical Template
```
User: "I always forget JSON syntax, help!"
        ↓
Retrieve: Semantic memory → JSON template
        ↓
Response: {"key": "value"} template
```

---

## Characteristics

| Aspect | Semantic Memory |
|--------|-----------------|
| **User-specific?** | No |
| **Event-specific?** | No |
| **Universal?** | Yes |
| **Changes often?** | Rarely |
| **Size** | Potentially huge |

---

## Storage Options

Semantic memory can be:
- Pre-loaded knowledge base
- Wikipedia-style facts
- Templates and snippets
- Domain-specific knowledge
- Public information

---

## Complete Memory Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                      MEMORY TYPES                           │
│                                                             │
│  Short-Term Memory (STM)                                   │
│  └── Current session conversation                          │
│      Example: "Order #132"                                 │
│                                                             │
│  Long-Term Memory (LTM)                                    │
│  ├── Factual Memory [Always]                              │
│  │   └── User: Name, age, preferences                     │
│  │                                                         │
│  ├── Episodic Memory [On-demand]                          │
│  │   └── User: Past interactions, events                  │
│  │                                                         │
│  └── Semantic Memory [Occasionally]                       │
│      └── World: General knowledge, facts                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Practical Note

> **"You usually don't have to worry about semantic memory a lot."**

Why?
- LLMs already have world knowledge built-in
- Only needed for specialized/proprietary information
- Most use cases focus on Factual + Episodic memories

---

## Summary Table

| Memory | Scope | Retrieval | Size | Example |
|--------|-------|-----------|------|---------|
| **Short-Term** | Session | Active | Small | Current conversation |
| **Factual** | User | Always | Small | Name, preferences |
| **Episodic** | User | On-demand | Large | Past events |
| **Semantic** | World | Occasional | Huge | General facts |

---

## What's Next?

✅ Short-Term Memory
✅ Long-Term Memory
✅ Factual Memory
✅ Episodic Memory
✅ Semantic Memory

**Next: Implementing memory with MEM0 + Qdrant!** 🚀

Time to build a real memory-enabled AI agent!


# Setting Up MEM0 for Memory Management

## What is MEM0?

**MEM0** = Framework for managing AI agent memory (factual, episodic, semantic)

- Website: https://mem0.ai
- Docs: https://docs.mem0.ai

---

## Installation

```bash
pip install mem0ai
pip freeze > requirements.txt
```

---

## Basic Usage (Simple)

```python
from mem0 import Memory
import os

# Set OpenAI key
os.environ["OPENAI_API_KEY"] = "your_key"

# Initialize memory
memory = Memory()

# Add memories
memory.add(
    messages=[
        {"role": "user", "content": "My name is Piyush"},
        {"role": "assistant", "content": "Hi Piyush!"}
    ],
    user_id="piyush_123",
    metadata={"session": "chat_001"}
)

# Retrieve memories
memories = memory.get_all(user_id="piyush_123")
```

---

## Why We Need More Than Basic Setup

**Basic MEM0** = In-memory storage (lost on restart)

**Our Goal** = Persistent storage with Qdrant

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Basic MEM0           →  Lost on restart                   │
│                                                             │
│  MEM0 + Qdrant        →  Persistent forever                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## What's Coming

1. ✅ MEM0 installed
2. ⏳ Configure MEM0 with Qdrant
3. ⏳ Set up vector store for memories
4. ⏳ Build memory-enabled agent

---

## Documentation Resources

| Resource | URL | Purpose |
|----------|-----|---------|
| Main Site | https://mem0.ai | Overview |
| Docs | https://docs.mem0.ai | Full documentation |
| Python SDK | docs.mem0.ai/sdks/python | Python-specific guide |
| Memory Types | docs.mem0.ai/concepts/memory-types | Memory concepts |

---

## Recommended Reading

Before proceeding, browse:
- Memory types (we already covered this)
- Configuration options
- Integration guides
- Examples

**No need to code anything yet - just familiarize yourself!**

---

## Next Steps

1. Set up Qdrant for persistent storage
2. Configure MEM0 to use Qdrant
3. Build first memory-enabled agent

**Next: Configuring MEM0 + Qdrant integration!** 🚀


# Configuring MEM0 with Qdrant

## Project Structure

```
memory_agent/
├── memory.py
├── .env
└── docker-compose.yml (Qdrant)
```

---

## Complete Configuration: `memory.py`

```python
import os
from mem0 import Memory

# Get OpenAI API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")

# MEM0 Configuration
config = {
    "version": "v1.1",
    
    # Embedding model configuration
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": openai_api_key,
            "model": "text-embedding-3-small"
        }
    },
    
    # LLM for extracting memories
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": openai_api_key,
            "model": "gpt-4.1"
        }
    },
    
    # Vector store for persistence
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

# Create memory client
memory = Memory.from_config(config)
```

---

## Configuration Breakdown

### 1. Version
```python
"version": "v1.1"  # MEM0 version
```

### 2. Embedder (Vector Embeddings)
```python
"embedder": {
    "provider": "openai",          # Who creates embeddings
    "config": {
        "api_key": openai_api_key,
        "model": "text-embedding-3-small"  # Embedding model
    }
}
```

### 3. LLM (Memory Extraction)
```python
"llm": {
    "provider": "openai",          # Who extracts memories
    "config": {
        "api_key": openai_api_key,
        "model": "gpt-4.1"         # LLM for extraction
    }
}
```

### 4. Vector Store (Persistence)
```python
"vector_store": {
    "provider": "qdrant",          # Storage provider
    "config": {
        "host": "localhost",       # Qdrant host
        "port": 6333               # Qdrant port
    }
}
```

---

## What Each Component Does

```
┌─────────────────────────────────────────────────────────────┐
│                    MEM0 Components                          │
│                                                             │
│  Embedder (text-embedding-3-small)                         │
│  └── Converts text → vectors                               │
│                                                             │
│  LLM (gpt-4.1)                                             │
│  └── Extracts important facts from conversations           │
│                                                             │
│  Vector Store (Qdrant)                                     │
│  └── Stores vectors for similarity search                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### 1. Environment Variable
Create `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

### 2. Qdrant Running
Make sure Qdrant is running:
```bash
docker compose up -d  # From earlier RAG setup
```

Verify:
```
http://localhost:6333/dashboard
```

---

## Memory Client Usage

```python
# Now you can use the memory client!

# Add memories
memory.add(...)

# Search memories
memory.search(...)

# Get all memories
memory.get_all(...)
```

---

## Summary

| Component | Provider | Purpose |
|-----------|----------|---------|
| **Embedder** | OpenAI | Convert text to vectors |
| **LLM** | OpenAI | Extract memories from text |
| **Vector Store** | Qdrant | Persistent storage |

**Memory client is ready!** 🎉

**Next: Using the memory client to add and retrieve memories!**

# Setting Up Qdrant for MEM0

## Quick Setup

We already know how to do this from the RAG section!

---

## Docker Compose: `docker-compose.yml`

```yaml
services:
  vector_database:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
```

---

## Start Qdrant

```bash
# Navigate to memory_agent folder
cd memory_agent

# Start Qdrant in detached mode
docker compose up -d
```

---

## Verify Qdrant is Running

### Option 1: Browser
```
http://localhost:6333/dashboard
```

### Option 2: Terminal
```bash
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE             PORTS
abc123...      qdrant/qdrant    0.0.0.0:6333->6333/tcp
```

---

## Current State

```
┌─────────────────────────────────────────────────────────────┐
│                    Qdrant Dashboard                         │
│                                                             │
│  Collections: 0                                            │
│  Points: 0                                                  │
│                                                             │
│  (Empty - ready for memories!)                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Connection Confirmed

```python
# In memory.py, this config now connects successfully:
"vector_store": {
    "provider": "qdrant",
    "config": {
        "host": "localhost",  # ✅
        "port": 6333          # ✅
    }
}
```

---

## Project Structure Now

```
memory_agent/
├── docker-compose.yml    # ✅ Qdrant setup
├── memory.py             # ✅ MEM0 config
├── .env                  # ✅ API keys
└── (Qdrant running)      # ✅ Port 6333
```

---

## What's Next?

1. ✅ Qdrant running
2. ✅ MEM0 configured
3. ⏳ Add memories to Qdrant
4. ⏳ Retrieve memories
5. ⏳ Build memory-enabled agent

**Next: Adding memories with MEM0!** 💾


# Adding and Retrieving Memories with MEM0

## Complete Code: `memory.py`

```python
import os
import json
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# MEM0 Configuration
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": openai_api_key,
            "model": "text-embedding-3-small"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": openai_api_key,
            "model": "gpt-4.1"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

# Create memory client
memory_client = Memory.from_config(config)

# Create OpenAI client
client = OpenAI()

# User ID for scoping memories
USER_ID = "piyushgarg"

# Chat loop
while True:
    # Get user input
    user_query = input("You: ")
    
    # Step 1: Search for relevant memories
    search_results = memory_client.search(user_query, user_id=USER_ID)
    
    # Step 2: Format memories
    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_results.get("results", [])
    ]
    
    print(f"Found memories: {memories}")
    
    # Step 3: Create system prompt with memories
    system_prompt = f"""Here is the context about the user:
{json.dumps(memories)}
"""
    
    # Step 4: Call OpenAI with memories as context
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    )
    
    ai_response = response.choices[0].message.content
    print(f"AI: {ai_response}")
    
    # Step 5: Save this conversation to memory
    memory_client.add(
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ],
        user_id=USER_ID
    )
    
    print("Memory has been saved.")
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                     Chat Loop                               │
│                                                             │
│  1. User asks: "What is my name?"                          │
│         ↓                                                   │
│  2. Search memories for relevant info                      │
│         ↓                                                   │
│  3. Found: "Name is Piyush Garg"                           │
│         ↓                                                   │
│  4. Inject into system prompt                              │
│         ↓                                                   │
│  5. LLM responds: "Your name is Piyush Garg"               │
│         ↓                                                   │
│  6. Save this conversation as new memory                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Functions

### Add Memory
```python
memory_client.add(
    messages=[
        {"role": "user", "content": "My name is Piyush"},
        {"role": "assistant", "content": "Hi Piyush!"}
    ],
    user_id="piyushgarg"
)
```

### Search Memory
```python
results = memory_client.search(
    query="What is my name?",
    user_id="piyushgarg"
)

# Access results
memories = results.get("results", [])
```

---

## Example Conversation

```
You: My name is Piyush
AI: Hello Piyush! How can I assist you today?
Memory saved: "Name is Piyush Garg" ✓

You: I like to eat pizza with cheese
AI: Pizza with cheese sounds delicious!
Memory saved: "Likes pizza with cheese" ✓

You: What is my name?
Found memories: ["Name is Piyush Garg"]
AI: Your name is Piyush Garg!

You: Can you suggest what food I should order?
Found memories: ["Likes pizza with cheese"]
AI: Since you like pizza with cheese, I recommend...
```

---

## Qdrant Dashboard

After conversations, check:
```
http://localhost:6333/dashboard
```

**You'll see:**
- Collection: `mem0`
- Points: User memories stored
- Each point contains memory text + vector embedding

---

## Key Points

| Feature | Description |
|---------|-------------|
| **No chat history needed** | Memories replace conversation history |
| **Automatic extraction** | MEM0 extracts facts from conversations |
| **Contradiction handling** | Updates memories when user corrects info |
| **Relevant only** | Similarity search returns only relevant memories |
| **User scoped** | Each user has their own memories |

---

## The Magic

> **We're NOT passing full chat history!**
> 
> Instead, we:
> 1. Search for relevant memories
> 2. Inject only what's needed
> 3. Save new facts for future

**This is memory-aware AI!** 🧠

---

## Summary

```
User Query → Search Memories → Inject Context → LLM → Response → Save Memory
```

**Built a production-ready memory system with:**
- ✅ MEM0 for memory management
- ✅ Qdrant for vector storage
- ✅ OpenAI for embeddings & LLM
- ✅ Automatic fact extraction
- ✅ Similarity-based retrieval

**Congratulations! You've built a memory-enabled AI agent!** 🎉
