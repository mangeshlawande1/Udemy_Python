# Graph Databases for AI Memory

## Part 1: What is a Graph?

### Basic Structure

```
       Node A ───────── Node B
          \              /
           \   Edges    /
            \          /
             Node C ───
```

**Two Components:**
- **Nodes**: Carry data (entities)
- **Edges**: Connections between nodes (relationships)

---

### Types of Graphs

#### Directed Graph
```
    A ──────→ B
    
    A is parent of B
    B is NOT parent of A
    (One-way relationship)
```

#### Undirected Graph
```
    A ──────── B
    
    A is friends with B
    B is friends with A
    (Two-way relationship)
```

---

## Part 2: Why Graphs for Memory?

### The Problem with Vector Embeddings

**Vector DBs store:**
- ✅ "Your name is Piyush"
- ✅ "You like pizza"
- ✅ Individual facts

**Vector DBs miss:**
- ❌ Relationships between entities
- ❌ Indirect connections
- ❌ Semantic knowledge

---

### Example: Company Relationships

```
                    ┌─────────────┐
                    │  Company X  │
                    └─────────────┘
                     /    |     \
              owns  /     |      \ employs
                   /   employs    \
                  /       |        \
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │   Alex   │  │   John   │  │   Jane   │
         │  (Owner) │  │(Employee)│  │(Employee)│
         └──────────┘  └──────────┘  └──────────┘
                              \        /
                               \      /
                            co-workers
                           (inferred!)
```

---

### What Graphs Enable

| Query | Graph Answer |
|-------|--------------|
| "Who are John's co-workers?" | Jane (both employed by X) |
| "Who should Jane report to?" | Alex (owns Company X) |
| "What's the relationship between John and Jane?" | Co-workers |
| "Who owns the company John works for?" | Alex |

**These are INFERRED relationships!**

---

### Vector DB vs Graph DB

| Aspect | Vector DB | Graph DB |
|--------|-----------|----------|
| Storage | Individual facts | Entities + Relationships |
| Retrieval | Similarity search | Relationship traversal |
| Indirect relations | ❌ Can't find | ✅ Automatically discovered |
| "Friends of friends" | ❌ Not possible | ✅ Easy |
| Semantic connections | Limited | Rich |

---

## Why Both Are Needed

```
┌─────────────────────────────────────────────────────────────┐
│                    Memory System                            │
│                                                             │
│  Vector DB (Qdrant)          Graph DB (Neo4j)              │
│  ├── "Name: Piyush"          ├── Piyush ──works_at──→ X   │
│  ├── "Likes: Pizza"          ├── X ──employs──→ Jane       │
│  └── Fast similarity search  └── Relationships!            │
│                                                             │
│  Combined = Complete Memory Understanding                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Real-World Analogy

**How humans think:**
- "John works at Company X"
- "Jane also works at Company X"
- → "John and Jane are co-workers" (inferred!)

**This is exactly what graph memory does!**

---

## Coming Up

1. Set up Neo4j (Graph Database)
2. Create knowledge graphs from conversations
3. Combine graph memory with vector memory
4. Build a complete memory system

**Next: Setting up Neo4j for graph-based memory!** 🕸️


# Neo4j Setup & Cypher Queries

## Part 1: Setting Up Neo4j

### Graph Database Options

| Database | Status | Notes |
|----------|--------|-------|
| **Neo4j** | Industry Standard | Heavy, scalable, mature |
| **KuzuDB** | New | Limited support |

**Recommendation**: Neo4j (industry standard)

---

### Neo4j Aura (Cloud Setup)

**Why Cloud?**
- Neo4j is heavy locally
- Free tier available
- Easier setup

**Steps:**
1. Go to Neo4j Aura: https://neo4j.com/cloud/aura/
2. Sign up / Login with Google
3. Create free instance
4. **Save credentials immediately!**

```
# Add to .env file
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_generated_password
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
```

---

## Part 2: Cypher Query Basics

**Cypher** = Query language for Neo4j (like SQL for graphs)

### Create a Node

```cypher
CREATE (u:User {name: "Piyush"})
RETURN u
```

**Breakdown:**
- `CREATE` - Create new node
- `u` - Variable name
- `:User` - Node type/label
- `{name: "Piyush"}` - Properties

### Create Multiple Nodes

```cypher
CREATE (u:User {name: "John"})
CREATE (u:User {name: "Jane"})
CREATE (u:User {name: "Alex"})
CREATE (c:Company {name: "Google"})
```

---

### Query All Nodes

```cypher
MATCH (n)
RETURN n
```

### Query by Type

```cypher
MATCH (u:User)
RETURN u
```

### Query by Property

```cypher
MATCH (u:User {name: "Piyush"})
RETURN u
```

---

### Create Relationships (The Right Way)

```cypher
-- Match existing nodes first, then merge relationship
MATCH (u:User {name: "Piyush"})
MATCH (c:Company {name: "Google"})
MERGE (u)-[:EMPLOYEE]->(c)
```

**Breakdown:**
- `MATCH` - Find existing nodes
- `MERGE` - Create relationship if doesn't exist
- `-[:EMPLOYEE]->` - Directed relationship named "EMPLOYEE"

### Multiple Relationships

```cypher
MATCH (u:User {name: "John"})
MATCH (c:Company {name: "Google"})
MERGE (u)-[:EMPLOYEE]->(c)

