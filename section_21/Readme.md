## Building chat with PDF Project Using RAG     
143 - 153
### Intro to RAG:
what is problem statement the rag trying to solve, 
we have all the data in pdf file , they have a lof of documents difficult to read them, lot fo manual process 
can you build some ai agent --
takes user query --> search this query in specific data, we have to search which is relevent content to this particular query.  

1. LLM doesnt have context about your data.(private data)
2. you cant give all file to llm as context limited context window .


- 145 Native retrived  based solution Approach.
take some pdf --> convert it into text --> prepare a system prompt 
you are ai assistant which can help user talk to their data 

Available data 
(Text) 
can you tell me about xyz .
sure this is what i got 
now here is query 2 
response.
 
 Problems :
 1. Cost 
 2. Context Window(1 Token Window)

How can you inges 50000 files into llm 
how can we optimize this thing better and make more scalable .
you have 2 phases you can make a rag 

1. indexing phase --> Provide the data (upload documents)
--> chunk the data (page level , para level ) data spilition 
what kind of data it hold for every chunk.
--> give every chunk to this embedding model    
Q: expect ths use to provide some data 
split the data __ pass it to the vector embedder __ create vector Embedding __ store it into vector data base (stores the actual content, some metadata [pageno, docs]) along with vectordb 



2. retrieval phase -->  chatting with the data 


### chunking --> give it to vector Embedding Mode 
How can you use indexing phase in retrival Phase with your 1000 files ? 


147. RAG Pipeline - Retrieval Phase Mechanism in depth 

Retrival 
 user_query __ vector Embedding __ Embedding Model __ Vector Embedding Query __ to vector DB(Vector similarity search)
 user trying to ask tihs can you search this vector and gove me relevant document/chunk 

 it will get only the relavent chunk instead of all the chunk 
 -- drop the vectors 

-------------------------------------
Perfect, this is **exactly** the right way to think about RAG.
I’ll clean this up, formalize it, and explain it **end-to-end**, but I’ll keep your language, flow, and intuition intact.

---

# 1. Problem Statement RAG Is Trying to Solve

### Real-world problem

You have:

* **Thousands of PDFs**
* Internal / private data
* Unstructured text
* Manual search is slow
* Humans must read documents to answer simple questions

User wants:

> “Can you tell me about **XYZ**?”

### Why LLM alone fails

### ❌ Problem 1: No private data

LLMs:

* Don’t know your PDFs
* Don’t know your internal docs
* Don’t know your company data

---

### ❌ Problem 2: Context window limit

Even GPT-4:

* Limited tokens
* Cannot load **50,000 PDFs**
* Sending everything every time = impossible

---

### ❌ Problem 3: Cost

* Sending full docs every query = 🔥💸
* Repeated tokens = repeated cost

---

### ❌ Problem 4: Manual workflows

* Humans reading PDFs
* Searching keywords manually
* High latency, high error

---

## 🎯 Core RAG Goal

> **Allow users to talk to their own data accurately, cheaply, and at scale.**

---

# 2. Naive Approach (What people try first)

### “Native Retrieval Based Solution” (Naive)

```
PDF → Text
Text → System Prompt
User Query → LLM
```

Example prompt:

```
You are an AI assistant.
Here is the data:
<ALL PDF TEXT>

User: Can you tell me about XYZ?
```

### Why this fails ❌

| Issue         | Why                    |
| ------------- | ---------------------- |
| Cost          | Huge tokens per query  |
| Context limit | LLM can’t fit it       |
| Slow          | Re-sending data        |
| Not scalable  | 1000+ files impossible |

---

# 3. How RAG Solves This (High Level)

RAG splits the problem into **two distinct phases**:

```
1. Indexing Phase  (offline, one-time cost)
2. Retrieval Phase (online, per-query)
```

This is the key insight.

---

# 4. Phase 1: Indexing Phase (Data Preparation)

### Goal

Convert **unstructured documents** into **searchable semantic memory**

---

## Step 1: Ingest documents

Input:

* PDFs
* Docs
* HTML
* Text files

Process:

```
PDF → Text extraction
```

---

## Step 2: Chunking (CRITICAL)

Why chunking?

* Embeddings work best on small, meaningful text
* One vector = one semantic idea

