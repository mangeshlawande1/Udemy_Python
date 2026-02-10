
# Introduction to LangGraph

## What is LangGraph?

**LangGraph** is a framework for building AI workflows as **graphs** instead of messy nested code.

---

## The Problem LangGraph Solves

### Traditional Approach (Messy Code)
```python
while True:
    if need_search:
        result = web_search()
        if not good_result:
            if retry_count < 3:
                continue
            else:
                break
    else:
        if condition_x:
            # More nested logic...
```

**Problems:**
- ❌ Nested if/else statements
- ❌ Complex while loops
- ❌ Hard to debug
- ❌ Unmaintainable
- ❌ Difficult to modify

### LangGraph Approach (Clean Graph)
```
Start → Plan → Need Search? → Yes → Web Search → LLM Call
                    ↓ No
              LLM Call → Quality Check → Good? → End
                              ↓ No
                           Retry
```

**Benefits:**
- ✅ Visual workflow
- ✅ Easy to debug
- ✅ Maintainable
- ✅ Easy to modify

---

## Installation

```bash
pip install -U langgraph
pip freeze > requirements.txt
```

---

## Core Concepts

### 1. Nodes (Functions)
```python
def get_user_input(state):
    # Do something
    return updated_state

def call_llm(state):
    # Do something
    return updated_state

def web_search(state):
    # Do something
    return updated_state
```

**Nodes = Functions that process and update state**

### 2. Edges (Connections)
```
Node A → Node B → Node C
```
**Edges = Define the flow between nodes**

### 3. State (Shared Data)
```python
class State(TypedDict):
    input: str
    output: str
    messages: list
```
**State = Data passed through all nodes**

---

## How LangGraph Works

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Initial State ──→ Node 1 ──→ Node 2 ──→ Node 3 ──→ Final State
│      (input)        ↓           ↓           ↓        (output)
│                  Update      Update      Update              │
│                  State       State       State               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Flow Example:
```
State = {input: "Hello"}
         ↓
    Node 1 reads state, updates → {input: "Hello", step1: "done"}
         ↓
    Node 2 reads state, updates → {input: "Hello", step1: "done", result: "..."}
         ↓
    Node 3 reads state, updates → {input: "Hello", step1: "done", result: "...", output: "Final!"}
         ↓
    Final State returned
```

---

## Basic Usage

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=your_model,
    tools=your_tools,
    prompt=your_prompt
)

# Invoke with initial state
result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})
```

---

## Visual Representation

```
        ┌─────────┐
        │  Start  │
        └────┬────┘
             │
        ┌────▼────┐
        │  Plan   │
        └────┬────┘
             │
        ┌────▼────┐     Yes    ┌────────────┐
        │ Search? │───────────→│ Web Search │
        └────┬────┘            └─────┬──────┘
             │ No                    │
             │◄──────────────────────┘
        ┌────▼────┐
        │   LLM   │
        └────┬────┘
             │
        ┌────▼────┐     No     ┌─────────┐
        │ Good?   │───────────→│  Retry  │
        └────┬────┘            └────┬────┘
             │ Yes                  │
             │◄─────────────────────┘
        ┌────▼────┐
        │   End   │
        └─────────┘
```

---

## Key Takeaways

| Concept | Description |
|---------|-------------|
| **Nodes** | Functions that process state |
| **Edges** | Connections between nodes |
| **State** | Shared data passed through graph |
| **Graph** | Complete workflow structure |

**LangGraph = Clean, maintainable, visual AI workflows!**

**Next: Building our first LangGraph agent!** 🚀



# LangGraph Setup - Creating State and Graph Builder

## Project Structure

```
langgraph_learning/
└── chat.py
```

---

## Step 1: Create the State

State is a **TypedDict** that holds data passed between nodes.

```python
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

---

## Understanding the State

### What is `Annotated[list, add_messages]`?

