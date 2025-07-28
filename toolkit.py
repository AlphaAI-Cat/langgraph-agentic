from settings import open_api_key

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from langchain_core.tools import tool
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
llm = ChatOpenAI(model="gpt-4o-mini", api_key=open_api_key)
from random import randint
from typing import Annotated



@tool
def get_stock_price(symbol: str) -> int:
    """Get the current stock price for a given symbol."""
    # possible_prices = {
    #     symbol:randint(100, 1000)
    # }
    return 100

# @tool
# def get_stock_price_history(symbol: str) -> str:
#     """Get the price history for a given stock symbol over the last 10 periods."""
#     price_history = {
#         symbol: [randint(100, 1000) for _ in range(10)]
#     }
#     return price_history[symbol]
tools= [get_stock_price]
# tools = [get_stock_price, get_stock_price_history]

class State(BaseModel):
    messages: Annotated[list, add_messages]
    
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    """Process user messages and generate responses using the LLM with tools."""
    response = llm_with_tools.invoke(state.messages)
    return {"messages": [AIMessage(content=response.content)]}

builder = StateGraph(State)

builder.add_node("chatbot_node", chatbot)
builder.add_node("tools", ToolNode(tools)) 

builder.add_edge(START, "chatbot_node")
builder.add_conditional_edges("chatbot_node",tools_condition)
builder.add_edge("chatbot_node", END)

graph = builder.compile()



# def save_graph_visualization(graph):
#     png_data = graph.get_graph().draw_mermaid_png()
#     with open("graph_visualization_toolkit.png", "wb") as f:
#         f.write(png_data)
#     print("Graph visualization saved as 'graph_visualization_toolkit.png'")

# # Save the graph visualization to a PNG file
# save_graph_visualization(graph)

result = graph.invoke({"messages": [{"role": "user", "content": "What is the price of AAPL stock?"}]})
print(result['messages'][-1].content)