
Training Isolation Forest on real benign flows...
Validation threshold: 0.329398

===== ISOLATION FOREST — REAL TEST =====
Accuracy:          0.6251
Balanced accuracy: 0.6251
Precision:         0.5721
Recall:            0.9926
F1:                0.7259
ROC-AUC:           0.6558
Confusion matrix:
[[1288 3712]
 [  37 4963]]

Training Random Forest on real labelled flows...
Validation threshold: 0.023552

===== RANDOM FOREST — REAL TEST =====
Accuracy:          0.8609
Balanced accuracy: 0.8609
Precision:         0.7871
Recall:            0.9894
F1:                0.8767
ROC-AUC:           0.9036
Confusion matrix:
[[3662 1338]
 [  53 4947]]

Training Autoencoder on: cpu
Autoencoder epoch 01/40: loss=0.991777
Autoencoder epoch 10/40: loss=0.065146
Autoencoder epoch 20/40: loss=0.014158
Autoencoder epoch 30/40: loss=0.011380
Autoencoder epoch 40/40: loss=0.010787
Validation threshold: 0.000875

===== AUTOENCODER — REAL TEST =====
Accuracy:          0.7586
Balanced accuracy: 0.7586
Precision:         0.7311
Recall:            0.8180
F1:                0.7721
ROC-AUC:           0.7765
Confusion matrix:
[[3496 1504]
 [ 910 4090]]

Building real flow-similarity graphs...
Training graph: 20,000 nodes, 320,000 directed edges
Validation graph: 4,000 nodes, 64,000 directed edges
Test graph: 10,000 nodes, 160,000 directed edges

Training GraphSAGE on: cpu
GraphSAGE epoch 01/80: loss=0.717868, validation_f1=0.6695
GraphSAGE epoch 10/80: loss=0.476546, validation_f1=0.0026
Early stopping at epoch 17
Validation threshold: 0.511871

===== GRAPHSAGE — REAL TEST =====
Accuracy:          0.5539
Balanced accuracy: 0.5539
Precision:         0.5285
Recall:            0.9988
F1:                0.6913
ROC-AUC:           0.7303
Confusion matrix:
[[ 545 4455]
 [   6 4994]]

Validation ensemble 1-of-4: F1=0.6667, balanced_accuracy=0.5000

Validation ensemble 2-of-4: F1=0.7235, balanced_accuracy=0.6182

Validation ensemble 3-of-4: F1=0.8134, balanced_accuracy=0.7742

Validation ensemble 4-of-4: F1=0.8553, balanced_accuracy=0.8553

Selected ensemble rule using validation data: 4-of-4 models

===== FOUR-MODEL ENSEMBLE — REAL TEST =====
Accuracy:          0.8471
Balanced accuracy: 0.8471
Precision:         0.8696
Recall:            0.8166
F1:                0.8423
ROC-AUC:           0.9015
Confusion matrix:
[[4388  612]
 [ 917 4083]]

Recall by real Friday attack family:
  Bot                  0.0227 (44 flows)
  DDoS                 0.8499 (2,152 flows)
  PortScan             0.8035 (2,804 flows)

===== REAL-ONLY EVALUATION COMPLETE =====
Models saved to: /home/pd/Downloads/flowguard/ml-service/app/models/real_only
Metrics saved to: /home/pd/Downloads/flowguard/docs/real_only_metrics.json

flowguard/ml-service main ? ❯ find /home/pd/Downloads/flowguard/ml-service/app/models/real_only \
  -maxdepth 1 -type f -printf '%f\n' | sort
anomaly_scaler.joblib
autoencoder.pt
graphsage_flow_similarity.pt
isolation_forest.joblib
random_forest.joblib
supervised_scaler.joblib
thresholds.json

You have now completed a real-only machine-learning evaluation using labelled CICIDS2017 network traffic.
Verified real-data results
Model	Accuracy	Precision	Recall	F1	ROC-AUC
Isolation Forest	62.51%	57.21%	99.26%	72.59%	65.58%
Random Forest	86.09%	78.71%	98.94%	87.67%	90.36%
Autoencoder	75.86%	73.11%	81.80%	77.21%	77.65%
GraphSAGE	55.39%	52.85%	99.88%	69.13%	73.03%
Four-model ensemble	84.71%	86.96%	81.66%	84.23%	90.15%

Your test set was balanced:

5,000 real benign flows
5,000 real attack flows

Therefore, the reported accuracy is meaningful and matches balanced accuracy.
Main conclusion

The Random Forest is currently your strongest overall detector:

Accuracy: 86.09%
Recall:   98.94%
F1:       87.67%

The four-model ensemble did not beat it in accuracy or F1:

Random Forest accuracy: 86.09%
Ensemble accuracy:      84.71%

However, the ensemble produced much fewer false positives:

Random Forest:
False positives: 1,338
False negatives:    53

Four-model ensemble:
False positives:   612
False negatives:   917

So the ensemble is more conservative:

fewer false alarms
but
more missed attacks

That is why its precision is higher at 86.96%, while recall falls to 81.66%.
Real attack-family performance

The ensemble detected:

DDoS:      84.99%
PortScan:  80.35%
Bot:        2.27%

Bot detection is currently the largest weakness. Only one of the 44 Bot flows was detected.

The low Bot result is understandable because:

    Bot was absent from the Monday–Wednesday training attacks.

    Only 44 Bot flows appeared in the test sample.

    Bot behaviour can differ significantly from DoS and brute-force traffic.

Important GraphSAGE finding

GraphSAGE achieved:

Accuracy: 55.39%
Recall:   99.88%

That means it classified almost every attack correctly, but also marked most benign flows as attacks:

True negatives:    545
False positives: 4,455
False negatives:     6
True positives:  4,994

Therefore, do not claim that GraphSAGE improved accuracy. It currently behaves like a very sensitive anomaly detector.

Also describe it accurately as:

    A GraphSAGE flow-similarity graph where real CICIDS2017 flows are nodes and nearest-neighbour feature relationships form edges.

Do not describe it as an IP communication graph because the CICIDS CSV files lacked source and destination IP addresses.
Resume-safe project wording
Strong resume bullet

    Trained and evaluated four intrusion-detection models on capture-day-separated CICIDS2017 traffic, achieving 86.1% accuracy, 98.9% recall, and 0.877 F1 with Random Forest on an untouched balanced test set of 10,000 real network flows.

Ensemble bullet

    Designed a four-model ensemble combining Random Forest, Isolation Forest, a PyTorch Autoencoder, and GraphSAGE, achieving 84.7% real-traffic accuracy and 87.0% precision while reducing false positives from 1,338 to 612 compared with the standalone Random Forest.

Evaluation-methodology bullet

    Prevented train-test leakage using capture-day separation: Monday–Wednesday for training, Thursday for threshold validation, and Friday for final testing across previously unseen DDoS, PortScan, and Bot attack families.

What you can now claim

You can honestly say:

    All four machine-learning models were trained and tested using real CICIDS2017 flows.

    Thresholds and ensemble rules were selected using separate real validation data.

    Final accuracy was measured on an untouched real Friday test split.

    The test set contained attack families not present in training.

    Random Forest achieved the best overall performance.

    The ensemble reduced false positives but sacrificed recall.

You should not say:

    The four-model ensemble achieved 98.9% real-data accuracy.

    GraphSAGE improved ensemble accuracy.

    The models achieved 86% accuracy on your infected-Android PCAP.

    The eBPF/XDP path is faster than libpcap.

The infected-Android PCAP still lacks per-flow ground-truth labels, and the eBPF-versus-libpcap performance benchmark is still pending.
Final verified headline

    FlowGuard achieved 86.09% accuracy, 98.94% recall, 78.71% precision, and 0.8767 F1 using Random Forest on 10,000 real, labelled, capture-day-separated CICIDS2017 flows.


Today 10:13 PM
mkae  a md file what all we conclude and how

Created the Markdown file with the complete methodology, results, conclusions, honest resume claims, limitations, and next improvements.


Pasted markdown(1).md
File
 help me execute next step

The next step should be to wire the verified real-data Random Forest into the live pipeline first.

Do not replace ensemble.py with the uploaded example yet. That example loads the old model directory, uses the earlier two-feature GNN, contains placeholder thresholds, and changes voting to 2-of-4, while your real validation selected 4-of-4.
1. Create a safe real-model predictor

Run this entire block:

cat > /home/pd/Downloads/flowguard/ml-service/app/ml/real_only_predictor.py <<'PY'
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


class RealOnlyRandomForestPredictor:
    """Load and run the verified real-data Random Forest."""

    def __init__(self) -> None:
        required_files = [
            SCALER_PATH,
            MODEL_PATH,
            THRESHOLDS_PATH,
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

        with THRESHOLDS_PATH.open(
            "r",
            encoding="utf-8",
        ) as threshold_file:
            thresholds = json.load(threshold_file)

        self.threshold = float(
            thresholds["random_forest"]
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
        """Convert one FlowGuard flow dictionary into model order."""

        missing_features = [
            feature
            for feature in FEATURE_COLUMNS
            if feature not in flow
        ]

        if missing_features:
            raise KeyError(
                "Flow is missing required features: "
                + ", ".join(missing_features)
            )

        values = []

        for feature in FEATURE_COLUMNS:
            value = float(flow[feature])

            if not np.isfinite(value):
                raise ValueError(
                    f"Feature {feature} is not finite: {value}"
                )

            values.append(value)

        return np.asarray(
            [values],
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
PY

2. Verify the saved threshold

cat /home/pd/Downloads/flowguard/ml-service/app/models/real_only/thresholds.json

You should see a random_forest threshold near:

0.023552

3. Test it against existing FlowGuard flows

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

PYTHONPATH=. python -m app.ml.real_only_predictor \
  /home/pd/Downloads/flowguard/data/flows_output.jsonl \
  5

Expected output for each compatible flow:

{
  "line": 1,
  "src_ip": "...",
  "dst_ip": "...",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.82,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}

4. What this proves

This confirms:

C++ flow output
      ↓
11 FlowGuard features
      ↓
real CICIDS2017 scaler
      ↓
real CICIDS2017 Random Forest
      ↓
live attack probability and decision

It does not produce a new accuracy score because your live JSONL flows have no ground-truth labels.

Run the predictor command and paste its output; the following step will connect this class to your existing /analyze endpoint without breaking the current API.

Pasted text(7).txt
Document

The predictor is loading correctly. The failure is only because your C++ JSONL contains the base counters but not these four derived features:

bytes_per_sec
packets_per_sec
syn_ack_ratio
rst_ratio

All 799 flows were skipped for that same reason.

Patch the predictor so it calculates those values automatically.
1. Apply the fix

Run from anywhere:

python - <<'PY'
from pathlib import Path
import re

path = Path(
    "/home/pd/Downloads/flowguard/"
    "ml-service/app/ml/real_only_predictor.py"
)

text = path.read_text(encoding="utf-8")

pattern = r'''    @staticmethod
    def _feature_vector\(
        flow: dict\[str, Any\],
    \) -> np\.ndarray:
.*?
    def predict\('''

replacement = '''    @staticmethod
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

    def predict('''

updated_text, replacements = re.subn(
    pattern,
    replacement,
    text,
    flags=re.DOTALL,
)

if replacements != 1:
    raise SystemExit(
        f"Patch failed: expected 1 function, found {replacements}"
    )

path.write_text(updated_text, encoding="utf-8")
print(f"Updated: {path}")
PY

2. Check the Python syntax

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python -m py_compile app/ml/real_only_predictor.py

No output means the syntax is valid.
3. Run the predictor again

PYTHONPATH=. python -m app.ml.real_only_predictor \
  /home/pd/Downloads/flowguard/data/flows_output.jsonl \
  5

You should now receive five results resembling:

{
  "line": 1,
  "src_ip": "192.168.x.x",
  "dst_ip": "x.x.x.x",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.74,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}

4. Ignore the other two errors for now

These failed because the files have not been created yet:

scripts/benchmark_capture.sh
training/loao_eval.py

They were proposed future scripts, not existing project files. Also continue using the actual project path:

/home/pd/Downloads/flowguard

rather than:

~/flowguard

The immediate goal is to get five live-flow predictions successfully. After that, the real predictor gets connected to the FastAPI /analyze endpoint.


path.write_text(updated_text, encoding="utf-8")
print(f"Updated: {path}")
PY
Updated: /home/pd/Downloads/flowguard/ml-service/app/ml/real_only_predictor.py

flowguard main  ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python -m py_compile app/ml/real_only_predictor.py

flowguard/ml-service main  ? ❯ PYTHONPATH=. python -m app.ml.real_only_predictor \
  /home/pd/Downloads/flowguard/data/flows_output.jsonl \
  5
{
  "line": 1,
  "src_ip": "10.10.2.1",
  "dst_ip": "10.10.2.101",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.155631,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}
{
  "line": 2,
  "src_ip": "10.10.2.1",
  "dst_ip": "10.10.2.101",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.154424,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}
{
  "line": 3,
  "src_ip": "10.10.2.1",
  "dst_ip": "10.10.2.101",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.152424,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}
{
  "line": 4,
  "src_ip": "10.10.2.1",
  "dst_ip": "10.10.2.101",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.154424,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}
{
  "line": 5,
  "src_ip": "10.10.2.1",
  "dst_ip": "10.10.2.101",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.154424,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}

flowguard/ml-service main  ? ❯

Great — the real-data predictor is working on your C++ flow output.

All five were marked as attacks because:

attack probability ≈ 0.15
configured threshold = 0.023552

That does not prove those five flows are genuine attacks; the live PCAP lacks ground-truth labels. We will first expose the model through a separate shadow-mode API endpoint without changing or breaking your existing /analyze endpoint.
1. Create the new API route

Run:

mkdir -p /home/pd/Downloads/flowguard/ml-service/app/routes
touch /home/pd/Downloads/flowguard/ml-service/app/routes/__init__.py

Then create the route:

cat > /home/pd/Downloads/flowguard/ml-service/app/routes/real_analysis.py <<'PY'
"""
Shadow-mode API route for FlowGuard's real-data Random Forest.

This endpoint:
- reads recent C++-generated flows,
- derives missing rate and ratio features,
- scores them with the verified CICIDS2017 Random Forest,
- returns predictions without modifying the existing alert pipeline.

The results are model predictions, not verified ground-truth attacks.
"""

from __future__ import annotations

import json
import os
from collections import deque
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from app.ml.real_only_predictor import RealOnlyRandomForestPredictor


router = APIRouter(
    prefix="/real-model",
    tags=["real-model"],
)

predictor = RealOnlyRandomForestPredictor()


def resolve_flow_file() -> Path:
    """Find the FlowGuard JSONL file in local or Docker execution."""

    candidates = []

    configured_path = os.getenv("FLOWGUARD_FLOW_FILE")

    if configured_path:
        candidates.append(Path(configured_path))

    candidates.extend(
        [
            # Docker shared data volume.
            Path("/data/flows_output.jsonl"),

            # Local repository:
            # flowguard/data/flows_output.jsonl
            Path(__file__).resolve().parents[3]
            / "data"
            / "flows_output.jsonl",
        ]
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "flows_output.jsonl was not found. Checked: "
        + ", ".join(str(path) for path in candidates)
    )


@router.get("/health")
def real_model_health() -> dict:
    """Confirm that the real-data model and flow file are available."""

    try:
        flow_file = resolve_flow_file()

        return {
            "status": "ok",
            "model": "real_only_random_forest",
            "threshold": predictor.threshold,
            "flow_file": str(flow_file),
            "mode": "shadow",
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error


@router.post("/analyze")
def analyze_real_flows(
    limit: int = Query(
        default=50,
        ge=1,
        le=5000,
    ),
) -> dict:
    """
    Score the most recent flows without saving alerts.

    Shadow mode lets us inspect behaviour before replacing the current
    production ensemble.
    """

    try:
        flow_file = resolve_flow_file()
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    recent_lines: deque[tuple[int, str]] = deque(
        maxlen=limit
    )

    try:
        with flow_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            for line_number, line in enumerate(
                file,
                start=1,
            ):
                if line.strip():
                    recent_lines.append(
                        (line_number, line)
                    )

    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not read flow file: {error}",
        ) from error

    results = []
    errors = []

    for line_number, line in recent_lines:
        try:
            flow = json.loads(line)
            prediction = predictor.predict(flow)

            results.append(
                {
                    "line": line_number,
                    "src_ip": flow.get("src_ip"),
                    "dst_ip": flow.get("dst_ip"),
                    "src_port": flow.get("src_port"),
                    "dst_port": flow.get("dst_port"),
                    "protocol": flow.get("protocol"),
                    **prediction,
                }
            )

        except Exception as error:
            errors.append(
                {
                    "line": line_number,
                    "error": str(error),
                }
            )

    alert_count = sum(
        1
        for result in results
        if result["alert"]
    )

    benign_count = len(results) - alert_count

    return {
        "mode": "shadow",
        "model": "real_only_random_forest",
        "threshold": predictor.threshold,
        "flow_file": str(flow_file),
        "requested": limit,
        "analyzed": len(results),
        "alerts": alert_count,
        "benign": benign_count,
        "errors": len(errors),
        "results": results,
        "error_details": errors[:20],
        "warning": (
            "Predictions are not verified attacks because live flows "
            "do not contain ground-truth labels."
        ),
    }
PY

2. Register the route in app/main.py

Run this safe patch:

python - <<'PY'
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/"
    "ml-service/app/main.py"
)

text = path.read_text(encoding="utf-8")

marker = "# FlowGuard real-data shadow endpoint"

if marker in text:
    print("Real-data route is already registered.")
else:
    addition = """

# FlowGuard real-data shadow endpoint
from app.routes.real_analysis import router as real_analysis_router
app.include_router(real_analysis_router)
"""

    path.write_text(
        text.rstrip() + addition + "\n",
        encoding="utf-8",
    )

    print(f"Updated: {path}")
PY

3. Check syntax and imports

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python -m py_compile \
  app/main.py \
  app/routes/real_analysis.py \
  app/ml/real_only_predictor.py

No output means the syntax is correct.

Test importing the complete API:

PYTHONPATH=. python -c "from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])"

Expected:

['/real-model/health', '/real-model/analyze']

4. Start FastAPI

Keep this terminal open:

PYTHONPATH=. uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload

5. Test it from another terminal

Health check:

curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool

Run shadow analysis on the five most recent flows:

curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=5" \
  | python -m json.tool

This completes:

C++ packet parsing
        ↓
JSONL flow aggregation
        ↓
derived flow features
        ↓
real CICIDS2017 scaler
        ↓
real CICIDS2017 Random Forest
        ↓
FastAPI response

Keep this in shadow mode until we inspect the API output and decide whether the very low 0.023552 threshold is suitable for live alert generation.


flowguard/ml-service main  ? ❯ python - <<'PY'
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/"
    "ml-service/app/main.py"
)

text = path.read_text(encoding="utf-8")

marker = "# FlowGuard real-data shadow endpoint"

if marker in text:
    print("Real-data route is already registered.")
else:
    addition = """

# FlowGuard real-data shadow endpoint
from app.routes.real_analysis import router as real_analysis_router
app.include_router(real_analysis_router)
"""

    path.write_text(
        text.rstrip() + addition + "\n",
        encoding="utf-8",
    )

    print(f"Updated: {path}")
PY
Updated: /home/pd/Downloads/flowguard/ml-service/app/main.py

flowguard/ml-service main  ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python -m py_compile \
  app/main.py \
  app/routes/real_analysis.py \
  app/ml/real_only_predictor.py

flowguard/ml-service main  ? ❯ PYTHONPATH=. python -c "from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/pd/Downloads/flowguard/ml-service/app/main.py", line 1, in <module>
    from app.ml.ensemble import EnsembleDetector
ImportError: cannot import name 'EnsembleDetector' from 'app.ml.ensemble' (/home/pd/Downloads/flowguard/ml-service/app/ml/ensemble.py)

Your new route is fine. The API fails earlier because app/main.py expects a class named:

EnsembleDetector

but app/ml/ensemble.py currently defines a different class name, most likely Ensemble.

Use a backward-compatible alias instead of rewriting the API.
1. Back up and patch ensemble.py

builtin cd /home/pd/Downloads/flowguard/ml-service

cp app/ml/ensemble.py app/ml/ensemble.py.bak

python - <<'PY'
from pathlib import Path
import ast

path = Path("app/ml/ensemble.py")
source = path.read_text(encoding="utf-8")
tree = ast.parse(source)

class_names = {
    node.name
    for node in tree.body
    if isinstance(node, ast.ClassDef)
}

print("Classes found:", sorted(class_names))

if "EnsembleDetector" in class_names:
    print("EnsembleDetector already exists.")

elif "Ensemble" in class_names:
    alias = "\n\n# Backward-compatible class name expected by app.main\nEnsembleDetector = Ensemble\n"

    if "EnsembleDetector = Ensemble" not in source:
        path.write_text(
            source.rstrip() + alias,
            encoding="utf-8",
        )

    print("Added alias: EnsembleDetector = Ensemble")

else:
    raise SystemExit(
        "Neither EnsembleDetector nor Ensemble exists in ensemble.py"
    )
PY

2. Check syntax

python -m py_compile \
  app/ml/ensemble.py \
  app/main.py \
  app/routes/real_analysis.py

3. Test the API import again

PYTHONPATH=. python -c "from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])"

Expected:

['/real-model/health', '/real-model/analyze']

If a new error appears after this, paste only that new traceback.


flowguard/ml-service main  ? ✗ builtin cd /home/pd/Downloads/flowguard/ml-service

cp app/ml/ensemble.py app/ml/ensemble.py.bak

python - <<'PY'
from pathlib import Path
import ast

path = Path("app/ml/ensemble.py")
source = path.read_text(encoding="utf-8")
tree = ast.parse(source)

class_names = {
    node.name
    for node in tree.body
    if isinstance(node, ast.ClassDef)
}

print("Classes found:", sorted(class_names))

if "EnsembleDetector" in class_names:
    print("EnsembleDetector already exists.")

elif "Ensemble" in class_names:
    alias = "\n\n# Backward-compatible class name expected by app.main\nEnsembleDetector = Ensemble\n"

    if "EnsembleDetector = Ensemble" not in source:
        path.write_text(
            source.rstrip() + alias,
            encoding="utf-8",
        )

    print("Added alias: EnsembleDetector = Ensemble")

else:
    raise SystemExit(
        "Neither EnsembleDetector nor Ensemble exists in ensemble.py"
    )
PY
Classes found: ['Ensemble']
Added alias: EnsembleDetector = Ensemble

flowguard/ml-service main  ? ❯ python -m py_compile \
  app/ml/ensemble.py \
  app/main.py \
  app/routes/real_analysis.py

flowguard/ml-service main  ? ❯ PYTHONPATH=. python -c "from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/pd/Downloads/flowguard/ml-service/app/main.py", line 19, in <module>
    detector = EnsembleDetector()
  File "/home/pd/Downloads/flowguard/ml-service/app/ml/ensemble.py", line 38, in __init__
    self.gnn.load_state_dict(torch.load(f"{model_dir}/gnn_graphsage.pt"))
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/pd/Downloads/flowguard/ml-service/.venv/lib/python3.14/site-packages/torch/nn/modules/module.py", line 2638, in load_state_dict
    raise RuntimeError(
    ...<3 lines>...
    )
RuntimeError: Error(s) in loading state_dict for FlowGraphSAGE:
	size mismatch for conv1.lin_l.weight: copying a param with shape torch.Size([32, 4]) from checkpoint, the shape in current model is torch.Size([32, 2]).
	size mismatch for conv1.lin_r.weight: copying a param with shape torch.Size([32, 4]) from checkpoint, the shape in current model is torch.Size([32, 2]).

flowguard/ml-service main  ? ✗?

The checkpoint was trained with 4 input features, but ensemble.py creates the GNN with only 2 input features:

checkpoint: 4 inputs
current model: 2 inputs

Patch it to infer the correct input size automatically.

Run:

builtin cd /home/pd/Downloads/flowguard/ml-service

python - <<'PY'
from pathlib import Path
import re

path = Path("app/ml/ensemble.py")
text = path.read_text(encoding="utf-8")

pattern = r'''self\.gnn\s*=\s*FlowGraphSAGE\(in_channels=2\)
\s*self\.gnn\.load_state_dict\(torch\.load\(f"\{model_dir\}/gnn_graphsage\.pt"\)\)'''

replacement = '''gnn_checkpoint_path = f"{model_dir}/gnn_graphsage.pt"
        gnn_state_dict = torch.load(
            gnn_checkpoint_path,
            map_location="cpu",
        )

        # Infer the input feature count directly from the saved checkpoint.
        gnn_input_channels = int(
            gnn_state_dict["conv1.lin_l.weight"].shape[1]
        )

        self.gnn = FlowGraphSAGE(
            in_channels=gnn_input_channels
        )

        self.gnn.load_state_dict(gnn_state_dict)'''

updated, count = re.subn(
    pattern,
    replacement,
    text,
)

if count != 1:
    raise SystemExit(
        f"Patch failed: expected 1 matching GNN block, found {count}"
    )

path.write_text(updated, encoding="utf-8")

print("Updated GNN loader.")
print("Input channels will now be inferred from the checkpoint.")
PY

Check syntax:

python -m py_compile \
  app/ml/ensemble.py \
  app/main.py \
  app/routes/real_analysis.py

Then test the API import again:

PYTHONPATH=. python -c "
from app.main import app
print([route.path for route in app.routes if 'real-model' in route.path])
"

Expected:

['/real-model/health', '/real-model/analyze']

This fixes the immediate mismatch without hardcoding 4. If the GNN is retrained later with a different number of features, the loader will adapt automatically.


flowguard/ml-service main  ? ✗ builtin cd /home/pd/Downloads/flowguard/ml-service

python - <<'PY'
from pathlib import Path
import re

path = Path("app/ml/ensemble.py")
text = path.read_text(encoding="utf-8")

pattern = r'''self\.gnn\s*=\s*FlowGraphSAGE\(in_channels=2\)
\s*self\.gnn\.load_state_dict\(torch\.load\(f"\{model_dir\}/gnn_graphsage\.pt"\)\)'''

replacement = '''gnn_checkpoint_path = f"{model_dir}/gnn_graphsage.pt"
        gnn_state_dict = torch.load(
            gnn_checkpoint_path,
            map_location="cpu",
        )

        # Infer the input feature count directly from the saved checkpoint.
        gnn_input_channels = int(
            gnn_state_dict["conv1.lin_l.weight"].shape[1]
        )

        self.gnn = FlowGraphSAGE(
            in_channels=gnn_input_channels
        )

        self.gnn.load_state_dict(gnn_state_dict)'''

updated, count = re.subn(
    pattern,
    replacement,
    text,
)

if count != 1:
    raise SystemExit(
        f"Patch failed: expected 1 matching GNN block, found {count}"
    )

path.write_text(updated, encoding="utf-8")

print("Updated GNN loader.")
print("Input channels will now be inferred from the checkpoint.")
PY
Updated GNN loader.
Input channels will now be inferred from the checkpoint.

flowguard/ml-service main  ? ❯ python -m py_compile \
  app/ml/ensemble.py \
  app/main.py \
  app/routes/real_analysis.py

flowguard/ml-service main  ? ❯ PYTHONPATH=. python -c "
from app.main import app
print([route.path for route in app.routes if 'real-model' in route.path])
"
Traceback (most recent call last):
  File "<string>", line 3, in <module>
    print([route.path for route in app.routes if 'real-model' in route.path])
                                                                 ^^^^^^^^^^
AttributeError: '_IncludedRouter' object has no attribute 'path'

flowguard/ml-service main  ? ✗

The API import now succeeds. The error is only from the route-inspection command, because one object in app.routes has no .path attribute.

Run this safer check:

PYTHONPATH=. python - <<'PY'
from app.main import app

paths = [
    getattr(route, "path", None)
    for route in app.routes
]

print([
    path
    for path in paths
    if path and "real-model" in path
])
PY

Expected:

['/real-model/health', '/real-model/analyze']

Then start FastAPI:

PYTHONPATH=. uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload

Keep that terminal open. In another terminal, run:

curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool

Then:

curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=5" \
  | python -m json.tool

Your GNN checkpoint mismatch is fixed; this latest error does not indicate a model or API failure.


flowguard main  ? ❯ curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
{
    "status": "ok",
    "model": "real_only_random_forest",
    "threshold": 0.023552277985182894,
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "mode": "shadow"
}

flowguard main  ? ❯ curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=5" \
  | python -m json.tool
{
    "mode": "shadow",
    "model": "real_only_random_forest",
    "threshold": 0.023552277985182894,
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "requested": 5,
    "analyzed": 5,
    "alerts": 5,
    "benign": 0,
    "errors": 0,
    "results": [
        {
            "line": 795,
            "src_ip": "43.160.255.143",
            "dst_ip": "10.10.2.101",
            "src_port": 8080,
            "dst_port": 56540,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.38435,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 796,
            "src_ip": "43.160.255.143",
            "dst_ip": "10.10.2.101",
            "src_port": 8080,
            "dst_port": 56548,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.082423,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 797,
            "src_ip": "45.207.200.251",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 34800,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.385731,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 798,
            "src_ip": "45.207.200.251",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 45152,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.219635,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 799,
            "src_ip": "45.207.207.168",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 38408,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.36909,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        }
    ],
    "error_details": [],
    "warning": "Predictions are not verified attacks because live flows do not contain ground-truth labels."
}

flowguard main  ? ❯

It is working end to end:

C++ flow capture
→ JSONL
→ derived features
→ real CICIDS2017 scaler
→ real-data Random Forest
→ FastAPI shadow endpoint

The next step is threshold analysis. Your current threshold, 0.023552, is very low, so nearly any probability above 2.35% becomes an alert. Do not connect it to permanent alert storage yet.
1. Analyze all 799 flows

mkdir -p /home/pd/Downloads/flowguard/docs

curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=799" \
  > /home/pd/Downloads/flowguard/docs/live_shadow_predictions.json

Verify:

python -m json.tool \
  /home/pd/Downloads/flowguard/docs/live_shadow_predictions.json \
  | head -n 30

2. Compare different thresholds

Run:

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "live_shadow_predictions.json"
)

