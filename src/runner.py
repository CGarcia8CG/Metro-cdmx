from centrality_utils import calculate_centralities
from config import Config
from graph_utils import build_metro_graph
from io_utils import save_graph
from preprocessing import remove_accents, open_df, open_gdf, join1, open_gdf_lines, lineas_change,connect_metro_stations, create_station_dict,enhance_name
import geopandas as gpd

config = Config()

df_agg = open_df()
gdf_puntos = open_gdf()
gdf_lineas = open_gdf_lines()
join_gdf = join1(df_agg,gdf_puntos)
gdf_lineas = lineas_change(gdf_lineas)

connections_gdf = connect_metro_stations(join_gdf,
                                         gdf_lineas,
                                         'LINEA',
                                         'CVE_EST')

station_dict = create_station_dict(join_gdf, id_col='CVE_EST', name_col='NOMBRE')
connections_gdf = enhance_name(connections_gdf,station_dict)

metro_graph = build_metro_graph(
    stations_gdf=join_gdf,
    connections_gdf=connections_gdf,
    station_id_col='NOMBRE',
    afluencia_col='afluencia'
)

calculate_centralities(metro_graph, weight='afluencia')

save_graph(metro_graph, config.output_data_dir+'\metro_graph.pkl')
print('Guardo el pkl')

#print(connections_gdf.head())
#print(station_dict)
# Imprimir un resumen del grafo

print(f"Nodos: {metro_graph.number_of_nodes()}, Aristas: {metro_graph.number_of_edges()}")
print('Funciona correcto')
