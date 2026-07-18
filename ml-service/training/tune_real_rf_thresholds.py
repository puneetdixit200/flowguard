"""
Select operational Random Forest thresholds using only the real Thursday
validation split.

Three modes are produced:

balanced:
    Threshold with the highest validation F1.

high_recall:
    Highest threshold that still achieves at least 98% validation recall.

high_precision:
    Threshold that achieves at least 95% validation precision while
    retaining the highest possible recall.

The untouched Friday test split is used only for final reporting.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIRECTORY = PROJECT_ROOT / "data" / "real_only"
MODEL_DIRECTORY = PROJECT_ROOT / "app" / "models" / "real_only"
DOCUMENT_DIRECTORY = PROJECT_ROOT.parent / "docs"

FEATURE_COLUMNS = [
    "duration_seconds",
    "packet_count",
    "total_bytes",
    "bytes_per_sec",
    "packets_per_sec",
    "syn_count",
    "ack_count",
    "fin_count",
    "rst_count",
    "syn_ack_ratio",
    "rst_ratio",
]


def load_dataset(file_name: str):
    path = DATA_DIRECTORY / file_name
    dataframe = pd.read_csv(path)

    features = dataframe[FEATURE_COLUMNS].to_numpy(
        dtype=np.float32
    )

    labels = dataframe["Label"].to_numpy(
        dtype=np.int64
    )

    return dataframe, features, labels


def metrics_for_threshold(
    labels: np.ndarray,
    probabilities: np.ndarray,
    threshold: float,
) -> dict:
    predictions = (
        probabilities >= threshold
    ).astype(np.int64)

    matrix = confusion_matrix(
        labels,
        predictions,
        labels=[0, 1],
    )

    true_negatives, false_positives = matrix[0]
    false_negatives, true_positives = matrix[1]

    return {
        "threshold": float(threshold),
        "accuracy": float(
            accuracy_score(labels, predictions)
        ),
        "balanced_accuracy": float(
            balanced_accuracy_score(labels, predictions)
        ),
        "precision": float(
            precision_score(
                labels,
                predictions,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                labels,
                predictions,
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                labels,
                predictions,
                zero_division=0,
            )
        ),
        "roc_auc": float(
            roc_auc_score(labels, probabilities)
        ),
        "true_negatives": int(true_negatives),
        "false_positives": int(false_positives),
        "false_negatives": int(false_negatives),
        "true_positives": int(true_positives),
        "alert_count": int(predictions.sum()),
        "total_rows": int(len(predictions)),
    }


def print_metrics(
    title: str,
    metrics: dict,
) -> None:
    print(f"\n===== {title} =====")
    print(f"Threshold:         {metrics['threshold']:.6f}")
    print(f"Accuracy:          {metrics['accuracy']:.4f}")
    print(
        f"Balanced accuracy: "
        f"{metrics['balanced_accuracy']:.4f}"
    )
    print(f"Precision:         {metrics['precision']:.4f}")
    print(f"Recall:            {metrics['recall']:.4f}")
    print(f"F1:                {metrics['f1']:.4f}")
    print(f"ROC-AUC:           {metrics['roc_auc']:.4f}")
    print(
        "Confusion matrix:\n"
        f"[[{metrics['true_negatives']} "
        f"{metrics['false_positives']}]\n"
        f" [{metrics['false_negatives']} "
        f"{metrics['true_positives']}]]"
    )


validation_dataframe, validation_features, validation_labels = (
    load_dataset("validation_real.csv")
)

test_dataframe, test_features, test_labels = load_dataset(
    "test_real.csv"
)

scaler = joblib.load(
    MODEL_DIRECTORY / "supervised_scaler.joblib"
)

model = joblib.load(
    MODEL_DIRECTORY / "random_forest.joblib"
)

validation_scaled = scaler.transform(
    validation_features
)

test_scaled = scaler.transform(
    test_features
)

model_classes = list(model.classes_)
attack_class_index = model_classes.index(1)

validation_probabilities = model.predict_proba(
    validation_scaled
)[:, attack_class_index]

test_probabilities = model.predict_proba(
    test_scaled
)[:, attack_class_index]


# Sweep 2,001 thresholds from zero to one.
threshold_values = np.linspace(
    0.0,
    1.0,
    2001,
)

validation_results = [
    metrics_for_threshold(
        validation_labels,
        validation_probabilities,
        threshold,
    )
    for threshold in threshold_values
]


# Balanced mode: highest validation F1.
balanced_result = max(
    validation_results,
    key=lambda result: (
        result["f1"],
        result["balanced_accuracy"],
        result["precision"],
    ),
)


# High-recall mode: highest threshold that preserves >= 98% recall.
high_recall_candidates = [
    result
    for result in validation_results
    if result["recall"] >= 0.98
]

if high_recall_candidates:
    high_recall_result = max(
        high_recall_candidates,
        key=lambda result: (
            result["threshold"],
            result["precision"],
        ),
    )
else:
    high_recall_result = max(
        validation_results,
        key=lambda result: (
            result["recall"],
            result["precision"],
        ),
    )


# High-precision mode: among thresholds with >= 95% precision,
# retain the greatest possible recall.
high_precision_candidates = [
    result
    for result in validation_results
    if result["precision"] >= 0.95
]

if high_precision_candidates:
    high_precision_result = max(
        high_precision_candidates,
        key=lambda result: (
            result["recall"],
            result["f1"],
        ),
    )
else:
    high_precision_result = max(
        validation_results,
        key=lambda result: (
            result["precision"],
            result["recall"],
        ),
    )


selected_validation_results = {
    "balanced": balanced_result,
    "high_recall": high_recall_result,
    "high_precision": high_precision_result,
}


print("===== THRESHOLDS SELECTED USING THURSDAY VALIDATION DATA =====")

for mode_name, validation_result in selected_validation_results.items():
    print_metrics(
        f"{mode_name.upper()} — VALIDATION",
        validation_result,
    )


print("\n\n===== UNTOUCHED FRIDAY TEST RESULTS =====")

test_results = {}

for mode_name, validation_result in selected_validation_results.items():
    threshold = validation_result["threshold"]

    test_result = metrics_for_threshold(
        test_labels,
        test_probabilities,
        threshold,
    )

    test_results[mode_name] = test_result

    print_metrics(
        f"{mode_name.upper()} — REAL TEST",
        test_result,
    )


# Also show fixed thresholds for comparison.
print("\n\n===== FIXED-THRESHOLD COMPARISON ON VALIDATION =====")
print(
    "threshold | accuracy | precision | recall | F1 | alerts"
)

for threshold in [
    0.023552,
    0.05,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
]:
    result = metrics_for_threshold(
        validation_labels,
        validation_probabilities,
        threshold,
    )

    print(
        f"{threshold:>9.6f} | "
        f"{result['accuracy']:.4f} | "
        f"{result['precision']:.4f} | "
        f"{result['recall']:.4f} | "
        f"{result['f1']:.4f} | "
        f"{result['alert_count']}/{result['total_rows']}"
    )


output = {
    "selection_dataset": "Thursday CICIDS2017 validation split",
    "reporting_dataset": "Friday CICIDS2017 untouched test split",
    "thresholds": {
        mode_name: float(result["threshold"])
        for mode_name, result in selected_validation_results.items()
    },
    "validation_metrics": selected_validation_results,
    "test_metrics": test_results,
}

output_path = (
    MODEL_DIRECTORY
    / "rf_operational_thresholds.json"
)

with output_path.open(
    "w",
    encoding="utf-8",
) as output_file:
    json.dump(
        output,
        output_file,
        indent=2,
    )

print(f"\nSaved operational thresholds: {output_path}")
