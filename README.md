# SafeDrop 🔐

**Sensitive Data Leak Detector with Multi‑File Support & Desktop GUI**
Detect API keys, passwords, emails, webhooks and more across folders in real time. SafeDrop monitors files, quarantines suspicious items, and keeps **sanitized CSV logs** plus **AES‑encrypted logs** for secure auditing.

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#usage">Usage</a> •
  <a href="#logs--reports">Logs & Reports</a> •
  <a href="#quarantine">Quarantine</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#troubleshooting">Troubleshooting</a>
</p>

---

## Highlights

* ✅ **Multi‑format scanning**: `.txt`, `.pdf`, `.docx`, `.json`, `.env`, `.log`, `.csv`, `.zip`
* 🔍 **Robust regex detection** for API keys (AWS/Google/etc.), emails, passwords, URLs with creds, Slack webhooks, and common `.env` secrets
* 🖥️ **Desktop GUI** (CustomTkinter) with real‑time results
* 🧼 **Sanitized display** (masked values) to avoid leaking more data in the UI
* 🔐 **AES‑256 encrypted logs** for secure, later decryption
* 🧰 **Quarantine mode**: suspicious files moved to a safe folder
* 📊 **Analysis panel**: per‑file details, developer/fingerprint info\* and decay tracking\*
* 🌗 **Dark/Light theme** toggle
* 🧪 **Unit‑tested handlers** and modular scanners (extensible)

> \*Optional/advanced depending on your current branch.

---

## Folder Structure (typical)

```
SafeDrop/
├─ gui/
│  └─ main_gui.py                # Desktop app entrypoint
├─ scanners/
│  ├─ aws_scanner.py
│  └─ azure_scanner.py
├─ reports/
│  ├─ formatter.py               # Writes plain & encrypted logs
│  └─ detection_logs.csv         # Sanitized
├─ utils/                        # helpers, crypto, fingerprints, decay tracking
├─ quarantine/                   # quarantined files (auto‑created)
├─ assets/
│  └─ screenshots/               # images used in README
├─ run_safedrop.py               # Convenience launcher (GUI)
├─ main.py                       # CLI runner (optional)
├─ requirements.txt
└─ README.md
```

---

## Quick Start

### 1) Clone

```bash
# HTTPS
git clone https://github.com/<you>/SafeDrop.git
cd SafeDrop
```

### 2) Create & activate a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Launch the GUI

```bash
python run_safedrop.py
```

> If your entrypoint differs, start via `python -m gui.main_gui` instead.

---

## Usage

### GUI Workflow

1. Click **Select Folder** and choose the directory to monitor (subfolders included).
2. Press **Start** to begin scanning in real time.
3. When a leak is found, you’ll see a **popup alert**; the file can be **quarantined** automatically.
4. Results appear in the top table (masked values). Click a row to open the **Analysis Panel** for details.
5. Use **Open Quarantine Folder** to inspect isolated files.

### CLI (optional)

```bash
# Example: scan an AWS bucket or Azure container from the CLI
python main.py --provider aws --bucket your-bucket-name
python main.py --provider azure --container your-container-name
```

> CLI output is written into the same report files as the GUI.

---

## Logs & Reports

* **Sanitized CSV**: `reports/detection_logs.csv`
  Masked values (e.g. `********xyz`) for safe sharing.

* **Encrypted CSV**: `reports/encrypted_logs.csv`
  AES‑256 encrypted entries. A key file (e.g. `.encryption.key`) is used to encrypt/decrypt.

* **Decrypting**
  Use the **Decrypt Logs** button in the GUI, or run your decrypt helper:

  ```bash
  python decrypt_logs.py --key .encryption.key --in reports/encrypted_logs.csv --out reports/decrypted_logs.csv
  ```

> Keep the key file safe and **out of version control**. Add it to `.gitignore`.

---

## Quarantine

* Quarantined files are moved to the `quarantine/` folder.
* The GUI provides a one‑click shortcut: **Open Quarantine Folder**.
* Restoring files is manual—inspect first, then move them out if they’re truly safe.

---

## Screenshots

| ![1](./screenshots/1.png)                                                                  | ![2](./screenshots/2.png)                                            |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| **Dashboard:** GUI running with folder selection, theme toggle, and active leak scan view. | **Folder Selection to Monitor:** Selection of the folder that needs to be monitored. |

| ![3](./screenshots/3.png)                                                  | ![4](./screenshots/4.png)                                                     |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Leak Alert Popup & Quarantine Confirmation:** Triggered when sensitive content is found in a file. File has been quarantined to protect the system. | **Leak Summary Panel:** Shows grouped summary of all detected leaks. |

| ![5](./screenshots/5.png)                                      | ![6](./screenshots/6.png)                                       | ![7](./screenshots/7.png)                                     |
| -------------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------- |
| **Quarantine Folder View:** Shows the isolated sensitive file. | **Encrypted Log File:** AES‑256 encrypted log of leak metadata. | **Sanitized CSV Log:** Human-readable log with masked values. |

| ![8](./screenshots/8.png)                                                                    |
| -------------------------------------------------------------------------------------------- |
| **Terminal Output (CLI mode):** Shows active scanning and encryption process in CLI if used. |

---

## Configuration Tips

* **Add screenshots** to `assets/screenshots/` and update paths in this README.
* **Ignore generated files** by adding the following to `.gitignore`:

  ```
  .venv/
  __pycache__/
  *.pyc
  quarantine/
  reports/*.csv
  .encryption.key
  .env
  ```
* **Environment variables** (if used) go in `.env` (not committed).

---

## Troubleshooting

* **Pip errors / missing wheels** → Upgrade pip: `python -m pip install --upgrade pip`
* **tkinter not found (Linux)** → Install Tk libs: `sudo apt-get install python3-tk`
* **PDF/DOCX reading fails** → Ensure `PyPDF2` and `python-docx` are installed.
* **Nothing detected** → Test with seeded samples (fake keys) and confirm the folder is correct.
* **Azure/AWS logs missing** → Verify the corresponding scanner returns results and `reports/formatter.py` is called for **both** providers.

---

## Roadmap

* [ ] Pluggable detection rules by file type
* [ ] Batch decrypt inside GUI
* [ ] Export filtered views (by provider/file/leak type)
* [ ] Rule tuner with test corpus

---

## Contributing

PRs are welcome! Please open an issue first to discuss major changes. Keep the GUI responsive and avoid leaking raw secrets in plaintext.

---

## License

This project is licensed under the **MIT License**.
