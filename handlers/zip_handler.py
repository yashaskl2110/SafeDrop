import os
import zipfile
import tempfile

from handlers.txt_handler import handle_txt
from handlers.pdf_handler import handle_pdf
from handlers.docx_handler import handle_docx
from handlers.json_handler import handle_json
from handlers.csv_handler import handle_csv
from handlers.env_handler import handle_env
from handlers.log_handler import handle_log

def handle_zip(zip_path):
    all_results = []

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            handler_map = {
                ".txt": handle_txt,
                ".pdf": handle_pdf,
                ".docx": handle_docx,
                ".json": handle_json,
                ".csv": handle_csv,
                ".env": handle_env,
                ".log": handle_log,
            }

            for root, _, files in os.walk(temp_dir):
                for filename in files:
                    ext = os.path.splitext(filename)[-1].lower()
                    extracted_file = os.path.join(root, filename)

                    handler = handler_map.get(ext)
                    if handler:
                        try:
                            leaks = handler(extracted_file)
                            all_results.extend(leaks)
                        except Exception as e:
                            print(f"[ZIP ERROR] {filename}: {e}")
                    else:
                        print(f"[ZIP] Skipped unsupported file: {filename}")

    except zipfile.BadZipFile:
        print(f"[!] Invalid ZIP file: {zip_path}")
    except Exception as e:
        print(f"[!] Failed to process ZIP file: {zip_path}: {e}")

    return all_results
