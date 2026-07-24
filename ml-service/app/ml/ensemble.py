# ml-service/app/ml/ensemble.py
"""
CHANGES:
1. RF threshold is now a configurable value (from tune_rf_threshold.py),
   not the default 0.5 — set OPERATIONAL_MODE below.
2. GNN is now actually loaded and voted, closing the gap where it sat
   trained-but-unused.
3. Ensemble vote is now 2-of-4 (was 2-of-3) since GNN is wired in.
"""
import joblib
import torch
from app.ml.autoencoder_def import Autoencoder

# Set based on tune_rf_threshold.py output — pick per deployment need.
OPERATIONAL_MODE = "balanced"  # "balanced" | "high_recall" | "high_precision"
RF_THRESHOLDS = {
    "balanced": 0.50,       # replace with your actual best-F1 threshold from item 2
    "high_recall": 0.30,    # replace with your actual high-recall threshold
    "high_precision": 0.70, # replace with your actual high-precision threshold
}

class Ensemble:
    def __init__(self, model_dir="app/models"):
        self.model_dir = model_dir
        self.scaler = joblib.load(f"{model_dir}/scaler.joblib")
        self.iso_forest = joblib.load(f"{model_dir}/isolation_forest.joblib")
        self.rf = joblib.load(f"{model_dir}/random_forest.joblib")
        self.label_encoder = joblib.load(f"{model_dir}/label_encoder.joblib")

        self.autoencoder = Autoencoder(input_dim=11)
        self.autoencoder.load_state_dict(torch.load(f"{model_dir}/autoencoder.pt"))
        self.autoencoder.eval()
        ae_meta = joblib.load(f"{model_dir}/autoencoder_meta.joblib")
        self.ae_threshold = ae_meta["threshold"]

        # The API's common path has no graph context, so defer the optional
        # PyG model until graph scoring is actually requested.
        self.gnn = None
        self.rf_threshold = RF_THRESHOLDS[OPERATIONAL_MODE]

    def _load_gnn(self):
        if self.gnn is not None:
            return

        from app.ml.gnn_model import FlowGraphSAGE

        gnn_checkpoint_path = f"{self.model_dir}/gnn_graphsage.pt"
        gnn_state_dict = torch.load(
            gnn_checkpoint_path,
            map_location="cpu",
        )

        # Infer the input feature count directly from the saved checkpoint.
        gnn_input_channels = int(
            gnn_state_dict["conv1.lin_l.weight"].shape[1]
        )

        self.gnn = FlowGraphSAGE(
            in_channels=gnn_input_channels
        )

        self.gnn.load_state_dict(gnn_state_dict)
        self.gnn.eval()

    def score_flow(self, flow_features, graph_context=None):
        X = self.scaler.transform([flow_features])

        # --- Isolation Forest vote ---
        iso_pred = self.iso_forest.predict(X)[0]
        iso_vote = 1 if iso_pred == -1 else 0

        # --- Random Forest vote, using tuned threshold instead of default 0.5 ---
        proba = self.rf.predict_proba(X)[0]
        benign_idx = list(self.label_encoder.classes_).index("BENIGN")
        attack_proba = 1 - proba[benign_idx]
        rf_vote = 1 if attack_proba >= self.rf_threshold else 0
        rf_label = self.label_encoder.inverse_transform([self.rf.predict(X)[0]])[0]

        # --- Autoencoder vote ---
        with torch.no_grad():
            x_tensor = torch.tensor(X, dtype=torch.float32)
            reconstructed = self.autoencoder(x_tensor)
            error = torch.mean((x_tensor - reconstructed) ** 2).item()
        ae_vote = 1 if error > self.ae_threshold else 0

        # --- GNN vote (NEW: only if graph context/node embedding is provided) ---
        gnn_vote = 0
        if graph_context is not None:
            self._load_gnn()
            with torch.no_grad():
                out = self.gnn(graph_context["x"], graph_context["edge_index"])
                node_idx = graph_context["node_idx"]
                gnn_vote = int(out[node_idx].argmax().item())

        votes = [iso_vote, rf_vote, ae_vote, gnn_vote]
        alert = sum(votes) >= 2  # 2-of-4 majority, now that GNN participates

        return {
            "alert": alert,
            "votes": {"isolation_forest": iso_vote, "random_forest": rf_vote,
                      "autoencoder": ae_vote, "gnn": gnn_vote},
            "rf_predicted_class": rf_label,
            "attack_probability": float(attack_proba),
            "autoencoder_error": float(error),
            "rf_threshold_used": self.rf_threshold,
            "operational_mode": OPERATIONAL_MODE,
        }

    def score(self, flow_features):
        """Return the API/alert contract for the three standalone models."""
        result = self.score_flow(flow_features)
        model_votes = result["votes"]
        vote_count = sum(
            model_votes[name]
            for name in ("isolation_forest", "random_forest", "autoencoder")
        )
        confidence = vote_count / 3
        is_anomaly = bool(result["alert"])

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
            "votes": vote_count,
            "confidence": confidence,
            "severity": severity,
            "predicted_class": result["rf_predicted_class"],
            "details": {
                "isolation_forest": (
                    "anomaly"
                    if model_votes["isolation_forest"]
                    else "normal"
                ),
                "random_forest": result["rf_predicted_class"],
                "autoencoder_error": result["autoencoder_error"],
            },
        }

# Backward-compatible class name expected by app.main
EnsembleDetector = Ensemble