MATCH (u:User {name: "Jane"})
MATCH (c:Company {name: "Google"})
MERGE (u)-[:EMPLOYEE]->(c)
```

---

### Query Relationships

```cypher
-- Find all employees of Google
MATCH (u:User)-[:EMPLOYEE]->(c:Company {name: "Google"})
RETURN u, c
```

---

### Delete Nodes

```cypher
-- Delete by element ID
MATCH (n)
WHERE elementId(n) = "4:xxx:0"
DELETE n
```

**Note:** Must delete relationships first before deleting nodes!

---

## Visual Result

```
        ┌─────────────┐
        │   Google    │
        │  (Company)  │
        └─────────────┘
         ↑   ↑   ↑   ↑
    EMPLOYEE EMPLOYEE EMPLOYEE EMPLOYEE
         │   │   │   │
    ┌────┘   │   │   └────┐
    │        │   │        │
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Piyush │ │ John  │ │ Jane  │ │ Alex  │
│(User) │ │(User) │ │(User) │ │(User) │
└───────┘ └───────┘ └───────┘ └───────┘
```

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| CREATE instead of MATCH | Creates duplicates | Use MATCH for existing nodes |
| Not matching before merge | Multiple nodes | Always MATCH first |
| Using deprecated `id()` | Error | Use `elementId()` |

---

## Key Cypher Commands

| Command | Purpose |
|---------|---------|
| `CREATE` | Create new node/relationship |
| `MATCH` | Find existing nodes |
| `MERGE` | Create if not exists |
| `RETURN` | Return results |
| `DELETE` | Remove node/relationship |
| `WHERE` | Filter condition |

---

## Good News!

> **You don't need to write Cypher queries manually!**
> 
> LLMs are excellent at generating Cypher:
> - Tell LLM the relationship
> - LLM generates Cypher
> - Stores in Neo4j
> - Fetches when needed

**Next: Integrating Neo4j with MEM0 for graph-based memory!** 🕸️


# Integrating Neo4j with MEM0

## Configuration Update

### Add Graph Store to Config

```python
import os
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

config = {
    "version": "v1.1",
    
    # Embedding model
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": openai_api_key,
            "model": "text-embedding-3-small"
        }
    },
    
    # LLM for extraction
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": openai_api_key,
            "model": "gpt-4.1"
        }
    },
    
    # Vector store (Qdrant)
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    },
    
    # NEW: Graph store (Neo4j)
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://xxxxx.databases.neo4j.io",
            "username": "neo4j",
            "password": "your_password"
        }
    }
}