payload = json.loads(path.read_text(encoding="utf-8"))
results = payload["results"]

probabilities = sorted(
    float(result["attack_probability"])
    for result in results
)

def percentile(values, fraction):
    if not values:
        return 0.0

    index = round((len(values) - 1) * fraction)
    return values[index]

print("===== LIVE SHADOW-MODE SUMMARY =====")
print(f"Flows analysed: {len(probabilities)}")
print(f"Minimum probability: {min(probabilities):.6f}")
print(f"Median probability:  {percentile(probabilities, 0.50):.6f}")
print(f"75th percentile:     {percentile(probabilities, 0.75):.6f}")
print(f"90th percentile:     {percentile(probabilities, 0.90):.6f}")
print(f"95th percentile:     {percentile(probabilities, 0.95):.6f}")
print(f"Maximum probability: {max(probabilities):.6f}")

print("\n===== ALERT COUNTS BY THRESHOLD =====")

for threshold in [
    0.023552,
    0.05,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.70,
]:
    alerts = sum(
        probability >= threshold
        for probability in probabilities
    )

    percentage = (
        100.0 * alerts / len(probabilities)
        if probabilities
        else 0.0
    )

    print(
        f"Threshold {threshold:>8.6f}: "
        f"{alerts:>4}/{len(probabilities)} alerts "
        f"({percentage:>6.2f}%)"
    )
PY

3. Show the most suspicious flows

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "live_shadow_predictions.json"
)

payload = json.loads(path.read_text(encoding="utf-8"))

ranked = sorted(
    payload["results"],
    key=lambda item: item["attack_probability"],
    reverse=True,
)

print("===== TOP 20 MODEL-PREDICTED FLOWS =====")

for number, flow in enumerate(ranked[:20], start=1):
    print(
        f"{number:02d}. "
        f"probability={flow['attack_probability']:.6f} | "
        f"{flow.get('src_ip')}:{flow.get('src_port')} -> "
        f"{flow.get('dst_ip')}:{flow.get('dst_port')} | "
        f"{flow.get('protocol')}"
    )
PY

What we are deciding

The output will help choose an operating mode:

Low threshold
→ catches more attacks
→ produces more false alarms

High threshold
→ produces fewer false alarms
→ may miss more attacks

Your verified CICIDS2017 metrics still belong to threshold 0.023552. Changing the live threshold does not change those documented test metrics unless we evaluate the new threshold again on the labelled test set.

Paste the alert-count table and top 20 flows next.


flowguard main  ? ❯ curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
{
    "status": "ok",
    "model": "real_only_random_forest",
    "threshold": 0.023552277985182894,
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "mode": "shadow"
}

flowguard main  ? ❯ curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=5" \
  | python -m json.tool
{
    "mode": "shadow",
    "model": "real_only_random_forest",
    "threshold": 0.023552277985182894,
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "requested": 5,
    "analyzed": 5,
    "alerts": 5,
    "benign": 0,
    "errors": 0,
    "results": [
        {
            "line": 795,
            "src_ip": "43.160.255.143",
            "dst_ip": "10.10.2.101",
            "src_port": 8080,
            "dst_port": 56540,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.38435,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 796,
            "src_ip": "43.160.255.143",
            "dst_ip": "10.10.2.101",
            "src_port": 8080,
            "dst_port": 56548,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.082423,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 797,
            "src_ip": "45.207.200.251",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 34800,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.385731,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 798,
            "src_ip": "45.207.200.251",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 45152,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.219635,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 799,
            "src_ip": "45.207.207.168",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 38408,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.36909,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        }
    ],
    "error_details": [],
    "warning": "Predictions are not verified attacks because live flows do not contain ground-truth labels."
}

flowguard main  ? ❯ mkdir -p /home/pd/Downloads/flowguard/docs

curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=799" \
  > /home/pd/Downloads/flowguard/docs/live_shadow_predictions.json

flowguard main  ? ❯ python -m json.tool \
  /home/pd/Downloads/flowguard/docs/live_shadow_predictions.json \
  | head -n 30
{
    "mode": "shadow",
    "model": "real_only_random_forest",
    "threshold": 0.023552277985182894,
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "requested": 799,
    "analyzed": 799,
    "alerts": 762,
    "benign": 37,
    "errors": 0,
    "results": [
        {
            "line": 1,
            "src_ip": "10.10.2.1",
            "dst_ip": "10.10.2.101",
            "src_port": 53,
            "dst_port": 1159,
            "protocol": "UDP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.155631,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 2,
            "src_ip": "10.10.2.1",
            "dst_ip": "10.10.2.101",
            "src_port": 53,
            "dst_port": 1711,

flowguard main  ? ❯
flowguard main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "live_shadow_predictions.json"
)

payload = json.loads(path.read_text(encoding="utf-8"))
results = payload["results"]

probabilities = sorted(
    float(result["attack_probability"])
    for result in results
)

def percentile(values, fraction):
    if not values:
        return 0.0

    index = round((len(values) - 1) * fraction)
    return values[index]

print("===== LIVE SHADOW-MODE SUMMARY =====")
print(f"Flows analysed: {len(probabilities)}")
print(f"Minimum probability: {min(probabilities):.6f}")
print(f"Median probability:  {percentile(probabilities, 0.50):.6f}")
print(f"75th percentile:     {percentile(probabilities, 0.75):.6f}")
print(f"90th percentile:     {percentile(probabilities, 0.90):.6f}")
print(f"95th percentile:     {percentile(probabilities, 0.95):.6f}")
print(f"Maximum probability: {max(probabilities):.6f}")

print("\n===== ALERT COUNTS BY THRESHOLD =====")

for threshold in [
    0.023552,
    0.05,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.70,
]:
    alerts = sum(
        probability >= threshold
        for probability in probabilities
    )

    percentage = (
        100.0 * alerts / len(probabilities)
        if probabilities
        else 0.0
    )

    print(
        f"Threshold {threshold:>8.6f}: "
        f"{alerts:>4}/{len(probabilities)} alerts "
        f"({percentage:>6.2f}%)"
    )
PY
===== LIVE SHADOW-MODE SUMMARY =====
Flows analysed: 799
Minimum probability: 0.003667
Median probability:  0.270419
75th percentile:     0.418763
90th percentile:     0.456239
95th percentile:     0.469807
Maximum probability: 0.616022

===== ALERT COUNTS BY THRESHOLD =====
Threshold 0.023552:  762/799 alerts ( 95.37%)
Threshold 0.050000:  756/799 alerts ( 94.62%)
Threshold 0.100000:  731/799 alerts ( 91.49%)
Threshold 0.200000:  514/799 alerts ( 64.33%)
Threshold 0.300000:  371/799 alerts ( 46.43%)
Threshold 0.400000:  251/799 alerts ( 31.41%)
Threshold 0.500000:    5/799 alerts (  0.63%)
Threshold 0.700000:    0/799 alerts (  0.00%)

flowguard main  ? ❯
flowguard main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "live_shadow_predictions.json"
)

payload = json.loads(path.read_text(encoding="utf-8"))

ranked = sorted(
    payload["results"],
    key=lambda item: item["attack_probability"],
    reverse=True,
)

print("===== TOP 20 MODEL-PREDICTED FLOWS =====")

for number, flow in enumerate(ranked[:20], start=1):
    print(
        f"{number:02d}. "
        f"probability={flow['attack_probability']:.6f} | "
        f"{flow.get('src_ip')}:{flow.get('src_port')} -> "
        f"{flow.get('dst_ip')}:{flow.get('dst_port')} | "
        f"{flow.get('protocol')}"
    )
PY
===== TOP 20 MODEL-PREDICTED FLOWS =====
01. probability=0.616022 | 142.250.138.139:443 -> 10.10.2.101:60046 | TCP
02. probability=0.524693 | 10.10.2.101:55566 -> 101.32.207.8:8080 | TCP
03. probability=0.516668 | 10.10.2.101:55560 -> 101.32.207.8:8080 | TCP
04. probability=0.513736 | 10.10.2.101:57660 -> 173.194.208.94:443 | TCP
05. probability=0.513736 | 10.10.2.101:57674 -> 173.194.208.94:443 | TCP
06. probability=0.492760 | 10.10.2.101:40782 -> 101.32.207.8:8080 | TCP
07. probability=0.490528 | 10.10.2.101:40810 -> 101.32.207.8:8080 | TCP
08. probability=0.490528 | 10.10.2.101:40298 -> 154.90.54.222:8080 | TCP
09. probability=0.490528 | 10.10.2.101:54066 -> 43.157.1.82:8080 | TCP
10. probability=0.490528 | 10.10.2.101:46096 -> 43.157.184.190:8080 | TCP
11. probability=0.490528 | 10.10.2.101:44200 -> 43.160.255.143:8080 | TCP
12. probability=0.488850 | 43.157.184.190:8080 -> 10.10.2.101:41176 | TCP
13. probability=0.488528 | 10.10.2.101:45086 -> 43.159.143.39:8080 | TCP
14. probability=0.486856 | 10.10.2.101:40798 -> 101.32.207.8:8080 | TCP
15. probability=0.484508 | 43.157.184.190:8080 -> 10.10.2.101:41154 | TCP
16. probability=0.484508 | 43.157.184.190:8080 -> 10.10.2.101:41162 | TCP
17. probability=0.482174 | 43.157.184.190:8080 -> 10.10.2.101:37784 | TCP
18. probability=0.478303 | 101.32.207.8:8080 -> 10.10.2.101:38848 | TCP
19. probability=0.472808 | 101.32.207.8:8080 -> 10.10.2.101:40112 | TCP
20. probability=0.472808 | 101.32.207.8:8080 -> 10.10.2.101:45962 | TCP

flowguard main  ? ❯

Pasted text(8).txt
Document
?

Your threshold tuning is complete.

The correct mode is balanced:

Threshold: 0.0235
Accuracy:  86.09%
Precision: 78.71%
Recall:    98.94%
F1:        87.67%

The high_recall mode only increased recall slightly—from 98.94% to 99.18%—but caused many more false positives and reduced accuracy to 78.08%. Also, your model could not achieve the requested 95% validation precision, so the script fell back to the same threshold as balanced; high_precision is therefore not a genuinely distinct mode. Thresholds such as 0.5 must not be used because validation recall collapsed to 0.4%.

Now connect the saved balanced threshold to the API.
1. Patch the predictor to load operational modes

builtin cd /home/pd/Downloads/flowguard/ml-service

python - <<'PY'
from pathlib import Path

path = Path("app/ml/real_only_predictor.py")
text = path.read_text(encoding="utf-8")

if "import os" not in text:
    text = text.replace(
        "import json\n",
        "import json\nimport os\n",
        1,
    )

old_constant = '''THRESHOLDS_PATH = MODEL_DIRECTORY / "thresholds.json"'''

new_constant = '''THRESHOLDS_PATH = MODEL_DIRECTORY / "thresholds.json"
OPERATIONAL_THRESHOLDS_PATH = (
    MODEL_DIRECTORY / "rf_operational_thresholds.json"
)'''

text = text.replace(
    old_constant,
    new_constant,
    1,
)

old_files = '''        required_files = [
            SCALER_PATH,
            MODEL_PATH,
            THRESHOLDS_PATH,
        ]'''

new_files = '''        required_files = [
            SCALER_PATH,
            MODEL_PATH,
            OPERATIONAL_THRESHOLDS_PATH,
        ]'''

text = text.replace(
    old_files,
    new_files,
    1,
)

old_threshold_block = '''        with THRESHOLDS_PATH.open(
            "r",
            encoding="utf-8",
        ) as threshold_file:
            thresholds = json.load(threshold_file)

        self.threshold = float(
            thresholds["random_forest"]
        )'''

new_threshold_block = '''        with OPERATIONAL_THRESHOLDS_PATH.open(
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
        )'''

if old_threshold_block not in text:
    raise SystemExit(
        "Could not find the old threshold-loading block."
    )

text = text.replace(
    old_threshold_block,
    new_threshold_block,
    1,
)

old_return = '''            "threshold": round(
                self.threshold,
                6,
            ),
            "model": "real_only_random_forest",'''

new_return = '''            "threshold": round(
                self.threshold,
                6,
            ),
            "operational_mode": self.operational_mode,
            "model": "real_only_random_forest",'''

text = text.replace(
    old_return,
    new_return,
    1,
)

path.write_text(text, encoding="utf-8")

print(f"Updated: {path}")
PY

2. Update the API health response

python - <<'PY'
from pathlib import Path

path = Path("app/routes/real_analysis.py")
text = path.read_text(encoding="utf-8")

old = '''            "threshold": predictor.threshold,
            "flow_file": str(flow_file),'''

new = '''            "threshold": predictor.threshold,
            "operational_mode": predictor.operational_mode,
            "flow_file": str(flow_file),'''

text = text.replace(old, new, 1)

old_second = '''        "threshold": predictor.threshold,
        "flow_file": str(flow_file),'''

new_second = '''        "threshold": predictor.threshold,
        "operational_mode": predictor.operational_mode,
        "flow_file": str(flow_file),'''

text = text.replace(old_second, new_second, 1)

path.write_text(text, encoding="utf-8")
print(f"Updated: {path}")
PY

3. Validate

python -m py_compile \
  app/ml/real_only_predictor.py \
  app/routes/real_analysis.py \
  app/main.py

4. Restart FastAPI in balanced mode

Stop the current Uvicorn process with Ctrl+C, then run:

RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload

5. Confirm the selected mode

In another terminal:

curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool

Expected:

{
    "status": "ok",
    "model": "real_only_random_forest",
    "threshold": 0.0235,
    "operational_mode": "balanced",
    "mode": "shadow"
}

Keep it in shadow mode. The 95.37% alert rate on the infected-Android capture suggests strong distribution shift, not that 95% of those flows are confirmed malicious.


flowguard main  ? ❯ curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
{
    "status": "ok",
    "model": "real_only_random_forest",
    "threshold": 0.0235,
    "operational_mode": "balanced",
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "mode": "shadow"
}

Perfect — the real-data Random Forest is now loaded through FastAPI in balanced shadow mode.

Next, verify predictions under the new operational configuration:

curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=20" \
  | python -m json.tool

Then inspect where your existing /analyze endpoint is defined before we connect the new model:

grep -RInE '@app\.(post|get)\("/analyze"|@router\.(post|get)\("/analyze"|def analyze' \
  /home/pd/Downloads/flowguard/ml-service/app

Also show the surrounding code:

grep -RInE -B 15 -A 80 \
  '@app\.(post|get)\("/analyze"|@router\.(post|get)\("/analyze"|def analyze' \
  /home/pd/Downloads/flowguard/ml-service/app

The next integration will use an environment switch such as:

DETECTION_MODEL=legacy
DETECTION_MODEL=real_rf
DETECTION_MODEL=compare

compare mode will run both systems side by side without replacing your existing alert pipeline. Paste the output of the two grep commands next.

Pasted text(9).txt
Document
?

Your output confirms two things:

    /analyze still uses the legacy ensemble and can persist alerts only when persist=true.

    /real-model/analyze runs the real-data Random Forest separately in shadow mode.

The safest next step is a comparison endpoint. It runs both models on the same flows but saves nothing to PostgreSQL.
1. Add /analyze/compare

Run:

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python - <<'PY'
from pathlib import Path

path = Path("app/main.py")
text = path.read_text(encoding="utf-8")

marker = "# FlowGuard legacy-versus-real comparison endpoint"

if marker in text:
    print("Comparison endpoint is already registered.")
else:
    addition = r'''

# FlowGuard legacy-versus-real comparison endpoint
from app.ml.real_only_predictor import RealOnlyRandomForestPredictor

comparison_real_predictor = RealOnlyRandomForestPredictor()


@app.post("/analyze/compare")
async def compare_detection_models(
    limit: int = 100,
):
    """
    Run the legacy ensemble and real-data Random Forest on the same
    recent flows.

    This endpoint never persists alerts. It is for shadow comparison only.
    """

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    all_flows = read_all_flows()
    flows = all_flows[-limit:]

    start_line = max(
        1,
        len(all_flows) - len(flows) + 1,
    )

    results = []

    legacy_alerts = 0
    real_rf_alerts = 0

    both_alert = 0
    both_benign = 0
    legacy_only = 0
    real_rf_only = 0

    errors = []

    for position, flow in enumerate(
        flows,
        start=start_line,
    ):
        try:
            normalized_features = normalize_flow(flow)

            legacy_feature_row = [
                normalized_features.get(column, 0.0)
                for column in FEATURE_COLUMNS
            ]

            legacy_result = detector.score(
                legacy_feature_row
            )

            real_result = (
                comparison_real_predictor.predict(flow)
            )

            legacy_is_alert = bool(
                legacy_result.get("is_anomaly", False)
            )

            real_is_alert = bool(
                real_result["alert"]
            )

            legacy_alerts += int(legacy_is_alert)
            real_rf_alerts += int(real_is_alert)

            if legacy_is_alert and real_is_alert:
                agreement_type = "both_alert"
                both_alert += 1

            elif not legacy_is_alert and not real_is_alert:
                agreement_type = "both_benign"
                both_benign += 1

            elif legacy_is_alert:
                agreement_type = "legacy_only"
                legacy_only += 1

            else:
                agreement_type = "real_rf_only"
                real_rf_only += 1

            results.append(
                {
                    "line": position,
                    "src_ip": flow.get("src_ip"),
                    "dst_ip": flow.get("dst_ip"),
                    "src_port": flow.get("src_port"),
                    "dst_port": flow.get("dst_port"),
                    "protocol": flow.get("protocol"),
                    "legacy_alert": legacy_is_alert,
                    "real_rf_alert": real_is_alert,
                    "agreement": agreement_type,
                    "real_rf_probability": (
                        real_result["attack_probability"]
                    ),
                    "real_rf_threshold": (
                        real_result["threshold"]
                    ),
                    "real_rf_operational_mode": (
                        real_result["operational_mode"]
                    ),
                }
            )

        except Exception as error:
            errors.append(
                {
                    "line": position,
                    "error": str(error),
                }
            )

    analyzed = len(results)

    agreements = both_alert + both_benign

    agreement_rate = (
        agreements / analyzed
        if analyzed
        else 0.0
    )

    return {
        "mode": "compare-shadow",
        "total_available_flows": len(all_flows),
        "requested": limit,
        "analyzed": analyzed,
        "errors": len(errors),
        "legacy_alerts": legacy_alerts,
        "real_rf_alerts": real_rf_alerts,
        "agreement": {
            "both_alert": both_alert,
            "both_benign": both_benign,
            "legacy_only": legacy_only,
            "real_rf_only": real_rf_only,
            "agreement_rate": round(
                agreement_rate,
                6,
            ),
        },
        "persistence_enabled": False,
        "results": results,
        "error_details": errors[:20],
        "warning": (
            "These are model comparisons, not verified attack labels."
        ),
    }
'''

    path.write_text(
        text.rstrip() + addition + "\n",
        encoding="utf-8",
    )

    print(f"Updated: {path}")
PY

2. Check syntax

python -m py_compile \
  app/main.py \
  app/ml/real_only_predictor.py

No output means it passed.
3. Confirm the route exists

PYTHONPATH=. python - <<'PY'
from app.main import app

print([
    getattr(route, "path", None)
    for route in app.routes
    if getattr(route, "path", None)
    == "/analyze/compare"
])
PY

Expected:

['/analyze/compare']

4. Restart FastAPI

Stop the current Uvicorn process with Ctrl+C, then run:

RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload

5. Compare both detectors

In another terminal:

curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  > /home/pd/Downloads/flowguard/docs/model_comparison.json

Show the summary without printing all 100 results:

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "model_comparison.json"
)

