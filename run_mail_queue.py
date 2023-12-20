import asyncio
import logging
import pprint

import arrow

from config.project_globals import app
from config.settings import EMAIL_TIME_TRIGGER_SECONDS
from mail.mail_utils import send_mail_from_queue


class AsyncProcesses(object):
    def __init__(self, logger, total_sleep_time, function_list):
        self.logger = logger
        self.total_sleep_time = total_sleep_time
        self.function_list = function_list

    def wait_for_all_then_repeat(self):
        async def rerun_these_forever(loop):
            start_time = arrow.utcnow().timestamp()
            while True:
                '''
                Subtract the run time from the total sleep time, so we don't slip.
                '''
                sleep_time = self.total_sleep_time - \
                    (arrow.utcnow().timestamp() - start_time)
                if sleep_time <= 0:
                    self.logger.error(
                        "Timer diff was negative, sleeping for 30 seconds")
                    sleep_time = 30
                await asyncio.sleep(sleep_time)
                self.logger.info(
                    f"Rerunning these processes: {pprint.pformat([x for x in self.function_list])}")
                start_time = arrow.utcnow().timestamp()
                await asyncio.wait(
                    [loop.create_task(f()) for f in self.function_list]
                )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(rerun_these_forever(loop))
        loop.close()

    def run_all(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.wait_for_all_then_repeat())
        loop.run_forever()


if __name__ == "__main__":
    try:
        proc = AsyncProcesses(function_list=[send_mail_from_queue],
                              total_sleep_time=EMAIL_TIME_TRIGGER_SECONDS,
                              logger=app.logger)
        proc.run_all()
    except Exception as e:
        logging.error(e)
