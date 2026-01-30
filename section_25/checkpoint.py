from dotenv import load_dotenv
from typing_extensions import TypedDict
from  typing import Annotated
from langgraph.graph.message import add_messages
from langchain.graph import Stategraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()


llm = init_chat_model(
    model= "gpt-4.1-mini",
    model_provider="openai"
)

class State(TypedDict):
    messages:Annotated[list, add_messages]

def chatbot(state:State):
    response = llm.invoke(state.get("messages"))
    return {"messages":[response]}


"""

...
...
...

"""
# add random function for assumption 

graph_builder = Stategraph(State)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge( "chatbot", END)

graph = graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
      return graph_builder.compile(checkpointer=checkpointer)  
     

DB_URI ="MONGODB://admin:admin@localhost:27017"  
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
# open a  connection build a graph with checkpointer do whatever you want to do close the conn
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)

    config ={
        "configurable":    {
            "thread_id":"langgraph",

        },
        }
    
# instead of invoke , you can stream the graph 

    for chunk in  graph_with_checkpointer.stream(
        State({"messages":["Hey, what's the status of checkpoint?"]}),
        config,
        stream_mode = "values"
        ):
         chunk["messages"][-1].pretty_print()
         # print last message

         

    # close a connection 
    # print("\n\nupdated_state: ",updated_state)


