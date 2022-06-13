import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config.settings import EMAIL_TIME_TRIGGER_SECONDS

from mail.mail_utils import send_mail_from_queue

if __name__ == "__main__":
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(send_mail_from_queue, "interval", seconds=EMAIL_TIME_TRIGGER_SECONDS)
        scheduler.start()
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        logging.error(e)
