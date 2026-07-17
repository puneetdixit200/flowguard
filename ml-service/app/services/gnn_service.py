"""
Load the trained GraphSAGE model and score a batch, or window,
of recent network flows.

The other models score one flow at a time.

The GNN must examine multiple flows together because it needs to see:
- which IPs communicate
- how many peers each IP contacts
- the overall graph structure
"""

import torch
from app.ml.gnn_model import FlowGraphSAGE
from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data

_model = None
_meta = None

def load_gnn():
    global _model, _meta
    if _model is None:
        _meta = torch.load("app/models/gnn_meta.pt")
        _model = FlowGraphSAGE(in_channels=_meta["in_channels"])
        _model.load_state_dict(torch.load("app/models/gnn_graphsage.pt"))
        _model.eval()
    return _model

def score_flow_window(flows: list[dict]) -> dict:
    """
    Returns a dict mapping IP -> {is_anomalous: bool, score: float}.
    This is how you catch a coordinated attacker: their IP node gets
    flagged even if each individual flow looked harmless.
    """
    if len(flows) < 3:
        return {}  # not enough flows to form a meaningful graph yet

    model = load_gnn()
    G = build_ip_graph(flows)
    data, node_list = graph_to_pyg_data(G)

    with torch.no_grad():
        logits = model(data.x, data.edge_index)
        probs = torch.softmax(logits, dim=1)
        preds = probs.argmax(dim=1)

    results = {}
    for i, ip in enumerate(node_list):
        results[ip] = {
            "is_anomalous": bool(preds[i].item() == 1),
            "anomaly_score": float(probs[i][1].item()),
        }
    return results
