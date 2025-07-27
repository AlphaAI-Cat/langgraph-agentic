from settings import google_api_key  # You'll need to add this to settings.py
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage
from pydantic import BaseModel

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

class State(BaseModel):
    messages: list[dict] = []

def chatbot(state: State) -> State:
    # Convert dict messages to LangChain message objects
    langchain_messages = []
    for msg in state.messages:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            langchain_messages.append(AIMessage(content=msg["content"]))
    
    # Get response from LLM
    response = llm.invoke(langchain_messages)
    
    # Convert response back to dict format
    response_dict = {
        "role": "assistant",
        "content": response.content
    }
    
    # Update state with new message
    new_messages = state.messages + [response_dict]
    return State(messages=new_messages)

builder = StateGraph(State)

builder.add_node("chatbot_node", chatbot)

builder.add_edge(START, "chatbot_node")
builder.add_edge("chatbot_node", END)

graph = builder.compile()

state = None

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        break
    
    if state is None:
        state = State(messages=[{"role": "user", "content": user_input}])
    else:
        # Add user message to existing state
        new_messages = state.messages + [{"role": "user", "content": user_input}]
        state = State(messages=new_messages)
    
    result = graph.invoke(state)
    print(f"Assistant: {result.messages[-1]['content']}")
    state = result 