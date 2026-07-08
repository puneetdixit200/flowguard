# FlowGuard

Intelligent network traffic analysis and threat detection platform.

## What it does
Captures network traffic, aggregates packets into flows, extracts security features,
runs a 3-model ML ensemble (Isolation Forest + Random Forest + Autoencoder), and
surfaces alerts through a REST API and live dashboard.

## Architecture
See `docs/architecture.md` and `docs/threading-model.md`.

## Quick start (Docker)
\`\`\`bash
docker compose up --build
\`\`\`
- Dashboard: http://localhost:8080
- API: http://localhost:8000/health

## Quick start (manual)
\`\`\`bash
# 1. C++ capture
cd capture-cpp/build && cmake .. && make && ./flowguard_capture

# 2. Python API
cd ml-service && uvicorn app.main:app --reload

# 3. Dashboard
open dashboard/index.html
\`\`\`

## Tests
\`\`\`bash
# C++
cd capture-cpp/build && ctest --output-on-failure

# Python
cd ml-service && pytest tests/ -v
\`\`\`

## Sample flow JSON
\`\`\`json
{"src_ip":"10.0.0.1","dst_ip":"10.0.0.2","src_port":51514,"dst_port":80,
 "protocol":"TCP","packet_count":42,"total_bytes":6300,
 "duration_seconds":1.2,"syn_count":1,"ack_count":40,"fin_count":1,"rst_count":0}
\`\`\`

## Model metrics
See `docs/ml-models.md` and run `training/evaluate_models.py` for live output.

## Tech stack
C++17, libpcap, Python, FastAPI, scikit-learn, PyTorch, Docker Compose, static HTML dashboard.