data = json.loads(
    path.read_text(encoding="utf-8")
)

print("===== MODEL COMPARISON =====")
print("Analyzed:", data["analyzed"])
print("Errors:", data["errors"])
print("Legacy alerts:", data["legacy_alerts"])
print("Real RF alerts:", data["real_rf_alerts"])
print("Both alert:", data["agreement"]["both_alert"])
print("Both benign:", data["agreement"]["both_benign"])
print("Legacy only:", data["agreement"]["legacy_only"])
print("Real RF only:", data["agreement"]["real_rf_only"])
print(
    "Agreement rate:",
    f"{data['agreement']['agreement_rate'] * 100:.2f}%"
)
PY

This keeps the existing alert pipeline untouched while measuring exactly how differently the old ensemble and real-data model behave.


flowguard main  ? ❯ RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
bash: command not found: uvicorn

flowguard main  ? ✗ curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  > /home/pd/Downloads/flowguard/docs/model_comparison.json

flowguard main  ? ❯
flowguard main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "model_comparison.json"
)

data = json.loads(
    path.read_text(encoding="utf-8")
)

print("===== MODEL COMPARISON =====")
print("Analyzed:", data["analyzed"])
print("Errors:", data["errors"])
print("Legacy alerts:", data["legacy_alerts"])
print("Real RF alerts:", data["real_rf_alerts"])
print("Both alert:", data["agreement"]["both_alert"])
print("Both benign:", data["agreement"]["both_benign"])
print("Legacy only:", data["agreement"]["legacy_only"])
print("Real RF only:", data["agreement"]["real_rf_only"])
print(
    "Agreement rate:",
    f"{data['agreement']['agreement_rate'] * 100:.2f}%"
)
PY
===== MODEL COMPARISON =====
Analyzed: 0
Errors: 100
Legacy alerts: 0
Real RF alerts: 0
Both alert: 0
Both benign: 0
Legacy only: 0
Real RF only: 0
Agreement rate: 0.00%

flowguard main  ? ❯ 
flowguard main  ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python - <<'PY'
from pathlib import Path

path = Path("app/main.py")
text = path.read_text(encoding="utf-8")

marker = "# FlowGuard legacy-versus-real comparison endpoint"

if marker in text:
    print("Comparison endpoint is already registered.")
else:
    addition = r'''

# FlowGuard legacy-versus-real comparison endpoint
from app.ml.real_only_predictor import RealOnlyRandomForestPredictor

comparison_real_predictor = RealOnlyRandomForestPredictor()


@app.post("/analyze/compare")
async def compare_detection_models(
    limit: int = 100,
):
    """
    Run the legacy ensemble and real-data Random Forest on the same
    recent flows.

    This endpoint never persists alerts. It is for shadow comparison only.
    """

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    all_flows = read_all_flows()
    flows = all_flows[-limit:]

    start_line = max(
        1,
        len(all_flows) - len(flows) + 1,
    )

    results = []

    legacy_alerts = 0
    real_rf_alerts = 0

    both_alert = 0
    both_benign = 0
    legacy_only = 0
    real_rf_only = 0

    errors = []

    for position, flow in enumerate(
        flows,
        start=start_line,
    ):
        try:
            normalized_features = normalize_flow(flow)

            legacy_feature_row = [
                normalized_features.get(column, 0.0)
                for column in FEATURE_COLUMNS
            ]

            legacy_result = detector.score(
                legacy_feature_row
            )

            real_result = (
                comparison_real_predictor.predict(flow)
            )

            legacy_is_alert = bool(
                legacy_result.get("is_anomaly", False)
            )

            real_is_alert = bool(
                real_result["alert"]
            )

            legacy_alerts += int(legacy_is_alert)
            real_rf_alerts += int(real_is_alert)

            if legacy_is_alert and real_is_alert:
                agreement_type = "both_alert"
                both_alert += 1

            elif not legacy_is_alert and not real_is_alert:
                agreement_type = "both_benign"
                both_benign += 1

            elif legacy_is_alert:
                agreement_type = "legacy_only"
                legacy_only += 1

            else:
                agreement_type = "real_rf_only"
                real_rf_only += 1

            results.append(
                {
                    "line": position,
                    "src_ip": flow.get("src_ip"),
                    "dst_ip": flow.get("dst_ip"),
                    "src_port": flow.get("src_port"),
                    "dst_port": flow.get("dst_port"),
                    "protocol": flow.get("protocol"),
                    "legacy_alert": legacy_is_alert,
                    "real_rf_alert": real_is_alert,
                    "agreement": agreement_type,
                    "real_rf_probability": (
                        real_result["attack_probability"]
                    ),
                    "real_rf_threshold": (
                        real_result["threshold"]
                    ),
                    "real_rf_operational_mode": (
                        real_result["operational_mode"]
                    ),
                }
            )

        except Exception as error:
            errors.append(
                {
                    "line": position,
                    "error": str(error),
                }
            )

    analyzed = len(results)

    agreements = both_alert + both_benign

    agreement_rate = (
        agreements / analyzed
        if analyzed
        else 0.0
    )

    return {
        "mode": "compare-shadow",
        "total_available_flows": len(all_flows),
        "requested": limit,
        "analyzed": analyzed,
        "errors": len(errors),
        "legacy_alerts": legacy_alerts,
        "real_rf_alerts": real_rf_alerts,
        "agreement": {
            "both_alert": both_alert,
            "both_benign": both_benign,
            "legacy_only": legacy_only,
            "real_rf_only": real_rf_only,
            "agreement_rate": round(
                agreement_rate,
                6,
            ),
        },
        "persistence_enabled": False,
        "results": results,
        "error_details": errors[:20],
        "warning": (
            "These are model comparisons, not verified attack labels."
        ),
    }
'''

    path.write_text(
        text.rstrip() + addition + "\n",
        encoding="utf-8",
    )

    print(f"Updated: {path}")
PY
Updated: app/main.py

flowguard/ml-service main  ? ❯ python -m py_compile \
  app/main.py \
  app/ml/real_only_predictor.py

flowguard/ml-service main  ? ❯ PYTHONPATH=. python - <<'PY'
from app.main import app

print([
    getattr(route, "path", None)
    for route in app.routes
    if getattr(route, "path", None)
    == "/analyze/compare"
])
PY
['/analyze/compare']

flowguard/ml-service main  ? ❯ RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
INFO:     Will watch for changes in these directories: ['/home/pd/Downloads/flowguard/ml-service']
ERROR:    [Errno 98] Address already in use

flowguard/ml-service main  ? ✗ RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
INFO:     Will watch for changes in these directories: ['/home/pd/Downloads/flowguard/ml-service']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2891373] using StatReload
INFO:     Started server process [2891474]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:60050 - "POST /analyze/compare?limit=100 HTTP/1.1" 200 OK

The server is now running correctly. The earlier Analyzed: 0, Errors: 100 result was generated before the updated comparison endpoint was running, so that saved JSON is stale.

Keep Uvicorn open and run this in another terminal:

curl --fail-with-body -sS -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  -o /home/pd/Downloads/flowguard/docs/model_comparison.json

Now print the new summary and any errors:

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))

print("===== MODEL COMPARISON =====")
print("Mode:", data.get("mode"))
print("Analyzed:", data.get("analyzed"))
print("Errors:", data.get("errors"))
print("Legacy alerts:", data.get("legacy_alerts"))
print("Real RF alerts:", data.get("real_rf_alerts"))

agreement = data.get("agreement", {})

print("Both alert:", agreement.get("both_alert"))
print("Both benign:", agreement.get("both_benign"))
print("Legacy only:", agreement.get("legacy_only"))
print("Real RF only:", agreement.get("real_rf_only"))
print(
    "Agreement rate:",
    f"{agreement.get('agreement_rate', 0) * 100:.2f}%"
)

errors = data.get("error_details", [])

if errors:
    print("\n===== FIRST ERRORS =====")
    for error in errors[:10]:
        print(error)
PY

The first uvicorn: command not found happened because the virtual environment was not active. The later 200 OK confirms the request reached the newly running API, but the fresh summary will tell us whether both models actually scored the flows.


flowguard main  ? ❯ RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
bash: command not found: uvicorn

flowguard main  ? ✗ curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  > /home/pd/Downloads/flowguard/docs/model_comparison.json

flowguard main  ? ❯
flowguard main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "model_comparison.json"
)

data = json.loads(
    path.read_text(encoding="utf-8")
)

print("===== MODEL COMPARISON =====")
print("Analyzed:", data["analyzed"])
print("Errors:", data["errors"])
print("Legacy alerts:", data["legacy_alerts"])
print("Real RF alerts:", data["real_rf_alerts"])
print("Both alert:", data["agreement"]["both_alert"])
print("Both benign:", data["agreement"]["both_benign"])
print("Legacy only:", data["agreement"]["legacy_only"])
print("Real RF only:", data["agreement"]["real_rf_only"])
print(
    "Agreement rate:",
    f"{data['agreement']['agreement_rate'] * 100:.2f}%"
)
PY
===== MODEL COMPARISON =====
Analyzed: 0
Errors: 100
Legacy alerts: 0
Real RF alerts: 0
Both alert: 0
Both benign: 0
Legacy only: 0
Real RF only: 0
Agreement rate: 0.00%

flowguard main  ? ❯ curl --fail-with-body -sS -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  -o /home/pd/Downloads/flowguard/docs/model_comparison.json

flowguard main  ? ❯
flowguard main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))

print("===== MODEL COMPARISON =====")
print("Mode:", data.get("mode"))
print("Analyzed:", data.get("analyzed"))
print("Errors:", data.get("errors"))
print("Legacy alerts:", data.get("legacy_alerts"))
print("Real RF alerts:", data.get("real_rf_alerts"))

agreement = data.get("agreement", {})

print("Both alert:", agreement.get("both_alert"))
print("Both benign:", agreement.get("both_benign"))
print("Legacy only:", agreement.get("legacy_only"))
print("Real RF only:", agreement.get("real_rf_only"))
print(
    "Agreement rate:",
    f"{agreement.get('agreement_rate', 0) * 100:.2f}%"
)

errors = data.get("error_details", [])

if errors:
    print("\n===== FIRST ERRORS =====")
    for error in errors[:10]:
        print(error)
PY
===== MODEL COMPARISON =====
Mode: compare-shadow
Analyzed: 0
Errors: 100
Legacy alerts: 0
Real RF alerts: 0
Both alert: 0
Both benign: 0
Legacy only: 0
Real RF only: 0
Agreement rate: 0.00%

===== FIRST ERRORS =====
{'line': 700, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 701, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 702, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 703, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 704, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 705, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 706, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 707, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 708, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 709, 'error': "'Ensemble' object has no attribute 'score'"}

flowguard main  ? ❯

The cause is clear: your legacy Ensemble exposes score_flow(...), not score(...). The comparison endpoint called the wrong method for all 100 flows. The ensemble result also uses "alert" rather than "is_anomaly".

Keep Uvicorn running. In another terminal, patch only the comparison endpoint:

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python - <<'PY'
from pathlib import Path

path = Path("app/main.py")
text = path.read_text(encoding="utf-8")

marker = "# FlowGuard legacy-versus-real comparison endpoint"

if marker not in text:
    raise SystemExit("Comparison endpoint marker was not found.")

before, comparison_section = text.split(marker, 1)

old_call = """legacy_result = detector.score(
                legacy_feature_row
            )"""

new_call = """legacy_result = detector.score_flow(
                legacy_feature_row
            )"""

old_result = """legacy_result.get("is_anomaly", False)"""
new_result = """legacy_result.get("alert", False)"""

if old_call not in comparison_section:
    raise SystemExit("Could not find detector.score in comparison endpoint.")

if old_result not in comparison_section:
    raise SystemExit("Could not find legacy is_anomaly lookup.")

comparison_section = comparison_section.replace(
    old_call,
    new_call,
    1,
)

comparison_section = comparison_section.replace(
    old_result,
    new_result,
    1,
)

path.write_text(
    before + marker + comparison_section,
    encoding="utf-8",
)

print("Updated comparison endpoint to use score_flow() and alert.")
PY

Check syntax:

python -m py_compile app/main.py

Because Uvicorn is running with --reload, it should restart automatically. Check its terminal for:

Application startup complete.

Then rerun the comparison:

curl --fail-with-body -sS -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  -o /home/pd/Downloads/flowguard/docs/model_comparison.json

Print the result:

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))
agreement = data.get("agreement", {})

print("===== MODEL COMPARISON =====")
print("Analyzed:", data.get("analyzed"))
print("Errors:", data.get("errors"))
print("Legacy alerts:", data.get("legacy_alerts"))
print("Real RF alerts:", data.get("real_rf_alerts"))
print("Both alert:", agreement.get("both_alert"))
print("Both benign:", agreement.get("both_benign"))
print("Legacy only:", agreement.get("legacy_only"))
print("Real RF only:", agreement.get("real_rf_only"))
print(
    "Agreement rate:",
    f"{agreement.get('agreement_rate', 0) * 100:.2f}%"
)

for error in data.get("error_details", [])[:5]:
    print("ERROR:", error)
PY

This patch only changes the shadow comparison endpoint; it does not persist alerts or replace either detector.

Pasted text(10).txt
Document
?

Great — the comparison endpoint now works correctly.
Result

Flows analyzed: 100
Errors: 0

Legacy ensemble alerts: 85
Real Random Forest alerts: 100

Both marked attack: 85
Both marked benign: 0
Legacy only: 0
Real RF only: 15

Agreement: 85%

This means the real-data Random Forest is more sensitive than the legacy ensemble. It flagged 15 additional flows, but because these live flows have no ground-truth labels, we cannot say whether those 15 are true attacks or false positives.

Keep both models in shadow mode for now.
Inspect the 15 disagreement flows

Run:

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))

disagreements = [
    result
    for result in data["results"]
    if result["agreement"] == "real_rf_only"
]

print("===== REAL RF ONLY FLOWS =====")
print("Total:", len(disagreements))

for number, flow in enumerate(disagreements, start=1):
    print(
        f"{number:02d}. "
        f"probability={flow['real_rf_probability']:.6f} | "
        f"{flow.get('src_ip')}:{flow.get('src_port')} -> "
        f"{flow.get('dst_ip')}:{flow.get('dst_port')} | "
        f"{flow.get('protocol')}"
    )
PY

Do not enable persist=true for the real RF yet. The current safe architecture is:

Legacy ensemble → existing alert pipeline
Real RF → shadow comparison only



flowguard main  ? ✗ builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python - <<'PY'
from pathlib import Path

path = Path("app/main.py")
text = path.read_text(encoding="utf-8")

marker = "# FlowGuard legacy-versus-real comparison endpoint"

if marker not in text:
    raise SystemExit("Comparison endpoint marker was not found.")

before, comparison_section = text.split(marker, 1)

old_call = """legacy_result = detector.score(
                legacy_feature_row
            )"""

new_call = """legacy_result = detector.score_flow(
                legacy_feature_row
            )"""

old_result = """legacy_result.get("is_anomaly", False)"""
new_result = """legacy_result.get("alert", False)"""

if old_call not in comparison_section:
    raise SystemExit("Could not find detector.score in comparison endpoint.")

if old_result not in comparison_section:
    raise SystemExit("Could not find legacy is_anomaly lookup.")

comparison_section = comparison_section.replace(
    old_call,
    new_call,
    1,
)

comparison_section = comparison_section.replace(
    old_result,
    new_result,
    1,
)

path.write_text(
    before + marker + comparison_section,
    encoding="utf-8",
)

print("Updated comparison endpoint to use score_flow() and alert.")
PY
Updated comparison endpoint to use score_flow() and alert.

flowguard/ml-service main  ? ❯ python -m py_compile app/main.py

flowguard/ml-service main  ? ❯ curl --fail-with-body -sS -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  -o /home/pd/Downloads/flowguard/docs/model_comparison.json

flowguard/ml-service main  ? ❯
flowguard/ml-service main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))
agreement = data.get("agreement", {})

print("===== MODEL COMPARISON =====")
print("Analyzed:", data.get("analyzed"))
print("Errors:", data.get("errors"))
print("Legacy alerts:", data.get("legacy_alerts"))
print("Real RF alerts:", data.get("real_rf_alerts"))
print("Both alert:", agreement.get("both_alert"))
print("Both benign:", agreement.get("both_benign"))
print("Legacy only:", agreement.get("legacy_only"))
print("Real RF only:", agreement.get("real_rf_only"))
print(
    "Agreement rate:",
    f"{agreement.get('agreement_rate', 0) * 100:.2f}%"
)

for error in data.get("error_details", [])[:5]:
    print("ERROR:", error)
PY
===== MODEL COMPARISON =====
Analyzed: 100
Errors: 0
Legacy alerts: 85
Real RF alerts: 100
Both alert: 85
Both benign: 0
Legacy only: 0
Real RF only: 15
Agreement rate: 85.00%

flowguard/ml-service main  ? ❯ ^C

flowguard/ml-service main  ? ✗
flowguard/ml-service main  ? ✗ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))

disagreements = [
    result
    for result in data["results"]
    if result["agreement"] == "real_rf_only"
]

print("===== REAL RF ONLY FLOWS =====")
print("Total:", len(disagreements))

for number, flow in enumerate(disagreements, start=1):
    print(
        f"{number:02d}. "
        f"probability={flow['real_rf_probability']:.6f} | "
        f"{flow.get('src_ip')}:{flow.get('src_port')} -> "
        f"{flow.get('dst_ip')}:{flow.get('dst_port')} | "
        f"{flow.get('protocol')}"
    )
PY
===== REAL RF ONLY FLOWS =====
Total: 15
01. probability=0.082423 | 43.157.1.82:8080 -> 10.10.2.101:59072 | TCP
02. probability=0.082690 | 43.157.184.190:8080 -> 10.10.2.101:37286 | TCP
03. probability=0.320024 | 43.157.184.190:8080 -> 10.10.2.101:37740 | TCP
04. probability=0.328078 | 43.157.184.190:8080 -> 10.10.2.101:37752 | TCP
05. probability=0.270603 | 43.157.184.190:8080 -> 10.10.2.101:37756 | TCP
06. probability=0.320024 | 43.159.143.39:8080 -> 10.10.2.101:46514 | TCP
07. probability=0.328078 | 43.159.143.39:8080 -> 10.10.2.101:46516 | TCP
08. probability=0.267563 | 43.159.143.39:8080 -> 10.10.2.101:46530 | TCP
09. probability=0.270990 | 43.159.99.24:8080 -> 10.10.2.101:44172 | TCP
10. probability=0.343764 | 43.159.99.24:8080 -> 10.10.2.101:44174 | TCP
11. probability=0.269931 | 43.159.99.24:8080 -> 10.10.2.101:44186 | TCP
12. probability=0.320024 | 43.160.255.143:8080 -> 10.10.2.101:47276 | TCP
13. probability=0.328078 | 43.160.255.143:8080 -> 10.10.2.101:47292 | TCP
14. probability=0.256603 | 43.160.255.143:8080 -> 10.10.2.101:47298 | TCP
15. probability=0.082423 | 43.160.255.143:8080 -> 10.10.2.101:56548 | TCP

This is a meaningful result. The 15 disagreements are not random:

    Every one is inbound TCP traffic.

    Every source uses port 8080.

    They come from a small group of repeated source IPs.

    They all target your local host 10.10.2.101.

    Random Forest probabilities range from about 0.082 to 0.344.

    The legacy ensemble marked all 15 benign.

So this is better interpreted as one repeated traffic pattern involving several hosts, not 15 unrelated attacks. It is still not proof that the traffic is malicious.
Generate a detailed disagreement report

Run:

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python - <<'PY'
import csv
import json
from collections import defaultdict
from pathlib import Path

project = Path("/home/pd/Downloads/flowguard")

comparison_path = project / "docs/model_comparison.json"
flow_path = project / "data/flows_output.jsonl"
output_path = project / "docs/real_rf_only_flows.csv"

comparison = json.loads(
    comparison_path.read_text(encoding="utf-8")
)

flows = []

with flow_path.open("r", encoding="utf-8") as file:
    for line in file:
        if line.strip():
            flows.append(json.loads(line))

disagreements = [
    result
    for result in comparison["results"]
    if result["agreement"] == "real_rf_only"
]

rows = []

for result in disagreements:
    line_number = int(result["line"])
    flow = flows[line_number - 1]

    duration = float(flow.get("duration_seconds", 0.0))
    packet_count = float(flow.get("packet_count", 0.0))
    total_bytes = float(flow.get("total_bytes", 0.0))
    syn_count = float(flow.get("syn_count", 0.0))
    ack_count = float(flow.get("ack_count", 0.0))
    rst_count = float(flow.get("rst_count", 0.0))

    rows.append(
        {
            "line": line_number,
            "src_ip": flow.get("src_ip"),
            "dst_ip": flow.get("dst_ip"),
            "src_port": flow.get("src_port"),
            "dst_port": flow.get("dst_port"),
            "protocol": flow.get("protocol"),
            "duration_seconds": duration,
            "packet_count": packet_count,
            "total_bytes": total_bytes,
            "bytes_per_sec": (
                total_bytes / duration
                if duration > 0
                else 0.0
            ),
            "packets_per_sec": (
                packet_count / duration
                if duration > 0
                else 0.0
            ),
            "syn_count": syn_count,
            "ack_count": ack_count,
            "fin_count": flow.get("fin_count", 0),
            "rst_count": rst_count,
            "syn_ack_ratio": syn_count / (ack_count + 1.0),
            "rst_ratio": rst_count / (packet_count + 1.0),
            "rf_probability": result["real_rf_probability"],
        }
    )

with output_path.open(
    "w",
    encoding="utf-8",
    newline="",
) as output_file:
    writer = csv.DictWriter(
        output_file,
        fieldnames=rows[0].keys(),
    )
    writer.writeheader()
    writer.writerows(rows)

groups = defaultdict(list)

for row in rows:
    groups[row["src_ip"]].append(row)

print("===== DISAGREEMENT GROUPS BY SOURCE IP =====")

for source_ip, source_rows in sorted(
    groups.items(),
    key=lambda item: len(item[1]),
    reverse=True,
):
    probabilities = [
        row["rf_probability"]
        for row in source_rows
    ]

    destination_ports = sorted(
        {
            row["dst_port"]
            for row in source_rows
        }
    )

    print(
        f"{source_ip}: "
        f"{len(source_rows)} flows | "
        f"average probability={sum(probabilities) / len(probabilities):.6f} | "
        f"maximum={max(probabilities):.6f} | "
        f"destination ports={destination_ports}"
    )

print("\n===== FLOW FEATURES =====")

for row in rows:
    print(
        f"line={row['line']} | "
        f"{row['src_ip']}:{row['src_port']} -> "
        f"{row['dst_ip']}:{row['dst_port']} | "
        f"packets={row['packet_count']:.0f} | "
        f"bytes={row['total_bytes']:.0f} | "
        f"duration={row['duration_seconds']:.6f}s | "
        f"pps={row['packets_per_sec']:.2f} | "
        f"syn={row['syn_count']:.0f} | "
        f"ack={row['ack_count']:.0f} | "
        f"rst={row['rst_count']:.0f} | "
        f"probability={row['rf_probability']:.6f}"
    )

print(f"\nSaved: {output_path}")
PY

The report will be saved here:

/home/pd/Downloads/flowguard/docs/real_rf_only_flows.csv

The correct architecture remains:

Individual flows
      ↓
Both models score them
      ↓
Group repeated flows by source IP and time window
      ↓
Create one consolidated incident alert

Do not create 15 separate permanent alerts for this pattern; later we

i wanta  metic how fast is thta ebpf laye is fater than the cpp layer , metrices

Yes. We should produce an actual measured speedup, not an assumed “eBPF is faster” claim.

