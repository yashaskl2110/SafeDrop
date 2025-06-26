import tempfile
import os
from unittest.mock import patch
from handlers import txt_handler

LEAK_CONTENT = "password = hunter2"

@patch("handlers.txt_handler.log_detection")
@patch("handlers.txt_handler.encrypt_and_log_raw")
def test_txt_handler_detects_leak(mock_encrypt, mock_log):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp:
        tmp.write(LEAK_CONTENT)
        tmp_path = tmp.name

    try:
        results = txt_handler.handle_txt(tmp_path)
        assert results  # ✅ Leak must be detected
        mock_log.assert_called()  # ✅ Confirm log_detection was called
        mock_encrypt.assert_called()  # ✅ Confirm encryption was called
    finally:
        os.remove(tmp_path)
 