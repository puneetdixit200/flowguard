FEATURE_COLUMNS = [
    "duration_seconds",
    "packet_count",
    "total_bytes",
    "bytes_per_sec",
    "packets_per_sec",
    "syn_count",
    "ack_count",
    "fin_count",
    "rst_count",
    "syn_ack_ratio",
    "rst_ratio",
]

LABEL_COLUMN = "Label"

if __name__ == "__main__":
    print("FEATURE_COLUMNS:")
    for col in FEATURE_COLUMNS:
        print("-", col)
