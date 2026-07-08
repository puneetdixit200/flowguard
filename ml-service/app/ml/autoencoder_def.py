"""
Shared model class — must be identical to the one used in training,
otherwise torch.load() will fail to match saved weights to the architecture.
"""

import torch.nn as nn


class Autoencoder(nn.Module):
    def __init__(self, input_dim: int):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 14),
            nn.ReLU(),
            nn.Linear(14, 7),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.Linear(7, 14),
            nn.ReLU(),
            nn.Linear(14, input_dim),
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))
