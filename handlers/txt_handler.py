from core.detectors import detect_leaks
from core.utils import log_detection, encrypt_and_log_raw

def handle_txt(file_path):
    results = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        leaks = detect_leaks(content)

        for label, match in leaks:
            print(f"[{label}] {match}")
            log_detection(file_path, label, match)         # ➤ Masked (for CSV/UI)
            encrypt_and_log_raw(file_path, label, match)   # ➤ Encrypted (for backup)
            results.append((label, match))

    except Exception as e:
        print(f"[TXT ERROR] {file_path}: {e}")

    return results
