# Baseline rule-based anomaly detector.
# This is intentionally simple — it proves the pipeline works end to end
# before swapping in Isolation Forest / Random Forest / Autoencoder. [file:1]

RULES = {
    "high_packet_rate": 500,  # packets/sec threshold
    "high_syn_ack_ratio": 5.0,  # possible SYN flood / scan
    "high_rst_ratio": 0.5,  # many resets = possible scan
}


def score_flow(features: dict) -> dict:
    reasons = []

    if features["packets_per_sec"] > RULES["high_packet_rate"]:
        reasons.append("high_packet_rate")

    if features["syn_ack_ratio"] > RULES["high_syn_ack_ratio"]:
        reasons.append("high_syn_ack_ratio")

    if features["rst_ratio"] > RULES["high_rst_ratio"]:
        reasons.append("high_rst_ratio")

    is_anomaly = len(reasons) > 0
    confidence = min(len(reasons) / len(RULES), 1.0)

    if confidence >= 0.85:
        severity = "critical"
    elif confidence >= 0.7:
        severity = "high"
    elif confidence >= 0.5:
        severity = "medium"
    elif is_anomaly:
        severity = "low"
    else:
        severity = "none"

    return {
        "is_anomaly": is_anomaly,
        "confidence": confidence,
        "severity": severity,
        "reasons": reasons,
    }
