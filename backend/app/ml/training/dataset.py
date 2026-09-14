# Converts NetworkX fraud-graph into PyTorchG Data object 

import torch
import networkx as nx
from torch_geometric.data import Data

NODE_TYPES = ["transaction", "account", "device", "email_domain"]

def networkx_to_pyg(g: nx.MultiDiGraph) -> tuple[Data, list[str]]:
    node_ids = list(g.nodes())
    node_index = {node_id: i for i, node_id in enumerate(node_ids)}

    features = []
    labels = []
    for node_id in node_ids:
        data = g.nodes[node_id]
        node_type = data.get("type", "unknown")
        one_hot = [1.0 if node_type == t else 0.0 for t in NODE_TYPES]
        amount = float(data.get("amount", 0.0))
        features.append(one_hot + [amount])
        labels.append(1 if data.get("is_fraud") else 0)

    edge_index = [[], []]
    for source, target in g.edges():
        edge_index[0].append(node_index[source])
        edge_index[1].append(node_index[target])
        edge_index[0].append(node_index[target])
        edge_index[1].append(node_index[source])

    x = torch.tensor(features, dtype = torch.float)
    y = torch.tensor(labels, dtype = torch.long)
    edge_index_tensor = torch.tensor(edge_index, dtype = torch.long)

    return Data(x = x, edge_index = edge_index_tensor, y=y), node_ids