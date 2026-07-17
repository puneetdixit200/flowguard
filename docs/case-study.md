# FlowGuard Case Study

## Objective

Build a local network anomaly detection pipeline that:

- converts packets into flows
- scores flows with a three-model ensemble
- stores alerts in PostgreSQL
- broadcasts alert activity through Redis
- exposes status through a FastAPI API and dashboard

## Implementation

- `capture-cpp` handles flow aggregation in C++ with libpcap
- `ml-service` loads saved models once at process start and exposes inference via FastAPI
- PostgreSQL stores durable alert records
- Redis publishes alert activity and caches counts
- `dashboard` is a static frontend served by Nginx

## Docker Outcome

Verified on Friday, July 17, 2026:

- `docker compose up -d --build` succeeds
- the API is reachable on `http://127.0.0.1:8000`
- the dashboard is reachable on `http://127.0.0.1:8080`

Key Docker corrections:

- the dashboard image now matches the actual static frontend
- the ML image installs CPU-only PyTorch wheels
- Redis configuration is environment-driven instead of hardcoded to `localhost`
- Prisma setup is performed automatically during container startup
- Postgres and Redis no longer publish host ports, which avoids local-port conflicts

## Evaluation Results

Held-out dataset size:

- `940` rows
- `830` benign
- `110` attack

Final ensemble metrics:

- Accuracy: `0.9894`
- Precision: `0.9630`
- Recall: `0.9455`
- F1: `0.9541`
- False positives: `4`
- False negatives: `6`

## Main Findings

- The ensemble materially outperforms the individual anomaly detectors.
- Aggregate accuracy on the Random Forest is good, but minority attack classes
  are still harder than the top-line metric suggests.
- Container startup correctness mattered as much as model quality; the previous
  Docker path was not aligned with the actual repo contents or runtime dependencies.

## Follow-Up Work

- move Prisma generation out of runtime startup if container boot time matters
- either wire the saved GNN into the live API path or explicitly treat it as offline-only
- add integration tests for `/alerts` against a real disposable Postgres instance
