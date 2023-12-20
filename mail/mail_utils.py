from email.mime.text import MIMEText
from smtplib import (
    SMTP_SSL as SMTP,)  # this invokes the secure SMTP protocol (port 465, uses SSL)
import sys
import os
import re

from config.settings import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS


def send(to, subject, content):

    msg = MIMEText(content, "html")
    msg["Subject"] = subject
    # some SMTP servers will do this automatically, not all
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = to

    conn = SMTP(EMAIL_HOST, 465 if EMAIL_USE_TLS else 587)
    conn.set_debuglevel(False)
    conn.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    try:
        recipients = re.split(r'[,;]\s*', to)
        conn.sendmail(EMAIL_HOST_USER, recipients, msg.as_string())
    finally:
        conn.quit()
