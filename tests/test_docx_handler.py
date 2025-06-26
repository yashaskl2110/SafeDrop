import tempfile
from unittest.mock import patch, MagicMock
from docx import Document
from handlers import docx_handler

LEAKY_TEXT = 'API_KEY = mysecretkey12345678'

@patch("handlers.docx_handler.log_detection")
@patch("handlers.docx_handler.encrypt_and_log_raw")
def test_handle_docx_detects_leak(mock_encrypt, mock_log):
    # Create a temporary .docx file with leaky content
    doc = Document()
    doc.add_paragraph(LEAKY_TEXT)

    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        doc.save(tmp.name)
        tmp_path = tmp.name

    results = docx_handler.handle_docx(tmp_path)

    # ✅ Should detect at least one leak
    assert results, "Should detect at least one leak"

    # ✅ Leak label should match expected regex
    assert any(label == "env_apikey" for label, _ in results)

    # ✅ Logging function should be called
    mock_log.assert_called()
