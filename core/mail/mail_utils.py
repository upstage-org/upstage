# -*- coding: iso8859-15 -*-
import json
import os
import re
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

import threading
import uuid
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate,make_msgid

from time import sleep

import aiosmtplib
import pymongo
import requests
from core.auth.fernet_crypto import decrypt, encrypt
from core.settings.models import Config
from core.project_globals import ScopedSession, app
from config import (
    ACCEPT_EMAIL_HOST,
    ACCEPT_SERVER_SEND_EMAIL_EXTERNAL,
    SUPPORT_EMAILS,
    EMAIL_HOST,
    EMAIL_HOST_DISPLAY_NAME,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_USER,
    EMAIL_PORT,
    EMAIL_TIME_EXPIRED_TOKEN,
    EMAIL_USE_TLS,
    HOSTNAME,
    SEND_EMAIL_SERVER,
    DOMAIN,
)
from core.event_archive.db import get_mongo_token_collection


async def send(to, subject, content, bcc=[], cc=[], filenames=[]):
    if HOSTNAME not in ACCEPT_EMAIL_HOST:
        call_send_email_external_api(subject, content, to, cc, bcc, filenames)
    else:
        msg = create_email(
            to=to, subject=subject, html=content, cc=cc, bcc=bcc, filenames=filenames
        )
        await send_async(msg=msg)


def remove_html(raw_html):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


async def send_async(msg, user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD):
    """
    Contact SMTP server and send Message
    We use this from a local server. TLS is not configured here.
    """
    host = EMAIL_HOST
    port = EMAIL_PORT
    smtp = aiosmtplib.SMTP(hostname=host, port=port, use_tls=EMAIL_USE_TLS)
    await smtp.connect()
    # if EMAIL_USE_TLS:
    #     await smtp.starttls()
    if user:
        await smtp.login(user, password)
    await smtp.send_message(msg)
    await smtp.quit()


def create_email(
    to,
    subject,
    html,
    filenames=[],
    cc=[],
    bcc=[],
    sender=EMAIL_HOST_USER,
    external=False,
):
    """
    Create an email
    """
    msg = MIMEMultipart("fixed")
    # Get Subject prefix in Upstage server
    if not external:
        with ScopedSession() as local_db_session:
            subject_prefix = (
                local_db_session.query(Config)
                .filter(Config.name == "EMAIL_SUBJECT_PREFIX")
                .first()
            )
            if subject_prefix:
                subject = f"{subject_prefix.value}: {subject}"
    msg.preamble = subject

    # Remove empty strings. Not sure how they get here.
    # Remove support admins if they've been listed as recipients.
    # They are implicitly added to all emails. No need to add them again.
    to = [x for x in to if x not in ("", None)]
    cc = [x for x in cc if x not in ("", None)]
    bcc = [x for x in bcc if x not in ("", None)]
    if to and SUPPORT_EMAILS:
        to = list(set(to).difference(set(SUPPORT_EMAILS)))
    if cc and SUPPORT_EMAILS:
        cc = list(set(cc).difference(set(SUPPORT_EMAILS)))
    if bcc and SUPPORT_EMAILS:
        bcc = list(set(bcc).difference(set(SUPPORT_EMAILS)))

    msg["message-id"] = make_msgid(domain=DOMAIN)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg["From"] = f"{EMAIL_HOST_DISPLAY_NAME} <{sender}>"
    msg["To"] = ", ".join(to) if to else ""
    msg["Cc"] = ", ".join(cc) if cc else ""
    if bcc:
        if SUPPORT_EMAILS:
            msg["Bcc"] = ", ".join(SUPPORT_EMAILS) + "," + ", ".join(bcc)
    else:
        if SUPPORT_EMAILS:
            msg["Bcc"] = ", ".join(SUPPORT_EMAILS)

    """
    Multipart message prep. Send both plain text and html, to ensure
    that it can be read.
    """
    msg_alternative = MIMEMultipart("alternative")
    msg_alternative.attach(MIMEText(remove_html(html), "plain", "latin-1"))
    msg_alternative.attach(MIMEText(html, "html", "latin-1"))
    """
    Attach plain and HTML variations of the body to main message content.
    """
    msg.attach(msg_alternative)
    """
    If files exists, attach them to the main message content.
    """
    for filename in filenames:
        with open(filename, "rb") as fp:
            part3 = MIMEApplication(fp.read())
            part3["Content-ID"] = "<{}>".format(os.path.basename(filename))
            part3["Content-Description"] = os.path.basename(filename)
            part3["Content-Disposition"] = 'attachment; filename = "{}"'.format(
                os.path.basename(filename)
            )
            msg.attach(part3)
            msg["X-MS-Has-Attach"] = "Yes"

    return msg


def call_send_email_external_api(subject, body, recipients, cc, bcc, filenames):
    # Get Subject prefix in client server
    with ScopedSession() as local_db_session:
        subject_prefix = (
            local_db_session.query(Config)
            .filter(Config.name == "EMAIL_SUBJECT_PREFIX")
            .first()
        )
        if subject_prefix:
            subject = f"{subject_prefix.value}: {subject}"
    s = requests.Session()
    url = f"{SEND_EMAIL_SERVER}/api/email_graphql/"
    client = get_mongo_token_collection()
    token = client.find_one({}, sort=[("_id", pymongo.DESCENDING)])
    headers = {}
    if token and "token" in token:
        headers["X-Email-Token"] = token["token"]
    data = """
    mutation
    sendEmailExternal($subject: String!, $body: String!, $recipients: [String!], $cc: [String!],$bcc: [String!], $filenames: [String!])
    {
        sendEmailExternal(
            emailInfo: {
                subject: $subject,
                body: $body,
                recipients: $recipients,
                cc: $cc,
                bcc: $bcc,
                filenames:$filenames
            }
        ){
            success
        }
    }
    """
    variables = {
        "subject": subject,
        "body": body,
        "recipients": recipients,
        "cc": cc,
        "bcc": bcc,
        "filenames": filenames,
    }
    result = s.post(
        url=url,
        data={"query": data, "variables": json.dumps(variables)},
        headers=headers,
    )
    if (
        result.ok
        and json.loads(result.text)["data"]["sendEmailExternal"]["success"] == True
    ):
        return True
    else:
        raise Exception(json.loads(result.text))


def save_email_token_client(token):
    client = get_mongo_token_collection()
    # client.delete_many({})
    client.insert_one({"token": token, "expired_date": datetime.utcnow()})


def valid_token(token):
    client = get_mongo_token_collection()
    if client.find_one({"token": decrypt(token)}):
        return True


def generate_email_token_clients():
    while True:
        client = get_mongo_token_collection()
        app.logger.info(f"client_server {ACCEPT_SERVER_SEND_EMAIL_EXTERNAL}")
        # client.delete_many({})

        for client_server in ACCEPT_SERVER_SEND_EMAIL_EXTERNAL:
            live_token = uuid.uuid4().hex
            client.insert_one(
                {
                    "token": live_token,
                    "from_server": client_server,
                    "expired_date": datetime.utcnow(),
                }
            )

            s = requests.Session()
            url = f"{client_server}/api/email_graphql/"
            data = (
                '''
            mutation{
                postToken(token: "'''
                + encrypt(live_token)
                + """"){
                    success
                }
            }
            """
            )

            result = s.post(url=url, data={"query": data})
            if result.ok:
                app.logger.info(f"Send email token to {client_server} successfully")
            else:
                app.logger.info(f"Send email token to {client_server} failed")

        sleep(EMAIL_TIME_EXPIRED_TOKEN)
