from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()

pdf_path = Path(__file__).parent/ "nodejs.pdf"

## load this file in python program 

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

print(docs[2])

## Chunking -> split the docs into smaller chunk 

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size= 1000,
     chunk_overlap=400,
)
chunks = text_splitter.split_documents(documents=docs)
 
 ## create vector Embedding from this chunk 
 ## can do it manually


# embedding_model =OpenAIEmbeddings(
#     model="gemini-embedding-001",
# )


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


vectorstore = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url="http://192.168.34.48:6333",
    collection_name = "learning_rag"
)



# vector_store = QdrantVectorStore.from_documents(
#     documents=chunks,
#     embedding=embedding_model,
#     url="http://192.168.34.48:6333",
#     collection_name = "learning_rag"
# );


print("Indexing of documents is done... ")


