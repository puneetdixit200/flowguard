"""
Live predictor using FlowGuard's verified real-data Random Forest.

The model was:
- trained on real CICIDS2017 Monday-Wednesday traffic,
- tuned using Thursday validation traffic,
- evaluated on untouched Friday traffic.

This module performs inference only. Live flows do not have ground-truth
labels, so its output cannot be treated as a new accuracy measurement.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import joblib
import numpy as np


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

APP_DIRECTORY = Path(__file__).resolve().parents[1]
MODEL_DIRECTORY = APP_DIRECTORY / "models" / "real_only"

SCALER_PATH = MODEL_DIRECTORY / "supervised_scaler.joblib"
MODEL_PATH = MODEL_DIRECTORY / "random_forest.joblib"
THRESHOLDS_PATH = MODEL_DIRECTORY / "thresholds.json"
OPERATIONAL_THRESHOLDS_PATH = (
    MODEL_DIRECTORY / "rf_operational_thresholds.json"
)


class RealOnlyRandomForestPredictor:
    """Load and run the verified real-data Random Forest."""

    def __init__(self) -> None:
        required_files = [
            SCALER_PATH,
            MODEL_PATH,
            OPERATIONAL_THRESHOLDS_PATH,
        ]

        missing_files = [
            str(path)
            for path in required_files
            if not path.exists()
        ]

        if missing_files:
            raise FileNotFoundError(
                "Missing real-only model files:\n"
                + "\n".join(missing_files)
            )

        self.scaler = joblib.load(SCALER_PATH)
        self.model = joblib.load(MODEL_PATH)

        with OPERATIONAL_THRESHOLDS_PATH.open(
            "r",
            encoding="utf-8",
        ) as threshold_file:
            threshold_configuration = json.load(
                threshold_file
            )

        self.operational_mode = os.getenv(
            "RF_OPERATIONAL_MODE",
            "balanced",
        ).strip().lower()

        available_modes = threshold_configuration[
            "thresholds"
        ]

        if self.operational_mode not in available_modes:
            raise ValueError(
                f"Unknown RF_OPERATIONAL_MODE: "
                f"{self.operational_mode}. "
                f"Available modes: "
                f"{sorted(available_modes)}"
            )

        self.threshold = float(
            available_modes[self.operational_mode]
        )

        model_classes = list(self.model.classes_)

        if 1 not in model_classes:
            raise ValueError(
                f"Attack class 1 is absent from model classes: "
                f"{model_classes}"
            )

        self.attack_class_index = model_classes.index(1)

    @staticmethod
    def _feature_vector(
        flow: dict[str, Any],
    ) -> np.ndarray:
        """
        Build the eleven model features.

        The C++ capture output stores basic counters. Rate and ratio
        features are calculated here when they are not already present.
        """

        required_base_features = [
            "duration_seconds",
            "packet_count",
            "total_bytes",
            "syn_count",
            "ack_count",
            "fin_count",
            "rst_count",
        ]

        missing_features = [
            feature
            for feature in required_base_features
            if feature not in flow
        ]

        if missing_features:
            raise KeyError(
                "Flow is missing required base features: "
                + ", ".join(missing_features)
            )

        duration_seconds = float(flow["duration_seconds"])
        packet_count = float(flow["packet_count"])
        total_bytes = float(flow["total_bytes"])

        syn_count = float(flow["syn_count"])
        ack_count = float(flow["ack_count"])
        fin_count = float(flow["fin_count"])
        rst_count = float(flow["rst_count"])

        # Avoid division by zero for extremely short or empty flows.
        bytes_per_sec = float(
            flow.get(
                "bytes_per_sec",
                total_bytes / duration_seconds
                if duration_seconds > 0
                else 0.0,
            )
        )

        packets_per_sec = float(
            flow.get(
                "packets_per_sec",
                packet_count / duration_seconds
                if duration_seconds > 0
                else 0.0,
            )
        )

        syn_ack_ratio = float(
            flow.get(
                "syn_ack_ratio",
                syn_count / (ack_count + 1.0),
            )
        )

        rst_ratio = float(
            flow.get(
                "rst_ratio",
                rst_count / (packet_count + 1.0),
            )
        )

        feature_values = {
            "duration_seconds": duration_seconds,
            "packet_count": packet_count,
            "total_bytes": total_bytes,
            "bytes_per_sec": bytes_per_sec,
            "packets_per_sec": packets_per_sec,
            "syn_count": syn_count,
            "ack_count": ack_count,
            "fin_count": fin_count,
            "rst_count": rst_count,
            "syn_ack_ratio": syn_ack_ratio,
            "rst_ratio": rst_ratio,
        }

        for feature_name, value in feature_values.items():
            if not np.isfinite(value):
                raise ValueError(
                    f"Feature {feature_name} is not finite: {value}"
                )

        ordered_values = [
            feature_values[feature_name]
            for feature_name in FEATURE_COLUMNS
        ]

        return np.asarray(
            [ordered_values],
            dtype=np.float32,
        )

    def predict(
        self,
        flow: dict[str, Any],
    ) -> dict[str, Any]:
        """Return the Random Forest attack decision and probability."""

        raw_features = self._feature_vector(flow)
        scaled_features = self.scaler.transform(raw_features)

        probabilities = self.model.predict_proba(
            scaled_features
        )[0]

        attack_probability = float(
            probabilities[self.attack_class_index]
        )

        alert = attack_probability >= self.threshold

        return {
            "alert": bool(alert),
            "predicted_label": (
                "ATTACK" if alert else "BENIGN"
            ),
            "attack_probability": round(
                attack_probability,
                6,
            ),
            "threshold": round(
                self.threshold,
                6,
            ),
            "operational_mode": self.operational_mode,
            "model": "real_only_random_forest",
        }


def test_jsonl(
    jsonl_path: Path,
    maximum_flows: int,
) -> None:
    """Score several flows from an existing FlowGuard JSONL file."""

    predictor = RealOnlyRandomForestPredictor()

    scored_flows = 0

    with jsonl_path.open(
        "r",
        encoding="utf-8",
    ) as flow_file:
        for line_number, line in enumerate(
            flow_file,
            start=1,
        ):
            if not line.strip():
                continue

            try:
                flow = json.loads(line)
                result = predictor.predict(flow)

                print(
                    json.dumps(
                        {
                            "line": line_number,
                            "src_ip": flow.get("src_ip"),
                            "dst_ip": flow.get("dst_ip"),
                            **result,
                        },
                        indent=2,
                    )
                )

                scored_flows += 1

                if scored_flows >= maximum_flows:
                    break

            except Exception as error:
                print(
                    f"Skipped line {line_number}: {error}",
                    file=sys.stderr,
                )

    if scored_flows == 0:
        raise RuntimeError(
            "No compatible flows were scored."
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(
            "Usage: python -m app.ml.real_only_predictor "
            "<flows.jsonl> [maximum_flows]"
        )

    input_path = Path(sys.argv[1])
    maximum = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    test_jsonl(input_path, maximum)
