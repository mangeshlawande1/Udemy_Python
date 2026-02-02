import os
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


## it will running inside a queue worker 

def process_query(query:str):
    print("Searching chunks:", query)
    search_results = vector_db.similarity_search(query=query)

    # Build context
    context = "\n\n\n".join([
        f'Page Content: {result.page_content}\nPage_Number: {result.metadata["page_label"]}\nFile Location: {result.metadata["source"]}' 
        for result in search_results
    ])

    SYSTEM_PROMPT = f"""
        You are a helpful AI Assistant who answers based on the available context.
        You should only answer the question based on the following context and navigate the user 
        to open the right page number to know more.

        Context:
        {context}
        """
    model = genai.GenerativeModel('gemini-3-flash-preview')
    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser Question: {query}")

    print(f"Response: {response.text}")

    return response.text

