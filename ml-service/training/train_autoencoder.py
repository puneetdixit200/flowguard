import os
import torch
import torch.nn as nn
import pandas as pd
import joblib
import numpy as np

from prepare_cicids_data import FEATURE_COLUMNS

INPUT_DIM = len(FEATURE_COLUMNS)

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

def main():
    df = pd.read_csv("../data/sample/sample_features.csv")
    normal_df = df[df["Label"].str.upper() == "BENIGN"]

    scaler = joblib.load("../app/models/scaler.joblib")

    X = scaler.transform(normal_df[FEATURE_COLUMNS])
    X_tensor = torch.tensor(X, dtype=torch.float32)

    model = Autoencoder(INPUT_DIM)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    EPOCHS = 50
    BATCH_SIZE = 256

    dataset = torch.utils.data.TensorDataset(X_tensor)
    loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    print("Training autoencoder on normal traffic only...")

    for epoch in range(EPOCHS):
        total_loss = 0.0

        for (batch,) in loader:
            optimizer.zero_grad()

            reconstructed = model(batch)
            loss = loss_fn(reconstructed, batch)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        if epoch % 10 == 0:
            print(f"Epoch {epoch}: loss={total_loss / len(loader):.6f}")

    model.eval()

    with torch.no_grad():
        reconstructed = model(X_tensor)
        errors = torch.mean((reconstructed - X_tensor) ** 2, dim=1).numpy()

    threshold = float(np.percentile(errors, 95))

    print(f"Anomaly threshold: {threshold:.6f}")

    os.makedirs("../app/models", exist_ok=True)

    torch.save(model.state_dict(), "../app/models/autoencoder.pt")
    joblib.dump(
        {"threshold": threshold, "input_dim": INPUT_DIM},
        "../app/models/autoencoder_meta.joblib"
    )

    print("Autoencoder + threshold saved.")

if __name__ == "__main__":
    main()
