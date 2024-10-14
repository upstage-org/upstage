from asyncio import sleep
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
import json
import os
import re
import uuid
import requests
import pymongo
import aiosmtplib
from global_config import (
    ACCEPT_SERVER_SEND_EMAIL_EXTERNAL,
    DOMAIN,
    EMAIL_HOST,
    EMAIL_HOST_DISPLAY_NAME,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_USER,
    EMAIL_PORT,
    EMAIL_TIME_EXPIRED_TOKEN,
    EMAIL_USE_TLS,
    ENV_TYPE,
    FULL_DOMAIN,
    SEND_EMAIL_SERVER,
    SUPPORT_EMAILS,
    ScopedSession,
)
from event_archive.config.mongodb import get_mongo_token_collection
from upstage_options.db_models.config import ConfigModel


async def send(to, subject, content, bcc=[], cc=[], filenames=[]):
    msg = create_email(
        to=to, subject=subject, html=content, cc=cc, bcc=bcc, filenames=filenames
    )

    to = list(set(to).difference(set(SUPPORT_EMAILS)))
    if ENV_TYPE != "test" and len(to):
        await send_async(msg=msg)


def call_send_email_external_api(subject, body, recipients, cc, bcc, filenames):
    with ScopedSession() as local_db_session:
        subject_prefix = (
            local_db_session.query(ConfigModel)
            .filter(ConfigModel.name == "EMAIL_SUBJECT_PREFIX")
            .first()
        )
        if subject_prefix:
            subject = f"{subject_prefix.value}: {subject}"

        s = requests.Session()
        url = f"{SEND_EMAIL_SERVER}/api/email_graphql/"
        client = get_mongo_token_collection()
        token = client.find_one(
            {"from_server": FULL_DOMAIN}, sort=[("_id", pymongo.DESCENDING)]
        )

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
        return headers["X-Email-Token"]
    else:
        raise Exception(json.loads(result.text))


def save_email_token_client(token, _):
    client = get_mongo_token_collection()
    # client.delete_many({})
    client.insert_one({"token": token, "expired_date": datetime.now()})


def valid_token(token):
    client = get_mongo_token_collection()
    # if client.find_one({"token": decrypt(token)}):
    if client.find_one({"token": token}):
        return True


async def generate_email_token_clients():
    while True:
        client = get_mongo_token_collection()
        """
        Only generate and insert new tokens locally.
        The remote site will have access to this mongodb server, and will be able
        to look them up directly.
        """
        for client_server in ACCEPT_SERVER_SEND_EMAIL_EXTERNAL:
            live_token = uuid.uuid4().hex
            client.insert_one(
                {
                    "token": live_token,
                    "from_server": client_server,
                    "expired_date": datetime.now(),
                }
            )
        await sleep(EMAIL_TIME_EXPIRED_TOKEN)


async def send_async(msg, user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD):
    """
    Contact SMTP server and send Message
    We use this from a local server. TLS is not configured here.
    """
    host = EMAIL_HOST
    port = EMAIL_PORT
    smtp = aiosmtplib.SMTP(hostname=host, port=int(port), use_tls=EMAIL_USE_TLS)
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
                local_db_session.query(ConfigModel)
                .filter(ConfigModel.name == "EMAIL_SUBJECT_PREFIX")
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

    msg["Subject"] = subject
    msg["message-id"] = make_msgid(domain=DOMAIN)
    msg["Date"] = formatdate(localtime=True)
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


def remove_html(raw_html):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext
