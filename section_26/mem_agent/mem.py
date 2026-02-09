from mem0 import Memory
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from langchain_openai import OpenAIEmbeddings


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



config = {
    "version": "v1.1",
     "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-3-flash-preview",
            "temperature": 0.1,
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


"""
we build a memory aware assistant ,using mem0, qdrantdb and 
this is how we use memory in your apps.

"""



# from mem0 import Memory
# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# import json

# OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")

# load_dotenv()

# client = OpenAI()

# config = {
#     "version":"v1.1",
#     # give an embedding  model 
#     "embedder": {
#         "provider":"openai",
#         # configuration map 
#         "config": {
#             "api_key": OPENAI_API_KEY,
#             "model":"text-embedding-3-small"
#         },
#         # which llm do you want to use to extract out the memory 
#         "llm":{
#             "provider":"openai",
#             "config": {
#             "api_key": OPENAI_API_KEY,
#             "model":"gemini-3-flash-preview"
#         },
#         },
#         # Where do you want to store it  
#         "vector_store":{
#             "provider":"qdrant",
#             "config":{
#                 "host":"192.168.34.48",
#                 "port":6333,
#             }
#         }
#     }
# }

# # using these config , we can create a memory client    
# mem_client = Memory.from_config(config)

# ## 187 . Vector db setup with docker .


# ## 188 . Vector db for AI   
# # adding some memory 
# '''
# TO  chat with the model --> 
#     we have to give every chat msg to the mem_client.
#     import or copy .env file 
#     import openai --> make client 
#     user_query = input("> ")
#     feed it into the client msg 
#     print it 

#     WE want this particular conversation to be extracted out as a memory.
#     client.add(msg=[...,{"role":"assisatant", "content":ai_response}])

#     it will extract semantic, factual from this things and stores it 
#     until it can able to save memory, but cant able to retrieved the memory 

# For Retrieval :     
#     add a layer --> search_mem 
#     - the search_mem give a dictionary
#     - create this dictionary into more simpler string.
#     - mem  have an id , which given to you 
#     = mem.get("memory")


# '''

# while True:
    
#     user_query = input("> ")

#     search_memory = mem_client.search(query=user_query, user_id='vector')


#     memories = [
#         f"ID: {mem.get("id") }\nMemory: {mem.get("memory")}" for mem in search_memory.get("results")
#     ]

#     SYSTEM_PROMPT = f"""
#         Here is the context about the user :
#         { json.dumps(memories)}

#     """

#     response = client.chat.completions.create(
#         model="gpt-4.1-mini",
#         messages=[
#             {"role": "system","content":SYSTEM_PROMPT},
#             { "role":"user","content":user_query}
#         ],
#         )

#     ai_response = response.choices[0].message.content

#     print("AI: ", ai_response)

#     mem_client.add(
#         user_id="Vector",
#         messages=[
#             {"role":"user", "content":user_query},
#             {"role":"assistant", "content":ai_response}
#         ]
#     )

#     print("Memory Has been saved... ")

