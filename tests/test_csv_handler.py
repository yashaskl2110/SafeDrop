import sys
import os
import tempfile
import csv
from unittest.mock import patch

# Make sure 'handlers' is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from handlers import csv_handler

LEAKY_ROW = {"email": "admin@example.com", "EMAIL_PASS": "hunter2"}

@patch("handlers.csv_handler.log_detection")
@patch("handlers.csv_handler.encrypt_and_log_raw")
def test_handle_csv_detects_leak(mock_encrypt, mock_log):
    with tempfile.NamedTemporaryFile(mode="w", newline='', suffix=".csv", delete=False) as tmp:
        writer = csv.DictWriter(tmp, fieldnames=LEAKY_ROW.keys())
        writer.writeheader()
        writer.writerow(LEAKY_ROW)
        tmp_path = tmp.name

    results = csv_handler.handle_csv(tmp_path)

    assert results, "Should detect at least one leak"
    assert any(label == "env_emailpass" for label, _ in results)
    mock_log.assert_called()
