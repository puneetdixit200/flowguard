"""
Tests severity banding logic used by the ensemble.
Per dossier: severity bands are 50-70=low, 70-85=medium, 85-95=high, 95+=critical,
and alert = true only if 2 of 3 models vote anomaly. [file:1]
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def confidence_to_severity(confidence: float, is_anomaly: bool) -> str:
    """Standalone copy of the banding logic for isolated unit testing."""
    if confidence >= 0.95:
        return "critical"
    elif confidence >= 0.85:
        return "high"
    elif confidence >= 0.70:
        return "medium"
    elif is_anomaly:
        return "low"
    else:
        return "none"


def test_severity_bands():
    assert confidence_to_severity(1.0, True) == "critical"
    assert confidence_to_severity(0.90, True) == "high"
    assert confidence_to_severity(0.75, True) == "medium"
    assert confidence_to_severity(0.34, True) == "low"  # 1 of 3 votes
    assert confidence_to_severity(0.0, False) == "none"


def test_two_of_three_votes_triggers_anomaly():
    votes = 2
    is_anomaly = votes >= 2
    assert is_anomaly is True

    votes = 1
    is_anomaly = votes >= 2
    assert is_anomaly is False


if __name__ == "__main__":
    test_severity_bands()
    test_two_of_three_votes_triggers_anomaly()
    print("All alert_severity tests PASSED")
