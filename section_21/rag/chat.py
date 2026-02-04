import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from openai import OpenAI

load_dotenv()

# Configure OpenAI client to use Google's Gemini API
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Use Google embeddings
embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Vector DB connection 
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://192.168.34.48:6333",
    collection_name="learning_rag"
)

# User input 
user_query = input("Ask something :: ")

# Similarity search
search_result = vector_db.similarity_search(query=user_query)

# Build context
context = "\n\n\n".join([
    f'Page Content: {result.page_content}\nPage_Number: {result.metadata["page_label"]}\nFile Location: {result.metadata["source"]}' 
    for result in search_result
])

SYSTEM_PROMPT= f"""You are a helpful AI Assistant who answers based on the available context.
You should only answer the question based on the following context and navigate the user 
to open the right page number to know more.

Context:
{context}"""

# Create chat completion request
response = client.chat.completions.create(
    model="gemini-3-flash-preview", 
    messages=[
        {
            "role": "system",
            "content":SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
)

# Print the result
print(f"Response: {response.choices[0].message.content}")



'''import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

load_dotenv()

# Configure Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use Google embeddings
embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Vector DB connection 
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://192.168.34.48:6333",
    collection_name="learning_rag"
)

# User input 
user_query = input("Ask something :: ")

# Similarity search
search_result = vector_db.similarity_search(query=user_query)

# Build context
context = "\n\n\n".join([
    f'Page Content: {result.page_content}\nPage_Number: {result.metadata["page_label"]}\nFile Location: {result.metadata["source"]}' 
    for result in search_result
])

SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who answers based on the available context.
You should only answer the question based on the following context and navigate the user 
to open the right page number to know more.

Context:
{context}
"""

# Use Gemini properly
model = genai.GenerativeModel('gemini-3-flash-preview')
response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser Question: {user_query}")

print(f"Response: {response.text}")'''