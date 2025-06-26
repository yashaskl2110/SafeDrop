import re
from core.utils import load_allowlist

# Load allowlist once
allowlist = load_allowlist()

# Precompiled leak pattern using named groups for each sensitive type
leak_pattern = re.compile(r"""(?ix)
    (?P<url_pass>https?://[^\s]+:[^\s]+) |
    (?P<email_pass>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}[:=][^\s]+) |
    (?P<api_key>(?:api|secret|key|bearer)[\s:=]+["']?[A-Za-z0-9_\-]{16,}["']?) |
    (?P<aws_key>AKIA[0-9A-Z]{16,}) |
    (?P<google_key>AIza[0-9A-Za-z\-_]{20,}) |
    (?P<slack_hook>https://hooks\.slack\.com/services/[A-Za-z0-9]+/[A-Za-z0-9]+/[A-Za-z0-9]+) |
    (?P<env_secret>SECRET_KEY["']?[:=]["']?sk_(live|test)_[A-Za-z0-9]{10,}["']?) |
    (?P<env_emailpass>EMAIL_PASS["']?\s*[:=]\s*["']?.{4,}["']?) |
    (?P<env_dbpass>DB_PASS["']?\s*[:=]\s*["']?.{4,}["']?) |
    (?P<env_apikey>API_KEY["']?\s*[:=]\s*["']?.{8,}["']?) |
    (?P<username_key>\b(user(name)?|email)\b\s*[:=]\s*[^\s]+) |
    (?P<password_key>\b(pass(word)?)\b\s*[:=]\s*[^\s]+)
""")

def detect_leaks(text):
    """Search the input text for sensitive patterns, excluding any allowlisted values."""
    results = []
    for match in leak_pattern.finditer(text):
        for label, value in match.groupdict().items():
            if value:
                # Extract just the value part (e.g., from 'key=value' to 'value') for allowlist comparison
                val_only = value.split('=', 1)[-1].strip() if '=' in value else value
                if val_only not in allowlist:
                    results.append((label, value))
    return results
