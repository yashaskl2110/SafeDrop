import tempfile
from unittest.mock import patch, MagicMock
from handlers import pdf_handler

LEAKY_TEXT = "KEY = sk_live_1234567890"  # This matches the `api_key` pattern

@patch("core.utils.log_detection")
@patch("core.utils.encrypt_and_log_raw")
@patch("pdfplumber.open")
def test_handle_pdf_detects_leak(mock_pdf_open, mock_encrypt, mock_log):
    # Simulate a PDF with one page and leak text
    mock_page = MagicMock()
    mock_page.extract_text.return_value = LEAKY_TEXT
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page]
    mock_pdf_open.return_value.__enter__.return_value = mock_pdf

    with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf") as tmp:
        tmp.write(b"%PDF-1.4 fake content")
        tmp.seek(0)

        results = pdf_handler.handle_pdf(tmp.name)
        assert results, "Should detect at least one leak"
        assert any(label == "api_key" for label, _ in results)  # ✅ FIXED label check
