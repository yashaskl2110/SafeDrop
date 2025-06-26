import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import detectors

def test_detect_api_key_label():
    text = 'api_key = "sk_test_abcdef1234567890"'
    results = detectors.detect_leaks(text)
    assert any(label in ["env_apikey", "api_key"] for label, _ in results)

def test_detect_aws_key():
    text = "AKIAIOSFODNN7EXAMPLE"
    results = detectors.detect_leaks(text)
    assert any(label == "aws_key" for label, _ in results)

def test_detect_slack_hook():
    text = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
    results = detectors.detect_leaks(text)
    assert any(label == "slack_hook" for label, _ in results)

def test_allowlist_removes_match(monkeypatch):
    # Patch the allowlist used inside detect_leaks
    monkeypatch.setattr(detectors, "allowlist", {"safe_value_from_file"})

    text = "api_key = safe_value_from_file"
    results = detectors.detect_leaks(text)

    # Should not return any leak because value is in allowlist
    assert not results
