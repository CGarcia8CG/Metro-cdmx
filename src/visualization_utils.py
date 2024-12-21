
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

def plot_centrality(G, centrality, title):
    """
    Plots the graph with nodes sized and colored based on centrality values.
    """
    pos = {node: (data['geometry'].x, data['geometry'].y) 
           for node, data in G.nodes(data=True)}
    node_colors = [centrality[node] for node in G.nodes()]
    node_sizes = [centrality[node] * 1000 for node in G.nodes()]

    norm = Normalize(vmin=min(node_colors), vmax=max(node_colors))
    sm = ScalarMappable(cmap=plt.cm.viridis, norm=norm)
    sm.set_array([])

    plt.figure(figsize=(20, 12))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, cmap=plt.cm.viridis,
                           node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_color="black", font_size=8)
    plt.colorbar(sm, label="Centrality Score")
    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.show()
