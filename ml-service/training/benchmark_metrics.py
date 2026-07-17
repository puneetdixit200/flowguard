"""
Generate resume-worthy FlowGuard ML metrics:

1. Accuracy, precision, recall and F1 score
2. Average inference latency per model
3. Full ensemble throughput
4. Dataset size, feature count and class count

Output:
    ../docs/resume_metrics.json
"""

import json
import time
from pathlib import Path

import joblib
import pandas as pd
import torch
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)

from app.ml.autoencoder_def import Autoencoder
from prepare_cicids_data import FEATURE_COLUMNS


# Absolute, reliable paths based on this file's location.
ML_SERVICE_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ML_SERVICE_ROOT / "app" / "models"
DATA_DIR = ML_SERVICE_ROOT / "data" / "sample"
DOCS_DIR = ML_SERVICE_ROOT.parent / "docs"


def measure_latency(predict_function, X, number_of_runs=100):
    """
    Measure the average time required to score one flow.

    The first row is used repeatedly so the measurement focuses on model
    inference rather than reading data from disk.
    """
    sample = X.iloc[[0]]

    # Warm up the model before timing.
    for _ in range(10):
        predict_function(sample)

    start = time.perf_counter()

    for _ in range(number_of_runs):
        predict_function(sample)

    elapsed_seconds = time.perf_counter() - start
    average_milliseconds = (
        elapsed_seconds / number_of_runs
    ) * 1000

    return round(average_milliseconds, 4)


