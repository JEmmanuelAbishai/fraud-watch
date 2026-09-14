import networkx as nx
import pandas as pd

def build_graph_from_transactions(df: pd.DataFrame) -> nx.MultiDiGraph:
    g = nx.MultiDiGraph()

    for _, row in df.iterrows():
        tx_id = f"tx_{row['transaction_id']}"
        acct_id = f"acct_{row['account_id']}"
        device_id = f"device_{row['device_id']}" if pd.notna(row.get('device_id')) else None
        email_domain = f"email_{row['email_domain']}" if pd.notna(row.get('email_domain')) else None

        g.add_node(tx_id, type="transaction", amount=float(row["amount"]),
                   is_fraud=bool(row.get("is_fraud", False)))
        g.add_node(acct_id, type="account")
        g.add_edge(tx_id, acct_id, relation="BELONGS_TO ")

        if device_id:
            g.add_node(device_id, type="device")
            g.add_edge(tx_id, device_id, relation="USED_DEVICE")
            g.add_edge(acct_id, device_id, relation="SEEN_ON")

        if email_domain:
            g.add_node(email_domain, type="email_domain")
            g.add_edge(tx_id, email_domain, relation="USED_EMAIL_DOMAIN")
            g.add_edge(acct_id, email_domain, relation="REGISTERED_WITH")

    return g

def k_hop_subgraph(g: nx.MultiDiGraph, center_node: str, k: int) -> nx.MultiDiGraph:
    undirected = g.to_undirected(as_view=True)
    nodes = set([center_node])
    frontier = set([center_node])
    for _ in range(k):
        next_frontier = set()
        for n in frontier:
            next_frontier.update(undirected.neighbors(n))
        nodes.update(next_frontier)
        frontier = next_frontier

    return g.subgraph(nodes).copy()

def graph_stats(g: nx.MultiDiGraph) -> dict:
    type_counts: dict[str, int] = {}
    for _, data in g.nodes(data=True):
        t = data.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
    return {
        "num_nodes": g.number_of_nodes(),
        "num_edges": g.number_of_edges(),
        "nodes_by_type": type_counts,
    }