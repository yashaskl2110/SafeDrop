from cryptography.fernet import Fernet
import os

# ----------------------------------------
# Configuration
# ----------------------------------------
KEY_FILE = "core/secret.key"  # Location of AES key
ENCRYPTED_LOG = "logs/encrypted_leaks.log"  # Encrypted log file path

# ----------------------------------------
# Load the encryption key
# ----------------------------------------
def load_key():
    if not os.path.exists(KEY_FILE):
        print("❌ Key file not found.")
        return None
    with open(KEY_FILE, 'rb') as f:
        return f.read()

# ----------------------------------------
# Decrypt and display logs
# ----------------------------------------
def decrypt_logs():
    key = load_key()
    if not key:
        return

    fernet = Fernet(key)

    if not os.path.exists(ENCRYPTED_LOG):
        print("❌ Encrypted log file not found.")
        return

    print("🔓 Decrypted Logs:\n")

    with open(ENCRYPTED_LOG, 'rb') as f:
        for line in f:
            try:
                decrypted = fernet.decrypt(line.strip()).decode()
                print(decrypted)
            except Exception as e:
                print(f"[!] Failed to decrypt line: {e}")

# ----------------------------------------
# Run standalone
# ----------------------------------------
if __name__ == "__main__":
    decrypt_logs()
