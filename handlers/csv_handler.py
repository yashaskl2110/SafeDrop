import csv
from core.detectors import detect_leaks
from core.utils import log_detection, encrypt_and_log_raw

def handle_csv(file_path):
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                for key, value in row.items():
                    text = f"{key}:{value}"
                    leaks = detect_leaks(text)

                    for leak_type, match in leaks:
                        print(f"[{leak_type}] {match}")
                        log_detection(file_path, leak_type, match)
                        encrypt_and_log_raw(file_path, leak_type, match)
                        results.append((leak_type, match))

    except Exception as e:
        print(f"[CSV ERROR] {file_path}: {e}")

    return results
