import itertools
from datetime import datetime, timezone

_alert_id_counter = itertools.count(1)
_alerts_store = []


def create_alert(flow: dict, result: dict) -> dict:
    alert = {
        "id": next(_alert_id_counter),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "src_ip": flow.get("src_ip"),
        "dst_ip": flow.get("dst_ip"),
        "protocol": flow.get("protocol"),
        "severity": result["severity"],
        "confidence": result["confidence"],
        "predicted_class": result.get("predicted_class"),
        "votes": result.get("votes"),
        "details": result.get("details"),
        "source": "ensemble-model",
    }
    _alerts_store.append(alert)
    return alert


def get_all_alerts():
    return list(reversed(_alerts_store))  # newest first


def get_alert_by_id(alert_id: int):
    return next((a for a in _alerts_store if a["id"] == alert_id), None)
