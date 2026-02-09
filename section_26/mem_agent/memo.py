from mem0 import MemoryClient
from openai import OpenAI
import os
from dotenv import load_dotenv
import time
from mem0 import Memory


load_dotenv()

# mem_client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))


config = {
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-3-flash-preview",
            "temperature": 0.1,
        }
    },
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "gemini-embedding-001",
            "api_key": os.getenv("GEMINI_API_KEY")

        }
    },
    "vector_store": {
        "provider": "qdrant",  # Or chroma, pinecone, etc.
        "config": {
            "host": "192.168.34.48",
            "port": 6333,
            "collection_name": "mem0_gemini",
            "embedding_model_dims": 768 # Required for text-embedding-004
        },
    }
}

# m = Memory.from_config(config)

mem_client = Memory.from_config(config)


# client = OpenAI(
#     api_key=os.getenv("GEMINI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com" # Changed v1beta to v1
)

user_id = "mango"

def extract_memories_from_response(response):
    """Extract memories list from API response"""
    if isinstance(response, dict) and 'results' in response:
        return response['results']
    elif isinstance(response, list):
        return response
    else:
        return []

def extract_memory_text(mem):
    """Extract text from a single memory"""
    if isinstance(mem, str):
        return mem
    elif isinstance(mem, dict):
        return (mem.get('memory') or 
                mem.get('text') or 
                mem.get('content') or 
                mem.get('data') or
                str(mem))
    else:
        return str(mem)

def show_all_memories():
    """Display all stored memories"""
    all_response = mem_client.get_all( user_id=user_id )
    #all_response =  mem_client.get_all(filters={"user_id": user_id})
    all_memories = extract_memories_from_response(all_response)
    
    print(f"\n📚 Total memories stored: {len(all_memories)}")
    
    if all_memories:
        print("\n" + "="*60)
        print("All Your Memories:")
        print("="*60)
        for i, m in enumerate(all_memories, 1):
            memory_text = extract_memory_text(m)
            print(f"{i}. {memory_text}")
        print("="*60)
    else:
        print("No memories stored yet.")

def chat(user_query):
    """Process a single chat interaction"""
    
    # Search for relevant memories
    search_response = mem_client.search(
        query=user_query,
        # filters={"user_id": user_id},
         user_id=user_id,
        limit=5
    )
    
    # Extract memories from response
    memories = extract_memories_from_response(search_response)
    
    # Build context
    context = ""
    if memories:
        context = "Here's what I remember about the user:\n"
        
        for mem in memories:
            memory_text = extract_memory_text(mem)
            context += f"- {memory_text}\n"
        
        context += "\nUse this information in your response.\n\n"
    
    # Create messages
    messages = []
    if context:
        messages.append({"role": "system", "content": context})
    messages.append({"role": "user", "content": user_query})
    
    # Get AI response
    response = client.chat.completions.create(
        model='gemini-3-flash-preview',
        messages=messages
    )
    
    ai_response = response.choices[0].message.content
    
    print(f"\n🤖 AI: {ai_response}\n")
    
    # Save to memory
    mem_client.add(
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ],
            user_id="mango",
    )
    
    print("✓ Memory saved!")

# Main loop
def main():
    print("="*70)
    print(" Memory-Aware Gemini Chatbot ".center(70, "="))
    print("="*70)
    print("\nCommands:")
    print("  • Type your message to chat")
    print("  • '/memories' - View all stored memories")
    print("  • '/clear' - Clear all memories")
    print("  • '/quit' or '/exit' - Exit the program")
    print("="*70)
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['/quit', '/exit', '/q']:
                print("\n👋 Goodbye! Your memories have been saved.")
                break
            
            elif user_input.lower() == '/memories':
                show_all_memories()
                continue
            
            elif user_input.lower() == '/clear':
                confirm = input("⚠️  Are you sure you want to clear all memories? (yes/no): ")
                if confirm.lower() == 'yes':
                    # Delete all memories
                    all_response = mem_client.get_all(filters={"user_id": user_id})
                    all_memories = extract_memories_from_response(all_response)
                    
                    for mem in all_memories:
                        if isinstance(mem, dict) and 'id' in mem:
                            mem_client.delete(memory_id=mem['id'])
                    
                    print("✓ All memories cleared!")
                else:
                    print("Cancelled.")
                continue
            
            # Normal chat
            chat(user_input)
            
            # Small delay for memory indexing
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Continuing...\n")

if __name__ == "__main__":
    main()