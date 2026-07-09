"""
Generates a synthetic flow dataset shaped like real CICIDS2017 output.
This lets you run train_isolation_forest.py, train_random_forest.py, and
train_autoencoder.py immediately, without downloading the 48GB real dataset.
Replace this with real CICIDS2017 later using prepare_cicids_data.py. [file:1]
"""

import os

import numpy as np
import pandas as pd

np.random.seed(42)
N_NORMAL = 4000
N_ATTACK = (
    400  # attacks are rarer than normal traffic, matching real-world class imbalance
)


def make_normal_rows(n):
    return pd.DataFrame(
        {
            "duration_seconds": np.random.uniform(0.1, 5.0, n),
            "packet_count": np.random.randint(5, 50, n),
            "total_bytes": np.random.randint(500, 5000, n),
            "bytes_per_sec": np.random.uniform(100, 2000, n),
            "packets_per_sec": np.random.uniform(1, 30, n),
            "syn_count": np.random.randint(0, 3, n),
            "ack_count": np.random.randint(5, 40, n),
            "fin_count": np.random.randint(0, 2, n),
            "rst_count": np.random.randint(0, 1, n),
            "syn_ack_ratio": np.random.uniform(0.0, 0.3, n),
            "rst_ratio": np.random.uniform(0.0, 0.05, n),
            "Label": "BENIGN",
        }
    )


def make_attack_rows(n, label, seed_offset):
    # Attacks get exaggerated features: high packet rate, high SYN/ACK ratio, high RST ratio.
    rng = np.random.default_rng(42 + seed_offset)
    return pd.DataFrame(
        {
            "duration_seconds": rng.uniform(0.01, 1.0, n),
            "packet_count": rng.integers(200, 2000, n),
            "total_bytes": rng.integers(1000, 20000, n),
            "bytes_per_sec": rng.uniform(2000, 50000, n),
            "packets_per_sec": rng.uniform(500, 5000, n),
            "syn_count": rng.integers(50, 500, n),
            "ack_count": rng.integers(1, 10, n),
            "fin_count": rng.integers(0, 2, n),
            "rst_count": rng.integers(20, 200, n),
            "syn_ack_ratio": rng.uniform(5.0, 50.0, n),
            "rst_ratio": rng.uniform(0.4, 0.9, n),
            "Label": label,
        }
    )


def main():
    normal = make_normal_rows(N_NORMAL)
    ddos = make_attack_rows(N_ATTACK // 2, "DDoS", 1)
    portscan = make_attack_rows(N_ATTACK // 2, "PortScan", 2)

    df = pd.concat([normal, ddos, portscan], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle

    output_path = "../data/sample/sample_features.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows -> {output_path}")
    print(df["Label"].value_counts())


if __name__ == "__main__":
    main()
