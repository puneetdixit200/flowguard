'''graphSAGE model for node-level anomaly clssifification
GraphSAGE works by having each node aggregate ("sample and aggregate") the
features of its neighbors, layer by layer — so a node's final embedding
encodes not just its own behavior, but the behavior of everything it talks to.
This is exactly why it catches coordinated multi-host attacks that per-flow
models can't see.
'''
"""
GraphSAGE model for node-level anomaly classification.

Each graph node represents an IP address.

For every IP, the model predicts:
    class 0 = normal host
    class 1 = anomalous/suspicious host

GraphSAGE combines:
    1. The node's own features
    2. Features from neighboring nodes

With two GraphSAGE layers, every node can learn information from
nodes up to two graph connections away.
"""

import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

class FlowGraphSAGE(torch.nn.Module):
    def __init__(self, in_channels :int, hidden_channels :int=32, out_channels :int=2):
        super().__init__()
        #two SAGECOnv layers = each node "sees" its neighbors and aggregates their features
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x=self.conv1(x, edge_index)
        x=F.relu(x)
        x=F.dropout(x, p=0.3, training=self.training)
        x=self.conv2(x, edge_index)
    #output is raw logits per node:[P(normal), P(anomaly)]
        return x
