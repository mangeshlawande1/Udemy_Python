from dotenv import load_dotenv
from typing_extensions import TypedDict, Annotated,Literal
from typing import Optional 
from langchain.graph import Stategraph, START, END

from openai import OpenAI


load_dotenv()

client = OpenAI()


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good:Optional[bool]


def chatbot(state:State):
    print("Chatbot node: ", state   )
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system","content":SYSTEM_PROMPT},
            { "role":"user","content":user_query}
        ],
    )
    state['llm_output'] = response.choices[0].message.content
    return state


def chatbot_gemini(state:State):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system","content":SYSTEM_PROMPT},
            { "role":"user","content":user_query}
        ],
    )
    state['llm_output'] = response.choices[0].message.content
    return state

def evaluate_response(state:State)-> Literal["chatbot_gemini", "endnode" ]:
    if True:
        return "endnode"
    return "chatbot_gemini"

def endnode(state:State):
    return state

# register a nodes 

graph_builder = Stategraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edge("chatbot", evaluate_response )
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages":["hi, Whats todays status..."]}))



