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
            "operational_mode": predictor.operational_mode,
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
        "operational_mode": predictor.operational_mode,
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
