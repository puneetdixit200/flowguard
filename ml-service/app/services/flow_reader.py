import json
from pathlib import Path


# This file is located at:
# flowguard/ml-service/app/services/flow_reader.py
#
# parents[3] points to the main flowguard folder:
# /home/pd/Downloads/flowguard
PROJECT_ROOT = Path(__file__).resolve().parents[3]

CANDIDATE_FLOW_FILES = [
    PROJECT_ROOT / "data" / "flows_output.jsonl",              # local C++ output
    PROJECT_ROOT / "ml-service" / "data" / "flows_output.jsonl", # copied local file
    Path("/app/data/flows_output.jsonl"),                      # Docker path
]


def get_flow_file_path():
    for path in CANDIDATE_FLOW_FILES:
        if path.exists():
            return path
    return CANDIDATE_FLOW_FILES[0]


def read_all_flows():
    flow_file = get_flow_file_path()

    if not flow_file.exists():
        return []

    flows = []

    with flow_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                flows.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return flows
