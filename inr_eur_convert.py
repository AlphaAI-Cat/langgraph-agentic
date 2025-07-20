from portfolio_convert.agent.linear_graph import calculate_linear_graph_general, calculate_usd_to_eur, calculate_usd_to_inr, choose_path_currency
from portfolio_convert.models.convert import PortfolioStateGeneral, Currency
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.graph.message import add_messages
from IPython.display import display
from rich.console import Console
console = Console()
def save_graph_visualization(graph):
    png_data = graph.get_graph().draw_mermaid_png()
    with open("graph_visualization_2d.png", "wb") as f:
        f.write(png_data)
    console.print("[blue]Graph visualization saved as 'graph_visualization_2d.png'[/blue]")
    
def main():
    print("Hello from langgraph-agentic!")
    builder = StateGraph(PortfolioStateGeneral)
    
    builder.add_node("calculate_linear_graph", calculate_linear_graph_general   )
    builder.add_node("calculate_usd_to_inr", calculate_usd_to_inr)
    builder.add_node("calculate_usd_to_eur", calculate_usd_to_eur)
    
    builder.add_edge(START, "calculate_linear_graph")
    
    builder.add_conditional_edges(
        "calculate_linear_graph",
        choose_path_currency,
        {
            "INR": "calculate_usd_to_inr",
            "EUR": "calculate_usd_to_eur",
        }
    )
    # builder.add_edge("calculate_usd_to_inr", END)
    # builder.add_edge("calculate_usd_to_eur", END)
    builder.add_edge(["calculate_usd_to_inr", "calculate_usd_to_eur"], END)
    
    
    graph = builder.compile()
    
    # Save the graph visualization to a PNG file
    save_graph_visualization(graph)

    result = graph.invoke({"amount_usd": 100, "target_currency": "EUR"})
    print(result)   
    
if __name__ == "__main__":
    main()
