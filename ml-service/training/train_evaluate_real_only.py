"""
Train and evaluate FlowGuard entirely on real CICIDS2017 network flows.

Data split:
    Monday–Wednesday -> training
    Thursday         -> validation and threshold selection
    Friday           -> final untouched test

Models:
    1. Isolation Forest
    2. Random Forest
    3. Autoencoder
    4. GraphSAGE flow-similarity Graph Neural Network

The script also evaluates a four-model voting ensemble.
"""

from __future__ import annotations

import copy
import json
import os
import random
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import torch
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from torch_geometric.data import Data
from torch_geometric.nn import SAGEConv


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

RANDOM_SEED = 42

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

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data" / "real_only"
MODEL_DIRECTORY = PROJECT_ROOT / "app" / "models" / "real_only"
DOCUMENT_DIRECTORY = PROJECT_ROOT.parent / "docs"

MODEL_DIRECTORY.mkdir(parents=True, exist_ok=True)
DOCUMENT_DIRECTORY.mkdir(parents=True, exist_ok=True)


def set_random_seeds(seed: int) -> None:
    """Make model training as reproducible as practical."""

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


set_random_seeds(RANDOM_SEED)

torch.set_num_threads(
    max(1, min(8, os.cpu_count() or 1))
)


# ---------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------

def load_split(file_name: str):
    """Load one prepared real CICIDS2017 split."""

    path = DATA_DIRECTORY / file_name

    if not path.exists():
        raise FileNotFoundError(f"Dataset was not found: {path}")

    dataframe = pd.read_csv(path)

    missing_columns = [
        column
        for column in FEATURE_COLUMNS + ["Label", "attack_type"]
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{file_name} is missing columns: {missing_columns}"
        )

    dataframe[FEATURE_COLUMNS] = dataframe[FEATURE_COLUMNS].apply(
        pd.to_numeric,
        errors="coerce",
    )

    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)

    original_size = len(dataframe)

    dataframe.dropna(
        subset=FEATURE_COLUMNS + ["Label"],
        inplace=True,
    )

    dataframe.reset_index(drop=True, inplace=True)

    dropped_rows = original_size - len(dataframe)

    if dropped_rows:
        print(
            f"Dropped {dropped_rows:,} invalid rows from {file_name}"
        )

    features = dataframe[FEATURE_COLUMNS].to_numpy(
        dtype=np.float32
    )

    labels = dataframe["Label"].to_numpy(dtype=np.int64)

    return dataframe, features, labels


train_dataframe, train_features, train_labels = load_split(
    "train_real.csv"
)

validation_dataframe, validation_features, validation_labels = load_split(
    "validation_real.csv"
)

test_dataframe, test_features, test_labels = load_split(
    "test_real.csv"
)


print("===== REAL-ONLY DATASET =====")
print(f"Training rows:   {len(train_labels):,}")
print(f"Validation rows: {len(validation_labels):,}")
print(f"Testing rows:    {len(test_labels):,}")
print()


# ---------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------

def calculate_metrics(
    true_labels: np.ndarray,
    predictions: np.ndarray,
    attack_scores: np.ndarray | None = None,
) -> dict:
    """Calculate binary intrusion-detection metrics."""

    result = {
        "accuracy": float(
            accuracy_score(true_labels, predictions)
        ),
        "balanced_accuracy": float(
            balanced_accuracy_score(true_labels, predictions)
        ),
        "precision": float(
            precision_score(
                true_labels,
                predictions,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                true_labels,
                predictions,
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                true_labels,
                predictions,
                zero_division=0,
            )
        ),
        "confusion_matrix": confusion_matrix(
            true_labels,
            predictions,
        ).tolist(),
    }

    if (
        attack_scores is not None
        and len(np.unique(true_labels)) == 2
    ):
        result["roc_auc"] = float(
            roc_auc_score(true_labels, attack_scores)
        )
    else:
        result["roc_auc"] = None

    return result


def print_metrics(model_name: str, metrics: dict) -> None:
    """Print a readable model report."""

    print(f"\n===== {model_name} =====")
    print(f"Accuracy:          {metrics['accuracy']:.4f}")
    print(
        f"Balanced accuracy: "
        f"{metrics['balanced_accuracy']:.4f}"
    )
    print(f"Precision:         {metrics['precision']:.4f}")
    print(f"Recall:            {metrics['recall']:.4f}")
    print(f"F1:                {metrics['f1']:.4f}")

    if metrics["roc_auc"] is not None:
        print(f"ROC-AUC:           {metrics['roc_auc']:.4f}")

    print("Confusion matrix:")
    print(np.asarray(metrics["confusion_matrix"]))


