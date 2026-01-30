from mem0 import Memory
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

load_dotenv()

client = OpenAI()

config = {
    "version":"v1.1",
    # give an embedding  model 
    "embedder": {
        "provider":"openai",
        # configuration map 
        "config": {
            "api_key": OPENAI_API_KEY,
            "model":"text-embedding-3-small"
        },
        # which llm do you want to use to extract out the memory 
        "llm":{
            "provider":"openai",
            "config": {
            "api_key": OPENAI_API_KEY,
            "model":"gpt-3.1"
        },
        },
        # Where do you want to store it  
        "vector_store":{
            "provider":"qdrant",
            "config":{
                "host":"localhost",
                "port":6333,
            }
        }
    }
}

# using these config , we can create a memory client    
mem_client = Memory.from_config(config)

## 187 . Vector db setup with docker .


## 188 . Vector db for AI   
# adding some memory 
'''
TO  chat with the model --> 
    we have to give every chat msg to the mem_client.
    import or copy .env file 
    import openai --> make client 
    user_query = input("> ")
    feed it into the client msg 
    print it 

    WE want this particular conversation to be extracted out as a memory.
    client.add(msg=[...,{"role":"assisatant", "content":ai_response}])

    it will extract semantic, factual from this things and stores it 
    until it can able to save memory, but cant able to retrieved the memory 

For Retrieval :     
    add a layer --> search_mem 
    - the search_mem give a dictionary
    - create this dictionary into more simpler string.
    - mem  have an id , which given to you 
    = mem.get("memory")


'''
while True:
    
    user_query = input("> ")

    search_memory = mem_client.search(query=user_query, user_id='vector')


    memories = [
        f"ID: {mem.get("id") }\nMemory: {mem.get("memory")}" for mem in search_memory.get("results")
    ]

    SYSTEM_PROMPT = f"""
        Here is the context about the user :
        { json.dumps(memories)}

    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system","content":SYSTEM_PROMPT},
            { "role":"user","content":user_query}
        ],
        )

    ai_response = response.choices[0].message.content

    print("AI: ", ai_response)

    mem_client.add(
        user_id="Vector",
        messages=[
            {"role":"user", "content":user_query},
            {"role":"assistant", "content":ai_response}
        ]
    )

    print("Memory Has been saved... ")
