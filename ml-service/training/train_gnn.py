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
# ml-service/training/train_gnn.py
"""
Trains GraphSAGE with 4 fixes aimed directly at false positives:
  1. class_weight in the loss -> stops the model from over-predicting "attack"
     just because attacks are rarer (imbalance-driven false positives).
  2. NeighborLoader mini-batching -> trains on graph neighborhoods instead of
     the whole graph at once, which generalizes better on larger real graphs.
  3. Validation split + early stopping -> stops training the moment validation
     loss stops improving, instead of overfitting the training graph.
  4. Dropout (already added in gnn_model.py) works together with this.
"""
import torch
import torch.nn.functional as F
from torch_geometric.loader import NeighborLoader
from app.ml.gnn_model import FlowGraphSAGE
from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data
import pandas as pd

df = pd.read_csv("../data/raw/cicids2017_sample.csv")
flows = df.to_dict("records")

G = build_ip_graph(flows)
data, node_list = graph_to_pyg_data(G)

# ---- Class weighting: compute weight inversely proportional to class frequency ----
num_pos = int(data.y.sum())
num_neg = int((data.y == 0).sum())
total = num_pos + num_neg
weight_for_benign = total / (2.0 * num_neg) if num_neg > 0 else 1.0
weight_for_attack = total / (2.0 * num_pos) if num_pos > 0 else 1.0
class_weights = torch.tensor([weight_for_benign, weight_for_attack], dtype=torch.float)
print(f"Class weights -> benign: {weight_for_benign:.3f}, attack: {weight_for_attack:.3f}")

# ---- Train/val split at the node level ----
num_nodes = data.num_nodes
perm = torch.randperm(num_nodes)
train_size = int(0.8 * num_nodes)
train_mask = torch.zeros(num_nodes, dtype=torch.bool)
val_mask = torch.zeros(num_nodes, dtype=torch.bool)
train_mask[perm[:train_size]] = True
val_mask[perm[train_size:]] = True

# ---- Mini-batching via NeighborLoader instead of full-graph training ----
train_loader = NeighborLoader(
    data,
    num_neighbors=[10, 10],   # sample up to 10 neighbors at each of 2 hops
    batch_size=64,
    input_nodes=train_mask,
    shuffle=True,
)

model = FlowGraphSAGE(in_channels=data.x.shape[1])
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

best_val_loss = float("inf")
patience = 5          # NEW: early stopping patience
patience_counter = 0
max_epochs = 100

for epoch in range(max_epochs):
    model.train()
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        out = model(batch.x, batch.edge_index)
        # weight= applies class_weights so minority attack nodes matter more,
        # and majority benign nodes don't dominate the gradient -> fewer FPs.
        loss = F.cross_entropy(out[:batch.batch_size], batch.y[:batch.batch_size], weight=class_weights)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    # ---- Validation pass (full graph, no grad) for early stopping ----
    model.eval()
    with torch.no_grad():
        val_out = model(data.x, data.edge_index)
        val_loss = F.cross_entropy(val_out[val_mask], data.y[val_mask], weight=class_weights).item()

    print(f"Epoch {epoch:03d} | train_loss={total_loss:.4f} | val_loss={val_loss:.4f}")

    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        torch.save(model.state_dict(), "../app/models/gnn_graphsage.pt")  # save best checkpoint
        print("  -> new best model saved")
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Early stopping at epoch {epoch} (no val improvement for {patience} epochs)")
            break

print("Training complete. Best val_loss:", best_val_loss)
