from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import  Optional, Literal   
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
import os 


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


class State(TypedDict):
    user_query:str
    llm_output:Optional[str]
    is_good:Optional[bool]


def chatbot(state:State):
    response = client.chat.completions.create(
    model="gemini-3-flash-preview",
        messages=[
            {"role":"user", "content":state.get("user_query")},
        ]
    )
    state['llm_output'] = response.choices[0].message.content
    return state


def evaluate_state(state: State) -> Literal["chatbot_gemini", "endnode"]:
    """Use AI to evaluate response quality with detailed criteria"""
    
    llm_output = state.get('llm_output', '')
    user_query = state.get('user_query', '')
    
    evaluation_prompt = f"""
You are an expert AI response evaluator. Evaluate the following response based on these criteria:
1. Accuracy: Does it correctly answer the question?
2. Completeness: Is the answer complete and thorough?
3. Clarity: Is it easy to understand?
4. Relevance: Does it stay on topic?

User Question: {user_query}

AI Response: {llm_output}

Provide your evaluation in this EXACT format:
VERDICT: [PASS or FAIL]
REASON: [Brief explanation]

Your evaluation:"""
    
    evaluation_response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role": "user", "content": evaluation_prompt}
        ],
        temperature=0
    )
    
    evaluation = evaluation_response.choices[0].message.content.strip()
    
    print(f"\n{'='*60}")
    print("🔍 AI EVALUATION:")
    print(f"{'='*60}")
    print(evaluation)
    print(f"{'='*60}\n")
    
    # Check if PASS appears in the verdict
    if "PASS" in evaluation.upper():
        print("✅ Response approved - routing to END")
        return "endnode"
    else:
        print("❌ Response needs improvement - routing to enhanced chatbot")
        return "chatbot_gemini" 



def chatbot_gemini (state:State):
    response = client.chat.completions.create(
    model="gemini-3-flash-preview",
        messages=[
            {"role":"user", "content":state.get("user_query")},
        ]
    )
    state['llm_output'] = response.choices[0].message.content
    return state


def endnode(state:State):
    return state



graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_state)
graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)


graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query":"Hey, What is 2+2?"}))

print(updated_state)




# from dotenv import load_dotenv
# from typing_extensions import TypedDict, Annotated,Literal
# from typing import Optional 
# from langgraph.graph import StateGraph, START, END

# from openai import OpenAI
# import os


# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("GEMINI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )


# class State(TypedDict):
#     user_query: str
#     llm_output: Optional[str]
#     is_good:Optional[bool]


# def chatbot(state:State):
#     print("Chatbot node: ", state   )
#     response = client.chat.completions.create(
#         model="gpt-4.1-mini",
#         messages=[
#             {"role": "system","content":SYSTEM_PROMPT},
#             { "role":"user","content":user_query}
#         ],
#     )
#     state['llm_output'] = response.choices[0].message.content
#     return state


# def chatbot_gemini(state:State):
#     response = client.chat.completions.create(
#         model="gpt-4.1-mini",
#         messages=[
#             {"role": "system","content":SYSTEM_PROMPT},
#             { "role":"user","content":user_query}
#         ],
#     )
#     state['llm_output'] = response.choices[0].message.content
#     return state

# def evaluate_response(state:State)-> Literal["chatbot_gemini", "endnode" ]:
#     if True:
#         return "endnode"
#     return "chatbot_gemini"

# def endnode(state:State):
#     return state

# # register a nodes 

# graph_builder = StateGraph(State)

# graph_builder.add_node("chatbot", chatbot)
# graph_builder.add_node("chatbot_gemini", chatbot_gemini)
# graph_builder.add_node("endnode", endnode)

# graph_builder.add_edge(START, "chatbot")
# graph_builder.add_conditional_edge("chatbot", evaluate_response )
# graph_builder.add_edge("endnode", END)

# graph = graph_builder.compile()

# updated_state = graph.invoke(State({"messages":["hi, Whats todays status..."]}))

