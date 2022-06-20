# -*- coding: iso8859-15 -*-
import os
import re
import sys
from time import sleep

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, '..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from config.models import Config
from config.project_globals import ScopedSession, app
from config.settings import (ADMIN_EMAIL, EMAIL_HOST, EMAIL_HOST_DISPLAY_NAME,
                             EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT,
                             EMAIL_USE_TLS, MONGO_DB, MONGODB_COLLECTION_EMAIL)
from event_archive.db import build_mongo_client


def send(to, subject, content, bcc=[], cc=[], filenames=[]):
    push_mail_info_to_queue({'sender': EMAIL_HOST_USER, 'password': EMAIL_HOST_PASSWORD,
                             'subject': subject, 'body': content, 'recipients': to,
                             'bcc': bcc, 'cc': cc, 'filenames': filenames})


def remove_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


async def send_async(msg, user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD):
    '''
    Contact SMTP server and send Message
    We use this from a local server. TLS is not configured here.
    '''
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


def create_email(to, subject, html, filenames=[], cc=[], bcc=[], sender=EMAIL_HOST_USER):
    '''
    Create an email
    '''
    msg = MIMEMultipart('fixed')
    with ScopedSession() as local_db_session:
        subject_prefix = local_db_session.query(Config).filter(
            Config.name == 'EMAIL_SUBJECT_PREFIX').first().value
    if subject_prefix:
        subject = f'{subject_prefix}: {subject}'
    msg.preamble = subject
    msg['Subject'] = subject
    msg['From'] = f'{EMAIL_HOST_DISPLAY_NAME} <{sender}>'
    msg['To'] = ', '.join(to)
    if len(cc):
        msg['Cc'] = ', '.join(cc)
    if len(bcc):
        msg['Bcc'] = ADMIN_EMAIL + ',' + ', '.join(bcc)
    else:
        ADMIN_EMAIL
    '''
    Multipart message prep. Send both plain text and html, to ensure
    that it can be read.
    '''
    msg_alternative = MIMEMultipart('alternative')
    msg_alternative.attach(MIMEText(remove_html(html), 'plain', 'utf-8'))
    msg_alternative.attach(MIMEText(html, 'html', 'iso8859-15'))
    '''
    Attach plain and HTML variations of the body to main message content.
    '''
    msg.attach(msg_alternative)
    '''
    If files exists, attach them to the main message content.
    '''
    for filename in filenames:
        with open(filename, 'rb') as fp:
            part3 = MIMEApplication(fp.read())
            part3['Content-ID'] = '<{}>'.format(os.path.basename(filename))
            part3['Content-Description'] = os.path.basename(filename)
            part3['Content-Disposition'] = 'attachment; filename = "{}"'.format(
                os.path.basename(filename))
            msg.attach(part3)
            msg['X-MS-Has-Attach'] = 'Yes'

    return msg


def push_mail_info_to_queue(email_info):
    '''
    Push email to queue
    '''
    try:
        client = build_mongo_client()
        db = client[MONGO_DB]
        db[MONGODB_COLLECTION_EMAIL].insert_one(
            email_info if isinstance(email_info, dict) else email_info.__dict__)
        client.close()
        app.logger('Push email success')
    except Exception as e:
        app.logger.error(f'Failed to push email to queue: {e}')


async def send_mail_from_queue():
    '''
    Pop email from queue and send
    '''
    app.logger.info('Send email from queue queue process!')
    client = build_mongo_client()
    db = client[MONGO_DB]
    queue = db[MONGODB_COLLECTION_EMAIL]
    mail = queue.find_one_and_delete({})
    while mail:
        try:
            if mail:
                sender = mail['sender']if mail['sender'] else EMAIL_HOST_USER
                password = mail['password']if mail['password'] else EMAIL_HOST_PASSWORD
                subject = mail['subject']
                body = mail['body']
                recipients = mail['recipients']
                bcc = mail['bcc']
                cc = mail['cc']
                filenames = mail['filenames']
                msg = create_email(to=recipients, subject=subject,
                                   html=body, cc=cc, bcc=bcc, sender=sender,filenames=filenames)
                await send_async(msg=msg, user=sender, password=password)
        except Exception as e:
            app.logger.error(f'Failed to send email: {e}')
            sleep(5)
            queue.insert_one(mail)
        mail = queue.find_one_and_delete({})
