from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph.messages import add_messages
from langchain.graph import Stategraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

llm = init_chat_model(
    model= "gemini-3-flash-preview",
    model_provider="openai"
)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def chatbot(state:State):
    response = llm.invoke(state.get("messages"))
    print("Inside chatbot node :", state)
    # return {"messages":["Hi, This is a message from chat bot Node "]}
    return response


def samplenode(state:State):
    print("Inside samplenode node :", state)
    return {"messages":[" sample msgs "]}

graph_builder = Stategraph(State)

# register a graph 
graph_builder.add_node("xyz", chatbot)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge( "chatbot", "samplenode")
graph_builder.add_edge( "samplenode", END)


# (START) => chatbot -> samplenode -> (END).

graph = graph_builder.compile()


updated_state = graph.invoke(State({"messages":["hi, Whats todays status..."]}))


print("\n\nUpdated state:", updated_state)



# state = { "messages":["Hey there "]}
# node runs: chatbot(state:["Hey there"]) -> ["Hi, This is a message from chat bot Node "]
# state =  {"messages":["Hey there ", "Hi, This is a message from chat bot Node "]}

