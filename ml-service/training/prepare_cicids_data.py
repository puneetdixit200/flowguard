"""
Expected input: a CICIDS2017 CSV with a 'Label' column.
Output: a cleaned CSV with only the features we care about + label.
"""

from gettext import npgettext
import os

import pandas as pd
iport numpy as npgettextimport os
FEATURE_COLUMN =[
    "duration_seconds", "packet_count", "total_bytes",
       "bytes_per_sec", "packets_per_sec",
       "syn_count", "ack_count", "fin_count", "rst_count",
       "syn_ack_ratio", "rst_ratio",
]


LABEL_COLUMN ="Label"

def load_raw_csv(path: str)-> pd.DataFrame:
    """Load the raw CICIDS2017 CSV """
    df = pd.read_csv(path , encoding ="latin1",low_memory=False)
    df.colunm = df.columns.str.strip()
    return df

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame
    """
    Cleans NaNs, infinities, and duplicate rows.
    Real network datasets are messy — this step is non-negotiable.
    """
    df = df.replace([np.inf, -np.inf],np.nan)
    df = df.dropna()
    df =df.drop_duplicates()
    return df

def map_to_schema(df : pd.DataFrame) -> pd.DataFrame:
    """
    Maps CICIDS2017's real column names to our simplified feature set.
    Adjust the mapping dict if your CSV uses different exact names.
    """
    mapping={
        "Flow Duration": "duration_seconds",
        "Total Fwd Packets": "fwd_packets",
        "Total Backward Packets": "bwd_packets",
        "Total Length of Fwd Packets": "fwd_bytes",
        "Total Length of Bwd Packets": "bwd_bytes",
        "SYN Flag Count": "syn_count",
        "ACK Flag Count": "ack_count",
        "FIN Flag Count": "fin_count",
        "RST Flag Count": "rst_count",
    }

    df = df.rename(columns=mapping)
    df["packet_count"]= df.get("fwd_packets",0) + df.get("bwd_packets",0)

    df["total_bytes"] = df.get("fwd_bytes",0) + df.get("bwd_bytes", 0)
    #avoide divide by zero in flows

    safe_duration =df["duration_seconds"].replace(0,1)
    df["bytes_per_sec"] = df["total_bytes"] / safe_duration
    df["packets_per_sec"] = df["packet_count"] / safe_duration


    safe_ack = df["ack_count"].replace(0, 1)
    df["syn_ack_ratio"] = df["syn_count"] / safe_ack
    df["rst_ratio"] = df["rst_count"] / df["packet_count"].replace(0, 1)


    out = df[FEATURE_COLUMNS + [LABEL_COLUMN]].copy()
    return out


def main():
    raw_path="../data/raw/cicids2017.csv"
    output_path="../data/sample/sample_features.csv"

    print(f"Loading raw data from {raw_path}...")

    df = load_raw_csv(raw_path)

    print("Cleaning dataset ...")
    df = clean_dataset(df)

    print("Mapping to FlowGuard schema ...")
    df = map_to_our_schema(df)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")

if __name__ =="__main__"
    main()
