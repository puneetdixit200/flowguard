"""
Honest, full evaluation report across ALL THREE models plus the ensemble.
Everything runs on test_holdout.csv — data none of the models saw during
training — so these numbers are trustworthy, not inflated. [web:54]
"""
import pandas as pd
from pathlib import Path
import numpy as np
import joblib
import torch
from sklearn.metrics import (
    classification_report, confusion_matrix, f1_score,
    accuracy_score, precision_score, recall_score
)

from prepare_cicids_data import FEATURE_COLUMNS
from app.ml.autoencoder_def import Autoencoder

def load_all_models():
    project_root = Path(__file__).resolve().parents[1]
    models_dir = project_root / "app" / "models"

    scaler = joblib.load(models_dir / "scaler.joblib")
    iso_forest = joblib.load(models_dir / "isolation_forest.joblib")
    rf_model = joblib.load(models_dir / "random_forest.joblib")
    encoder = joblib.load(models_dir / "label_encoder.joblib")
    ae_meta = joblib.load(models_dir / "autoencoder_meta.joblib")

    autoencoder = Autoencoder(ae_meta["input_dim"])
    autoencoder.load_state_dict(
        torch.load(models_dir / "autoencoder.pt", map_location="cpu")
    )
    autoencoder.eval()

    return (
        scaler,
        iso_forest,
        rf_model,
        encoder,
        autoencoder,
        ae_meta["threshold"],
    )

def evaluate_isolation_forest(iso_forest, scaler, X, y_true_binary):
    """Isolation Forest only knows normal vs anomaly, not attack types."""
    X_scaled = scaler.transform(X)
    preds = iso_forest.predict(X_scaled)          # -1 = anomaly, 1 = normal
    preds_binary = (preds == -1).astype(int)        # convert to 0/1

    print("\n=== ISOLATION FOREST (unsupervised, binary anomaly detection) ===")
    print(f"Accuracy:  {accuracy_score(y_true_binary, preds_binary):.4f}")
    print(f"Precision: {precision_score(y_true_binary, preds_binary, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_true_binary, preds_binary, zero_division=0):.4f}")
    print(f"F1:        {f1_score(y_true_binary, preds_binary, zero_division=0):.4f}")
    print("Confusion matrix [rows=actual, cols=predicted] (0=normal,1=anomaly):")
    print(confusion_matrix(y_true_binary, preds_binary))
    return preds_binary

def evaluate_random_forest(rf_model, encoder, X, y_true_multiclass):
    """Random Forest gives per-class detail — DDoS vs PortScan vs Benign."""
    preds = rf_model.predict(X)

    print("\n=== RANDOM FOREST (supervised, multi-class) ===")
    print(f"Accuracy: {accuracy_score(y_true_multiclass, preds):.4f}")
    print(classification_report(y_true_multiclass, preds, target_names=encoder.classes_, zero_division=0))
    print("Confusion matrix:")
    print(confusion_matrix(y_true_multiclass, preds))
    return preds

def evaluate_autoencoder(autoencoder, scaler, threshold, X, y_true_binary):
    """Autoencoder flags anomalies via reconstruction error vs a fixed threshold."""
    X_scaled = scaler.transform(X)
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)

    with torch.no_grad():
        reconstructed = autoencoder(X_tensor)
        errors = torch.mean((reconstructed - X_tensor) ** 2, dim=1).numpy()

    preds_binary = (errors > threshold).astype(int)

    print("\n=== AUTOENCODER (deep learning, reconstruction-error anomaly) ===")
    print(f"Threshold used: {threshold:.6f}")
    print(f"Accuracy:  {accuracy_score(y_true_binary, preds_binary):.4f}")
    print(f"Precision: {precision_score(y_true_binary, preds_binary, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_true_binary, preds_binary, zero_division=0):.4f}")
    print(f"F1:        {f1_score(y_true_binary, preds_binary, zero_division=0):.4f}")
    print("Confusion matrix:")
    print(confusion_matrix(y_true_binary, preds_binary))
    return preds_binary

def evaluate_ensemble(iso_preds, rf_is_attack, ae_preds, y_true_binary):
    """The 2-of-3 vote rule, scored against the same held-out labels."""
    votes = iso_preds + rf_is_attack + ae_preds  # each is 0 or 1 per row
    ensemble_preds = (votes >= 2).astype(int)

    print("\n=== ENSEMBLE (2-of-3 vote across all three models) ===")
    print(f"Accuracy:  {accuracy_score(y_true_binary, ensemble_preds):.4f}")
    print(f"Precision: {precision_score(y_true_binary, ensemble_preds, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_true_binary, ensemble_preds, zero_division=0):.4f}")
    print(f"F1:        {f1_score(y_true_binary, ensemble_preds, zero_division=0):.4f}")
    print("Confusion matrix:")
    print(confusion_matrix(y_true_binary, ensemble_preds))

    fp_count = ((ensemble_preds == 1) & (y_true_binary == 0)).sum()
    fn_count = ((ensemble_preds == 0) & (y_true_binary == 1)).sum()
    print(f"\nFalse positives: {fp_count} | False negatives: {fn_count}")
    print("These numbers are your honest failure cases — document them in docs/false-positive-analysis.md")

def main():
    project_root = Path(__file__).resolve().parents[1]
    test_data_path = project_root / "data" / "sample" / "test_holdout.csv"
    df = pd.read_csv(test_data_path)
    X = df[FEATURE_COLUMNS]

    scaler, iso_forest, rf_model, encoder, autoencoder, threshold = load_all_models()

    y_true_multiclass = encoder.transform(df["Label"])
    y_true_binary = (df["Label"].str.upper() != "BENIGN").astype(int).values

    print(f"Evaluating on {len(df)} UNSEEN test rows ({(y_true_binary==1).sum()} attacks, {(y_true_binary==0).sum()} benign)")

    iso_preds = evaluate_isolation_forest(iso_forest, scaler, X, y_true_binary)
    rf_preds = evaluate_random_forest(rf_model, encoder, X, y_true_multiclass)
    rf_is_attack = (encoder.inverse_transform(rf_preds) != "BENIGN").astype(int)
    ae_preds = evaluate_autoencoder(autoencoder, scaler, threshold, X, y_true_binary)

    evaluate_ensemble(iso_preds, rf_is_attack, ae_preds, y_true_binary)

if __name__ == "__main__":
    main()
