
import pickle

def save_graph(graph, filepath):
    """
    Saves a NetworkX graph to a pickle file.
    """
    with open(filepath, "wb") as f:
        pickle.dump(graph, f)

def load_graph(filepath):
    """
    Loads a NetworkX graph from a pickle file.
    """
    with open(filepath, "rb") as f:
        return pickle.load(f)
