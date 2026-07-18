# Baseline rule-based anomaly detector.
# This is intentionally simple — it proves the pipeline works end to end
# before swapping in Isolation Forest / Random Forest / Autoencoder. [file:1]

# ml-service/app/services/detector.py
# CHANGE: detector now builds a lightweight graph_context per flow so the
# ensemble's GNN vote has something to score, instead of always defaulting
# to gnn_vote=0.
from app.ml.ensemble import Ensemble

ensemble = Ensemble()

def detect(flow_features: dict, graph_context=None):
    """
    graph_context: optional dict with keys x, edge_index, node_idx —
    built by app/services/gnn_service.py from recent flow history.
    If None, GNN abstains (vote=0) and detection falls back to the
    original 3-model behavior.
    """
    ordered_features = [
        flow_features["flow_duration"], flow_features["total_packets"],
        flow_features["total_bytes"], flow_features["packets_per_second"],
        flow_features["bytes_per_second"], flow_features["syn_count"],
        flow_features["ack_count"], flow_features["fin_count"],
        flow_features["rst_count"], flow_features["avg_packet_size"],
        flow_features["src_port"],
    ]
    return ensemble.score_flow(ordered_features, graph_context=graph_context)
