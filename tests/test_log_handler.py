import tempfile
from unittest.mock import patch
from handlers import log_handler

LEAK_CONTENT = "EMAIL_PASS = hunter2"

@patch("handlers.log_handler.log_detection")
@patch("handlers.log_handler.encrypt_and_log_raw")
def test_log_handler_detects_leak(mock_encrypt, mock_log):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as tmp:
        tmp.write(LEAK_CONTENT)
        tmp_path = tmp.name

    results = log_handler.handle_log(tmp_path)

    assert results, "Should detect leak"
    assert any(label == "env_emailpass" for label, _ in results)
    mock_log.assert_called()
