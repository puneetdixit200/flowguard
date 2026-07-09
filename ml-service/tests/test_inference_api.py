"""
API contract tests using FastAPI's TestClient.
Per dossier: "API endpoints return valid JSON" is a required test. [file:1]
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_alerts_endpoint_returns_list():
    response = client.get("/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_flows_recent_returns_list():
    response = client.get("/flows/recent")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_alert_not_found_returns_404():
    response = client.get("/alerts/999999")
    assert response.status_code == 404


if __name__ == "__main__":
    test_health_endpoint()
    test_alerts_endpoint_returns_list()
    test_flows_recent_returns_list()
    test_alert_not_found_returns_404()
    print("All inference_api tests PASSED")
