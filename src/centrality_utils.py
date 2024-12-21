
import networkx as nx

def calculate_centralities(G, weight='weight'):
    """
    Calculates different centralities for a graph and returns them as a dictionary.
    """
    #centralities = {
    #    'closeness': nx.closeness_centrality(G, distance=weight),
    #    'betweenness': nx.betweenness_centrality(G, weight=weight),
    #    'eigenvector': nx.eigenvector_centrality_numpy(G, weight=weight),
    #    'pagerank': nx.pagerank(G, weight=weight)
    #}

    closeness = nx.closeness_centrality(G, distance=weight)
    betweenness = nx.betweenness_centrality(G, weight=weight)
    eigenvector = nx.eigenvector_centrality_numpy(G, weight=weight)
    pagerank = nx.pagerank(G, weight=weight)

    # Agregar centralidades como atributos al grafo
    nx.set_node_attributes(G, closeness, 'closeness')
    nx.set_node_attributes(G, betweenness, 'betweenness')
    nx.set_node_attributes(G, eigenvector, 'eigenvector')
    nx.set_node_attributes(G, pagerank, 'pagerank')

    # 2. Graficar el grafo por importancia
    centralities = {'Closeness': closeness, 'Betweenness': betweenness, 
                    'Eigenvector': eigenvector, 'PageRank': pagerank}


    return centralities
