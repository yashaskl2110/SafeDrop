import json
from core.detectors import detect_leaks
from core.utils import log_detection, encrypt_and_log_raw

def flatten_json(data, parent_key='', sep='.'):
    items = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.extend(flatten_json(v, new_key, sep))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            new_key = f"{parent_key}[{i}]"
            items.extend(flatten_json(v, new_key, sep))
    else:
        items.append((parent_key, str(data)))
    return items

def handle_json(file_path):
    leaks_found = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)

        for key, value in flatten_json(content):
            lowered_key = key.lower()
            entry = f"{key}:{value}"

            if 'username' in lowered_key:
                leaks_found.append(('username', entry))
                log_detection(file_path, 'username', entry)
                encrypt_and_log_raw(file_path, 'username', entry)

            elif 'password' in lowered_key:
                leaks_found.append(('password', entry))
                log_detection(file_path, 'password', entry)
                encrypt_and_log_raw(file_path, 'password', entry)

            else:
                for label, match in detect_leaks(value):
                    combined = f"{key}:{match}"
                    leaks_found.append((label, combined))
                    log_detection(file_path, label, combined)
                    encrypt_and_log_raw(file_path, label, combined)

    except Exception as e:
        print(f"[JSON ERROR] {file_path}: {e}")

    return leaks_found
