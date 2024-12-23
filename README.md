# **Análisis de Centralidades en el Metro de CDMX** 🚇

## **Descripción del Proyecto**
Este proyecto analiza la red del **Metro de la Ciudad de México** utilizando métricas de **centralidad** para identificar estaciones clave y patrones de movilidad. Utiliza herramientas avanzadas como **GeoPandas**, **NetworkX**, **Folium** y **Streamlit** para generar visualizaciones interactivas y estadísticas.

## **Objetivos del Proyecto**
1. **Identificar Estaciones Críticas**: Localizar las estaciones más importantes en función de métricas de centralidad como **closeness**, **betweenness**, **eigenvector** y **PageRank**.
2. **Visualizar la Red del Metro**: Mostrar un mapa interactivo con escalas de colores tipo semáforo y tamaños proporcionales a los valores de centralidad (distintas formas de calcular la centralidad).
3. **Reflexionar sobre políticas públicas para mejorar el sistema de movilidad.**: Analizar posibles ubicaciones para nuevas estaciones basadas en la estructura de la red existente.

---

## **Estructura del Proyecto**
/ (root)
├── packages.txt                  # Dependencias del sistema operativo
├── src/                          # Código fuente
│   ├── init.py
│   ├── config.py                 # Configuración del proyecto
│   ├── io_utils.py               # Manejo de datos y gráficos
│   ├── preprocessing.py          # Preprocesamiento de datos
│   ├── graph_utils.py            # Funciones para creación de grafos
│   ├── app.py                    # Aplicación principal de Streamlit
│   ├── requirements.txt          # Dependencias de Python
│   ├── runner.py                 # Archivo (pipe) para construir la red
│   ├── test_network.py           # Archivo de prueba de la red
├── input_data/                   # Datos de entrada
│   ├── stations.geojson          # Estaciones del metro
│   ├── metro_lines.geojson       # Líneas del metro
│   ├── cropped_photo.jpg         # Foto del perfil
├── output_data/                  # Datos generados como resultados
├── README.md                     # Documentación general
├── notebooks/                    # Notebooks para análisis exploratorio
├── .env/                         # env pydantic
---

## **Requisitos del Proyecto**
**Dependencias de Python (requirements.txt)**

---
### Uso de la Aplicación

1. Selector de Centralidades: Cambia entre diferentes métricas de centralidad para analizar los nodos.

2. Mapas Interactivos: Visualiza estaciones con colores tipo semáforo y tamaños proporcionales a su relevancia.

3. Tablas de Resultados: Consulta las 5 estaciones con mayor y menor centralidad.


## Contacto

Nombre: Carlos David García Hernández

Correo: [carlos.garcia.economist@gmail.com](mailto:carlos.garcia.economist@gmail.com)

LinkedIn: [LinkedIn](https://www.linkedin.com/in/cgarcia8cg/)

GitHub: [GitHub](https://cgarcia8cg.github.io/)
