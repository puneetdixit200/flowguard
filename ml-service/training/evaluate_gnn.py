"""
Evaluate the trained GraphSAGE model on unseen synthetic network graphs.

Important:
- This is a node-level synthetic evaluation.
- It is not a real CICIDS2017 evaluation.
- It is not directly comparable to flow-level Random Forest metrics.
"""

from pathlib import Path
import random
import sys

import torch
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

# ml-service/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.ml.gnn_model import FlowGraphSAGE
from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data
from train_gnn import generate_synthetic_flow_graph


MODEL_DIRECTORY = PROJECT_ROOT / "app" / "models"
MODEL_PATH = MODEL_DIRECTORY / "gnn_graphsage.pt"
META_PATH = MODEL_DIRECTORY / "gnn_meta.pt"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"GNN model not found: {MODEL_PATH}")

if not META_PATH.exists():
    raise FileNotFoundError(f"GNN metadata not found: {META_PATH}")


# Load the architecture information saved during training.
metadata = torch.load(META_PATH, map_location="cpu")

model = FlowGraphSAGE(
    in_channels=int(metadata["in_channels"]),
    hidden_channels=32,
    out_channels=2,
)

model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

all_true_labels = []
all_predictions = []

# Evaluate on 20 independently generated graphs that were not used to train.
for test_seed in range(1000, 1020):
    random.seed(test_seed)
    torch.manual_seed(test_seed)

    flows, labels = generate_synthetic_flow_graph(
        n_normal_hosts=80,
        n_scanners=10,
        n_targets=120,
    )

    graph = build_ip_graph(flows)
    data, node_list = graph_to_pyg_data(graph)

    true_labels = torch.tensor(
        [labels.get(ip_address, 0) for ip_address in node_list],
        dtype=torch.long,
    )

    with torch.no_grad():
        logits = model(data.x, data.edge_index)
        predictions = logits.argmax(dim=1)

    all_true_labels.extend(true_labels.tolist())
    all_predictions.extend(predictions.tolist())


print("===== GRAPHSAGE SYNTHETIC EVALUATION =====")
print(f"Graphs evaluated: 20")
print(f"Nodes evaluated:  {len(all_true_labels)}")
print(f"Accuracy:          {accuracy_score(all_true_labels, all_predictions):.4f}")
print(
    f"Precision:         "
    f"{precision_score(all_true_labels, all_predictions, zero_division=0):.4f}"
)
print(
    f"Recall:            "
    f"{recall_score(all_true_labels, all_predictions, zero_division=0):.4f}"
)
print(
    f"F1:                "
    f"{f1_score(all_true_labels, all_predictions, zero_division=0):.4f}"
)
print("Confusion matrix:")
print(confusion_matrix(all_true_labels, all_predictions))
