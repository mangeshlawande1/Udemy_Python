# RAG (Retrieval Augmented Generation) - Problem Statement

## The Business Problem

**Scenario**: A company (e.g., law firm) has:
- Thousands of PDF documents
- Case files, contracts, legal documents
- Too much data for humans to manually search

**What they want**:
- Employees ask questions in natural language
- AI finds relevant information from their private documents
- AI provides answers with source references

## Example Query
```
User: "Tell me about case number 32"
```

**Expected AI Response**:
- Details about case #32
- Parties involved
- Current status
- **Source**: "Found in file X, page Y"

## The Two Core Problems

### Problem 1: LLMs Don't Know Your Private Data
```
LLM Training Data = Public Internet Data
Your Business Data = Private, Internal Files
                  ↓
LLM has ZERO context about your documents
```

### Problem 2: Context Window Limitations
```
You have: 1,000+ documents
LLM accepts: Limited context window (e.g., 128K tokens)
                  ↓
Cannot feed ALL documents to LLM at once
```

**Even if possible**:
- Extremely expensive (paying for all tokens every query)
- Slow processing
- Impractical for production

## What RAG Solves

Instead of feeding everything:
1. **Retrieve** only relevant chunks from documents
2. **Augment** the LLM prompt with just those chunks
3. **Generate** answer based on relevant context only

**Result**: Fast, cost-effective, accurate answers from private data

## Why RAG Matters
- **90% of enterprise AI use cases** involve RAG
- Production-critical skill
- Enables AI on private/proprietary data

-----------------------------------------------------------------------------

# RAG Solution: Naive Approach

## What is RAG?
**Retrieval Augmented Generation** - An AI framework that combines LLMs with external knowledge sources.

---

## Naive Solution (Simple but Limited)

### The Approach
```
Step 1: Convert all files → Text
Step 2: Put ALL text in system prompt
Step 3: User asks questions
Step 4: LLM answers using the context
```

### System Prompt Example
```
You are an AI assistant that helps users talk to their data.

Available Data:
[... ALL 1000 files converted to text ...]
```

### Does It Work?
✅ **Yes**, technically it works for small datasets

---

## Problems with Naive Approach

### Problem 1: Cost 💰
- Sending massive amounts of tokens every query
- API costs scale with token count
- Very expensive for large datasets

### Problem 2: Context Window Limit 📏
Even with 1 million token windows:

```
50,000 files × 10 pages = 500,000 pages
500,000 pages × 250 characters = Too much data!
```

**Result**: Cannot fit all data in context window

---

## When Naive RAG Works
✅ Only **1 file** with **2-3 pages**
❌ Does NOT scale to thousands of files

---

## Key Takeaway

| Aspect | Naive RAG |
|--------|-----------|
| Simplicity | ✅ Very simple |
| Small data | ✅ Works |
| Large data | ❌ Fails |
| Cost | ❌ Expensive |
| Scalability | ❌ None |

**Next**: How to make RAG scalable for 50,000+ files using smart retrieval!

--------------------------------------------------------


# RAG: Indexing Phase Explained

## Two Phases of RAG

| Phase | Purpose |
|-------|---------|
| **Indexing Phase** | Users provide/upload data |
| **Retrieval Phase** | Users chat with the data |

These are **completely separate** with different code!

---

## Indexing Phase: Step-by-Step

### Step 1: Chunking 📄➡️📑
**Split large documents into smaller pieces**

```
Large Document → [Chunk A] [Chunk B] [Chunk C] [Chunk D]...
```

**Chunking strategies:**
- By **page** (1 page = 1 chunk)
- By **paragraph** (1 paragraph = 1 chunk)
- By **character count** (250 chars = 1 chunk)
- Your choice based on use case!

---

### Step 2: Create Embeddings 📑➡️🔢
**Convert each chunk to vector embeddings**

```
[Chunk A] → Embedding Model → [0.23, -0.45, 0.89, ...]
[Chunk B] → Embedding Model → [0.12, 0.67, -0.34, ...]
[Chunk C] → Embedding Model → [-0.56, 0.23, 0.78, ...]
```

Use OpenAI embeddings or any embedding model.

---

### Step 3: Store in Vector Database 🔢➡️🗄️
**Save embeddings + content + metadata**

```
Vector DB stores:
├── Chunk A
│   ├── Vector: [0.23, -0.45, 0.89, ...]
│   ├── Content: "Actual text of chunk A..."
│   └── Metadata: {doc: "file1.pdf", page: 3}
├── Chunk B
│   ├── Vector: [0.12, 0.67, -0.34, ...]
│   ├── Content: "Actual text of chunk B..."
│   └── Metadata: {doc: "file1.pdf", page: 4}
```