Your current programs cannot yet be compared fairly:

    The C++ program reads a PCAP file using pcap_open_offline() and also performs queueing, flow aggregation and JSON output.

    The eBPF loader captures from a live interface and currently prints and flushes every packet event, which adds major terminal I/O overhead.

So timing the current binaries directly would give a misleading number.
Metrics we will calculate

1. Throughput
   packets processed per second

2. Processing cost
   nanoseconds per packet

3. Packet-loss rate
   sent packets versus successfully processed packets

4. CPU usage
   CPU time and CPU percentage

5. Speedup
   eBPF packets/sec ÷ C++ packets/sec

6. CPU efficiency
   packets processed per CPU-second

Example final result format:

C++ libpcap throughput:     420,000 packets/sec
eBPF/XDP throughput:      1,260,000 packets/sec
eBPF speedup:                  3.00×
C++ packet cost:              2,381 ns/packet
eBPF packet cost:               794 ns/packet
C++ packet loss:               3.20%
eBPF packet loss:              0.10%

Those are only example numbers—we will generate your real numbers.
Step 1: Find the benchmark PCAP and tools

Run exactly this:

builtin cd /home/pd/Downloads/flowguard

echo "===== AVAILABLE PCAP FILES ====="

find /home/pd/Downloads/flowguard \
  -type f \
  \( -iname "*.pcap" -o -iname "*.pcapng" \) \
  -printf "%s bytes  %p\n" \
  | sort -nr \
  | head -n 20

echo
echo "===== REQUIRED TOOLS ====="

for tool in tcpreplay tcpdump perf bpftool clang cmake; do
    printf "%-12s : " "$tool"

    if command -v "$tool" >/dev/null 2>&1; then
        command -v "$tool"
    else
        echo "MISSING"
    fi
done

echo
echo "===== NETWORK INTERFACES ====="
ip -br link

Paste only that output next.

Then we will build a controlled benchmark using:

same PCAP
same packet count
same virtual interface
no terminal printing
multiple runs
median result

The benchmark will generate:

docs/ebpf_vs_cpp_benchmark.json
docs/ebpf_vs_cpp_benchmark.md
docs/ebpf_vs_cpp_runs.csv

Until that benchmark is complete, the honest project statement remains that eBPF/XDP was implemented but its speed advantage over the C++ layer has not yet been measured.


flowguard main ❯ builtin cd /home/pd/Downloads/flowguard

echo "===== AVAILABLE PCAP FILES ====="

find /home/pd/Downloads/flowguard \
  -type f \
  \( -iname "*.pcap" -o -iname "*.pcapng" \) \
  -printf "%s bytes  %p\n" \
  | sort -nr \
  | head -n 20

echo
echo "===== REQUIRED TOOLS ====="

for tool in tcpreplay tcpdump perf bpftool clang cmake; do
    printf "%-12s : " "$tool"

    if command -v "$tool" >/dev/null 2>&1; then
        command -v "$tool"
    else
        echo "MISSING"
    fi
done

echo
echo "===== NETWORK INTERFACES ====="
ip -br link
===== AVAILABLE PCAP FILES =====
24144199 bytes  /home/pd/Downloads/flowguard/data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap
144172 bytes  /home/pd/Downloads/flowguard/data/sample/real_attack.pcap
38861 bytes  /home/pd/Downloads/flowguard/capture-cpp/build/small_sample.pcap
4287 bytes  /home/pd/Downloads/flowguard/data/sample/small_sample.pcap

===== REQUIRED TOOLS =====
tcpreplay    : /usr/bin/tcpreplay
tcpdump      : /usr/bin/tcpdump
perf         : MISSING
bpftool      : /usr/bin/bpftool
clang        : /usr/bin/clang
cmake        : /usr/bin/cmake

===== NETWORK INTERFACES =====
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
wlan0            UP             30:03:c8:3c:83:c5 <BROADCAST,MULTICAST,UP,LOWER_UP>
br-14c11fcfc44a  DOWN           02:3b:46:7a:ef:84 <NO-CARRIER,BROADCAST,MULTICAST,UP>
docker0          DOWN           4e:1a:12:f3:af:d6 <NO-CARRIER,BROADCAST,MULTICAST,UP>
kdeap0           UP             32:03:c8:3c:83:c5 <BROADCAST,MULTICAST,UP,LOWER_UP>

flowguard main ❯

Good. We’ll use the 24.1 MB infected-Android PCAP as the common workload. perf is optional; bpftool can give us the eBPF program’s exact kernel runtime.

First create a fair C++ packet-parser-only benchmark. Your existing benchmark also performs flow aggregation, so it would not be a clean comparison against XDP.
1. Create the C++ parser benchmark

cat > /home/pd/Downloads/flowguard/capture-cpp/src/parser_benchmark.cpp <<'CPP'
#include "PacketParser.hpp"

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <pcap.h>
#include <string>
#include <time.h>
#include <vector>

struct StoredPacket {
    pcap_pkthdr header{};
    std::vector<u_char> data;
};

static std::uint64_t process_cpu_time_ns()
{
    timespec value{};
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &value);

    return (
        static_cast<std::uint64_t>(value.tv_sec) * 1'000'000'000ULL
        + static_cast<std::uint64_t>(value.tv_nsec)
    );
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        std::cerr
            << "Usage: " << argv[0]
            << " <pcap-file> [repetitions]\n";
        return 1;
    }

    const std::string pcap_path = argv[1];
    const int repetitions = argc >= 3
        ? std::max(1, std::stoi(argv[2]))
        : 7;

    char error_buffer[PCAP_ERRBUF_SIZE]{};

    pcap_t *handle = pcap_open_offline(
        pcap_path.c_str(),
        error_buffer
    );

    if (handle == nullptr) {
        std::cerr << "Could not open PCAP: "
                  << error_buffer << "\n";
        return 1;
    }

    std::vector<StoredPacket> packets;

    pcap_pkthdr *header = nullptr;
    const u_char *packet_data = nullptr;

    while (true) {
        const int result = pcap_next_ex(
            handle,
            &header,
            &packet_data
        );

        if (result == 1) {
            StoredPacket packet;
            packet.header = *header;

            packet.data.assign(
                packet_data,
                packet_data + header->caplen
            );

            packets.push_back(std::move(packet));
        } else if (result == -2) {
            break;
        } else if (result == -1) {
            std::cerr << "PCAP read error: "
                      << pcap_geterr(handle) << "\n";
            pcap_close(handle);
            return 1;
        }
    }

    pcap_close(handle);

    if (packets.empty()) {
        std::cerr << "PCAP contains no packets.\n";
        return 1;
    }

    PacketParser parser;

    // Warm-up run, excluded from measurements.
    std::uint64_t warmup_checksum = 0;

    for (const StoredPacket &packet : packets) {
        const auto parsed = parser.parse(
            &packet.header,
            packet.data.data()
        );

        if (parsed.has_value()) {
            warmup_checksum += parsed->packet_length;
            warmup_checksum += parsed->src_port;
            warmup_checksum += parsed->dst_port;
        }
    }

    std::vector<double> wall_ns_per_packet;
    std::vector<double> cpu_ns_per_packet;
    std::vector<double> packets_per_second;
    std::vector<double> cpu_percentages;

    std::uint64_t final_checksum = warmup_checksum;
    std::size_t parsed_packets = 0;

    std::cout << std::fixed << std::setprecision(3);
    std::cout << "Packets loaded: " << packets.size() << "\n";
    std::cout << "Repetitions: " << repetitions << "\n\n";

    for (int run = 1; run <= repetitions; ++run) {
        std::uint64_t checksum = 0;
        std::size_t parsed = 0;

        const std::uint64_t cpu_start =
            process_cpu_time_ns();

        const auto wall_start =
            std::chrono::steady_clock::now();

        for (const StoredPacket &packet : packets) {
            const auto result = parser.parse(
                &packet.header,
                packet.data.data()
            );

            if (result.has_value()) {
                ++parsed;

                checksum += result->packet_length;
                checksum += result->src_port;
                checksum += result->dst_port;
                checksum += result->tcp_flags;
                checksum += result->src_ip.size();
                checksum += result->dst_ip.size();
            }
        }

        const auto wall_end =
            std::chrono::steady_clock::now();

        const std::uint64_t cpu_end =
            process_cpu_time_ns();

        const double wall_ns =
            std::chrono::duration<double, std::nano>(
                wall_end - wall_start
            ).count();

        const double cpu_ns =
            static_cast<double>(cpu_end - cpu_start);

        const double inspected =
            static_cast<double>(packets.size());

        const double wall_cost =
            wall_ns / inspected;

        const double cpu_cost =
            cpu_ns / inspected;

        const double throughput =
            inspected * 1'000'000'000.0 / wall_ns;

        const double cpu_percentage =
            100.0 * cpu_ns / wall_ns;

        wall_ns_per_packet.push_back(wall_cost);
        cpu_ns_per_packet.push_back(cpu_cost);
        packets_per_second.push_back(throughput);
        cpu_percentages.push_back(cpu_percentage);

        parsed_packets = parsed;
        final_checksum ^= checksum;

        std::cout
            << "Run " << run
            << ": inspected=" << packets.size()
            << " parsed=" << parsed
            << " wall_ns_per_packet=" << wall_cost
            << " cpu_ns_per_packet=" << cpu_cost
            << " packets_per_second=" << throughput
            << " cpu_percent=" << cpu_percentage
            << "\n";
    }

    auto median = [](std::vector<double> values) {
        std::sort(values.begin(), values.end());
        return values[values.size() / 2];
    };

    std::cout << "\n===== C++ PARSER MEDIAN =====\n";
    std::cout
        << "CPP_TOTAL_PACKETS=" << packets.size() << "\n";
    std::cout
        << "CPP_PARSED_PACKETS=" << parsed_packets << "\n";
    std::cout
        << "CPP_MEDIAN_WALL_NS_PER_PACKET="
        << median(wall_ns_per_packet) << "\n";
    std::cout
        << "CPP_MEDIAN_CPU_NS_PER_PACKET="
        << median(cpu_ns_per_packet) << "\n";
    std::cout
        << "CPP_MEDIAN_PACKETS_PER_SECOND="
        << median(packets_per_second) << "\n";
    std::cout
        << "CPP_MEDIAN_CPU_PERCENT="
        << median(cpu_percentages) << "\n";
    std::cout
        << "CHECKSUM=" << final_checksum << "\n";

    return 0;
}
CPP

2. Register it in CMake

python - <<'PY'
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/"
    "capture-cpp/CMakeLists.txt"
)

text = path.read_text(encoding="utf-8")

marker = "# FlowGuard packet-parser-only benchmark"

if marker not in text:
    text += """

# FlowGuard packet-parser-only benchmark
add_executable(
    flowguard_parser_benchmark
    src/parser_benchmark.cpp
    src/PacketParser.cpp
)

target_link_libraries(
    flowguard_parser_benchmark
    pcap
)

target_compile_options(
    flowguard_parser_benchmark
    PRIVATE
    -O3
)
"""

    path.write_text(text, encoding="utf-8")
    print("Added flowguard_parser_benchmark.")
else:
    print("Benchmark target already exists.")
PY

3. Build it in Release mode

builtin cd /home/pd/Downloads/flowguard

cmake \
  -S capture-cpp \
  -B capture-cpp/build-benchmark \
  -DCMAKE_BUILD_TYPE=Release

cmake \
  --build capture-cpp/build-benchmark \
  --target flowguard_parser_benchmark \
  -j"$(nproc)"

4. Run seven measured repetitions

capture-cpp/build-benchmark/flowguard_parser_benchmark \
  data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap \
  7 \
  | tee docs/cpp_parser_benchmark.txt

The important output will look like:

CPP_MEDIAN_WALL_NS_PER_PACKET=...
CPP_MEDIAN_CPU_NS_PER_PACKET=...
CPP_MEDIAN_PACKETS_PER_SECOND=...
CPP_MEDIAN_CPU_PERCENT=...

After this, we will attach a silent benchmark XDP program to a temporary veth interface and obtain:

EBPF_RUNTIME_NS_PER_PACKET
EBPF_PACKETS_PER_SECOND_EQUIVALENT
EBPF_SUSTAINED_REPLAY_PPS
EBPF_PACKET_LOSS_PERCENT
EBPF_VS_CPP_SPEEDUP



flowguard main  ? ❯ capture-cpp/build-benchmark/flowguard_parser_benchmark \
  data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap \
  7 \
  | tee docs/cpp_parser_benchmark.txt
Packets loaded: 29125
Repetitions: 7

Run 1: inspected=29125 parsed=29125 wall_ns_per_packet=110.278 cpu_ns_per_packet=108.456 packets_per_second=9067962.864 cpu_percent=98.348
Run 2: inspected=29125 parsed=29125 wall_ns_per_packet=100.470 cpu_ns_per_packet=99.877 packets_per_second=9953212.213 cpu_percent=99.409
Run 3: inspected=29125 parsed=29125 wall_ns_per_packet=136.940 cpu_ns_per_packet=134.828 packets_per_second=7302474.643 cpu_percent=98.458
Run 4: inspected=29125 parsed=29125 wall_ns_per_packet=128.016 cpu_ns_per_packet=127.151 packets_per_second=7811544.511 cpu_percent=99.324
Run 5: inspected=29125 parsed=29125 wall_ns_per_packet=128.340 cpu_ns_per_packet=111.315 packets_per_second=7791799.896 cpu_percent=86.734
Run 6: inspected=29125 parsed=29125 wall_ns_per_packet=106.409 cpu_ns_per_packet=105.689 packets_per_second=9397719.895 cpu_percent=99.324
Run 7: inspected=29125 parsed=29125 wall_ns_per_packet=102.140 cpu_ns_per_packet=101.490 packets_per_second=9790435.929 cpu_percent=99.363

===== C++ PARSER MEDIAN =====
CPP_TOTAL_PACKETS=29125
CPP_PARSED_PACKETS=29125
CPP_MEDIAN_WALL_NS_PER_PACKET=110.278
CPP_MEDIAN_CPU_NS_PER_PACKET=108.456
CPP_MEDIAN_PACKETS_PER_SECOND=9067962.864
CPP_MEDIAN_CPU_PERCENT=99.324
CHECKSUM=1454654?

Your C++ baseline is now measured:

Packets:                    29,125
Median processing cost:     108.456 ns/packet CPU
Median wall cost:           110.278 ns/packet
Equivalent throughput:      9,067,963 packets/second
CPU usage:                  99.324%

The ? after CHECKSUM=1454654 is only your shell prompt, not an error.

We should not benchmark the existing XDP program directly because it updates a source map, starts dropping after 500 packets from a source, and sends events through a ring buffer. That would cause different packets to follow different execution paths.

We will create a dedicated XDP parser benchmark that parses the same Ethernet, IPv4, TCP and UDP fields without terminal or JSON overhead. Your C++ parser also performs IP-to-string conversion, which remains part of its measured userspace cost.
1. Create the eBPF benchmark program

cat > /home/pd/Downloads/flowguard/capture-ebpf/xdp_parser_benchmark.c <<'C'
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/in.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>

#include <bpf/bpf_endian.h>
#include <bpf/bpf_helpers.h>


struct benchmark_stats {
    __u64 packets;
    __u64 bytes;
    __u64 checksum;
};


/*
 * Per-CPU storage avoids lock contention while ensuring that parsed
 * values have an observable side effect and cannot be optimized away.
 */
struct {
    __uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, struct benchmark_stats);
} parser_benchmark_stats SEC(".maps");


SEC("xdp")
int xdp_parser_benchmark(struct xdp_md *context)
{
    void *packet_start =
        (void *)(long)context->data;

    void *packet_end =
        (void *)(long)context->data_end;

    struct ethhdr *ethernet_header =
        packet_start;

    if ((void *)(ethernet_header + 1) > packet_end) {
        return XDP_PASS;
    }

    if (
        ethernet_header->h_proto
        != bpf_htons(ETH_P_IP)
    ) {
        return XDP_PASS;
    }

    struct iphdr *ipv4_header =
        (void *)(ethernet_header + 1);

    if ((void *)(ipv4_header + 1) > packet_end) {
        return XDP_PASS;
    }

    if (
        ipv4_header->version != 4
        || ipv4_header->ihl < 5
    ) {
        return XDP_PASS;
    }

    __u32 ipv4_header_length =
        (__u32)ipv4_header->ihl * 4;

    if (
        (void *)ipv4_header + ipv4_header_length
        > packet_end
    ) {
        return XDP_PASS;
    }

    __u16 source_port = 0;
    __u16 destination_port = 0;

    void *transport_header =
        (void *)ipv4_header + ipv4_header_length;

    if (ipv4_header->protocol == IPPROTO_TCP) {
        struct tcphdr *tcp_header =
            transport_header;

        if ((void *)(tcp_header + 1) <= packet_end) {
            source_port =
                bpf_ntohs(tcp_header->source);

            destination_port =
                bpf_ntohs(tcp_header->dest);
        }
    } else if (
        ipv4_header->protocol == IPPROTO_UDP
    ) {
        struct udphdr *udp_header =
            transport_header;

        if ((void *)(udp_header + 1) <= packet_end) {
            source_port =
                bpf_ntohs(udp_header->source);

            destination_port =
                bpf_ntohs(udp_header->dest);
        }
    }

    __u32 stats_key = 0;

    struct benchmark_stats *stats =
        bpf_map_lookup_elem(
            &parser_benchmark_stats,
            &stats_key
        );

    if (stats != NULL) {
        stats->packets += 1;

        stats->bytes +=
            (__u64)(
                context->data_end
                - context->data
            );

        stats->checksum +=
            (__u64)ipv4_header->saddr
            + (__u64)ipv4_header->daddr
            + (__u64)source_port
            + (__u64)destination_port
            + (__u64)ipv4_header->protocol;
    }

    return XDP_PASS;
}


char program_license[] SEC("license") = "GPL";
C

2. Compile it

builtin cd /home/pd/Downloads/flowguard

clang \
  -O2 \
  -g \
  -target bpf \
  -D__TARGET_ARCH_x86 \
  -c capture-ebpf/xdp_parser_benchmark.c \
  -o capture-ebpf/xdp_parser_benchmark.o

Verify:

file capture-ebpf/xdp_parser_benchmark.o

It should report an eBPF ELF object.
3. Create the complete benchmark script

mkdir -p scripts docs/benchmark-logs

cat > scripts/benchmark_ebpf_vs_cpp.sh <<'BASH'
#!/usr/bin/env bash

set -Eeuo pipefail


ROOT="/home/pd/Downloads/flowguard"

PCAP="$ROOT/data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap"

CPP_RESULTS="$ROOT/docs/cpp_parser_benchmark.txt"

BPF_OBJECT="$ROOT/capture-ebpf/xdp_parser_benchmark.o"

CSV_OUTPUT="$ROOT/docs/ebpf_vs_cpp_runs.csv"
JSON_OUTPUT="$ROOT/docs/ebpf_vs_cpp_benchmark.json"
MARKDOWN_OUTPUT="$ROOT/docs/ebpf_vs_cpp_benchmark.md"

LOG_DIRECTORY="$ROOT/docs/benchmark-logs"

TX_INTERFACE="fgbench_tx"
RX_INTERFACE="fgbench_rx"

PIN_PATH="/sys/fs/bpf/flowguard_xdp_parser_benchmark"

RUNS=7
PCAP_LOOPS=50

ATTACH_MODE="unknown"

OLD_BPF_STATS="$(
    cat /proc/sys/kernel/bpf_stats_enabled
)"


cleanup()
{
    set +e

    sudo ip link set \
        dev "$RX_INTERFACE" \
        xdp off \
        >/dev/null 2>&1

    sudo ip link set \
        dev "$RX_INTERFACE" \
        xdpgeneric off \
        >/dev/null 2>&1

    sudo rm -f "$PIN_PATH"

    sudo ip link delete \
        "$TX_INTERFACE" \
        >/dev/null 2>&1

    sudo sysctl -q -w \
        kernel.bpf_stats_enabled="$OLD_BPF_STATS" \
        >/dev/null 2>&1
}


trap cleanup EXIT


read_program_stats()
{
    sudo bpftool -j prog show pinned "$PIN_PATH" |
        python -c '
import json
import sys

data = json.load(sys.stdin)

if isinstance(data, list):
    data = data[0]

print(
    int(data.get("run_time_ns", 0)),
    int(data.get("run_cnt", 0)),
)
'
}


mkdir -p "$LOG_DIRECTORY"

for required_file in \
    "$PCAP" \
    "$CPP_RESULTS" \
    "$BPF_OBJECT"
do
    if [[ ! -f "$required_file" ]]; then
        echo "Missing required file: $required_file" >&2
        exit 1
    fi
done


for required_command in \
    bpftool \
    clang \
    ip \
    python \
    tcpreplay
do
    if ! command -v "$required_command" >/dev/null 2>&1; then
        echo "Missing command: $required_command" >&2
        exit 1
    fi
done


CPP_TOTAL_PACKETS="$(
    awk -F= '
        /^CPP_TOTAL_PACKETS=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"

CPP_CPU_NS="$(
    awk -F= '
        /^CPP_MEDIAN_CPU_NS_PER_PACKET=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"

CPP_WALL_NS="$(
    awk -F= '
        /^CPP_MEDIAN_WALL_NS_PER_PACKET=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"

CPP_PPS="$(
    awk -F= '
        /^CPP_MEDIAN_PACKETS_PER_SECOND=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"


if [[ -z "$CPP_TOTAL_PACKETS" ]]; then
    echo "Could not read C++ packet count." >&2
    exit 1
fi


EXPECTED_PACKETS=$(
    (
        CPP_TOTAL_PACKETS
        * PCAP_LOOPS
    )
)


echo "C++ packets per PCAP: $CPP_TOTAL_PACKETS"
echo "PCAP loops per run: $PCAP_LOOPS"
echo "Expected packets per run: $EXPECTED_PACKETS"
echo "eBPF measured runs: $RUNS"
echo


sudo -v

sudo sysctl -q -w \
    kernel.bpf_stats_enabled=1


if ! mountpoint -q /sys/fs/bpf; then
    echo "/sys/fs/bpf is not mounted." >&2
    exit 1
fi


sudo ip link delete \
    "$TX_INTERFACE" \
    >/dev/null 2>&1 || true

sudo rm -f "$PIN_PATH"


sudo ip link add \
    "$TX_INTERFACE" \
    type veth \
    peer name "$RX_INTERFACE"

sudo ip link set "$TX_INTERFACE" up
sudo ip link set "$RX_INTERFACE" up


sudo bpftool prog load \
    "$BPF_OBJECT" \
    "$PIN_PATH" \
    type xdp


if sudo ip link set \
    dev "$RX_INTERFACE" \
    xdp pinned "$PIN_PATH" \
    2>"$LOG_DIRECTORY/native-attach-error.txt"
then
    ATTACH_MODE="native"
else
    echo "Native XDP attach failed; trying generic XDP."

    sudo ip link set \
        dev "$RX_INTERFACE" \
        xdpgeneric pinned "$PIN_PATH"

    ATTACH_MODE="generic"
fi


echo "XDP attach mode: $ATTACH_MODE"
echo


printf '%s\n' \
    "run,expected_packets,xdp_run_count,runtime_ns,wall_seconds,kernel_ns_per_packet,kernel_equivalent_pps,replay_pps,delivery_percent" \
    > "$CSV_OUTPUT"


for run_number in $(seq 1 "$RUNS"); do
    read -r runtime_before count_before \
        < <(read_program_stats)

    start_time_ns="$(date +%s%N)"

    sudo tcpreplay \
        --intf1="$TX_INTERFACE" \
        --topspeed \
        --preload-pcap \
        --loop="$PCAP_LOOPS" \
        "$PCAP" \
        >"$LOG_DIRECTORY/tcpreplay-run-${run_number}.txt" \
        2>&1

    end_time_ns="$(date +%s%N)"

    # Allow final ingress processing to complete before reading counters.
    sleep 0.2

    read -r runtime_after count_after \
        < <(read_program_stats)

    runtime_delta=$(
        (
            runtime_after
            - runtime_before
        )
    )

    count_delta=$(
        (
            count_after
            - count_before
        )
    )

    wall_time_ns=$(
        (
            end_time_ns
            - start_time_ns
        )
    )

    if (( count_delta <= 0 )); then
        echo "Run $run_number received zero XDP packets." >&2
        exit 1
    fi

    metrics="$(
        awk \
            -v runtime="$runtime_delta" \
            -v packets="$count_delta" \
            -v wall="$wall_time_ns" \
            -v expected="$EXPECTED_PACKETS" \
            'BEGIN {
                kernel_ns = runtime / packets
                kernel_pps = 1000000000 / kernel_ns
                wall_seconds = wall / 1000000000
                replay_pps = packets / wall_seconds
                delivery = 100 * packets / expected

                printf "%.9f %.3f %.3f %.3f %.6f",
                    wall_seconds,
                    kernel_ns,
                    kernel_pps,
                    replay_pps,
                    delivery
            }'
    )"

    read -r \
        wall_seconds \
        kernel_ns_per_packet \
        kernel_equivalent_pps \
        replay_pps \
        delivery_percent \
        <<< "$metrics"

    printf '%s\n' \
        "$run_number,$EXPECTED_PACKETS,$count_delta,$runtime_delta,$wall_seconds,$kernel_ns_per_packet,$kernel_equivalent_pps,$replay_pps,$delivery_percent" \
        >> "$CSV_OUTPUT"

    echo \
        "Run $run_number: " \
        "xdp_packets=$count_delta " \
        "kernel_ns_per_packet=$kernel_ns_per_packet " \
        "kernel_equivalent_pps=$kernel_equivalent_pps " \
        "replay_pps=$replay_pps " \
        "delivery=$delivery_percent%"
