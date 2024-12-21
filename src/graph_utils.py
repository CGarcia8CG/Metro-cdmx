
import networkx as nx

def build_metro_graph(stations_gdf, connections_gdf, station_id_col, afluencia_col):
    """
    Constructs a NetworkX graph from GeoDataFrames of stations and their connections.
    """
    G = nx.Graph()

    # Add nodes
    for _, station in stations_gdf.iterrows():
        G.add_node(
            station[station_id_col],
            geometry=station.geometry,
            afluencia=station[afluencia_col],
            **station.drop([station_id_col, 'geometry', afluencia_col]).to_dict()
        )

    # Add edges
    for _, connection in connections_gdf.iterrows():
        G.add_edge(
            connection['from_name'],
            connection['to_name'],
            weight=connection['avg_afluencia'],
            geometry=connection.geometry,
            line=connection['line']
        )
    
    return G


# Crear el grafo a partir de las estaciones y conexiones
#metro_graph = create_networkx_graph_from_connections(
    #stations_gdf=join_gdf,
    #connections_gdf=connections_gdf,
    #station_id_col='NOMBRE',
    #afluencia_col='afluencia'
#)

# Imprimir un resumen del grafo
#print(f"Nodos: {metro_graph.number_of_nodes()}, Aristas: {metro_graph.number_of_edges()}")

# Ver las propiedades de un nodo
#node_data = list(metro_graph.nodes(data=True))
#print("Ejemplo de nodo:", node_data[0])

# Ver las propiedades de una arista
#edge_data = list(metro_graph.edges(data=True))
#print("Ejemplo de arista:", edge_data[0])