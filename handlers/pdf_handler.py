import pdfplumber
from core.detectors import detect_leaks
from core.utils import log_detection, encrypt_and_log_raw

def handle_pdf(file_path):
    try:
        content = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                content += page.extract_text() or ""

        leaks = detect_leaks(content)
        results = []

        for label, match in leaks:
            print(f"[{label}] {match}")
            log_detection(file_path, label, match)         # ➤ Masked for UI/CSV
            encrypt_and_log_raw(file_path, label, match)   # ➤ Encrypted for secure backup
            results.append((label, match))

        return results

    except Exception as e:
        print(f"[PDF ERROR] {file_path}: {e}")
        return []
