import tempfile
import json
from unittest.mock import patch, MagicMock
from handlers import json_handler

# This matches the env_apikey regex: 'API_KEY=sk_live_1234567890'
LEAKY_JSON = {"config": 'API_KEY = sk_live_1234567890'}

@patch("handlers.json_handler.log_detection")
@patch("handlers.json_handler.encrypt_and_log_raw")
def test_handle_json_detects_leak(mock_encrypt, mock_log):
    # ✅ Write leaky JSON to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json.dump(LEAKY_JSON, tmp)
        tmp_path = tmp.name

    # ✅ Run handler
    results = json_handler.handle_json(tmp_path)

    # ✅ Assert at least one leak is found
    assert results, "Should detect at least one leak"

    # ✅ Confirm it’s the correct leak type
    assert any(label == "env_apikey" for label, _ in results)

    # ✅ Make sure log was triggered
    mock_log.assert_called()
