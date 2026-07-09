import os
import joblib
import torch
import numpy as np

from app.ml.autoencoder_def import Autoencoder

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


class EnsembleDetector:
    def __init__(self):
        self.scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.joblib"))

        self.iso_forest = joblib.load(
            os.path.join(MODEL_DIR, "isolation_forest.joblib")
        )

        self.rf_model = joblib.load(
            os.path.join(MODEL_DIR, "random_forest.joblib")
        )

        self.label_encoder = joblib.load(
            os.path.join(MODEL_DIR, "label_encoder.joblib")
        )

        ae_meta = joblib.load(
            os.path.join(MODEL_DIR, "autoencoder_meta.joblib")
        )

        self.ae_threshold = ae_meta["threshold"]

        self.autoencoder = Autoencoder(ae_meta["input_dim"])

        state_dict = torch.load(
            os.path.join(MODEL_DIR, "autoencoder.pt"),
            map_location="cpu"
        )

        self.autoencoder.load_state_dict(state_dict)
        self.autoencoder.eval()

    def score(self, feature_row: list[float]) -> dict:
        X = np.array(feature_row, dtype=float).reshape(1, -1)
        X_scaled = self.scaler.transform(X)

        votes = 0
        details = {}

        iso_pred = self.iso_forest.predict(X_scaled)[0]
        iso_anomaly = iso_pred == -1
        votes += int(iso_anomaly)
        details["isolation_forest"] = "anomaly" if iso_anomaly else "normal"

        rf_pred_idx = self.rf_model.predict(X)[0]
        rf_label = self.label_encoder.inverse_transform([rf_pred_idx])[0]
        rf_anomaly = rf_label.upper() != "BENIGN"
        votes += int(rf_anomaly)
        details["random_forest"] = rf_label

        with torch.no_grad():
            X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
            reconstructed = self.autoencoder(X_tensor)
            error = torch.mean((reconstructed - X_tensor) ** 2).item()

        ae_anomaly = error > self.ae_threshold
        votes += int(ae_anomaly)
        details["autoencoder_error"] = round(error, 6)

        is_anomaly = votes >= 2
        confidence = votes / 3.0

        if confidence >= 0.95:
            severity = "critical"
        elif confidence >= 0.85:
            severity = "high"
        elif confidence >= 0.70:
            severity = "medium"
        elif is_anomaly:
            severity = "low"
        else:
            severity = "none"

        return {
            "is_anomaly": is_anomaly,
            "votes": votes,
            "confidence": round(confidence, 2),
            "severity": severity,
            "predicted_class": rf_label,
            "details": details,
        }