**Popular Vector Databases:** Pinecone, Weaviate, Chroma, Qdrant

---

## Indexing Phase Flow

```
Documents → Chunking → Embedding Model → Vector DB
    📄         📑           🔢              🗄️
```

---

## What's Stored in Vector DB?

| Field | Description |
|-------|-------------|
| **Vectors** | Numerical representation of chunk |
| **Content** | Original text of the chunk |
| **Metadata** | Page number, document name, etc. |

---

## Key Takeaway
Indexing phase **prepares** your data for fast retrieval later. The heavy processing happens once during indexing, making chat queries fast and efficient!

**Next**: How to use indexed data in the Retrieval Phase!


--------------------------------------
# RAG: Retrieval Phase Explained

## Retrieval Phase: Step-by-Step

### Step 1: User Query → Embeddings
```
User: "Tell me about case number 32"
                ↓
        Embedding Model
                ↓
    Query Vector: [0.45, -0.23, 0.67, ...]
```

---

### Step 2: Vector Similarity Search
```
Query Vector → Search Vector DB → Find Similar Vectors
                                        ↓
                            Return Relevant Chunks Only!
```

**Key Point**: Out of 50,000 chunks, you get only 2-3 relevant ones!

---

### Step 3: Get Chunk Data
Each returned chunk contains:
- ✅ **Content**: The actual text/paragraph
- ✅ **Metadata**: Page number, document name
- ❌ Vectors (not needed anymore)

---

### Step 4: Send to LLM
```python
System Prompt:
"You are an AI assistant. Here is the relevant data:

Chunk 1: [content from case 32...]
Source: document.pdf, Page 15

Chunk 2: [more relevant content...]
Source: document.pdf, Page 16"

User Query: "Tell me about case number 32"
```

---

### Step 5: LLM Response
```
"Case number 32 involves [details]...
You can find this information on Page 15-16 of document.pdf"
```

---

## Complete RAG Pipeline

```
┌─────────────────── INDEXING PHASE ───────────────────┐
│  Documents → Chunking → Embeddings → Vector DB       │
└──────────────────────────────────────────────────────┘
                          ↓
┌─────────────────── RETRIEVAL PHASE ──────────────────┐
│  User Query → Embeddings → Similarity Search         │
│       ↓                           ↓                  │
│  Relevant Chunks ──────────────→ LLM → Response      │
└──────────────────────────────────────────────────────┘
```

---

## Why This Works

| Naive Approach | RAG Approach |
|----------------|--------------|
| Send ALL data to LLM | Send ONLY relevant chunks |
| 50,000 chunks | 2-3 chunks |
| Expensive | Cost-effective |
| Hits context limits | Fits easily |
| Slow | Fast |

---

## Key Takeaway
**RAG = Smart filtering before LLM call**

Instead of overwhelming the LLM with everything, you retrieve only what's relevant, making it scalable for millions of documents!

----------------------------------------------------

# Setting Up Vector Database for RAG

## Vector Database Options

| Database | Type | Notes |
|----------|------|-------|
| **Pinecone** | Managed/Hosted | Not open source |
| **Weaviate** | Open Source | Self-hosted option |
| **ChromaDB** | Open Source | Popular choice |
| **PGVector** | Open Source | PostgreSQL extension |
| **Qdrant** | Open Source | Lightweight, fast ⭐ |

**Chosen: Qdrant** - Easy setup, lightweight, fast!

---

## Prerequisites
- **Docker** installed and running
- Basic Docker knowledge (essential for developers!)

---

## Setup Steps

### 1. Create Project Structure
```
rag/
├── docker-compose.yml
```

### 2. Docker Compose File
```yaml
services:
  vector_database:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
```

### 3. Start Qdrant
```bash
# Navigate to rag folder
cd rag

# Run in detached mode (background)
docker compose up -d
```

---

## Verify Setup

**Check Docker Desktop:**
- Container: `rag` → `vector_database`
- Status: Running
- Port: 6333 exposed

**Or via terminal:**
```bash
docker ps
```

---

## Key Points

| Command | Purpose |
|---------|---------|
| `docker compose up` | Start (blocks terminal) |
| `docker compose up -d` | Start in background |
| `Ctrl+C` | Stop (if not detached) |
| `docker compose down` | Stop containers |

---

## What's Next?
- Install Python dependencies
- Code the **Indexing Phase**
- Process documents → chunks → embeddings → Qdrant

**Qdrant is now ready to store vector embeddings!**


----------------------------------

# Introduction to LangChain

## What is LangChain?

**LangChain** is a utility library that provides pre-built tools for common AI development tasks.

---

## The Problem It Solves