def find_best_threshold(
    true_labels: np.ndarray,
    attack_scores: np.ndarray,
) -> tuple[float, dict]:
    """
    Select a decision threshold using validation data only.

    The threshold maximizing F1 is selected. Balanced accuracy is used
    as a tie-breaker.
    """

    attack_scores = np.asarray(
        attack_scores,
        dtype=np.float64,
    )

    if np.all(attack_scores == attack_scores[0]):
        threshold = float(attack_scores[0])
        predictions = (
            attack_scores >= threshold
        ).astype(np.int64)

        return threshold, calculate_metrics(
            true_labels,
            predictions,
            attack_scores,
        )

    candidates = np.unique(
        np.quantile(
            attack_scores,
            np.linspace(0.0, 1.0, 501),
        )
    )

    best_threshold = float(candidates[0])
    best_metrics = None
    best_key = (-1.0, -1.0)

    for threshold in candidates:
        predictions = (
            attack_scores >= threshold
        ).astype(np.int64)

        metrics = calculate_metrics(
            true_labels,
            predictions,
            attack_scores,
        )

        comparison_key = (
            metrics["f1"],
            metrics["balanced_accuracy"],
        )

        if comparison_key > best_key:
            best_key = comparison_key
            best_threshold = float(threshold)
            best_metrics = metrics

    return best_threshold, best_metrics


def print_attack_family_recall(
    dataframe: pd.DataFrame,
    predictions: np.ndarray,
) -> None:
    """Show detection recall for each real attack family."""

    print("\nRecall by real Friday attack family:")

    attack_types = sorted(
        dataframe.loc[
            dataframe["Label"] == 1,
            "attack_type",
        ].astype(str).unique()
    )

    for attack_type in attack_types:
        mask = (
            dataframe["attack_type"].astype(str)
            == attack_type
        ).to_numpy()

        family_recall = float(
            np.mean(predictions[mask] == 1)
        )

        print(
            f"  {attack_type:<20} "
            f"{family_recall:.4f} "
            f"({int(mask.sum()):,} flows)"
        )


# ---------------------------------------------------------------------
# Feature scaling
# ---------------------------------------------------------------------

# Random Forest and GraphSAGE use this scaler.
supervised_scaler = StandardScaler()

scaled_train_features = supervised_scaler.fit_transform(
    train_features
).astype(np.float32)

scaled_validation_features = supervised_scaler.transform(
    validation_features
).astype(np.float32)

scaled_test_features = supervised_scaler.transform(
    test_features
).astype(np.float32)


# Isolation Forest and Autoencoder are trained only on real benign flows.
benign_train_features = train_features[train_labels == 0]

anomaly_scaler = StandardScaler()

scaled_benign_train_features = anomaly_scaler.fit_transform(
    benign_train_features
).astype(np.float32)

scaled_validation_anomaly_features = anomaly_scaler.transform(
    validation_features
).astype(np.float32)

scaled_test_anomaly_features = anomaly_scaler.transform(
    test_features
).astype(np.float32)


joblib.dump(
    supervised_scaler,
    MODEL_DIRECTORY / "supervised_scaler.joblib",
)

joblib.dump(
    anomaly_scaler,
    MODEL_DIRECTORY / "anomaly_scaler.joblib",
)


# ---------------------------------------------------------------------
# Model 1: Isolation Forest
# ---------------------------------------------------------------------

print("\nTraining Isolation Forest on real benign flows...")

isolation_forest = IsolationForest(
    n_estimators=300,
    max_samples="auto",
    contamination="auto",
    random_state=RANDOM_SEED,
    n_jobs=-1,
)

isolation_forest.fit(scaled_benign_train_features)

# score_samples() is higher for normal samples.
# Negating it makes larger values mean "more likely attack".
isolation_validation_scores = -isolation_forest.score_samples(
    scaled_validation_anomaly_features
)

isolation_test_scores = -isolation_forest.score_samples(
    scaled_test_anomaly_features
)

