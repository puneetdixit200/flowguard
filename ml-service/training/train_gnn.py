"""
Trains the GraphSAGE model. Since we don't have real labeled multi-host
attack graphs, this trains on synthetic graphs: some IPs behave normally,
others simulate scanning behavior (many peers, low bytes each).
Swap this data generator for real flow logs once you have them.

Train the GraphSAGE model using synthetic network traffic.

Because we currently do not have enough labelled multi-host attack graphs,
we create fake normal hosts, scanner hosts, and target hosts.

Normal hosts:
    Contact only a few targets
    Transfer a reasonable amount of data

Scanner hosts:
    Contact many different targets
    Transfer very few bytes per connection

Later, this synthetic generator should be replaced with real labelled flows.
"""

import torch
import torch.nn.functional as F
import networkx as nx
import random
from app.ml.gnn_model import FlowGraphSAGE
from app.ml.graph_builder import graph_to_pyg_data


def generate_synthetic_flow_graph(n_normal_hosts=40, n_scanners=5, n_targets=60):
    """
    Builds a synthetic network: normal hosts talk to a few peers with
    real byte volume; scanner hosts touch MANY targets with near-zero bytes
    """
    flows = []

    normal_ips = [f"10.0.0.{i}" for i in range(n_normal_hosts)]
    scanner_ips = [f"10.0.1.{i}" for i in range(n_scanners)]
    target_ips = [f"10.0.2.{i}" for i in range(n_targets)]

    # Normal traffic: each normal host talks to 2-5 random targets with real bytes.
    for ip in normal_ips:
        peers = random.sample(target_ips, k=random.randint(2, 5))
        for peer in peers:
            flows.append({
                "src_ip": ip, "dst_ip": peer, "protocol": "TCP",
                "packet_count": random.randint(10, 200),
                "total_bytes": random.randint(2000, 50000),
                "syn_count": random.randint(1, 3),
            })

    # Scanner traffic: each scanner touches MANY targets, each with tiny bytes.
    for ip in scanner_ips:
        peers = random.sample(target_ips, k=random.randint(30, 60))
        for peer in peers:
            flows.append({
                "src_ip": ip, "dst_ip": peer, "protocol": "TCP",
                "packet_count": random.randint(1, 3),
                "total_bytes": random.randint(40, 120),   # tiny — just a SYN probe
                "syn_count": 1,
            })

    labels = {}
    for ip in normal_ips + target_ips:
        labels[ip] = 0  # normal
    for ip in scanner_ips:
        labels[ip] = 1  # anomalous (scanner)

    return flows, labels

def main():
    flows, labels = generate_synthetic_flow_graph()
    G = nx.DiGraph()
    from app.ml.graph_builder import build_ip_graph
    G = build_ip_graph(flows)
    data ,node_list =graph_to_pyg_data(G)
    #map string labels dict to a tensor alignes with node_list order
    y = torch.tensor([labels.get(ip, 0) for ip in node_list],dtype=torch.long)
    model=FlowGraphSAGE(in_channels=data.x.shape[1],hidden_channels=32,out_channels=2)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    model.train()

    for epoch in range(1,101):
        optimizer.zero_grad()
        out = model(data.x, data.edge_index)
        loss = F.cross_entropy(out, y)
        loss.backward()
        optimizer.step()
        if epoch % 20 == 0:
            pred = out.argmax(dim=1)
            acc = (pred == y).float().mean().item()
            print(f'Epoch {epoch:03d}, Loss: {loss.item():.4f}, Train Accuracy: {acc:.4f}')

    torch.save(model.state_dict(), "app/models/gnn_graphsage.pt")
    torch.save({"in_channels": data.x.shape[1]}, "app/models/gnn_meta.pt")
    print("GNN model saved -> ../app/models/gnn_graphsage.pt")

if __name__ == "__main__":
    main()
