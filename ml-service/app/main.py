from app.ml.ensemble import EnsembleDetector
from app.services.alert_service import create_alert, get_alert_by_id, get_all_alerts
from app.services.feature_normalizer import normalize_flow
from app.services.flow_reader import read_all_flows
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prepare_cicids_data import FEATURE_COLUMNS  # same order used in training

app = FastAPI(title="FlowGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load all 3 models ONCE at startup, not per-request — this is a real production pattern.
detector = EnsembleDetector()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/flows/recent")
def get_recent_flows(limit: int = 20):
    flows = read_all_flows()
    return flows[-limit:]


@app.post("/analyze")
def analyze_flows():
    """
    Runs the full ensemble (Isolation Forest + Random Forest + Autoencoder)
    over every captured flow and stores an alert for each anomaly found.
    """
    flows = read_all_flows()
    new_alerts = []

    for flow in flows:
        features = normalize_flow(flow)
        # Build the feature vector in the EXACT training column order.
        feature_row = [features.get(col, 0.0) for col in FEATURE_COLUMNS]

        result = detector.score(feature_row)
        if result["is_anomaly"]:
            alert = create_alert(flow, result)
            new_alerts.append(alert)

    return {"analyzed": len(flows), "new_alerts": len(new_alerts)}


@app.get("/alerts")
def list_alerts():
    return get_all_alerts()


@app.get("/alerts/{alert_id}")
def get_alert(alert_id: int):
    alert = get_alert_by_id(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.get("/metrics/model")
def model_metrics():
    """Static metrics summary — replace with real evaluate_models.py output later."""
    return {
        "isolation_forest": {"contamination": 0.05},
        "random_forest": {"n_estimators": 300},
        "autoencoder": {"threshold": detector.ae_threshold},
        "ensemble_rule": "2 of 3 models must agree",
    }