isolation_threshold, _ = find_best_threshold(
    validation_labels,
    isolation_validation_scores,
)

isolation_validation_predictions = (
    isolation_validation_scores >= isolation_threshold
).astype(np.int64)

isolation_test_predictions = (
    isolation_test_scores >= isolation_threshold
).astype(np.int64)

isolation_metrics = calculate_metrics(
    test_labels,
    isolation_test_predictions,
    isolation_test_scores,
)

print(f"Validation threshold: {isolation_threshold:.6f}")
print_metrics("ISOLATION FOREST — REAL TEST", isolation_metrics)

joblib.dump(
    isolation_forest,
    MODEL_DIRECTORY / "isolation_forest.joblib",
)


# ---------------------------------------------------------------------
# Model 2: Random Forest
# ---------------------------------------------------------------------

print("\nTraining Random Forest on real labelled flows...")

random_forest = RandomForestClassifier(
    n_estimators=500,
    min_samples_leaf=2,
    class_weight="balanced_subsample",
    random_state=RANDOM_SEED,
    n_jobs=-1,
)

random_forest.fit(
    scaled_train_features,
    train_labels,
)

random_forest_validation_scores = random_forest.predict_proba(
    scaled_validation_features
)[:, 1]

random_forest_test_scores = random_forest.predict_proba(
    scaled_test_features
)[:, 1]

random_forest_threshold, _ = find_best_threshold(
    validation_labels,
    random_forest_validation_scores,
)

random_forest_validation_predictions = (
    random_forest_validation_scores
    >= random_forest_threshold
).astype(np.int64)

random_forest_test_predictions = (
    random_forest_test_scores
    >= random_forest_threshold
).astype(np.int64)

random_forest_metrics = calculate_metrics(
    test_labels,
    random_forest_test_predictions,
    random_forest_test_scores,
)

print(
    f"Validation threshold: "
    f"{random_forest_threshold:.6f}"
)

print_metrics(
    "RANDOM FOREST — REAL TEST",
    random_forest_metrics,
)

joblib.dump(
    random_forest,
    MODEL_DIRECTORY / "random_forest.joblib",
)


# ---------------------------------------------------------------------
# Model 3: Autoencoder
# ---------------------------------------------------------------------

class FlowAutoencoder(nn.Module):
    """Autoencoder for real benign flow reconstruction."""

    def __init__(self, input_dimension: int):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dimension, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
        )

        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, input_dimension),
        )

    def forward(self, features):
        encoded = self.encoder(features)
        return self.decoder(encoded)


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"\nTraining Autoencoder on: {device}")

autoencoder = FlowAutoencoder(
    input_dimension=len(FEATURE_COLUMNS)
).to(device)

autoencoder_optimizer = torch.optim.AdamW(
    autoencoder.parameters(),
    lr=0.001,
    weight_decay=1e-5,
)

autoencoder_loss_function = nn.MSELoss()

benign_tensor = torch.tensor(
    scaled_benign_train_features,
    dtype=torch.float32,
)

benign_loader = DataLoader(
    TensorDataset(benign_tensor),
    batch_size=256,
    shuffle=True,
)

AUTOENCODER_EPOCHS = 40

for epoch in range(1, AUTOENCODER_EPOCHS + 1):
    autoencoder.train()
    total_loss = 0.0

    for (batch_features,) in benign_loader:
        batch_features = batch_features.to(device)

        autoencoder_optimizer.zero_grad()

        reconstructed_features = autoencoder(
            batch_features
        )

        loss = autoencoder_loss_function(
            reconstructed_features,
            batch_features,
        )

        loss.backward()
        autoencoder_optimizer.step()

        total_loss += (
            loss.item() * len(batch_features)
        )

    average_loss = total_loss / len(benign_tensor)

    if epoch == 1 or epoch % 10 == 0:
        print(
            f"Autoencoder epoch {epoch:02d}/"
            f"{AUTOENCODER_EPOCHS}: "
            f"loss={average_loss:.6f}"
        )


