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

    intel_matched = bool(src_intel.get("matched") or dst_intel.get("matched"))
    intel_note = src_intel["note"] or dst_intel["note"] or ""
    details = result.get("details", {})
    explanation = build_explanation(result)

    alert=await prisma.alert.create(data={
        "srcIP": flow.get("src_ip"),
        "dstIP": flow.get("dst_ip"),
        "protocol": flow.get("protocol"),
        "severity": result["severity"],
        "confidence": str(result.get("confidence", "unknown")),
        "votes": result["votes"],
        "predictedClass": result.get("predicted_class", "unknown"),
        "isoForestVerdict": details.get("isolation_forest", "unknown"),
        "rfVerdict": details.get("random_forest", "unknown"),
        "aeReconError": details.get("autoencoder_error", 0.0),
        "explanation": explanation,
        "threatIntelMatch": intel_matched,
        "threatIntelNote": intel_note,
    })
    await prisma.disconnect()

    alert_dict={
        "id": alert.id, "src_ip": alert.srcIP, "dst_ip": alert.dstIP,
              "severity": alert.severity, "confidence": alert.confidence,
              "votes": alert.votes, "explanation": alert.explanation,
              "threat_intel_match": alert.threatIntelMatch,
              "threat_intel_note": alert.threatIntelNote,
              "timestamp": alert.createdAt.isoformat(),


    }
    publish_alert(alert_dict)  # publish the alert to the redis channel
    cache_recent_alert_count()  # increment the alert count in redis

    return alert_dict

def serialize_alert(alert) -> dict:
    return {
        "id": alert.id,
        "src_ip": alert.srcIP,
        "dst_ip": alert.dstIP,
        "protocol": alert.protocol,
        "severity": alert.severity,
        "confidence": float(alert.confidence),
        "votes": alert.votes,
        "predicted_class": alert.predictedClass,
        "explanation": alert.explanation,
        "threat_intel_match": alert.threatIntelMatch,
        "threat_intel_note": alert.threatIntelNote,
        "timestamp": alert.createdAt.isoformat(),
    }

async def get_all_alerts():
    prisma = await get_prisma()
    alerts = await prisma.alert.find_many(order={"createdAt": "desc"}, take=100)
    await prisma.disconnect()
    return [serialize_alert(alert) for alert in alerts]

async def get_alert_by_id(alert_id: str):
    prisma = await get_prisma()
    try:
        alert_pk = int(alert_id)
    except ValueError:
        await prisma.disconnect()
        return None

    alert = await prisma.alert.find_unique(where={"id": alert_pk})
    await prisma.disconnect()
    return serialize_alert(alert) if alert else None
