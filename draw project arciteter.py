import matplotlib.pyplot as plt
import networkx as nx

# Create a new graph
G = nx.DiGraph()

# Add nodes
G.add_node("Client 1", pos=(-1, 3))
G.add_node("Client 2", pos=(0, 3))
G.add_node("Client 3", pos=(1, 3))
G.add_node("Server", pos=(0, 2))
G.add_node("Database", pos=(1, 2))
G.add_node("Reed-Solomon Encoding", pos=(0, 1))
G.add_node("Servant 1", pos=(-1.5, 0))
G.add_node("Servant 2", pos=(-0.5, 0))
G.add_node("Servant 3", pos=(0.5, 0))
G.add_node("Servant 4", pos=(1.5, 0))

# Add edges
G.add_edge("Client 1", "Server", label="File Upload")
G.add_edge("Client 2", "Server", label="File Upload")
G.add_edge("Client 3", "Server", label="File Upload")
G.add_edge("Server", "Reed-Solomon Encoding", label="Forward File")
G.add_edge("Server", "Database", label="Save File Info")
G.add_edge("Reed-Solomon Encoding", "Servant 1", label="Distribute Chunks")
G.add_edge("Reed-Solomon Encoding", "Servant 2", label="Distribute Chunks")
G.add_edge("Reed-Solomon Encoding", "Servant 3", label="Distribute Chunks")
G.add_edge("Reed-Solomon Encoding", "Servant 4", label="Distribute Chunks")

# Set node colors
node_colors = ["#E1F5FE", "#E1F5FE", "#E1F5FE", "#B3E5FC", "#81D4FA", "#4FC3F7", "#29B6F6", "#03A9F4", "#039BE5", "#039BE5"]

# Set node sizes
node_sizes = [1000 if node.startswith("Client") else 1200 if node in ["Server", "Reed-Solomon Encoding"] else 1000 for node in G.nodes]

# Set edge styles
edge_styles = ["solid" if edge[0].startswith("Client") or edge[0] == "Server" else "dashed" for edge in G.edges]

# Draw the graph
pos = nx.get_node_attributes(G, 'pos')
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)

# Draw edges with different styles
for edge, style in zip(G.edges, edge_styles):
    nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='gray', arrows=True, style=style, width=1.5)

nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold', font_family='Arial')
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'), font_size=14)

# Remove axis
plt.axis('off')

# Add a title
plt.title("Server-Client Architecture with Multiple Clients", fontsize=20, fontweight='bold', fontfamily='Arial')

# Show the diagram
plt.tight_layout()
plt.show()