### Chunking strategies

| Strategy                       | When to use            |
| ------------------------------ | ---------------------- |
| Page-level                     | Legal, research papers |
| Paragraph-level                | Articles               |
| Sentence-level                 | FAQs                   |
| Fixed tokens (e.g. 500 tokens) | General use            |

Example:

```
Document
 ├── Chunk 1 (para 1)
 ├── Chunk 2 (para 2)
 ├── Chunk 3 (para 3)
```

---

## Step 3: What each chunk contains

Each chunk stores:

```json
{
  "chunk_text": "Actual content text",
  "embedding": [0.012, -0.98, ...],
  "metadata": {
    "document_id": "file_123",
    "page_no": 4,
    "source": "policy.pdf"
  }
}
```

👉 Metadata is **very important**

* Traceability
* Source citation
* Debugging

---

## Step 4: Create Vector Embeddings

### What is an embedding?

* A vector representation of meaning
* Similar meanings → closer vectors

Process:

```
Chunk → Embedding Model → Vector
```

Example:

```
"Refund policy" → [0.23, -0.91, ...]
"Return policy" → [0.24, -0.89, ...]
```

➡️ Semantically close

---

## Step 5: Store in Vector Database

Vector DB stores:

* Vector
* Text
* Metadata

Popular vector DBs:

* Pinecone
* Weaviate
* FAISS
* Chroma
* Qdrant

### After indexing

You can have:

* 50,000 files
* Millions of chunks
* Stored **once**
* No LLM calls during indexing except embeddings

---

# 5. Phase 2: Retrieval Phase (Chatting with Data)

This is **runtime**, happens per user query.

---

## Step 1: User Query

User asks:

> “Can you tell me about XYZ?”

---

## Step 2: Query Embedding

Same embedding model is used:

```
User Query → Embedding Model → Query Vector
```

⚠️ Important:
**Indexing embeddings and query embeddings must use the SAME model**

---

## Step 3: Vector Similarity Search

Query vector is sent to vector DB:

```
Vector DB.search(
  query_vector,
  top_k=5
)
```

The DB returns:

* Only the **most relevant chunks**
* Based on cosine similarity / dot product

Example result:

```
Chunk 12 (policy.pdf, page 5)
Chunk 87 (refunds.pdf, page 2)
Chunk 201 (faq.pdf, page 1)
```

---

## Step 4: Drop everything else

🚮 All irrelevant chunks are ignored

Instead of:

* 1,000 files
* 1,000,000 chunks

You now have:

* 5–10 relevant chunks only

This solves:

* Context window
* Cost
* Latency

---

## Step 5: Prompt Construction

Now you build a **small, precise prompt**:

```
System:
You are an AI assistant that answers questions using ONLY the provided context.

Context:
[Chunk 1 text]
[Chunk 2 text]
[Chunk 3 text]

User:
Can you tell me about XYZ?
```

---

## Step 6: LLM Generation

LLM:

* Reads limited context
* Generates grounded answer
* Can cite source

---

# 6. Why This Scales to 50,000+ Files

### Key insight:

**LLM never sees all data**

| Phase     | LLM Used?           | Cost         |
| --------- | ------------------- | ------------ |
| Indexing  | ❌ (only embeddings) | One-time     |
| Retrieval | ✅                   | Small tokens |
| Search    | ❌ (vector DB)       | Cheap        |

---

## Cost optimization

* Embeddings are **cheap**
* Search is **O(log n)** or ANN
* LLM only sees **relevant chunks**

---

# 7. Summary Diagram (Mental Model)

```
INDEXING PHASE
PDFs
 ↓
Text
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector DB
```

```
RETRIEVAL PHASE
User Query
 ↓
Query Embedding
 ↓
Vector Search
 ↓
Top-K Chunks
 ↓
Prompt
 ↓
LLM Answer
```

---

# 8. Final One-Line Definition of RAG

> **RAG is a system that augments an LLM with external, searchable knowledge by retrieving only the most relevant pieces of data at query time.**

-------------------------------------


148. Local vector db setup with docker compose ::
- PineconeDB: A hosted managed service 
- Weaviate : Opensource 
- Chrome DB 
- PG vector DB
- Qdrant DB 

