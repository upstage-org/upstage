# -*- coding: iso8859-15 -*-
import os,sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from loguru import logger
from multiprocessing import cpu_count

#from scheduler_config import project_config as config

# Socket Path
bind = 'unix:/home/upstage/socket/gunicorn.sock'


# Worker Options
workers = cpu_count() + 1
worker_class = 'run.workers.UvicornWorker'

# Logging Options
logger.remove()
logger.add(
    sys.stderr,
    colorize=True,
    format="<blue>{time}</blue> <level>{message}</level>",
)
logger.add("/var/log/upstage/access.log", rotation="500 MB", enqueue=True, backtrace=True, diagnose=True)
logger.add("/var/log/upstage/error.log", rotation="500 MB", enqueue=True, backtrace=True, diagnose=True)
logger.add("/var/log/upstage/log.json", rotation="500 MB", enqueue=True, backtrace=True, diagnose=True, serialize=True)
logger.level('DEBUG')