```python
# Without annotation - replaces entire list
messages = ["Hello"]  → messages = ["New"]  # Old message lost!

# With add_messages annotation - appends to list
messages = ["Hello"]  → messages = ["Hello", "New"]  # Both kept!
```

**`add_messages`** = Always append new messages, never replace

---

## Step 2: Create Graph Builder

```python
from langgraph.graph import StateGraph

# Create graph builder with state schema
graph_builder = StateGraph(State)
```

---

## Complete Code So Far: `chat.py`

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

# Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Create Graph Builder
graph_builder = StateGraph(State)
```

---

## What We Have Now

```
┌─────────────────────────────────────┐
│              State                  │
│  ┌─────────────────────────────┐   │
│  │ messages: [                 │   │
│  │   "User: Hello",            │   │
│  │   "AI: Hi there!",          │   │
│  │   "User: How are you?",     │   │
│  │   "AI: I'm great!"          │   │
│  │ ]                           │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│          Graph Builder              │
│  (Ready to add nodes and edges)     │
└─────────────────────────────────────┘
```

---

## Key Concepts

| Component | Purpose |
|-----------|---------|
| **State** | Container for shared data |
| **TypedDict** | Type-safe dictionary |
| **Annotated** | Add special behaviors |
| **add_messages** | Append instead of replace |
| **StateGraph** | Builder for creating graphs |

---

## Message Flow Example

```
Initial State:
  messages: [{"role": "user", "content": "Hello"}]
                          ↓
After Node 1:
  messages: [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"}  ← Added
  ]
                          ↓
After Node 2:
  messages: [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
    {"role": "user", "content": "Thanks!"}  ← Added
  ]
```

---

## Next Steps

1. ✅ State created
2. ✅ Graph builder initialized
3. ⏳ Add nodes (functions)
4. ⏳ Add edges (connections)
5. ⏳ Compile and run graph

**Next: Creating nodes and connecting them with edges!** 🚀


# LangGraph - Creating Nodes

## What is a Node?

**Node = A function that:**
1. Receives the current state
2. Does some processing
3. Returns updates to the state

---

## Creating Nodes

### Node 1: Chatbot
```python
def chatbot(state: State):
    # Access current state
    # Return new messages to append
    return {
        "messages": ["Hi, this is a message from chatbot node"]
    }
```

### Node 2: Sample Node
```python
def sample(state: State):
    return {
        "messages": ["Sample message appended"]
    }
```

---

## Registering Nodes with Graph Builder

```python
# Register nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample", sample)
```

---

## Complete Code So Far: `chat.py`

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

# Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Create Graph Builder
graph_builder = StateGraph(State)

# Node 1: Chatbot
def chatbot(state: State):
    return {
        "messages": ["Hi, this is a message from chatbot node"]
    }

# Node 2: Sample
def sample(state: State):
    return {
        "messages": ["Sample message appended"]
    }

# Register nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample", sample)
```

---

## How State Updates Work

### Initial State
```python
{"messages": ["Hey there"]}
```

### After Chatbot Node
```python
{
    "messages": [
        "Hey there",
        "Hi, this is a message from chatbot node"  # ← Appended!
    ]
}
```

### After Sample Node
```python
{
    "messages": [
        "Hey there",
        "Hi, this is a message from chatbot node",
        "Sample message appended"  # ← Appended!
    ]
}
```

**Key:** `add_messages` annotation = Always append, never replace!

---

## Visual Representation

```
┌─────────────────────────────────────────────────┐
│              Graph Builder                      │
│                                                 │
│   ┌──────────────┐    ┌──────────────┐         │
│   │   chatbot    │    │    sample    │         │
│   │    (node)    │    │    (node)    │         │
│   └──────────────┘    └──────────────┘         │
│                                                 │
│   (Not connected yet - need edges!)             │
└─────────────────────────────────────────────────┘
```

---

## Node Structure

