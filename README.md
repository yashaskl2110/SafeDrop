🔐 SafeDrop: Sensitive Data Leak Detection Tool
SafeDrop is a powerful and extensible desktop-based security utility that automatically scans files for sensitive information leaks using custom regex-based patterns, real-time file monitoring, encryption, and a clean, user-friendly GUI.

🚀 Overview
SafeDrop is designed to monitor folders in real-time and detect potential leaks of confidential data, such as:

API keys

AWS credentials

Google API keys

Email:Password combos

Webhooks

Environment secrets

Hardcoded credentials (username/password)

Slack tokens and URLs

Secrets in URLs

It supports automatic quarantine, sanitized UI display, AES encryption for secure logging, and includes full unit testing coverage.

🧱 Key Features
Feature	Description
🔍 Regex-based Detection	Detects sensitive patterns across various formats using carefully tuned regex patterns with named groups.
📁 Multi-file Support	Handles .txt, .pdf, .docx, .json, .csv, .log, .env, .zip.
🖥️ GUI (Tkinter + CustomTkinter)	Includes folder selection, live status, alert popups, theme toggle, navigation, and scrollable tables.
📊 Analysis Summary Panel	Collapsible panel summarizing leak types and counts.
🧼 Sanitized Logging & Display	All leaks shown in GUI and CSV logs are masked (e.g., ****ssword) to avoid accidental exposure.
🔐 Encrypted Raw Log (AES-256)	Full leak values are stored securely in logs/encrypted_leaks.log using cryptography.Fernet.
📦 Quarantine System	Automatically moves flagged files to a quarantine/ folder and provides a button to open it.
✅ Allowlist Support	Ignore known safe strings or values (e.g., placeholder API keys) by listing them in core/allowlist.txt.
🧪 Unit Tests	Tests written using pytest for all handlers and utility modules with mocking and temp files.
🧱 Modular Codebase	Separated into core/, handlers/, tests/, and GUI for readability and easy maintenance.
🌙 Dark Mode Support	GUI includes light/dark mode toggle.
⏭ Pagination in GUI	Leak logs are paginated with navigation to improve GUI performance and clarity.
🔁 Zip File Support	Automatically extracts and scans supported files inside .zip archives.
🎯 Lightweight Dependencies	Does not require any external database or cloud integration — fully local and offline-capable.

🧠 Technologies Used
Python 3.x

CustomTkinter / tkinter – GUI

cryptography – AES-256 encryption (Fernet)

PyPDF2 / pdfplumber – PDF text extraction

python-docx – .docx file parsing

watchdog – Real-time folder monitoring

pytest – Testing framework

os, shutil, zipfile, tempfile, json, csv – File system and data handling

📁 Project Structure
graphql
Copy
Edit
SafeDrop/
│
├── core/
│   ├── detectors.py            # Regex pattern matching + allowlist
│   ├── utils.py                # Sanitization, logging, encryption helpers
│   ├── watcher.py              # Real-time file monitoring via watchdog
│   ├── decrypt_logs.py         # CLI tool to decrypt AES logs
│   ├── secret.key              # Auto-generated AES key (never shared)
│
├── handlers/                   # Modular file-specific logic
│   ├── txt_handler.py
│   ├── pdf_handler.py
│   ├── docx_handler.py
│   ├── json_handler.py
│   ├── csv_handler.py
│   ├── env_handler.py
│   ├── log_handler.py
│   ├── zip_handler.py
│   └── __init__.py
│
├── gui.py                      # Tkinter-based user interface
├── logs/
│   ├── detections_log.csv      # UI + CSV sanitized log
│   ├── encrypted_leaks.log     # AES-256 encrypted log of full leaks
│
├── quarantine/                 # Folder for quarantined files
├── requirements.txt
├── tests/
│   ├── test_utils.py           # Tests for sanitization, logging, encryption
│   ├── test_txt_handler.py     # All file handler tests (mocked)
│   └── ...                     # Additional tests (json, env, zip, etc.)
└── README.md
⚙️ Setup & Installation
Clone the Repository

bash
Copy
Edit
git clone https://github.com/yashaskl2110/SafeDrop.git
cd SafeDrop
Create Virtual Environment (Optional but Recommended)

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/Mac
Install Requirements

bash
Copy
Edit
pip install -r requirements.txt
If you don’t have requirements.txt, install manually:

bash
Copy
Edit
pip install customtkinter watchdog cryptography pdfplumber python-docx PyPDF2
Run the App

bash
Copy
Edit
python gui.py
🔐 Encryption & Decryption
A secret AES key is auto-generated (core/secret.key) on first run.

Encrypted logs are written to logs/encrypted_leaks.log.

To decrypt:

bash
Copy
Edit
python core/decrypt_logs.py
✅ Unit Testing
To run all tests:

bash
Copy
Edit
pytest tests/
Includes:

Sanitization & Encryption tests

Handler tests (txt, pdf, json, env, csv, log, zip)

Allowlist testing

📝 How Quarantine Works
When a file contains a leak, it’s automatically moved to quarantine/ folder.

Users are notified via popup.

GUI includes a button to open the quarantine folder in the system file explorer.

🧾 Logging Behavior
Type	File	Contents
Sanitized Log	logs/detections_log.csv	Timestamp, file path, label, masked value
Encrypted Log	logs/encrypted_leaks.log	AES-encrypted full raw value
Allowlist	core/allowlist.txt	Skips matching strings from being flagged

✨ Demo Scenarios
Add a .env file with DB_PASS=123456

Place a .pdf file containing user@example.com:supersecret

Drop a .zip archive with mixed file types

🟢 SafeDrop will:

Detect and mask the values

Show sanitized entries in GUI

Quarantine the files

Save encrypted logs securely

🙋‍♂️ Author
Made with 💻 by Yashas Kumara Lakawath
