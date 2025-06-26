import os
import tempfile
import zipfile
from unittest.mock import patch
from handlers import zip_handler

LEAKY_CONTENT = "API_KEY = sk_test_abc1234567890"

@patch("handlers.txt_handler.log_detection")
@patch("handlers.txt_handler.encrypt_and_log_raw")
def test_handle_zip_detects_leak(mock_encrypt, mock_log):
    # Step 1: Create a leaky .txt file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as leaky_file:
        leaky_file.write(LEAKY_CONTENT)
        leaky_file_path = leaky_file.name

    # Step 2: Zip that file
    zip_path = tempfile.NamedTemporaryFile(suffix=".zip", delete=False).name
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(leaky_file_path, arcname="leaky.txt")

    # Step 3: Call the handler
    results = zip_handler.handle_zip(zip_path)

    # Step 4: Assertions
    assert results, "Should detect at least one leak"
    assert any(label == "env_apikey" for label, _ in results)
    mock_log.assert_called()

    # Cleanup
    os.remove(leaky_file_path)
    os.remove(zip_path)
