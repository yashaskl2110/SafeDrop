import os
import sys
import pytest
from cryptography.fernet import Fernet

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.utils import sanitize, load_allowlist, encrypt_and_log_raw, get_fernet

def test_sanitize_short():
    assert sanitize("abc") == "******"

def test_sanitize_long():
    assert sanitize("mysecretpassword") == "****ssword"

def test_allowlist_loading(tmp_path):
    allowlist_path = tmp_path / "allowlist.txt"
    allowlist_path.write_text("safe_value\nanother\n")
    result = load_allowlist(str(allowlist_path))
    assert "safe_value" in result
    assert "another" in result
    assert "not_in_list" not in result

def test_encrypt_and_log_raw(tmp_path, monkeypatch):
    log_file = tmp_path / "encrypted_test.log"
    key_file = tmp_path / "test.key"

    # Create and save a test key
    test_key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(test_key)

    # Patch the key path and log file used in utils.py
    monkeypatch.setattr("core.utils.KEY_PATH", str(key_file))
    monkeypatch.setattr("core.utils.ENCRYPTED_LOG_FILE", str(log_file))

    # Use actual encrypt function from utils with patched key + log
    encrypt_and_log_raw("test.txt", "api_key", "123456")

    # Decrypt and validate contents
    with open(log_file, "rb") as f:
        encrypted_line = f.readline().strip()
    decrypted = get_fernet().decrypt(encrypted_line).decode()

    assert "api_key" in decrypted
    assert "123456" in decrypted