Without LangChain, developers had to write code from scratch for:
- Reading documents (PDFs, web pages, etc.)
- Chunking documents
- Creating embeddings
- Connecting to vector databases
- Making LLM calls

**LangChain provides ready-made functions for all of this!**

---

## How LangChain Helps Our RAG Pipeline

| Task | LangChain Says |
|------|----------------|
| Read PDF documents | ✅ "I have a loader for that" |
| Split into chunks | ✅ "I have a splitter for that" |
| Create embeddings | ✅ "I have a function for that" |
| Connect to Qdrant/Pinecone | ✅ "I have connectors for that" |

---

## Document Loaders

LangChain supports loading from:
- 📄 PDF files
- 🌐 Web pages
- 🗂️ Sitemaps
- 📁 Various file formats
- And many more...

---

## Installation

```bash
pip install langchain-community pypdf
```

**Packages installed:**
- `langchain` - Core library
- `langchain-community` - Community integrations
- `pypdf` - PDF reading capability
- `text-splitters` - Document chunking

---

## Update Requirements

```bash
pip freeze > requirements.txt
```

---

## Key Takeaway

**LangChain = Toolbox for AI Development**

Instead of reinventing the wheel, use LangChain's pre-built utilities for:
- Document loading
- Text splitting
- Embeddings
- Vector store connections
- LLM integrations

**Next**: Using LangChain to load and process PDF documents!
------------------------------------------------------

# RAG Indexing: Loading and Chunking Documents

## Step 1: Get a Sample PDF

Using a Node.js PDF (104 pages) downloaded from the internet.

**File structure:**
```
rag/
├── docker-compose.yml
├── index.py          # New file for indexing
└── nodejs.pdf        # Sample PDF document
```

---

## Step 2: Load PDF with LangChain

### Code: `index.py`

```python
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

# Get PDF file path
pdf_path = Path(__file__).parent / "nodejs.pdf"

# Create PDF loader
loader = PyPDFLoader(file_path=pdf_path)

# Load all pages
docs = loader.load()

# Test: Print page 12
print(docs[12])
```

### What `loader.load()` Returns:
- List of documents (one per page)
- Each document contains:
  - `page_content`: The text content
  - `metadata`: Page number, source file, etc.

---

## Output Example

```python
Document(
    page_content="JavaScript is a programming language...",
    metadata={'source': 'nodejs.pdf', 'page': 12}
)
```

---

## Summary So Far

| Step | Status | Tool Used |
|------|--------|-----------|
| Load PDF | ✅ Done | `PyPDFLoader` |
| Page-by-page access | ✅ Done | `loader.load()` |
| Chunking | ⏳ Next | Text Splitters |

---

## Key Points

1. **`PyPDFLoader`** - LangChain utility for reading PDFs
2. **`loader.load()`** - Returns list of page documents
3. **Each page** is accessible by index (`docs[0]`, `docs[1]`, etc.)
4. **No manual PDF parsing** - LangChain handles it!

---

## What's Next?
**Chunking** - Split pages into smaller pieces using LangChain's text splitters!

-----------------------------------------------------------------------------

# RAG Indexing: Smart Chunking with LangChain

## Why Chunking?
Breaking large documents into smaller, manageable pieces for:
- Better embedding quality
- Fitting within context windows
- More precise retrieval

---

## Installation

```bash
pip install langchain-text-splitters
pip freeze > requirements.txt
```

---

## Code: Text Splitting

```python
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load PDF
pdf_path = Path(__file__).parent / "nodejs.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# Split into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks = text_splitter.split_documents(docs)
```

---

## Understanding Chunk Overlap

### Without Overlap ❌
```
[Chunk 1] | [Chunk 2] | [Chunk 3]
   ↓           ↓           ↓
Context lost between chunks!
```

### With Overlap ✅
```
[----Chunk 1----]
         [----Chunk 2----]
                  [----Chunk 3----]
```

**Overlap = Recap from previous chunk**
- Preserves context continuity
- Important information isn't cut off
- Better understanding for embeddings

---

## Parameters Explained

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `chunk_size` | 1000 | Max characters per chunk |
| `chunk_overlap` | 400 | Characters shared between chunks |

---

## What We Have Now

```
104-page PDF → docs (pages) → chunks (small pieces)
```

| Step | Input | Output |
|------|-------|--------|
| Loading | PDF file | 104 page documents |
| Chunking | Page documents | Many smaller chunks |

---

## Summary

✅ **2 lines of code** to convert pages into smart chunks!

```python
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(docs)
```

**Next**: Create vector embeddings from chunks!

---------------------------------------------------


# RAG Indexing: Creating Embeddings & Storing in Qdrant

## Overview
Final step of indexing: Convert chunks → embeddings → store in vector DB

---

## Installation

