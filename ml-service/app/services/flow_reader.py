import _json
import os

FLOW_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "data", "flow_output.jsonl"
)


def read_all_flows() -> list[dict]:
    if not os.path.exists(FLOW_FILE):
        return []
    flows = []
    with open(FLOWS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                flows.append(json.loads(line))
    return flows
