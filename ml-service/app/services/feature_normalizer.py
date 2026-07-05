from app.services.alert_service import create_alert, get_alert_by_id, get_all_alerts
from app.services.detector import score_flow
from app.services.feature_normalizer import normalize_flow
from app.services.flow_reader import read_all_flows
from fastapi import FastAPI, HTTPException

app = FastAPI(title="FlowGuard API")

# Matches the Layer 5 API surface from your dossier. [file:1]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/flows/recent")
def get_recent_flows(limit: int = 20):
    flows = read_all_flows()
    return flows[-limit:]


@app.post("/analyze")
def analyze_flows():
    """Runs the baseline detector over all captured flows and stores alerts."""
    flows = read_all_flows()
    new_alerts = []

    for flow in flows:
        features = normalize_flow(flow)
        score = score_flow(features)
        if score["is_anomaly"]:
            alert = create_alert(flow, score)
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