def main():
    test_file = DATA_DIR / "test_holdout.csv"
    training_file = DATA_DIR / "sample_features.csv"

    if not test_file.exists():
        raise FileNotFoundError(
            f"Test dataset not found: {test_file}"
        )

    required_models = [
        "scaler.joblib",
        "isolation_forest.joblib",
        "random_forest.joblib",
        "label_encoder.joblib",
        "autoencoder_meta.joblib",
        "autoencoder.pt",
    ]

    missing_models = [
        filename
        for filename in required_models
        if not (MODELS_DIR / filename).exists()
    ]

    if missing_models:
        raise FileNotFoundError(
            "Missing model files: " + ", ".join(missing_models)
        )

    # ---------------------------------------------------------
    # Load held-out data that the models did not see in training
    # ---------------------------------------------------------
    df = pd.read_csv(test_file)

    X = df[FEATURE_COLUMNS]

    y_true_binary = (
        df["Label"].str.upper() != "BENIGN"
    ).astype(int).to_numpy()

    # ---------------------------------------------------------
    # Load trained models
    # ---------------------------------------------------------
    scaler = joblib.load(MODELS_DIR / "scaler.joblib")
    isolation_forest = joblib.load(
        MODELS_DIR / "isolation_forest.joblib"
    )
    random_forest = joblib.load(
        MODELS_DIR / "random_forest.joblib"
    )
    label_encoder = joblib.load(
        MODELS_DIR / "label_encoder.joblib"
    )
    autoencoder_metadata = joblib.load(
        MODELS_DIR / "autoencoder_meta.joblib"
    )

    autoencoder = Autoencoder(
        autoencoder_metadata["input_dim"]
    )

    autoencoder.load_state_dict(
        torch.load(
            MODELS_DIR / "autoencoder.pt",
            map_location="cpu",
        )
    )

    autoencoder.eval()

    metrics = {}

    # ---------------------------------------------------------
    # Isolation Forest
    # ---------------------------------------------------------
    X_scaled = scaler.transform(X)

    isolation_predictions = (
        isolation_forest.predict(X_scaled) == -1
    ).astype(int)

    def isolation_predict(sample):
        scaled_sample = scaler.transform(sample)
        return isolation_forest.predict(scaled_sample)

    metrics["isolation_forest"] = {
        "accuracy": round(
            accuracy_score(
                y_true_binary,
                isolation_predictions,
            ),
            4,
        ),
        "precision": round(
            precision_score(
                y_true_binary,
                isolation_predictions,
                zero_division=0,
            ),
            4,
        ),
        "recall": round(
            recall_score(
                y_true_binary,
                isolation_predictions,
                zero_division=0,
            ),
            4,
        ),
        "f1": round(
            f1_score(
                y_true_binary,
                isolation_predictions,
                zero_division=0,
            ),
            4,
        ),
        "average_inference_ms": measure_latency(
            isolation_predict,
            X,
        ),
    }

    # ---------------------------------------------------------
    # Random Forest
    # ---------------------------------------------------------
    random_forest_predictions = random_forest.predict(X)

    decoded_random_forest_predictions = (
        label_encoder.inverse_transform(
            random_forest_predictions
        )
    )

    random_forest_binary = (
        decoded_random_forest_predictions != "BENIGN"
    ).astype(int)

    metrics["random_forest"] = {
        "accuracy": round(
            accuracy_score(
                y_true_binary,
                random_forest_binary,
            ),
            4,
        ),
        "precision": round(
            precision_score(
                y_true_binary,
                random_forest_binary,
                zero_division=0,
            ),
            4,
        ),
        "recall": round(
            recall_score(
                y_true_binary,
                random_forest_binary,
                zero_division=0,
            ),
            4,
        ),
        "f1": round(
            f1_score(
                y_true_binary,
                random_forest_binary,
                zero_division=0,
            ),
            4,
        ),
        "average_inference_ms": measure_latency(
            random_forest.predict,
            X,
        ),
    }

    # ---------------------------------------------------------
    # Autoencoder
    # ---------------------------------------------------------
    def autoencoder_predict(sample):
        scaled_sample = scaler.transform(sample)

        tensor = torch.tensor(
            scaled_sample,
            dtype=torch.float32,
        )

        with torch.no_grad():
            reconstructed = autoencoder(tensor)

            errors = torch.mean(
                (reconstructed - tensor) ** 2,
                dim=1,
            )

        return errors.cpu().numpy()

    autoencoder_errors = autoencoder_predict(X)

    autoencoder_predictions = (
        autoencoder_errors
        > autoencoder_metadata["threshold"]
    ).astype(int)

    metrics["autoencoder"] = {
        "accuracy": round(
            accuracy_score(
                y_true_binary,
                autoencoder_predictions,
            ),
            4,
        ),
        "precision": round(
            precision_score(
                y_true_binary,
                autoencoder_predictions,
                zero_division=0,
            ),
            4,
        ),
        "recall": round(
            recall_score(
                y_true_binary,
                autoencoder_predictions,
                zero_division=0,
            ),
            4,
        ),
        "f1": round(
            f1_score(
                y_true_binary,
                autoencoder_predictions,
                zero_division=0,
            ),
            4,
        ),
        "average_inference_ms": measure_latency(
            autoencoder_predict,
            X,
        ),
        "threshold": float(
            autoencoder_metadata["threshold"]
        ),
    }

    # ---------------------------------------------------------
    # Ensemble: at least two of three models must flag the flow
    # ---------------------------------------------------------
    votes = (
        isolation_predictions
        + random_forest_binary
        + autoencoder_predictions
    )

    ensemble_predictions = (votes >= 2).astype(int)

    metrics["ensemble"] = {
        "accuracy": round(
            accuracy_score(
                y_true_binary,
                ensemble_predictions,
            ),
            4,
        ),
        "precision": round(
            precision_score(
                y_true_binary,
                ensemble_predictions,
                zero_division=0,
            ),
            4,
        ),
        "recall": round(
            recall_score(
                y_true_binary,
                ensemble_predictions,
                zero_division=0,
            ),
            4,
        ),
        "f1": round(
            f1_score(
                y_true_binary,
                ensemble_predictions,
                zero_division=0,
            ),
            4,
        ),
        "false_positives": int(
            (
                (ensemble_predictions == 1)
                & (y_true_binary == 0)
            ).sum()
        ),
        "false_negatives": int(
            (
                (ensemble_predictions == 0)
                & (y_true_binary == 1)
            ).sum()
        ),
    }

    # ---------------------------------------------------------
    # Dataset scale
    # ---------------------------------------------------------
    training_rows = 0

    if training_file.exists():
        training_rows = len(pd.read_csv(training_file))

    metrics["dataset_scale"] = {
        "training_rows": training_rows,
        "test_rows": len(df),
        "total_rows": training_rows + len(df),
        "feature_count": len(FEATURE_COLUMNS),
        "class_count": len(label_encoder.classes_),
        "classes": label_encoder.classes_.tolist(),
        "test_attack_rows": int(y_true_binary.sum()),
        "test_benign_rows": int(
            (y_true_binary == 0).sum()
        ),
    }

    # ---------------------------------------------------------
    # Full ensemble throughput
    # ---------------------------------------------------------
    throughput_start = time.perf_counter()

    for row_number in range(len(X)):
        row = X.iloc[[row_number]]
        scaled_row = scaler.transform(row)

        isolation_vote = int(
            isolation_forest.predict(scaled_row)[0] == -1
        )

        random_forest_prediction = random_forest.predict(
            row
        )

        random_forest_label = (
            label_encoder.inverse_transform(
                random_forest_prediction
            )[0]
        )

        random_forest_vote = int(
            random_forest_label != "BENIGN"
        )

        tensor = torch.tensor(
            scaled_row,
            dtype=torch.float32,
        )

        with torch.no_grad():
            reconstructed = autoencoder(tensor)

            reconstruction_error = torch.mean(
                (reconstructed - tensor) ** 2
            ).item()

        autoencoder_vote = int(
            reconstruction_error
            > autoencoder_metadata["threshold"]
        )

        _ensemble_result = (
            isolation_vote
            + random_forest_vote
            + autoencoder_vote
        ) >= 2

    throughput_elapsed = (
        time.perf_counter() - throughput_start
    )

    metrics["ensemble_throughput"] = {
        "flows_scored": len(X),
        "total_seconds": round(
            throughput_elapsed,
            4,
        ),
        "flows_per_second": round(
            len(X) / throughput_elapsed,
            2,
        ),
        "average_ensemble_ms_per_flow": round(
            throughput_elapsed / len(X) * 1000,
            4,
        ),
    }

    # ---------------------------------------------------------
    # Save and print results
    # ---------------------------------------------------------
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    output_file = DOCS_DIR / "resume_metrics.json"

    with output_file.open("w") as file:
        json.dump(metrics, file, indent=2)

    print(json.dumps(metrics, indent=2))
    print(f"\nSaved metrics to: {output_file}")


if __name__ == "__main__":
    main()
