import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
from shapely.geometry import LineString
import re
from config import Config

config = Config()

# Función para eliminar acentos y convertir a minúsculas
def remove_accents(text):
    # Mapeo de caracteres acentuados a sus equivalentes sin acentos
    accents_mapping = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',
        'ñ': 'n', 'Ñ': 'n'
    }
    # Usar re.sub para reemplazar caracteres con acentos
    for accented_char, plain_char in accents_mapping.items():
        text = re.sub(accented_char, plain_char, text)
    # Convertir a minúsculas
    return text.lower()


def open_df():
    #vardf = '../input_data/data metro cdmx 2022-2024-12-04.csv'
    vardf = config.input_data_dir_csv

    df = pd.read_csv(vardf)

    # Aplicar la función a la columna
    df['estacion'] = df['estacion'].apply(remove_accents)
    df_agg = df.groupby('estacion').agg({'afluencia':'count'})
    df_agg.reset_index(inplace=True)

    return (df_agg)

def open_gdf():
    #vargdf = '../input_data/metro_shp/stcmetro_shp/STC_Metro_estaciones_utm14n.shp'
    vargdf = config.input_data_dir_geop

    gdf_puntos = gpd.read_file(vargdf,crs='EPSG:4326')

    # Crear nuevas columnas para latitud y longitud
    gdf_puntos['longitude'] = gdf_puntos.geometry.x  # Longitud (coordenada X)
    gdf_puntos['latitude'] = gdf_puntos.geometry.y  # Latitud (coordenada Y)
    # Aplicar la función a la columna
    gdf_puntos['NOMBRE'] = gdf_puntos['NOMBRE'].apply(remove_accents)

    return (gdf_puntos)

def join1(df,gdf):
    # Join df_agg y gdf_puntos
    join_gdf = gdf.merge(df, left_on = 'NOMBRE', right_on = 'estacion', how ='left')

    return(join_gdf)


def open_gdf_lines():
    #vargdf_l = '../input_data/metro_shp/stcmetro_shp/STC_Metro_lineas_utm14n.shp'
    vargdf_l = config.input_data_dir_geol
    gdf_lineas = gpd.read_file(vargdf_l)
    gdf_lineas = gdf_lineas.to_crs(config.default_crs) #config.default_crs 'EPSG:4326'

    return(gdf_lineas)

def lineas_change(gdf_line):
    gdf_line["LINEA"] = gdf_line["LINEA"].replace({'1':'01', '2':'02','3':'03',
                                                   '4':'04', '5':'05','6':'06',
                                                   '7':'07', '8':'08','9':'09'})
    
    return(gdf_line)


def connect_metro_stations(stations_gdf, lines_gdf, line_col, station_id_col):
    """
    Connects metro stations based on their corresponding line and calculates 
    average attributes for each connection.
    
    Parameters:
        stations_gdf (GeoDataFrame): GeoDataFrame containing metro stations with geometry,
                                     latitude, longitude, and attributes like passenger flow.
        lines_gdf (GeoDataFrame): GeoDataFrame containing metro lines as geometries.
        line_col (str): Column name in both DataFrames that associates stations with lines.
        station_id_col (str): Unique identifier for each station.
        
    Returns:
        GeoDataFrame: A new GeoDataFrame representing the connections between stations
                      with calculated average attributes.
    """
    connections = []

    for line_id in lines_gdf[line_col].unique():
        # Filtrar estaciones y líneas según el identificador de línea
        line_stations = stations_gdf[stations_gdf[line_col] == line_id].sort_values(by=station_id_col)
        line_geometry = lines_gdf[lines_gdf[line_col] == line_id].geometry.iloc[0]

        # Conectar estaciones secuencialmente
        for i in range(len(line_stations) - 1):
            station_a = line_stations.iloc[i]
            station_b = line_stations.iloc[i + 1]

            # Calcular línea entre estaciones
            segment_geom = LineString([station_a.geometry, station_b.geometry])

            # Calcular promedio de atributos
            avg_passenger_flow = (station_a['afluencia'] + station_b['afluencia']) / 2

            # Crear registro de conexión
            connections.append({
                'line': line_id,
                'from_station': station_a[station_id_col],
                'to_station': station_b[station_id_col],
                'avg_afluencia': avg_passenger_flow,
                'geometry': segment_geom
            })

    # Crear un GeoDataFrame con las conexiones
    connections_gdf = gpd.GeoDataFrame(connections, crs=stations_gdf.crs)

    return connections_gdf

#connections_gdf = connect_metro_stations(
    #stations_gdf=join_gdf,
    #lines_gdf=gdf_lineas,
    #line_col='LINEA',
    #station_id_col='CVE_EST'
#)

### Crear un diccionario para trasladar from_station y to_station a nombre de estaciones
def create_station_dict(gdf, id_col, name_col):
    """
    Creates a dictionary mapping station IDs to station names from a GeoDataFrame.

    Parameters:
        gdf (GeoDataFrame): GeoDataFrame containing station data.
        id_col (str): Column name with unique station IDs.
        name_col (str): Column name with station names.

    Returns:
        dict: Dictionary mapping station IDs to station names.
    """
    return gdf.set_index(id_col)[name_col].to_dict()

#station_dict = create_station_dict(join_gdf, id_col='CVE_EST', name_col='NOMBRE')

def enhance_name(connections_gdf,station_dict):
    connections_gdf['from_name'] = connections_gdf['from_station'].map(station_dict).fillna("Desconocido")
    connections_gdf['to_name'] = connections_gdf['to_station'].map(station_dict).fillna("Desconocido")

    return connections_gdf
