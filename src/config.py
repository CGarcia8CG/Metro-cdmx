from pydantic import Field, ValidationError#, validator
from pydantic_settings import BaseSettings
import re

class Config(BaseSettings):
    # Rutas de entrada/salida
    input_data_dir_csv: str = Field('input_data\data metro cdmx 2022-2024-12-04.csv', description='Directory where input data is stored')
    input_data_dir_geop: str = Field('input_data\metro_shp\stcmetro_shp\STC_Metro_estaciones_utm14n.shp', description='Directory where input geo data is stored')
    input_data_dir_geol: str = Field('input_data\metro_shp\stcmetro_shp\STC_Metro_lineas_utm14n.shp', description='Directory where input geo data is stored')
    output_data_dir: str = Field("output_data", description="Directory where output data is stored")

    # Columnas requeridas
    #station_id_col: str = Field("station_id", description="Column name for station IDs")
    #station_name_col: str = Field("station_name", description="Column name for station names")
    #afluencia_col: str = Field("afluencia", description="Column name for passenger flow")
    #from_station_col: str = Field("from_station", description="Column name for connection start")
    #to_station_col: str = Field("to_station", description="Column name for connection end")
    #avg_afluencia_col: str = Field("avg_afluencia", description="Column name for average passenger flow")

    #CRS
    default_crs: str = Field("EPSG:4326", description="Default CRS for geospatial data")

    #@validator("default_crs")
    #def validate_epsg(cls, value):
    #    if not re.match(r"^EPSG:\d+$", value):
    #        raise ValueError(f"'{value}' is not a valid EPSG code. It must follow the format 'EPSG:<number>'.")
    #    return value

    class Config:
        env_file = ".env"  # Allows overriding via environment variables