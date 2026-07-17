"""
Evaluate FlowGuard's trained flat models against real CICIDS2017 flows.

Models evaluated:
- Isolation Forest
- Random Forest
- Autoencoder
- 2-of-3 ensemble

The GNN is not included here because it requires constructing an IP graph,
rather than independently evaluating each flow row.
"""

from pathlib import Path

import joblib
import pandas as pd
import torch
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from app.ml.autoencoder_def import Autoencoder
from prepare_cicids_data import FEATURE_COLUMNS


ML_SERVICE_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = (
    ML_SERVICE_ROOT
    / "data"
    / "cicids2017"
    / "real_test_set.csv"
)
MODELS_DIRECTORY = ML_SERVICE_ROOT / "app" / "models"


def load_distributed_sample(
    path: Path,
    maximum_rows: int = 200_000,
) -> pd.DataFrame:
    """
    Sample rows from across the whole CSV without loading all 2.8 million
    rows into memory at once.
    """

    sampled_chunks = []

    for chunk_number, chunk in enumerate(
        pd.read_csv(path, chunksize=100_000)
    ):
        rows_to_take = min(15_000, len(chunk))

        sampled_chunks.append(
            chunk.sample(
                n=rows_to_take,
                random_state=42 + chunk_number,
            )
        )

    dataframe = pd.concat(
        sampled_chunks,
        ignore_index=True,
    )

    if len(dataframe) > maximum_rows:
        dataframe = dataframe.sample(
            n=maximum_rows,
            random_state=42,
        )

    return dataframe.reset_index(drop=True)


def print_metrics(
    model_name: str,
    true_labels,
    predictions,
) -> None:
    print(f"\n===== {model_name} =====")

    print(
        f"Accuracy:  "
        f"{accuracy_score(true_labels, predictions):.4f}"
    )
    print(
        f"Precision: "
        f"{precision_score(true_labels, predictions, zero_division=0):.4f}"
    )
    print(
        f"Recall:    "
        f"{recall_score(true_labels, predictions, zero_division=0):.4f}"
    )
    print(
        f"F1:        "
        f"{f1_score(true_labels, predictions, zero_division=0):.4f}"
    )

    print("Confusion matrix:")
    print(confusion_matrix(true_labels, predictions))


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Prepared CICIDS dataset not found: {DATA_FILE}"
        )

    print("Loading a distributed sample from CICIDS2017...")

    dataframe = load_distributed_sample(DATA_FILE)

    missing_features = [
        feature
        for feature in FEATURE_COLUMNS
        if feature not in dataframe.columns
    ]

    if missing_features:
        raise ValueError(
            "Prepared data is missing features: "
            + ", ".join(missing_features)
        )

    X = dataframe[FEATURE_COLUMNS]

    true_binary_labels = (
        dataframe["Label"]
        .astype(str)
        .str.strip()
        .str.upper()
        .ne("BENIGN")
        .astype(int)
        .to_numpy()
    )

    scaler = joblib.load(
        MODELS_DIRECTORY / "scaler.joblib"
    )

    isolation_forest = joblib.load(
        MODELS_DIRECTORY / "isolation_forest.joblib"
    )

    random_forest = joblib.load(
        MODELS_DIRECTORY / "random_forest.joblib"
    )

    label_encoder = joblib.load(
        MODELS_DIRECTORY / "label_encoder.joblib"
    )

    autoencoder_metadata = joblib.load(
        MODELS_DIRECTORY / "autoencoder_meta.joblib"
    )

    autoencoder = Autoencoder(
        autoencoder_metadata["input_dim"]
    )

    autoencoder.load_state_dict(
        torch.load(
            MODELS_DIRECTORY / "autoencoder.pt",
            map_location="cpu",
        )
    )

    autoencoder.eval()

    # ---------------------------------------------------------
    # Isolation Forest
    # ---------------------------------------------------------
    X_scaled = scaler.transform(X)

    isolation_predictions = (
        isolation_forest.predict(X_scaled) == -1
    ).astype(int)

    # ---------------------------------------------------------
    # Random Forest
    # ---------------------------------------------------------
    random_forest_raw = random_forest.predict(X)

    random_forest_labels = (
        label_encoder.inverse_transform(
            random_forest_raw
        )
    )

    random_forest_predictions = (
        random_forest_labels != "BENIGN"
    ).astype(int)

    # ---------------------------------------------------------
    # Autoencoder
    # ---------------------------------------------------------
    X_tensor = torch.tensor(
        X_scaled,
        dtype=torch.float32,
    )

    with torch.no_grad():
        reconstructed = autoencoder(X_tensor)

        reconstruction_errors = torch.mean(
            (reconstructed - X_tensor) ** 2,
            dim=1,
        ).cpu().numpy()

    autoencoder_predictions = (
        reconstruction_errors
        > autoencoder_metadata["threshold"]
    ).astype(int)

    # ---------------------------------------------------------
    # Ensemble
    # ---------------------------------------------------------
    votes = (
        isolation_predictions
        + random_forest_predictions
        + autoencoder_predictions
    )

    ensemble_predictions = (votes >= 2).astype(int)

    print("\n===== REAL CICIDS2017 DATASET =====")
    print(f"Evaluated rows: {len(dataframe):,}")
    print(
        f"Real attack rows: "
        f"{int(true_binary_labels.sum()):,}"
    )
    print(
        f"Real benign rows: "
        f"{int((true_binary_labels == 0).sum()):,}"
    )

    print_metrics(
        "ISOLATION FOREST",
        true_binary_labels,
        isolation_predictions,
    )

    print_metrics(
        "RANDOM FOREST",
        true_binary_labels,
        random_forest_predictions,
    )

    print_metrics(
        "AUTOENCODER",
        true_binary_labels,
        autoencoder_predictions,
    )

    print_metrics(
        "2-OF-3 ENSEMBLE",
        true_binary_labels,
        ensemble_predictions,
    )


if __name__ == "__main__":
    main()
