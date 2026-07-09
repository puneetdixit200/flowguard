"""
Tests that feature normalization produces the correct shape and values.
Per dossier: "feature normalization shape is correct" is a required test. [file:1]
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.feature_normalizer import normalize_flow


def test_normalize_flow_basic():
    raw_flow = {
        "src_ip": "10.0.0.1",
        "dst_ip": "10.0.0.2",
        "protocol": "TCP",
        "packet_count": 100,
        "total_bytes": 5000,
        "duration_seconds": 2.0,
        "syn_count": 10,
        "ack_count": 5,
        "rst_count": 2,
    }

    result = normalize_flow(raw_flow)

    # Check all expected keys exist.
    expected_keys = {
        "src_ip",
        "dst_ip",
        "protocol",
        "packet_count",
        "total_bytes",
        "duration_seconds",
        "bytes_per_sec",
        "packets_per_sec",
        "syn_ack_ratio",
        "rst_ratio",
    }
    assert expected_keys.issubset(result.keys())

    # Check derived math is correct: bytes_per_sec = total_bytes / duration.
    assert result["bytes_per_sec"] == 5000 / 2.0
    assert result["packets_per_sec"] == 100 / 2.0
    assert result["syn_ack_ratio"] == 10 / 5


def test_normalize_flow_zero_duration_does_not_crash():
    # Zero duration must not cause a ZeroDivisionError (we clamp to 0.0001).
    raw_flow = {"duration_seconds": 0, "packet_count": 5, "total_bytes": 500}
    result = normalize_flow(raw_flow)
    assert result["bytes_per_sec"] > 0  # should be a huge number, not a crash


if __name__ == "__main__":
    test_normalize_flow_basic()
    test_normalize_flow_zero_duration_does_not_crash()
    print("All feature_normalizer tests PASSED")
