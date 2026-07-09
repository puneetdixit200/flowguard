"""
Generates a synthetic flow dataset shaped like real CICIDS2017 output.
UPDATED: now includes overlapping ranges and noisy/borderline samples so the
dataset is NOT trivially separable — this is what makes accuracy meaningful. [file:1]
"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)
N_NORMAL = 4000
N_ATTACK = 400
N_BORDERLINE = 300  # NEW: ambiguous samples that look like attacks but aren't, and vice versa

def make_normal_rows(n):
    return pd.DataFrame({
        "duration_seconds": np.random.uniform(0.1, 5.0, n),
        "packet_count": np.random.randint(5, 80, n),          # widened range, overlaps attacks
        "total_bytes": np.random.randint(500, 8000, n),        # widened range
        "bytes_per_sec": np.random.uniform(100, 3000, n),       # widened, now overlaps low-end attacks
        "packets_per_sec": np.random.uniform(1, 200, n),        # widened — some bursty normal traffic
        "syn_count": np.random.randint(0, 8, n),
        "ack_count": np.random.randint(3, 40, n),
        "fin_count": np.random.randint(0, 2, n),
        "rst_count": np.random.randint(0, 5, n),               # some normal retries cause resets
        "syn_ack_ratio": np.random.uniform(0.0, 1.5, n),        # overlaps low-end attack ratio
        "rst_ratio": np.random.uniform(0.0, 0.15, n),
        "Label": "BENIGN",
    })

def make_attack_rows(n, label, seed_offset):
    rng = np.random.default_rng(42 + seed_offset)
    return pd.DataFrame({
        "duration_seconds": rng.uniform(0.01, 2.0, n),          # overlaps normal duration
        "packet_count": rng.integers(60, 2000, n),              # overlaps normal upper range
        "total_bytes": rng.integers(1000, 20000, n),
        "bytes_per_sec": rng.uniform(500, 50000, n),            # overlaps normal upper range
        "packets_per_sec": rng.uniform(100, 5000, n),           # overlaps normal upper range
        "syn_count": rng.integers(5, 500, n),                   # overlaps normal upper range
        "ack_count": rng.integers(1, 30, n),                    # overlaps normal
        "fin_count": rng.integers(0, 3, n),
        "rst_count": rng.integers(1, 200, n),                   # overlaps normal upper range
        "syn_ack_ratio": rng.uniform(0.8, 50.0, n),             # overlaps normal upper range
        "rst_ratio": rng.uniform(0.1, 0.9, n),                  # overlaps normal upper range
        "Label": label,
    })

def make_borderline_rows(n):
    """
    NEW: creates genuinely ambiguous flows — some are mislabeled-looking normal
    traffic with attack-like bursts (false positive bait), and some are slow/stealthy
    attacks that look mostly normal (false negative bait). Real detection systems
    must handle exactly this kind of ambiguity.
    """
    rng = np.random.default_rng(999)
    half = n // 2

    noisy_normal = pd.DataFrame({
        "duration_seconds": rng.uniform(0.05, 1.0, half),
        "packet_count": rng.integers(50, 150, half),
        "total_bytes": rng.integers(4000, 9000, half),
        "bytes_per_sec": rng.uniform(2000, 6000, half),
        "packets_per_sec": rng.uniform(80, 300, half),
        "syn_count": rng.integers(3, 10, half),
        "ack_count": rng.integers(10, 30, half),
        "fin_count": rng.integers(0, 2, half),
        "rst_count": rng.integers(0, 6, half),
        "syn_ack_ratio": rng.uniform(0.3, 1.2, half),
        "rst_ratio": rng.uniform(0.05, 0.2, half),
        "Label": "BENIGN",
    })

    stealthy_attack = pd.DataFrame({
        "duration_seconds": rng.uniform(1.0, 4.0, n - half),
        "packet_count": rng.integers(20, 60, n - half),
        "total_bytes": rng.integers(1000, 4000, n - half),
        "bytes_per_sec": rng.uniform(300, 1500, n - half),
        "packets_per_sec": rng.uniform(10, 60, n - half),
        "syn_count": rng.integers(4, 15, n - half),
        "ack_count": rng.integers(2, 10, n - half),
        "fin_count": rng.integers(0, 2, n - half),
        "rst_count": rng.integers(2, 10, n - half),
        "syn_ack_ratio": rng.uniform(0.8, 2.5, n - half),
        "rst_ratio": rng.uniform(0.1, 0.35, n - half),
        "Label": "PortScan",
    })

    return pd.concat([noisy_normal, stealthy_attack], ignore_index=True)

def main():
    normal = make_normal_rows(N_NORMAL)
    ddos = make_attack_rows(N_ATTACK // 2, "DDoS", 1)
    portscan = make_attack_rows(N_ATTACK // 2, "PortScan", 2)
    borderline = make_borderline_rows(N_BORDERLINE)

    df = pd.concat([normal, ddos, portscan, borderline], ignore_index=True)

    # Add small random noise to every numeric column so no two rows are
    # identical and the model can't just memorize exact values.
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    noise = np.random.normal(0, 0.02, df[numeric_cols].shape) * df[numeric_cols].std().values
    df[numeric_cols] = df[numeric_cols] + noise
    df[numeric_cols] = df[numeric_cols].clip(lower=0)  # no negative counts/bytes

    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    output_path = "../data/sample/sample_features.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows -> {output_path}")
    print(df["Label"].value_counts())

if __name__ == "__main__":
    main()
