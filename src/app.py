import geopandas as gpd
import folium
from streamlit_folium import st_folium
import networkx as nx
from config import Config
from io_utils import load_graph
import matplotlib.colors as mcolors
import pandas as pd
import streamlit as st
import os

# Cargar configuración
config = Config()

# Cargar el grafo
#metro_graph = load_graph(config.output_data_dir+'\metro_graph.pkl')
metro_graph = load_graph(os.path.join(config.output_data_dir,'metro_graph.pkl'))

#print(metro_graph.nodes['pantitlan'])

# --- SIDEBAR INTERACTIVO ---
with st.sidebar:
    # Foto e Información Personal
    st.image("input_data/cropped_carlos.png", width=150)  # Cambia por tu foto
    st.markdown("## About Me:")
    st.write("""
    **Name:** Carlos David García Hernández  
    **Rol:** Data Scientist @ Tec de Monterrey
             Teacher of regional economic analysis @ Universidad Nacional Autónoma de México
             
    **Contact:** [carlos.garcia.economist@gmail.com](mailto:carlos.garcia.economist@gmail.com)  
    """)

    # Enlace a LinkedIn
    st.markdown("### Connect with me:")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/cgarcia8cg/)")  # Cambia tu URL
    st.markdown("[GitHub](https://cgarcia8cg.github.io/)")  # Cambia tu URL

    st.write("---")

    # Información sobre el Proyecto
    st.markdown("## About the proyect")
    st.write("""
    Este proyecto analiza la red del metro de la CDMX utilizando 
    métricas de **centralidad** para identificar estaciones clave.  
    Se basa en bibliotecas como **GeoPandas**, **NetworkX** y **Folium** 
    para visualizaciones geoespaciales interactivas.
    """)

    st.write("**Objectives:**")
    st.markdown("- Identificar estaciones críticas por diversas métricas de centralidad.")
    st.markdown("- Visualizar patrones de movilidad.")
    st.markdown("- Reflexionar sobre políticas públicas para mejorar el sistema de movilidad.")

    st.write("---")
    st.write("Explora los resultados en el mapa interactivo y analiza las métricas seleccionadas.")

# Título de la App
st.title("Visualización del Metro CDMX - Centralidades")

# Selector para elegir la centralidad
centrality_option = st.selectbox(
    "Select you measure of centrality for visualization:",
    options=["closeness", "betweenness", "eigenvector", "pagerank"]
)

# Función para obtener información de nodos
def get_node_info(graph, centrality):
    node_data = []
    for node, data in graph.nodes(data=True):
        # Obtener el valor de centralidad
        centrality_value = data.get(centrality, 0)

        # Multiplicar por 50 solo para PageRank
        if centrality == "pagerank":
            centrality_value *= 50

        node_data.append({
            "name": data.get("estacion", "Desconocido"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "centrality": centrality_value,
            "afluencia": data.get("afluencia", 0),
            "tipo": data.get("TIPO", "Desconocido"),
            "linea": data.get("LINEA", "Desconocida"),
        })
    return node_data


# Obtener datos de los nodos
nodes_info = get_node_info(metro_graph, centrality_option)

# Crear mapa centrado en CDMX
m = folium.Map(location=[19.4326, -99.1332], zoom_start=11)

# Crear escala de colores (semaforo)
values = [node["centrality"] for node in nodes_info]
norm = mcolors.Normalize(vmin=min(values), vmax=max(values))
cmap = mcolors.LinearSegmentedColormap.from_list("semaforo", ["red", "yellow", "green"])

# Ajustar el tamaño de los nodos proporcionalmente
min_size = 4  # Tamaño mínimo
max_size = 20  # Tamaño máximo
scaled_sizes = [
    min_size + ((node["centrality"] - min(values)) / (max(values) - min(values))) * (max_size - min_size)
    for node in nodes_info
]

# Añadir nodos al mapa
for i, node in enumerate(nodes_info):
    color = mcolors.to_hex(cmap(norm(node["centrality"])))
    folium.CircleMarker(
        location=[node["latitude"], node["longitude"]],
        radius=scaled_sizes[i],  # Usar tamaño escalado
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=(
            f"<b>{node['name']}</b><br>"
            f"Línea: {node['linea']}<br>"
            f"Tipo: {node['tipo']}<br>"
            f"Afluencia: {node['afluencia']}<br>"
            f"Centralidad ({centrality_option}): {node['centrality']:.4f}"
        ),
    ).add_to(m)

# Añadir conexiones entre nodos (aristas)
for u, v, data in metro_graph.edges(data=True):
    coords = [
        [metro_graph.nodes[u]["latitude"], metro_graph.nodes[u]["longitude"]],
        [metro_graph.nodes[v]["latitude"], metro_graph.nodes[v]["longitude"]]
    ]
    folium.PolyLine(coords, color="gray", weight=3, opacity=0.7).add_to(m)

# Mostrar el mapa
st_folium(m, width=700, height=600)

# ---- Tablas con las estaciones ----
# Crear DataFrame con la información de centralidad
df = pd.DataFrame(nodes_info)

# Ordenar por centralidad
df_sorted = df.sort_values(by="centrality", ascending=False)

# Dividir en dos tablas
top_stations = df_sorted.head(5)[["name", "centrality"]]  # Mejores 10 estaciones
bottom_stations = df_sorted.tail(5)[["name", "centrality"]]  # Peores 10 estaciones

# Mostrar tablas en dos columnas
col1, col2 = st.columns(2)

# Tabla de mayores valores
with col1:
    st.write(f"### Top 5 Stations -<br> {centrality_option.capitalize()}", unsafe_allow_html=True)
    st.table(top_stations)

# Tabla de menores valores
with col2:
    st.write(f"### Bottom 5 Stations -<br> {centrality_option.capitalize()}", unsafe_allow_html=True)
    st.table(bottom_stations)