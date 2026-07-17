# FlowGuard Run Guide

This is the tested runbook for FlowGuard as of Friday, July 17, 2026.

## Preferred Path: Docker Compose

From the repo root:

```bash
docker compose up -d --build
```

Check container state:

```bash
docker compose ps
```

Expected services:

- `postgres`
- `redis`
- `capture`
- `ml-service`
- `dashboard`

Verify the API:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/flows/recent?limit=2
```

Verify the dashboard:

```bash
curl -I http://127.0.0.1:8080
```

Open in browser:

- Dashboard: `http://127.0.0.1:8080`
- OpenAPI docs: `http://127.0.0.1:8000/docs`

## Startup Behavior

The ML container does the following on startup:

1. waits for Postgres
2. waits for Redis
3. runs `prisma db push`
4. runs `prisma generate`
5. starts `uvicorn app.main:app --host 0.0.0.0 --port 8000`

This means the API can take a few seconds longer than the other containers to
accept requests.

## Manual API Run

If you want to run the API outside Docker:

```bash
cd ml-service
PYTHONPATH=. .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Required local services for that mode:

- PostgreSQL on `127.0.0.1:5432`
- Redis on `127.0.0.1:6379`

## Evaluation

Run the held-out evaluation:

```bash
cd ml-service
PYTHONPATH=. .venv/bin/python training/evaluate_models.py
```

Verified metrics from Friday, July 17, 2026:

- Isolation Forest Accuracy: `0.9511`
- Isolation Forest F1: `0.8175`
- Random Forest Accuracy: `0.9521`
- Autoencoder Accuracy: `0.9415`
- Autoencoder F1: `0.7737`
- Ensemble Accuracy: `0.9894`
- Ensemble Precision: `0.9630`
- Ensemble Recall: `0.9455`
- Ensemble F1: `0.9541`
- False positives: `4`
- False negatives: `6`

Full output is stored in [docs/evaluation_report.txt](/home/pd/Downloads/flowguard/docs/evaluation_report.txt).

## Tests

Run Python tests:

```bash
cd ml-service
PYTHONPATH=. .venv/bin/python -m pytest tests -q
```

Verified result on Friday, July 17, 2026:

```text
8 passed
```

## Shutdown

```bash
docker compose down
```

To also remove the Postgres volume:

```bash
docker compose down -v
```
