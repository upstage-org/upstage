from multiprocessing import Process
from email.mime.text import MIMEText
from smtplib import (
    SMTP_SSL as SMTP,)  # this invokes the secure SMTP protocol (port 465, uses SSL)
import sys
import os
import re
from config.models import Config
from config.project_globals import DBSession

from config.settings import (EMAIL_HOST, EMAIL_PORT,
    EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST_DISPLAY_NAME,
    ADMIN_EMAIL, ENV_TYPE)

def send_sync(to, subject, content):
    subject_prefix = DBSession.query(Config).filter(Config.name == 'EMAIL_SUBJECT_PREFIX').first()
    msg = MIMEText(content, "html")
    msg["Subject"] = f'{subject_prefix}: {subject}'
    # some SMTP servers will do this automatically, not all
    msg["From"] = f'{EMAIL_HOST_DISPLAY_NAME} <{EMAIL_HOST_USER}>'
    msg["To"] = to
    msg["Bcc"] = ADMIN_EMAIL

    # Always use TLS.
    conn = SMTP(EMAIL_HOST, EMAIL_PORT)
    conn.set_debuglevel(False)
    conn.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    try:
        recipients = re.split(r'[,;]\s*', '{},{}'.format(to, ADMIN_EMAIL))
        conn.sendmail(EMAIL_HOST_USER, recipients, msg.as_string())
    finally:
        conn.quit()

def send(to, subject, content):
    Process(target=send_sync, args=(to, subject, content)).start()
