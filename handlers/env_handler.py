from core.detectors import detect_leaks
from core.utils import log_detection, encrypt_and_log_raw

def handle_env(file_path):
    leaks_found = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        for label, match in detect_leaks(content):
            log_detection(file_path, label, match)        # Masked for CSV/UI
            encrypt_and_log_raw(file_path, label, match)  # Encrypted for secure storage
            leaks_found.append((label, match))
    except Exception as e:
        print(f"[ENV ERROR] {file_path}: {e}")

    return leaks_found
