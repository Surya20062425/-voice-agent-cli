#!/usr/bin/env python3
"""Demo: send a hello email via Gmail SMTP.

Fill in the three config values below, then run:
    python send_demo_mail.py

Requirements:
    - A Gmail account (or any SMTP provider)
    - 2-Step Verification enabled on the account
    - An App Password (not your regular password)
      Generate at: https://myaccount.google.com/apppasswords
"""

import smtplib
from email.mime.text import MIMEText

# ── Config ────────────────────────────────────────────────────────────────
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587
SENDER      = "b.7993974026@gmail.com"       # ← your Gmail address
APP_PASSWORD = "your-16-char-app-password"   # ← generate at myaccount.google.com/apppasswords
RECIPIENT   = "b.7993974026@gmail.com"       # ← where to send (can be same as sender)
# ──────────────────────────────────────────────────────────────────────────

msg = MIMEText(
    "Hello!\n\n"
    "This is a demo email sent from Hermes Agent.\n"
    "Ponytail skill is installed. Voice agent CLI is ready.\n\n"
    "Cheers,\nHermes"
)
msg["Subject"] = "Hello from Hermes Agent — Demo"
msg["From"]    = SENDER
msg["To"]      = RECIPIENT

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
        s.starttls()
        s.login(SENDER, APP_PASSWORD)
        s.sendmail(SENDER, [RECIPIENT], msg.as_string())
    print("✓ Demo email sent successfully to", RECIPIENT)
except Exception as e:
    print("✗ Failed:", e)
    print("\nFix the config values at the top of this script and retry.")