def autoencoder_scores(
    model: nn.Module,
    features: np.ndarray,
    batch_size: int = 1024,
) -> np.ndarray:
    """Calculate reconstruction error for each flow."""

    model.eval()

    tensor = torch.tensor(
        features,
        dtype=torch.float32,
    )

    loader = DataLoader(
        TensorDataset(tensor),
        batch_size=batch_size,
        shuffle=False,
    )

    scores = []

    with torch.no_grad():
        for (batch_features,) in loader:
            batch_features = batch_features.to(device)

            reconstruction = model(batch_features)

            batch_scores = torch.mean(
                (reconstruction - batch_features) ** 2,
                dim=1,
            )

            scores.extend(
                batch_scores.cpu().numpy().tolist()
            )

    return np.asarray(scores, dtype=np.float64)


autoencoder_validation_scores = autoencoder_scores(
    autoencoder,
    scaled_validation_anomaly_features,
)

autoencoder_test_scores = autoencoder_scores(
    autoencoder,
    scaled_test_anomaly_features,
)

autoencoder_threshold, _ = find_best_threshold(
    validation_labels,
    autoencoder_validation_scores,
)

autoencoder_validation_predictions = (
    autoencoder_validation_scores >= autoencoder_threshold
).astype(np.int64)

autoencoder_test_predictions = (
    autoencoder_test_scores >= autoencoder_threshold
).astype(np.int64)

autoencoder_metrics = calculate_metrics(
    test_labels,
    autoencoder_test_predictions,
    autoencoder_test_scores,
)

print(
    f"Validation threshold: "
    f"{autoencoder_threshold:.6f}"
)

print_metrics(
    "AUTOENCODER — REAL TEST",
    autoencoder_metrics,
)

torch.save(
    {
        "state_dict": autoencoder.state_dict(),
        "input_dimension": len(FEATURE_COLUMNS),
        "feature_columns": FEATURE_COLUMNS,
    },
    MODEL_DIRECTORY / "autoencoder.pt",
)


# ---------------------------------------------------------------------
# Model 4: GraphSAGE flow-similarity graph
# ---------------------------------------------------------------------

def build_similarity_graph(
    features: np.ndarray,
    labels: np.ndarray,
    neighbors_per_node: int = 8,
) -> Data:
    """
    Build a graph where:
        node = one real CICIDS2017 flow
        edge = two flows with similar feature values
    """

    number_of_nodes = len(features)

    if number_of_nodes < 2:
        raise ValueError(
            "At least two flows are required for a graph"
        )

    neighbor_count = min(
        neighbors_per_node + 1,
        number_of_nodes,
    )

    nearest_neighbors = NearestNeighbors(
        n_neighbors=neighbor_count,
        metric="euclidean",
        algorithm="auto",
        n_jobs=-1,
    )

    nearest_neighbors.fit(features)

    neighbor_indices = nearest_neighbors.kneighbors(
        features,
        return_distance=False,
    )

    source_nodes = []
    destination_nodes = []

    for node_index, neighbors in enumerate(
        neighbor_indices
    ):
        added_neighbors = 0

        for neighbor_index in neighbors:
            if int(neighbor_index) == node_index:
                continue

            source_nodes.append(node_index)
            destination_nodes.append(
                int(neighbor_index)
            )

            # Add reverse edge.
            source_nodes.append(
                int(neighbor_index)
            )
            destination_nodes.append(node_index)

            added_neighbors += 1

            if added_neighbors >= neighbors_per_node:
                break

    edge_index = torch.tensor(
        [source_nodes, destination_nodes],
        dtype=torch.long,
    )

    node_features = torch.tensor(
        features,
        dtype=torch.float32,
    )

    node_labels = torch.tensor(
        labels,
        dtype=torch.float32,
    )

    return Data(
        x=node_features,
        edge_index=edge_index,
        y=node_labels,
    )


class FlowSimilarityGraphSAGE(nn.Module):
    """GraphSAGE binary classifier for real flow nodes."""

    def __init__(
        self,
        input_dimension: int,
        hidden_dimension: int = 64,
    ):
        super().__init__()

        self.convolution_one = SAGEConv(
            input_dimension,
            hidden_dimension,
        )

        self.convolution_two = SAGEConv(
            hidden_dimension,
            hidden_dimension,
        )

        self.classifier = nn.Linear(
            hidden_dimension,
            1,
        )

        self.dropout = nn.Dropout(0.20)

    def forward(self, node_features, edge_index):
        hidden = self.convolution_one(
            node_features,
            edge_index,
        )

        hidden = torch.relu(hidden)
        hidden = self.dropout(hidden)

        hidden = self.convolution_two(
            hidden,
            edge_index,
        )

        hidden = torch.relu(hidden)

        return self.classifier(hidden).squeeze(-1)


