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
async def analyze_flows(
    offset: int = 0,
    limit: int = 100,
    persist: bool = False,
):
    """
    Analyze captured flows in manageable batches.

    persist=false:
        Score flows without inserting alerts into PostgreSQL.

    persist=true:
        Score flows and save detected anomalies as alerts.
    """

    if offset < 0:
        raise HTTPException(
            status_code=400,
            detail="offset must be zero or greater",
        )

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    all_flows = read_all_flows()
    flows = all_flows[offset:offset + limit]

    anomalies = 0
    persisted_alerts = 0

    for flow in flows:
        features = normalize_flow(flow)

        feature_row = [
            features.get(column, 0.0)
            for column in FEATURE_COLUMNS
        ]

        result = detector.score(feature_row)

        if result["is_anomaly"]:
            anomalies += 1

            if persist:
                await create_alert(flow, result)
                persisted_alerts += 1

    next_offset = offset + len(flows)

    return {
        "total_available_flows": len(all_flows),
        "offset": offset,
        "analyzed": len(flows),
        "anomalies_detected": anomalies,
        "persisted_alerts": persisted_alerts,
        "next_offset": (
            next_offset
            if next_offset < len(all_flows)
            else None
        ),
    }


@app.get("/alerts")
async def list_alerts():
    return await get_all_alerts()


@app.get("/alerts/{alert_id}")
async def get_alert(alert_id: str):
    alert = await get_alert_by_id(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.get("/metrics/model")
def model_metrics():
    """Snapshot of the held-out evaluation verified on 2026-07-17."""
    return {
        "evaluated_on": "2026-07-17",
        "test_rows": 940,
        "attacks": 110,
        "benign": 830,
        "isolation_forest": {
            "accuracy": 0.9511,
            "precision": 0.7254,
            "recall": 0.9364,
            "f1": 0.8175,
            "contamination": 0.05,
        },
        "random_forest": {
            "accuracy": 0.9521,
            "classes": ["BENIGN", "DDoS", "PortScan"],
        },
        "autoencoder": {
            "accuracy": 0.9415,
            "precision": 0.7068,
            "recall": 0.8545,
            "f1": 0.7737,
            "threshold": detector.ae_threshold,
        },
        "ensemble": {
            "accuracy": 0.9894,
            "precision": 0.9630,
            "recall": 0.9455,
            "f1": 0.9541,
            "false_positives": 4,
            "false_negatives": 6,
        },
        "ensemble_rule": "2 of 3 models must agree",
    }


@app.post("/analyse/real")
async def analyse_real_attack():
    '''runs the same ensemble used on synthtic data , but agaist real captured attck traffic '''
    import json ,os
    real_path=os.path.join(os.path.dirname(__file__),"..","..""data","real_attck_flows.jsonl")
    if not os.path.exists(real_path):
        raise HTTPException(status_code=404, detail="Real attack data not found ")

    flows=[]
    with open(real_path) as f:
        for line in f:
            if line.strip():
                flows.append(json.loads(line))

    results = []
    for flow in flows:
        features = normalize_flow(flow)
        feature_row = [features.get(col, 0.0) for col in FEATURE_COLUMNS]
        result = detector.score(feature_row)
        results.append({"flow": flow, "result": result})
        if result["is_anomaly"]:
            await create_alert(flow, result)

    detected = sum(1 for r in results if r["result"]["is_anomaly"])
    return {
            "total_real_flows": len(flows),
            "detected_as_anomaly": detected,
            "detection_rate": round(detected / max(len(flows), 1), 2),
            "note": "This is real nmap SYN scan traffic, not synthetic data.",
}

# FlowGuard real-data shadow endpoint
from app.routes.real_analysis import router as real_analysis_router
app.include_router(real_analysis_router)

# FlowGuard legacy-versus-real comparison endpoint
from app.ml.real_only_predictor import RealOnlyRandomForestPredictor

comparison_real_predictor = RealOnlyRandomForestPredictor()


@app.post("/analyze/compare")
async def compare_detection_models(
    limit: int = 100,
):
    """
    Run the legacy ensemble and real-data Random Forest on the same
    recent flows.

    This endpoint never persists alerts. It is for shadow comparison only.
    """

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    all_flows = read_all_flows()
    flows = all_flows[-limit:]

    start_line = max(
        1,
        len(all_flows) - len(flows) + 1,
    )

    results = []

    legacy_alerts = 0
    real_rf_alerts = 0

    both_alert = 0
    both_benign = 0
    legacy_only = 0
    real_rf_only = 0

    errors = []

    for position, flow in enumerate(
        flows,
        start=start_line,
    ):
        try:
            normalized_features = normalize_flow(flow)

            legacy_feature_row = [
                normalized_features.get(column, 0.0)
                for column in FEATURE_COLUMNS
            ]

            legacy_result = detector.score_flow(
                legacy_feature_row
            )

            real_result = (
                comparison_real_predictor.predict(flow)
            )

            legacy_is_alert = bool(
                legacy_result.get("alert", False)
            )

            real_is_alert = bool(
                real_result["alert"]
            )

            legacy_alerts += int(legacy_is_alert)
            real_rf_alerts += int(real_is_alert)

            if legacy_is_alert and real_is_alert:
                agreement_type = "both_alert"
                both_alert += 1

            elif not legacy_is_alert and not real_is_alert:
                agreement_type = "both_benign"
                both_benign += 1

            elif legacy_is_alert:
                agreement_type = "legacy_only"
                legacy_only += 1

            else:
                agreement_type = "real_rf_only"
                real_rf_only += 1

            results.append(
                {
                    "line": position,
                    "src_ip": flow.get("src_ip"),
                    "dst_ip": flow.get("dst_ip"),
                    "src_port": flow.get("src_port"),
                    "dst_port": flow.get("dst_port"),
                    "protocol": flow.get("protocol"),
                    "legacy_alert": legacy_is_alert,
                    "real_rf_alert": real_is_alert,
                    "agreement": agreement_type,
                    "real_rf_probability": (
                        real_result["attack_probability"]
                    ),
                    "real_rf_threshold": (
                        real_result["threshold"]
                    ),
                    "real_rf_operational_mode": (
                        real_result["operational_mode"]
                    ),
                }
            )

        except Exception as error:
            errors.append(
                {
                    "line": position,
                    "error": str(error),
                }
            )

    analyzed = len(results)

    agreements = both_alert + both_benign

    agreement_rate = (
        agreements / analyzed
        if analyzed
        else 0.0
    )

    return {
        "mode": "compare-shadow",
        "total_available_flows": len(all_flows),
        "requested": limit,
        "analyzed": analyzed,
        "errors": len(errors),
        "legacy_alerts": legacy_alerts,
        "real_rf_alerts": real_rf_alerts,
        "agreement": {
            "both_alert": both_alert,
            "both_benign": both_benign,
            "legacy_only": legacy_only,
            "real_rf_only": real_rf_only,
            "agreement_rate": round(
                agreement_rate,
                6,
            ),
        },
        "persistence_enabled": False,
        "results": results,
        "error_details": errors[:20],
        "warning": (
            "These are model comparisons, not verified attack labels."
        ),
    }

