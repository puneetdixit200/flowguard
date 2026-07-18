# ml-service/training/build_host_graph_from_cicids.py
"""
Builds a TRUE host-communication graph from real CICIDS2017 PCAP-derived
flows (with real src_ip/dst_ip), instead of the earlier synthetic/CSV-only
graph that had no genuine IP topology.

Nodes = unique IPs. Edges = flows between them. Node features = aggregated
traffic stats per IP. This is what makes GraphSAGE actually learn
host-communication patterns (e.g. one host scanning many others) instead of
just per-flow statistics.
"""
import json
import networkx as nx
import torch
from torch_geometric.utils import from_networkx

# CICIDS2017 attacker/victim IPs are publicly documented per day (from the
# official dataset description) — used to label nodes for training/eval.
KNOWN_ATTACKER_IPS = {"192.168.10.50", "205.174.165.73"}  # example subset; verify against the official CICIDS2017 attack IP table for the day you downloaded

def load_flows(jsonl_path):
    flows = []
    with open(jsonl_path) as f:
        for line in f:
            if line.strip():
                flows.append(json.loads(line))
    return flows

def build_graph(flows):
    G = nx.Graph()
    for flow in flows:
        src, dst = flow["src_ip"], flow["dst_ip"]
        for ip in (src, dst):
            if ip not in G:
                # Node features: total packets/bytes seen, updated incrementally.
                G.add_node(ip, packets=0, bytes=0,
                           label=1 if ip in KNOWN_ATTACKER_IPS else 0)
        G.nodes[src]["packets"] += flow.get("packet_count", 0)
        G.nodes[src]["bytes"] += flow.get("total_bytes", 0)
        # Edge = a real observed communication between two hosts.
        if G.has_edge(src, dst):
            G[src][dst]["weight"] += 1
        else:
            G.add_edge(src, dst, weight=1)
    return G

def graph_to_pyg(G):
    # Convert node feature dicts into a tensor GraphSAGE can consume.
    for node in G.nodes:
        packets = G.nodes[node]["packets"]
        bytes_ = G.nodes[node]["bytes"]
        G.nodes[node]["x"] = [packets, bytes_]
    data = from_networkx(G, group_node_attrs=["x"])
    data.x = data.x.float()
    data.y = torch.tensor([G.nodes[n]["label"] for n in G.nodes], dtype=torch.long)
    return data, list(G.nodes)

if __name__ == "__main__":
    flows = load_flows("../../data/cicids_raw/wednesday_flows.jsonl")
    G = build_graph(flows)
    print(f"Built graph: {G.number_of_nodes()} host nodes, {G.number_of_edges()} edges")
    data, node_list = graph_to_pyg(G)
    torch.save({"data": data, "node_list": node_list}, "../data/sample/real_host_graph.pt")
    print("Saved -> ml-service/data/sample/real_host_graph.pt")
