"""
UPDATED: alerts are now persisted in PostgreSQL via Prisma (not in-memory),
broadcast live via Redis, checked against threat intel, and given a
human-readable explanation built from the ensemble's individual verdicts.
"""
from datetime import datetime, timezone
from app.db import get_prisma
from app.storage.redis_client import publish_alert, cache_recent_alert_count
from app.services.threat_intel_service import check_ip

def build_explanation(result: dict) -> str:
    """
    Converts raw model output into a sentence a human analyst can read
    without knowing anything about Isolation Forest or autoencoders.
    """
    reasons = []
    details = result.get("details", {})

    if details.get("isolation_forest") == "anomaly":
        reasons.append("statistical outlier vs. normal traffic baseline")
    if details.get("random_forest") not in (None, "BENIGN"):
        reasons.append(f"classified as '{details.get('random_forest')}' pattern")
    ae_error = details.get("autoencoder_error", 0)
    if ae_error:
        reasons.append(f"reconstruction error {ae_error:.4f} (unusual shape)")

    if not reasons:
        return "No individual model flagged strong signals; borderline case."

    return f"Flagged by {result['votes']}/3 models: " + "; ".join(reasons) + "."

async def create_alert(flow: dict, result: dict) -> dict:
    prisma = await get_prisma()

    #threat check on both sooruce and destion ip

    src_intel = await check_ip(flow.get("src_ip"))
    dst_intel = await check_ip(flow.get("dst_ip"))

    intel_matched = src_intel["note"] or dst_intel["note"]
    details = result.get("details", {})

    alert=await prisma.alert.create(data={
        "srcIp": flow.get("src_ip"),
        "dstIp": flow.get("dst_ip"),
        "protocol": flow.get("protocol"),
        "severity": result["severity"],
        "confidence": result["confidence"],
        "votes": result["votes"],
        "predictedClass": result.get("predicted_class", "unknown"),
        "isoForestVerdict": details.get("isolation_forest", "unknown"),
        "rfVerdict": details.get("random_forest", "unknown"),
        "aeReconError": details.get("autoencoder_error", 0.0),
        "explanation": explanation,
        "threatIntelMatch": intel_matched,
        "threatIntelNote": intel_note,
    })

    alert_dict={
        "id": alert.id, "src_ip": alert.srcIp, "dst_ip": alert.dstIp,
              "severity": alert.severity, "confidence": alert.confidence,
              "votes": alert.votes, "explanation": alert.explanation,
              "threat_intel_match": alert.threatIntelMatch,
              "threat_intel_note": alert.threatIntelNote,
              "timestamp": alert.createdAt.isoformat(),


    }
    publish_alert(alert_dict)  # publish the alert to the redis channel
    cache_recent_alert_count()  # increment the alert count in redis

    return alert_dict

async def get_recent_alert_count():
    prisma = await get_prisma()
    alerts = await prisma.alert.find_many(order_by={"createdAt": "desc"}, take =100)
    return alerts

async def get_alert_by_id(alert_id: str):
    prisma = await get_prisma()
    alert = await prisma.alert.find_unique(where={"id": alert_id})
    return alert
