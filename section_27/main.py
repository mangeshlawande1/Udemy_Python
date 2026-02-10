from mem0 import Memory
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from langchain_openai import OpenAIEmbeddings
from groq import Groq



load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )


config = {
    "version": "v1.1",
     "llm": {
        "provider": "groq",
        "config": {
            "model": "llama-3.3-70b-versatile",
            "temperature": 0.1,
            "max_tokens": 2000,
        }
    },
    "embedder": {
        "provider": "gemini",
        # "provider": "openai",

        "config": {
             "model": "gemini-embedding-001",
            #  "model": "text-embedding-3-small",
             "api_key":os.getenv("GEMINI_API_KEY"),
        }
    },
    "graph_store":{
        "provider":"neo4j",
        "config":{
            "url":"neo4j+s://06585853.databases.neo4j.io",
            "username":"neo4j",
            "password":"hIxKGrzyNkb_WSo0YxdiKjkvwipygY-IUGr3AfxsTB4",
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "192.168.34.48",
            "port": 6333,
            "collection_name": "mem0_gemini",
            "embedding_model_dims": 768 # Required for text-embedding-004
        }
    }
}


mem_client = Memory.from_config(config)

while True:
    user_query = input("Input--> ")

    # retrived the memory add a layer 
    search_mem = mem_client.search(query=user_query, user_id="mango")
    # it will find only relevant memory, it gives dictionary  

    memories = [
        f" ID: {mem.get("id")}\n Memory: {mem.get("memory")}" for mem in search_mem.get("results")
    ]
    print("Found Memories: ",memories)

    SYSTM_PROMPT =f"""
    Here is the context about the user 
    {json.dumps(memories)}
"""
    response = client.chat.completions.create(
        model='gemini-3-flash-preview',
        # model="llama-3.3-70b-versatile",

        messages=[
            {"role":"system", "content":SYSTM_PROMPT },
            {"role":"user", "content":user_query }
        ]
    )

    ai_response = response.choices[0].message.content

    print("AI:", ai_response)



    mem_client.add(
        messages= [
            {"role":"user", "content": user_query },
            {"role":"assistant", "content" : ai_response }
        ],
        user_id="mango",
    )

    print("Memory has been saved...")






# from openai import OpenAI

# # Point to LMSYS, not OpenAI
# client = OpenAI(base_url="https://api.lmsys.org/v1/", api_key="lm-sys") 




# response = client.chat.completions.create(
#     model="claude-3-opus-20240229",
#     messages=[{"role": "user", "content": "Hello!"}]
# )
# print(response.choices[0].message.content)


"""
what is graph database , what is role of graph memory in memory assiatant , what is knowledge graph , what problem it solve 
why do we nned graph like data structure to store memory more efficiently 
For role users

190. what is  graph in ai and data systems.
graph - is a set of nodes which are connected each other using edges.
- it represent flow and relations ,

191. why graph Memory needed in AI agents 

192. Introduction to graph database Neo4j and Kuzu 
graph database --> neo4j 

193 setup neo4j cloud instance 
- it is heavy  to dockerize 
- how to query these kind of db -- cypher query 

195. Adding graph database Support for Memory Agent 

pip install rank-bm25
"""