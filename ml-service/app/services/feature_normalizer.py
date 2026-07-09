def normalize_flow(flow: dict) -> dict:
    """
    Convert a raw flow dictionary into normalized/derived features.

    Keeps identity fields:
    - src_ip
    - dst_ip
    - protocol

    Adds ML features:
    - bytes_per_sec
    - packets_per_sec
    - syn_ack_ratio
    - rst_ratio
    """

    duration = max(float(flow.get("duration_seconds", 0.0001)), 0.0001)
    packets = int(flow.get("packet_count", 0))
    total_bytes = int(flow.get("total_bytes", 0))

    syn_count = int(flow.get("syn_count", 0))
    ack_count = int(flow.get("ack_count", 0))
    fin_count = int(flow.get("fin_count", 0))
    rst_count = int(flow.get("rst_count", 0))

    return {
        "src_ip": flow.get("src_ip"),
        "dst_ip": flow.get("dst_ip"),
        "protocol": flow.get("protocol"),

        "duration_seconds": duration,
        "packet_count": packets,
        "total_bytes": total_bytes,

        "bytes_per_sec": total_bytes / duration,
        "packets_per_sec": packets / duration,

        "syn_count": syn_count,
        "ack_count": ack_count,
        "fin_count": fin_count,
        "rst_count": rst_count,

        "syn_ack_ratio": syn_count / max(ack_count, 1),
        "rst_ratio": rst_count / max(packets, 1),
    }
