import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# File handlers
from handlers.txt_handler import handle_txt
from handlers.pdf_handler import handle_pdf
from handlers.docx_handler import handle_docx
from handlers.json_handler import handle_json
from handlers.csv_handler import handle_csv
from handlers.env_handler import handle_env
from handlers.log_handler import handle_log
from handlers.zip_handler import handle_zip

# Prevent rapid duplicate triggers
recent_files = {}
DUPLICATE_TIMEOUT = 1.0

class FileAlert(FileSystemEventHandler):
    def __init__(self, callback=None):
        self.log_callback = callback

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        ext = os.path.splitext(file_path)[-1].lower()
        now = time.time()

        # Debounce repeated triggers
        if file_path in recent_files and now - recent_files[file_path] < DUPLICATE_TIMEOUT:
            return
        recent_files[file_path] = now

        print(f"[+] File added: {file_path}")
        time.sleep(0.3)  # Small delay to ensure file is ready

        try:
            def run_handler(handler_func):
                leaks = handler_func(file_path)
                if leaks and self.log_callback:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    for label, value in leaks:
                        self.log_callback(timestamp, file_path, label, value)

            handler_map = {
                ".txt": handle_txt,
                ".pdf": handle_pdf,
                ".docx": handle_docx,
                ".json": handle_json,
                ".csv": handle_csv,
                ".env": handle_env,
                ".log": handle_log,
                ".zip": handle_zip
            }

            handler = handler_map.get(ext)
            if handler:
                run_handler(handler)
            else:
                print(f"[!] Unsupported file type: {ext}")

        except Exception as e:
            print(f"[!] Error handling file: {e}")

def start_watching(folder, log_callback=None):
    print(f"🛡️ SafeDrop is watching: {folder}")
    observer = Observer()
    observer.schedule(FileAlert(callback=log_callback), folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped.")
        observer.stop()
    observer.join()