```python
def node_name(state: State):
    # 1. Read from state
    current_messages = state["messages"]
    
    # 2. Do processing
    result = some_processing(current_messages)
    
    # 3. Return state updates
    return {
        "messages": [result]  # Will be appended
    }
```

---

## Key Points

| Concept | Description |
|---------|-------------|
| **Node** | Function with state in, state updates out |
| **add_node()** | Register function as a node |
| **Name** | String identifier for the node |
| **State** | Passed to every node automatically |

---

## What's Missing?

✅ State defined
✅ Nodes created
✅ Nodes registered
❌ **Edges not connected!**

Nodes exist but aren't linked together yet.

**Next: Adding edges to connect nodes!** 🚀



# LangGraph - Creating Edges

## What are Edges?

**Edges = Connections that define the flow between nodes**

```
START → Node A → Node B → END
```

---

## Special Nodes: START and END

```python
from langgraph.graph import START, END
```

| Node | Purpose |
|------|---------|
| `START` | Entry point of the graph |
| `END` | Exit point of the graph |

---

## Adding Edges

```python
# Import special nodes
from langgraph.graph import START, END

# Define flow
graph_builder.add_edge(START, "chatbot")      # Start → Chatbot
graph_builder.add_edge("chatbot", "sample")   # Chatbot → Sample
graph_builder.add_edge("sample", END)         # Sample → End
```

---

## Complete Code: `chat.py`

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Create Graph Builder
graph_builder = StateGraph(State)

# Node 1: Chatbot
def chatbot(state: State):
    print("We are inside the chatbot node")
    print(f"Current state: {state}")
    return {
        "messages": ["Hi, this is a message from chatbot node"]
    }

# Node 2: Sample
def sample(state: State):
    print("We are inside the sample node")
    print(f"Current state: {state}")
    return {
        "messages": ["Sample message appended"]
    }

# Register nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample", sample)

# Add edges (define flow)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sample")
graph_builder.add_edge("sample", END)

# Compile the graph
graph = graph_builder.compile()
```

---

## Visual Flow

```
    ┌─────────┐
    │  START  │
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │ chatbot │  ← Receives initial state
    └────┬────┘    Returns: "message from chatbot"
         │
         ▼
    ┌─────────┐
    │ sample  │  ← Receives updated state
    └────┬────┘    Returns: "sample message"
         │
         ▼
    ┌─────────┐
    │   END   │  ← Final state returned
    └─────────┘
```

---

## Edge Count

| Edge | From | To |
|------|------|-----|
| 1 | START | chatbot |
| 2 | chatbot | sample |
| 3 | sample | END |

---

## Summary

```python
# Structure
graph_builder.add_edge(FROM, TO)

# Examples
graph_builder.add_edge(START, "first_node")     # Entry point
graph_builder.add_edge("node_a", "node_b")      # Node to node
graph_builder.add_edge("last_node", END)        # Exit point
```

---

## What We Have Now

✅ State defined
✅ Nodes created
✅ Nodes registered
✅ Edges connected
✅ **Graph compiled!**

```python
graph = graph_builder.compile()  # Ready to run!
```

**Next: Invoking the graph and seeing it in action!** 🚀



# LangGraph - Conditional Edges

## What are Conditional Edges?

**Conditional Edge** = A decision point that routes to different nodes based on logic

```
           ┌─── If Good ───→ End Node
Evaluate ──┤
           └─── If Bad ────→ Try Again Node
```

---

## Project: Response Quality Check

### Flow
```
User Query → Chatbot (GPT) → Evaluate → Good? → Yes → End
                                         ↓ No
                                    Chatbot (Gemini) → End
```

---

## Complete Code: `chat_2.py`

```python
from typing import Optional, Literal
from typing_extensions import TypedDict
from dotenv import load_dotenv
from openai import OpenAI
from langgraph.graph import StateGraph, START, END

load_dotenv()

# Define State
class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