QdrantDB _ Easy to setup 
- fast and lightweight 

To setup locally need have knowledge of docker 

> docker compose up

> docker compose up -d 

149. Langchain Installation & Setup 
- the utility which its provides 
connection to vector db writing a document making some ai call   

- provide lot of tools out of the box 
- reading a docs --> use utility 
- converting docs in pieces of chunk -- use utility     
- create vector embedding & send it to vector db , 
connect pinecone to qdrantdb -- also have utility 

- search langchain document loaders 

- install py pdf 

how can we load and chunk of pdf 
- index file responsible for 
indexing the data 


151. 
how we can do smart chunking 
- search for langchin textsplit -- docspliter
- install langchian textsplitter

- import 
- size , chunk_overlap=400

152. 
 ## create vector Embedding from this chunk 
 ## can do it manually
 - install langchain openai embedding 


embedding_model =OpenAIEmbeddings(
    model="text-embedding-3-large",
);

this needs to create  embeddings for this chunks and store it in qdrant db 

- search langchain qdrant db 

- when user gives a query you use an embedding model,
to create embeddiign query you search something your yector db you jbring back the relevant chunk you give that chunk to chat model with the query and response , its a retrival part 

-----------------------------------------------

Awesome — this is basically **“RAG engineering from zero to working system”**.
I’ll explain this **step-by-step**, connect all the dots, and keep it practical (what / why / how).

I’ll structure it like a **lecture + implementation guide**.

---

# 1. Local Vector DB Setup – Big Picture

When building RAG, you need **persistent semantic memory**.
That memory lives in a **Vector Database**.

You have **two choices**:

## Option A: Managed (Hosted)

* Pinecone
* No infra headache
* Costs money
* Internet required

## Option B: Local / Self-hosted

* Weaviate
* Chroma
* PGVector
* Qdrant

👉 For **learning + local dev**, we use **Docker-based vector DBs**

---

# 2. Vector DB Comparison (Very Important)

| DB         | Type         | Managed | Local | Notes                 |
| ---------- | ------------ | ------- | ----- | --------------------- |
| Pinecone   | SaaS         | ✅       | ❌     | Best managed          |
| Weaviate   | Open source  | ✅       | ✅     | Heavy but powerful    |
| ChromaDB   | Open source  | ❌       | ✅     | Simple, dev-friendly  |
| PGVector   | Postgres ext | ❌       | ✅     | SQL + vectors         |
| **Qdrant** | Open source  | ❌       | ✅     | **Fast, lightweight** |

👉 **Qdrant is the best balance**
Fast, Rust-based, production-grade, easy Docker setup.

---

# 3. Why QdrantDB?

### Qdrant advantages

* Written in Rust (fast)
* Lightweight
* Easy Docker setup
* Supports:

  * Cosine similarity
  * Metadata filtering
  * Hybrid search
* LangChain support out-of-the-box

👉 That’s why most tutorials & startups use Qdrant locally.

---

# 4. Docker Basics (Required Knowledge)

### Why Docker?

* Vector DB is a server
* Needs persistence
* Needs ports
* Docker gives isolated, reproducible environment

---

## Key commands

```bash
docker compose up
```

* Runs services
* Shows logs
* Blocks terminal

```bash
docker compose up -d
```

* Runs in background (detached)
* Preferred for dev

---

# 5. Qdrant Local Setup with Docker Compose

### Step 1: Create `docker-compose.yml`

```yaml
version: "3.8"

services:
  qdrant:
    image: qdrant/qdrant
    container_name: qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_data:/qdrant/storage
```

### Step 2: Start Qdrant

```bash
docker compose up -d
```

### Step 3: Verify

Open browser:

```
http://localhost:6333
```

If it loads → Qdrant is running ✅

---

# 6. LangChain – What & Why?

### What is LangChain?

LangChain is **NOT an LLM**
It is a **framework for building LLM-powered applications**

### What LangChain gives you

| Feature              | Why it matters   |
| -------------------- | ---------------- |
| Document loaders     | Load PDFs, docs  |
| Text splitters       | Smart chunking   |
| Embedding wrappers   | Easy embeddings  |
| Vector DB connectors | Pinecone, Qdrant |
| Retrieval chains     | RAG pipelines    |
| Tool integration     | Agents           |

