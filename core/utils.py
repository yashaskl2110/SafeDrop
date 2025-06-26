import csv
import os
from datetime import datetime
from cryptography.fernet import Fernet

# ----------------------------------------
# 1. Sanitize sensitive values for logs and UI
# ----------------------------------------
def sanitize(value):
    """Mask all but last 6 characters."""
    if not value or len(value) <= 6:
        return "******"
    return "****" + value[-6:]

# ----------------------------------------
# 2. Load allowlist from file
# ----------------------------------------
def load_allowlist(path="core/allowlist.txt"):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            patterns = [line.strip() for line in f if line.strip()]
        return set(patterns)
    except FileNotFoundError:
        return set()

# ----------------------------------------
# 3. Log detection (sanitized CSV)
# ----------------------------------------
def log_detection(file_path, label, match_text, log_file="logs/detections_log.csv"):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    masked = sanitize(match_text)
    with open(log_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([time_now, file_path, label, masked])

# ----------------------------------------
# 4. AES Encryption Setup
# ----------------------------------------
KEY_PATH = "core/secret.key"
ENCRYPTED_LOG_FILE = "logs/encrypted_leaks.log"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, 'wb') as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_PATH):
        generate_key()
    with open(KEY_PATH, 'rb') as f:
        return f.read()

def get_fernet():
    return Fernet(load_key())

# ----------------------------------------
# 5. Encrypted raw log (unsanitized)
# ----------------------------------------
def encrypt_and_log_raw(file_path, label, value):
    fernet=get_fernet()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    raw_log = f"{time_now} | {file_path} | {label} | {value}"
    encrypted = fernet.encrypt(raw_log.encode())

    with open(ENCRYPTED_LOG_FILE, 'ab') as f:
        f.write(encrypted + b'\n')
