# SafeDrop 🔐

SafeDrop is a sensitive data leak detection tool with support for multiple file formats (`.txt`, `.pdf`, `.docx`, `.json`, `.env`, `.log`, `.csv`, `.zip`). It features:

- 🔍 Regex-based leak detection
- 📊 GUI with file monitoring, summaries, and collapsible analysis panels
- 🧪 Built-in unit tests for all file handlers
- 🔐 AES-256 encrypted logs
- 🧼 Sanitized UI outputs
- 🧱 Modular file structure for easy extensibility

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yashaskl2110/SafeDrop.git
cd SafeDrop
2. Create a virtual environment (optional but recommended)
bash
Copy code
python -m venv venv
venv\Scripts\activate
# On Windows
🧩 Install Dependencies
Install all required packages:

bash
pip install -r requirements.txt
If you don't have a requirements.txt, install manually:

bash
pip install customtkinter pycryptodome python-docx PyPDF2
🔐 Encryption Setup
The app uses AES encryption (via PyCryptodome) to store sensitive values.

The encryption key is automatically generated and saved in a secure key file (key.key).

Logs are stored encrypted separately in .encrypted_log.txt.

🚀 Run the App
bash
Copy code
python gui.py
🧪 Run Tests
Use pytest to run all handler and detection tests:

bash
Copy code
pytest tests/
📁 Folder Structure
Copy code
SafeDrop/
│
├── core/
│   ├── detectors.py
│   ├── utils.py
│
├── handlers/
│   ├── txt_handler.py
│   ├── pdf_handler.py
│   ├── docx_handler.py
│   ├── json_handler.py
│   ├── csv_handler.py
│   ├── env_handler.py
│   ├── log_handler.py
│   ├── zip_handler.py
│
├── gui/
│   └── gui.py
│
├── tests/
│   └── test_*.py
│
├── detection_logs.csv
├── encrypted_log.txt
└── README.md

🙋‍♂️ Author
Built with 💻 by Yashas Kumara Lakawath

---

### ✅ 2. **Create `requirements.txt`**

You can auto-generate it by running:

```bash
pip freeze > requirements.txt
