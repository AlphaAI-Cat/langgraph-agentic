from portfolio_convert.agent.linear_graph import calculate_linear_graph, usd_to_inr
from portfolio_convert.models.convert import PortfolioStateInr
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.graph.message import add_messages
from IPython.display import display
from rich.console import Console
console = Console()
def save_graph_visualization(graph):
    png_data = graph.get_graph().draw_mermaid_png()
    with open("graph_visualization.png", "wb") as f:
        f.write(png_data)
    console.print("[green]Graph visualization saved as 'graph_visualization.png'[/green]")
    
def main():
    print("Hello from langgraph-agentic!")
    builder = StateGraph(PortfolioStateInr)
    
    builder.add_node("calculate_linear_graph", calculate_linear_graph)
    builder.add_node("usd_to_inr", usd_to_inr)
    
    
    builder.add_edge(START, "calculate_linear_graph")
    builder.add_edge("calculate_linear_graph", "usd_to_inr")
    builder.add_edge("usd_to_inr", END)
    
    
    graph = builder.compile()
    
    # Save the graph visualization to a PNG file
    save_graph_visualization(graph)

    result = graph.invoke({"amount_usd": 100})
    print(result)   
    
if __name__ == "__main__":
    main()