print("\nBuilding real flow-similarity graphs...")

training_graph = build_similarity_graph(
    scaled_train_features,
    train_labels,
)

validation_graph = build_similarity_graph(
    scaled_validation_features,
    validation_labels,
)

test_graph = build_similarity_graph(
    scaled_test_features,
    test_labels,
)

print(
    f"Training graph: "
    f"{training_graph.num_nodes:,} nodes, "
    f"{training_graph.num_edges:,} directed edges"
)

print(
    f"Validation graph: "
    f"{validation_graph.num_nodes:,} nodes, "
    f"{validation_graph.num_edges:,} directed edges"
)

print(
    f"Test graph: "
    f"{test_graph.num_nodes:,} nodes, "
    f"{test_graph.num_edges:,} directed edges"
)

training_graph = training_graph.to(device)
validation_graph = validation_graph.to(device)
test_graph = test_graph.to(device)

graphsage = FlowSimilarityGraphSAGE(
    input_dimension=len(FEATURE_COLUMNS),
    hidden_dimension=64,
).to(device)

graphsage_optimizer = torch.optim.AdamW(
    graphsage.parameters(),
    lr=0.003,
    weight_decay=5e-4,
)

graphsage_loss_function = nn.BCEWithLogitsLoss()

best_graphsage_state = None
best_validation_f1 = -1.0
epochs_without_improvement = 0

GRAPHSAGE_EPOCHS = 80
GRAPHSAGE_PATIENCE = 15

print(f"\nTraining GraphSAGE on: {device}")

for epoch in range(1, GRAPHSAGE_EPOCHS + 1):
    graphsage.train()
    graphsage_optimizer.zero_grad()

    training_logits = graphsage(
        training_graph.x,
        training_graph.edge_index,
    )

    training_loss = graphsage_loss_function(
        training_logits,
        training_graph.y,
    )

    training_loss.backward()
    graphsage_optimizer.step()

    graphsage.eval()

    with torch.no_grad():
        validation_logits = graphsage(
            validation_graph.x,
            validation_graph.edge_index,
        )

        validation_probabilities = torch.sigmoid(
            validation_logits
        ).cpu().numpy()

    validation_predictions_at_half = (
        validation_probabilities >= 0.5
    ).astype(np.int64)

    validation_f1 = f1_score(
        validation_labels,
        validation_predictions_at_half,
        zero_division=0,
    )

    if validation_f1 > best_validation_f1:
        best_validation_f1 = validation_f1
        best_graphsage_state = copy.deepcopy(
            graphsage.state_dict()
        )
        epochs_without_improvement = 0
    else:
        epochs_without_improvement += 1

    if epoch == 1 or epoch % 10 == 0:
        print(
            f"GraphSAGE epoch {epoch:02d}/"
            f"{GRAPHSAGE_EPOCHS}: "
            f"loss={training_loss.item():.6f}, "
            f"validation_f1={validation_f1:.4f}"
        )

    if epochs_without_improvement >= GRAPHSAGE_PATIENCE:
        print(
            f"Early stopping at epoch {epoch}"
        )
        break


if best_graphsage_state is None:
    raise RuntimeError(
        "GraphSAGE did not produce a valid model state"
    )

graphsage.load_state_dict(best_graphsage_state)
graphsage.eval()

with torch.no_grad():
    graphsage_validation_scores = torch.sigmoid(
        graphsage(
            validation_graph.x,
            validation_graph.edge_index,
        )
    ).cpu().numpy()

    graphsage_test_scores = torch.sigmoid(
        graphsage(
            test_graph.x,
            test_graph.edge_index,
        )
    ).cpu().numpy()


graphsage_threshold, _ = find_best_threshold(
    validation_labels,
    graphsage_validation_scores,
)

graphsage_validation_predictions = (
    graphsage_validation_scores
    >= graphsage_threshold
).astype(np.int64)

graphsage_test_predictions = (
    graphsage_test_scores
    >= graphsage_threshold
).astype(np.int64)

graphsage_metrics = calculate_metrics(
    test_labels,
    graphsage_test_predictions,
    graphsage_test_scores,
)

