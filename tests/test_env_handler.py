import tempfile
from unittest.mock import patch, MagicMock
from handlers import env_handler

LEAKY_ENV = 'DB_PASS = supersecretpass123'

@patch("handlers.env_handler.log_detection")
@patch("handlers.env_handler.encrypt_and_log_raw")
def test_handle_env_detects_leak(mock_encrypt, mock_log):
    # Create a temporary .env file with a leak
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as tmp:
        tmp.write(LEAKY_ENV)
        tmp_path = tmp.name

    results = env_handler.handle_env(tmp_path)

    # ✅ Check leak is detected
    assert results, "Should detect at least one leak"

    # ✅ Check label
    assert any(label == "env_dbpass" for label, _ in results)

    # ✅ Ensure it was logged
    mock_log.assert_called()