memory_client = Memory.from_config(config)
```

---

## Install Required Packages

```bash
pip install langchain-neo4j
pip install neo4j
```

---

## Example Conversation

```
You: My name is Piyush and I like pizza with tomatoes topping

AI: That's great to know!

→ Graph creates: (User:Piyush)-[:LIKES]->(Food:Pizza)
→ Graph creates: (Pizza)-[:HAS_TOPPING]->(Topping:Tomatoes)
```

```
You: I am a full stack developer. My tech stack is Node.js and JavaScript with Postgres

AI: Nice tech stack!

→ Graph creates: (Piyush)-[:IS_A]->(Role:Full Stack Developer)
→ Graph creates: (Piyush)-[:USES]->(Tech:Node.js)
→ Graph creates: (Piyush)-[:USES]->(Tech:JavaScript)
→ Graph creates: (Piyush)-[:USES]->(Database:Postgres)
```

```
You: I also work with Python for GenAI workloads

AI: Great addition!

→ Graph creates: (Piyush)-[:WORKS_WITH]->(Python)
→ Graph creates: (Python)-[:USED_FOR]->(GenAI)
```

---

## Knowledge Graph Built Automatically

```
                    ┌──────────────────┐
                    │  Full Stack Dev  │
                    └────────┬─────────┘
                             │ IS_A
                             │
    ┌────────────────────────┼────────────────────────┐
    │                        │                        │
    │                   ┌────▼────┐                   │
    │                   │ Piyush  │                   │
    │                   └────┬────┘                   │
    │          ┌─────────────┼─────────────┐         │
    │          │             │             │         │
    │      LIKES         USES          WORKS_WITH    │
    │          │             │             │         │
    │    ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐  │
    │    │   Pizza   │ │  Node.js  │ │  Python   │  │
    │    └─────┬─────┘ │JavaScript │ └─────┬─────┘  │
    │          │       │  Postgres │       │        │
    │    HAS_TOPPING   └───────────┘   USED_FOR    │
    │          │                           │        │
    │    ┌─────▼─────┐               ┌─────▼─────┐  │
    │    │ Tomatoes  │               │   GenAI   │  │
    │    └───────────┘               └───────────┘  │
    └───────────────────────────────────────────────┘
```

---

## Query Results

```
You: What is my tech stack and what do I primarily work on?

AI: Your main tech stack includes Node.js, JavaScript, and Postgres.
    You primarily work as a full stack developer.
    You also work with Python for Generative AI workloads.
```

**All from graph relationships - no chat history needed!**

---

## What MEM0 Creates Automatically

| Entity | Type | Relationships |
|--------|------|---------------|
| Piyush | User | LIKES, USES, IS_A, WORKS_WITH |
| Pizza | Food | HAS_TOPPING |
| Node.js | Tech Stack | - |
| Python | Tech Stack | USED_FOR |
| GenAI | Domain | - |

---

## Vector Store vs Graph Store

| Aspect | Vector Store (Qdrant) | Graph Store (Neo4j) |
|--------|----------------------|---------------------|
| Storage | Individual facts | Relationships |
| Query | Similarity search | Relationship traversal |
| Example | "Likes pizza" | Piyush → LIKES → Pizza → HAS_TOPPING → Tomatoes |
| Strength | Fast retrieval | Complex relationships |

**MEM0 uses BOTH for complete memory!**

---

## Summary

```
User Conversation → MEM0 → Extracts Entities & Relationships
                       ↓
              ┌────────┴────────┐
              ↓                 ↓
        Vector Store       Graph Store
         (Qdrant)           (Neo4j)
              ↓                 ↓
        Facts stored    Relationships stored
              └────────┬────────┘
                       ↓
              Complete Memory System
```

**Congratulations!** You've built a production-ready memory system with:
- ✅ Short-term memory (conversation history)
- ✅ Long-term vector memory (facts)
- ✅ Knowledge graph (relationships)

🎉 **Complete AI Memory Implementation!**



