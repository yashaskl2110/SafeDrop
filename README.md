CloudSentinel ☁️🔍

Multi-Cloud Sensitive Data Leak Detection with GUI Dashboard

CloudSentinel is a desktop security tool for scanning AWS S3 buckets and Azure Blob containers for sensitive data leaks (API keys, passwords, tokens, secrets, etc.). It features encrypted logging, developer attribution, file decay tracking, leak fingerprinting, and a cross-cloud GUI for interactive analysis.

🧩 Features

✅ Multi-Cloud Support: AWS S3 + Azure Blob Storage scanning

🔍 Regex-based leak detection across .env, .txt, .json, .log, .csv and more

📊 GUI Dashboard:

Leak file, leak type, masked value

Click any row for detailed analysis (developer info, file age, timestamps, encrypted value)

🔐 AES-256 Encrypted Logs: Leak data securely stored in encrypted_logs.csv

🧑‍💻 Developer Fingerprinting: Identify which developer introduced the leak

⏳ File Decay Tracking: First seen, last modified, age in days

🆔 Leak Fingerprinting: Unique IDs for leak entries to avoid duplicates

🔄 Cross-Cloud View: Analyze AWS and Azure leaks in one interface

🖥 Offline Log Review: View encrypted logs without running scans

🖥️ Screenshots
Azure Leak Scan	Decrypt All Logs

	
AWS Leak Scan	Empty Dashboard

	
Azure Blob Container	AWS S3 Bucket

	
⚙️ Setup & Installation
📦 Clone the Repo
git clone https://github.com/YOUR_USERNAME/CloudSentinel.git
cd CloudSentinel

🛠 Create a Virtual Environment (Recommended)
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

📥 Install Dependencies
pip install -r requirements.txt

🔑 Configuration

Create a .env file in the root folder:

# AWS credentials
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_region

# Azure credentials
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account
AZURE_STORAGE_ACCOUNT_KEY=your_account_key

🚀 Running the App
🖱 GUI Mode
python gui/main_gui.py

🗂️ Project Structure
CloudSentinel/
│
├── gui/
│   ├── main_gui.py           # Main GUI entry point
│   ├── decrypt_popup.py      # Decrypt all logs popup
│
├── scanners/
│   ├── aws_scanner.py        # AWS S3 scanning logic
│   ├── azure_scanner.py      # Azure Blob scanning logic
│
├── utils/
│   ├── dev_fingerprint.py    # Developer identity tracking
│   ├── decay_log.py          # File decay tracking
│
├── reports/
│   ├── formatter.py          # Logging & encryption
│
├── requirements.txt
├── .env
└── README.md

🧠 How It Works

Select a cloud provider (AWS or Azure) in the GUI.

Enter the bucket or container name.

Click Start Scan → leaks appear in the dashboard in real-time.

Click a leak entry → view details in the Analysis Panel:

Leak type

Developer fingerprint

First seen / last modified / file age

Encrypted value

Optionally click Decrypt All Logs → enter your key to see full values.

🔒 Leak Types Detected

aws_key: AWS Access Key

secret_key: Secrets in .env

db_pass: Database password

password: Generic password

api_key: Generic API Key / Token

google_key: Google API Key

slack_hook: Slack Webhook URL

url_pass: URLs containing passwords

👨‍💻 Author

Built with ☁️❤️ by Yashas Kumara Lakawath

📄 License

This project is licensed under the MIT License. See LICENSE for details.
