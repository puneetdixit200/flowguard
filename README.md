# FlowGuard

FlowGuard is a network-flow anomaly detection project with four main parts:

- `capture-cpp`: C++ packet-to-flow aggregation
- `ml-service`: FastAPI inference service backed by PostgreSQL and Redis
- `dashboard`: static HTML dashboard served by Nginx
- `docker-compose.yml`: end-to-end local stack definition

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

- `docker compose up -d --build` succeeds
- API health check returns `200` at `http://127.0.0.1:8000/health`
- Dashboard returns `200` at `http://127.0.0.1:8080`
- `GET /flows/recent` returns captured sample flow data
- Python tests pass: `8 passed`
- Held-out evaluation completed on `ml-service/data/sample/test_holdout.csv`

## Project Layout

```text
flowguard/
├── capture-cpp/
├── capture-ebpf/
├── dashboard/
├── data/
├── docs/
├── ml-service/
├── docker-compose.yml
└── HOW_TO_RUN.md
```

## Quick Start

```bash
docker compose up -d --build
```

Then check:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/flows/recent?limit=2
```

Open:

- Dashboard: `http://127.0.0.1:8080`
- API docs: `http://127.0.0.1:8000/docs`

Notes:

- PostgreSQL and Redis are intentionally not published to host ports in
  `docker-compose.yml`. They are only used internally by the compose network.
- The ML container waits for Postgres and Redis, runs `prisma db push`, then
  starts Uvicorn.
- First startup of `ml-service` takes a few extra seconds because Prisma
  generates its client during container boot.

## Manual Run

If you want to run only the API locally:

```bash
cd ml-service
PYTHONPATH=. .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

If you want to evaluate the saved models locally:

```bash
cd ml-service
PYTHONPATH=. .venv/bin/python training/evaluate_models.py
```

## Test Results

Python API tests:

```bash
cd ml-service
PYTHONPATH=. .venv/bin/python -m pytest tests -q
```

Verified result on Friday, July 17, 2026:

```text
8 passed
```

## Model Metrics

Held-out test set: `940` rows total

- Benign: `830`
- Attacks: `110`

Ensemble results:

- Accuracy: `0.9894`
- Precision: `0.9630`
- Recall: `0.9455`
- F1: `0.9541`
- False positives: `4`
- False negatives: `6`

Full report: [docs/evaluation_report.txt](/home/pd/Downloads/flowguard/docs/evaluation_report.txt)

Additional model notes:

- [docs/ml-models.md](/home/pd/Downloads/flowguard/docs/ml-models.md)
- [docs/false-positive-analysis.md](/home/pd/Downloads/flowguard/docs/false-positive-analysis.md)
- [docs/case-study.md](/home/pd/Downloads/flowguard/docs/case-study.md)
- [docs/threading-model.md](/home/pd/Downloads/flowguard/docs/threading-model.md)

## API Endpoints

- `GET /health`
- `GET /flows/recent?limit=20`
- `POST /analyze`
- `GET /alerts`
- `GET /alerts/{alert_id}`
- `GET /metrics/model`
- `POST /analyse/real`

## Docker Notes

Docker-specific fixes applied and verified:

- `dashboard/Dockerfile` now serves the existing static dashboard with Nginx
  instead of expecting a missing React/Vite build pipeline
- `ml-service/Dockerfile` installs CPU-only PyTorch wheels instead of pulling
  large default GPU stacks
- `ml-service` waits for Postgres and Redis before startup
- Redis host and port are environment-driven, so the service works in compose
- Prisma client generation is built into the image and refreshed at container
  startup after schema sync
- `.dockerignore` files prevent local build outputs and virtualenv contents from
  bloating the image contexts