```bash
pip install langchain-openai langchain-qdrant
```

---

## Complete Indexing Code: `index.py`

```python
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# Load environment variables
load_dotenv()

# 1. Load PDF
pdf_path = Path(__file__).parent / "nodejs.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
chunks = text_splitter.split_documents(docs)

# 3. Create embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# 4. Store in Qdrant
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

print("Indexing of documents done!")
```

---

## Environment Setup

Create `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

---

## Verify in Qdrant Dashboard

**URL**: `http://localhost:6333/dashboard`

After running, you'll see:
- ✅ Collection: `learning_rag`
- ✅ Points: ~192 (your chunks)
- ✅ Each point contains:
  - **Vectors**: Numerical embeddings
  - **Page content**: Original text
  - **Metadata**: Page number, source file, author, etc.

---

## What's Stored in Qdrant

| Field | Content |
|-------|---------|
| **Vectors** | `[0.023, -0.456, 0.789, ...]` |
| **Page Content** | Actual text chunk |
| **Metadata** | Source, page number, author, creator |

---

## Complete Indexing Pipeline

```
PDF File
    ↓
PyPDFLoader (Load)
    ↓
104 Page Documents
    ↓
RecursiveCharacterTextSplitter (Chunk)
    ↓
~192 Smaller Chunks
    ↓
OpenAIEmbeddings (Embed)
    ↓
Vector Embeddings
    ↓
QdrantVectorStore (Store)
    ↓
✅ Qdrant Database
```

---

## Key Takeaway

**4 main components:**
1. `PyPDFLoader` - Load documents
2. `RecursiveCharacterTextSplitter` - Chunk documents
3. `OpenAIEmbeddings` - Create vectors
4. `QdrantVectorStore` - Store everything

**Indexing complete! Next: Retrieval phase** 🎉

---------------------------------------------

# RAG Retrieval: Chatting with Your Documents

## Retrieval Flow
```
User Query → Embeddings → Similarity Search → Relevant Chunks → LLM → Response
```

---

## Complete Retrieval Code: `chat.py`

```python
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

# Load environment variables
load_dotenv()

# 1. Setup embedding model (same as indexing!)
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# 2. Connect to existing Qdrant collection
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model
)

# 3. Get user query
user_query = input("Ask something: ")

# 4. Similarity search - get relevant chunks
search_results = vector_db.similarity_search(query=user_query)

# 5. Build context from results
context = "\n\n".join([
    f"Page Content: {result.page_content}\n"
    f"Page Number: {result.metadata.get('page', 'N/A')}\n"
    f"Source: {result.metadata.get('source', 'N/A')}"
    for result in search_results
])

# 6. Create system prompt with context
system_prompt = f"""You are a helpful AI assistant who answers user queries 
based on the available context retrieved from a PDF file.
Along with the page content and page number, you should only answer 
based on the following context and navigate user to open the right 
page number to know more.

Context:
{context}
"""

# 7. Call OpenAI
openai_client = OpenAI()

response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
)

# 8. Print response
print(f"🤖 {response.choices[0].message.content}")
```

---

## Key Differences from Indexing

| Indexing | Retrieval |
|----------|-----------|
| `from_documents()` | `from_existing_collection()` |
| Store chunks | Search chunks |
| One-time process | Every user query |

---

## Example Interactions

**Query 1:**
```
Ask something: Can you help me understand debugging in Node.js?

🤖 Here's a quick overview... [examples from book]
   See page 23-24 for more details.
```

**Query 2:**
```
Ask something: Can you help me understand arrow functions?

🤖 Here's a quick guide... [examples from book]
   Check page 20-21 for more information.
```

---

## What Happens Behind the Scenes

```
1. User: "debugging in Node.js"
          ↓
2. Embedding Model → [0.23, -0.45, ...]
          ↓
3. Qdrant Similarity Search
          ↓
4. Returns: Chunks from pages 23, 24
          ↓
5. System Prompt + Context + Query → GPT-4
          ↓
6. Response with page references
```

---

## Complete RAG Pipeline Summary

```
┌─── INDEXING (one-time) ───┐
│ PDF → Chunks → Embeddings │
│         → Qdrant          │
└───────────────────────────┘
            ↓
┌─── RETRIEVAL (per query) ───┐
│ Query → Embeddings          │
│      → Similarity Search    │
│      → Relevant Chunks      │
│      → LLM → Response       │
└─────────────────────────────┘
```

---

## Key Takeaways

1. **Same embedding model** for indexing AND retrieval
2. **Similarity search** returns only relevant chunks
3. **Context injection** into system prompt
4. **Page references** help users verify information
5. **Works with any data** - not just PDFs!

**Congratulations! You've built a complete RAG system!** 🎉


