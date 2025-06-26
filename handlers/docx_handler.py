import docx
from core.detectors import detect_leaks
from core.utils import log_detection, encrypt_and_log_raw

def handle_docx(file_path):
    try:
        doc = docx.Document(file_path)
        content = "\n".join(para.text for para in doc.paragraphs)

        leaks = detect_leaks(content)
        for label, match in leaks:
            print(f"[{label}] {match}")
            log_detection(file_path, label, match)
            encrypt_and_log_raw(file_path, label, match)

        return leaks

    except Exception as e:
        print(f"[DOCX ERROR] {file_path}: {e}")
        return []