done


python - \
    "$CSV_OUTPUT" \
    "$JSON_OUTPUT" \
    "$MARKDOWN_OUTPUT" \
    "$CPP_TOTAL_PACKETS" \
    "$CPP_CPU_NS" \
    "$CPP_WALL_NS" \
    "$CPP_PPS" \
    "$ATTACH_MODE" \
    "$PCAP_LOOPS" \
    <<'PY'
import csv
import json
import statistics
import sys
from pathlib import Path


(
    csv_path,
    json_path,
    markdown_path,
    cpp_packets,
    cpp_cpu_ns,
    cpp_wall_ns,
    cpp_pps,
    attach_mode,
    pcap_loops,
) = sys.argv[1:]


with Path(csv_path).open(
    "r",
    encoding="utf-8",
    newline="",
) as file:
    rows = list(csv.DictReader(file))


def values(column: str) -> list[float]:
    return [
        float(row[column])
        for row in rows
    ]


ebpf_kernel_ns = statistics.median(
    values("kernel_ns_per_packet")
)

ebpf_kernel_pps = statistics.median(
    values("kernel_equivalent_pps")
)

ebpf_replay_pps = statistics.median(
    values("replay_pps")
)

delivery_percent = statistics.median(
    values("delivery_percent")
)

cpp_cpu_ns_value = float(cpp_cpu_ns)
cpp_wall_ns_value = float(cpp_wall_ns)
cpp_pps_value = float(cpp_pps)

cpu_cost_speedup = (
    cpp_cpu_ns_value / ebpf_kernel_ns
)

wall_cost_speedup = (
    cpp_wall_ns_value / ebpf_kernel_ns
)

equivalent_throughput_speedup = (
    ebpf_kernel_pps / cpp_pps_value
)

packet_loss_percent = max(
    0.0,
    100.0 - delivery_percent,
)


report = {
    "workload": {
        "pcap": (
            "2025-10-02-traffic-from-infected-Android-phone.pcap"
        ),
        "packets_per_loop": int(cpp_packets),
        "pcap_loops_per_run": int(pcap_loops),
        "measured_runs": len(rows),
    },
    "cpp_parser": {
        "median_cpu_ns_per_packet": cpp_cpu_ns_value,
        "median_wall_ns_per_packet": cpp_wall_ns_value,
        "median_packets_per_second": cpp_pps_value,
    },
    "ebpf_xdp_parser": {
        "attach_mode": attach_mode,
        "median_kernel_ns_per_packet": ebpf_kernel_ns,
        "median_kernel_equivalent_pps": ebpf_kernel_pps,
        "median_sustained_replay_pps": ebpf_replay_pps,
        "median_delivery_percent": delivery_percent,
        "median_packet_loss_percent": packet_loss_percent,
    },
    "comparison": {
        "cpu_cost_speedup_x": cpu_cost_speedup,
        "wall_cost_speedup_x": wall_cost_speedup,
        "equivalent_throughput_speedup_x": (
            equivalent_throughput_speedup
        ),
        "kernel_cost_reduction_percent": (
            100.0
            * (
                1.0
                - ebpf_kernel_ns / cpp_cpu_ns_value
            )
        ),
    },
}


Path(json_path).write_text(
    json.dumps(report, indent=2),
    encoding="utf-8",
)


markdown = f"""# FlowGuard eBPF/XDP vs C++ Parser Benchmark

## Workload

- PCAP packets: {int(cpp_packets):,}
- PCAP loops per eBPF run: {int(pcap_loops)}
- Measured runs: {len(rows)}
- XDP attachment mode: `{attach_mode}`

## Median results

| Metric | C++ parser | eBPF/XDP parser |
|---|---:|---:|
| Processing cost | {cpp_cpu_ns_value:,.3f} ns/packet | {ebpf_kernel_ns:,.3f} ns/packet |
| Equivalent throughput | {cpp_pps_value:,.0f} packets/s | {ebpf_kernel_pps:,.0f} packets/s |
| Sustained replay throughput | Not measured | {ebpf_replay_pps:,.0f} packets/s |
| Packet delivery | Not applicable | {delivery_percent:.4f}% |
| Packet loss | Not applicable | {packet_loss_percent:.4f}% |

## Comparison

- eBPF processing-cost speedup: **{cpu_cost_speedup:.2f}×**
- Equivalent-throughput speedup: **{equivalent_throughput_speedup:.2f}×**
- Kernel processing-cost reduction: **{report["comparison"]["kernel_cost_reduction_percent"]:.2f}%**

## Interpretation

The processing-cost comparison measures the average runtime of the
XDP parser in the kernel against the measured CPU cost of the C++
userspace packet parser.

The sustained replay value measures the complete test path, including
tcpreplay, the virtual Ethernet pair, kernel scheduling and XDP.

These metrics do not include FlowGuard ML inference or database work.
"""


Path(markdown_path).write_text(
    markdown,
    encoding="utf-8",
)


print("\n===== FINAL BENCHMARK =====")
print(
    f"C++ CPU cost:            "
    f"{cpp_cpu_ns_value:.3f} ns/packet"
)
print(
    f"eBPF kernel cost:        "
    f"{ebpf_kernel_ns:.3f} ns/packet"
)
print(
    f"eBPF cost speedup:       "
    f"{cpu_cost_speedup:.2f}x"
)
print(
    f"C++ equivalent PPS:      "
    f"{cpp_pps_value:,.0f}"
)
print(
    f"eBPF equivalent PPS:     "
    f"{ebpf_kernel_pps:,.0f}"
)
print(
    f"Throughput speedup:      "
    f"{equivalent_throughput_speedup:.2f}x"
)
print(
    f"Sustained replay PPS:    "
    f"{ebpf_replay_pps:,.0f}"
)
print(
    f"Delivery rate:           "
    f"{delivery_percent:.4f}%"
)
print(
    f"Packet-loss rate:        "
    f"{packet_loss_percent:.4f}%"
)

print(f"\nSaved CSV:      {csv_path}")
print(f"Saved JSON:     {json_path}")
print(f"Saved Markdown: {markdown_path}")
PY
BASH

4. Run it

chmod +x scripts/benchmark_ebpf_vs_cpp.sh

./scripts/benchmark_ebpf_vs_cpp.sh

This will ask for your sudo password and run seven eBPF measurements of approximately 1,456,250 packets each.

The final output will directly state:

eBPF cost speedup:       ...x
Throughput speedup:      ...x
Sustained replay PPS:    ...
Packet-loss rate:        ...%

Paste the ===== FINAL BENCHMARK ===== section after it finishes.

Pasted text(11).txt
Document
?

The script has invalid Bash arithmetic blocks. It used:

$(
    (
        CPP_TOTAL_PACKETS * PCAP_LOOPS
    )
)

Bash interpreted CPP_TOTAL_PACKETS as a command, causing the errors shown.

Patch all four arithmetic blocks:

builtin cd /home/pd/Downloads/flowguard

python - <<'PY'
from pathlib import Path
import re

path = Path("scripts/benchmark_ebpf_vs_cpp.sh")
text = path.read_text(encoding="utf-8")

replacements = {
    r'''EXPECTED_PACKETS=\$\(\s*
        \(\s*
            CPP_TOTAL_PACKETS\s*
            \*\s*
            PCAP_LOOPS\s*
        \)\s*
    \)''': 'EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS))',

    r'''runtime_delta=\$\(\s*
        \(\s*
            runtime_after\s*
            -\s*
            runtime_before\s*
        \)\s*
    \)''': 'runtime_delta=$((runtime_after - runtime_before))',

    r'''count_delta=\$\(\s*
        \(\s*
            count_after\s*
            -\s*
            count_before\s*
        \)\s*
    \)''': 'count_delta=$((count_after - count_before))',

    r'''wall_time_ns=\$\(\s*
        \(\s*
            end_time_ns\s*
            -\s*
            start_time_ns\s*
        \)\s*
    \)''': 'wall_time_ns=$((end_time_ns - start_time_ns))',
}

total = 0

for pattern, replacement in replacements.items():
    text, count = re.subn(
        pattern,
        replacement,
        text,
        flags=re.VERBOSE,
    )
    total += count
    print(f"Patched: {replacement} ({count})")

if total != 4:
    raise SystemExit(
        f"Expected to patch 4 arithmetic blocks, patched {total}"
    )

path.write_text(text, encoding="utf-8")
print(f"\nUpdated: {path}")
PY

Check the script:

bash -n scripts/benchmark_ebpf_vs_cpp.sh &&
echo "Bash syntax is valid"

Confirm the corrected lines:

grep -nE \
  'EXPECTED_PACKETS=|runtime_delta=|count_delta=|wall_time_ns=' \
  scripts/benchmark_ebpf_vs_cpp.sh

You should see:

EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS))
runtime_delta=$((runtime_after - runtime_before))
count_delta=$((count_after - count_before))
wall_time_ns=$((end_time_ns - start_time_ns))

Then run the benchmark again:

./scripts/benchmark_ebpf_vs_cpp.sh

Your established C++ baseline remains:

CPU cost:       108.456 ns/packet
Wall cost:      110.278 ns/packet
Throughput:     9,067,963 packets/second

The script will now measure the eBPF side and calculate the actual speedup.



flowguard main  ? ❯ chmod +x scripts/benchmark_ebpf_vs_cpp.sh

./scripts/benchmark_ebpf_vs_cpp.sh
./scripts/benchmark_ebpf_vs_cpp.sh: line 156: CPP_TOTAL_PACKETS: command not found
./scripts/benchmark_ebpf_vs_cpp.sh: line 157: capture-cpp: command not found
[sudo] password for pd:

flowguard main  ? ✗
flowguard main  ? ✗ builtin cd /home/pd/Downloads/flowguard

python - <<'PY'
from pathlib import Path
import re

path = Path("scripts/benchmark_ebpf_vs_cpp.sh")
text = path.read_text(encoding="utf-8")

replacements = {
    r'''EXPECTED_PACKETS=\$\(\s*
        \(\s*
            CPP_TOTAL_PACKETS\s*
            \*\s*
            PCAP_LOOPS\s*
        \)\s*
    \)''': 'EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS))',

    r'''runtime_delta=\$\(\s*
        \(\s*
            runtime_after\s*
            -\s*
            runtime_before\s*
        \)\s*
    \)''': 'runtime_delta=$((runtime_after - runtime_before))',

    r'''count_delta=\$\(\s*
        \(\s*
            count_after\s*
            -\s*
            count_before\s*
        \)\s*
    \)''': 'count_delta=$((count_after - count_before))',

    r'''wall_time_ns=\$\(\s*
        \(\s*
            end_time_ns\s*
            -\s*
            start_time_ns\s*
        \)\s*
    \)''': 'wall_time_ns=$((end_time_ns - start_time_ns))',
}

total = 0

for pattern, replacement in replacements.items():
    text, count = re.subn(
        pattern,
        replacement,
        text,
        flags=re.VERBOSE,
    )
    total += count
    print(f"Patched: {replacement} ({count})")

if total != 4:
    raise SystemExit(
        f"Expected to patch 4 arithmetic blocks, patched {total}"
    )

path.write_text(text, encoding="utf-8")
print(f"\nUpdated: {path}")
PY
Patched: EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS)) (1)
Patched: runtime_delta=$((runtime_after - runtime_before)) (1)
Patched: count_delta=$((count_after - count_before)) (1)
Patched: wall_time_ns=$((end_time_ns - start_time_ns)) (1)

Updated: scripts/benchmark_ebpf_vs_cpp.sh

flowguard main  ? ❯ bash -n scripts/benchmark_ebpf_vs_cpp.sh &&
echo "Bash syntax is valid"
Bash syntax is valid

flowguard main  ? ❯ grep -nE \
  'EXPECTED_PACKETS=|runtime_delta=|count_delta=|wall_time_ns=' \
  scripts/benchmark_ebpf_vs_cpp.sh
151:EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS))
244:    runtime_delta=$((runtime_after - runtime_before))
246:    count_delta=$((count_after - count_before))
248:    wall_time_ns=$((end_time_ns - start_time_ns))?

Yes, the four arithmetic lines are fixed correctly.

The final ? you typed is most likely just your question, not part of the script. Verify the actual line once:

sed -n '248p' scripts/benchmark_ebpf_vs_cpp.sh | cat -A

Correct output should end like this:

    wall_time_ns=$((end_time_ns - start_time_ns))$

Then run the benchmark:

./scripts/benchmark_ebpf_vs_cpp.sh

It will:

    create temporary fgbench_tx and fgbench_rx interfaces,

    attach the XDP benchmark,

    replay about 1,456,250 packets per run,

    perform seven runs,

    clean up the XDP program and interfaces automatically.

Paste the output beginning from:

XDP attach mode:

through:

===== FINAL BENCHMARK =====



flowguard main  ? ❯ sed -n '248p' scripts/benchmark_ebpf_vs_cpp.sh | cat -A
    wall_time_ns=$((end_time_ns - start_time_ns))$

flowguard main  ? ❯ ./scripts/benchmark_ebpf_vs_cpp.sh
C++ packets per PCAP: 29125
PCAP loops per run: 50
Expected packets per run: 1456250
eBPF measured runs: 7

XDP attach mode: native

Run 1:  xdp_packets=1456269  kernel_ns_per_packet=56.326  kernel_equivalent_pps=17753819.371  replay_pps=349222.638  delivery=100.001305%
Run 2:  xdp_packets=1456251  kernel_ns_per_packet=65.205  kernel_equivalent_pps=15336273.136  replay_pps=302079.975  delivery=100.000069%
Run 3:  xdp_packets=1456251  kernel_ns_per_packet=55.595  kernel_equivalent_pps=17987284.688  replay_pps=353057.518  delivery=100.000069%
Run 4:  xdp_packets=1456250  kernel_ns_per_packet=62.301  kernel_equivalent_pps=16051174.705  replay_pps=316329.887  delivery=100.000000%
Run 5:  xdp_packets=1456250  kernel_ns_per_packet=62.830  kernel_equivalent_pps=15915903.263  replay_pps=313105.650  delivery=100.000000%
Run 6:  xdp_packets=1456251  kernel_ns_per_packet=61.371  kernel_equivalent_pps=16294299.064  replay_pps=320640.357  delivery=100.000069%
Run 7:  xdp_packets=1456250  kernel_ns_per_packet=64.625  kernel_equivalent_pps=15473868.289  replay_pps=306540.196  delivery=100.000000%

===== FINAL BENCHMARK =====
C++ CPU cost:            108.456 ns/packet
eBPF kernel cost:        62.301 ns/packet
eBPF cost speedup:       1.74x
C++ equivalent PPS:      9,067,963
eBPF equivalent PPS:     16,051,175
Throughput speedup:      1.77x
Sustained replay PPS:    316,330
Delivery rate:           100.0001%
Packet-loss rate:        0.0000%

Saved CSV:      /home/pd/Downloads/flowguard/docs/ebpf_vs_cpp_runs.csv
Saved JSON:     /home/pd/Downloads/flowguard/docs/ebpf_vs_cpp_benchmark.json
Saved Markdown: /home/pd/Downloads/flowguard/docs/ebpf_vs_cpp_benchmark.md

Your benchmark is successful. Native XDP/eBPF is measurably faster than the C++ userspace parser on your machine.
Final metrics
Metric	C++ parser	eBPF/XDP parser
Processing cost	108.456 ns/packet	62.301 ns/packet
Equivalent throughput	9.07 million packets/s	16.05 million packets/s
Sustained replay throughput	—	316,330 packets/s
Packet loss	—	0.0000%
Improvement

    eBPF processing speedup: 1.74×

    eBPF throughput speedup: 1.77×

    Processing-cost reduction: approximately 42.6%

    Throughput increase: approximately 77%

    XDP attachment mode: native

    Packets tested: about 1.456 million per run

    Measured runs: 7

Simple meaning

For every packet:

C++ userspace parser: 108.456 nanoseconds
eBPF/XDP parser:       62.301 nanoseconds

So the eBPF parser used roughly 46 fewer nanoseconds per packet.

At its measured processing cost:

C++:   ~9.07 million packets/second
eBPF: ~16.05 million packets/second

Therefore, your defensible claim is:

    FlowGuard’s native XDP/eBPF packet-processing layer achieved 1.74× lower per-packet processing cost and 1.77× higher equivalent throughput than its C++ userspace parser, processing packets in 62.3 ns versus 108.5 ns across seven benchmark runs.

Important interpretation

The 316,330 packets/s sustained replay rate is not the maximum eBPF processing capacity. It measures the entire testing pipeline:

PCAP → tcpreplay → veth interface → Linux networking → XDP

That result is mainly limited by replay generation, virtual interfaces and kernel scheduling.

The 16.05 million packets/s figure is the parser’s runtime-equivalent throughput, calculated from its measured kernel execution cost.

The delivery rate slightly exceeding 100%:

100.0001%

means a few extra background/control packets crossed the virtual interface. It does not mean more PCAP packets were magically created. Report packet loss as approximately 0%, not delivery above 100%.
Resume version

    Benchmarked FlowGuard’s native XDP/eBPF packet parser against a C++ userspace parser across seven runs and 1.45M+ packets per run, achieving 1.77× higher equivalent throughput, 42.6% lower per-packet processing cost, and approximately zero packet loss.

Your benchmark evidence is saved in:

docs/ebpf_vs_cpp_runs.csv
docs/ebpf_vs_cpp_benchmark.json
docs/ebpf_vs_cpp_benchmark.md


now make a final md with full detils od bproject with all keywrda and metrices for my resime ,, full detiled md

Created the complete 1,300-line FlowGuard resume and portfolio dossier with:

    Resume-ready 1-line, 3-bullet, 4-bullet, and detailed versions

    Full architecture and component explanation

    C++17/libpcap, eBPF/XDP, FastAPI, ML, PostgreSQL, Redis, Prisma, Docker, and Nginx details

    Real CICIDS2017 methodology and verified model metrics

    Complete confusion-matrix and attack-family analysis

    XDP vs C++ benchmark metrics

    ATS keyword bank

    Role-specific bullets for software, backend, ML, and cybersecurity jobs

    Interview walkthroughs and technical talking points

    Safe claims and claims to avoid

    Future improvements and portfolio description

The document uses the defensible real-data headline rather than the older synthetic result, and includes the verified capture-day-separated methodology and ensemble trade-offs. It also reflects the verified repository architecture and Docker stack.


now also ehlp me write detaield readme # FlowGuard

FlowGuard is a network-flow anomaly detection project with four main parts:

- capture-cpp: C++ packet-to-flow aggregation
- ml-service: FastAPI inference service backed by PostgreSQL and Redis
- dashboard: static HTML dashboard served by Nginx
- docker-compose.yml: end-to-end local stack definition

This README reflects the setup verified on Friday, July 17, 2026.

## What It Does

FlowGuard reads captured network flows, extracts security features, and scores
them with an ensemble of:

- Isolation Forest for unsupervised anomaly detection
- Random Forest for supervised attack classification
- PyTorch Autoencoder for reconstruction-error anomaly detection

An alert is raised when at least 2 of the 3 models vote anomalous.

## Verified Status

Verified on Friday, July 17, 2026:

- docker compose up -d --build succeeds
- API health check returns 200 at http://127.0.0.1:8000/health
- Dashboard returns 200 at http://127.0.0.1:8080
- GET /flows/recent returns captured sample flow data
- Python tests pass: 8 passed
- Held-out evaluation completed on ml-service/data/sample/test_holdout.csv

## Project Layout

text
flowguard/
├── capture-cpp/
├── capture-ebpf/
├── dashboard/
├── data/
├── docs/
├── ml-service/
├── docker-compose.yml
└── HOW_TO_RUN.md



## Quick Start

bash
docker compose up -d --build



Then check:

bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/flows/recent?limit=2



Open:

- Dashboard: 
http://127.0.0.1:8080
- API docs: http://127.0.0.1:8000/docs

## Render Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/puneetdixit200/flowguard)

This repo includes `render.yaml` for one Docker web service, one Render Postgres database, and one Render Key Value instance. The hosted service serves the dashboard at `/` and the API at the same origin.

Free Render limits apply: the web service can spin down after idle time, Free Postgres expires after 30 days, and Free Key Value does not persist data across restarts.

Notes:

- PostgreSQL and Redis are intentionally not published to host ports in
  docker-compose.yml. They are only used internally by the compose network.
- The ML container waits for Postgres and Redis, runs prisma db push, then
  starts Uvicorn.
- First startup of ml-service takes a few extra seconds because Prisma
  generates its client during container boot.

## Manual Run

If you want to run only the API locally:

bash
cd ml-service
PYTHONPATH=. .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000



If you want to evaluate the saved models locally:

bash
cd ml-service
PYTHONPATH=. .venv/bin/python training/evaluate_models.py



## Test Results

Python API tests:

bash
cd ml-service
PYTHONPATH=. .venv/bin/python -m pytest tests -q



Verified result on Friday, July 17, 2026:

text
8 passed



## Model Metrics

Held-out test set: 
940 rows total

- Benign: 830
- Attacks: 110

Ensemble results:

- Accuracy: 0.9894
- Precision: 0.9630
- Recall: 0.9455
- F1: 0.9541
- False positives: 4
- False negatives: 6

Full report: [docs/evaluation_report.txt](/home/pd/Downloads/flowguard/docs/evaluation_report.txt)

Additional model notes:

- [docs/ml-models.md](/home/pd/Downloads/flowguard/docs/ml-models.md)
- [docs/false-positive-analysis.md](/home/pd/Downloads/flowguard/docs/false-positive-analysis.md)
- [docs/case-study.md](/home/pd/Downloads/flowguard/docs/case-study.md)
- [docs/threading-model.md](/home/pd/Downloads/flowguard/docs/threading-model.md)

## API Endpoints

- GET /health
- GET /flows/recent?limit=20
- POST /analyze
- GET /alerts
- GET /alerts/{alert_id}
- GET /metrics/model
- POST /analyse/real

## Docker Notes

Docker-specific fixes applied and verified:

- dashboard/Dockerfile now serves the existing static dashboard with Nginx
  instead of expecting a missing React/Vite build pipeline
- ml-service/Dockerfile installs CPU-only PyTorch wheels instead of pulling
  large default GPU stacks
- ml-service waits for Postgres and Redis before startup
- Redis host and port are environment-driven, so the service works in compose
- Prisma client generation is built into the image and refreshed at container
  startup after schema sync
- .dockerignore files prevent local build outputs and virtualenv contents from
  bloating the image contexts

I created a complete, professional GitHub README that updates the older README’s three-model prototype description and historical 98.94% result with the latest real-data evaluation, shadow-mode routes, four-model research pipeline, and XDP benchmark.

It includes:

    Project overview and table of contents

    Verified ML and XDP performance metrics

    Full system architecture

    C++ capture and flow-aggregation design

    eBPF/XDP implementation

    All 11 engineered features

    CICIDS2017 capture-day-separated methodology

    Individual model and ensemble results

    Confusion matrices and attack-family analysis

    Legacy versus real-model distinction

    Shadow-mode API documentation

    Docker Compose and manual setup instructions

    C++ and Python testing commands

    Benchmark reproduction instructions

    Limitations, honest claims, roadmap, resume bullets, and ATS keywords

    Portable relative paths instead of /home/pd/... links

The API section also covers the newly added real-model and comparison routes present in the current backend. The deployment section reflects the five-service PostgreSQL, Redis, capture, ML, and dashboard Compose architecture.

Replace the repository’s existing README.md with this file before committing.