👉 Without LangChain, you write **a LOT** of glue code.

---

# 7. LangChain Installation & Setup

```bash
pip install langchain langchain-community langchain-openai
```

Additional dependencies:

```bash
pip install pypdf
pip install qdrant-client
```

---

# 8. Loading PDF Documents

### Why document loaders?

PDFs are:

* Binary
* Page-based
* Messy

LangChain handles:

* Parsing
* Page splitting
* Metadata extraction

---

## Load PDF using LangChain

```python
from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/myfile.pdf")
documents = loader.load()
```

### Output

Each page becomes a `Document` object:

```python
Document(
  page_content="Some text...",
  metadata={"page": 1, "source": "myfile.pdf"}
)
```

---

# 9. Why Chunking Is Mandatory

### Problem

Embeddings fail on:

* Large text
* Multiple topics in one chunk

### Solution

Split into **semantically meaningful chunks**

---

# 10. Smart Chunking with LangChain TextSplitters

LangChain provides **document splitters**

```bash
pip install langchain-text-splitters
```

---

## Recommended Splitter

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
```

### Why Recursive?

* Splits by:

  1. Paragraph
  2. Sentence
  3. Words
* Preserves meaning

---

## Chunking Example

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks = text_splitter.split_documents(documents)
```

### Parameters explained

| Param           | Meaning            |
| --------------- | ------------------ |
| `chunk_size`    | Tokens per chunk   |
| `chunk_overlap` | Context continuity |

👉 Overlap avoids broken sentences & lost meaning.

---

# 11. Indexing Phase – Creating Embeddings

### What happens here?

* Each chunk → embedding vector
* Stored once
* One-time cost

---

## Install OpenAI Embeddings

```bash
pip install langchain-openai
```

---

## Create Embedding Model

```python
from langchain_openai import OpenAIEmbeddings

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)
```

---

# 12. Store Embeddings in Qdrant

### Connect LangChain → Qdrant

```python
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient

client = QdrantClient(
    url="http://localhost:6333"
)

vector_store = Qdrant.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="my_docs"
)
```

### What happens internally?

For each chunk:

1. Create vector embedding
2. Store:

   * Vector
   * Text
   * Metadata (page, file)

✅ **Indexing complete**

---

# 13. Retrieval Phase – Chat With Data

This is the **live user interaction phase**

---

## Step 1: User Query

```python
query = "Explain refund policy"
```

---

## Step 2: Query Embedding

```python
query_embedding = embedding_model.embed_query(query)
```

(Same model as indexing!)

---

## Step 3: Vector Search

```python
results = vector_store.similarity_search(
    query,
    k=5
)
```

### Returned:

```python
[
  Document(page_content="...", metadata={...}),
  Document(page_content="...", metadata={...})
]
```

Only **relevant chunks**, nothing else.

---

# 14. Give Context to LLM

Now we construct prompt:

```python
context = "\n\n".join([doc.page_content for doc in results])

prompt = f"""
You are an AI assistant.
Answer using only the context below.

Context:
{context}

Question:
{query}
"""
```

---

## Step 5: Generate Answer

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

response = llm.invoke(prompt)
print(response.content)
```

---

# 15. End-to-End RAG Flow (Final Mental Model)

```
INDEXING (once)
PDF → Loader → Chunking → Embeddings → Qdrant
```

```
RETRIEVAL (per query)
User Query
 → Query Embedding
 → Vector Search
 → Relevant Chunks
 → Prompt
 → LLM Answer
```

---

# 16. Why This Is Scalable (50,000+ Files)

* Vector DB handles millions of chunks
* Search is fast (ANN)
* LLM only sees **top-K chunks**
* Cost stays low
* Context window respected

---

# 17. Final One-Line Summary

> **RAG + LangChain + Qdrant = scalable, private, cost-efficient AI that can talk to your documents.**

---

If you want next, I can:

* Build a **full RAG project structure**
* Explain **hybrid search (BM25 + vectors)**
* Add **re-ranking**
* Add **citations**
* Convert this into an **AI agent**
* Compare **Qdrant vs Pinecone in production**

Just say the word 🚀

----------------------------------------------------------------

