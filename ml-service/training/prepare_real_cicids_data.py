"""
Convert CICIDS2017 CSV files into the feature format expected by FlowGuard.

Input:
    flowguard/data/cicids2017/*.csv

Output:
    flowguard/ml-service/data/cicids2017/real_test_set.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd


ML_SERVICE_ROOT = Path(__file__).resolve().parents[1]
FLOWGUARD_ROOT = ML_SERVICE_ROOT.parent

SOURCE_DIRECTORY = FLOWGUARD_ROOT / "data" / "cicids2017"
OUTPUT_DIRECTORY = ML_SERVICE_ROOT / "data" / "cicids2017"
OUTPUT_FILE = OUTPUT_DIRECTORY / "real_test_set.csv"


REQUIRED_COLUMNS = [
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Flow Bytes/s",
    "Flow Packets/s",
    "SYN Flag Count",
    "ACK Flag Count",
    "FIN Flag Count",
    "RST Flag Count",
    "Label",
]


def convert_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """
    Convert one CICIDS2017 chunk into the FlowGuard feature schema.
    """

    # CICIDS column names often contain leading or trailing spaces.
    chunk.columns = chunk.columns.str.strip()

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in chunk.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing CICIDS columns: "
            + ", ".join(missing_columns)
        )

    def numeric(column_name: str) -> pd.Series:
        return pd.to_numeric(
            chunk[column_name],
            errors="coerce",
        )

    # CICIDS Flow Duration is measured in microseconds.
    duration_seconds = numeric("Flow Duration") / 1_000_000.0

    packet_count = (
        numeric("Total Fwd Packets")
        + numeric("Total Backward Packets")
    )

    total_bytes = (
        numeric("Total Length of Fwd Packets")
        + numeric("Total Length of Bwd Packets")
    )

    result = pd.DataFrame(
        {
            "duration_seconds": duration_seconds,
            "packet_count": packet_count,
            "total_bytes": total_bytes,
            "bytes_per_sec": numeric("Flow Bytes/s"),
            "packets_per_sec": numeric("Flow Packets/s"),
            "syn_count": numeric("SYN Flag Count"),
            "ack_count": numeric("ACK Flag Count"),
            "fin_count": numeric("FIN Flag Count"),
            "rst_count": numeric("RST Flag Count"),
            "Label": chunk["Label"].astype(str).str.strip(),
        }
    )

    # Avoid division by zero.
    safe_ack_count = result["ack_count"].replace(0, 1)
    safe_packet_count = result["packet_count"].replace(0, 1)

    result["syn_ack_ratio"] = (
        result["syn_count"] / safe_ack_count
    )

    result["rst_ratio"] = (
        result["rst_count"] / safe_packet_count
    )

    # Remove broken real-world rows containing infinity or missing values.
    result = result.replace(
        [np.inf, -np.inf],
        np.nan,
    ).dropna()

    result = result[result["packet_count"] > 0]

    return result[
        [
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
            "Label",
        ]
    ]


def main() -> None:
    csv_files = sorted(SOURCE_DIRECTORY.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CICIDS CSV files found in {SOURCE_DIRECTORY}"
        )

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Remove an older output before writing the new dataset.
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    first_write = True
    total_rows = 0
    benign_rows = 0
    attack_rows = 0

    for csv_file in csv_files:
        print(f"\nReading: {csv_file.name}")

        file_rows = 0

        # Read in chunks so the full multi-million-row dataset does not
        # have to remain in RAM simultaneously.
        for chunk in pd.read_csv(
            csv_file,
            chunksize=100_000,
            low_memory=False,
        ):
            converted = convert_chunk(chunk)

            converted.to_csv(
                OUTPUT_FILE,
                mode="w" if first_write else "a",
                header=first_write,
                index=False,
            )

            first_write = False

            rows = len(converted)
            benign = int(
                converted["Label"]
                .str.upper()
                .eq("BENIGN")
                .sum()
            )

            total_rows += rows
            file_rows += rows
            benign_rows += benign
            attack_rows += rows - benign

            print(
                f"  Processed {file_rows:,} clean rows",
                end="\r",
            )

        print(f"  Finished with {file_rows:,} clean rows")

    print("\n===== CICIDS2017 PREPARATION COMPLETE =====")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Total clean rows: {total_rows:,}")
    print(f"Benign rows: {benign_rows:,}")
    print(f"Attack rows: {attack_rows:,}")


if __name__ == "__main__":
    main()
