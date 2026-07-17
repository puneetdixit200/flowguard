'''convert batch of flows into graph structure that pytorch geometric can read,
Nodes = unique IP addresses. Edges = flows between them.
Each node gets aggregated features (total flows, total bytes, unique peers,
scan-like ratio) — this is what lets the GNN "see" a host's overall behavior,
not just one connection at a time'''

import networkx as nx
import torch
from torch_geometric.data import Data
from collections import defaultdict

def build_ip_graph(flows:list [dict]) -> nx.DiGraph:
    '''build drirected graph from a list of flow dicts'''
    G = nx.DiGraph()

    for flow  in flows:
        scr,dst = flow["scr_ip"],flow["dist_ip"]
        #enusre both node exixt before adding stats
        if scr not in G:
            G.add_node(scr ,out_flows=0 ,out_bytes=0 ,unique_peers=0 , syn_sent=0)
        if dst not in G:
            G.add_node(dst ,out_flows=0 ,out_bytes=0 ,unique_peers=0 , syn_sent=0)

           # Update source node's behavior stats — this is the key signal:
                # a scanning host will have MANY unique_peers and LOW bytes per flow.
        G.nodes[scr]["out_flows"] += 1
        G.nodes[scr]["out_bytes"] += flow.get("total_bytes", 0)
        G.nodes[scr]["unique_peers"].add(dst)
        G.nodes[scr]["syn_sent"] += flow.get("syn_sent", 0)

        #add the edge itself , carrying the flow
        G.add_edge(scr, dst, packets=flow.get("packet_count", 0),
            bytes=flow.get("total_bytes", 0),
            protocol=flow.get("protocol", "OTHER"))
    return G


def graph_to_pyg_data(G: nx.DiGraph) -> tuple[Data, list[str]]:
    '''convert networkx graph to torch geometric data'''
    node_list = list(G.nodes())
    node_index= {ip:i for i, ip in enumerate(node_list)}
    #build per-node feature vectors

    features=[]
    for ip in node_list:
        attr =G.nodes[ip]
        unique_peer_count = len(attr["unique_peers"])
        #scan_ratio :many peers +few bytes per flow =classic scan featur
        avg_bytes_per_flow = attr["out_bytes"] / max(attr["out_flows"] , 1)
        features.append([attr["out_flows"], attr["out_bytes"], unique_peer_count, avg_bytes_per_flow])

    x = torch.tensor(features, dtype=torch.float)

    #build edge index in COO format
    edges = [[node_index[u], node_index[v]] for u, v in G.edges()]
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous() if edges else torch.empty((2, 0), dtype=torch.long)

    data = Data(
        x=x,
        edge_index=edge_index,
        edge_attr=edge_attr,
    )
    return data, node_list