print(
    f"Validation threshold: "
    f"{graphsage_threshold:.6f}"
)

print_metrics(
    "GRAPHSAGE — REAL TEST",
    graphsage_metrics,
)

torch.save(
    {
        "state_dict": graphsage.state_dict(),
        "input_dimension": len(FEATURE_COLUMNS),
        "hidden_dimension": 64,
        "neighbors_per_node": 8,
        "feature_columns": FEATURE_COLUMNS,
    },
    MODEL_DIRECTORY / "graphsage_flow_similarity.pt",
)


# ---------------------------------------------------------------------
# Four-model ensemble
# ---------------------------------------------------------------------

validation_model_predictions = np.column_stack(
    [
        isolation_validation_predictions,
        random_forest_validation_predictions,
        autoencoder_validation_predictions,
        graphsage_validation_predictions,
    ]
)

test_model_predictions = np.column_stack(
    [
        isolation_test_predictions,
        random_forest_test_predictions,
        autoencoder_test_predictions,
        graphsage_test_predictions,
    ]
)

validation_vote_counts = validation_model_predictions.sum(
    axis=1
)

test_vote_counts = test_model_predictions.sum(axis=1)

best_required_votes = 1
best_ensemble_validation_key = (-1.0, -1.0)

for required_votes in range(1, 5):
    validation_ensemble_predictions = (
        validation_vote_counts >= required_votes
    ).astype(np.int64)

    validation_ensemble_metrics = calculate_metrics(
        validation_labels,
        validation_ensemble_predictions,
        validation_vote_counts / 4.0,
    )

    comparison_key = (
        validation_ensemble_metrics["f1"],
        validation_ensemble_metrics[
            "balanced_accuracy"
        ],
    )

    print(
        f"\nValidation ensemble {required_votes}-of-4: "
        f"F1={validation_ensemble_metrics['f1']:.4f}, "
        f"balanced_accuracy="
        f"{validation_ensemble_metrics['balanced_accuracy']:.4f}"
    )

    if comparison_key > best_ensemble_validation_key:
        best_ensemble_validation_key = comparison_key
        best_required_votes = required_votes


ensemble_test_predictions = (
    test_vote_counts >= best_required_votes
).astype(np.int64)

ensemble_test_scores = test_vote_counts / 4.0

ensemble_metrics = calculate_metrics(
    test_labels,
    ensemble_test_predictions,
    ensemble_test_scores,
)

print(
    f"\nSelected ensemble rule using validation data: "
    f"{best_required_votes}-of-4 models"
)

print_metrics(
    "FOUR-MODEL ENSEMBLE — REAL TEST",
    ensemble_metrics,
)

print_attack_family_recall(
    test_dataframe,
    ensemble_test_predictions,
)


# ---------------------------------------------------------------------
# Save thresholds and metrics
# ---------------------------------------------------------------------

thresholds = {
    "isolation_forest": float(isolation_threshold),
    "random_forest": float(random_forest_threshold),
    "autoencoder": float(autoencoder_threshold),
    "graphsage": float(graphsage_threshold),
    "ensemble_required_votes": int(best_required_votes),
}

all_metrics = {
    "dataset": {
        "training_rows": int(len(train_labels)),
        "validation_rows": int(len(validation_labels)),
        "testing_rows": int(len(test_labels)),
        "test_benign_rows": int(
            np.sum(test_labels == 0)
        ),
        "test_attack_rows": int(
            np.sum(test_labels == 1)
        ),
    },
    "isolation_forest": isolation_metrics,
    "random_forest": random_forest_metrics,
    "autoencoder": autoencoder_metrics,
    "graphsage": graphsage_metrics,
    "four_model_ensemble": ensemble_metrics,
    "thresholds": thresholds,
}

with open(
    MODEL_DIRECTORY / "thresholds.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(thresholds, file, indent=2)

with open(
    DOCUMENT_DIRECTORY / "real_only_metrics.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(all_metrics, file, indent=2)


print("\n===== REAL-ONLY EVALUATION COMPLETE =====")
print(
    f"Models saved to: {MODEL_DIRECTORY}"
)
print(
    f"Metrics saved to: "
    f"{DOCUMENT_DIRECTORY / 'real_only_metrics.json'}"
)
