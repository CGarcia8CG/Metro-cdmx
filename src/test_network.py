from io_utils import load_graph
from config import Config

config = Config()
metro_graph = load_graph(config.output_data_dir+'\metro_graph.pkl')

print(metro_graph.nodes['pantitlan'])
print(metro_graph.edges('pantitlan', 'zaragoza'))