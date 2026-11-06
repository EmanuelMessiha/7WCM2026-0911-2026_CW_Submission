# Emanuel Messiha
# 7WCM2026-0911-2026 - Data Structure and Algorithms 2
# Question 2 - MST using Kruskals algorithm.

# NetworkX allows us to create and work with our connected graphs.
import networkx as nx
from networkx import Graph

#Matplotlib allows us to display the origial graphs and their MSTs.
import matplotlib.pyplot as plt
from pathlib import Path


#Below is the exact function signature printed in the assignment.
def MyMinimumSpannigTree(Graph) -> Graph:

    #First we have to check that the graph is connected, since the question does require this
    if Graph.number_of_nodes() == 0 or not nx.is_connected(Graph):
        raise ValueError("The graph must be connected and contain at least one node.")

    #We also need to check that every edge has a weight for Kruskals algorithm to use:
    if any("weight" not in data for _, _, data in Graph.edges(data=True)):
        raise ValueError("Every edge must have a weight.")

    #Below creates an empty MST containing all the original nodes but no edges.
    mst = nx.Graph()
    mst.add_nodes_from(Graph.nodes(data=True))

    # I have choosen to use Kruskals algorithm.
    # Kruskals algorithm starts by sorting the edges from the lowest weight to the highest.
    sorted_edges = sorted(Graph.edges(data=True), key=lambda edge: edge[2]["weight"])
    total_weight = 0

    print("Edges sorted from the smallest weight to the largest:")
    print([(u, v, data["weight"]) for u, v, data in sorted_edges])
    print()

    #We now have to check each edge one by one to build our MST graph.
    for step, (u, v, data) in enumerate(sorted_edges, start=1):
        weight = data["weight"]
        print(f"Step {step}: Checking edge {u} - {v} with weight {weight}")


        #If a path already exists between the two nodes in our MST, adding an edge would create a cycle so we dont add it.
        if nx.has_path(mst, u, v):
            print("Rejected, adding this edge would create a cycle")
        else:
            #Otherwise, we add the edge and update the total weight of the MST.
            mst.add_edge(u, v, weight=weight)
            total_weight += weight
            print(f"Added edge {u} - {v} has been added to the MST.")
            print(f"Current MST edges: {list(mst.edges(data='weight'))}")
            print(f"Current total weight: {total_weight}")


        #A spanning tree has exactly the number of nodes minus one edge.
        #Therefore, we must stop once all the nodes have been connected without cycles
        if mst.number_of_edges() == Graph.number_of_nodes() - 1:
            print("All nodes are now connected. MST completed.")
            break
        print()

    print(f"Final MST edges: {list(mst.edges(data='weight'))}")
    print(f"Final MST total weight: {total_weight}")
    return mst

# This second name matches the spelling used in the assignment's explanation.
def MyMinimumSpanningTree(Graph) -> Graph:
    return MyMinimumSpannigTree(Graph)


# The function below allows us to create our three different weighted graphs.
def create_graph(edges):
    graph = nx.Graph()
    graph.add_weighted_edges_from(edges)
    return graph


# This function uses Matplotlib to draw the nodes, edges and their weights.
# The same positions are used for each original graph and its MST for easy comparison.
def draw_graph(graph, positions, title, filename, ax=None):
    own_figure = ax is None
    if own_figure:
        figure, ax = plt.subplots(figsize=(9, 7))

    nx.draw_networkx_nodes(graph, positions, ax=ax, node_color="lightblue", node_size=1250,
                           edgecolors="black", linewidths=1.1)
    nx.draw_networkx_edges(graph, positions, ax=ax, edge_color="dimgray", width=2.1)
    nx.draw_networkx_labels(graph, positions, ax=ax, font_size=12, font_weight="bold")

    # These labels display the weight of each edge on our graph.
    edge_weights = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_weights, ax=ax,
                                 font_size=10, bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85})

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_axis_off()
    ax.margins(0.2)

    # The images are saved so we can insert them directly into our Word report.
    if own_figure:
        figure.tight_layout()
        figure.savefig(filename, dpi=220, bbox_inches="tight")
        plt.close(figure)


if __name__ == "__main__":

    # We create a folder for the six graph images and a combined image.
    output_folder = Path("question2_figures")
    output_folder.mkdir(exist_ok=True)

    # Graph 1 is our main example, containing exactly 6 nodes and 11 edges.
    graph1 = create_graph([
        ("A", "B", 1), ("B", "C", 2), ("A", "C", 3),
        ("C", "D", 4), ("D", "E", 5), ("B", "D", 6),
        ("E", "F", 7), ("C", "E", 8), ("A", "D", 9),
        ("B", "E", 10), ("D", "F", 11)
    ])

    # Graph 2 is different from the first, with 5 nodes and 8 edges.
    graph2 = create_graph([
        ("P", "Q", 2), ("P", "R", 3), ("Q", "R", 4),
        ("R", "S", 5), ("S", "T", 7), ("P", "S", 8),
        ("Q", "T", 9), ("R", "T", 10)
    ])

    # Graph 3 is also different, containing 7 nodes and 10 edges.
    graph3 = create_graph([
        ("G", "H", 1), ("I", "J", 2), ("G", "I", 3),
        ("H", "I", 4), ("I", "K", 5), ("K", "L", 6),
        ("J", "K", 7), ("H", "J", 8), ("L", "M", 9),
        ("G", "M", 10)
    ])

    graphs = [graph1, graph2, graph3]
    figure, axes = plt.subplots(3, 2, figsize=(15, 19))

    for number, graph in enumerate(graphs, start=1):
        # We check each graph meets the required number of nodes and edges.
        required_nodes = 6 if number == 1 else 5
        required_edges = 11 if number == 1 else 8
        assert nx.is_connected(graph)
        assert graph.number_of_nodes() >= required_nodes
        assert graph.number_of_edges() >= required_edges

        print("=" * 65)
        print(f"GRAPH {number}: {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
        print("Kruskal's Algorithm - Creating the MST step by step")
        print("=" * 65)

        # We use the function to build the MST and print each step to the console.
        mst = MyMinimumSpanningTree(graph)
        assert nx.is_tree(mst)
        assert mst.number_of_edges() == graph.number_of_nodes() - 1

        # This ensures that each original graph and its MST use the same layout.
        positions = nx.spring_layout(graph, seed=(93 if number == 1 else number * 10), weight=None)
        weight = sum(data["weight"] for _, _, data in mst.edges(data=True))

        original_title = f"Graph {number} - Original ({graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges)"
        mst_title = f"Graph {number} - MST (total weight = {weight})"

        draw_graph(graph, positions, original_title,
                   output_folder / f"graph{number}_original.png")
        draw_graph(mst, positions, mst_title,
                   output_folder / f"graph{number}_mst.png")

        draw_graph(graph, positions, original_title, None, axes[number - 1, 0])
        draw_graph(mst, positions, mst_title, None, axes[number - 1, 1])
        print()

    # Lastly, we save and display all six Matplotlib diagrams together.
    figure.tight_layout(pad=3.0)
    figure.savefig(output_folder / "all_three_graphs_and_msts.png", dpi=180, bbox_inches="tight")
    plt.show()