Library
/
PROJECT 1
/FlowGuard_Detailed_README.md

# FlowGuard

> A full-stack network intrusion detection and traffic-analysis platform built with C++17, native XDP/eBPF, FastAPI, scikit-learn, PyTorch, PyTorch Geometric, PostgreSQL, Redis, Prisma ORM, Docker Compose, and Nginx.

FlowGuard converts raw network packets into flow-level security telemetry, evaluates each flow using multiple machine-learning approaches, and exposes the resulting detections through a REST API and monitoring dashboard.

The project combines three engineering areas:

- **Systems and networking:** C++ packet parsing, multithreading, flow aggregation, libpcap, Linux networking, native XDP/eBPF, BPF maps, and ring buffers.
- **Machine learning:** Random Forest, Isolation Forest, Autoencoder, GraphSAGE, feature engineering, threshold tuning, capture-day-separated evaluation, and ensemble analysis.
- **Backend and infrastructure:** FastAPI, PostgreSQL, Prisma ORM, Redis pub/sub, Docker Compose, Nginx, health checks, persistence, and shadow deployment.

---

## Table of Contents

- [Highlights](#highlights)
- [Verified Results](#verified-results)
- [What FlowGuard Does](#what-flowguard-does)
- [Architecture](#architecture)
- [Project Components](#project-components)
- [Network Features](#network-features)
- [Machine-Learning Models](#machine-learning-models)
- [Dataset and Evaluation Methodology](#dataset-and-evaluation-methodology)
- [Real-Data Model Results](#real-data-model-results)
- [eBPF/XDP Performance Benchmark](#ebpfxdp-performance-benchmark)
- [Live Shadow-Mode Evaluation](#live-shadow-mode-evaluation)
- [Project Layout](#project-layout)
- [Requirements](#requirements)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Manual C++ Capture Run](#manual-c-capture-run)
- [Manual FastAPI Run](#manual-fastapi-run)
- [eBPF/XDP Build and Run](#ebpfxdp-build-and-run)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Benchmark Reproduction](#benchmark-reproduction)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Generated Artifacts](#generated-artifacts)
- [Docker and Infrastructure Notes](#docker-and-infrastructure-notes)
- [Design Decisions](#design-decisions)
- [Limitations and Honest Interpretation](#limitations-and-honest-interpretation)
- [Roadmap](#roadmap)
- [Resume-Ready Summary](#resume-ready-summary)
- [Technology Keywords](#technology-keywords)

---

## Highlights

- Multithreaded **C++17/libpcap** packet-to-flow processing pipeline.
- Ethernet, IPv4, TCP, UDP, and ICMP parsing.
- Bounded producer-consumer queue with backpressure.
- Five-tuple flow aggregation and TCP flag statistics.
- Native **XDP/eBPF** packet parsing and early filtering.
- Kernel-to-userspace communication through a BPF ring buffer.
- FastAPI inference service with batch analysis and alert persistence.
- PostgreSQL-backed alert storage through Prisma ORM.
- Redis-based internal messaging/pub-sub support.
- Random Forest, Isolation Forest, PyTorch Autoencoder, and GraphSAGE.
- Real CICIDS2017 training and capture-day-separated final evaluation.
- Validation-selected Random Forest operating thresholds.
- Shadow deployment and legacy-versus-real model comparison.
- Reproducible C++ versus XDP performance benchmark.
- Docker Compose orchestration for the complete local stack.

---

## Verified Results

### Real-data intrusion-detection result

The strongest individual model was Random Forest:

| Metric | Result |
|---|---:|
| Test flows | 10,000 |
| Benign flows | 5,000 |
| Attack flows | 5,000 |
| Accuracy | **86.09%** |
| Precision | **78.71%** |
| Recall | **98.94%** |
| F1 score | **0.8767** |
| ROC-AUC | **0.9036** |
| False positives | 1,338 |
| False negatives | 53 |

The test data was separated by capture day from the training and validation data.

### Native XDP/eBPF performance result

| Metric | C++ userspace parser | Native XDP/eBPF parser |
|---|---:|---:|
| Processing cost | 108.456 ns/packet | **62.301 ns/packet** |
| Equivalent throughput | 9.07 million packets/s | **16.05 million packets/s** |
| Processing-cost reduction | — | **42.6%** |
| Equivalent-throughput improvement | — | **1.77×** |
| Sustained complete replay path | — | 316,330 packets/s |
| Observed packet loss | — | approximately 0% |

The XDP benchmark used seven measured runs and approximately 1.46 million replayed packets per run.

### Four-model ensemble result

The strict four-model ensemble prioritized agreement and reduced false alarms:

| Metric | Result |
|---|---:|
| Accuracy | 84.71% |
| Precision | **86.96%** |
| Recall | 81.66% |
| F1 score | 0.8423 |
| False positives | 612 |
| False negatives | 917 |
| False-positive reduction vs Random Forest | **54.3%** |

The ensemble improved precision and reduced false positives, but it also missed more attacks. Random Forest therefore remains the strongest general headline model.

---

## What FlowGuard Does

FlowGuard implements the following pipeline:

1. Read packets from a PCAP file or inspect live ingress traffic.
2. Validate Ethernet and IPv4 headers.
3. Parse TCP, UDP, ICMP, ports, lengths, timestamps, and TCP flags.
4. Convert packets into a structured `PacketInfo` representation.
5. Group packets into flows using a network five-tuple.
6. Calculate duration, traffic volume, rate, and TCP-behaviour features.
7. Emit completed flows as JSON Lines.
8. Load the flows into a FastAPI inference service.
9. Score each flow with one or more detection models.
10. Compare model decisions in shadow mode.
11. Optionally persist alerts in PostgreSQL.
12. Expose flows, alerts, metrics, and health state through REST endpoints.
13. Display operational data through an Nginx-served dashboard.

---

## Architecture

```text
                         ┌──────────────────────────────┐
                         │ PCAP replay or live traffic  │
                         └──────────────┬───────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ C++17/libpcap capture  │              │ Native XDP/eBPF path   │
        │ Userspace packet path  │              │ Kernel ingress path    │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ PacketParser           │              │ BPF maps / ring buffer │
        │ Ethernet/IP/TCP/UDP    │              │ pass/drop/event output │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     └───────────────────┬───────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Five-tuple aggregation │
                            │ Packet/byte/TCP stats  │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ JSONL feature pipeline │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ FastAPI ML service     │
                            │ Normalization/scoring  │
                            └────────────┬───────────┘
                                         ▼
          ┌──────────────────────────────────────────────────────────┐
          │ Random Forest │ Isolation Forest │ Autoencoder │ GraphSAGE │
          └──────────────────────────────┬───────────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Shadow comparison /    │
                            │ voting / alert logic   │
                            └────────────┬───────────┘
                                         ▼
                  ┌──────────────────────┴──────────────────────┐
                  ▼                                             ▼
        ┌────────────────────────┐                  ┌────────────────────────┐
        │ PostgreSQL + Prisma    │                  │ Redis pub/sub          │
        │ Durable alert storage  │                  │ Internal notifications │
        └────────────┬───────────┘                  └────────────┬───────────┘
                     └───────────────────┬───────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Nginx dashboard        │
                            │ Flows/alerts/metrics   │
                            └────────────────────────┘
```

---

## Project Components

### `capture-cpp`

The C++17 layer is responsible for packet parsing and flow aggregation.

Key responsibilities:

- Open PCAP files through libpcap.
- Parse Ethernet and IPv4 packet structure.
- Extract transport protocol and ports.
- Record packet size and nanosecond timestamp representation.
- Extract TCP SYN, ACK, FIN, and RST flags.
- Send parsed packets through a bounded blocking queue.
- Aggregate packets into flows.
- Write completed flow records to JSONL.

Concurrency model:

```text
Capture thread
    │
    ▼
BlockingQueue<PacketInfo>
    │
    ▼
Aggregation thread
```

The bounded queue provides backpressure when aggregation is slower than capture and prevents unrestricted memory growth.

### `capture-ebpf`

The eBPF layer performs packet inspection at the Linux XDP hook.

Implemented concepts:

- Native XDP attachment.
- Safe packet-bound checks required by the eBPF verifier.
- Ethernet and IPv4 parsing.
- Variable-length IPv4 header handling.
- TCP and UDP port extraction.
- Per-source tracking through BPF maps.
- Demonstration early-drop action.
- BPF ring-buffer event transfer.
- libbpf userspace loader.
- Signal-based cleanup and XDP detach.
- Dedicated silent benchmark program.

### `ml-service`

The Python service provides:

- Flow normalization.
- Feature generation.
- Saved-model loading.
- Legacy ensemble inference.
- Real-data Random Forest inference.
- Operational-threshold selection.
- Shadow-mode scoring.
- Side-by-side model comparison.
- Optional alert persistence.
- Alert lookup.
- Model metric reporting.
- OpenAPI documentation.

### `dashboard`

The verified dashboard is a static HTML/CSS/JavaScript interface served by Nginx.

It is intended to display:

- Recent network flows.
- Detected anomalies.
- Persisted alerts.
- Model and system metrics.
- Basic operational health.

### `docker-compose.yml`

The local stack contains:

- PostgreSQL 16
- Redis 7
- C++ capture service
- FastAPI ML service
- Nginx dashboard

PostgreSQL and Redis are kept inside the Compose network and are not intentionally exposed through host ports.

---

## Network Features

The real-data model pipeline uses 11 flow-level features:

| Feature | Meaning |
|---|---|
| `duration_seconds` | Time between first and last packet |
| `packet_count` | Number of packets in the flow |
| `total_bytes` | Total transferred bytes |
| `bytes_per_sec` | Byte-transfer rate |
| `packets_per_sec` | Packet rate |
| `syn_count` | TCP SYN flags observed |
| `ack_count` | TCP ACK flags observed |
| `fin_count` | TCP FIN flags observed |
| `rst_count` | TCP RST flags observed |
| `syn_ack_ratio` | SYN count relative to ACK activity |
| `rst_ratio` | RST count relative to packet count |

Derived features:

```text
bytes_per_sec   = total_bytes / duration_seconds
packets_per_sec = packet_count / duration_seconds
syn_ack_ratio   = syn_count / (ack_count + 1)
rst_ratio       = rst_count / (packet_count + 1)
```

Zero-duration flows are handled safely to avoid division by zero.

---

## Machine-Learning Models

### Random Forest

A supervised binary attack classifier trained on labelled benign and malicious traffic.

Strengths:

- Best overall real-data F1 score.
- Very high attack recall.
- Direct attack-probability output.
- Feature-importance support.
- Fast CPU inference.

### Isolation Forest

An unsupervised anomaly detector trained on benign traffic.

Strengths:

- Does not require attack labels during fitting.
- Detects outliers that differ from normal behaviour.
- Provides an independent anomaly signal.

Observed limitation:

- Very high recall but excessive false positives on the final real-data test split.

### PyTorch Autoencoder

A neural anomaly detector trained to reconstruct benign feature vectors.

Detection principle:

```text
low reconstruction error  → resembles learned benign behaviour
high reconstruction error → possible anomaly
```

The reconstruction threshold is selected from validation behaviour.

### GraphSAGE

A graph neural network implemented with PyTorch Geometric.

For the real CICIDS2017 experiment:

- Each flow is represented as a node.
- Similar flows are connected through feature-space proximity.
- GraphSAGE aggregates neighbourhood information.
- The correct description is a **flow-similarity graph model**.

The CICIDS2017 CSV files used in this experiment did not provide source and destination IP columns, so this model must not be described as a host-communication graph.

### Legacy three-model ensemble

The original project path combines:

- Isolation Forest
- Random Forest
- Autoencoder

An anomaly is raised when at least two of the three models agree.

This path belongs to the earlier prototype/held-out evaluation.

### Real-data four-model ensemble

The research evaluation combines:

- Random Forest
- Isolation Forest
- Autoencoder
- GraphSAGE

The evaluated strict agreement rule reduced false positives but caused a substantial recall drop.

---

## Dataset and Evaluation Methodology

### CICIDS2017 data

Total labelled records available locally:

| Category | Count |
|---|---:|
| Total | 2,830,743 |
| Benign | 2,273,097 |
| Attack | 557,646 |

Attack families represented in the source collection include:

- DDoS
- PortScan
- Bot
- FTP-Patator
- SSH-Patator
- DoS Hulk
- DoS GoldenEye
- DoS Slowhttptest
- DoS slowloris
- Heartbleed
- Web Attack — Brute Force
- Web Attack — XSS
- Web Attack — SQL Injection
- Infiltration

### Capture-day-separated splits

Instead of randomly mixing rows from the same capture files, FlowGuard separates the data by collection day:

| Split | Capture days | Benign | Attack | Total |
|---|---|---:|---:|---:|
| Training | Monday–Wednesday | 10,000 | 10,000 | 20,000 |
| Validation | Thursday | 2,000 | 2,000 | 4,000 |
| Final test | Friday | 5,000 | 5,000 | 10,000 |

The validation set is used for threshold selection. The Friday test split remains untouched until final evaluation.

### Why day separation matters

Random row splitting can produce overly optimistic results when nearly identical flows from the same capture occur in both training and test data.

Day-separated evaluation provides a more difficult test of:

- Cross-day generalization.
- Traffic-distribution changes.
- Previously unseen or sparsely represented attack families.
- Threshold robustness.
- Resistance to train-test leakage.

---

## Real-Data Model Results

### Binary classification metrics

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Isolation Forest | 62.51% | 57.21% | 99.26% | 72.59% |
| Random Forest | **86.09%** | 78.71% | **98.94%** | **87.67%** |
| Autoencoder | 75.86% | 73.11% | 81.80% | 77.21% |
| GraphSAGE | 55.39% | 52.85% | 99.88% | 69.13% |
| Strict four-model ensemble | 84.71% | **86.96%** | 81.66% | 84.23% |

Random Forest ROC-AUC:

```text
0.9036
```

### Confusion matrices

Format:

```text
[[true negatives, false positives],
 [false negatives, true positives]]
```

Random Forest:

```text
[[3662, 1338],
 [  53, 4947]]
```

Strict four-model ensemble:

```text
[[4388,  612],
 [ 917, 4083]]
```

### Operational trade-off

Compared with Random Forest, the ensemble:

- Reduced false positives from 1,338 to 612.
- Reduced false positives by 54.3%.
- Increased precision from 78.71% to 86.96%.
- Increased false negatives from 53 to 917.
- Reduced attack recall from 98.94% to 81.66%.

The ensemble is useful when false alarms are especially expensive, but Random Forest is the stronger general detector.

### Per-family ensemble recall

| Attack family | Recall | Test flows |
|---|---:|---:|
| DDoS | 84.99% | 2,152 |
| PortScan | 80.35% | 2,804 |
| Bot | 2.27% | 44 |

Bot recall was poor because the final sampling included few Bot flows and the training-day attack data did not provide equivalent Bot coverage.

---

## eBPF/XDP Performance Benchmark

### Workload

- PCAP: infected-Android traffic capture.
- PCAP size: approximately 24 MB.
- Packets per PCAP loop: 29,125.
- XDP replay loops per measured run: 50.
- Expected packets per measured run: 1,456,250.
- Measured runs: 7.
- XDP attachment mode: native.
- C++ build: Release mode with `-O3`.
- XDP benchmark: silent parser using a per-CPU map.
- Runtime measurement: kernel BPF program statistics through `bpftool`.

### Median C++ result

```text
C++ median CPU cost:          108.456 ns/packet
C++ median wall cost:         110.278 ns/packet
C++ equivalent throughput:    9,067,963 packets/s
```

### Median native-XDP result

```text
XDP median kernel cost:       62.301 ns/packet
XDP equivalent throughput:    16,051,175 packets/s
XDP sustained replay rate:    316,330 packets/s
XDP observed packet loss:     approximately 0%
```

### Improvement

```text
Processing-cost speedup:      1.74×
Equivalent-throughput gain:   1.77×
Processing-cost reduction:    42.6%
Equivalent-throughput rise:   approximately 77%
```

### Interpretation

The 16.05 million packets/s result is equivalent throughput calculated from measured kernel execution time.

The 316,330 packets/s result measures the complete replay path:

```text
PCAP
  → tcpreplay
  → virtual Ethernet pair
  → Linux ingress path
  → native XDP program
```

The complete replay rate includes replay generation, veth, scheduling, and other kernel overhead. It should not be described as the XDP parser's maximum theoretical capacity.

A measured delivery rate slightly above 100% was caused by a few additional control/interface packets. It is reported as approximately 100% delivery and approximately 0% loss.

---

## Live Shadow-Mode Evaluation

The selected real-data Random Forest is integrated into FastAPI without replacing the legacy alert pipeline.

### Real-model health example

```json
{
  "status": "ok",
  "model": "real_only_random_forest",
  "threshold": 0.0235,
  "operational_mode": "balanced",
  "flow_file": "data/flows_output.jsonl",
  "mode": "shadow"
}
```

### Operational mode

Select the threshold configuration through:

```bash
RF_OPERATIONAL_MODE=balanced
```

The balanced threshold was selected on the Thursday validation split.

### Model-comparison endpoint

The comparison route runs the legacy ensemble and real-data Random Forest on the same recent flows without writing alerts.

Verified comparison over 100 flows:

| Metric | Result |
|---|---:|
| Analyzed | 100 |
| Errors | 0 |
| Legacy alerts | 85 |
| Real Random Forest alerts | 100 |
| Both alert | 85 |
| Both benign | 0 |
| Legacy only | 0 |
| Real Random Forest only | 15 |
| Agreement | 85% |

The 15 disagreements shared a repeated inbound TCP/source-port-8080 pattern.

These live flows did not contain ground-truth labels. Therefore, the results show model disagreement and alert volume—not verified attacks or live accuracy.

---

## Historical Prototype Result

The earlier synthetic/held-out prototype used 940 rows:

- 830 benign
- 110 attacks

The legacy 2-of-3 ensemble achieved:

| Metric | Result |
|---|---:|
| Accuracy | 98.94% |
| Precision | 96.30% |
| Recall | 94.55% |
| F1 | 95.41% |
| False positives | 4 |
| False negatives | 6 |

This result is retained for project history and regression comparison. It is not the main real-data headline.

---

## Project Layout

Representative layout:

```text
flowguard/
├── capture-cpp/
│   ├── include/
│   │   ├── BlockingQueue.hpp
│   │   ├── FeatureEmitter.hpp
│   │   ├── FlowAggregator.hpp
│   │   ├── FlowKey.hpp
│   │   ├── FlowStats.hpp
│   │   ├── JsonSerializer.hpp
│   │   ├── PacketInfo.hpp
│   │   └── PacketParser.hpp
│   ├── src/
│   │   ├── main.cpp
│   │   ├── PacketParser.cpp
│   │   ├── FlowAggregator.cpp
│   │   ├── FeatureEmitter.cpp
│   │   ├── JsonSerializer.cpp
│   │   ├── benchmark.cpp
│   │   └── parser_benchmark.cpp
│   ├── tests/
│   ├── CMakeLists.txt
│   └── Dockerfile
├── capture-ebpf/
│   ├── xdp_filter.bpf.c
│   ├── xdp_filter.o
│   ├── loader.c
│   ├── loader
│   ├── xdp_parser_benchmark.c
│   └── xdp_parser_benchmark.o
├── ml-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── ml/
│   │   │   ├── ensemble.py
│   │   │   └── real_only_predictor.py
│   │   ├── routes/
│   │   │   └── real_analysis.py
│   │   ├── services/
│   │   └── models/
│   │       └── real_only/
│   ├── data/
│   │   └── real_only/
│   ├── training/
│   │   ├── train_evaluate_real_only.py
│   │   └── tune_real_rf_thresholds.py
│   ├── tests/
│   ├── prisma/
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/
│   ├── index.html
│   └── Dockerfile
├── data/
│   ├── sample/
│   ├── attack_samples/
│   ├── cicids2017/
│   └── flows_output.jsonl
├── docs/
│   ├── cpp_parser_benchmark.txt
│   ├── ebpf_vs_cpp_runs.csv
│   ├── ebpf_vs_cpp_benchmark.json
│   ├── ebpf_vs_cpp_benchmark.md
│   └── model_comparison.json
├── scripts/
│   └── benchmark_ebpf_vs_cpp.sh
├── docker-compose.yml
├── HOW_TO_RUN.md
└── README.md
```

Some generated datasets, model artifacts, PCAPs, and build outputs may be intentionally excluded from Git.

---

## Requirements

### General

- Linux
- Git
- Docker and Docker Compose
- Python 3
- CMake
- A C++17 compiler

### C++ capture

- libpcap
- pthread support

### eBPF/XDP

- Linux kernel with eBPF and XDP support
- Clang/LLVM
- libbpf and development headers
- bpftool
- Linux networking tools (`ip`)
- Root privileges for loading and attaching XDP programs

### Benchmarking

- tcpreplay
- tcpdump
- Python 3
- `kernel.bpf_stats_enabled` support

---

## Quick Start with Docker Compose

From the repository root:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

Expected services:

```text
postgres
redis
capture
ml-service
dashboard
```

Check the API:

```bash
curl http://127.0.0.1:8000/health
curl "http://127.0.0.1:8000/flows/recent?limit=2"
```

Open:

- Dashboard: `http://127.0.0.1:8080`
- OpenAPI documentation: `http://127.0.0.1:8000/docs`

View logs:

```bash
docker compose logs -f ml-service
```

Stop the stack:

```bash
docker compose down
```

Remove the PostgreSQL volume as well:

```bash
docker compose down -v
```

---

## Manual C++ Capture Run

### Configure and compile

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Release

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

### Process a PCAP

```bash
./capture-cpp/build/flowguard_capture \
  data/sample/small_sample.pcap \
  data/flows_output.jsonl
```

### Inspect output

```bash
head -n 5 data/flows_output.jsonl
```

Each line represents one aggregated flow.

---

## Manual FastAPI Run

From the repository root:

```bash
cd ml-service
source .venv/bin/activate
```

Run the selected real-data operating mode:

```bash
RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
python -m uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
```

Using `python -m uvicorn` avoids relying on a globally installed `uvicorn` command.

Check the service:

```bash
curl -s http://127.0.0.1:8000/health | python -m json.tool
```

Check the real model:

```bash
curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
```

Run shadow inference:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=20" \
  | python -m json.tool
```

Compare detectors:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  | python -m json.tool
```

---

## eBPF/XDP Build and Run

### Compile the XDP program

From the repository root:

```bash
clang \
  -O2 \
  -g \
  -target bpf \
  -D__TARGET_ARCH_x86 \
  -c capture-ebpf/xdp_filter.bpf.c \
  -o capture-ebpf/xdp_filter.o
```

Verify the object:

```bash
file capture-ebpf/xdp_filter.o
```

Expected type:

```text
ELF 64-bit LSB relocatable, eBPF
```

### Compile the userspace loader

```bash
cc \
  -O2 \
  -g \
  capture-ebpf/loader.c \
  -o capture-ebpf/loader \
  $(pkg-config --cflags --libs libbpf)
```

### Attach to an interface

First identify the interface:

```bash
ip -br link
```

Then run the loader from the directory containing `xdp_filter.o`:

```bash
cd capture-ebpf
sudo ./loader wlan0
```

Replace `wlan0` with the correct interface.

Press `Ctrl+C` to stop the loader and detach the XDP program.

### Warning

The demonstration packet threshold in `xdp_filter.bpf.c` counts packets over the lifetime of the BPF map entry. It is not a time-windowed packets-per-second production rate limiter.

---

## Model Training and Evaluation

### Expected real-data locations

```text
data/cicids2017/
ml-service/data/real_only/
```

### Real-only training/evaluation

From `ml-service`:

```bash
PYTHONPATH=. \
.venv/bin/python \
training/train_evaluate_real_only.py
```

### Operational-threshold tuning

```bash
PYTHONPATH=. \
.venv/bin/python \
training/tune_real_rf_thresholds.py
```

Generated real-model artifacts are stored under:

```text
ml-service/app/models/real_only/
```

Expected artifacts include:

```text
random_forest.joblib
supervised_scaler.joblib
isolation_forest.joblib
anomaly_scaler.joblib
autoencoder.pt
graphsage_flow_similarity.pt
thresholds.json
rf_operational_thresholds.json
```

### Important reproducibility note

Do not select thresholds using the final Friday test set. The project uses Thursday validation data for threshold selection and Friday data only for final evaluation.

---

## Benchmark Reproduction

### C++ parser benchmark

```bash
./capture-cpp/build-benchmark/flowguard_parser_benchmark \
  data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap \
  7 \
  | tee docs/cpp_parser_benchmark.txt
```

### Full XDP versus C++ benchmark

```bash
chmod +x scripts/benchmark_ebpf_vs_cpp.sh
./scripts/benchmark_ebpf_vs_cpp.sh
```

The script:

- Enables BPF runtime statistics temporarily.
- Creates a temporary veth pair.
- Loads and pins the benchmark XDP program.
- Attaches it in native mode when supported.
- Replays the PCAP multiple times.
- Reads BPF runtime and packet counters.
- Calculates median metrics.
- Writes CSV, JSON, and Markdown reports.
- Detaches XDP and removes the temporary interfaces.

Generated output:

```text
docs/ebpf_vs_cpp_runs.csv
docs/ebpf_vs_cpp_benchmark.json
docs/ebpf_vs_cpp_benchmark.md
```

The benchmark requires `sudo`.

---

## API Reference

### Health

```http
GET /health
```

Basic API health check.

### Recent flows

```http
GET /flows/recent?limit=20
```

Returns the most recent captured flow records.

### Legacy batch analysis

```http
POST /analyze?offset=0&limit=100&persist=false
```

Parameters:

| Parameter | Meaning |
|---|---|
| `offset` | Starting flow index |
| `limit` | Batch size, up to 1,000 |
| `persist` | Save detected anomalies to PostgreSQL |

Use `persist=false` while validating behaviour.

### Alerts

```http
GET /alerts
GET /alerts/{alert_id}
```

Retrieves persisted alerts.

### Historical model metrics

```http
GET /metrics/model
```

Returns the historical held-out prototype metrics. This endpoint does not represent the final real-only Random Forest evaluation.

### Real-data model health

```http
GET /real-model/health
```

Returns:

- Model identifier
- Selected operational threshold
- Operational mode
- Resolved flow file
- Shadow-mode state

### Real-data shadow analysis

```http
POST /real-model/analyze?limit=50
```

Scores recent flows with the real-only Random Forest.

It does not persist alerts.

### Detector comparison

```http
POST /analyze/compare?limit=100
```

Runs the legacy ensemble and real Random Forest on the same recent flows.

Returns:

- Alert totals
- Agreement categories
- Agreement rate
- Real Random Forest probabilities
- Per-flow disagreement information
- Error details

The comparison route never persists alerts.

### Legacy real-capture route

```http
POST /analyse/real
```

This older experimental route is retained for compatibility. Prefer the `/real-model/*` routes for current shadow evaluation.

---

## Testing

### Python tests

```bash
cd ml-service

PYTHONPATH=. \
.venv/bin/python \
-m pytest tests -q
```

Previously verified result:

```text
8 passed
```

Re-run the suite after modifying inference routes or model-loading code.

### C++ tests

Configure and build:

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Debug

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

Run registered tests:

```bash
ctest \
  --test-dir capture-cpp/build \
  --output-on-failure
```

C++ test targets cover areas such as:

- Flow key ordering
- Flow aggregation
- Blocking queue behaviour
- Packet parsing
- JSON serialization

### Syntax checks

Python:

```bash
python -m py_compile \
  ml-service/app/main.py \
  ml-service/app/ml/real_only_predictor.py \
  ml-service/app/routes/real_analysis.py
```

Bash:

```bash
bash -n scripts/benchmark_ebpf_vs_cpp.sh
```

---

## Generated Artifacts

### Model artifacts

```text
ml-service/app/models/real_only/
├── anomaly_scaler.joblib
├── autoencoder.pt
├── graphsage_flow_similarity.pt
├── isolation_forest.joblib
├── random_forest.joblib
├── rf_operational_thresholds.json
├── supervised_scaler.joblib
└── thresholds.json
```

### Evaluation artifacts

```text
docs/
├── cpp_parser_benchmark.txt
├── ebpf_vs_cpp_runs.csv
├── ebpf_vs_cpp_benchmark.json
├── ebpf_vs_cpp_benchmark.md
├── model_comparison.json
└── rf_threshold_tuning.txt
```

### Prepared real-data splits

```text
ml-service/data/real_only/
├── train_real.csv
├── validation_real.csv
└── test_real.csv
```

Large datasets, model files, PCAPs, and generated build files may need Git LFS or external storage rather than ordinary Git commits.

---

## Docker and Infrastructure Notes

### PostgreSQL

PostgreSQL provides durable alert storage.

The Compose configuration uses:

```text
database: flowguard
user: flowguard_user
```

Credentials in the development Compose file are for local use only and must be replaced for deployment.

### Prisma ORM

Prisma provides schema-driven database access.

The ML container startup performs:

1. Wait for PostgreSQL.
2. Wait for Redis.
3. Run `prisma db push`.
4. Run `prisma generate`.
5. Start Uvicorn.

### Redis

Redis is used inside the Compose network for messaging/pub-sub support.

It is not intentionally exposed to the host.

### Capture permissions

The capture container receives:

```text
NET_ADMIN
NET_RAW
```

These capabilities are required for packet-capture and networking operations but should be minimized in production.

### ML image

The ML image installs CPU-only PyTorch packages to avoid pulling unnecessary GPU/CUDA layers for the local CPU inference workflow.

### Dashboard image

The verified dashboard container serves the static dashboard through Nginx.

---

## Design Decisions

### JSONL between C++ and Python

JSON Lines was selected because it is:

- Human-readable.
- Append-friendly.
- Easy to debug with standard shell tools.
- Supported directly by Python.
- Independent of the C++ process lifetime.
- Suitable for replay and offline evaluation.

### Bounded queue instead of an unbounded queue

A bounded queue prevents the capture thread from consuming unlimited memory if the aggregation thread cannot keep pace.

### Model loading at startup

Saved models are loaded once when the API process starts rather than once per request. This reduces inference latency and avoids repeated disk deserialization.

### Shadow deployment

The real-data model does not immediately replace or persist into the existing alert path.

Shadow deployment allows FlowGuard to measure:

- Alert volume.
- Model disagreement.
- Probability distribution.
- Feature-semantic mismatch.
- Domain shift.
- Runtime errors.

### Day-separated evaluation

Capture-day separation was selected to reduce leakage and make the model prove that it can generalize beyond the exact capture distribution used for fitting.

### Median benchmark reporting

Performance results use medians across repeated runs to reduce sensitivity to scheduler noise and occasional outliers.

---

## Limitations and Honest Interpretation

FlowGuard is an engineering and research project, not a production-certified intrusion-detection appliance.

### Live predictions are not ground truth

A live model label of `ATTACK` is a prediction, not confirmation of malicious activity.

Accuracy, precision, and recall require labelled data.

### High live alert rate indicates possible domain shift

The real-only Random Forest produced a high alert rate on the infected-host capture. This can reflect:

- Truly unusual traffic.
- Different feature semantics.
- Dataset-to-live distribution shift.
- Poor probability calibration.
- Incomplete flow reconstruction.

It must not be described as a verified attack rate.

### Balanced final test set

The final test set intentionally contains equal benign and attack counts.

This makes model comparison clear but does not represent the natural attack prevalence of most real networks.

### GraphSAGE limitations

The GraphSAGE model had extremely high recall but very poor benign classification.

It demonstrates graph-learning implementation but requires:

- Better graph construction.
- Calibration.
- Class weighting.
- Additional validation.
- More representative graph data.

### Infected-Android PCAP labels

The infected-Android PCAP does not provide per-flow ground-truth labels.

It is valid for:

- Systems benchmarking.
- Replay.
- End-to-end testing.
- Shadow inference.
- Disagreement analysis.

It is not valid for reporting classification accuracy.

### eBPF benchmark scope

The benchmark compares implemented parser-level cost.

It does not include:

- Flow aggregation parity.
- Machine-learning inference.
- PostgreSQL persistence.
- Redis publication.
- Dashboard latency.
- Complete packet-to-alert latency.

### Demonstration drop threshold

The original XDP source counter is lifetime-based. Production rate limiting requires a time-windowed policy.

---

## Roadmap

### Detection quality

- Probability calibration using isotonic regression or Platt scaling.
- Evaluation on naturally imbalanced traffic.
- Precision-recall curves and confidence intervals.
- Leave-one-attack-family-out testing.
- Better Bot-family coverage.
- Weighted voting or stacking instead of strict agreement.
- Incident-level alert grouping.
- Feature-semantic alignment between C++ flows and CICIDS flow generation.

### Graph learning

- True IP host-communication graphs.
- Temporal graph construction.
- Class-weighted GraphSAGE loss.
- Focal loss.
- Graph mini-batching.
- Validation-based early stopping.
- Neighbourhood and edge-feature ablation studies.

### eBPF/XDP

- Time-windowed packet-rate limiting.
- Production per-CPU counters.
- Ring-buffer loss counters.
- IPv6 parsing.
- VLAN support.
- AF_XDP experiment.
- Multi-core scaling benchmark.
- Physical-NIC benchmark.
- Packet-to-alert latency measurement.

### Backend and operations

- Prometheus metrics.
- Grafana dashboards.
- Authentication and role-based access.
- Model registry and rollback.
- Alert deduplication.
- Deployment-specific secrets.
- CI for Python, C++, Docker, and eBPF verifier checks.
- Structured logging and tracing.

---

## Resume-Ready Summary

### Detailed version

> Built FlowGuard, a full-stack network intrusion detection platform using C++17/libpcap, native XDP/eBPF, FastAPI, PostgreSQL, Redis, Prisma ORM, and Docker Compose. Trained Random Forest, Isolation Forest, a PyTorch Autoencoder, and GraphSAGE on capture-day-separated CICIDS2017 data; Random Forest achieved 86.09% accuracy, 98.94% recall, 78.71% precision, and 0.8767 F1 on 10,000 real labelled flows. Benchmarked native XDP across seven runs and approximately 1.46 million packets per run, achieving 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than the C++ userspace parser.

### Compact bullets

- Built a C++17/Python network intrusion detection pipeline using libpcap, native XDP/eBPF, five-tuple flow aggregation, FastAPI, PostgreSQL, Redis, and Docker Compose.
- Achieved **86.09% accuracy, 98.94% recall, and 0.8767 F1** with Random Forest on **10,000 real capture-day-separated CICIDS2017 flows**.
- Reduced Random Forest false positives by **54.3%** with a strict four-model ensemble, improving precision to **86.96%** while documenting the recall trade-off.
- Benchmarked native XDP at **62.3 ns/packet and 16.05M equivalent packets/s**, delivering **1.77× higher equivalent throughput** than the C++ parser.

---

## Technology Keywords

### Languages and systems

```text
C++17, C, Python, SQL, Bash, JavaScript, Linux, systems programming,
multithreading, producer-consumer, bounded queue, backpressure, mutex,
condition variable, atomic state, kernel programming
```

### Networking

```text
libpcap, PCAP, tcpreplay, Ethernet, IPv4, TCP, UDP, ICMP, five-tuple,
flow aggregation, TCP flags, packet parsing, network telemetry,
network intrusion detection, NIDS, DDoS, PortScan, Bot detection
```

### eBPF/XDP

```text
eBPF, XDP, native XDP, libbpf, bpftool, BPF maps, per-CPU maps,
ring buffer, kernel-space packet processing, packet filtering,
nanoseconds per packet, packets per second
```

### Machine learning

```text
scikit-learn, PyTorch, PyTorch Geometric, Random Forest,
Isolation Forest, Autoencoder, GraphSAGE, GNN, anomaly detection,
supervised learning, unsupervised learning, feature engineering,
threshold tuning, ensemble learning, ROC-AUC, precision, recall,
F1 score, confusion matrix, domain shift, data leakage,
capture-day separation, model generalization, shadow deployment
```

### Backend and DevOps

```text
FastAPI, REST API, Uvicorn, PostgreSQL, Prisma ORM, Redis, pub/sub,
Docker, Docker Compose, Nginx, CMake, Clang, health checks,
model serving, persistent storage, internal service networking
```

---

## Security and Research Notice

FlowGuard is intended for authorized defensive-security research, learning, benchmarking, and controlled network monitoring.

Only capture, replay, or inspect traffic on systems and networks where you have permission.

Model outputs should be reviewed by a human analyst before being treated as confirmed security incidents.

---

## Current Verified Headline

> **FlowGuard achieved 86.09% accuracy, 98.94% recall, and 0.8767 F1 on 10,000 real capture-day-separated CICIDS2017 flows, while its native XDP parser delivered 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than its C++ userspace parser.**

Library
/
PROJECT 1
/FlowGuard_Detailed_README.md

# FlowGuard

> A full-stack network intrusion detection and traffic-analysis platform built with C++17, native XDP/eBPF, FastAPI, scikit-learn, PyTorch, PyTorch Geometric, PostgreSQL, Redis, Prisma ORM, Docker Compose, and Nginx.

FlowGuard converts raw network packets into flow-level security telemetry, evaluates each flow using multiple machine-learning approaches, and exposes the resulting detections through a REST API and monitoring dashboard.

The project combines three engineering areas:

- **Systems and networking:** C++ packet parsing, multithreading, flow aggregation, libpcap, Linux networking, native XDP/eBPF, BPF maps, and ring buffers.
- **Machine learning:** Random Forest, Isolation Forest, Autoencoder, GraphSAGE, feature engineering, threshold tuning, capture-day-separated evaluation, and ensemble analysis.
- **Backend and infrastructure:** FastAPI, PostgreSQL, Prisma ORM, Redis pub/sub, Docker Compose, Nginx, health checks, persistence, and shadow deployment.

---

## Table of Contents

- [Highlights](#highlights)
- [Verified Results](#verified-results)
- [What FlowGuard Does](#what-flowguard-does)
- [Architecture](#architecture)
- [Project Components](#project-components)
- [Network Features](#network-features)
- [Machine-Learning Models](#machine-learning-models)
- [Dataset and Evaluation Methodology](#dataset-and-evaluation-methodology)
- [Real-Data Model Results](#real-data-model-results)
- [eBPF/XDP Performance Benchmark](#ebpfxdp-performance-benchmark)
- [Live Shadow-Mode Evaluation](#live-shadow-mode-evaluation)
- [Project Layout](#project-layout)
- [Requirements](#requirements)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Manual C++ Capture Run](#manual-c-capture-run)
- [Manual FastAPI Run](#manual-fastapi-run)
- [eBPF/XDP Build and Run](#ebpfxdp-build-and-run)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Benchmark Reproduction](#benchmark-reproduction)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Generated Artifacts](#generated-artifacts)
- [Docker and Infrastructure Notes](#docker-and-infrastructure-notes)
- [Design Decisions](#design-decisions)
- [Limitations and Honest Interpretation](#limitations-and-honest-interpretation)
- [Roadmap](#roadmap)
- [Resume-Ready Summary](#resume-ready-summary)
- [Technology Keywords](#technology-keywords)

---

## Highlights

- Multithreaded **C++17/libpcap** packet-to-flow processing pipeline.
- Ethernet, IPv4, TCP, UDP, and ICMP parsing.
- Bounded producer-consumer queue with backpressure.
- Five-tuple flow aggregation and TCP flag statistics.
- Native **XDP/eBPF** packet parsing and early filtering.
- Kernel-to-userspace communication through a BPF ring buffer.
- FastAPI inference service with batch analysis and alert persistence.
- PostgreSQL-backed alert storage through Prisma ORM.
- Redis-based internal messaging/pub-sub support.
- Random Forest, Isolation Forest, PyTorch Autoencoder, and GraphSAGE.
- Real CICIDS2017 training and capture-day-separated final evaluation.
- Validation-selected Random Forest operating thresholds.
- Shadow deployment and legacy-versus-real model comparison.
- Reproducible C++ versus XDP performance benchmark.
- Docker Compose orchestration for the complete local stack.

---

## Verified Results

### Real-data intrusion-detection result

The strongest individual model was Random Forest:

| Metric | Result |
|---|---:|
| Test flows | 10,000 |
| Benign flows | 5,000 |
| Attack flows | 5,000 |
| Accuracy | **86.09%** |
| Precision | **78.71%** |
| Recall | **98.94%** |
| F1 score | **0.8767** |
| ROC-AUC | **0.9036** |
| False positives | 1,338 |
| False negatives | 53 |

The test data was separated by capture day from the training and validation data.

### Native XDP/eBPF performance result

| Metric | C++ userspace parser | Native XDP/eBPF parser |
|---|---:|---:|
| Processing cost | 108.456 ns/packet | **62.301 ns/packet** |
| Equivalent throughput | 9.07 million packets/s | **16.05 million packets/s** |
| Processing-cost reduction | — | **42.6%** |
| Equivalent-throughput improvement | — | **1.77×** |
| Sustained complete replay path | — | 316,330 packets/s |
| Observed packet loss | — | approximately 0% |

The XDP benchmark used seven measured runs and approximately 1.46 million replayed packets per run.

### Four-model ensemble result

The strict four-model ensemble prioritized agreement and reduced false alarms:

| Metric | Result |
|---|---:|
| Accuracy | 84.71% |
| Precision | **86.96%** |
| Recall | 81.66% |
| F1 score | 0.8423 |
| False positives | 612 |
| False negatives | 917 |
| False-positive reduction vs Random Forest | **54.3%** |

The ensemble improved precision and reduced false positives, but it also missed more attacks. Random Forest therefore remains the strongest general headline model.

---

## What FlowGuard Does

FlowGuard implements the following pipeline:

1. Read packets from a PCAP file or inspect live ingress traffic.
2. Validate Ethernet and IPv4 headers.
3. Parse TCP, UDP, ICMP, ports, lengths, timestamps, and TCP flags.
4. Convert packets into a structured `PacketInfo` representation.
5. Group packets into flows using a network five-tuple.
6. Calculate duration, traffic volume, rate, and TCP-behaviour features.
7. Emit completed flows as JSON Lines.
8. Load the flows into a FastAPI inference service.
9. Score each flow with one or more detection models.
10. Compare model decisions in shadow mode.
11. Optionally persist alerts in PostgreSQL.
12. Expose flows, alerts, metrics, and health state through REST endpoints.
13. Display operational data through an Nginx-served dashboard.

---

## Architecture

```text
                         ┌──────────────────────────────┐
                         │ PCAP replay or live traffic  │
                         └──────────────┬───────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ C++17/libpcap capture  │              │ Native XDP/eBPF path   │
        │ Userspace packet path  │              │ Kernel ingress path    │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ PacketParser           │              │ BPF maps / ring buffer │
        │ Ethernet/IP/TCP/UDP    │              │ pass/drop/event output │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     └───────────────────┬───────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Five-tuple aggregation │
                            │ Packet/byte/TCP stats  │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ JSONL feature pipeline │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ FastAPI ML service     │
                            │ Normalization/scoring  │
                            └────────────┬───────────┘
                                         ▼
          ┌──────────────────────────────────────────────────────────┐
          │ Random Forest │ Isolation Forest │ Autoencoder │ GraphSAGE │
          └──────────────────────────────┬───────────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Shadow comparison /    │
                            │ voting / alert logic   │
                            └────────────┬───────────┘
                                         ▼
                  ┌──────────────────────┴──────────────────────┐
                  ▼                                             ▼
        ┌────────────────────────┐                  ┌────────────────────────┐
        │ PostgreSQL + Prisma    │                  │ Redis pub/sub          │
        │ Durable alert storage  │                  │ Internal notifications │
        └────────────┬───────────┘                  └────────────┬───────────┘
                     └───────────────────┬───────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Nginx dashboard        │
                            │ Flows/alerts/metrics   │
                            └────────────────────────┘
```

---

## Project Components

### `capture-cpp`

The C++17 layer is responsible for packet parsing and flow aggregation.

Key responsibilities:

- Open PCAP files through libpcap.
- Parse Ethernet and IPv4 packet structure.
- Extract transport protocol and ports.
- Record packet size and nanosecond timestamp representation.
- Extract TCP SYN, ACK, FIN, and RST flags.
- Send parsed packets through a bounded blocking queue.
- Aggregate packets into flows.
- Write completed flow records to JSONL.

Concurrency model:

```text
Capture thread
    │
    ▼
BlockingQueue<PacketInfo>
    │
    ▼
Aggregation thread
```

The bounded queue provides backpressure when aggregation is slower than capture and prevents unrestricted memory growth.

### `capture-ebpf`

The eBPF layer performs packet inspection at the Linux XDP hook.

Implemented concepts:

- Native XDP attachment.
- Safe packet-bound checks required by the eBPF verifier.
- Ethernet and IPv4 parsing.
- Variable-length IPv4 header handling.
- TCP and UDP port extraction.
- Per-source tracking through BPF maps.
- Demonstration early-drop action.
- BPF ring-buffer event transfer.
- libbpf userspace loader.
- Signal-based cleanup and XDP detach.
- Dedicated silent benchmark program.

### `ml-service`

The Python service provides:

- Flow normalization.
- Feature generation.
- Saved-model loading.
- Legacy ensemble inference.
- Real-data Random Forest inference.
- Operational-threshold selection.
- Shadow-mode scoring.
- Side-by-side model comparison.
- Optional alert persistence.
- Alert lookup.
- Model metric reporting.
- OpenAPI documentation.

### `dashboard`

The verified dashboard is a static HTML/CSS/JavaScript interface served by Nginx.

It is intended to display:

- Recent network flows.
- Detected anomalies.
- Persisted alerts.
- Model and system metrics.
- Basic operational health.

### `docker-compose.yml`

The local stack contains:

- PostgreSQL 16
- Redis 7
- C++ capture service
- FastAPI ML service
- Nginx dashboard

PostgreSQL and Redis are kept inside the Compose network and are not intentionally exposed through host ports.

---

## Network Features

The real-data model pipeline uses 11 flow-level features:

| Feature | Meaning |
|---|---|
| `duration_seconds` | Time between first and last packet |
| `packet_count` | Number of packets in the flow |
| `total_bytes` | Total transferred bytes |
| `bytes_per_sec` | Byte-transfer rate |
| `packets_per_sec` | Packet rate |
| `syn_count` | TCP SYN flags observed |
| `ack_count` | TCP ACK flags observed |
| `fin_count` | TCP FIN flags observed |
| `rst_count` | TCP RST flags observed |
| `syn_ack_ratio` | SYN count relative to ACK activity |
| `rst_ratio` | RST count relative to packet count |

Derived features:

```text
bytes_per_sec   = total_bytes / duration_seconds
packets_per_sec = packet_count / duration_seconds
syn_ack_ratio   = syn_count / (ack_count + 1)
rst_ratio       = rst_count / (packet_count + 1)
```

Zero-duration flows are handled safely to avoid division by zero.

---

## Machine-Learning Models

### Random Forest

A supervised binary attack classifier trained on labelled benign and malicious traffic.

Strengths:

- Best overall real-data F1 score.
- Very high attack recall.
- Direct attack-probability output.
- Feature-importance support.
- Fast CPU inference.

### Isolation Forest

An unsupervised anomaly detector trained on benign traffic.

Strengths:

- Does not require attack labels during fitting.
- Detects outliers that differ from normal behaviour.
- Provides an independent anomaly signal.

Observed limitation:

- Very high recall but excessive false positives on the final real-data test split.

### PyTorch Autoencoder

A neural anomaly detector trained to reconstruct benign feature vectors.

Detection principle:

```text
low reconstruction error  → resembles learned benign behaviour
high reconstruction error → possible anomaly
```

The reconstruction threshold is selected from validation behaviour.

### GraphSAGE

A graph neural network implemented with PyTorch Geometric.

For the real CICIDS2017 experiment:

- Each flow is represented as a node.
- Similar flows are connected through feature-space proximity.
- GraphSAGE aggregates neighbourhood information.
- The correct description is a **flow-similarity graph model**.

The CICIDS2017 CSV files used in this experiment did not provide source and destination IP columns, so this model must not be described as a host-communication graph.

### Legacy three-model ensemble

The original project path combines:

- Isolation Forest
- Random Forest
- Autoencoder

An anomaly is raised when at least two of the three models agree.

This path belongs to the earlier prototype/held-out evaluation.

### Real-data four-model ensemble

The research evaluation combines:

- Random Forest
- Isolation Forest
- Autoencoder
- GraphSAGE

The evaluated strict agreement rule reduced false positives but caused a substantial recall drop.

---

## Dataset and Evaluation Methodology

### CICIDS2017 data

Total labelled records available locally:

| Category | Count |
|---|---:|
| Total | 2,830,743 |
| Benign | 2,273,097 |
| Attack | 557,646 |

Attack families represented in the source collection include:

- DDoS
- PortScan
- Bot
- FTP-Patator
- SSH-Patator
- DoS Hulk
- DoS GoldenEye
- DoS Slowhttptest
- DoS slowloris
- Heartbleed
- Web Attack — Brute Force
- Web Attack — XSS
- Web Attack — SQL Injection
- Infiltration

### Capture-day-separated splits

Instead of randomly mixing rows from the same capture files, FlowGuard separates the data by collection day:

| Split | Capture days | Benign | Attack | Total |
|---|---|---:|---:|---:|
| Training | Monday–Wednesday | 10,000 | 10,000 | 20,000 |
| Validation | Thursday | 2,000 | 2,000 | 4,000 |
| Final test | Friday | 5,000 | 5,000 | 10,000 |

The validation set is used for threshold selection. The Friday test split remains untouched until final evaluation.

### Why day separation matters

Random row splitting can produce overly optimistic results when nearly identical flows from the same capture occur in both training and test data.

Day-separated evaluation provides a more difficult test of:

- Cross-day generalization.
- Traffic-distribution changes.
- Previously unseen or sparsely represented attack families.
- Threshold robustness.
- Resistance to train-test leakage.

---

## Real-Data Model Results

### Binary classification metrics

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Isolation Forest | 62.51% | 57.21% | 99.26% | 72.59% |
| Random Forest | **86.09%** | 78.71% | **98.94%** | **87.67%** |
| Autoencoder | 75.86% | 73.11% | 81.80% | 77.21% |
| GraphSAGE | 55.39% | 52.85% | 99.88% | 69.13% |
| Strict four-model ensemble | 84.71% | **86.96%** | 81.66% | 84.23% |

Random Forest ROC-AUC:

```text
0.9036
```

### Confusion matrices

Format:

```text
[[true negatives, false positives],
 [false negatives, true positives]]
```

Random Forest:

```text
[[3662, 1338],
 [  53, 4947]]
```

Strict four-model ensemble:

```text
[[4388,  612],
 [ 917, 4083]]
```

### Operational trade-off

Compared with Random Forest, the ensemble:

- Reduced false positives from 1,338 to 612.
- Reduced false positives by 54.3%.
- Increased precision from 78.71% to 86.96%.
- Increased false negatives from 53 to 917.
- Reduced attack recall from 98.94% to 81.66%.

The ensemble is useful when false alarms are especially expensive, but Random Forest is the stronger general detector.

### Per-family ensemble recall

| Attack family | Recall | Test flows |
|---|---:|---:|
| DDoS | 84.99% | 2,152 |
| PortScan | 80.35% | 2,804 |
| Bot | 2.27% | 44 |

Bot recall was poor because the final sampling included few Bot flows and the training-day attack data did not provide equivalent Bot coverage.

---

## eBPF/XDP Performance Benchmark

### Workload

- PCAP: infected-Android traffic capture.
- PCAP size: approximately 24 MB.
- Packets per PCAP loop: 29,125.
- XDP replay loops per measured run: 50.
- Expected packets per measured run: 1,456,250.
- Measured runs: 7.
- XDP attachment mode: native.
- C++ build: Release mode with `-O3`.
- XDP benchmark: silent parser using a per-CPU map.
- Runtime measurement: kernel BPF program statistics through `bpftool`.

### Median C++ result

```text
C++ median CPU cost:          108.456 ns/packet
C++ median wall cost:         110.278 ns/packet
C++ equivalent throughput:    9,067,963 packets/s
```

### Median native-XDP result

```text
XDP median kernel cost:       62.301 ns/packet
XDP equivalent throughput:    16,051,175 packets/s
XDP sustained replay rate:    316,330 packets/s
XDP observed packet loss:     approximately 0%
```

### Improvement

```text
Processing-cost speedup:      1.74×
Equivalent-throughput gain:   1.77×
Processing-cost reduction:    42.6%
Equivalent-throughput rise:   approximately 77%
```

### Interpretation

The 16.05 million packets/s result is equivalent throughput calculated from measured kernel execution time.

The 316,330 packets/s result measures the complete replay path:

```text
PCAP
  → tcpreplay
  → virtual Ethernet pair
  → Linux ingress path
  → native XDP program
```

The complete replay rate includes replay generation, veth, scheduling, and other kernel overhead. It should not be described as the XDP parser's maximum theoretical capacity.

A measured delivery rate slightly above 100% was caused by a few additional control/interface packets. It is reported as approximately 100% delivery and approximately 0% loss.

---

## Live Shadow-Mode Evaluation

The selected real-data Random Forest is integrated into FastAPI without replacing the legacy alert pipeline.

### Real-model health example

```json
{
  "status": "ok",
  "model": "real_only_random_forest",
  "threshold": 0.0235,
  "operational_mode": "balanced",
  "flow_file": "data/flows_output.jsonl",
  "mode": "shadow"
}
```

### Operational mode

Select the threshold configuration through:

```bash
RF_OPERATIONAL_MODE=balanced
```

The balanced threshold was selected on the Thursday validation split.

### Model-comparison endpoint

The comparison route runs the legacy ensemble and real-data Random Forest on the same recent flows without writing alerts.

Verified comparison over 100 flows:

| Metric | Result |
|---|---:|
| Analyzed | 100 |
| Errors | 0 |
| Legacy alerts | 85 |
| Real Random Forest alerts | 100 |
| Both alert | 85 |
| Both benign | 0 |
| Legacy only | 0 |
| Real Random Forest only | 15 |
| Agreement | 85% |

The 15 disagreements shared a repeated inbound TCP/source-port-8080 pattern.

These live flows did not contain ground-truth labels. Therefore, the results show model disagreement and alert volume—not verified attacks or live accuracy.

---

## Historical Prototype Result

The earlier synthetic/held-out prototype used 940 rows:

- 830 benign
- 110 attacks

The legacy 2-of-3 ensemble achieved:

| Metric | Result |
|---|---:|
| Accuracy | 98.94% |
| Precision | 96.30% |
| Recall | 94.55% |
| F1 | 95.41% |
| False positives | 4 |
| False negatives | 6 |

This result is retained for project history and regression comparison. It is not the main real-data headline.

---

## Project Layout

Representative layout:

```text
flowguard/
├── capture-cpp/
│   ├── include/
│   │   ├── BlockingQueue.hpp
│   │   ├── FeatureEmitter.hpp
│   │   ├── FlowAggregator.hpp
│   │   ├── FlowKey.hpp
│   │   ├── FlowStats.hpp
│   │   ├── JsonSerializer.hpp
│   │   ├── PacketInfo.hpp
│   │   └── PacketParser.hpp
│   ├── src/
│   │   ├── main.cpp
│   │   ├── PacketParser.cpp
│   │   ├── FlowAggregator.cpp
│   │   ├── FeatureEmitter.cpp
│   │   ├── JsonSerializer.cpp
│   │   ├── benchmark.cpp
│   │   └── parser_benchmark.cpp
│   ├── tests/
│   ├── CMakeLists.txt
│   └── Dockerfile
├── capture-ebpf/
│   ├── xdp_filter.bpf.c
│   ├── xdp_filter.o
│   ├── loader.c
│   ├── loader
│   ├── xdp_parser_benchmark.c
│   └── xdp_parser_benchmark.o
├── ml-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── ml/
│   │   │   ├── ensemble.py
│   │   │   └── real_only_predictor.py
│   │   ├── routes/
│   │   │   └── real_analysis.py
│   │   ├── services/
│   │   └── models/
│   │       └── real_only/
│   ├── data/
│   │   └── real_only/
│   ├── training/
│   │   ├── train_evaluate_real_only.py
│   │   └── tune_real_rf_thresholds.py
│   ├── tests/
│   ├── prisma/
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/
│   ├── index.html
│   └── Dockerfile
├── data/
│   ├── sample/
│   ├── attack_samples/
│   ├── cicids2017/
│   └── flows_output.jsonl
├── docs/
│   ├── cpp_parser_benchmark.txt
│   ├── ebpf_vs_cpp_runs.csv
│   ├── ebpf_vs_cpp_benchmark.json
│   ├── ebpf_vs_cpp_benchmark.md
│   └── model_comparison.json
├── scripts/
│   └── benchmark_ebpf_vs_cpp.sh
├── docker-compose.yml
├── HOW_TO_RUN.md
└── README.md
```

Some generated datasets, model artifacts, PCAPs, and build outputs may be intentionally excluded from Git.

---

## Requirements

### General

- Linux
- Git
- Docker and Docker Compose
- Python 3
- CMake
- A C++17 compiler

### C++ capture

- libpcap
- pthread support

### eBPF/XDP

- Linux kernel with eBPF and XDP support
- Clang/LLVM
- libbpf and development headers
- bpftool
- Linux networking tools (`ip`)
- Root privileges for loading and attaching XDP programs

### Benchmarking

- tcpreplay
- tcpdump
- Python 3
- `kernel.bpf_stats_enabled` support

---

## Quick Start with Docker Compose

From the repository root:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

Expected services:

```text
postgres
redis
capture
ml-service
dashboard
```

Check the API:

```bash
curl http://127.0.0.1:8000/health
curl "http://127.0.0.1:8000/flows/recent?limit=2"
```

Open:

- Dashboard: `http://127.0.0.1:8080`
- OpenAPI documentation: `http://127.0.0.1:8000/docs`

View logs:

```bash
docker compose logs -f ml-service
```

Stop the stack:

```bash
docker compose down
```

Remove the PostgreSQL volume as well:

```bash
docker compose down -v
```

---

## Manual C++ Capture Run

### Configure and compile

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Release

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

### Process a PCAP

```bash
./capture-cpp/build/flowguard_capture \
  data/sample/small_sample.pcap \
  data/flows_output.jsonl
```

### Inspect output

```bash
head -n 5 data/flows_output.jsonl
```

Each line represents one aggregated flow.

---

## Manual FastAPI Run

From the repository root:

```bash
cd ml-service
source .venv/bin/activate
```

Run the selected real-data operating mode:

```bash
RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
python -m uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
```

Using `python -m uvicorn` avoids relying on a globally installed `uvicorn` command.

Check the service:

```bash
curl -s http://127.0.0.1:8000/health | python -m json.tool
```

Check the real model:

```bash
curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
```

Run shadow inference:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=20" \
  | python -m json.tool
```

Compare detectors:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  | python -m json.tool
```

---

## eBPF/XDP Build and Run

### Compile the XDP program

From the repository root:

```bash
clang \
  -O2 \
  -g \
  -target bpf \
  -D__TARGET_ARCH_x86 \
  -c capture-ebpf/xdp_filter.bpf.c \
  -o capture-ebpf/xdp_filter.o
```

Verify the object:

```bash
file capture-ebpf/xdp_filter.o
```

Expected type:

```text
ELF 64-bit LSB relocatable, eBPF
```

### Compile the userspace loader

```bash
cc \
  -O2 \
  -g \
  capture-ebpf/loader.c \
  -o capture-ebpf/loader \
  $(pkg-config --cflags --libs libbpf)
```

### Attach to an interface

First identify the interface:

```bash
ip -br link
```

Then run the loader from the directory containing `xdp_filter.o`:

```bash
cd capture-ebpf
sudo ./loader wlan0
```

Replace `wlan0` with the correct interface.

Press `Ctrl+C` to stop the loader and detach the XDP program.

### Warning

The demonstration packet threshold in `xdp_filter.bpf.c` counts packets over the lifetime of the BPF map entry. It is not a time-windowed packets-per-second production rate limiter.

---

## Model Training and Evaluation

### Expected real-data locations

```text
data/cicids2017/
ml-service/data/real_only/
```

### Real-only training/evaluation

From `ml-service`:

```bash
PYTHONPATH=. \
.venv/bin/python \
training/train_evaluate_real_only.py
```

### Operational-threshold tuning

```bash
PYTHONPATH=. \
.venv/bin/python \
training/tune_real_rf_thresholds.py
```

Generated real-model artifacts are stored under:

```text
ml-service/app/models/real_only/
```

Expected artifacts include:

```text
random_forest.joblib
supervised_scaler.joblib
isolation_forest.joblib
anomaly_scaler.joblib
autoencoder.pt
graphsage_flow_similarity.pt
thresholds.json
rf_operational_thresholds.json
```

### Important reproducibility note

Do not select thresholds using the final Friday test set. The project uses Thursday validation data for threshold selection and Friday data only for final evaluation.

---

## Benchmark Reproduction

### C++ parser benchmark

```bash
./capture-cpp/build-benchmark/flowguard_parser_benchmark \
  data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap \
  7 \
  | tee docs/cpp_parser_benchmark.txt
```

### Full XDP versus C++ benchmark

```bash
chmod +x scripts/benchmark_ebpf_vs_cpp.sh
./scripts/benchmark_ebpf_vs_cpp.sh
```

The script:

- Enables BPF runtime statistics temporarily.
- Creates a temporary veth pair.
- Loads and pins the benchmark XDP program.
- Attaches it in native mode when supported.
- Replays the PCAP multiple times.
- Reads BPF runtime and packet counters.
- Calculates median metrics.
- Writes CSV, JSON, and Markdown reports.
- Detaches XDP and removes the temporary interfaces.

Generated output:

```text
docs/ebpf_vs_cpp_runs.csv
docs/ebpf_vs_cpp_benchmark.json
docs/ebpf_vs_cpp_benchmark.md
```

The benchmark requires `sudo`.

---

## API Reference

### Health

```http
GET /health
```

Basic API health check.

### Recent flows

```http
GET /flows/recent?limit=20
```

Returns the most recent captured flow records.

### Legacy batch analysis

```http
POST /analyze?offset=0&limit=100&persist=false
```

Parameters:

| Parameter | Meaning |
|---|---|
| `offset` | Starting flow index |
| `limit` | Batch size, up to 1,000 |
| `persist` | Save detected anomalies to PostgreSQL |

Use `persist=false` while validating behaviour.

### Alerts

```http
GET /alerts
GET /alerts/{alert_id}
```

Retrieves persisted alerts.

### Historical model metrics

```http
GET /metrics/model
```

Returns the historical held-out prototype metrics. This endpoint does not represent the final real-only Random Forest evaluation.

### Real-data model health

```http
GET /real-model/health
```

Returns:

- Model identifier
- Selected operational threshold
- Operational mode
- Resolved flow file
- Shadow-mode state

### Real-data shadow analysis

```http
POST /real-model/analyze?limit=50
```

Scores recent flows with the real-only Random Forest.

It does not persist alerts.

### Detector comparison

```http
POST /analyze/compare?limit=100
```

Runs the legacy ensemble and real Random Forest on the same recent flows.

Returns:

- Alert totals
- Agreement categories
- Agreement rate
- Real Random Forest probabilities
- Per-flow disagreement information
- Error details

The comparison route never persists alerts.

### Legacy real-capture route

```http
POST /analyse/real
```

This older experimental route is retained for compatibility. Prefer the `/real-model/*` routes for current shadow evaluation.

---

## Testing

### Python tests

```bash
cd ml-service

PYTHONPATH=. \
.venv/bin/python \
-m pytest tests -q
```

Previously verified result:

```text
8 passed
```

Re-run the suite after modifying inference routes or model-loading code.

### C++ tests

Configure and build:

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Debug

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

Run registered tests:

```bash
ctest \
  --test-dir capture-cpp/build \
  --output-on-failure
```

C++ test targets cover areas such as:

- Flow key ordering
- Flow aggregation
- Blocking queue behaviour
- Packet parsing
- JSON serialization

### Syntax checks

Python:

```bash
python -m py_compile \
  ml-service/app/main.py \
  ml-service/app/ml/real_only_predictor.py \
  ml-service/app/routes/real_analysis.py
```

Bash:

```bash
bash -n scripts/benchmark_ebpf_vs_cpp.sh
```

---

## Generated Artifacts

### Model artifacts

```text
ml-service/app/models/real_only/
├── anomaly_scaler.joblib
├── autoencoder.pt
├── graphsage_flow_similarity.pt
├── isolation_forest.joblib
├── random_forest.joblib
├── rf_operational_thresholds.json
├── supervised_scaler.joblib
└── thresholds.json
```

### Evaluation artifacts

```text
docs/
├── cpp_parser_benchmark.txt
├── ebpf_vs_cpp_runs.csv
├── ebpf_vs_cpp_benchmark.json
├── ebpf_vs_cpp_benchmark.md
├── model_comparison.json
└── rf_threshold_tuning.txt
```

### Prepared real-data splits

```text
ml-service/data/real_only/
├── train_real.csv
├── validation_real.csv
└── test_real.csv
```

Large datasets, model files, PCAPs, and generated build files may need Git LFS or external storage rather than ordinary Git commits.

---

## Docker and Infrastructure Notes

### PostgreSQL

PostgreSQL provides durable alert storage.

The Compose configuration uses:

```text
database: flowguard
user: flowguard_user
```

Credentials in the development Compose file are for local use only and must be replaced for deployment.

### Prisma ORM

Prisma provides schema-driven database access.

The ML container startup performs:

1. Wait for PostgreSQL.
2. Wait for Redis.
3. Run `prisma db push`.
4. Run `prisma generate`.
5. Start Uvicorn.

### Redis

Redis is used inside the Compose network for messaging/pub-sub support.

It is not intentionally exposed to the host.

### Capture permissions

The capture container receives:

```text
NET_ADMIN
NET_RAW
```

These capabilities are required for packet-capture and networking operations but should be minimized in production.

### ML image

The ML image installs CPU-only PyTorch packages to avoid pulling unnecessary GPU/CUDA layers for the local CPU inference workflow.

### Dashboard image

The verified dashboard container serves the static dashboard through Nginx.

---

## Design Decisions

### JSONL between C++ and Python

JSON Lines was selected because it is:

- Human-readable.
- Append-friendly.
- Easy to debug with standard shell tools.
- Supported directly by Python.
- Independent of the C++ process lifetime.
- Suitable for replay and offline evaluation.

### Bounded queue instead of an unbounded queue

A bounded queue prevents the capture thread from consuming unlimited memory if the aggregation thread cannot keep pace.

### Model loading at startup

Saved models are loaded once when the API process starts rather than once per request. This reduces inference latency and avoids repeated disk deserialization.

### Shadow deployment

The real-data model does not immediately replace or persist into the existing alert path.

Shadow deployment allows FlowGuard to measure:

- Alert volume.
- Model disagreement.
- Probability distribution.
- Feature-semantic mismatch.
- Domain shift.
- Runtime errors.

### Day-separated evaluation

Capture-day separation was selected to reduce leakage and make the model prove that it can generalize beyond the exact capture distribution used for fitting.

### Median benchmark reporting

Performance results use medians across repeated runs to reduce sensitivity to scheduler noise and occasional outliers.

---

## Limitations and Honest Interpretation

FlowGuard is an engineering and research project, not a production-certified intrusion-detection appliance.

### Live predictions are not ground truth

A live model label of `ATTACK` is a prediction, not confirmation of malicious activity.

Accuracy, precision, and recall require labelled data.

### High live alert rate indicates possible domain shift

The real-only Random Forest produced a high alert rate on the infected-host capture. This can reflect:

- Truly unusual traffic.
- Different feature semantics.
- Dataset-to-live distribution shift.
- Poor probability calibration.
- Incomplete flow reconstruction.

It must not be described as a verified attack rate.

### Balanced final test set

The final test set intentionally contains equal benign and attack counts.

This makes model comparison clear but does not represent the natural attack prevalence of most real networks.

### GraphSAGE limitations

The GraphSAGE model had extremely high recall but very poor benign classification.

It demonstrates graph-learning implementation but requires:

- Better graph construction.
- Calibration.
- Class weighting.
- Additional validation.
- More representative graph data.

### Infected-Android PCAP labels

The infected-Android PCAP does not provide per-flow ground-truth labels.

It is valid for:

- Systems benchmarking.
- Replay.
- End-to-end testing.
- Shadow inference.
- Disagreement analysis.

It is not valid for reporting classification accuracy.

### eBPF benchmark scope

The benchmark compares implemented parser-level cost.

It does not include:

- Flow aggregation parity.
- Machine-learning inference.
- PostgreSQL persistence.
- Redis publication.
- Dashboard latency.
- Complete packet-to-alert latency.

### Demonstration drop threshold

The original XDP source counter is lifetime-based. Production rate limiting requires a time-windowed policy.

---

## Roadmap

### Detection quality

- Probability calibration using isotonic regression or Platt scaling.
- Evaluation on naturally imbalanced traffic.
- Precision-recall curves and confidence intervals.
- Leave-one-attack-family-out testing.
- Better Bot-family coverage.
- Weighted voting or stacking instead of strict agreement.
- Incident-level alert grouping.
- Feature-semantic alignment between C++ flows and CICIDS flow generation.

### Graph learning

- True IP host-communication graphs.
- Temporal graph construction.
- Class-weighted GraphSAGE loss.
- Focal loss.
- Graph mini-batching.
- Validation-based early stopping.
- Neighbourhood and edge-feature ablation studies.

### eBPF/XDP

- Time-windowed packet-rate limiting.
- Production per-CPU counters.
- Ring-buffer loss counters.
- IPv6 parsing.
- VLAN support.
- AF_XDP experiment.
- Multi-core scaling benchmark.
- Physical-NIC benchmark.
- Packet-to-alert latency measurement.

### Backend and operations

- Prometheus metrics.
- Grafana dashboards.
- Authentication and role-based access.
- Model registry and rollback.
- Alert deduplication.
- Deployment-specific secrets.
- CI for Python, C++, Docker, and eBPF verifier checks.
- Structured logging and tracing.

---

## Resume-Ready Summary

### Detailed version

> Built FlowGuard, a full-stack network intrusion detection platform using C++17/libpcap, native XDP/eBPF, FastAPI, PostgreSQL, Redis, Prisma ORM, and Docker Compose. Trained Random Forest, Isolation Forest, a PyTorch Autoencoder, and GraphSAGE on capture-day-separated CICIDS2017 data; Random Forest achieved 86.09% accuracy, 98.94% recall, 78.71% precision, and 0.8767 F1 on 10,000 real labelled flows. Benchmarked native XDP across seven runs and approximately 1.46 million packets per run, achieving 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than the C++ userspace parser.

### Compact bullets

- Built a C++17/Python network intrusion detection pipeline using libpcap, native XDP/eBPF, five-tuple flow aggregation, FastAPI, PostgreSQL, Redis, and Docker Compose.
- Achieved **86.09% accuracy, 98.94% recall, and 0.8767 F1** with Random Forest on **10,000 real capture-day-separated CICIDS2017 flows**.
- Reduced Random Forest false positives by **54.3%** with a strict four-model ensemble, improving precision to **86.96%** while documenting the recall trade-off.
- Benchmarked native XDP at **62.3 ns/packet and 16.05M equivalent packets/s**, delivering **1.77× higher equivalent throughput** than the C++ parser.

---

## Technology Keywords

### Languages and systems

```text
C++17, C, Python, SQL, Bash, JavaScript, Linux, systems programming,
multithreading, producer-consumer, bounded queue, backpressure, mutex,
condition variable, atomic state, kernel programming
```

### Networking

```text
libpcap, PCAP, tcpreplay, Ethernet, IPv4, TCP, UDP, ICMP, five-tuple,
flow aggregation, TCP flags, packet parsing, network telemetry,
network intrusion detection, NIDS, DDoS, PortScan, Bot detection
```

### eBPF/XDP

```text
eBPF, XDP, native XDP, libbpf, bpftool, BPF maps, per-CPU maps,
ring buffer, kernel-space packet processing, packet filtering,
nanoseconds per packet, packets per second
```

### Machine learning

```text
scikit-learn, PyTorch, PyTorch Geometric, Random Forest,
Isolation Forest, Autoencoder, GraphSAGE, GNN, anomaly detection,
supervised learning, unsupervised learning, feature engineering,
threshold tuning, ensemble learning, ROC-AUC, precision, recall,
F1 score, confusion matrix, domain shift, data leakage,
capture-day separation, model generalization, shadow deployment
```

### Backend and DevOps

```text
FastAPI, REST API, Uvicorn, PostgreSQL, Prisma ORM, Redis, pub/sub,
Docker, Docker Compose, Nginx, CMake, Clang, health checks,
model serving, persistent storage, internal service networking
```

---

## Security and Research Notice

FlowGuard is intended for authorized defensive-security research, learning, benchmarking, and controlled network monitoring.

Only capture, replay, or inspect traffic on systems and networks where you have permission.

Model outputs should be reviewed by a human analyst before being treated as confirmed security incidents.

---

## Current Verified Headline

> **FlowGuard achieved 86.09% accuracy, 98.94% recall, and 0.8767 F1 on 10,000 real capture-day-separated CICIDS2017 flows, while its native XDP parser delivered 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than its C++ userspace parser.**
