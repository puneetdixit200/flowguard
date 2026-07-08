"""combine isloation forest , reandom forst and autoencdoer votes"""

"""
Rule per dossier: if 2 of 3 models flag anomaly -> alert = true.
Severity bands: 50-70=low, 70-85=medium, 85-95=high, 95+=critical. [file:1]"""

import os
from lzma import MODE_FAST
from multiprocessing.managers import Server
from winreg import SetValue

import joblib
import numpy as np
import torch
from app.ml.autoencoder_def import Autoencoder
from numpy._core.multiarray import _reconstruct

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


class EnsembleDetector:
    def __init__(self):
        # load evething once at startup
        self.scalar = joblib.load(os.path.join(MODEL_DIR, "autoencoder_meta.joblib"))
        self.iso_forest = joblib.load(os.path.join(MODEL_DIR, "iso_forest.joblib"))
        self.rf_forest = joblib.load(os.path.join(MODEL_DIR, "rf_forest.joblib"))
        self.label_encoder = joblib.load(
            os.path.join(MODEL_DIR, "label_encoder.joblib")
        )

        ae_meta = joblib.load(os.path.join(MODEL_DIR, "autoencoder_meta.joblib"))
        self.ae_thresshold = ae_meta["threshold"]
        self.autoencoder = Autoencoder(ae_meta["imput_dim"])
        self.autoencoder.load_state_dict(
            torch.load(os.path.join(MODEL_DIR, "autoencoder.pt"))
        )
        self.autoencoder.eval()

    def score(self, feature_row: list[float]) -> dict:
        """
        feature_row must be in the exact same order as FEATURE_COLUMNS
        used during training — order mismatches silently break predictions.
        """
        X = np.array(feature_row).reshape(1, -1)
        X_scaled = self.scalar.transform(X)
        votes = 0
        details = {}
        # vote 1 by islation forest

        iso_pred = self.iso_forest.predict(X_scaled)[0]
        iso_anomaly = iso_pred == -1
        votes += int(iso_anomaly)
        details["iso_forest"] = "anomaly" if iso_anomaly else "normal"

        # vote 2 by random forest

        rf_pred_idx = self.rf_model.predict(X)[0]
        rf_label = self.label_encoder.inverse_transform([rf_pred_idx])[0]
        rf_anomaly = rf_label.upper() == "BENIGN"
        votes += int(rf_anomaly)
        details["rf_forest"] = rf_label

        # vote 3 by autoencoder

        with torch.no_grad():
            X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
            reconstructed = self.autoencoder(X_tensor)
            error = torch.mean((reconstructed - X_tensor) ** 2).item()
        ae_anomaly = error > self.ae_thresshold
        votes += int(ae_anomaly)
        details["autoencoder"] = round(error, 6)

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
