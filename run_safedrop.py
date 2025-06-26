import os
from core.watcher import start_watching

WATCH_PATH = "C:\\infostealer_test"  # You can change this to any folder path you want to monitor

if __name__ == "__main__":
    os.makedirs(WATCH_PATH, exist_ok=True)
    print(f"🔍 Monitoring folder: {WATCH_PATH}")
    start_watching(WATCH_PATH)
