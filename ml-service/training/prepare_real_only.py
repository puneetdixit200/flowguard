"""
Create real-only FlowGuard train, validation, and test datasets.

No synthetic rows are generated.

Capture-day split:
    Monday–Wednesday -> training
    Thursday         -> validation
    Friday           -> final testing

Each output split is balanced between BENIGN and ATTACK so that accuracy
cannot become artificially high by predicting the majority class.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CICIDS_ROOT = PROJECT_ROOT.parent / "data" / "cicids2017"
OUTPUT_ROOT = PROJECT_ROOT / "data" / "real_only"

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
CHUNK_SIZE = 100_000

RAW_COLUMNS = {
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
}

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

SPLITS = {
    "train": {
        "files": [
            "Monday-WorkingHours.pcap_ISCX.csv",
            "Tuesday-WorkingHours.pcap_ISCX.csv",
            "Wednesday-workingHours.pcap_ISCX.csv",
        ],
        "benign_target": 10_000,
        "attack_target": 10_000,
    },
    "validation": {
        "files": [
            "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
            "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
        ],
        "benign_target": 2_000,
        "attack_target": 2_000,
    },
    "test": {
        "files": [
            "Friday-WorkingHours-Morning.pcap_ISCX.csv",
            "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
            "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
        ],
        "benign_target": 5_000,
        "attack_target": 5_000,
    },
}


def convert_chunk(raw: pd.DataFrame) -> pd.DataFrame:
    """Convert CICIDS2017 columns into FlowGuard's eleven features."""

    raw.columns = [str(column).strip() for column in raw.columns]

    labels = raw["Label"].astype(str).str.strip()

    numeric_names = [column for column in RAW_COLUMNS if column != "Label"]

    for column in numeric_names:
        raw[column] = pd.to_numeric(raw[column], errors="coerce")

    output = pd.DataFrame()

    output["duration_seconds"] = raw["Flow Duration"] / 1_000_000.0

    output["packet_count"] = (
        raw["Total Fwd Packets"] +
        raw["Total Backward Packets"]
    )

    output["total_bytes"] = (
        raw["Total Length of Fwd Packets"] +
        raw["Total Length of Bwd Packets"]
    )

    output["bytes_per_sec"] = raw["Flow Bytes/s"]
    output["packets_per_sec"] = raw["Flow Packets/s"]

    output["syn_count"] = raw["SYN Flag Count"]
    output["ack_count"] = raw["ACK Flag Count"]
    output["fin_count"] = raw["FIN Flag Count"]
    output["rst_count"] = raw["RST Flag Count"]

    output["syn_ack_ratio"] = (
        output["syn_count"] /
        (output["ack_count"] + 1.0)
    )

    output["rst_ratio"] = (
        output["rst_count"] /
        (output["packet_count"] + 1.0)
    )

    # Preserve the exact CICIDS attack name for later analysis.
    output["attack_type"] = labels

    # Binary classification:
    # 0 = BENIGN
    # 1 = any attack family
    output["Label"] = (labels != "BENIGN").astype(np.int64)

    output.replace([np.inf, -np.inf], np.nan, inplace=True)
    output.dropna(subset=FEATURE_COLUMNS, inplace=True)

    # Remove physically impossible negative values.
    valid_rows = (output[FEATURE_COLUMNS] >= 0).all(axis=1)
    output = output.loc[valid_rows].copy()

    output[FEATURE_COLUMNS] = output[FEATURE_COLUMNS].astype(np.float32)

    return output


def update_reservoir(
    current: pd.DataFrame | None,
    candidates: pd.DataFrame,
    target_size: int,
    random_generator: np.random.Generator,
) -> pd.DataFrame | None:
    """
    Keep a deterministic random sample without loading an entire capture
    file into memory.
    """

    if candidates.empty:
        return current

    candidates = candidates.copy()
    candidates["_sample_key"] = random_generator.random(len(candidates))

    if current is None:
        combined = candidates
    else:
        combined = pd.concat([current, candidates], ignore_index=True)

    if len(combined) > target_size:
        combined = combined.nsmallest(target_size, "_sample_key")

    return combined


def create_split(
    split_name: str,
    file_names: list[str],
    benign_target: int,
    attack_target: int,
) -> pd.DataFrame:
    """Create one balanced real-data split."""

    random_generator = np.random.default_rng(
        RANDOM_SEED + sum(ord(character) for character in split_name)
    )

    benign_reservoir = None
    attack_reservoir = None

    print(f"\n===== BUILDING {split_name.upper()} SPLIT =====")

    for file_name in file_names:
        path = CICIDS_ROOT / file_name

        if not path.exists():
            raise FileNotFoundError(f"Missing CICIDS file: {path}")

        print(f"Reading: {file_name}")

        for raw_chunk in pd.read_csv(
            path,
            chunksize=CHUNK_SIZE,
            low_memory=False,
            usecols=lambda column: str(column).strip() in RAW_COLUMNS,
        ):
            converted = convert_chunk(raw_chunk)

            benign_rows = converted[converted["Label"] == 0]
            attack_rows = converted[converted["Label"] == 1]

            benign_reservoir = update_reservoir(
                benign_reservoir,
                benign_rows,
                benign_target,
                random_generator,
            )

            attack_reservoir = update_reservoir(
                attack_reservoir,
                attack_rows,
                attack_target,
                random_generator,
            )

    if benign_reservoir is None:
        raise RuntimeError(f"No benign rows found for {split_name}")

    if attack_reservoir is None:
        raise RuntimeError(f"No attack rows found for {split_name}")

    benign_reservoir.drop(columns="_sample_key", inplace=True)
    attack_reservoir.drop(columns="_sample_key", inplace=True)

    result = pd.concat(
        [benign_reservoir, attack_reservoir],
        ignore_index=True,
    )

    result = result.sample(
        frac=1.0,
        random_state=RANDOM_SEED,
    ).reset_index(drop=True)

    print(f"Rows selected: {len(result):,}")
    print("Binary labels:")
    print(result["Label"].value_counts().sort_index().to_string())

    print("Attack types:")
    print(
        result.loc[result["Label"] == 1, "attack_type"]
        .value_counts()
        .to_string()
    )

    return result


def main() -> None:
    for split_name, configuration in SPLITS.items():
        dataset = create_split(
            split_name=split_name,
            file_names=configuration["files"],
            benign_target=configuration["benign_target"],
            attack_target=configuration["attack_target"],
        )

        output_path = OUTPUT_ROOT / f"{split_name}_real.csv"
        dataset.to_csv(output_path, index=False)

        print(f"Saved: {output_path}")

    print("\n===== REAL-ONLY DATASET PREPARATION COMPLETE =====")
    print(f"Training rows:   {sum(1 for _ in open(OUTPUT_ROOT / 'train_real.csv')) - 1:,}")
    print(f"Validation rows: {sum(1 for _ in open(OUTPUT_ROOT / 'validation_real.csv')) - 1:,}")
    print(f"Testing rows:    {sum(1 for _ in open(OUTPUT_ROOT / 'test_real.csv')) - 1:,}")


if __name__ == "__main__":
    main()
