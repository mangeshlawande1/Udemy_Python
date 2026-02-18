from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()
client = Client(
    host="http://192.168.34.48:11434"
)



@app.get('/')
def read_root():
    return {"Hello":"World" }


# @app.get("/contact-us")
# def read_root():
#     return {"Email": "mangeshlawande@gmail.com"}

@app.post("/chat")
def chat(
        message: str = Body(..., description="The message ")    
):
    response = client.chat(
        model="llama3.2",
        messages=[
            {"role":"user", "content":message }
        ])
    return {"response": response.message.content }

    


#  fastapi dev server.py