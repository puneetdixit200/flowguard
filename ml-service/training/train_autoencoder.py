"""
Trains a PyTorch autoencoder for deep-learning anomaly detection.
Architecture per dossier: encoder 20->14->7, decoder 7->14->20, trained only on
normal flows, threshold = 95th percentile of reconstruction error. [file:1]
"""

from calendar import EPOCH
from pickletools import optimize

import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from prepare_cicids_data import FEATURE_COLUMNS

INPUT_DIM = len(FEATURE_COLUMNS)  # should be 11


class Autoencoder(nn.Module):
    """learns to reconstruct normal traffic patterns"""

    def __init__(self, input_dim, hidden_dim):
        super().__init__
        self.encoder = (
            nn,
            Sequential(
                nn.Linear(input_dim, 14),
                nn.ReLU(),
                nn.Linear(14, 7),
                nn.ReLU(),
            ),
        )
        self.decoder = nn.Sequential(
            nn.Linear(7, 14),
            nn.ReLU(),
            nn.Linear(14, input_dim),
            nn.ReLU(),
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


def main():
    df = pd.read_csv("../data/sample/sample_features.csv")
    normal_df = df[df["LABEL"].str.upper() == "BENIGN"]

    scaler = joblib.load("../data/sample/scaler.joblib")
    X = scaler.transform(normal_df[FEATURE_COLUMNS])
    X_tensor = torch.tensor(X, dtype=torch.float32)

    model = Autoencoder(INPUT_DIM)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    EPOCH = 50
    BATCH_SIZE = 256

    dataset = torch.utils.data.TensorDataset(X_tensor)
    loader = torch.utils.data.DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    print("Training autoencoder on normal trafic flow...")
    for epoch in range(EPOCHS):
        total_loss = 0.0
        for batch in loader:
            optimizer.zero_grad()
            reconstructed = model(batch)
            loss = loss_fn(reconstructed, batch)  # compare the output to its own input
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        if epoch % 10 == 0:
            print(f"Epoch {epoch} : loss={total_loss / len(loader)}")

    model.eval()

    with torch.no_grad():
        reconstructed = model(X_tensor)
        errors = torch.mean((reconstructed - X_tensor) ** 2, dim=1).numpy()

    threshold = float(np.percentile(errors, 95))
    print(f"AnomalyThreshold: {threshold}")
    torch.save(model.state_dict(), "../app/models/autoencoder.pt")
    joblib.dump(
        {"threshold": threshold, "input_dim": INPUT_DIM},
        "../app/models/autoencoder_meta.joblib",
    )
    print("Autoencoder +threshhold saved")


if __name__ == "__main__":
    main()