# Initialize clients
client = OpenAI()

# Node 1: Chatbot (GPT)
def chatbot(state: State):
    print("Chatbot node")
    print(f"State: {state}")
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{
            "role": "user",
            "content": state.get("user_query")
        }]
    )
    
    return {
        "llm_output": response.choices[0].message.content
    }

# Node 2: Evaluate Response (Conditional)
def evaluate_response(state: State) -> Literal["end_node", "chatbot_gemini"]:
    print("Evaluate node")
    
    # TODO: Use AI to evaluate (homework!)
    evaluation_is_good = True  # Hardcoded for now
    
    if evaluation_is_good:
        return "end_node"
    else:
        return "chatbot_gemini"

# Node 3: Chatbot Gemini (Fallback)
def chatbot_gemini(state: State):
    print("Chatbot Gemini node")
    
    # Use a different/better model
    response = client.chat.completions.create(
        model="gpt-4.1",  # Or actual Gemini
        messages=[{
            "role": "user",
            "content": state.get("user_query")
        }]
    )
    
    return {
        "llm_output": response.choices[0].message.content
    }

# Node 4: End Node
def end_node(state: State):
    print("End node")
    return state

# Build Graph
graph_builder = StateGraph(State)

# Register nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("evaluate_response", evaluate_response)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("end_node", end_node)

# Add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "evaluate_response")

# Conditional edge
graph_builder.add_conditional_edges("evaluate_response", evaluate_response)

# Regular edges after conditional
graph_builder.add_edge("chatbot_gemini", "end_node")
graph_builder.add_edge("end_node", END)

# Compile
graph = graph_builder.compile()

# Run
updated_state = graph.invoke({
    "user_query": "What is two plus two?"
})

print(updated_state)
```

---

## Visual Flow

```
        ┌─────────┐
        │  START  │
        └────┬────┘
             │
        ┌────▼────┐
        │ chatbot │  (GPT-4.1-mini)
        └────┬────┘
             │
     ┌───────▼───────┐
     │   evaluate    │  ← Conditional!
     │   response    │
     └───────┬───────┘
             │
      ┌──────┴──────┐
      │             │
 (Good)         (Bad)
      │             │
      ▼             ▼
 ┌─────────┐  ┌───────────┐
 │end_node │  │  chatbot  │
 │         │  │  gemini   │
 └────┬────┘  └─────┬─────┘
      │             │
      │       ┌─────▼─────┐
      │       │ end_node  │
      │       └─────┬─────┘
      │             │
      └──────┬──────┘
             │
        ┌────▼────┐
        │   END   │
        └─────────┘
```

---

## Execution Traces

### When `evaluation_is_good = True`:
```
Chatbot node → Evaluate node → End node
```

### When `evaluation_is_good = False`:
```
Chatbot node → Evaluate node → Chatbot Gemini node → End node
```

---

## Key Syntax

### Conditional Edge Function
```python
def evaluate_response(state: State) -> Literal["node_a", "node_b"]:
    if condition:
        return "node_a"
    else:
        return "node_b"
```

### Adding Conditional Edge
```python
graph_builder.add_conditional_edges("source_node", routing_function)
```

---

## Homework Assignment 📝

Replace the hardcoded evaluation:
```python
evaluation_is_good = True  # Replace this!
```

With an actual AI call:
```python
# Use another LLM to evaluate quality
eval_response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{
        "role": "system",
        "content": "Evaluate if this response is good. Reply YES or NO only."
    }, {
        "role": "user", 
        "content": state.get("llm_output")
    }]
)
evaluation_is_good = "YES" in eval_response.choices[0].message.content
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **Conditional Edge** | Routes to different nodes based on logic |
| **Literal** | Type hint specifying possible return values |
| **add_conditional_edges()** | Registers conditional routing |
| **Return value** | Node name (string) to route to |

**LangGraph makes complex AI workflows clean and maintainable!** 🚀