import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

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